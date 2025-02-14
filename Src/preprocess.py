from Src.split_data_order import *
from sklearn import preprocessing
from dotenv import load_dotenv
from Src.data_loader import *
import pandas as pd
import numpy as np
import os

# Create pipline here

load_dotenv()
label_encoder = preprocessing.LabelEncoder()
LIMIT_TRUCK = int(os.getenv('LIMIT_TRUCK'))

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    return 6371 * 2 * np.arcsin(np.sqrt(a))

def encode_features(df, key):
    df['ShipToType'] = label_encoder.fit_transform(df['ShipToType'].astype(str))
    df['AreaCode'] = label_encoder.fit_transform(df['AreaCode'].astype(str))
    df['Distance'] = haversine(df['PickupLat'], df['PickupLon'], df['ShipToLat'], df['ShipToLon'])
    df['EquipTypeNo'] = df.groupby(key)['Volume'].transform('sum')
    return df

def encode_predict_value_features(df):
    df['Label'] = df['TripNo'].factorize()[0]
    return df
def data_history_processing():
    trip_data = DataLoader().load_excel('dataSet.xlsx')
    trip_data = encode_features(trip_data,"TripNo")
    trip_data = encode_predict_value_features(trip_data)
    trip_data = trip_data.dropna()
    return trip_data
   
def data_predict_processing():
    orders_data = DataLoader().load_excel('dataOrders.xlsx')
    # orders_data = DataLoader().load_excel('dataValidate.xlsx')
    split_orders = []
    
    for index, row in orders_data.iterrows():
        order = row.to_dict()
        split_result = split_order(order, LIMIT_TRUCK)
        split_orders.extend(split_result)
        
    orders_data = pd.DataFrame(split_orders)
    orders_data = encode_features(orders_data,"OrderId")
    return orders_data

