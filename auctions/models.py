from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Categories(models.Model):
    name = models.CharField(max_length=64)


class Auctions(models.Model):
    title = models.CharField(max_length=64, null=False)
    description = models.CharField(max_length=500, null=False)
    starting_bid = models.IntegerField(null=False)
    time = models.DateTimeField(null=False)
    image = models.URLField(default="N/A")
    closed = models.BooleanField(default=False)
    interested = models.ManyToManyField(User, blank=True, related_name="watchlist")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases", null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="auctions", null=True)


class Bids(models.Model):
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="bids", null=False)
    bid = models.IntegerField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    time = models.DateTimeField(null=False)






class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=False)
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="comments", null=False)
    comment = models.CharField(max_length=300, null=False)
    time = models.DateTimeField(null=True)
