from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response

from django.contrib.auth.models import User

from easy_thumbnails.files import get_thumbnailer
from datetime import timedelta
from django.utils import timezone

from .models import Image, Thumbnail, Profile, BinaryImage
from .serializers import ImageSerializer, ThumbnailSerializer, BinaryImageSerializer

import cv2
from PIL import Image as pillow_image
import random


class ImageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        profile = Profile.objects.filter(user=self.request.user)
        return Image.objects.filter(uploaded_by=profile[0])
    
    def perform_create(self, image_serializer):
        profile = Profile.objects.filter(user=self.request.user)[0]
        image_serializer.save(uploaded_by=profile)
        self.create_thumbnails(image_serializer)

    def create_thumbnails(self, image_serializer):
        base_image = Image.objects.last()
        created_by = base_image.uploaded_by
        granted_tier = created_by.granted_tier
        thumbnail_sizes = []
        if granted_tier.thumbnail_200px:
            thumbnail_sizes.append(200)
        if granted_tier.thumbnail_400px:
            thumbnail_sizes.append(400)    
        if granted_tier.arbitrary_thumbnail_size:
            thumbnail_sizes.append(granted_tier.arbitrary_thumbnail_size)
        for th_size in thumbnail_sizes:        
            thumbnailer = get_thumbnailer(base_image.image)
            th = thumbnailer.get_thumbnail({'size': (th_size, th_size), 'crop': True})
            Thumbnail.objects.create(created_by=created_by, base_image=base_image, thumbnail_image=str(th), thumbnail_size=th_size)

image_list_create_api_view = ImageListCreateAPIView.as_view()


class ImageDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        image_id = self.kwargs['pk']  
        profile = Profile.objects.filter(user=self.request.user)[0]
        if profile.granted_tier.original_size == True:
            return Image.objects.filter(uploaded_by=profile, id=image_id)
        return Response({"error": "You cannot access image in orginal size. Upgrate Your account tier."})
           
image_detail_api_view = ImageDetailAPIView.as_view()


class ThumbnailListAPIView(generics.ListAPIView):    
    serializer_class = ThumbnailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        base_image_id = self.kwargs['pk']  
        profile = Profile.objects.filter(user=self.request.user)
        return Thumbnail.objects.filter(created_by=profile[0], base_image=base_image_id)

thumbnail_list_api_view = ThumbnailListAPIView.as_view()


class BinaryImageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BinaryImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        base_image_id = self.kwargs['pk']
        BinaryImage.objects.filter(expiration_date__lt=timezone.now()).delete()
        profile = Profile.objects.filter(user=self.request.user)        
        return BinaryImage.objects.filter(created_by=profile[0], base_image=base_image_id) 

    def perform_create(self, serializer):
        base_image_id = self.kwargs['pk']
        profile = Profile.objects.filter(user=self.request.user)[0]
        if profile.granted_tier.generate_expiring_links == True:            
            base_image = Image.objects.get(pk=base_image_id)
            data = self.request.POST.copy()
            seconds = self.request.data['seconds_to_expiration']
            if base_image.image:
                img = cv2.imread(base_image.image.url[1:])
                height = img.shape[0]
                width = img.shape[1]
                down_width = width
                if down_width > 1024:
                    down_width = 1024
                down_height = int((height/width)*down_width)
                down_points = (down_width, down_height)
                resized_down = cv2.resize(img, down_points, interpolation=cv2.INTER_LINEAR)
                gray = cv2.cvtColor(resized_down, cv2.COLOR_BGR2GRAY)
                ret, tresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                filename = f'binary/binary{random.randint(1000, 9999)}-{base_image.id}-{seconds}.png'
                im = pillow_image.fromarray(tresh1)
                im.save('media/' + filename)
            
            if serializer.is_valid():        
                serializer.save(created_by=profile, 
                base_image=base_image, 
                binary_image=filename, 
                created=timezone.now(),
                expiration_date=(timezone.now() + timedelta(seconds=int(seconds)))
                )
                return Response({"message": "Successfully created"})
        return Response({"error": "You cannot generate expiring links to binary images. Upgrate Your account tier."})

binary_image_list_create_api_view = BinaryImageListCreateAPIView.as_view()
