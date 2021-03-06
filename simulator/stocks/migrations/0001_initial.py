# Generated by Django 4.0.5 on 2022-06-30 07:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash', models.FloatField(default=20000.0)),
                ('cashInvested', models.FloatField(default=0.0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=20)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.portfolio')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stockName', models.CharField(max_length=20)),
                ('bought', models.BooleanField(default=True)),
                ('numberOfStocks', models.IntegerField()),
                ('stockPrice', models.FloatField()),
                ('date', models.DateField()),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.portfolio')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('ticker', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('priceBought', models.FloatField()),
                ('stocksBought', models.IntegerField()),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.portfolio')),
            ],
        ),
        migrations.CreateModel(
            name='AllStocks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('ticker', models.CharField(max_length=20)),
                ('totalCost', models.FloatField()),
                ('stocksOwned', models.IntegerField()),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.portfolio')),
            ],
        ),
    ]
