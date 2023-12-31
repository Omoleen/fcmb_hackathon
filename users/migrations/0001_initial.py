# Generated by Django 4.2.6 on 2023-10-28 18:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True, verbose_name='email address')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('wallet', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('otp', models.CharField(default='0000', max_length=4)),
                ('location_lat', models.FloatField(blank=True, default=0, null=True)),
                ('location_long', models.FloatField(blank=True, default=0, null=True)),
                ('address', models.TextField(blank=True, null=True, verbose_name='home address')),
                ('credit_score', models.IntegerField(default=0)),
                ('verify_ID', models.FileField(blank=True, null=True, upload_to='verifyId')),
                ('verify_ID_name', models.CharField(blank=True, choices=[('DRIVERS_LICENCE', "driver's license"), ('NIN', 'nin'), ('VOTERS_CARD', "voter's card")], max_length=512, null=True)),
                ('nin', models.CharField(blank=True, max_length=512, null=True)),
                ('bvn', models.CharField(blank=True, max_length=512, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_agent', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdvertisedLoan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_amount', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('total_amount_remaining', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('interest', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('period', models.IntegerField(verbose_name='number of days')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('times_to_pay', models.IntegerField(verbose_name='pay x times')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='advertised_loan', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('advertised_loan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='loan', to='users.advertisedloan')),
                ('receiving_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='loan', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, choices=[('WITHDRAWAL', 'withdrawal'), ('DEPOSIT', 'deposit'), ('TRANSFER', 'transfer'), ('LOAN_REPAYMENT', 'loan_repayment')], max_length=512, null=True)),
                ('remaining_balance', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agent_transaction_history', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transaction_history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LoanRepayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('remaining_balance', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repayment', to='users.loan')),
            ],
        ),
        migrations.CreateModel(
            name='BenificiaryContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=512, null=True)),
                ('last_name', models.CharField(blank=True, max_length=512, null=True)),
                ('bvn', models.CharField(blank=True, max_length=512, null=True)),
                ('verify_ID', models.FileField(blank=True, null=True, upload_to='verifyId')),
                ('verify_ID_name', models.CharField(blank=True, choices=[('DRIVERS_LICENCE', "driver's license"), ('NIN', 'nin'), ('VOTERS_CARD', "voter's card")], max_length=512, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beneficiary', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
