## Using the API

### Register a new name 
On the command line where the app is deployed run `flask initgame`, you will be prompted for a game slug and a game secret will be generated. Save those values for using them in your requests.

### Log a new score for a player

To make it easy for logging game scores, there is only one endpoint for adding a score to a game's board. If the board or player do not exist, they will be created on the fly and the score will be logged for that player on that board of the designated game.

`[POST] http://api.yourhost.com/score/add`

In the request's body supply the following values need to be sent:

- **fb_id** The facebook ID of the player 
- **game_slug** The slug of the game you're logging scores for
- **fb_access_token** The facebook access token of your player
- **score_value** The value of the score you're logging
- **board_slug** The slug or name of the board you're logging on
- **game_secret** the game secret of the game you're logging scores for

On success a reply should look like this:

```
{
  "data": {
    "board": "board",
    "created_at": "Sat, 08 Apr 2017 09:35:21 GMT",
    "game": "wewe",
    "player": {
      "fb_id": "99999999",
      "name": "Ayman Farhat"
    },
    "score": 45555
  },
  "status": "success"
}
```

### List a player's score history

`[GET] http://api.yourhost.com/playerboard/{YOUR_GAME_NAME}/ {YOUR_BOARD_NAME}/{YOUR_PLAYER_FB_ID}`


This will list the player's last 10 scores in a certain game on a certain board. Sample reply would look something like:

(Sorting and setting a limit in the API coming soon)

```
{
  "data": [
    {
      "created_at": "Sat, 08 Apr 2017 09:35:21 GMT",
      "score": 4555
    },
    {
      "created_at": "Sat, 08 Apr 2017 12:03:31 GMT",
      "score": 42555
    },
    {
      "created_at": "Sat, 08 Apr 2017 12:03:32 GMT",
      "score": 44555
    }
  ],
  "status": "success"
}
```

### List the top N players on a board

This will show all unique top 10 players on a chosen board, sorted in descending order. (requesting top n and overriding the sort order coming soon)

`[GET] http://api.yourhost.com/leaderboard/{YOUR_GAME_NAME}/{YOUR_BOARD_NAME}`

Sample reply:

```
{
  "data": [
    {
      "created_at": "Sat, 08 Apr 2017 09:35:21 GMT",
      "player_fbid": "9999999",
      "player_name": "Ayman Farhat",
      "score": 45555
    }
  ],
  "status": "success"
}
```



## Run the server (quick notes)

`export FLASK_DEBUG=1`
then
`flask run`

Before running the flask app needs to be referenced in an environment variable: `export FLASK_APP=scoreo/__init__.py`

Update the database:

After updating the models file for the database scheme run: `flask db migrate` to generate a new migration.
After generating the new migration, run `flask db upgrade` to apply the migration.

If a migrations folder does not exist this means the database is not yet initialised. run `flask db init` then migrate it upgrade.

To run on gunicorn: Run via `gunicorn --bind 0.0.0.0:5000 wsgi:app`

Also make sure to create an upstart script for gunicorn on ubuntu, reference: 
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04
