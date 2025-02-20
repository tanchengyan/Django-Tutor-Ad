# Generated by Django 5.1.2 on 2024-12-28 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0034_tutorad_linkedin_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorad',
            name='linkedin_url',
        ),
        migrations.RemoveField(
            model_name='tutorad',
            name='wechat',
        ),
        migrations.AddField(
            model_name='author',
            name='linkedin_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='preferred_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='tel_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='wechat',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tutorad',
            name='contact_email',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tutorad',
            name='contact_tel',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tutorad',
            name='contact_wechat',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tutorad',
            name='rate',
            field=models.DecimalField(decimal_places=0, max_digits=8),
        ),
    ]
