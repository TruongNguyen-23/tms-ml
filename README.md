# 🚛 Transport Management System (TMS) - Machine Learning Project  

## 📌 Mô tả dự án  
Hệ thống **TMS (Transport Management System)** sử dụng **Machine Learning** để tối ưu hóa vận chuyển hàng hóa, dự đoán thời gian giao hàng và tối ưu tuyến đường.  

### 🎯 Mục tiêu:  
- Dự đoán thời gian giao hàng (**ETA - Estimated Time of Arrival**).  
- Xây dựng mô hình tối ưu hóa tuyến đường.  

---

## 📂 Cấu trúc thư mục  
```bash
 tms_project/
 │── data/                     # Dữ liệu
 │── notebooks/                # Phân tích dữ liệu
 │── src/                      # Code chính
 │   ├── preprocess.py         # Tiền xử lý dữ liệu
 │   ├── model.py              # Xây dựng mô hình
 │   ├── train.py              # Huấn luyện mô hình
 │   ├── predict.py            # Dự đoán thời gian giao hàng
 │── models/                   # Lưu trữ mô hình đã huấn luyện
 │── reports/                  # Báo cáo và kết quả
 │── logs/                     # Log quá trình chạy
 │── tests/                    # Unit test kiểm thử mô hình
 │── configs/                  # File cấu hình tham số mô hình
 │── requirements.txt          # Thư viện cần thiết
 │── README.md                 # Tài liệu hướng dẫn
```

---

## 🛠 Cài đặt môi trường  
```bash
# # Tạo môi trường ảo
# python -m venv venv
# source venv/bin/activate  # MacOS/Linux
# venv\Scripts\activate     # Windows

# Cài đặt thư viện cần thiết
pip install -r requirements.txt
```

---

## 📊 Dữ liệu  
- **Input:**  
  - `order_id`: Mã đơn hàng  
  - `pickup_time`: Thời gian lấy hàng  
  - `delivery_time`: Thời gian giao hàng thực tế  
  - `distance`: Khoảng cách di chuyển  
  - `traffic_conditions`: Điều kiện giao thông  
  - `weather`: Thời tiết tại thời điểm giao hàng  
- **Output:**  
  - `predicted_eta`: Thời gian dự đoán giao hàng  

<!-- 📌 **Lưu ý:** Dữ liệu gốc cần được đặt trong thư mục `data/raw/`.   -->

---

## 🚀 Cách chạy dự án  
### 1️⃣ Huấn luyện mô hình  
```bash
python src/train.py --epochs 100 --lr 0.01
```
<!-- ### 2️⃣ Dự đoán thời gian giao hàng  
```bash
python src/predict.py --order_id 12345
``` -->

---

## 🔍 Mô hình sử dụng  
- **Decision Tree Regressor**: Dự đoán thời gian giao hàng dựa trên dữ liệu đầu vào.  

---

<!-- ## ✅ Kiểm thử  
Chạy unit test để kiểm tra mô hình:  
```bash
pytest tests/
``` -->

---

## 📈 Kết quả  
Mô hình đạt **R² Score: 0.85**, giúp tối ưu hóa việc giao hàng chính xác hơn.  

---

<!-- ## 🔧 Cấu hình  
Thay đổi tham số mô hình trong `configs/config.yaml`:  
```yaml
model:
  name: "RandomForest"
  max_depth: 10
  n_estimators: 100
``` -->

---

## 📌 Đóng góp  
Nếu bạn muốn đóng góp, hãy mở **Pull Request** hoặc liên hệ qua email nguyenkhoatruong231199@gmail.com.  

---

## 📜 Giấy phép  
Dự án này tuân theo giấy phép **MIT License**.  
