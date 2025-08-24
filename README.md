
# SCE LED Matrix

The SCE LED Matrix is an SCE intern project for Winter 2024. The matrix consists of four interconnected LED panels, controlled by a Raspberry Pi.  
This repository contains code and resources for controlling and managing the SCE LED Matrix Display. The below is a description of the layout of this repository.

## Main Files

- **start_led.sh**: The script to start the entire session. This uses the `tmux` command to run both the LED Matrix and the FastAPI code.
- **server.py**: The main Python script for running the LED Matrix server. Handles requests, controls the database, and manages communication.
- **docker-compose.yml**: The script to Dockerize the FastAPI backend. Run this file using `docker-compose up --build`.
- **Dockerfile**: Contains configuration information for the Docker container.
- **server_config.yml**: YAML configuration file for the server. Allows customization of which database file to use, API keys, and what port to run the server on. 
- **requirements.txt**: Lists the Python dependencies required to run the project. Install with `pip install -r requirements.txt`.
- **text-example**: C++ binary that connects Python backend to the Raspberry Pi, allowing the Pi to control the LED panels to display text.
- **5x7.bdf**: Bitmap Distribution Format (BDF) font file for a 5x7 pixel font, used for rendering text on the LED matrix.

## modules/ Directory
Contains helper modules and utilities used by the main server script:

- **args.py**: Handles command-line argument parsing for the server or scripts.
- **leetcode_helpers.py**: Contains helper functions related to fetching and displaying LeetCode stats for registered users of the leaderboard.
- **logger.py**: Provides logging functionality for the server and other scripts, enabling debug and info output.
- **sqlite_helpers.py**: Helper functions for interacting with SQLite databases, used for storing and retrieving registered users' data.

---

## How To Run The Project
1. Run `./start_led.sh`. There. That's it! 

## Contact
For questions or support, contact the repository owners:
- [Oliver Majano](https://github.com/iOliver678)
- [Adarsh Mallya](https://github.com/adarshm11)
- [Evan Ugarte](https://github.com/evanugarte)

---
