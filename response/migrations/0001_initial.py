# Generated by Django 2.1.4 on 2018-12-10 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classification', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AffectiveResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('familiarity', models.IntegerField(choices=[(1, 'For the first time'), (2, 'More Often')])),
                ('accompany', models.IntegerField(choices=[(1, 'Alone'), (2, 'With family member(s)'), (3, 'With friend(s)'), (4, 'With adult(s)'), (5, 'with child(ren)')])),
                ('comfortability', models.IntegerField(choices=[(1, 'Very uncomfortable'), (2, 'Uncomfortable'), (3, 'Slightly uncomfortable'), (4, 'Neutral'), (5, 'Slightly comfortable'), (6, 'Comfortable'), (7, 'Very comfortable')])),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classification.Category')),
            ],
            options={
                'verbose_name_plural': 'affective responses',
            },
        ),
    ]