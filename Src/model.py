from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from collections import Counter
from dotenv import load_dotenv
from Src.logger import *
import pickle
import os

load_dotenv()
LIMIT_TRUCK = int(os.getenv('LIMIT_TRUCK'))

def model_train_test(data, orders_data, key):
    X = data[key]
    y = data['Label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
    
    train_logger.info("Start training")
    train_logger.info(f"Sample data train = {len(X_train)}, Sample data test = {len(X_test)}")

    # Manual split data train and test
    # X_train, y_train, X_test, y_test = X[:80], y[:80], X[80:], y[80:]
    
    # Function find max depth
    temp_number = {}
    best_accuracy = 0
    best_depth = None
    
    for depth in range(1, 10):
        clf = DecisionTreeRegressor(max_features = 'sqrt', max_depth = depth, random_state = 42)
        clf.fit(X_train, y_train)
        train_logger.info(f"Hyperparameters: max_features='sqrt', max_depth = {depth}, random_state = 42")
        
        accuracy = clf.score(X_test, y_test) * 100
        orders_data["PredictedLabel"] = clf.predict(orders_data[key])
        number_trip = len(group_data_predict_with_limit(orders_data))
        
        train_logger.info(f"Max Depth: {depth}, Accuracy: {accuracy}")
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_depth = depth
        temp_number[depth] = number_trip
    
    max_depth = find_max_depth(temp_number)
    train_logger.info(f"Max depth: {max_depth}, Temp Number: {temp_number}, Best Depth: {best_depth}")
    
    model = DecisionTreeRegressor(max_features = 'sqrt', max_depth = best_depth, random_state = 42)
    model.fit(X_train, y_train)
    train_logger.info(f"Success training")
   
    # Predict Model
    y_pred = model.predict(X_test)

    # Evaluate Model
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
       
    eval_logger.info(f"Evaluate Model: MAE: {mae}, MSE: {mse}, R2: {r2} \n\n")
    save_model(model)
    
    train_logger.info("Save data to file model.pkl \n\n")
    
    return model
def group_data_predict_with_limit(orders_data):
    result = []
    for label, group in orders_data.groupby('PredictedLabel'):
        current_group = []
        current_weight = 0

        for _, row in group.iterrows():
            if current_weight + row['Volume'] > LIMIT_TRUCK:
                result.append(current_group)
                current_group = []
                current_weight = 0
            current_group.append(row.to_dict())
            current_weight += row['Volume']

        if current_group:
            result.append(current_group)
            
    return result

def find_max_depth(data):
    value_counts = Counter(data.values())
    duplicate = [key for key, count in value_counts.items() if count > 1]
    if duplicate:
        for item in duplicate:
            keys_with_number = [key for key, value in data.items() if value == item]
            max_key = max(keys_with_number) if keys_with_number else None
    else:
        max_key = min(data)
        
    return max_key

def save_model(model):
    
    model_pkl_file = "Models/model.pkl" 
     
    with open(model_pkl_file, 'wb') as file:  
        pickle.dump(model, file)