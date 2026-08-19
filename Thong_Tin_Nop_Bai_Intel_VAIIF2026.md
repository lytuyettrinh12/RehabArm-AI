# HỒ SƠ MẪU ĐĂNG KÝ BÀI THI - INTEL VIETNAM AI IMPACT FESTIVAL 2026

Tài liệu này tổng hợp toàn bộ nội dung câu trả lời chuẩn hóa dành cho Form nộp bài thi cuộc thi Intel VAIIF 2026. Bạn chỉ cần copy/paste nội dung này vào Google Form nộp bài.

---

### 1. THÔNG TIN CHUNG VỀ DỰ ÁN (PROJECT OVERVIEW)
* **Tên dự án (Tiếng Anh):** FlexiMind AI - Smart Active-Assistive Rehab Sleeve powered by Intel OpenVINO
* **Tên dự án (Tiếng Việt):** FlexiMind AI - Đai nẹp đeo tay thông minh hỗ trợ phục hồi chức năng chủ động dựa trên AI tại biên
* **Lĩnh vực (Category):** AI for Accessibility & Healthcare (AI cho Y tế & Hỗ trợ người khuyết tật)
* **Đối tượng mục tiêu (Target Users):** Bệnh nhân phục hồi sau đột quỵ/tai biến, bệnh nhân chấn thương cột sống/chi trên, người cao tuổi cần tập vật lý trị liệu tại nhà.

---

### 2. TÓM TẮT VẤN ĐỀ XÃ HỘI (PROBLEM STATEMENT)
Hiện nay, hàng triệu bệnh nhân sau đột quỵ hoặc chấn thương chi trên gặp rất nhiều khó khăn trong việc phục hồi chức năng vận động:
1. **Chi phí đắt đỏ:** Các thiết bị robot phục hồi chức năng (exoskeleton) hiện nay trên thị trường có giá từ $5,000 - $50,000 USD, quá tầm tay với đa số người dân Việt Nam.
2. **Nguy cơ chấn thương thứ cấp:** Khi tự tập tại nhà không có bác sĩ giám sát, bệnh nhân dễ cố quá sức dẫn đến co giật cơ (spasm) hoặc tổn thương khớp vĩnh viễn.
3. **Thiếu dữ liệu theo dõi từ xa:** Bác sĩ không có công cụ đo lường chính xác tiến trình hồi phục thực tế của bệnh nhân khi họ tập luyện tại nhà.

---

### 3. GIẢI PHÁP AI & ĐỔI MỚI CÔNG NGHỆ (AI SOLUTION & INNOVATION)
FlexiMind AI là hệ thống nẹp đeo tay thông minh tích hợp Cảm biến sinh học đa phương thức (Multimodal Sensing) và AI tại biên (Edge AI):

* **Thu thập dữ liệu đa phương thức (Multi-Modal Sensing Hub):**
  - **Cảm biến sEMG (Surface Electromyography):** Thu xung điện cơ bắp thời gian thực để giải mã ý định vận động.
  - **Cảm biến IMU (MPU6050):** Đo vận tốc góc và hành trình di chuyển của khuỷu tay.

* **Thuật toán AI Dự đoán mỏi cơ (AI Fatigue Detection Engine):**
  - Lọc nhiễu dải tần 20Hz - 450Hz, tính toán biến đổi RMS và Tần số trung vị (Median Frequency).
  - Mô hình AI nhận diện sự sụt giảm tần số ngầm khi cơ bắp kiệt sức với độ chính xác >90%.

* **Vòng lặp phản hồi thực thể (Closed-Loop Physical Actuation):**
  - Khi AI phát hiện ngưỡng nguy hiểm (Co giật/Mỏi nặng), hệ thống tự động phát lệnh cho Động cơ Servo xoay 90° để nới lỏng đai tay ngay lập tức, ngắt lực cản bảo vệ khớp bệnh nhân.

---

### 4. ỨNG DỤNG CÔNG NGHỆ INTEL (INTEL TECH INTEGRATION - METRIC 03)
Dự án tích hợp sâu bộ công cụ **Intel OpenVINO Toolkit**:
* **Intel OpenVINO Model Optimizer:** Chuyển đổi mô hình AI huấn luyện sang định dạng tối ưu IR (.xml & .bin).
* **Intel OpenVINO Runtime Engine:** Chạy suy luận (Inference) trực tiếp trên phần cứng CPU Intel của thiết bị với độ trễ cực thấp (<10ms).
* Việc sử dụng Intel OpenVINO giúp hệ thống phản ứng ngắt lực cản tức thì, đảm bảo an toàn tuyệt đối cho bệnh nhân mà không phụ thuộc vào kết nối Internet/Cloud.

---

### 5. TÁC ĐỘNG XÃ HỘI & TÍNH KHẢ THI (SOCIAL IMPACT & FEASIBILITY - METRIC 01)
* **Chi phí siêu rẻ (< $20 USD ~ 380.000 VNĐ):** Giảm chi phí sản xuất gấp 100 lần so với thiết bị thương mại, giúp mọi bệnh nhân nghèo đều có thể tiếp cận.
* **Phục hồi nhanh gấp 2-3 lần:** Áp dụng nguyên lý y khoa "Trợ lực theo nhu cầu" (Assistance-as-Needed), kích thích khả năng tái tạo thần kinh (Neuroplasticity).
* **Kết nối Bác sĩ từ xa (Tele-rehab):** Tự động đồng bộ tiến trình tập luyện lên Web Dashboard cho bác sĩ theo dõi và điều chỉnh phác đồ điều trị.

---

### 6. DANH SÁCH LINK NỘP BÀI (SUBMISSION LINKS)
* **Link Video Demo (2 phút trên YouTube):** `[Chèn link YouTube Video 2 phút tại đây]`
* **Link GitHub Source Code Public:** `[Chèn link GitHub repository tại đây]`
* **Link Web Dashboard Demo:** `[Chèn link Web Demo/Streamlit tại đây]`
