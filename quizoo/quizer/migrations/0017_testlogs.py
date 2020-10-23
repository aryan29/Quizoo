# Generated by Django 3.1.1 on 2020-10-23 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizer', '0016_remove_usersgivingtest_curr_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('type', models.CharField(max_length=100)),
                ('img', models.ImageField(upload_to='logs')),
                ('whom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizer.usersgivingtest')),
            ],
        ),
    ]