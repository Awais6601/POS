from django.db import migrations, models
from django.utils import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),  # Ensure this file exists
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='manufacture_date',
            field=models.DateField(default=timezone.now().date),
        ),
        migrations.AddField(
            model_name='medicine',
            name='expiry_date',
            field=models.DateField(default=timezone.now().date),
        ),
        migrations.AddField(
            model_name='medicine',
            name='purchasing_date',
            field=models.DateField(default=timezone.now().date),
        ),
    ]
