from django.db import models
import pandas as pd

class Bidder(models.Model):
    bidder_id = models.CharField(max_length=100, unique=True)
    capacity = models.IntegerField()
    
    def __str__(self):
        return self.bidder_id

class Lot(models.Model):
    lot_name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.lot_name

class Bid(models.Model):
    bidder = models.ForeignKey(Bidder, on_delete=models.CASCADE)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    cost = models.FloatField()
    
    def __str__(self):
        return f"{self.bidder} - {self.lot} ({self.cost})"

class Assignment(models.Model):
    bidder = models.ForeignKey(Bidder, on_delete=models.CASCADE)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    cost = models.FloatField()
    
    def __str__(self):
        return f"{self.lot} -> {self.bidder} (Cost: {self.cost})"

class UploadedBid(models.Model):
    bidder_id = models.CharField(max_length=100)
    capacity = models.IntegerField()
    lot_name = models.CharField(max_length=100)
    cost = models.FloatField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.bidder_id} - {self.lot_name} ({self.cost})"
