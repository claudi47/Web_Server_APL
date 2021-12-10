from django.db import models

# In Django, a model defines the structure of DB table
# models.py is where we define our database models which Django automatically transaltes into database tables
# Create your models here.
class BetData(models.Model):
    # region Declaration of BetData's fields
    # models is a package, <Type>Field indicates the type of field
    date = models.CharField(max_length=127)
    match = models.CharField(max_length=127)
    one = models.CharField(max_length=127)
    ics = models.CharField(max_length=127)
    two = models.CharField(max_length=127)
    gol = models.CharField(max_length=127)
    over = models.CharField(max_length=127)
    under = models.CharField(max_length=127)
    web_site = models.CharField(max_length=127)
    timestamp = models.DateTimeField(auto_now_add=True)

    search_id = models.ForeignKey('Search', on_delete=models.CASCADE)

    # endregion


class User(models.Model):
    # region Declaration of the User's fields
    username = models.CharField(max_length=127)
    user_identifier = models.CharField(max_length=127, primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # endregion

class Search(models.Model):
    csv_url = models.URLField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
