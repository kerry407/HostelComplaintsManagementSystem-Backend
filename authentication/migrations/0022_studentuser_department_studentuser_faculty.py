# Generated by Django 4.2.2 on 2023-07-04 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0021_alter_hostel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentuser',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='studentuser',
            name='faculty',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]