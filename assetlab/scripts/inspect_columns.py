import os, sys
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assetlab.settings')
import django
django.setup()
from django.db import connection
cur = connection.cursor()
cur.execute("SHOW COLUMNS FROM api_user")
for row in cur.fetchall():
    print(row[0])
