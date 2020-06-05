from configparser import ConfigParser
from db_service import DbClient
from flask import Flask, make_response, jsonify, request

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def service():
    if request.method == 'GET':
        return 'Hi! Welcome to cricradar'
    if request.method == 'POST':
        request.data
        player_id = request.form.get('id')
        format_ = request.form.get('format')
        aspect = request.form.get('aspect')
        client = DbClient()
        query_response = client.fetch_stats(player_id, format_, aspect)
        return jsonify(query_response)

# @app.route('/', methods = ['POST'])
# def stats(id, table):
#     data = {
#         'id':id,
#         'format':table,
#         'stats':{
#             'matches':1,
#             'runs':12,
#             'tenturies':1
#         }
#     }
#     return jsonify(data)

@app.errorhandler(404)
def data_not_found(error):
    return make_response(jsonify({'message':'data not avaialable'}), 404)

if __name__ == "__main__":
    config = ConfigParser()
    config.read("../config.ini")
    
    port = int(config['Server']['Port'])
    app.run(port = port, debug = True)