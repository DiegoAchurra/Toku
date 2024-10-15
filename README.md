# Superhero Battle Simulator

This repository contains a **Superhero Battle Simulator** built using the [Superhero API](https://www.superheroapi.com/) to simulate battles between randomly chosen heroes and villains. This project was developed based on the instructions outlined in the **"Pelea de personajes"** PDF document, which required simulating battles between randomly generated teams.

## Features

- **Team Generation**: The simulator randomly selects two teams of 5 characters, with no repeating IDs, and ensures that each team is either good or bad based on the majority alignment of its members.
  
- **Stats Calculation**:
  - **Actual Stamina (AS)**: Each character is assigned an "Actual Stamina" stat, which is a random value between 0 and 10.
  - **Filiation Coefficient (FB)**: Depending on whether the character's alignment matches their team's alignment, a bonus or penalty is applied to their stats.
  - **Health Points (HP)**: Initially, we calculated HP for each character using base stats, but this led to inconsistencies in how stats were handled. Since the PDF instructions are not entirely clear, we made the decision to calculate HP after updating the character's stats at the start of the simulation. This ensures that the character can withstand the "buffed" attacks throughout the battle. Characters recover full health at the start of each battle round.
  
- **Attack Types**:
  - There are three possible attack types: **Mental**, **Strong**, and **Fast**. Each type calculates damage based on specific character stats like intelligence, strength, and speed.
  
- **Battle Mechanics**:
  - For the first five rounds, each character from both teams is matched against a corresponding opponent based on their position in the team lineup (i.e., first hero vs. first hero, second hero vs. second hero, etc.).
  - Battles are printed to the console, showing the attack sequence and the damage dealt until one character's HP reaches zero.
  - After the first five rounds, the remaining characters will battle randomly until all heroes from one team are defeated.
  
  
- **Mail Summary**:
  - After the simulation, the user can input an email address, and the system will send a summary of the battle to the provided email using a mail service.

## Project Structure

- **urls.py**: Defines the routing for the application, creating three key endpoints:
  - An endpoint for the battle simulation initiation.
  - An endpoint for sending the battle results via email.
  - The index endpoint, which clears any previous session data and presents the start page.

- **views.py**: Implements the Django views responsible for handling HTTP requests. Each view calls the appropriate service logic and returns the results:
  - The `index_view` clears session data and serves the index page.
  - The `battle_simulation_view` initiates the battle simulation, calling the logic from the service layers and storing the results in the session.
  - The `send_battle_email_view` triggers the email sending process for the battle results.

- **service.py**: Organized within directories named based on the type of service (e.g., `Battle`, `FetchHero`, `Alignment`), this file contains the core logic for:
  - **Team creation**: Randomly generates two teams of characters for the battle.
  - **HP calculation**: Calculates each character's health points based on their stats, ensuring they are properly initialized and not recalculated during the battle.
  - **Attack damage calculation**: Handles the logic for calculating different types of attacks (mental, strong, fast) and applying damage based on characters' updated stats.
  - **Stat updates**: Applies filiation bonuses and other stat modifiers to characters before the battle starts, ensuring fair calculation and application of buffs.

This modular structure keeps the code organized and ensures a separation of concerns between routing, request handling, and business logic.

## Installation

To run this project, follow these steps:

1. **Clone the repository**:

```bash
git clone https://github.com/DiegoAchurra/Toku_Project.git
cd Toku_Project
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Run the Django server**:

```bash
python manage.py runserver
```

## Usage

1. **Start the Simulation**: After starting the server, navigate to the homepage (`http://127.0.0.1:8000/`). The homepage will show a "Start Simulation" button. Click it to initiate the battle simulation.

2. **View Battle Results**: Once the battle is simulated, you will be redirected to the battle results page. Here you will see:
   - A list of heroes for each team, including their names, alignments, and updated stats (with their HP displayed as badges).
   - A detailed battle history showing the round-by-round results, including which hero won each round.
   - The final winner of the simulation and surviving heroes.

3. **Re-Simulate or Return to Index**: You can either re-simulate the battle by clicking the "Re-Simulate" button or return to the index page, which will clear the session and start fresh.

4. **Send Battle Summary via Email**: At the end of the battle, you can input an email address and send the battle results summary to yourself or someone else.

## Acknowledgments

This project was developed as part of the 'Pelea de personajes' exercise provided by the Toku team. A special thanks to them for the opportunity to showcase my skills through such an engaging and enjoyable challenge.

I utilized tools like ChatGPT during the development process to help accelerate certain coding tasks, such as structuring initial code drafts and generating documentation outlines. This allowed me to focus on refining and enhancing the core functionality of the project while maintaining efficiency. Using such tools thoughtfully enabled me to streamline repetitive tasks, while ensuring the final result reflected my own technical skills and problem-solving abilities.
