# HỒ SƠ ĐĂNG KÝ BÀI THI CHÍNH THỨC - INTEL VIETNAM AI IMPACT FESTIVAL 2026

---

## 1. THÔNG TIN CHUNG VỀ DỰ ÁN (PROJECT OVERVIEW)
* **Tên dự án (Tiếng Anh):** RehabArm AI: AI-Powered Active-Assistive Upper-Limb Rehabilitation
* **Tên dự án (Tiếng Việt):** RehabArm AI - Hệ Thống Trợ Lực & Phục Hồi Chức Năng Chi Trên Chủ Động Bằng AI
* **Nền tảng Tối ưu hóa AI:** Intel® OpenVINO™ Toolkit
* **Lĩnh vực (Category):** AI for Accessibility & Healthcare (AI Y tế & Hỗ trợ phục hồi chức năng)
* **Đối tượng mục tiêu (Target Users):** Bệnh nhân sau đột quỵ/tai biến liệt chi trên, người bệnh chấn thương khớp khuỷu tay, người cao tuổi cần tập phục hồi chức năng chủ động tại nhà.

---

## 2. BỐI CẢNH & BÀI TOÁN THỰC TIỄN (PROBLEM STATEMENT)
1. **Tỷ lệ di chứng đột quỵ cao:** Hàng năm tại Việt Nam có hơn 200.000 ca đột quỵ mới. Hơn 80% bệnh nhân bị di chứng liệt nửa người hoặc suy giảm vận động chi trên (khớp cùi chỏ), làm mất khả năng tự ăn uống, chải đầu và sinh hoạt cá nhân.
2. **Quá tải bệnh viện & Thiếu chuyên viên:** Bệnh nhân chỉ được điều trị nội trú từ 2-4 tuần rồi phải về nhà tự tập trong "giai đoạn vàng" phục hồi thần kinh cơ (3-6 tháng đầu).
3. **Rào cản chi phí:** Các hệ thống robot phục hồi chức năng nhập ngoại có giá từ 5.000 - 50.000 USD (hàng trăm triệu đến hàng tỷ đồng); thuê chuyên viên tập tại nhà tốn 200.000đ - 500.000đ/buổi, vượt quá khả năng tài chính của đại đa số gia đình.
4. **Rủi ro chấn thương thứ cấp khi tự tập:** Người bệnh không có thiết bị đo lường lực cơ, dễ tập quá sức dẫn đến rách cơ, cứng khớp hoặc chấn thương do co thắt đột ngột (Spasm).

---

## 3. GIẢI PHÁP & KIẾN TRÚC KỸ THUẬT (SYSTEM ARCHITECTURE & INNOVATION)
RehabArm AI là hệ thống nẹp thông minh khép kín vòng phản hồi sinh học (Closed-Loop Biofeedback) kết hợp: **Cơ sinh học + IoT Edge + AI Intel OpenVINO + Y tế từ xa (Tele-Rehabilitation)**.

### 🔹 5 Tầng Công Nghệ Cốt Lõi:
1. **Tầng Cảm biến sinh học (Edge Sensing Hub):**
   - **sEMG (AD8232):** Thu nhận điện thế hoạt động cơ bắp (Action Potential) từ cơ nhị đầu ($20\text{ Hz} - 450\text{ Hz}$) để giải mã ý chí vận động trước khi cánh tay kịp di chuyển.
   - **6-DOF IMU (MPU6050):** Đo gia tốc trọng trường và vận tốc góc để tính chính xác góc gập khuỷu tay ($0^\circ - 90^\circ$).
2. **Tầng Xử lý tín hiệu số (DSP Pipeline):**
   - Lọc dải thông Bandpass (20-450Hz) + Lọc bẫy Notch Filter (50Hz), trích xuất 5 đặc trưng: RMS (lực cơ), MAV (biên độ trung bình), VAR (phương sai), ZCR (tỷ lệ qua 0) và **MDF - Median Frequency** (tần số trung vị - chỉ số vàng nhận diện mỏi cơ).
3. **Tầng Trí tuệ nhân tạo (Intel® OpenVINO™ Optimization):**
   - Mô hình phân loại mỏi cơ (Fatigue Classifier) được tối ưu sang định dạng OpenVINO IR (`.xml` & `.bin`), suy luận trực tiếp trên CPU Intel với độ trễ siêu thấp dưới 2 mili-giây.
4. **Tầng Cơ cấu chấp hành & An toàn 3 lớp (3-Tier Safety Actuation):**
   - Động cơ Servo điều khiển thanh đòn trợ lực khi bệnh nhân gập tay.
   - Cơ chế ngắt khẩn cấp (Emergency Release): Tự động quay $90^\circ$ nhả lỏng đai khi phát hiện **Mỏi cơ quá mức, Chuột rút hoặc Kẹt khớp**.
5. **Tầng Giám sát từ xa (Patient Digital Twin & Cloud):**
   - Cánh tay Hologram giải phẫu 3D chuyển động đồng bộ 60 FPS theo thời gian thực.
   - Tự động đếm số lần tập (Reps Counter) và lưu lịch sử điều trị trên Web 24/7.

---

## 4. MA TRẬN ĐÁNH GIÁ SWOT CỦA DỰ ÁN

| Yếu Tố | Chi Tiết Phân Tích |
| :--- | :--- |
| **STRENGTHS (Điểm mạnh)** | • Chi phí chế tạo PoC siêu rẻ (~300.000 VNĐ).<br>• Tối ưu hóa sâu trên phần cứng Intel bằng OpenVINO Engine.<br>• Có cơ chế bảo vệ an toàn chủ động (Safety-First Actuation).<br>• Giao diện Web Digital Twin 3D trực quan, không cần cài đặt app. |
| **WEAKNESSES (Điểm yếu)** | • Bản PoC sinh viên đang dùng Servo công suất nhỏ (chưa kéo được tải người lớn nặng).<br>• Cảm biến sEMG AD8232 có thể bị nhiễu mồ hôi nếu dán thời gian dài. |
| **OPPORTUNITIES (Cơ hội)** | • Thị trường thiết bị phục hồi chức năng thông minh tại nhà đang bùng nổ.<br>• Xu hướng số hóa y tế (Tele-medicine) sau đại dịch.<br>• Khả năng nhân rộng tại các trạm y tế xã phường vùng sâu vùng xa. |
| **THREATS (Thách thức)** | • Cần xin chứng nhận an toàn thiết bị y tế nếu muốn thương mại hóa chính thức.<br>• Thói quen ngại sử dụng công nghệ của bệnh nhân lớn tuổi. |

---

## 5. TÁC ĐỘNG XÃ HỘI (SOCIAL IMPACT - TIÊU CHÍ INTEL)
* **Bình đẳng hóa tiếp cận y tế (Democratizing Healthcare):** Biến một giải pháp robot trị giá hàng chục nghìn USD thành một thiết bị nẹp có chi phí chế tạo dưới 20 USD (~300.000 VNĐ), giúp mọi bệnh nhân nghèo ở nông thôn đều có thể tiếp cận.
* **Giảm tải cho hệ thống y tế công:** Cho phép bác sĩ theo dõi tiến độ tập luyện của hàng chục bệnh nhân tại nhà cùng lúc thông qua Web Cloud Dashboard.
* **Đóng góp vào các Mục tiêu Phát triển Bền vững (UN SDGs):**
  - **SDG 3:** Sức khỏe và cuộc sống tốt lành (*Good Health and Well-being*).
  - **SDG 10:** Giảm bất bình đẳng trong tiếp cận dịch vụ y tế cao cấp (*Reduced Inequalities*).

---

## 6. LỘ TRÌNH PHÁT TRIỂN THƯƠNG MẠI (COMMERCIAL ROADMAP)
* **Giai đoạn 1 (Hiện tại - PoC Prototype):** Hoàn thiện mạch đeo ESP32 + MPU6050 + AD8232 + Động cơ Servo + Intel OpenVINO + Web Cloud 24/7.
* **Giai đoạn 2 (Tiền thương mại hóa - 6 tháng tới):** Nâng cấp sang **Xi lanh điện tuyến tính (Linear Actuator)** hoặc **Cơ khí mềm (Soft Pneumatics)** cho lực kéo 5 - 10kg; tích hợp điện cực khô (Dry Electrodes) không cần gel dán.
* **Giai đoạn 3 (Hệ sinh thái toàn diện - 1 năm tới):** Tích hợp thêm **Module Găng tay thông minh (Smart Glove)** để hỗ trợ tập cầm nắm từng ngón tay; thử nghiệm lâm sàng tại các trung tâm phục hồi chức năng.

---

## 7. ĐƯỜNG DẪN MINH CHỨNG DỰ ÁN (PROJECT VERIFICATION LINKS)
* **Link Web Dashboard Online 24/7:** [https://rehabarm-ai.streamlit.app](https://rehabarm-ai.streamlit.app)
* **Link GitHub Mã Nguồn Dự Án:** [https://github.com/lytuyettrinh12/RehabArm-AI](https://github.com/lytuyettrinh12/RehabArm-AI)
* **Link Video Demo (2 phút trên YouTube):** `[Chèn link YouTube Video 2 phút sau khi quay]`
