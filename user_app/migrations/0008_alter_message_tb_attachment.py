# Generated by Django 5.0.2 on 2024-02-23 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0007_alter_message_tb_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message_tb',
            name='attachment',
            field=models.FileField(blank=True, default='default.png', null=True, upload_to='thunder'),
        ),
    ]
