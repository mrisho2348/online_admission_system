# Generated by Django 4.2.5 on 2023-09-17 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='education_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_application.educationlevel'),
        ),
    ]
