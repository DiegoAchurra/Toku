from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
import random
from .FetchHero.service import fetch_superhero_data
from .Battle.service import simulate_battle
from .Alignment.service import determine_team_alignment
from django.core.mail import EmailMultiAlternatives

# Index page view (title and button)
def index_view(request):
    # Clear session data whenever the index page is loaded
    request.session.clear()

    # Show the simple index page with just the button
    return render(request, 'index.html')

# Battle simulation view
def battle_simulation_view(request):
    if request.method == 'POST':
        hero_ids = set()  # Set to track used hero IDs

        # Function to get a unique hero ID
        def get_unique_hero_id():
            while True:
                hero_id = random.randint(1, 731)
                if hero_id not in hero_ids:
                    hero_ids.add(hero_id)
                    return hero_id

        # Fetching unique heroes for both teams
        team_a = [fetch_superhero_data(get_unique_hero_id()) for _ in range(5)]
        team_b = [fetch_superhero_data(get_unique_hero_id()) for _ in range(5)]

        # Determine team alignment
        alignment_team_a = determine_team_alignment(team_a)
        alignment_team_b = determine_team_alignment(team_b)

        # Simulating the battle and collecting the tale (step-by-step process)
        winner, original_team_a, original_team_b, battle_tale, winning_team = simulate_battle(
            team_a, team_b, alignment_team_a, alignment_team_b
        )

        print(f'\nAnd the winning Team is: {winner}')

        # Store battle results in session
        request.session['team_a'] = original_team_a
        request.session['team_b'] = original_team_b
        request.session['team_a_alignment'] = alignment_team_a
        request.session['team_b_alignment'] = alignment_team_b
        request.session['battle_tale'] = battle_tale
        request.session['winner'] = winner
        request.session['winning_team'] = winning_team
        request.session['battle_started'] = True  # Mark battle as started

        # Redirect to the same page to display the battle results
        return redirect('battle_simulation')

    # Fetch battle results from session if they exist
    context = {
        'team_a': request.session.get('team_a'),
        'team_b': request.session.get('team_b'),
        'team_a_alignment': request.session.get('team_a_alignment'),
        'team_b_alignment': request.session.get('team_b_alignment'),
        'battle_tale': request.session.get('battle_tale'),
        'winner': request.session.get('winner'),
        'winning_team': request.session.get('winning_team'),
        'email_sent': request.session.pop('email_sent', False),  # Get and remove the email flag
    }
    return render(request, 'clash/battle-simulation.html', context)

# Email sending view (same as before)
def send_battle_email_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        team_a = request.session.get('team_a', [])
        team_b = request.session.get('team_b', [])
        team_a_alignment = request.session.get('team_a_alignment', 'Unknown')
        team_b_alignment = request.session.get('team_b_alignment', 'Unknown')
        battle_tale = request.session.get('battle_tale', [])
        winner = request.session.get('winner', 'Unknown')
        winning_team = request.session.get('winning_team', [])

        # Build the HTML content for the email
        battle_html = f"""
        <html>
        <body>
            <h1 style="text-align: left; color: green;">Battle Summary</h1>

            <h2 style="color: blue;">Team A ({team_a_alignment})</h2>
            <ul>
                {''.join([f"<li>{hero['name']} ({hero['biography']['alignment']}) - {hero['hp']} HP</li>" for hero in team_a])}
            </ul>

            <h2 style="color: blue;">Team B ({team_b_alignment})</h2>
            <ul>
                {''.join([f"<li>{hero['name']} ({hero['biography']['alignment']}) - {hero['hp']} HP</li>" for hero in team_b])}
            </ul>

            <h3 style="color: red;">Battle Rounds</h3>
            <ul>
                {''.join([f"<li>Round {round['round_num']}: {round['hero_a']} vs {round['hero_b']} - <strong>{round['winner']}</strong> wins</li>" for round in battle_tale])}
            </ul>

            <h2 style="color: green;">Winner: <strong>{winner}</strong></h2>
            <h3>Surviving Heroes in <strong>{winner}</strong>:</h3>
            <ul>
                {''.join([f"<li>{hero['name']}</li>" for hero in winning_team])}
            </ul>
        </body>
        </html>
        """

        # Set up the email with both plain text and HTML versions
        subject = 'Battle Summary'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]

        text_content = f"Battle Summary\n\nWinner: {winner}"  # Fallback for plain text email clients
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(battle_html, "text/html")

        # Send the email
        msg.send()

        # Set email sent flag in the session and redirect back to the battle simulation page
        request.session['email_sent'] = True
        return redirect('battle_simulation')

    return redirect('index')
