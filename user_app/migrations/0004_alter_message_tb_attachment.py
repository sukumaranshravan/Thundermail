# Generated by Django 5.0.2 on 2024-02-23 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0003_alter_message_tb_recipient_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message_tb',
            name='attachment',
            field=models.FileField(blank=True, default='default.png', null=True, upload_to='media'),
        ),
    ]
