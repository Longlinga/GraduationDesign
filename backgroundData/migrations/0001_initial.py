# Generated by Django 4.1.3 on 2023-01-15 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='jd_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_titel', models.CharField(max_length=255)),
                ('d_price', models.CharField(max_length=100)),
                ('add_time', models.CharField(max_length=100)),
            ],
        ),
    ]
