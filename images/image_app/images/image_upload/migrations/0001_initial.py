# Generated by Django 4.0.9 on 2023-02-26 15:46

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountTier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('thumbnail_200px', models.BooleanField(default=True)),
                ('thumbnail_400px', models.BooleanField(default=False)),
                ('arbitrary_thumbnail_size', models.PositiveIntegerField(blank=True, null=True)),
                ('original_size', models.BooleanField(default=False)),
                ('generate_expiring_links', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('granted_tier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='image_upload.accounttier')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail_image', models.ImageField(upload_to='thumbnails/%Y/%m/%d/')),
                ('thumbnail_size', models.PositiveIntegerField(editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('base_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='image_upload.image')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='image_upload.profile')),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='uploaded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='image_upload.profile'),
        ),
        migrations.CreateModel(
            name='BinaryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('binary_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('created', models.DateTimeField(null=True)),
                ('expiration_date', models.DateTimeField(null=True)),
                ('seconds_to_expiration', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(300), django.core.validators.MaxValueValidator(30000)])),
                ('base_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='image_upload.image')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='image_upload.profile')),
            ],
        ),
    ]
