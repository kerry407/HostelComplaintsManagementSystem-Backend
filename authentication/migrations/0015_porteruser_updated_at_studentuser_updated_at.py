# Generated by Django 4.2.2 on 2023-07-01 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_alter_customuser_first_name_alter_customuser_gender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='porteruser',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='studentuser',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]