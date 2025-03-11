from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from collections import Counter
from dotenv import load_dotenv
from Src.logger import *
import pickle
import optuna
import json
import os

load_dotenv()
LIMIT_TRUCK = int(os.getenv('LIMIT_TRUCK'))

def model_train_test(data, orders_data, key):
    X = data[key]
    y = data['Label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
    # Manual split data train and test
    # X_train, y_train, X_test, y_test = X[:80], y[:80], X[80:], y[80:]
    
    train_logger.info("Start training")
    train_logger.info(f"Sample data train = {len(X_train)}, Sample data test = {len(X_test)}")


    # model = model_lgbmregressor(X_train, X_test, y_train, y_test)
    model = model_decision_tree_regressor(X_train, X_test, y_train, y_test)
    # model = model_xgboost()
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
def model_xgboost():          
    # Model XGBoost
    model = XGBRegressor(
        n_estimators=100,             
        learning_rate=0.01,           
        max_depth=1,                  
        min_child_weight=1,          
        gamma=0.1,                    
        subsample=0.8,               
        colsample_bytree=0.8,         
        reg_alpha=0.01,               
        reg_lambda=1,                 
        objective='reg:squarederror', 
        scale_pos_weight=1,           
        random_state = 42,            
        n_jobs = -1                    
    )  
    return model

def model_decision_tree_regressor(X_train, X_test, y_train, y_test):
    # Model DecisionTreeRegressor
    # Function find max depth
    best_accuracy = 0
    best_depth = None
    
    for depth in range(1, 10):
        clf = DecisionTreeRegressor(max_depth = depth, random_state = 42, max_features = "sqrt")
        clf.fit(X_train, y_train)
        accuracy = clf.score(X_test, y_test) * 100
        train_logger.info(f"Hyperparameters:{clf.get_params()}")
        train_logger.info(f"Max Depth: {depth}, Accuracy: {accuracy}")
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_depth = depth
    
    train_logger.info(f"Best Depth: {best_depth}")
    
    model = DecisionTreeRegressor(max_depth = best_depth, random_state = 42, max_features = "sqrt")
    return model

def model_lgbmregressor(X_train, X_test, y_train, y_test):
    param_model = optimize(X_train, X_test, y_train, y_test)
    model = LGBMRegressor(**param_model)
    return model
def optimize(X_train, X_test, y_train, y_test, n_trials=1):
        def objective(trial):
        
            param = {
                'random_state': 48,
                'early_stopping_round': 200,
                'verbose': -1,
                'n_jobs': 0,
                'n_estimators': trial.suggest_int('n_estimators', 5000, 10000),
                'reg_alpha': trial.suggest_float('reg_alpha', 1e-3, 10.0),
                'reg_lambda': trial.suggest_float('reg_lambda', 1e-3, 10.0),
                'colsample_bytree': trial.suggest_categorical('colsample_bytree', [0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]),
                'subsample': trial.suggest_categorical('subsample', [0.4,0.5,0.6,0.7,0.8,1.0]),
                'learning_rate': trial.suggest_float('learning_rate', 0.006, 0.02),
                'max_depth': trial.suggest_int('max_depth', 10, 100),
                'num_leaves' : trial.suggest_int('num_leaves', 1, 1000)}

            model = LGBMRegressor(**param)  
            model.fit(
                X_train, y_train,
                eval_set=[(X_test,y_test)], verbose = -1
            )
            
            predict = model.predict(X_test)
            r2 = r2_score(y_test, predict)
            
            return r2
        study = optuna.create_study(direction='maximize')
        study.optimize(lambda trial: objective(trial), n_trials=n_trials)

        print('Number of finished trials:', len(study.trials))

        best_params = study.best_trial.params
        print('Best params', best_params)
        
        return best_params
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

# def find_max_depth(data):
#     value_counts = Counter(data.values())
#     duplicate = [key for key, count in value_counts.items() if count > 1]
#     if duplicate:
#         for item in duplicate:
#             keys_with_number = [key for key, value in data.items() if value == item]
#             max_key = max(keys_with_number) if keys_with_number else None
#     else:
#         max_key = min(data)
        
#     return max_key

def save_model(model):
    
    model_pkl_file = "Models/model.pkl" 
     
    with open(model_pkl_file, 'wb') as file:  
        pickle.dump(model, file)