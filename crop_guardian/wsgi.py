import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crop_guardian.settings')

application = get_wsgi_application()
app = application  # ✅ Required by Vercel
