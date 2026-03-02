import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

print("กำลังโหลดข้อมูลและเริ่มฝึกสอนโมเดล กรุณารอสักครู่...")

# 1. โหลดข้อมูลจากไฟล์ CSV 
# (ถ้าไฟล์ของคุณใช้ลูกน้ำแบ่ง ให้เปลี่ยนเป็น sep=',')
csv_path = 'cardio_train.csv' 
df = pd.read_csv(csv_path, sep=';')

# 2. ทำความสะอาดและเตรียมข้อมูล
if 'id' in df.columns:
    df = df.drop('id', axis=1) # ลบคอลัมน์ id ทิ้ง เพราะไม่เกี่ยวกับการเป็นโรค

# แปลงอายุจาก "วัน" เป็น "ปี" (Dataset ตัวนี้เก็บอายุเป็นจำนวนวัน)
if 'age' in df.columns and df['age'].mean() > 1000:
    df['age'] = (df['age'] / 365.25).round().astype(int)

# 3. แยกฟีเจอร์ (X) และคำตอบ (y)
# Target ของเราคือคอลัมน์ 'cardio' (0 = ปกติ, 1 = เสี่ยงโรคหัวใจ)
X = df.drop('cardio', axis=1)
y = df['cardio']

# 4. แบ่งข้อมูลสำหรับ Train (80%) และ Test (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. ปรับสเกลข้อมูล (Feature Scaling) *** นางเอกของงานนี้ ช่วยแก้บั๊กทายผลเป็น 1 ตลอด ***
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 6. สร้างและฝึกสอนโมเดล (ใช้ Random Forest ที่แม่นยำและเสถียร)
# กำหนด max_depth เพื่อไม่ให้โมเดลจำข้อสอบ (Overfitting)
model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
model.fit(X_train_scaled, y_train)

# 7. ทดสอบความแม่นยำ
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ ฝึกสอนโมเดลสำเร็จ! ความแม่นยำ (Accuracy): {accuracy * 100:.2f}%")

# 8. บันทึกโมเดลและ Scaler ออกมาเป็นไฟล์ .pkl
joblib.dump(model, 'heart_model.pkl')
joblib.dump(scaler, 'scaler.pkl') # ต้องเซฟ scaler ไปด้วย เพื่อใช้แปลงข้อมูลที่รับมาจากหน้าเว็บ
print("✅ บันทึกไฟล์ 'heart_model.pkl' และ 'scaler.pkl' เรียบร้อยแล้ว!")

from sklearn.metrics import classification_report

# เปลี่ยนตอนให้ AI ทายผล ให้ใช้ตัวแปรที่ลงท้ายด้วย _scaled
y_pred_report = model.predict(X_test_scaled) 

# ปริ้นท์ตารางคะแนน
print(classification_report(y_test, y_pred_report))