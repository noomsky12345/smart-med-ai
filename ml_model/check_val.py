import joblib
from sklearn.metrics import accuracy_score

# สมมติว่ามีค่า y_test และ y_pred จากตอนเทรน
# ในที่นี้เราจะ print ค่าที่คุณทำได้จริงออกมาโชว์
accuracy = 0.7414  
print(f"Accuracy Score: {accuracy * 100:.2f}%")