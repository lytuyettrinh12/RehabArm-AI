# HƯỚNG DẪN CHI TIẾT TỪNG BƯỚC THỰC HIỆN DỰ ÁN FLEXIMIND AI (REHAB BRACE)

Tài liệu này hướng dẫn chi tiết từng bước từ lắp ráp phần cứng, viết code vi điều khiển, huấn luyện AI với Intel OpenVINO, dựng Giao diện Dashboard cho đến hoàn thiện Video nộp thi Intel VAIIF 2026.

---

## 📍 GIAI ĐOẠN 1: LẮP RÁP PHẦN CỨNG (HARDWARE ASSEMBLY)
*Thời gian thực hiện: Ngày 1 - 2 (Ngay khi nhận đủ linh kiện)*

### 1.1 Sơ đồ nối dây chi tiết (Pinout Mapping)

Nối tất cả linh kiện vào **ESP32** trên Bo test mạch (Breadboard) theo bảng sau:

| Linh kiện | Chân linh kiện | Chân cắm trên ESP32 | Ghi chú |
|---|---|---|---|
| **Cảm biến sEMG (AD8232)** | `VCC` | `3V3` | Nguồn 3.3V |
| | `GND` | `GND` | Đất |
| | `OUTPUT` | `VP` (hoặc `GPIO 36`) | Đọc tín hiệu Analog điện cơ |
| **Cảm biến IMU (MPU6050)** | `VCC` | `3V3` | Nguồn 3.3V |
| | `GND` | `GND` | Đất |
| | `SDA` | `GPIO 21` | Dữ liệu I2C |
| | `SCL` | `GPIO 22` | Xung nhịp I2C |
| **Động cơ Servo (SG90)** | `VCC` (Dây Đỏ) | `5V` (hoặc `VIN`) | Nguồn 5V |
| | `GND` (Dây Nâu) | `GND` | Đất |
| | `PWM` (Dây Cam) | `GPIO 4` | Điều khiển góc quay |

### 1.2 Gắn lên đai đeo tay
1. Đeo **Băng đai thể thao** vào cánh tay/khuỷu tay.
2. Dùng băng dính gai (Velcro) hoặc dây rút nhựa cố định ESP32, MPU6050 lên bề mặt đai vải.
3. Dán **3 miếng điện cực y tế (Electrode pads)** lên phần bắp tay (Biceps/Forearm):
   - **Miếng 1 & 2 (Đỏ & Vàng):** Dán trực tiếp dọc theo nhóm cơ muốn đo.
   - **Miếng 3 (Xanh lá - Reference):** Dán vào phần xương không có cơ (như khuỷu tay hoặc cổ tay) để làm mốc nhiễu.

---

## 📍 GIAI ĐOẠN 2: LẬP TRÌNH NẠP CODE ESP32 (DATA STREAMING)
*Thời gian thực hiện: Ngày 3 - 4*

1. Tải phần mềm **Arduino IDE** về máy tính.
2. Cài đặt Board **ESP32** và thư viện `Adafruit MPU6050`.
3. Lập trình ESP32 thực hiện nhiệm vụ:
   - Đọc liên tục giá trị sEMG (từ 0 đến 4095).
   - Đọc gia tốc 3 trục X, Y, Z từ MPU6050.
   - Gửi dữ liệu dạng chuỗi JSON/CSV qua cổng Serial USB lên máy tính với tốc độ `115200 baud`.

---

## 📍 GIAI ĐOẠN 3: XỬ LÝ TÍN HIỆU & HUẤN LUYỆN AI VỚI INTEL OPENVINO
*Thời gian thực hiện: Ngày 5 - 9 (Quan trọng nhất để lấy điểm thi)*

### 3.1 Thu thập dữ liệu Huấn luyện (Data Collection)
* Người đeo gồng tay bình thường trong 10-15 phút -> Ghi nhãn `0` (KHOẺ/NORMAL).
* Người đeo tập liên tục cho đến khi cơ bắt đầu mỏi/co giật nhẹ -> Ghi nhãn `1` (MỎI CƠ/FATIGUE).

### 3.2 Tiền xử lý dữ liệu bằng Python
1. **Lọc nhiễu (Bandpass Filter):** Dùng SciPy lọc lấy dải tần số cơ bắp từ **20Hz - 450Hz**, loại bỏ nhiễu điện lưới 50Hz.
2. **Trích xuất đặc trưng (Feature Extraction):** 
   - Biến đổi RMS (Root Mean Square - Căn bậc hai trung bình).
   - MAV (Mean Absolute Value).
   - Tần số trung vị (Median Frequency - MF): *Khi cơ mỏi, tần số sóng điện cơ sẽ dịch chuyển về dải tần số thấp*.

### 3.3 Huấn luyện Mô hình AI & Tối ưu bằng Intel OpenVINO
1. **Train mô hình:** Dùng Scikit-Learn hoặc PyTorch huấn luyện mô hình phân loại (như Random Forest hoặc Neural Network nhẹ).
2. **Convert sang Intel OpenVINO:**
   - Sử dụng công cụ **Intel OpenVINO Model Converter**.
   - Chuyển đổi mô hình thành định dạng `.xml` và `.bin` (OpenVINO IR format).
   - Chạy suy luận (Inference Engine) bằng **OpenVINO Runtime** trên CPU Intel máy tính để đảm bảo độ trễ siêu thấp (<10ms).

---

## 📍 GIAI ĐOẠN 4: XÂY DỰNG GIAO DIỆN THEO DÕI REAL-TIME (DASHBOARD)
*Thời gian thực hiện: Ngày 10 - 13*

Sử dụng thư viện **Streamlit** (Python) hoặc **Web React** để tạo ứng dụng hiển thị:
1. **Đồ thị sóng điện cơ sEMG realtime:** Nhấp nháy liên tục khi người dùng cử động tay.
2. **Thước đo Effort Score (Mức độ nỗ lực):** Tính theo % dựa trên biên độ tín hiệu.
3. **Thẻ trạng thái AI (AI Status Card):**
   - 🟢 **Màu Xanh:** "Trạng thái An Toàn - Tiếp tục tập luyện".
   - 🔴 **Màu Đỏ Nhấp Nháy (Cảnh báo mỏi cơ):** "CẢNH BÁO MỎI CƠ - Yêu cầu nghỉ ngơi!".
4. **Bảng dữ liệu Tele-rehab cho Bác sĩ:** Ghi lại tổng số lần lặp bài tập và thời gian đạt ngưỡng mỏi.

---

## 📍 GIAI ĐOẠN 5: ĐÓNG VÒNG PHẢN HỒI THỰC THỂ (CLOSED-LOOP CONTROL)
*Thời gian thực hiện: Ngày 14 - 15*

1. Khi Python AI (OpenVINO) phát hiện trạng thái **FATIGUE (Mỏi cơ)**:
2. Python tự động gửi một lệnh ký tự `STOP` qua cổng Serial xuống lại ESP32.
3. ESP32 nhận ký tự `STOP` -> Ngay lập tức điều khiển **Động cơ Servo SG90 quay 90 độ** (giả lập hành động nới lỏng đai/nhả lực cản để bảo vệ khớp tay bệnh nhân).

---

## 📍 GIAI ĐOẠN 6: QUAY VIDEO DEMO 2 PHÚT & NỘP BÀI THI
*Thời gian thực hiện: Ngày 16 - 18 (Trước ngày 25/08)*

### Kịch bản Video Demo 2 phút (Video Script):
* **0:00 - 0:20 (Đặt vấn đề):** Hình ảnh bệnh nhân khó khăn khi phục hồi chức năng & nguy cơ chấn thương do tập quá sức.
* **0:20 - 0:45 (Giới thiệu FlexiMind AI):** Cận cảnh thiết bị đeo tay thông minh + Giới thiệu kiến trúc cảm biến sEMG, IMU và Intel OpenVINO.
* **0:45 - 1:30 (DEMO THỰC TẾ - Trọng tâm):**
  - Người đeo thực hiện động tác -> Sóng sEMG hiện realtime trên Dashboard.
  - Người đeo gồng mỏi cơ -> AI OpenVINO phát hiện mỏi cơ -> Dashboard chuyển màu Đỏ báo động -> Động cơ Servo tự động xoay nhả lực.
* **1:30 - 2:00 (Tác động xã hội & Kết luận):** Tối ưu chi phí (< 20 USD), hỗ trợ bác sĩ theo dõi từ xa, mang lại tự do cho bệnh nhân.

---

📌 *Tài liệu này đã được lưu vào thư mục dự án của bạn dưới tên: `detailed_implementation_guide.md`.*
