# 🚛 Transport Management System (TMS) - Machine Learning Project

## 📌 Project Description
The **TMS (Transport Management System)** system uses **Machine Learning** to optimize freight transport, predict delivery times and optimize routes.

### 🎯 Objectives:
- Predict delivery times (**ETA - Estimated Time of Arrival**).

- Build a route optimization model.

---

## 📂 Directory Structure
```bash
tms_project/
│── data/ # Data
│── notebooks/ # Data analysis
│── src/ # Main code
│ ├── preprocess.py # Data preprocessing
│ ├── model.py # Model building
│ ├── train.py # Model training
│ ├── predict.py # Delivery time prediction
│── models/ # Store trained model
│── reports/ # Reports and results
│── logs/ # Run logs
│── tests/ # Unit test model testing
│── configs/ # Model parameter configuration file
│── requirements.txt # Required libraries
│── README.md # Documentation
```

---

## 🛠 Environment setup
```bash
# Install required libraries
pip install -r requirements.txt
```

---

## 📊 Data
- **Input:**

- `OrderId`: Order code
- `Volume`: Vehicle Load M3
- `AreaCode`: Delivery area
- `ShipToLat,ShipToLon`: Delivery point
- `PickUpLat,PickUpLon`: Pickup point
- `Distance`: Distance way of moving
- `EquipTypeNo`: Allowed vehicle load
- `ShipToType`: Individual customers or supermarkets
- **Output:**
- `PredictedLabel`: Predict the number of orders in a trip

---

## 🚀 How to run the project
### 1️⃣ Train the model
```bash
python main.py

```
## Or edit as follows to create a new file to run
## For example, create a run_main.py file to see the number of trips
## Or you can look through the Template/map.html file
```bash
from Src.train import trip_for_machine_learning
result = trip_for_machine_learning()
print(result)

```

<!-- ### 2️⃣ Predict delivery time
```bash
python src/predict.py --order_id 12345
``` -->

---

## 🔍 Model used
- **Decision Tree Regressor**: Predict optimal number of trips on input data.

---

<!-- ## ✅ Testing
Run unit test to test the model:
```bash
pytest tests/
``` -->

---

## 📈 Results
The model achieved **R² Score: 0.95**, helping to optimize delivery.

---

<!-- ## 🔧 Configuration
Change model parameters in `configs/config.yaml`:
```yaml
model:
name: "RandomForest"
max_depth: 10
n_estimators: 100
``` -->

---

## 📌 Contribute
If you would like to contribute, please open a **Pull Request** or contact us via email nguyenkhoatruong231199@gmail.com.

---

## 📜 License
This project is licensed under the **MIT License**.