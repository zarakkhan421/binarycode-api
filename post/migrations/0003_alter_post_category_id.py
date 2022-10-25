# Generated by Django 4.1.2 on 2022-10-25 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('post', '0002_alter_post_category_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category_id',
            field=models.ManyToManyField(blank=True, related_name='posts', to='common.category', verbose_name='Categories'),
        ),
    ]
