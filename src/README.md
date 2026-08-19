# FlexiMind AI - Full Source Code Package

Bộ mã nguồn hoàn chỉnh 100% cho dự án **FlexiMind AI (Smart Active-Assistive Rehab Sleeve)** nộp thi Intel VAIIF 2026.

## 📁 Cấu trúc Mã nguồn (Source Code Structure)

```
d:\AI\Intel_Project\src\
├── esp32_firmware.ino         # Code C++ nạp vào vi điều khiển ESP32 (Arduino IDE)
├── signal_processing.py      # Module Python lọc nhiễu sEMG (Bandpass 20-450Hz) & lấy RMS, MF
├── train_openvino_model.py   # Script huấn luyện AI & Tối ưu hóa mô hình Intel OpenVINO
├── fatigue_model.pkl         # File mô hình AI đã được train sẵn
├── app_dashboard.py          # Ứng dụng Web Dashboard Streamlit hiển thị realtime & điều khiển Servo
└── requirements.txt          # Danh sách các thư viện Python cần thiết
```

---

## 🚀 Hướng dẫn chạy Thử nghiệm Giao diện Web Dashboard (Chạy ngay không cần phần cứng!)

Bạn hoàn toàn có thể **chạy thử giao diện Dashboard và mô phỏng AI ngay bây giờ** trên máy tính mà chưa cần cắm phần cứng:

### Bước 1: Mở Terminal / Command Prompt tại thư mục `src`
```bash
cd d:\AI\Intel_Project\src
```

### Bước 2: Cài đặt các thư viện Python
```bash
pip install -r requirements.txt
```

### Bước 3: Khởi chạy Giao diện Web Dashboard
```bash
streamlit run app_dashboard.py
```

Trang Web Dashboard sẽ tự động mở lên trên trình duyệt (`http://localhost:8501`). 
Bạn sẽ thấy **sóng sEMG nhảy realtime**, **thước đo điểm Effort Score** và **AI Intel OpenVINO chuyển màu XANH/ĐỎ báo động mỏi cơ** hoàn toàn tự động!

---

## 🔌 Hướng dẫn khi cắm Phần cứng thật (Linh kiện về tay)

1. Mở phần mềm **Arduino IDE**, nạp file `esp32_firmware.ino` vào bo mạch **ESP32**.
2. Cắm cáp USB nối ESP32 vào Laptop.
3. Trên giao diện Web Dashboard (`app_dashboard.py`), ở thanh bên trái (Sidebar):
   - Chuyển chế độ từ **`Simulated Data (Demo)`** ➔ sang **`Hardware ESP32 Serial`**.
   - Nhập cổng COM (Ví dụ: `COM3`).
4. Ngay lập tức, Dashboard sẽ chuyển sang đọc sóng cơ thật từ tay của bạn!
