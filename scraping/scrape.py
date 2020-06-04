import ast
from bs4 import BeautifulSoup
from configparser import ConfigParser
import pandas as pd
from pathlib import Path
import pickle as pk
from pymongo import MongoClient
import re
import requests
import sqlite3

def fetch_player_data(url, id):
    player_url = '{}?PlayerID={}'.format(url, id)
    page = requests.get(player_url)
    if page.status_code == 200:
        return page.text
    else:
        return None

def fetch_mappings(url):
    players_page = requests.get(url)
    players_bs = BeautifulSoup(players_page.content, 'html.parser')
    mappings = players_bs.find_all(class_='LinkNormal', href = re.compile('PlayerOverviewSummary'))
    id_mapping = {}
    for tag in mappings:
        player = tag.text
        player_id = re.search(r'.*PlayerID=(.*)', tag.attrs['href']).group(1)
        id_mapping[player_id] = player
    return id_mapping

def fetch_stats(url, player_id, formats):
    player_data = fetch_player_data(url, player_id)
    player_data = player_data.replace("\n","")
    player_data = player_data.replace("\t","")
    player_data = player_data.replace("\r","")
    
    player_bs4 = BeautifulSoup(player_data)
    tables = player_bs4.find_all('table', {'class':'BorderedBox3'})
    stats = {}
    
    for ind, format_ in formats.items():
        if ind < len(tables):
            table = tables[ind]
            stats[format_] = {}
            profile = None
            for row in table.findAll('tr'):
                cells = row.findAll('td')
                if len(cells) == 1:
                    profile = cells[0].text
                    stats[format_][profile] = {}
                else:
                    row_stripped = [str.strip(cell.text) for cell in cells]
                    stats[format_][profile][row_stripped[0]] = None 
                    try:
                        stats[format_][profile][row_stripped[0]] = float(row_stripped[1])
                    except:
                        pass
    return stats

def fetch_all_stats(mapping, player_url, formats):
    stats = {}
    for player_id in id_mapping.keys():
        player_stats = None
        try:
            player_stats = fetch_stats(player_url, player_id, formats)
        except:
            print('Error for player id {} - {}'.format(player_id, id_mapping[player_id]))
        finally:
            if player_stats is not None and player_stats != {} :
                stats[player_id] = player_stats
                print("Fetched stats for player {} - {}".format(player_id, mapping[player_id]))
    return stats

def remove_blanks(stats):
    trimmed_stats = {}
    for pid, stat in stats.items():
        if stat != {}:
            trimmed_stats[pid] = stat
    
    return trimmed_stats

def split_stats_to_formats(stats, formats, aspects):
    restructured_stats = {}
    for pid, stat in stats.items():
        for format_, format_stat in stat.items():
            if format_ not in restructured_stats.keys():
                restructured_stats[format_] = {}
            for aspect, aspect_stat in format_stat.items():
                if aspect not in restructured_stats[format_].keys():
                    restructured_stats[format_][aspect] = []
                if format_ in formats.values() and aspect in aspects and aspect_stat is not None:
                    aspect_stat.update({'pid':pid})
                    restructured_stats[format_][aspect].append(aspect_stat)
    
    return restructured_stats

def stats_to_dataframes(stats, formats, aspects, columns_to_drop):
    dataframes = {}
    for format_ in formats.values():
        dataframes[format_] = {}
        for aspect in aspects:
            dataframes[format_][aspect] = pd.DataFrame(stats[format_][aspect])
            dataframes[format_][aspect].fillna(0, inplace=True)
            df = dataframes[format_][aspect]
            df.columns = df.columns.str.replace(' ', '_')
            df.columns = df.columns.str.replace(':', '')
            df = df[(df.drop('pid', axis = 1).T != 0).any()]
            dataframes[format_][aspect] = df = df.loc[:, (df != 0).any(axis=0)]
            sel_columns = [col for col in columns_to_drop[aspect] if col in dataframes[format_][aspect].columns]
            if len(sel_columns) > 0:
                dataframes[format_][aspect].drop(sel_columns, axis = 1, inplace=True)
            dataframes[format_][aspect].set_index('pid', inplace=True)

    return dataframes

def convert_to_rank(dataframes, formats, aspects):
    dataframes_pct = {}
    for format_ in formats.values():
        dataframes_pct[format_] = {}
        for aspect in aspects:
            dataframes_pct[format_][aspect] = dataframes[format_][aspect].rank(pct=True)

    return dataframes_pct

def write_tables(dataframes, dataframes_pct, formats, aspects, client):
    db = client.stats
    for format_ in formats.values():
        for aspect in aspects:

            dataframes[format_][aspect].reset_index(inplace=True)
            dataframes_pct[format_][aspect].reset_index(inplace=True)

            stats = db['stats_{}_{}'.format(format_, aspect)]
            stats_pct = db['stats_pct_{}_{}'.format(format_, aspect)]
            
            for record in dataframes[format_][aspect].to_dict(orient='records'):
                stats.insert_one(record)
                print('Stats for Player {} added'.format(record['pid']))
            
            for record in dataframes_pct[format_][aspect].to_dict(orient='records'):
                stats_pct.insert_one(record)
                print('Percentile Stats for Player {} added'.format(record['pid']))
            

if __name__ == "__main__":
    config = ConfigParser()
    config.read("../config.ini")
    
    base_url = config['URLs']['BaseURL']
    list_url = '{}/{}'.format(base_url, config['URLs']['AllPlayersRoute'])
    player_url = '{}/{}'.format(base_url, config['URLs']['PlayerRoute'])
    
    base_path = config['Files']['BasePath']
    mappings_file = '{}/{}'.format(base_path, config['Files']['Mappings'])
    stats_file = '{}/{}'.format(base_path, config['Files']['Stats'])

    db_url = config['DB']['url']
    db_port = int(config['DB']['PORT'])
    to_write_db = ast.literal_eval(config['DB']['TO_WRITE'])

    formats = {int(index):format_ for index, format_ in dict(config['MatchFormats']).items()}
    aspects = eval(config['Player']['Aspects'])
    columns_to_drop = {key.capitalize():eval(value) for key, value in dict(config['ToDrop']).items()}

    if to_write_db:
        id_mapping = None
        if Path(mappings_file).is_file():
            with open(mappings_file, 'rb') as f:
                id_mapping = pk.load(f)
        else:
            id_mapping = fetch_mappings(list_url)
            with open(mappings_file, 'wb') as f:
                pk.dump(id_mapping, f)

        stats = None
        if Path(stats_file).is_file():
            with open(stats_file, 'rb') as f:
                stats = pk.load(f)
        else:
            stats = fetch_all_stats(id_mapping, player_url, formats)
            if stats is not None or stats != {}:
                with open(stats_file, 'wb') as f:
                    pk.dump(stats, f)
            else:
                raise Exception('Error in fetching stats')
        
        stats = remove_blanks(stats)
        stats = split_stats_to_formats(stats, formats, aspects)
        dataframes = stats_to_dataframes(stats, formats, aspects, columns_to_drop)
        percentile_dataframes = convert_to_rank(dataframes, formats, aspects)

        client = MongoClient(db_url, db_port)
        write_tables(dataframes, percentile_dataframes, formats, aspects, client)