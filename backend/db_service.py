from configparser import ConfigParser
import pickle as pk
from pymongo import MongoClient

def clean(text):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    text = text.lower()
    for mark in punctuations:
        text = text.replace(mark, "")
    return text

class DbClient:
    def __init__(self):
        config = ConfigParser()
        config.read("../config.ini")
        self.db_url = config['DB']['url']
        self.db_port = int(config['DB']['PORT'])
        self.mapping = {
            'raw':{},
            'clean':{}
        }
        with open('../scraping/stats/mapping.pk', 'rb') as f:
            self.mapping['raw'] = pk.load(f)
        for pid, name in self.mapping['raw'].items():
            self.mapping['clean'][pid] = clean(name)

    def fetch_mappings(self, pattern, num_searches = 10):
        pattern = clean(pattern)
        result = []
        for pid, clean_name in self.mapping['clean'].items():
            if len(result) >= num_searches:
                break
            else:
                if pattern in clean_name:
                    result.append({
                        'id':pid,
                        'name':self.mapping['raw'][pid]
                    })
        return result

    def fetch_stats(self, player_id, format_, aspect):
        table_names = {
            'stats':'stats_{}_{}'.format(format_, aspect),
            'percentiles':'stats_pct_{}_{}'.format(format_, aspect)
        }
        client = MongoClient(self.db_url, self.db_port)
        db = client.stats
        result = {}
        result['name'] = self.mapping['raw'][player_id]
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