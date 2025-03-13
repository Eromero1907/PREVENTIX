# Generated by Django 5.1.6 on 2025-03-13 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_history', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('file', models.FileField(upload_to='')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
