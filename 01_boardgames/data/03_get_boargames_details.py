import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os


def get_urls(boardgames_list_path, boardgames_details_path):
    new_ids = pd.read_csv(boardgames_list_path, usecols=['id', 'link'])

    if os.path.isfile(boardgames_details_path):
        old_ids = pd.read_csv(boardgames_details_path, usecols=['id'])
    else:
        old_ids = []

    return list(new_ids.loc[~new_ids['id'].isin(old_ids['id']), 'link'])


def extract_json_from_html(url):
    # Fetch the HTML content from the URL
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to load page: {response.status_code}")

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all script tags
    script_tags = soup.find_all('script')

    # Iterate through each script tag to find the one containing 'GEEK.geekitemPreload'
    for script in script_tags:
        if script.string and 'GEEK.geekitemPreload' in script.string:
            # Extract the JSON string from the script tag
            json_str = script.string.split('GEEK.geekitemPreload = ', 1)[1]

            # Remove any trailing JavaScript code or semicolons
            json_str = json_str.split(';\n', 1)[0]

            # Convert the JSON string to a Python dictionary
            json_data = json.loads(json_str)['item']

            userplayers = json_data['polls']['userplayers']

            main_data = {
                'id': json_data['objectid'],
                'name': json_data['name'],
                'link': json_data['href'],
                'year': json_data['yearpublished'],
                'users_rated': json_data['stats']['usersrated'],
                'avg_rating': json_data['stats']['average'],
                'geek_rating': json_data['stats']['baverage'],
                'weight': json_data['stats']['avgweight'],
                'owned': json_data['stats']['numowned'],
                'fans': json_data['stats']['numfans'],
                'views': json_data['stats']['views'],
                'plays': json_data['stats']['numplays'],
                'plays_month': json_data['stats']['numplays_month'],
                'min_players': json_data['minplayers'],
                'max_players': json_data['maxplayers'],
                'min_players_recomended': userplayers['recommended'][0]['min'] if 'min' in str(
                    userplayers['recommended']) else None,
                'max_players_recomended': userplayers['recommended'][0]['max'] if 'max' in str(
                    userplayers['recommended']) else None,
                'min_players_best': userplayers['best'][0]['min'] if 'min' in str(userplayers['best']) else None,
                'max_players_best': userplayers['best'][0]['max'] if 'max' in str(userplayers['best']) else None,
                'min_playtime': json_data['minplaytime'],
                'max_playtime': json_data['maxplaytime'],
                'min_age': json_data['minage'],
                'subdomain': [x['name'] for x in json_data['links']['boardgamesubdomain']],
                'categories': [x['name'] for x in json_data['links']['boardgamecategory']],
                'mechanics': [x['name'] for x in json_data['links']['boardgamemechanic']],
                'awards': json_data['linkcounts']['boardgamehonor'],
                'expansions': json_data['linkcounts']['boardgameexpansion'],
                'ranks': {x['shortprettyname']: x['rank'] for x in json_data['rankinfo']}
            }

            return main_data


def main(boardgames_list_path, boardgames_details_path):
    # Get remaining urls
    urls = get_urls(boardgames_list_path, boardgames_details_path)
    print(len(urls))

    boardgames_details_list = []

    for url in urls:
        boardgames_details_list.append(extract_json_from_html(url))

        # Save results every 100
        if len(boardgames_details_list) == 100 or url == urls[-1]:
            df = pd.DataFrame(boardgames_details_list)

            # Add header if file doesn't exist
            header = not os.path.isfile(boardgames_details_path)
            df.to_csv(boardgames_details_path, mode='a', header=header, index=False)

            boardgames_details_list = []


boardgames_list_path = r'raw\boardgames_list_clean.csv'
boardgames_details_path = r'raw\boardgames_details.csv'

main(boardgames_list_path, boardgames_details_path)
