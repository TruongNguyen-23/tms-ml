from dotenv import load_dotenv
from Src.preprocess import *
from random import randbytes
from jinja2 import Template
from Src.map_view import *
from Src.model import *
from Vrp.vrp import *
import pickle
import os
import json



load_dotenv()
FEATURE_KEY = ['Volume','AreaCodes','ShipToLat', 'ShipToLon','PickupLat', 'PickupLon','Distance','EquipTypeNo','ShipToTypes']
LIMIT_TRUCK = int(os.getenv('LIMIT_TRUCK'))
DATA_COLOR = "color.json"

def training_data():
    history_data = data_history_processing()

    orders_data = data_predict_processing()

    model_file = "Models/model.pkl"
    
    # if model_file:
    #     with open(model_file, 'rb') as file:
    #         model = pickle.load(file)
    # else:
    model = model_train_test(history_data, orders_data, FEATURE_KEY)
   
    orders_data['PredictedLabel'] = model.predict(orders_data[FEATURE_KEY])
    
    return orders_data

def get_color_template():
    color = []
    data = json.load(open(DATA_COLOR))
    for items in data["colors"]:
        color.append(items["code"]["hex"])
    return color

def random_color_for_trip(number):
    while len(get_color_template()) < number:
        color_random = f"#{randbytes(3).hex()}"
        template_color = {
            "color": "",
            "category": "",
            "type": "primary",
            "code": {
                "rgba": [255, 0, 0, 1],
                "hex": color_random
                }
            }
        with open(DATA_COLOR, 'r') as file:
            data = json.load(file)
        if template_color not in data["colors"]:
            data['colors'].append(template_color)
        with open(DATA_COLOR, 'w') as file:
            json.dump(data, file)
            
def trip_for_machine_learning():
    data_trip = {}
    result = []
    orders_data = training_data()
    for label, group in orders_data.groupby('PredictedLabel'):
        current_group = []
        current_weight = 0

        for _, row in group.iterrows():
            # if current_weight + row['Volume'] > LIMIT_TRUCK:
            #     result.append(current_group)
            #     current_group = []
            #     current_weight = 0
            current_group.append(row.to_dict()) 
            # current_weight += row['Volume']

        if current_group:
            result.append(current_group)

    trip_no = []
    data_format = []
    color_maker = get_color_template()
    trip_split = []
    
    # for index,item in enumerate(result):
    #     total = sum([value['Volume'] for value in item])
    #     total_point = list(set([(value["ShipToLat"],value["ShipToLon"]) for value in item]))
    #     num_vehicles = round(total / LIMIT_TRUCK)
        
    #     if  total > LIMIT_TRUCK and len(total_point) > 1:
    #         item_split = solve_vrp(item, num_vehicles, LIMIT_TRUCK)
    #         if item_split:
    #             trip_split.extend(item_split)
    #             del result[index]
    #         else:
    #             break
    #     else:
    #         current_weight = 0
    #         current_group_ = []
    #         for value_ in item:
    #             if current_weight + value_['Volume'] > LIMIT_TRUCK:
    #                 trip_split.append(current_group_)
    #                 current_group_ = []
    #                 current_weight = 0
    #             current_weight += value_['Volume']
            
    
    # for index in range(len(result) - 1, -1, -1):  # Duyệt từ cuối lên
    #     item = result[index]
    #     total = sum(value["Volume"] for value in item)
    #     num_vehicles = round(total / LIMIT_TRUCK)
    #     if total > LIMIT_TRUCK:
    #         item_split = solve_vrp(item, num_vehicles, LIMIT_TRUCK)
    #         if item_split:
    #             trip_split.extend(item_split)
    #             del result[index]  

    index = 0
    while index < len(result):
        item = result[index]
        total = sum(value["Volume"] for value in item)
        total_point = list(set([(value["ShipToLat"],value["ShipToLon"]) for value in item]))
        num_vehicles = round(total / LIMIT_TRUCK)
        if total > LIMIT_TRUCK:
            if total < 100:
                item_split = run_solve_vrp_with_timeout(item, num_vehicles, LIMIT_TRUCK)
                if item_split and len(total_point) > 1:
                    trip_split.extend(item_split)
            else:
                current_weight = 0
                current_group_ = []
                # sorted data item with distance to pickup point
                
                for value_ in item:
                    if current_weight + value_['Volume'] > LIMIT_TRUCK:
                        if current_group_:
                            trip_split.append(current_group_)
                        current_group_ = []
                        current_weight = 0
                    current_group_.append(value_)
                    current_weight += value_['Volume']
                if current_group_:
                    result.append(current_group_)
            del result[index]
            continue
        index += 1

            
    result.extend(trip_split)
    # print('result',result)
    # convent data in map or api:
    for index,item in enumerate(result):
        
        trip_no.append('Trip #{}'.format(index+1))
        orders = []
        for items in item:
            orders_datas = [
                items["OrderNo"],
                items["ShipToLat"],
                items["ShipToLon"],
                items["ShipToCode"],
                items["ShipTo"],
                items["OrderId"],
                str(index),
                items["ShipToType"]
            ]
            orders.append(orders_datas)
        data_format.append(orders)
    html = MapCluster().show_data_on_map(trip_no, data_format, color_maker[:len(trip_no)])
    save_data_to_file(html)
    
    for index, items in enumerate(result):
        if items:
            data_trip[f"Trip {index + 1}"] = items
            print('toatl trip',f"Trip {index + 1}",sum([item['Volume'] for item in items]))
        
    return data_trip

def save_data_to_file(data):
    file_name = "Templates/map.html"
    try:
        with open(file_name, "r") as file:
            print(f"Cleared old content in {file_name}")
    except FileNotFoundError:
        print(f"File {file_name} does not exist")
    with open(file_name, "w") as file:
        file.write(data)
        print(f"Written content{file_name}")
 