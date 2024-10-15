import random

# ---------------------------------------------------------------------------------------------------- #
# Main function to simulate a battle between two teams
def simulate_battle(team_a, team_b, alignment_team_a, alignment_team_b):
    battle_tale = []  # List to hold the story of each round
    battle_results = []  # Store the results of the first 5 rounds

    # Create copies of the original teams
    original_team_a = team_a.copy()
    original_team_b = team_b.copy()

    # Assign initial stats, Filiation Bonus, and HP
    for hero in team_a + team_b:
        hero['AS'] = random.randint(0, 10)

        team_alignment = alignment_team_a if hero in team_a else alignment_team_b
        hero['fb'] = calculate_filiation_bonus(hero['biography']['alignment'], team_alignment)

        update_stats_with_formula(hero)

        hero['hp'] = calculate_hp(hero)
        hero['base_hp'] = hero['hp']  # Store base HP to reset it at the start of each round

    round_num = 1

    # First 5 rounds: Match corresponding heroes based on their list position
    for i in range(5):
        if i < len(team_a) and i < len(team_b):
            if team_a[i]['hp'] > 0 and team_b[i]['hp'] > 0:
                # Simulate the round
                loser = simulate_round(team_a[i], team_b[i])

                # Determine the winner
                winner = team_a[i] if loser in team_b else team_b[i]

                # Store the result for elimination after the first 5 rounds
                battle_results.append((team_a[i], team_b[i], loser))

                # Add round information to the battle tale with the winner included as structured data
                battle_tale.append({
                    'round_num': round_num,
                    'hero_a': team_a[i]['name'],
                    'hero_b': team_b[i]['name'],
                    'winner': winner['name']
                })
                round_num += 1

    # After the first 5 rounds, eliminate the defeated heroes
    print(f"")
    for hero_a, hero_b, loser in battle_results:
        if loser in team_a:
            team_a.remove(loser)
            print(f"{loser['name']} has been removed from Team A.")
        elif loser in team_b:
            team_b.remove(loser)
            print(f"{loser['name']} has been removed from Team B.")

    # Continue the battle randomly with the remaining heroes
    while any(hero['hp'] > 0 for hero in team_a) and any(hero['hp'] > 0 for hero in team_b):
        # Choose random heroes who still have HP > 0
        hero_a = random.choice([h for h in team_a if h['hp'] > 0])
        hero_b = random.choice([h for h in team_b if h['hp'] > 0])

        # Simulate the round
        loser = simulate_round(hero_a, hero_b)

        # Determine the winner
        winner = hero_a if loser in team_b else hero_b

        # Simulate a round and record the winner in the battle tale
        battle_tale.append({
            'round_num': round_num,
            'hero_a': hero_a['name'],
            'hero_b': hero_b['name'],
            'winner': winner['name']
        })
        round_num += 1

        # Remove the losing hero
        print(f"")
        if loser in team_a:
            team_a.remove(loser)
            print(f"{loser['name']} has been removed from Team A.")
        elif loser in team_b:
            team_b.remove(loser)
            print(f"{loser['name']} has been removed from Team B.")

    # Determine the final winner
    if any(hero['hp'] > 0 for hero in team_a):
        final_winner = "Team A"
        winning_team = team_a  # Store the final list of surviving heroes
    else:
        final_winner = "Team B"
        winning_team = team_b  # Store the final list of surviving heroes

    # Return the final state of the battle along with the original teams and the winning team's survivors
    return final_winner, original_team_a, original_team_b, battle_tale, winning_team

# ---------------------------------------------------------------------------------------------------- #
# Function to calculate Filiation Coefficient (FB)
def calculate_filiation_bonus(character_alignment, team_alignment):
    rand_value = random.uniform(0, 9)
    if character_alignment == team_alignment:
        filiation_bonus = 1 + rand_value
    else:
        filiation_bonus = (1 + rand_value) ** -1

    # Print debug information
    print(f"\nCalculating Filiation Bonus:")
    print(f"  Character Alignment: {character_alignment}")
    print(f"  Team Alignment: {team_alignment}")
    print(f"  Random Value: {rand_value:.2f}")
    print(f"  Filiation Bonus: {filiation_bonus:.2f}")

    return filiation_bonus

# ---------------------------------------------------------------------------------------------------- #
# Update stats based on formula
def update_stats_with_formula(hero):
    print(f"\nUpdating stats for {hero['name']}...")  # Print when the function is called for each hero
    stats_to_update = ['intelligence', 'strength', 'speed', 'durability', 'power', 'combat']
    for stat in stats_to_update:
        base_value = get_stat_value(hero['powerstats'][stat])
        AS = hero['AS']
        FB = hero['fb']
        updated_stat = ((2 * base_value + AS) / 1.1) * FB
        hero['powerstats'][stat] = int(updated_stat)  # Round to an integer
        print(f"  {stat.capitalize()}: base value = {base_value}, updated value = {updated_stat:.2f}")  # Print stat details

    return hero

# ---------------------------------------------------------------------------------------------------- #
# Calculate HP based on stats, should only be called once
def calculate_hp(hero):
    strength = get_stat_value(hero['powerstats']['strength'])
    durability = get_stat_value(hero['powerstats']['durability'])
    power = get_stat_value(hero['powerstats']['power'])
    AS = hero.get('AS', 0)

    # Debug print to track stats before calculating HP
    print(f"\nCalculating HP for {hero['name']}:")
    print(f"  Strength: {strength}")
    print(f"  Durability: {durability}")
    print(f"  Power: {power}")
    print(f"  AS: {AS}")

    # Calculate HP once
    hp = ((strength * 0.8 + durability * 0.7 + power) / 2) * (1 + AS / 10) + 100
    return int(hp)  # Round to an integer

# ---------------------------------------------------------------------------------------------------- #
# Simulate a round between two heroes (HP adjusted only locally)
def simulate_round(hero1, hero2):
    # At the start of each round, reset the HP to the base HP
    hero1_hp = hero1['base_hp']
    hero2_hp = hero2['base_hp']

    print(f"\n--- New Round: {hero1['name']} (hp: {hero1_hp}) vs {hero2['name']} (hp: {hero2_hp}) ---")

    # Determine who attacks first based on speed
    hero1_speed = get_stat_value(hero1['powerstats']['speed'])
    hero2_speed = get_stat_value(hero2['powerstats']['speed'])

    if hero1_speed >= hero2_speed:
        first_attacker, second_attacker = hero1, hero2
        first_attacker_hp, second_attacker_hp = hero1_hp, hero2_hp
    else:
        first_attacker, second_attacker = hero2, hero1
        first_attacker_hp, second_attacker_hp = hero2_hp, hero1_hp

    print(f"{first_attacker['name']} attacks first due to higher speed!")

    attacks = ['Mental', 'Strong', 'Fast']

    first_attack_printed = False
    second_attack_printed = False

    while first_attacker_hp > 0 and second_attacker_hp > 0:
        # First attack
        first_attack = random.choice(attacks)
        first_damage = calculate_attack(first_attacker, first_attack)
        second_attacker_hp -= first_damage

        # Only print the first attack once
        if not first_attack_printed:
            print(f"{first_attacker['name']} uses {first_attack} attack and deals {first_damage} damage. {second_attacker['name']} has {max(0, second_attacker_hp)} HP left.")
            first_attack_printed = True

        if second_attacker_hp <= 0:
            # Final blow by first attacker
            print(f"At the end of the day... {first_attacker['name']} defeated {second_attacker['name']}!")
            return second_attacker  # Return the loser

        # Second attack
        second_attack = random.choice(attacks)
        second_damage = calculate_attack(second_attacker, second_attack)
        first_attacker_hp -= second_damage

        # Only print the second attack once
        if not second_attack_printed:
            print(f"{second_attacker['name']} uses {second_attack} attack and deals {second_damage} damage. {first_attacker['name']} has {max(0, first_attacker_hp)} HP left.")
            second_attack_printed = True

        if first_attacker_hp <= 0:
            # Final blow by second attacker
            print(f"At the end of the day... {second_attacker['name']} defeated {first_attacker['name']}!")
            return first_attacker  # Return the loser

# ---------------------------------------------------------------------------------------------------- #
# Function to calculate the attack damage
def calculate_attack(hero, attack_type):
    intelligence = get_stat_value(hero['powerstats']['intelligence'])
    strength = get_stat_value(hero['powerstats']['strength'])
    speed = get_stat_value(hero['powerstats']['speed'])
    durability = get_stat_value(hero['powerstats']['durability'])
    power = get_stat_value(hero['powerstats']['power'])
    combat = get_stat_value(hero['powerstats']['combat'])
    FB = hero['fb']  # Filiation Bonus

    if attack_type == 'Mental':
        mental_damage = (intelligence * 0.7 + speed * 0.2 + combat * 0.1) * FB
        return int(mental_damage)  # Round to an integer

    elif attack_type == 'Strong':
        strong_damage = (strength * 0.6 + power * 0.2 + combat * 0.2) * FB
        return int(strong_damage)  # Round to an integer

    elif attack_type == 'Fast':
        fast_damage = (speed * 0.55 + durability * 0.25 + strength * 0.2) * FB
        return int(fast_damage)  # Round to an integer

    return 0

# ---------------------------------------------------------------------------------------------------- #
# Helper function to convert powerstats to a number or default to 0
def get_stat_value(stat):
    try:
        return int(stat) if stat != 'null' else 0
    except (ValueError, TypeError):
        return 0

# ---------------------------------------------------------------------------------------------------- #