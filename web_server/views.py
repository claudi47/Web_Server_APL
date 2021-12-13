import requests
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from web_server.serializers import UserSerializer, SearchSerializer, BetDataSerializer


# In Django, a view determines the content of a web page
# views.py is where we handle the request/response logic of our web server

# Guarantee the atomic execution of a given block, adding a context manager to the underneath wrapper (Api_View)
# this ctx manager manages the workflow of the transaction, checking if the savepoints are valid (no error/exception)
# if this condition is true, the __exit__ func will have "exc_type" == None and the transaction block will be commited
# if this condition is false, the entire transaction is aborted and a rollback is executed by the ctx manager
@transaction.atomic
@api_view(['POST']) # returns a decorator that transforms the function in a APIView REST class
def bet_data_view(request):
    if request.method == 'POST':

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
                bet_data = BetDataSerializer(data={**element, 'search':search.data.get('id')})
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
                return Response(response_from_cpp.text, status=status.HTTP_200_OK)
                # updated_search = SearchSerializer(search_instance, data={'csv_url':response_from_cpp.text})
                # if updated_search.is_valid():
                #     updated_search.save()
                # else:
                #     transaction.savepoint_rollback(sid)
                #     return Response('Error!', status=status.HTTP_400_BAD_REQUEST)
                # return Response('Success!', status=status.HTTP_201_CREATED)

        transaction.savepoint_rollback(sid)
        return Response('Error!', status=status.HTTP_400_BAD_REQUEST)

