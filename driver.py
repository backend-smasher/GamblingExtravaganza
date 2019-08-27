import requests
import config
import json
import csv
import os
import time


def run_driver():
    ncaa_fb_spreads_url = config.config_urls['ncaa_fb_spreads_url']
    ncaa_fb_totals_url = config.config_urls['ncaa_fb_totals_url']
    ncaa_fb_h2h_url = config.config_urls['ncaa_fb_h2h_url']

    ncaa_fb_spreads_response = requests.get(ncaa_fb_spreads_url)
    ncaa_fb_spreads = json.loads(ncaa_fb_spreads_response.content)

    ncaa_fb_totals_response = requests.get(ncaa_fb_totals_url)
    ncaa_fb_totals = json.loads(ncaa_fb_totals_response.content)

    ncaa_fb_h2h_response = requests.get(ncaa_fb_h2h_url)
    ncaa_fb_h2hs = json.loads(ncaa_fb_h2h_response.content)

    write_games_to_csv(ncaa_fb_spreads, ncaa_fb_totals, ncaa_fb_h2hs)


def write_games_to_csv(ncaa_fb_spreads, ncaa_fb_totals, ncaa_fb_h2hs):
    new_file = str(int(time.time())) + '.csv'
    if not os.path.exists(new_file):
        open(new_file, 'w').close()

    f = open(new_file, 'a')
    writer = csv.DictWriter(
        f, fieldnames=['HomeTeam', 'AwayTeam', 'Vendor', 'Favorite', 'HomeSpread', 'AwaySpread', 'HomeOdds', 'AwayOdds',
                       'OverUnder', 'OverOdds', 'UnderOdds', 'FaveMoneyLine', 'UnderdogMoneyLine', 'TravisPick'])
    writer.writeheader()

    all_games = ncaa_fb_spreads['data']
    all_totals = ncaa_fb_totals['data']
    all_h2hs = ncaa_fb_h2hs['data']

    for game in all_games:
        game_info = {}
        home_index = find_home_index(game['teams'], game['home_team'])
        away_index = find_away_index(game['teams'], game['home_team'])

        game_info['HomeTeam'] = game['home_team']
        game_info['AwayTeam'] = find_away_team(game['teams'], game['home_team'])

        for site in game['sites']:
            if site['site_key'] != 'betonlineag':
                continue
            game_info['Vendor'] = site['site_nice']
            game_info['Favorite'] = find_favorite(game['teams'], site['odds']['spreads']['points'])
            game_info['HomeSpread'] = site['odds']['spreads']['points'][home_index]
            game_info['AwaySpread'] = site['odds']['spreads']['points'][away_index]
            game_info['HomeOdds'] = site['odds']['spreads']['odds'][home_index]
            game_info['AwayOdds'] = site['odds']['spreads']['odds'][away_index]

        for total in all_totals:
            if total['home_team'] != game_info['HomeTeam']:
                continue
            for site in total['sites']:
                if site['site_key'] != 'betonlineag': # find a way to determine if site_key exists first
                    continue
                game_info['OverUnder'] = site['odds']['totals']['points'][0]
                game_info['OverOdds'] = site['odds']['totals']['odds'][0]
                game_info['UnderOdds'] = site['odds']['totals']['odds'][1]

        for h2h in all_h2hs:
            if h2h['home_team'] != game_info['HomeTeam']:
                continue
            for site in h2h['sites']:
                if site['site_key'] == 'betonlineag':
                    game_info['FaveMoneyLine'] = find_fave_money_line(home_index, away_index, site)
                    game_info['UnderdogMoneyLine'] = find_underdog_money_line(home_index, away_index, site)

        writer.writerows(
            [{'HomeTeam': game_info['HomeTeam'],
             'AwayTeam': game_info['AwayTeam'],
             'Vendor': game_info['Vendor'],
             'Favorite': game_info['Favorite'],
             'HomeSpread': game_info['HomeSpread'],
             'AwaySpread': game_info['AwaySpread'],
             'HomeOdds': game_info['HomeOdds'],
             'AwayOdds': game_info['AwayOdds'],
             'OverUnder': game_info['OverUnder'],
             'OverOdds': game_info['OverOdds'],
             'UnderOdds': game_info['UnderOdds'],
             'FaveMoneyLine': game_info['FaveMoneyLine'],
             'UnderdogMoneyLine': game_info['UnderdogMoneyLine']}
            ])
    f.close()


def find_away_team(teams, home_team):
    for team in teams:
        if team != home_team:
            return team


def find_favorite(teams, points):
    if points[0] > points[1]:
        return teams[1]
    elif points[1] > points[0]:
        return teams[0]
    else:
        return 'Push'


def find_home_index(teams, home_team):
    for num in range(0, len(teams)):
        if teams[num] == home_team:
            return num


def find_away_index(teams, home_team):
    for num in range(0, len(teams)):
        if teams[num] != home_team:
            return num


def find_fave_money_line(home_index, away_index, site):
    if site['odds']['h2h'][home_index] > site['odds']['h2h'][away_index]:
        return str(lower_money_line_formula(site['odds']['h2h'][away_index]))
    else:
        return str(lower_money_line_formula(site['odds']['h2h'][home_index]))


def find_underdog_money_line(home_index, away_index, site):
    if site['odds']['h2h'][home_index] < site['odds']['h2h'][away_index]:
        return '+' + str(higher_money_line_formula(site['odds']['h2h'][away_index]))
    else:
        return '+' + str(higher_money_line_formula(site['odds']['h2h'][home_index]))


def lower_money_line_formula(num):
    return int(round((-100) / (num - 1)))


def higher_money_line_formula(num):
    return int(round((num - 1) * (100)))
