# Generated by Django 4.0.6 on 2022-08-11 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_category_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorytranslation',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='producttranslation',
            name='slug',
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='131', max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='13sa', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='categorytranslation',
            name='language_code',
            field=models.CharField(db_index=True, max_length=15, verbose_name='Language'),
        ),
        migrations.AlterField(
            model_name='producttranslation',
            name='language_code',
            field=models.CharField(db_index=True, max_length=15, verbose_name='Language'),
        ),
    ]
