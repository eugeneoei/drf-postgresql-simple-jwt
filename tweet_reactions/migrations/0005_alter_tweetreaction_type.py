# Generated by Django 3.2.9 on 2021-12-03 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet_reactions', '0004_alter_tweetreaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetreaction',
            name='type',
            field=models.CharField(choices=[('LI', 'Like'), ('DI', 'Dislike'), ('LO', 'Love'), ('SA', 'Sad')], max_length=2),
        ),
    ]
