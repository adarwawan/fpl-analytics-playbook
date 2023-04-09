import pandas as pd
import numpy as np

name_mapping = {
    'Man City': 'Manchester City',
    'Man Utd': 'Manchester United',
    'Newcastle': 'Newcastle United',
    'Spurs': 'Tottenham',
    'Wolves': 'Wolverhampton Wanderers',
    "Nott'm Forest": "Nottingham Forest"
}

short_name = {
    'Arsenal': 'ARS',
    'Aston Villa': 'AVL',
    'Brentford': 'BRE',
    'Bournemouth': 'BOU',
    'Brighton': 'BHA',
    'Chelsea': 'CHE',
    'Crystal Palace': 'CRY',
    'Fulham': 'FUL',
    'Everton': 'EVE',
    'Leeds': 'LEE',
    'Leicester': 'LEI',
    'Liverpool': 'LIV',
    'Manchester City': 'MCI',
    'Manchester United': 'MUN',
    'Newcastle United': 'NEW',
    'Nottingham Forest': 'NOT',
    'Southampton': 'SOU',
    'Tottenham': 'TOT',
    'West Ham': 'WHU',
    'Wolverhampton Wanderers': 'WOL'
}

def get_fixtures():
    # data from https://github.com/vaastav/Fantasy-Premier-League
    teams = pd.read_csv('../Fantasy-Premier-League/data/2022-23/teams.csv')
    fixtures = pd.read_csv('../Fantasy-Premier-League/data/2022-23/fixtures.csv')
    teams = teams.set_index('id')
    teams = teams.replace(name_mapping)

    fixtures = fixtures.join(teams[['name']], 'team_h').rename(columns={'name':'team_home'})
    fixtures = fixtures.join(teams[['name']], 'team_a').rename(columns={'name':'team_away'})

    fixtures = fixtures[~fixtures.event.isnull()]

    fixture_not_finished = fixtures[fixtures.finished == False]

    return fixture_not_finished

def get_next_fixtures(fixtures, start_gw, end_gw):
    upcoming_match = []
    for index in short_name:
        t_fixture = fixtures[(fixtures.team_home == index) | 
                                        (fixtures.team_away == index)]
        t_fixture['h/a'] = np.where(t_fixture['team_home'] == index, 'home', 'away')
        t_fixture['opponent'] = np.where(t_fixture['h/a'] == 'home', t_fixture['team_away'], t_fixture['team_home'])
        f_rows = t_fixture[(t_fixture.event >= start_gw) & (t_fixture.event <= end_gw)].to_dict('records')
        data = {}
        opponents = []
        for i, row in enumerate(f_rows):
            opponent_comp = {'h/a': row['h/a'], 'opponent': row['opponent']}
            opponents.append(opponent_comp)
        data['opponents'] = opponents
        data['team'] = index
        data['number_games'] = len(opponents)
        upcoming_match.append(data)

    return upcoming_match

def get_next_team(upcoming_match, index):
    team_next_fixtures = upcoming_match[index]['opponents']
    team_name = upcoming_match[index]['team']
    teams = [short_name[team_name]]
    for data in team_next_fixtures:
        teams.append(short_name[data['opponent']])
    return teams

def draw_scatter(teams_df, title):

    plot_form_team = teams_df[['scored_mean', 'allowed_mean']].plot.scatter(x='scored_mean', y='allowed_mean',marker=".")

    lims = [
        np.min([plot_form_team.get_xlim(), plot_form_team.get_ylim()]),  # min of both axes
        np.max([plot_form_team.get_xlim(), plot_form_team.get_ylim()]),  # max of both axes
    ]

    plot_form_team.plot([1,1], lims, 'g--', alpha=0.75, zorder=0)
    plot_form_team.plot(lims, [1.05,1.05], 'g--', alpha=0.25, zorder=0)
    plot_form_team.set_title(title)
    for i, txt in teams_df['name'].items():
        if txt == title:
            plot_form_team.annotate(txt, (teams_df['scored_mean'][i], teams_df['allowed_mean'][i]), weight="bold", bbox=dict(boxstyle="square,pad=0.3"))
        elif teams_df['scored_mean'][i] >= 1.5:
            plot_form_team.annotate(txt, (teams_df['scored_mean'][i], teams_df['allowed_mean'][i]), color="red")
        elif teams_df['allowed_mean'][i] >= 1.5:
            plot_form_team.annotate(txt, (teams_df['scored_mean'][i], teams_df['allowed_mean'][i]), color="green")
        else:
            plot_form_team.annotate(txt, (teams_df['scored_mean'][i], teams_df['allowed_mean'][i]))