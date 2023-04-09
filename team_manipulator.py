import pandas as pd
import numpy as np

def get_teams_stats_table(teams, buffer, last_check, h_a):
    xg_data = {}
    g_data = {}
    xga_data = {}
    ga_data = {}
    pts_data = {}
    for t_name, t_hist in teams.items():
        xg_hist = []
        g_hist = []
        xga_hist = []
        ga_hist = []
        pts_hist = []
        for h in t_hist:
            if h_a != '':
                if h['h_a'] == h_a:
                    xg_hist.append(h['xG'])
                    g_hist.append(h['scored'])
                    xga_hist.append(h['xGA'])
                    ga_hist.append(h['missed'])
                    pts_hist.append(h['pts'])
            else:
                xg_hist.append(h['xG'])
                g_hist.append(h['scored'])
                xga_hist.append(h['xGA'])
                ga_hist.append(h['missed'])
                pts_hist.append(h['pts'])
        while len(xg_hist) < buffer:
            xg_hist.insert(0, None)
            g_hist.insert(0, None)
            xga_hist.insert(0, None)
            ga_hist.insert(0, None)
            pts_hist.insert(0, None)
        xg_data[t_name] = xg_hist
        g_data[t_name] = g_hist
        xga_data[t_name] = xga_hist
        ga_data[t_name] = ga_hist
        pts_data[t_name] = pts_hist

    columns = [f'Gw-{i}' for i in range(1,last_check+1,1)]
    df_xg = pd.DataFrame(xg_data, index=[f'Gw-{i}' for i in range(buffer,0,-1)]).T
    df_xga = pd.DataFrame(xga_data, index=[f'Gw-{i}' for i in range(buffer,0,-1)]).T
    df_g = pd.DataFrame(g_data, index=[f'Gw-{i}' for i in range(buffer,0,-1)]).T
    df_ga = pd.DataFrame(ga_data, index=[f'Gw-{i}' for i in range(buffer,0,-1)]).T
    df_pts = pd.DataFrame(pts_data, index=[f'Gw-{i}' for i in range(buffer,0,-1)]).T

    df_xg = df_xg[columns]
    df_xga = df_xga[columns]
    df_g = df_g[columns]
    df_ga = df_ga[columns]
    df_xg['xg_mean'] = df_xg.mean(axis=1)     
    df_xga['xga_mean'] = df_xga.mean(axis=1)
    df_g['g_mean'] = df_g.mean(axis=1)
    df_ga['ga_mean'] = df_ga.mean(axis=1)

    df_xg = df_xg.sort_values('xg_mean', ascending=False)
    df_xg['scored_mean'] = df_g['g_mean']
    df_xg['xg_rank'] = np.arange(1,len(df_xg)+1)
    df_xg = df_xg.sort_values('scored_mean', ascending=False)
    df_xg['scored_rank'] = np.arange(1,len(df_xg)+1)
    df_xg = df_xg.reset_index()
    df_xg['short_name'] = df_xg['index'].apply(lambda x: short_name[x])
    df_xg = df_xg.reset_index()
    df_xg = df_xg.set_index('short_name')
 
    df_xga = df_xga.sort_values('xga_mean', ascending=True)
    df_xga['allowed_mean'] = df_ga['ga_mean']
    df_xga['xga_rank'] = np.arange(1,len(df_xga)+1)
    df_xga = df_xga.sort_values('allowed_mean', ascending=True)
    df_xga['allowed_rank'] = np.arange(1,len(df_xga)+1)
    df_xga = df_xga.reset_index()
    df_xga['short_name'] = df_xga['index'].apply(lambda x: short_name[x])
    df_xga = df_xga.reset_index()
    df_xga = df_xga.set_index('short_name')

    return df_xg, df_xga

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

def get_team_form(df_xg, df_xga):
    teams = []
    for index, row in df_xg.iterrows():
        team = {}
        team['name'] = index
        team['scored_mean'] = row.scored_mean
        team['xg_mean'] = row.xg_mean
        team['scored_rank'] = row.scored_rank
        team['xg_rank'] = row.xg_rank
        team['allowed_mean'] = df_xga.loc[index].allowed_mean
        team['xga_mean'] = df_xga.loc[index].xga_mean
        team['allowed_rank'] = df_xga.loc[index].allowed_rank
        team['xga_rank'] = df_xga.loc[index].xga_rank
        teams.append(team)
        
    return teams

# a, b = get_teams_stats_table(teams=get_team_data(), buffer=21, last_check=4, h_a="")
# print(a,b)
# print(get_team_form(a,b))