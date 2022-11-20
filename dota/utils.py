import os
import requests
import pandas as pd
from datetime import datetime, timezone, timedelta
import time
import random
import numpy as np

from dota.hero import heroes

def search_dota(route:str, n_sample=0, save=False):
    """
    Args:
        route (str): sub route for dota api, e.g. /heroes
        n_sample (int, optional): number of sample results to print out. Defaults to 0.
        save (bool, optional): save dataframe locally. Defaults to False.

    Returns:
        query results as dataframe if results is list, else return list of (key, value) tuples
    """    

    url = f'https://api.opendota.com/api/{route}'    
    r = requests.get(url)
    
    if r.status_code == 200:
        res = r.json()        
        # print(f'\nretrieved {len(res)} results:')
        # print(res)

        if 'explorer' in route:
            res = res['rows']
                
        if type(res) is list:     
            # list save as dataframe  
            df = pd.DataFrame(res)            
            if save: 
                df.to_csv(route.replace('/','_')+'.csv', index=False)
            if n_sample: 
                print(df.head(n_sample))
            return df
        elif type(res) is dict:
            #dict as list of (key, value) tuples
            res = list(res.items())
            if n_sample: 
                print(res[:n_sample])
            return res
    else:
        raise Exception(f'counter {r.status_code} error for route: {route}')


def get_player_win_rate(player_id:int, last_date='', last_days=0, rounding=3) -> float: 
    """get player win rate, for all or after a date or days

    Args:
        player_id (int): player account_id
        last_date (str, optional): win rate after this date. Defaults to ''.
        last_days (int, optional): win rate after last days from today. Defaults to 0.
        rounding (int, optional): win rate rounding point. Defaults to 3.

    Returns:
        float: rounded win rate, if player no data, return 0
    """    

    # if no time indicated, use total win rate
    if not last_date and not last_days:
        res = search_dota(f'players/{player_id}/wl')
        res = [r[1] for r in res]
        if sum(res) == 0:
            return 0
        return round(res[0] / sum(res), rounding)
        
    
    elif last_days:
        dt = datetime.today() - timedelta(days=last_days)
        y, m, d = dt.year, dt.month, dt.day
    else:
        y, m, d = map(int, last_date.split('-'))
    
    ts = datetime(y, m, d, tzinfo=timezone.utc).timestamp()
    df = search_dota(f'players/{player_id}/matches')
    if len(df) == 0:
        return 0
    
    # if last date earlier than last played time, select games played before this date
    if ts<df.start_time.iloc[0]: 
        df = df[df.start_time>=ts]
        if len(df) == 0:
            return 0
        print(f'{len(df)} games played before {y}-{m}-{d}')
    
    df['start_time'] = df['start_time'].apply(datetime.utcfromtimestamp)    
    wins = df.radiant_win.sum()

    return round(wins / len(df), rounding)


def get_default_hero(random_choose=False) -> int:  
    """return hero id if player has no play history, return either random hero or most picked hero

    Args:
        random_choose (bool, optional): if True, return random hero. Defaults to False.

    Returns:
        int: hero id
    """    

    if random_choose:
        return random.choice(list(heroes.keys()))
    else:
        pt = 'db/heroes_ranked.npy'            
        if os.path.isfile(pt):
            with open(pt, 'rb') as f:
                heroes_ranked = np.load(f)
        else:
            hero = search_dota('heroStats', 2, save=True)
            cols = [c for c in hero.columns if 'pick' in c]
            hero['sum_pick'] = hero[cols].sum() // 1000000
            hero = hero[['id', 'sum_pick']].sort_values('sum_pick', ascending=False)
            heroes_ranked = hero.id.values
            
            with open(pt, 'wb') as f:
                np.save(f, heroes_ranked)                       
            
        return heroes_ranked[0]
                                


if __name__ == '__main__':
    start = time.time()
    id = 1 #161683666

    rate = get_player_win_rate(id)
    print(rate)
    rate = get_player_win_rate(id, last_date='2022-11-1')
    print(rate)
    rate = get_player_win_rate(id, last_days=20)
    print(rate)

    

    # hero = get_default_hero(random_choose=True)
    # print(hero)

    # sql('select * from player_matches where account_id = 161683666')
    print(round(time.time() - start), ' seconds consumed.')