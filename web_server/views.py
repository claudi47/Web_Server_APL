import datetime
import requests

from apscheduler.jobstores.base import JobLookupError
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from web_server.models import Search, BetData
from web_server.serializers import UserSerializer, SearchSerializer, BetDataSerializer
from web_server.transaction_scheduler import transaction_scheduler


@transaction.atomic
def rollback_function(search_id):
    # this is a query where we select the rows with that search_id and after we delete them
    BetData.objects.filter(search=search_id).delete()
    Search.objects.get(pk=search_id).delete() # delete of entry search with that primary key

# In Django, a view determines the content of a web page
# views.py is where we handle the request/response logic of our web server

# Guarantee the atomic execution of a given block, adding a context manager to the underneath wrapper (Api_View)
# this ctx manager manages the workflow of the transaction, checking if the savepoints are valid (no error/exception)
# if this condition is true, the __exit__ func will have "exc_type" == None and the transaction block will be commited
# if this condition is false, the entire transaction is aborted and a rollback is executed by the ctx manager
@transaction.atomic
@api_view(['POST']) # returns a decorator that transforms the function in a APIView REST class
def bet_data_view(request):

    user_identifier = request.data['user_id']
    username = request.data['username']
    sid = transaction.savepoint()

    user = UserSerializer(data={'username': username, 'user_identifier': user_identifier})
    if user.is_valid(): # verifies if the user is already created
        user.save()

    csv_url = ''
    search = SearchSerializer(data={'csv_url': csv_url, 'user': user_identifier})
    if search.is_valid():
        search_instance = search.save()
        bet_data_list = request.data['data']
        for element in bet_data_list:
            # **element passes the entire content of the dictionary where bet_data are present
            bet_data = BetDataSerializer(data={**element, 'search':search_instance.pk})
            if bet_data.is_valid():
                bet_data.save()
            else:
                transaction.savepoint_rollback(sid)
                return Response('Error!', status=status.HTTP_400_BAD_REQUEST)

        response_from_cpp = requests.post("http://localhost:3000", json=bet_data_list)
        if not response_from_cpp.ok:
            transaction.savepoint_rollback(sid)
            return Response('Error!', status=status.HTTP_400_BAD_REQUEST)
        else:
            associated_search_data = {'search_id': search_instance.pk, 'filename': response_from_cpp.text}
            # Adds the given job to the job list and wakes up the scheduler if it's already running.
            # params: 1) function to be scheduled, 2) 'date' is the trigger type that indicates when the job must be
            # executed, 3) args are the params to pass to the 1), 4) id assigned to the job
            transaction_scheduler.add_job(rollback_function, 'date',
                                          run_date=datetime.datetime.now()+datetime.timedelta(seconds=5),
                                          args=[search_instance.pk],
                                          id=str(search_instance.pk))
            return Response(associated_search_data, status=status.HTTP_200_OK)

    transaction.savepoint_rollback(sid)
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
        except JobLookupError: # when the job is not found
            return Response('Job removal failed', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        updated_search.save()
        return Response('Csv transaction success', status=status.HTTP_201_CREATED)
    else:
        return Response('Csv transaction failed, data not valid', status=status.HTTP_400_BAD_REQUEST)


