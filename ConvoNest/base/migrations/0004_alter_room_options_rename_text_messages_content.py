# Generated by Django 5.0.3 on 2024-03-13 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_messages_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.RenameField(
            model_name='messages',
            old_name='text',
            new_name='content',
        ),
    ]