from rest_framework import serializers
from .models import ReactUrl

class MySerializer(serializers.ModelSerializer):
   
   class Meta:
       model = ReactUrl
       fields = ['id', 'url']
