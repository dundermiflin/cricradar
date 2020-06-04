from configparser import ConfigParser
from flask import Flask, make_response, jsonify

app = Flask(__name__)

@app.route('/')
def greeting():
    return 'Hi! Welcome to cricradar'

@app.route('/<int:id>')
def stats(id):
    data = {
        'id':id,
        'stats':{
            'matches':1,
            'runs':12,
            'tenturies':1
        }
    }
    return jsonify(data)

@app.errorhandler(404)
def data_not_found(error):
    return make_response(jsonify({'message':'data not avaialable'}), 404)

if __name__ == "__main__":
    config = ConfigParser()
    config.read("../config.ini")
    
    port = int(config['Server']['Port'])
    app.run(port = port, debug = True)