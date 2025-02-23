from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class OptimizationResultSerializer(serializers.Serializer):
    lot = serializers.CharField()
    bidder = serializers.CharField()
    bidder_name = serializers.CharField()  # 🔹 New field to include bidder's name
    cost = serializers.FloatField()
    total_allocation = serializers.FloatField()  # Shows the bidder's total allocation
    turnover_capacity = serializers.FloatField()  # Shows the bidder's turnover capacity
