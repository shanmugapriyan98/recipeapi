# Generated by Django 4.2.14 on 2024-07-19 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=50)),
                ('info', models.TextField(max_length=1000)),
            ],
            options={
                'db_table': 'recipe',
            },
        ),
    ]
