import requests
import sys
import argparse
import constants
from openpyxl import Workbook


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id')
    parser.add_argument('-v', '--venue')
    parser.add_argument('-t', '--team')
    

    return parser

def make_json_from_url(tournament_id, venue):
	url = f"https://api.rating.chgk.net/tournaments/{tournament_id}/results.json?includeTeamMembers=1&includeMasksAndControversials=1&includeTeamFlags=0&includeRatingB=0"
	if venue is not None:
		url += f"&venue={venue}"

	t = requests.get(url)

	return t.json()

def save_data_to_xlsx(data, filename):
	wb = Workbook()
	ws = wb.active
	for d in data:
		ws.append(d)

	wb.save(filename)

def preparing_list_for_squads():
	rows = []
	dict = {}
	dict['A'] = 'Team ID'
	dict['B'] = 'Название'
	dict['C'] = 'Город'
	dict['D'] = 'Флаг'
	dict['E'] = 'IDplayer'
	dict['F'] = 'Фамилия'
	dict['G'] = 'Имя'
	dict['H'] = 'Отчество'
	rows.append(dict)

	return rows

def preparing_list_for_results():
	rows = ['Team ID', 'Название','Город']
	for x in range(0, 36):
		rows.append(x + 1)

	return rows

def make_xslx_squad_from_json(table, tournament_id):
	rows = preparing_list_for_squads()
	for j in table:
		for player in j['teamMembers']:
			dict = {}
			dict['A'] = j['team']['id']
			dict['B'] = j['team']['name']
			dict['C'] = j['team']['town']['name']
			dict['D'] = player['flag']
			dict['E'] = player['player']['id']
			dict['F'] = player['player']['surname']
			dict['G'] = player['player']['name']
			dict['H'] = player['player']['patronymic']
			rows.append(dict)
		print(f"squad of team {j['team']['id']} added.")
	
	filename = f'{constants.NAME_SQUAD_FILE}{tournament_id}.xlsx'

	save_data_to_xlsx(rows, filename)

def make_xsls_results_from_json(table, tournament_id):
	result = []
	result.append(preparing_list_for_results())

	for j in table:
		id_team = j['team']['id']
		team_name = j['team']['name']
		team_town = j['team']['town']['name']
		rows = [id_team, team_name, team_town]
		print(f"preparing results of team {id_team} is in progress")
		if j['mask'] is not None:
			for x in range(0, 36):
				if j['mask'][x] == "X" or j['mask'][x] == "?":
					ball = j['mask'][x]
				else:
					ball = int(j['mask'][x])
				rows.append(ball)
			print(f"results of team {id_team} completed")
		else:
			for x in range(0, 36):
				rows.append(0)
			print(f"results of team {id_team} are not complete")
		result.append(rows)

	filename = f'{constants.NAME_RESULTS_FILE}{tournament_id}.xlsx'

	save_data_to_xlsx(result, filename)

def make_file(tournament_id, venue, id_team):
	teams = make_json_from_url(tournament_id, venue)

	if id_team is not None:
		for t in teams:
			id_iterable = int(t['team']['id'])
			if id_iterable == id_team:
				print(f"making squad of team {id_team}")
				rows = [t]
				make_xslx_squad_from_json(rows,tournament_id)
				make_xsls_results_from_json(rows, tournament_id)
				return
		print(f"haven't find team with id {id_team}")

	print(f"preparing data from venue {venue}")
	make_xslx_squad_from_json(teams, tournament_id)
	make_xsls_results_from_json(teams, tournament_id)


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    if namespace.id:
    	tournament_id = namespace.id
    if namespace.venue:
    	venue = namespace.venue
    else:
    	venue = None
    if namespace.team:
    	team = int(namespace.team)
    else:
    	team = None

    make_file(tournament_id, venue, team)

