
from dota.utils import search_dota, get_default_hero, get_player_win_rate
from dota.hero import heroes


def get_player_hero(player_id:int, random=False) -> dict:
    """recommend most played hero for given player, if no play history return most picked hero on Dota

    Args:
        player_id (int)
        random (bool, optional): if True then random assign hero, else check history

    Returns:
        int: hero id
    """    
    if random:
        hero_id = get_default_hero(random_choose=True)

    else:
        df = search_dota(f'players/{player_id}/heroes', 0)
        # if no play history return most picked hero on Dota
        if df.games.iloc[0] == 0:
            hero_id = get_default_hero(random_choose=False)
        else:
            hero_id = df.hero_id.iloc[0]
    return {hero_id: heroes[hero_id]}

    

def get_leaderboard(player_ids: list[int], last_date='', last_days=0) -> list[dict]:
    
    """return ranked player ids in order of descending win rate, if player no history put at bottom

    Args:
        player_ids (list): list of player ids
        last_date (str, optional): based on win rate before this date. Defaults to ''.
        last_days (int, optional): based on win rate before last days from today. Defaults to 0.

    Returns:
        list: ranked list of player, their win rate and rank
    """    
    # get win rates/ scores
    scores = []    
    for id in player_ids:
        score = get_player_win_rate(id, last_date, last_days)
        scores.append(score)        
    
    # sort scores and get rank, e.g. [3, 1, 1, 4, 5]
    sort_scores = sorted(scores, reverse=True)
    rank = [sort_scores.index(v)+1 for v in scores]

    # make leader board
    board = []
    for i in range(len(rank)):
        board.append( 
            {'player_id': player_ids[i],
            'win_rate': scores[i],
            'rank': rank[i],
            }
            )

    return sorted(board, key=lambda item: item['rank'])

    

if __name__ == '__main__':
    ids = [1, 2, 10000, 161683666, 268590680, 134784663]
    
    # res = get_leaderboard(ids)
    # print(res)

    for id in ids:
        res = get_player_hero(id, True)
        print(res)