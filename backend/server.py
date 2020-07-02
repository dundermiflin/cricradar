from configparser import ConfigParser
from db_service import DbClient
from flask import Flask, make_response, jsonify, request, abort

def build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def corsify_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

app = Flask(__name__)

@app.route('/test', methods = ['GET'])
def test_service():
    if request.method == 'GET':
        print("TEST received")
        response = jsonify({'msg':'Hi, Welcome to CricRadar!'})
        return corsify_response(response)

@app.route('/search', methods = ['POST', 'OPTIONS'])
def mapping_service():
    if request.method == 'OPTIONS':
        print("CORS request")
        return build_cors_prelight_response()
    if request.method == 'POST':
        params = request.get_json()
        pattern = params.get('pattern')
        num_searches = params.get('num')
        print(pattern, num_searches)
        client = DbClient()
        query_response = client.fetch_mappings(pattern, int(num_searches))
        if query_response is None:
            abort(404, description="Resource not found")
        json_response = jsonify(query_response)
        return corsify_response(json_response)


@app.route('/stats', methods = ['POST', 'OPTIONS'])
def stats_service():
    if request.method == 'OPTIONS':
        print("CORS request")
        return build_cors_prelight_response()
    if request.method == 'POST':
        params = request.get_json()
        print(params)
        player_id = params.get('id')
        format_ = params.get('format')
        aspect = params.get('aspect')
        print(player_id, format_, aspect)
        client = DbClient()
        query_response = client.fetch_stats(player_id, format_, aspect)
        if query_response is None:
            abort(404, description="Resource not found")
        json_response = jsonify(query_response)
        return corsify_response(json_response)

@app.errorhandler(404)
def data_not_found(error):
    return make_response(jsonify({'message':'data not avaialable'}), 404)

if __name__ == "__main__":
    config = ConfigParser()
    config.read("../config.ini")
    
    port = int(config['Server']['Port'])
    app.run(port = port, debug = True)