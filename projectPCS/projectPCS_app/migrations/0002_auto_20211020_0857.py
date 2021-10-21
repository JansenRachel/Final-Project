# Generated by Django 2.2 on 2021-10-20 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectPCS_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='move_info',
            name='id',
        ),
        migrations.AlterField(
            model_name='move_info',
            name='user_moving',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='projectPCS_app.User'),
        ),
    ]