from django.apps import AppConfig
import os

class PredictionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prediction'

    def ready(self):
        # 🌟 สั่งให้ทำงานเมื่อ App พร้อม
        if os.environ.get('RUN_MAIN') == 'true': # ป้องกันการรันซ้ำซ้อนตอนเปิดเซิร์ฟเวอร์
            os.system('python manage.py migrate')