from configparser import ConfigParser
from pymongo import MongoClient

class DbClient:
    def __init__(self):
        config = ConfigParser()
        config.read("../config.ini")
        self.db_url = config['DB']['url']
        self.db_port = int(config['DB']['PORT'])

    def fetch_stats(self, player_id, format_, aspect):
        table_names = {
            'stats':'stats_{}_{}'.format(format_, aspect),
            'percentiles':'stats_pct_{}_{}'.format(format_, aspect)
        }
        client = MongoClient(self.db_url, self.db_port)
        db = client.stats
        result = {}
        for key, table_name in table_names.items():
            table = db[table_name]
            
            db_response = table.find_one({'pid':str(player_id)})
            if db_response == None:
                return None
            result[key] = db_response
            result[key].pop('_id',None)
            result[key].pop('pid',None)
            captions = list(result[key].keys())
            result['captions'] = {x:x.replace("_"," ") for x in captions}

        return result 

if __name__ == "__main__":
    print("DB Service!")