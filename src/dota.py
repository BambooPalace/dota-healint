import requests
import pandas as pd
from datetime import datetime

def search_api(route, n_sample=5):
    #route, i.e. matches/271145478

    url = f'https://api.opendota.com/api/{route}'
    r = requests.get(url)
    if r.status_code == 200:
        res = r.json()        
        print(f'retrieved {len(res)} results, sample as below:')

        if 'explorer' in route:
            res = res['rows']
        
        if type(res) is dict:
            print(list(res.items())[:n_sample])
            return res
        else:            
            df = pd.DataFrame(res)
            # df.to_csv(route.replace('/','_')+'.csv', index=False)
            if n_sample: print(df.head(n_sample))
            return df
    else:
        raise Exception(f'counter {r.status_code} error for route: {route}')


def get_player_win_rate(player_id, before_date=''):
    df = search_api(f'players/{player_id}/matches', 0)
    df['start_time'] = df['start_time'].apply(datetime.utcfromtimestamp)    
    wins = df.radiant_win.sum()
    print(wins, len(df)-wins)
    # search_api(f'players/{player_id}/wl', 5)

    return df[['radiant_win', 'start_time']]


def get_player_hero(player_id):
    pass


if __name__ == '__main__':
    get_player_win_rate(161683666)

    # sql('select * from player_matches where account_id = 161683666')