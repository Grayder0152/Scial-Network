# Generated by Django 3.2.3 on 2021-05-23 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_likeanalytics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likeanalytics',
            name='liked_time',
            field=models.DateField(),
        ),
    ]
