import random
def determine_team_alignment(team):
    good_count = sum(1 for hero in team if hero['biography']['alignment'] == 'good')
    bad_count = sum(1 for hero in team if hero['biography']['alignment'] == 'bad')

    if good_count > bad_count:
        return 'good'
    elif bad_count > good_count:
        return 'bad'
    else:
        return random.choice(['good', 'bad'])