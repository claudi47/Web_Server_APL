from abc import ABC

from rest_framework import serializers
from web_server.models import BetData, User, Search, Settings


# A Serializer is an object that permits to define the shape of a request/response sent by a client/server.
# Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes
# that can then be easily rendered into JSON, XML or other content types.
# Lastly, it is the intermediary between the server and the db for the persistence of data
class BetDataSerializer(serializers.ModelSerializer): # extension of the class ModelSerializer
    # This class is necessary to Django REST framework to initialize the Serializer
    class Meta:
        model = BetData
        fields = ['id', 'web_site', 'date', 'match', 'one', 'ics', 'two', 'gol', 'over', 'under', 'search']

class UserSerializer(serializers.ModelSerializer):
    # Creation of a property (read-only type [NO PERSISTENCE ON THE DB]) to define a relation one-to-many
    searches = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'user_identifier', 'searches', 'max_research', 'ban_period']

class SearchSerializer(serializers.ModelSerializer):
    bet_data = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Search
        fields = ['id', 'csv_url', 'user', 'bet_data']

class SettingsSearializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ['goldbet_research', 'bwin_research']

class SettingsDataSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError

    max_researches = serializers.IntegerField()
    bool_for_all = serializers.BooleanField()
    username_research = serializers.CharField(max_length=64)
    user_suspended = serializers.CharField(max_length=64)
    period_of_suspension = serializers.DateTimeField()
    bool_toggle_godlbet = serializers.BooleanField()
    bool_toggle_bwin = serializers.BooleanField()

