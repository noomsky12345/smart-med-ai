from django.shortcuts import render
from django.conf import settings
import os
import joblib
import numpy as np

# กำหนดเส้นทางไปหาไฟล์โมเดลในโฟลเดอร์ ml_model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_model', 'heart_model.pkl')
SCALER_PATH = os.path.join(settings.BASE_DIR, 'ml_model', 'scaler.pkl')

# โหลดโมเดลและ Scaler เตรียมไว้ (โหลดแค่ครั้งเดียวตอนเซิร์ฟเวอร์รัน)
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def predict_risk(request):
    result = None
    if request.method == 'POST':
        try:
            # 1. รับค่าจากฟอร์มหน้าเว็บ (รับมาเป็น string ต้องแปลงเป็น float/int)
            age = float(request.POST.get('age'))
            gender = int(request.POST.get('gender'))
            height = float(request.POST.get('height'))
            weight = float(request.POST.get('weight'))
            ap_hi = float(request.POST.get('ap_hi'))
            ap_lo = float(request.POST.get('ap_lo'))
            cholesterol = int(request.POST.get('cholesterol'))
            gluc = int(request.POST.get('gluc'))
            smoke = int(request.POST.get('smoke'))
            alco = int(request.POST.get('alco'))
            active = int(request.POST.get('active'))

            # 2. จัดเรียงข้อมูลให้ตรงกับตอนที่ใช้เทรนโมเดลเป๊ะๆ (11 คอลัมน์)
            features = np.array([[age, gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active]])

            # 3. ปรับสเกลข้อมูล (สำคัญมาก! ถ้าไม่ทำ โมเดลจะรวน)
            features_scaled = scaler.transform(features)

            # 4. ให้โมเดลทำนายผล (0 = ปกติ, 1 = เสี่ยง)
            prediction = model.predict(features_scaled)

            if prediction[0] == 1:
                result = "⚠️ มีความเสี่ยงเป็นโรคหลอดเลือดหัวใจ แนะนำให้ปรึกษาแพทย์"
            else:
                result = "✅ ความเสี่ยงต่ำ (ไม่พบสัญญาณอันตราย)"

        except Exception as e:
            result = f"เกิดข้อผิดพลาดในการประมวลผล: {e}"

    # ส่งผลลัพธ์กลับไปแสดงที่หน้าเว็บ
    return render(request, 'prediction/form.html', {'result': result})
def patients_mock(request):
    return render(request, 'prediction/mock_page.html', {'page_title': 'ทะเบียนผู้ป่วย (Patient Registry)', 'icon': '👥'})

def history(request):
    return render(request, 'prediction/mock_page.html', {'page_title': 'ประวัติการวิเคราะห์ (Analysis History)', 'icon': '📄'})

def settings_page(request):
    return render(request, 'prediction/mock_page.html', {'page_title': 'การตั้งค่าระบบ (System Settings)', 'icon': '⚙️'})