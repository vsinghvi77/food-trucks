# all of these data processing and data can be shifted on a real database

from socket import timeout
import geopandas
import json
from shapely.geometry import  Point
from flask_caching import Cache
from __main__ import cache

food_truck_data = None
food_truck_data_mat = None
food_truck_data_columns = None
sorted_column_name = None

def prepare_data():
    global food_truck_data
    global food_truck_data_columns
    global sorted_column_name
    # prepare data
    data_filename = "./sanfransiscofoodtruckdata.json"
    with open(data_filename) as data_file:
        json_data = json.load(data_file)
        food_truck_data = geopandas.GeoDataFrame.from_dict(json_data["data"])

        food_truck_data = geopandas.GeoDataFrame(food_truck_data.loc[(food_truck_data[22]!="0") | (food_truck_data[23]!="0")])

        food_truck_data_columns = geopandas.GeoDataFrame.from_dict(json_data["meta"]["view"]["columns"])
        # prepare columns
        column_name=[]
        for i,r in food_truck_data_columns.iterrows():
            if (r["position"] >=1):
                column_name.append({"pos":r["position"],"name":r["name"]})
        
        sorted_column_name = sorted(column_name, key = lambda e: e["pos"])
        sorted_column_name = [i["name"] for i in sorted_column_name]
        
        # add geomtery
        food_truck_data = geopandas.GeoDataFrame(food_truck_data,geometry=geopandas.points_from_xy(food_truck_data[23],food_truck_data[22]),crs="EPSG:4326")
        
        food_truck_data.reset_index(inplace=True)
        
        # food_truck_data.columns = sorted_column_name
        
        # food_truck_data = food_truck_data.to_crs("EPSG:3310") 
        # food_truck_data.to_crs("EPSG:3310",inplace=True)

    # prepare distance matrix
    
    # food_truck_data_mat = food_truck_data.geometry.apply(lambda g:food_truck_data.distance(g))

    # tmp_closest_food_truck_data = []
    # for idx in food_truck_data_mat:
    #     # get 10 closest trucks
    #     closest_trucks = food_truck_data_mat[idx].sort_values().index[1:11]
    #     tmp_closest_food_truck_data.append(closest_trucks)

    # # add closest truck data to main data frame

    # food_truck_data["closest_trucks_indexes"] = tmp_closest_food_truck_data


prepare_data()

def data_refetch_data():
    pass



@cache.memoize(None)
def data_get_closest_truck(lat,long,num):
    center_point = Point(long,lat)
    # get closest truck and from that truck get other closest truck
    distances = food_truck_data.distance(center_point)
    distances_sorted = distances.sort_values()
    return food_truck_data.iloc[distances_sorted.index[0:num]]