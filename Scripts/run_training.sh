#!/bin/bash

# Dừng script nếu có lỗi
set -e  

# Hiển thị từng lệnh khi thực thi
set -x  

# Kích hoạt môi trường ảo (nếu dùng virtualenv hoặc conda)
source venv/bin/activate  # Nếu dùng virtualenv
# conda activate my_env   # Nếu dùng Conda

# Chạy script huấn luyện mô hình
python src/train.py --config configs/config.yaml

# Sau khi train xong, lưu mô hình vào thư mục models/
echo "Training completed. Model saved in models/"

# Tắt môi trường ảo (nếu cần)
deactivate
