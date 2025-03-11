from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import numpy as np
import threading

def create_distance_matrix(data):
    locations = []
    for item in data:
        point = [item['ShipToLat'],item['ShipToLon']]
        pick_up = [item["PickupLat"],item['PickupLon']]
        # if point not in locations:
        locations.append(point)
        if pick_up not in locations:
            locations.insert(0,pick_up)
    num_locations = len(locations)
    distance_matrix = np.zeros((num_locations, num_locations))
    
    def haversine(lat1, lon1, lat2, lon2):
        from math import radians, cos, sin, sqrt, atan2
        R = 6371  # Earth radius in km
        dlat, dlon = radians(lat2 - lat1), radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        return round(int(2 * R * atan2(sqrt(a), sqrt(1-a))))
    
    for i in range(num_locations):
        for j in range(num_locations):
            if i != j:
                distance_matrix[i][j] = haversine(*locations[i], *locations[j])
    
    return distance_matrix.tolist()

def solve_vrp(data, num_vehicles, capacity, result_container = []):
    try:
        distance_matrix = create_distance_matrix(data)
        # print('distance_matrix',distance_matrix)
        volumes = [0] + [order['Volume'] for order in data]  # Volume constraints

        manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, 0)
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int(distance_matrix[from_node][to_node])

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            return int(volumes[from_node])

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(demand_callback_index, 0, [capacity] * num_vehicles, True, "Capacity")

        search_params = pywrapcp.DefaultRoutingSearchParameters()
        search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

        solution = routing.SolveWithParameters(search_params)
        if solution:
            routes = []
            for vehicle_id in range(num_vehicles):
                index = routing.Start(vehicle_id)
                route = []
                while not routing.IsEnd(index):
                    node = manager.IndexToNode(index)
                    if 0 < node <= len(data):
                        route.append(data[node - 1])
                    index = solution.Value(routing.NextVar(index))
                if route:
                    routes.append(route)
            result_container.append(routes)
        else:
            result_container.append(None)
    except Exception as e:
        result_container.append(f"Error: {e}")
        print('Error Solution')
    return result_container
def run_solve_vrp_with_timeout(data, num_vehicles, capacity, timeout = 1):
    """Chạy solve_vrp trong 1 thread, dừng nếu quá timeout giây"""
    result_container = []
    thread = threading.Thread(target=solve_vrp, args=(data, num_vehicles, capacity, result_container))
    thread.start()
    thread.join(timeout)  # Chờ tối đa `timeout` giây

    if thread.is_alive():
        return None
    
    return result_container[0] if result_container else None
