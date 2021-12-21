import datetime
import requests

from apscheduler.jobstores.base import JobLookupError
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from web_server.models import Search, BetData, User, Settings
from web_server.serializers import UserSerializer, SearchSerializer, BetDataSerializer, SettingsDataSerializer
from web_server.setting_category import GENERAL
from web_server.transaction_scheduler import transaction_scheduler


def rollback_function(search_id):
    # this is a query where we select the rows with that search_id and after we delete them
    BetData.objects.filter(search=search_id).delete()
    Search.objects.get(pk=search_id).delete()  # delete of entry search with that primary key


# In Django, a view determines the content of a web page
# views.py is where we handle the request/response logic of our web server

@api_view(['POST'])  # returns a decorator that transforms the function in a APIView REST class
def bet_data_view(request):
    user_identifier = request.data['user_id']
    username = request.data['username']
    try:
        user = UserSerializer(data={'username': username, 'user_identifier': user_identifier})
        if user.is_valid():  # verifies if the user is already created
            user.save()

        csv_url = ''
        search = SearchSerializer(data={'csv_url': csv_url, 'user': user_identifier})
        if search.is_valid():
            search_instance = search.save()
            bet_data_list = request.data['data']
            for element in bet_data_list:
                # **element passes the entire content of the dictionary where bet_data are present
                bet_data = BetDataSerializer(data={**element, 'search': search_instance.pk})
                if bet_data.is_valid():
                    bet_data.save()
                else:
                    rollback_function(search_instance.pk)
                    return Response('Error!', status=status.HTTP_400_BAD_REQUEST)

            response_from_cpp = requests.post("http://localhost:3000", json=bet_data_list)
            if not response_from_cpp.ok:
                rollback_function(search_instance.pk)
                return Response('Error!', status=status.HTTP_400_BAD_REQUEST)
            else:
                associated_search_data = {'search_id': search_instance.pk, 'filename': response_from_cpp.text}
                # Adds the given job to the job list and wakes up the scheduler if it's already running.
                # params: 1) function to be scheduled, 2) 'date' is the trigger type that indicates when the job must be
                # executed, 3) args are the params to pass to the 1), 4) id assigned to the job
                transaction_scheduler.add_job(rollback_function, 'date',
                                              run_date=datetime.datetime.now() + datetime.timedelta(seconds=5),
                                              args=[search_instance.pk],
                                              id=str(search_instance.pk))
                return Response(associated_search_data, status=status.HTTP_200_OK)
    except:
        try:
            rollback_function(search_instance.pk)
        except:
            pass

    return Response('Error!', status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def url_csv_view(request):
    csv_url = request.data['url_csv']
    search_id = request.data['search_id']
    updated_search = SearchSerializer(Search.objects.get(pk=int(search_id)), data={'csv_url': csv_url}, partial=True)
    if updated_search.is_valid():
        try:
            # if in 5 seconds the job is removed, the rollback function is not called
            transaction_scheduler.remove_job(str(search_id))
        except JobLookupError:  # when the job is not found
            return Response('Job removal failed', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        updated_search.save()
        return Response('Csv transaction success', status=status.HTTP_201_CREATED)
    else:
        return Response('Csv transaction failed, data not valid', status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def stats_view(request):
    match request.query_params['stat']:
        case "1":
            stat_from_cpp = requests.get("http://localhost:3000/stats?stat=1")
            if not stat_from_cpp.ok:
                return Response('Bad Response from CPP', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return HttpResponse(stat_from_cpp.text, status=status.HTTP_200_OK)
    return Response("wow", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def settings_view(request):
    settings_serializer = SettingsDataSerializer(data=request.data)
    if settings_serializer.is_valid():
        if settings_serializer.data['max_researches'] is not None:
            if settings_serializer.data['bool_for_all'] is True:
                User.objects.update(max_research=settings_serializer['max_researches'])
            elif settings_serializer.data['username_research'] is not None:
                User.objects.filter(username=settings_serializer.data['username_research']).update(
                    max_research=settings_serializer.data['max_researches'])
        if settings_serializer.data['period_of_suspension'] is not None and settings_serializer.data[
            'user_suspended'] is not None:
            User.objects.filter(username=settings_serializer.data['user_suspended']).update(
                ban_period=settings_serializer.data['period_of_suspension'])
        Settings.objects.filter(pk=GENERAL).update(goldbet_research=settings_serializer.data['bool_toggle_goldbet'],
                                                   bwin_research=settings_serializer.data['bool_toggle_bwin'])
        return Response("Success!", status=status.HTTP_200_OK)
    else:
        return Response(settings_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
