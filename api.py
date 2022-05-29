#
#   all api definitions here
#   caching the search for a few hours
#   calculating upto 4 decimal places only
#
from __main__ import app, cache
from protocol import ProtocolPayload,ProtocolSearchPayload

from local_data import food_truck_data, data_get_closest_truck
from flask import request
from flask import Response


@app.route("/")
@cache.cached(timeout=50)
def api_root():
    return ""


@app.route("/trucks", methods=["GET"])
@cache.cached(timeout=3600, query_string=True)
def api_truck():
    try:
        pn = request.args.get('pn')
        pp = request.args.get('pp')
        pn = int(pn)
        pp = int(pp)
    except Exception as e:
        print(e)
        return "", 503

    # validate per pag value
    if pp > 15:
        pp = 10  # set to default

    # prepare page number and items per page
    skip_value = (pn-1)*10
    if skip_value < 0:
        skip_value = 0
    elif skip_value > food_truck_data.size:
        skip_value = food_truck_data.size


    data = food_truck_data[food_truck_data.columns[~food_truck_data.columns.isin(
        ['closest_trucks_indexes'])]].iloc[skip_value:skip_value+pp].to_json()

    search_resp = ProtocolSearchPayload(len(food_truck_data),data)
    resp = ProtocolPayload("success",search_resp.to_json())

    return Response(resp.to_json(), mimetype='application/json')


@app.route("/close", methods=["GET"])
@cache.cached(timeout=3600, query_string=True)
def api_close():
    try:
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        num = request.args.get('num')
        lat = float(lat)
        lng = float(lng)
        num = int(num)
    except Exception as e:
        print(e)
        return "", 503

    if num > 10:
        return "", 400
    data = data_get_closest_truck(lat, lng, num)
    data = data[data.columns[~data.columns.isin(
        ['closest_trucks_indexes'])]].to_json()
    
    resp = ProtocolPayload("success",data)
    return Response(resp.to_json(), mimetype='application/json')


@app.errorhandler(404)
@cache.cached(timeout=50)
def page_not_found(e):
    return "", 404
