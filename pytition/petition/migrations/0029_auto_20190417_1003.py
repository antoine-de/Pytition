# Generated by Django 2.2 on 2019-04-17 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('petition', '0028_auto_20190417_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='slugownership',
            name='organization',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='petition.Organization'),
        ),
        migrations.AddField(
            model_name='slugownership',
            name='user',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='petition.PytitionUser'),
        ),
    ]