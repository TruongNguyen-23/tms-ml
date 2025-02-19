from Src.feature_engineering import *
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
    # df['Qty'] = df.groupby(key)['Qty'].transform('sum')
    # df['Weight'] = df.groupby(key)['Weight'].transform('sum')
    return df

def encode_predict_value_features(df):
    df['Label'] = df['TripNo'].factorize()[0]
    return df
def data_history_processing():
    key_trip_drop = ['BatchGroupNo','TripType','OrderNo','OrderNote','CompanyCode','Priority']
    data = DataLoader().load_excel('dataSet.xlsx')
    df_trip = encode_features(data,"TripNo")
    df_trip = encode_predict_value_features(df_trip)
    df_trip.drop(key_trip_drop, axis=1, inplace=True)
    # trip_data = FeatureEngineering().feature_engineering(trip_data)
    df_trip = df_trip.dropna()
    print('df_trip',df_trip)
    return df_trip    
   
def data_predict_processing():
    
    orders_data = DataLoader().load_excel('dataOrders.xlsx')
    
    # orders_data = DataLoader().load_excel('dataValidate.xlsx')
    # orders_data = DataLoader().load_excel('dataTest.xlsx')
    
    split_orders = []
    
    for index, row in orders_data.iterrows():
        order = row.to_dict()
        split_result = split_order(order, LIMIT_TRUCK)
        split_orders.extend(split_result)
        
    df_orders = pd.DataFrame(split_orders)
    df_orders = encode_features(df_orders,"OrderId")

    return df_orders

