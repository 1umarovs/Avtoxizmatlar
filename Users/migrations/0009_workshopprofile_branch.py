# Generated by Django 5.0.6 on 2025-05-31 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0008_alter_workshopprofile_options_workshoprating'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshopprofile',
            name='branch',
            field=models.ManyToManyField(blank=True, related_name='branches', to='Users.workshopprofile'),
        ),
    ]
