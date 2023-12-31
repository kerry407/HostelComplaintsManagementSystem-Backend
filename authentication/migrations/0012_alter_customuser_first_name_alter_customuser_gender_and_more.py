# Generated by Django 4.2.2 on 2023-07-01 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_customuser_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='hostel',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.hostel'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='matric_number',
            field=models.CharField(max_length=11, null=True, unique=True),
        ),
    ]
