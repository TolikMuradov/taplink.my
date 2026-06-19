from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_link_icon_iconify'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='link_type',
            field=models.CharField(default='link', max_length=20),
        ),
    ]
