import os
import sys
# ensure workspace root is on sys.path so `assetlab` package can be imported
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)
print('WORKSPACE_ROOT=', WORKSPACE_ROOT)
print('sys.path[0:5]=', sys.path[0:5])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assetlab.settings')
import django
django.setup()

import traceback
from django.test.client import RequestFactory
from api.views import LoginView

rf = RequestFactory()
body = '{"email": "jane@example.com", "password": "secret123"}'
req = rf.post('/api/auth/login/', body, content_type='application/json')
view = LoginView.as_view()
try:
    resp = view(req)
    # resp may be an HttpResponse object
    print('Status:', getattr(resp, 'status_code', None))
    try:
        print(resp.content.decode())
    except Exception:
        print(resp)
except Exception:
    traceback.print_exc()
