# Generated by Django 4.0.10 on 2023-07-15 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='supervisor',
            new_name='parent',
        ),
    ]
