# Boardgames Data
This repository contains a dataset of board games, meticulously scraped from [boardgamegeek.com](https://boardgamegeek.com). While the site offers an [XML API](https://boardgamegeek.com/wiki/page/Data_Mining#) for data collection, my goal was to gather a more extensive dataset than what the API provides.
<br/><br/>
The data collection and cleaning process was executed in four distinct stages:
| № | Description | Link to Code | Result |
|---|-------------|--------------|--------|
| 1 | Scraping a comprehensive list of all board games | [Python script](https://github.com/sk-il/garage/blob/main/01_boardgames/data/01_get_boardgames_list.py) | [boardgames_list.csv](https://github.com/sk-il/garage/tree/main/01_boardgames/data/raw) (~150K rows) |
| 2 | Refining the list to include only board games with ratings | [Jupyter notebook](https://github.com/sk-il/garage/blob/main/01_boardgames/data/02_boardgame_list_cleaning.ipynb) | [boardgames_list_clean.csv](https://github.com/sk-il/garage/tree/main/01_boardgames/data/raw) (~25K rows) |
| 3 | Scraping detailed information for each board game | [Python script](https://github.com/sk-il/garage/blob/main/01_boardgames/data/03_get_boargames_details.py) | [boardgames_list_clean.csv](https://github.com/sk-il/garage/tree/main/01_boardgames/data/raw) (~25K rows) |
| 4 | Comprehensive data cleaning, filtering, and organization | [Jupyter notebook](https://github.com/sk-il/garage/blob/main/01_boardgames/data/04_boardgames_details_cleaning.ipynb) | [01_boardgames_main.csv](https://github.com/sk-il/garage/tree/main/01_boardgames/data/final) (~6K rows) + additional tables for subdomains, categories, and mechanics (multiple entries possible per game ID) |

<br/><br/>
### Fields Description for `01_boardgames_main.csv`
| №   | Field Name             | Description                                                                                     | Example                             |
|-----|------------------------|-------------------------------------------------------------------------------------------------|-------------------------------------|
| 1   | id                     | Unique identifier for each board game                                                           | 224517                              |
| 2   | name                   | Name of the board game                                                                          | Brass: Birmingham                   |
| 3   | year                   | Year of the board game's release                                                                | 2018                                |
| 4   | users_rated            | Number of users who have rated the game                                                         | 41813                               |
| 5   | avg_rating             | Average rating given by users                                                                   | 8.60725                             |
| 6   | geek_rating            | BoardGameGeek's ranking based on user ratings and Bayesian averaging. [More details here](https://boardgamegeek.com/thread/1702432/what-geek-rating)                            | 8.42183                             |
| 7   | weight                 | Complexity rating of the game (1=easy, 5=hard)                                                  | 3.8910                              |
| 8   | owned                  | Number of users who own the game                                                                | 57802                               |
| 9   | fans                   | Number of fans or followers of the game                                                         | 4196                                |
| 10  | views                  | Total views of the game's page on BoardGameGeek                                                 | 3836310                             |
| 11  | plays                  | Total recorded plays of the game                                                                | 109572                    |
| 12  | plays_month            | Plays last month                                                                           | 1408                   |
| 13  | min_players            | Minimum number of players by rules                                                                       | 2                   |
| 14  | max_players            | Maximum number of players by rules                                                                       | 4                    |
| 15  | min_players_recomended | Recommended minimum number of players for optimal experience                                   | 2                    |
| 16  | max_players_recomended | Recommended maximum number of players for optimal experience                                   | 4                   |
| 17  | min_players_best       | Optimal minimum number of players for best gameplay experience                                  | 3                                   |
| 18  | max_players_best       | Optimal maximum number of players for best gameplay experience                                  | 4                                   |
| 19  | min_playtime           | Minimum playtime in minutes                                                                     | 60                                  |
| 20  | max_playtime           | Maximum playtime in minutes                                                                     | 120                                 |
| 21  | awards                 | Number of awards the game has received                                                          | 20                                  |
| 22  | expansions             | Number of expansions available for the game                                                     | 0                                   |
| 23  | min_age                | Minimum recommended age for players                                                             | 14                                  |
| 24  | link                   | Link to the game's page on BoardGameGeek                                                        | /boardgame/224517/brass-birmingham  |
| 25  | description            | Brief description of the game                                                                   | Build networks, grow industries...  |
| 26  | price_euro             | Price of the game in Euros                                                                      | 91.63                               |
