# Generated by Django 4.2.19 on 2025-02-23 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedBid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidder_id', models.CharField(max_length=100)),
                ('capacity', models.IntegerField()),
                ('lot_name', models.CharField(max_length=100)),
                ('cost', models.FloatField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
