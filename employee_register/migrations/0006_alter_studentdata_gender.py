# Generated by Django 3.2.9 on 2021-12-13 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_register', '0005_alter_studentdata_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentdata',
            name='gender',
            field=models.CharField(choices=[('Male', 'male'), ('Female', 'female'), ('Others', 'others')], max_length=50),
        ),
    ]