from django.db import models

class PatientRecord(models.Model):
    # ข้อมูลทั่วไป
    age = models.IntegerField(verbose_name="อายุ (ปี)")
    gender = models.IntegerField(choices=[(1, 'หญิง'), (2, 'ชาย')], verbose_name="เพศ")
    height = models.FloatField(verbose_name="ส่วนสูง (cm)")
    weight = models.FloatField(verbose_name="น้ำหนัก (kg)")
    
    # ข้อมูลทางการแพทย์
    ap_hi = models.FloatField(verbose_name="ความดันตัวบน")
    ap_lo = models.FloatField(verbose_name="ความดันตัวล่าง")
    cholesterol = models.IntegerField(verbose_name="คอเลสเตอรอล")
    gluc = models.IntegerField(verbose_name="น้ำตาลในเลือด")
    
    # พฤติกรรม
    smoke = models.IntegerField(verbose_name="สูบบุหรี่")
    alco = models.IntegerField(verbose_name="ดื่มแอลกอฮอล์")
    active = models.IntegerField(verbose_name="ออกกำลังกาย")
    
    # ผลลัพธ์จาก AI
    risk_percentage = models.IntegerField(verbose_name="เปอร์เซ็นต์ความเสี่ยง")
    is_risk = models.BooleanField(default=False, verbose_name="มีความเสี่ยงหรือไม่")
    
    # วันที่บันทึก
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่ประเมิน")

    def __str__(self):
        risk_text = "เสี่ยง" if self.is_risk else "ปกติ"
        return f"เคสอายุ {self.age} ปี - ผลลัพธ์: {risk_text} ({self.risk_percentage}%)"