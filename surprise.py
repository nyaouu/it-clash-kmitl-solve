import cv2
import os

def read_qr_opencv(folder_path):
    detector = cv2.QRCodeDetector() # ใช้ Detector ของ OpenCV โดยตรง

    files = sorted([f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))])

    for filename in files:
        img = cv2.imread(os.path.join(folder_path, filename))
        if img is None: continue

        # อ่านข้อมูล
        data, bbox, straight_qrcode = detector.detectAndDecode(img)

        if data:
            print(f"[{filename}] Data: {data}")
        else:
            print(f"[{filename}] ไม่พบ QR Code")

read_qr_opencv('./qr')
