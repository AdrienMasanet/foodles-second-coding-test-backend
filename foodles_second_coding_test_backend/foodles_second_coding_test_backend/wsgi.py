import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodles_second_coding_test_backend.settings")

application = get_wsgi_application()
