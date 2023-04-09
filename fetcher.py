import requests
import json
from bs4 import BeautifulSoup
import re
import codecs
from datetime import date, timedelta


def get_player_form(last_gw, start_date_fmt=""):
    """ Retrieve the fpl player data from the hard-coded url
    """
    url = "https://understat.com/main/getPlayersStats/"
    if start_date_fmt == '':
        start_date = date.today() - timedelta(weeks=last_gw + 1)
        start_date_fmt = start_date.strftime("%Y-%m-%d")
    payload = "season=2022&league=EPL&n_last_matches=" +  str(last_gw) + "&date_start=" + start_date_fmt + "+17:00:00"
    headers = {}
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code != 200:
        raise Exception("Response was code " + str(response.status_code))
    responseStr = response.text
    data = json.loads(responseStr)
    return data['response']['players']

# print(get_player_form(2))

def get_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Response was code " + str(response.status_code))
    html = response.text
    parsed_html = BeautifulSoup(html, 'html.parser')
    scripts = parsed_html.findAll('script')
    filtered_scripts = []
    for script in scripts:
        if len(script.contents) > 0:
            filtered_scripts += [script]
    return scripts

def get_team_data():
    scripts = get_data("https://understat.com/league/EPL/2022")
    teamData = {}
    for script in scripts:
        for c in script.contents:
            split_data = c.split('=')
            data = split_data[0].strip()
            if data == 'var teamsData':
                content = re.findall(r'JSON\.parse\(\'(.*)\'\)',split_data[1])
                decoded_content = codecs.escape_decode(content[0], "hex")[0].decode('utf-8')
                teamData = json.loads(decoded_content)

    teams = {value['title']: value['history'] for _, value in teamData.items()}
    return teams

# print(get_team_data())