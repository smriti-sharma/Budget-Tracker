# Generated by Django 4.0 on 2021-12-24 20:03

import budgettracker.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField(choices=[(0, 'Entertainment'), (1, 'Food'), (2, 'Utility'), (3, 'Bill'), (4, 'Shopping')], default=4)),
                ('amount', models.IntegerField(default=0, validators=[])),
                ('kind', models.IntegerField(choices=[(0, 'Credit'), (1, 'Debit')], default=1)),
                ('processed_at', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('last_modified_at', models.DateField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budgettracker.account')),
            ],
        ),
    ]
