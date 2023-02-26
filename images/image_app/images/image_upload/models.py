from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
# Create your models here.


class AccountTier(models.Model):
    name = models.CharField(max_length=50, unique=True)
    thumbnail_200px = models.BooleanField(default=True)
    thumbnail_400px = models.BooleanField(default=False)
    arbitrary_thumbnail_size = models.PositiveIntegerField(blank=True, null=True)
    original_size = models.BooleanField(default=False)
    generate_expiring_links = models.BooleanField(default=False)

    def __str__(self):
        account_description = f"{self.name} tier:"
        if self.thumbnail_200px:
            account_description += " 200px"
        if self.thumbnail_400px:
            account_description += " 400px"
        if self.arbitrary_thumbnail_size:
            account_description += f" {self.arbitrary_thumbnail_size}px"
        if self.original_size:
            account_description += " + orginal"
        if self.generate_expiring_links:
            account_description += " + expiring links"
        return account_description


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    granted_tier = models.ForeignKey(AccountTier, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f'{self.user}'


class Image(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', max_length=100, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    uploaded_by = models.ForeignKey(Profile, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)


class Thumbnail(models.Model):
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    base_image = models.ForeignKey(Image, on_delete=models.CASCADE)
    thumbnail_image = models.ImageField(upload_to='thumbnails/%Y/%m/%d/', max_length=100)
    thumbnail_size = models.PositiveIntegerField(null=False, blank=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)


class BinaryImage(models.Model):
    base_image = models.ForeignKey(Image, on_delete=models.CASCADE)
    binary_image = models.ImageField(blank=True, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(null=True)
    expiration_date = models.DateTimeField(null=True)
    seconds_to_expiration = models.PositiveIntegerField(validators=[MinValueValidator(300), MaxValueValidator(30000)])
    