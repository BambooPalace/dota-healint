from src.dota import search_api
import time

def test_api(route, n_sample=5):
    res = search_api(route, n_sample)    
    time.sleep(1)
    return res

if __name__ == '__main__':
    routes = [
        # 'matches/271145478',
        # 'playersByRank',
        'players/268590680',
        # 'metadata',
        # 'rankings?hero_id=1',
        # 'benchmarks?hero_id=1',
        'heroes',
        # 'heroes?hero_id=1/players',
        # 'heroStats',
        'leagues',
        # 'constants',
        # 'schema'
    ]
    df = test_api('schema')

    print(df[df.column_name.str.contains('time')])

    player_routes = [
        'wl',
        'matches',
        'heroes',
        # 'peers',
        # 'pros',
        # 'totals',
        # 'counts',
        # 'histograms',
        # 'wardmap',
        # 'wordcloud',
        # 'ratings', #not based on win rate
        'rankings'
    ]
    for r in player_routes[:0]:        
        id = 268590680
        route = f'/players/{id}/{r}'
        print(f'\n\n{route}')
        test_api(route)