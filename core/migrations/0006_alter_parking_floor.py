# Generated by Django 4.0.5 on 2022-08-08 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_parking_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parking',
            name='floor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.floor'),
        ),
    ]
