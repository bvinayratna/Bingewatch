# Generated by Django 4.0.3 on 2022-03-30 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_liked_songs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liked_songs',
            name='u_name',
            field=models.ForeignKey(db_column='username', on_delete=django.db.models.deletion.PROTECT, to='app.user', to_field='username'),
        ),
    ]
