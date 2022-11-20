#this is the repo for dota API assigned by Healint

## How to run docker containers (Mac)
0. open Docker.app
1. two ways of getting docker image<br>
a) build docker image locally
- clone git repo
`git clone https://github.com/BambooPalace/dota-healint.git
`
- build docker image
`docker build -t dota-healint .
`
<br>b)  Or pull from docker hub
`docker pull clairegong/dota-healint:latest
`
2. run container
- run docker container
`docker run -p 8000:5000 dota-healint
`
3. call Api
- run in explorer or make get requests to `http://localhost:8000/`. for how to make query please look at next section



## About API
### The API perform two queries, layered on data from OpenDota API:
1. Given a list of player_ids return a leaderboard of the players based on their win rate. The API can take two additional parameters
<br>
optional parameters:
-  day/week/month/year: int, e.g. 1, 2
* date: str, e.g. ‘2022-01-01’
<br>
example urls:

```
http://localhost:8000/players/1,161683666,%20268590680/leaderboard?date=2022-01-01
http://localhost:8000/players/1,161683666,%20268590680/leaderboard?month=1
```


2. Given one player_id, return a suggestion of a hero that the player should play based on the player's historical data. 
<br>
(If no history available return most picked heros in Dota. If pass random=1, then assign heros randomly )
example url:

```
http://localhost:8000/players/1/hero
http://localhost:8000/players/161683666/hero
http://localhost:8000/players/161683666/hero?random=1
```

## Comments
1. Which tech stacks / frameworks did you consider for the development of this application?

As I am familar with using Flask with python, Flask is my first choice considering speed. FastAPI could be a good alternative due to its functionalities for documentations and supporting concurrency.

2. What are some limitations of your application and how do you plan to work around them in the future?

Currently each call to my API is done by calling  Opendota API in the backend, which is slower. Ideally, we should have the database hosting related users tables e.g. users_win_rate_by_date, users_top_hero, which can be regularly updated by mass queries to Opendota. 

I did plan to use sql database to save some queries results in db to speed up future queries for the same players, discard this idead due to time limit.

3. How would you ensure data required for the application stays up to date?

My current backend is always calling API thus is always updated, if use with mysql, need to have data pipelines to regularly writes related new data to our own tables.

4. Why is your recommendation engine a good solution?
- It returns real time data by calling the API. 
- It has flexible parameters that support requests, e.g. recommend hero randomly which is very fast, or return most liked heros in Dota games.

5. What are some features you would like to add to the application?

Due to time limit, below features were neglected but would be good to have:
- Adding mysql to host related tables to reduce response time
- include CI configurations to instantly update app at commits time
