# RatingGraph
![Animated graph](https://github.com/kehtabp/RatingGraph/blob/master/example.gif?raw=true)

### To install requirements and run

1) Install python 3.2+ and pip
2) Run
```
pip install -r requirements.txt
python src/load.py -u lichess_username -e
```
### Help
```
python src/load.py -h
usage: src/load.py [-h] (--file | -u USERNAME) [-e] [--upload_video]
               [-n NUMBER_OF_GAMES] [-m GAME_MODE] [-b] [--noupdate]

Generate graph for Lichess

optional arguments:
  -h, --help            show this help message and exit
  --file                Pass to load usernames and game modes from data\queue.csv
  -u USERNAME, --username USERNAME
                        Pass to make a graph for a single username/gamemode
  -e, --export_video    Export video to ./export/ChessGraph_USERNAME_GAMEMODE_SIZE.mp4. 
                        !If this is not passed graph will be displayed in the UI Window!
  --upload_video        Upload to Streamable ./secrets.py needs to contain stramable_username 
                        and stramable_password
  -n NUMBER_OF_GAMES, --num NUMBER_OF_GAMES
                        Number of games to show on graph. (0 for all games)
  -m GAME_MODE, --mode GAME_MODE
                        Game mode (bullet/blitz/classical)
  -b, --big             Generate big chart, Defaults to smaller resolution
  --noupdate            Pass to create graph from existing data only
```
