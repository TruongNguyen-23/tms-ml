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
# Cài đặt thư viện cần thiết
pip install -r requirements.txt
```

---

## 📊 Dữ liệu  
- **Input:**  
  - `order_id`: Mã đơn hàng  
  - `Volume`: Thời gian lấy hàng  
  - `AreaCode`: Khu vực giao hàng  
  - `ShipToLat,ShipToLon`: Điểm giao hàng 
  - `PickUpLat,PickUpLon`: Điểm lấy hàng 
  - `Distance`: Khoảng cách di chuyển  
  - `EquipTypeNo`: Tải trọng xe cho phép  
  - `ShipToType`: Khách hàng cá nhân hoặc siêu thị  
- **Output:**  
  - `predicted_label`: Dự đoán số lượng order trong một trip 


---

## 🚀 Cách chạy dự án  
### 1️⃣ Huấn luyện mô hình  
```bash
python main.py

```
## Hoặc chỉnh sửa như sau tạo một file mới thực hiện chạy 
## Ví dụ tạo file run_main.py để xem số lượng trip
## Hoặc có thể xem qua file Template/map.html
```bash
from Src.train import trip_for_machine_learning
result = trip_for_machine_learning()
print(result)

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
Mô hình đạt **R² Score: 0.95**, giúp tối ưu hóa việc giao hàng.  

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
