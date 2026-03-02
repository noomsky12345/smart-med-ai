import os
from django.core.wsgi import get_wsgi_application

# 🌟 เพิ่มโค้ดสั่ง Migrate ตรงนี้
os.system('python manage.py migrate')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
application = get_wsgi_application()