from django.db import models


class Collection(models.Model):
    collection_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Card(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)