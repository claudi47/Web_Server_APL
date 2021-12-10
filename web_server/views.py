import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from web_server import serializers
from web_server.models import User


# In Django, a view determines the content of a web page
# views.py is where we handle the request/response logic of our web server
# Create your views here. (function or class)
@api_view(['POST']) # returns a decorator that transforms the function in a APIView REST class
def bet_data_view(request):
    if request.method == 'POST':
        var = User.objects.all()
        for bet_elem in request.data:
            serializer = serializers.BetDataSerializer(data=bet_elem, context={'request': request})
        #     if serializer.is_valid():
        #         serializer.save()
        #         response_from_cpp = requests.post("http://localhost:3000", json=serializer.data)
        #         print(response_from_cpp.text)
        #     else:
        #         return Response("Error", status=status.HTTP_400_BAD_REQUEST)
        # return Response("Success", status=status.HTTP_201_CREATED)
