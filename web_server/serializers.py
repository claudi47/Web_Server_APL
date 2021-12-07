from rest_framework import serializers
from web_server.models import BetData, User

# A Serializer is an object that permits to define the shape of a request/response sent by a client/server.
# Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes
# that can then be easily rendered into JSON, XML or other content types.
# Lastly, it is the intermediary between the server and the db for the persistence of data
class BetDataSerializer(serializers.ModelSerializer): # extension of the class ModelSerializer
    # This class is necessary to Django REST framework to initialize the Serializer
    class Meta:
        model = BetData
        fields = ['id', 'web_site', 'date', 'match', 'one', 'ics', 'two', 'gol', 'over', 'under']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'user_id']