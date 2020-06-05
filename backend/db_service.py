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
            result[key] = table.find_one({'pid':str(player_id)})
            result[key].pop('_id',None)

        return result 

if __name__ == "__main__":
    print("DB Service!")