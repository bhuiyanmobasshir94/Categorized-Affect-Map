# Generated by Django 2.1.4 on 2018-12-11 21:03

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('response', '0004_auto_20181211_0456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affectiveresponse',
            name='feature_set',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(19, 'Interactive '), (20, 'Friendly'), (21, 'Cooperative'), (22, 'Comfortable'), (23, 'Satisfactory'), (24, 'Diverse'), (25, 'Neighbourly'), (26, 'Welcoming'), (27, 'Supervicious'), (28, 'Hostile'), (29, 'Superstitious'), (30, 'Disgusting'), (31, 'Frustating'), (32, 'Social'), (33, 'Frightening'), (34, 'Unsocial'), (35, 'Rude'), (36, 'Active'), (37, 'Exciting'), (38, 'Beautiful'), (39, 'Populated'), (40, 'Disgusting'), (41, 'Frustating'), (42, 'Enjoyable'), (43, 'Ugly'), (44, 'Insignificent'), (45, 'Magestic'), (46, 'Hectic'), (47, 'Harsh'), (48, 'Simulating'), (49, 'Unsimulating'), (50, 'Sleepy'), (51, 'Festive'), (52, 'Boring'), (53, 'Transport service Quality'), (54, 'Bus Availability'), (55, 'Emergency'), (56, 'well connected'), (57, 'Moderately connected'), (58, 'Disconnected'), (59, 'Heavy traffic'), (60, 'Moderate traffic'), (61, 'Low Traffic'), (62, 'Desolate'), (63, 'Rickshaw  available'), (64, 'Rickshaw only'), (65, 'Walkway available'), (66, 'Walkway only'), (67, 'Private transport available'), (68, 'Private transport unavailable'), (69, 'Public transport available'), (70, 'Public transport unavailable')], default=0, max_length=20),
        ),
    ]
