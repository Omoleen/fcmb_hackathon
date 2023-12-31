# Generated by Django 4.2.6 on 2023-10-28 21:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_advertisedloan_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='KorapayTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, choices=[('WITHDRAWAL', 'withdrawal'), ('DEPOSIT', 'deposit')], max_length=512, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('reference', models.TextField()),
                ('status', models.CharField(blank=True, choices=[('PENDING', 'Pending'), ('FAILED', 'Failed'), ('SUCCESS', 'Success')], default='PENDING', max_length=512, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='web_transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
