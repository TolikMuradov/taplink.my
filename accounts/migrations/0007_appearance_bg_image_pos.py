from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_giftcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='appearance',
            name='bg_image_pos_x',
            field=models.FloatField(default=50.0),
        ),
        migrations.AddField(
            model_name='appearance',
            name='bg_image_pos_y',
            field=models.FloatField(default=50.0),
        ),
    ]
