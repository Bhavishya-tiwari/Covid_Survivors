# Generated by Django 3.2.4 on 2021-07-16 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_comment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='email',
            field=models.CharField(default=2, max_length=70),
            preserve_default=False,
        ),
    ]
