# Generated by Django 2.1.4 on 2018-12-10 22:56

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('response', '0003_auto_20181211_0222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affectiveresponse',
            name='feature_set',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Superstitious'), (2, 'Interactive '), (3, 'Friendly'), (4, 'Cooperative'), (5, 'Comfortable'), (6, 'Satisfactory'), (7, 'Diverse'), (8, 'Neighbourly'), (9, 'Welcoming'), (10, 'Supervicious'), (11, 'Hostile'), (12, 'Superstitious'), (13, 'Disgusting'), (14, 'Frustating'), (15, 'Social'), (16, 'Frightening'), (17, 'Unsocial'), (18, 'Rude')], default=0, max_length=20),
        ),
    ]