from django.db import migrations, connection


def add_missing_fields(apps, schema_editor):
    db_name = connection.settings_dict.get('NAME')
    cols = {
        'last_login': 'DATETIME NULL',
        'is_active': 'TINYINT(1) NOT NULL DEFAULT 1',
        'is_staff': 'TINYINT(1) NOT NULL DEFAULT 0',
        'is_superuser': 'TINYINT(1) NOT NULL DEFAULT 0',
    }
    with connection.cursor() as cursor:
        for col, coltype in cols.items():
            cursor.execute(
                "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND COLUMN_NAME=%s",
                [db_name, 'api_user', col]
            )
            if cursor.fetchone()[0] == 0:
                cursor.execute(f"ALTER TABLE api_user ADD COLUMN `{col}` {coltype};")


def remove_missing_fields(apps, schema_editor):
    cols = ['last_login', 'is_active', 'is_staff', 'is_superuser']
    with connection.cursor() as cursor:
        for col in cols:
            cursor.execute(
                "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=%s AND COLUMN_NAME=%s",
                ['api_user', col]
            )
            if cursor.fetchone()[0] > 0:
                cursor.execute(f"ALTER TABLE api_user DROP COLUMN `{col}`;")


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_user_age'),
    ]

    operations = [
        migrations.RunPython(add_missing_fields, remove_missing_fields),
    ]
