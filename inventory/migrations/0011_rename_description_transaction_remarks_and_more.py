# Generated by Django 5.1.1 on 2024-09-19 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_rename_transaction_date_transaction_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='description',
            new_name='remarks',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='type',
            new_name='transaction_type',
        ),
    ]
