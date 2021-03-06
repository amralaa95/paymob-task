# Generated by Django 2.2 on 2020-11-04 14:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import promo.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('promo_type', models.CharField(max_length=50)),
                ('promo_code', models.CharField(default=promo.models.generate_promo_code, max_length=40, unique=True)),
                ('promo_amount', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.CharField(max_length=300)),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeductPromo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('promo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deductions', to='promo.Promo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
