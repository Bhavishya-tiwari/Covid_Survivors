# Generated by Django 3.2.4 on 2021-07-28 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_remove_report_authorusername'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='title',
            field=models.CharField(default=9, max_length=255),
            preserve_default=False,
        ),
    ]