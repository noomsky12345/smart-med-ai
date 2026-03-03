import joblib
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score

# ระบุที่อยู่ไฟล์โมเดลให้ถูกต้องตามโครงสร้างของคุณ
model = joblib.load('ml_model/heart_model.pkl') 

# ตัวอย่างการจำลองค่าเพื่อดูรูปแบบรายงาน (ในงานจริงคุณจะใช้ y_test จากการ split ข้อมูล)
y_test = [0, 1, 0, 1, 1, 0, 1, 0, 1, 0] 
y_pred = [0, 1, 1, 1, 0, 0, 1, 0, 1, 0] 

print("=== Model Performance Report ===")
print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print("\nDetailed Classification Report:")
print(classification_report(y_test, y_pred))    