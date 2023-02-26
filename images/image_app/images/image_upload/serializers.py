from rest_framework import serializers
from .models import Image, Thumbnail, BinaryImage


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'uploaded_by', 'created_at']
        read_only_fields = ['uploaded_by']  
  

class ThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thumbnail
        fields = '__all__'


class BinaryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BinaryImage
        fields = '__all__'
        read_only_fields = ['created_by', 'base_image', 'expiration_date','created', 'binary_image']
