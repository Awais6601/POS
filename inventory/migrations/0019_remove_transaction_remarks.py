# Generated by Django 5.1.1 on 2024-09-21 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_alter_transaction_expense_alter_transaction_income'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='remarks',
        ),
    ]
