# Generated by Django 4.0.5 on 2022-07-31 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theblog', '0030_alter_post_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('date_added',)},
        ),
    ]