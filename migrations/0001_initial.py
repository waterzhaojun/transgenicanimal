# Generated by Django 2.1.7 on 2019-02-28 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TransgenicAnimalLog',
            fields=[
                ('animalid', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('cageid', models.CharField(max_length=20)),
                ('dob', models.DateField(blank=True, null=True)),
                ('ear_punch', models.CharField(blank=True, max_length=10, null=True)),
                ('gender', models.CharField(blank=True, max_length=1, null=True)),
                ('genotype', models.TextField(blank=True, null=True)),
                ('purchase_info', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'transgenic_animal_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TransgenicMouseBreeding',
            fields=[
                ('mateid', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('cageid', models.CharField(max_length=20)),
                ('pair_date', models.DateField(blank=True, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('weaning_date', models.DateField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('inprocess', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'transgenic_mouse_breeding',
                'managed': False,
            },
        ),
    ]
