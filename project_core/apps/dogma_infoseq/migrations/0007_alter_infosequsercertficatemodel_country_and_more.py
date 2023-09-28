# Generated by Django 4.2 on 2023-05-11 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogma_infoseq', '0006_alter_infosequsercertficatemodel_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infosequsercertficatemodel',
            name='country',
            field=models.CharField(choices=[('1', 'RU')], default='1', max_length=2),
        ),
        migrations.AlterField(
            model_name='infosequsercertficatemodel',
            name='key_size',
            field=models.CharField(choices=[('1', '2048')], default='1', max_length=2),
        ),
        migrations.AlterField(
            model_name='infosequsercertficatemodel',
            name='key_usage',
            field=models.CharField(choices=[('1', 'tls-client')], default='1', max_length=2),
        ),
        migrations.AlterField(
            model_name='infosequsercertficatemodel',
            name='locality',
            field=models.CharField(choices=[('1', 'KRD'), ('2', 'MSK'), ('3', 'OMK')], default='1', max_length=2),
        ),
        migrations.AlterField(
            model_name='infosequsercertficatemodel',
            name='organization',
            field=models.CharField(choices=[('1', 'DOGMA')], default='1', max_length=2),
        ),
        migrations.AlterField(
            model_name='infosequsercertficatemodel',
            name='state',
            field=models.CharField(choices=[(1, '31')], default=1, max_length=2),
        ),
        migrations.AlterField(
            model_name='infosequsercertficatemodel',
            name='unit',
            field=models.CharField(choices=[('1', 'DIS')], default='1', max_length=2),
        ),
    ]
