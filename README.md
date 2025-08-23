
# SCE LED Matrix

The SCE LED Matrix is an SCE intern project for Winter 2024. The matrix consists of four interconnected LED panels, controlled by a Raspberry Pi.  
This repository contains code and resources for controlling and managing the SCE LED Matrix Display. The below is a description of the layout of this repository.

## Main Files

- **server.py**: The main Python script for running the LED Matrix server. Handles requests, controls the database, and manages communication.
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

## Getting Started
1. **Create a Python virtual environment to run the backend:**  `python3 -m venv .venv`
2. **Activate the virtual environment:**  
**On MacOS/Linux:** `source .venv/bin/activate`  
**On Windows:** `.venv\Scripts\activate`   
3. Install dependencies: `pip install -r requirements.txt`
4. Configure the server to your liking using `server_config.yml`.
5. Run the server: `python server.py`
6. Finally, start the LED Matrix: `./start.sh`  

## Contact
For questions or support, contact the repository owners:
- [Oliver Majano](https://github.com/iOliver678)
- [Adarsh Mallya](https://github.com/adarshm11)
- [Evan Ugarte](https://github.com/evanugarte)

---
