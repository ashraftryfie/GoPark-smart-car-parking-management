# Generated by Django 4.0.5 on 2022-08-08 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0006_alter_camera_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='path',
            field=models.CharField(blank='', max_length=250, null=True),
        ),
    ]
