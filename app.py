import os
from flask import Flask, jsonify, request
import re

from dota.dota import get_player_hero, get_leaderboard

app = Flask(__name__)
@app.route('/')
def main():
    return "available api: 1)'/players/id/hero', 2)'/players/id1,id2,id3/leaderboard', optional parameters e.g. ?day/week/month/year=1 or ?date=2022-01-01;' "

@app.route('/players/<int:id>/hero')
def player_hero(id):
    random = request.args.get('random')
    if random: random = True
    return jsonify(get_player_hero(id, random))


def parse_peiord():  
    try:               
        d = request.args.get('day')
        days = int(d) if d else 0
        yr = request.args.get('year')
        if yr: 
            days += 365*int(yr)

        m = request.args.get('month')
        if m:            
            days += 30*int(m)

        w = request.args.get('week')
        if w:
            days += 7*int(w)
                
        return days
    except:
        raise Exception('invalid parameter: please indicate period by parameters i.e. day, week, month, year')


def parse_date():
    date = request.args.get('date')
    if date:
        res = re.match('\d{4}-\d{2}-\d{2}', date)
        if res is not None:
            return date
        else:
            raise Exception('invalide date format, i.e. 2022-11-01')



@app.route('/players/<string:ids>/leaderboard')
def leaderboard(ids):
    days = parse_peiord()
    date = parse_date()

    ids = ids.split(',')
    if not ids:
        return 'please input players ids seperate by comma, e.g. players/1,2,3,4/leaderboard'
    print(ids)
    return jsonify(get_leaderboard(ids, date, days))


if __name__ == "__main__":
    app.run(host ='0.0.0.0')