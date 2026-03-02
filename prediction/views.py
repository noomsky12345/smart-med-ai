from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required  # ระบบล็อกประตู
from django.contrib.auth import logout  # ระบบออกจากระบบ
import os
import joblib
import numpy as np
from .models import PatientRecord 

# กำหนดเส้นทางไปหาไฟล์โมเดลในโฟลเดอร์ ml_model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_model', 'heart_model.pkl')
SCALER_PATH = os.path.join(settings.BASE_DIR, 'ml_model', 'scaler.pkl')

# โหลดโมเดลและ Scaler เตรียมไว้ 
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# 🌟 ฟังก์ชันหน้าประเมินผล (ลบ @login_required ออกแล้ว เพื่อให้คนทั่วไปเข้าใช้งานได้)
def predict_risk(request):
    result = None
    risk_percentage = 0

    if request.method == 'POST':
        try:
            # รับค่าจากฟอร์มหน้าเว็บ 
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

            # จัดเรียงข้อมูล
            features = np.array([[age, gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active]])

            # ปรับสเกลข้อมูล 
            features_scaled = scaler.transform(features)

            # ให้โมเดลทำนายผล 
            prediction = model.predict(features_scaled)
            prediction_prob = model.predict_proba(features_scaled)[0][1]
            risk_percentage = int(prediction_prob * 100)

            # กำหนดสถานะความเสี่ยง
            is_risk = False
            if prediction[0] == 1:
                result = "⚠️ มีความเสี่ยงเป็นโรคหลอดเลือดหัวใจ แนะนำให้ปรึกษาแพทย์"
                is_risk = True
            else:
                result = "✅ ความเสี่ยงต่ำ (ไม่พบสัญญาณอันตราย)"
                is_risk = False

            # บันทึกข้อมูลลงฐานข้อมูล
            PatientRecord.objects.create(
                age=age,
                gender=gender,
                height=height,
                weight=weight,
                ap_hi=ap_hi,
                ap_lo=ap_lo,
                cholesterol=cholesterol,
                gluc=gluc,
                smoke=smoke,
                alco=alco,
                active=active,
                risk_percentage=risk_percentage,
                is_risk=is_risk
            )

        except Exception as e:
            result = f"เกิดข้อผิดพลาดในการประมวลผล: {e}"
            risk_percentage = 0

    # ดึงสถิติจริงจากฐานข้อมูล
    total_cases = PatientRecord.objects.count() 
    high_risk_cases = PatientRecord.objects.filter(is_risk=True).count() 
    ai_accuracy = 74.14 

    # ส่งผลลัพธ์และสถิติกลับไปแสดงที่หน้าเว็บ
    return render(request, 'prediction/form.html', {
        'result': result, 
        'risk_percentage': risk_percentage,
        'total_cases': total_cases,          
        'high_risk_cases': high_risk_cases,  
        'ai_accuracy': ai_accuracy
    })


# ==============================================================================
# 🌟 โซนสำหรับคุณหมอ/แอดมิน (ต้องเข้าสู่ระบบก่อนถึงจะเข้าได้)
# ==============================================================================

@login_required(login_url='login')
def patients_mock(request):
    return render(request, 'prediction/mock_page.html', {'page_title': 'ทะเบียนผู้ป่วย (Patient Registry)', 'icon': '👥'})

@login_required(login_url='login')
def history(request):
    # ดึงข้อมูลคนไข้ทั้งหมดจากตาราง เรียงลำดับจากวันที่ประเมินล่าสุด (ใหม่ไปเก่า)
    records = PatientRecord.objects.all().order_by('-created_at')
    return render(request, 'prediction/history.html', {
        'page_title': 'ประวัติการวิเคราะห์ (Analysis History)',
        'records': records
    })

@login_required(login_url='login')
def settings_page(request):
    return render(request, 'prediction/mock_page.html', {'page_title': 'การตั้งค่าระบบ (System Settings)', 'icon': '⚙️'})

# 🌟 ฟังก์ชันสำหรับออกจากระบบ
def logout_user(request):
    logout(request)
    return redirect('login')