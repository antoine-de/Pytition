# Generated by Django 2.2 on 2019-04-17 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petition', '0030_remove_petition_slugs'),
    ]

    operations = [
        migrations.AddField(
            model_name='petition',
            name='slugs',
            field=models.ManyToManyField(blank=True, through='petition.SlugOwnership', to='petition.SlugModel'),
        ),
    ]