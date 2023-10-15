from rest_framework import serializers
from connector.models import Products  # Replace with your actual model

class YourModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products  # Replace with your actual model
        fields = '__all__'  # You can also specify specific fields
