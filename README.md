# Space-Invaders
Built Space Invaders in class because I was bored and college had blocked the game site.

Overview
Control your spaceship to shoot enemies that gradually become more challenging. Enemies are positioned in a grid with increasing rows and columns, and their firing rate intensifies as levels advance.

Features
Matrix of Enemies: Enemies are organized in a grid that scales with the level.

Dynamic Difficulty: Enemy speed, firing frequency, and formation complexity increase with each level.

Player and Enemy Shooting: Both the player and enemies can shoot bullets.

Collision Detection: Simple collision detection handles interactions between bullets, enemies, and the player.

Game Over State: The game ends when enemies reach too close to the bottom or the player is hit.

Controls
Left Arrow: Move left

Right Arrow: Move right

Space Bar: Fire bullet

Escape: Exit the game

Installation
Install Python 3.x:
Download and install Python from python.org.

Install Pygame:
Open your terminal or command prompt and run:

bash
Copy
pip install pygame
Clone or Download the Repository:
Ensure that you have the following asset files in the same folder as the Python script:

player.png — the player's spaceship

enemy.png — the enemy sprite

bullet.png — the bullet image

Usage
Run the game from your terminal or command prompt with:

bash
Copy
python your_game_file.py
Replace your_game_file.py with the filename of your Python script.

Customization
Enemy Formation:
Modify the spawn_enemies(level) function to change the number of rows and columns.

Difficulty Settings:
Adjust variables such as enemy speed, descent amount, and bullet cooldown in the reset_level(lvl) function for a custom challenge.

Graphics:
Swap out the player.png, enemy.png, and bullet.png files with your own images. Adjust image scaling in the code if needed.

Contributing
Contributions are welcome! To contribute:

Fork the repository.

Create a new branch for your changes.

Submit a pull request with a detailed description of your changes.

License
This project is licensed under the MIT License.
