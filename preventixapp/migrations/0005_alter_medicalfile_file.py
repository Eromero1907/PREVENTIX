# Generated by Django 5.1.6 on 2025-02-20 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preventixapp', '0004_medicalfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalfile',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]
