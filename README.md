# Log Analyser

**LogAnalyser** is a Python-based tool for parsing, filtering, and gaining insights from log files.  
Designed to make it easier to extract meaningful information from raw logs, it supports customizable rules and flexible output formats.

---

## Features

- Load and process text-based log files  
- Filter logs by keywords or categories
- The whole run is based on generators
- Configuration file
- Available in 3 architectures designs
  - Monolithic architecture
  - Three tier architecture
  - MVC architecture (not yet implemented)

---

## Project layout

- Monolith
  - app.py - the whole log proggram
  - monolith_main - load the config via app.py and run the program
  - config.ini - configuration file, there you can change your path to the file
- ThreeTier
  - data.py - layer for communication with the file
  - logic.py - layer for logic things and to start the program
  - user_interface.py - layer that communicate with user
  - three_tier_main.py - configs the data layer path for file, run the program
- MVC (NOT YET IMPLEMENTED)

---

## Requirements

- Python 3.10+ (standard library only)

---

## Run the app on Windows

- Create or edit the JSON with initial accounts (optional). A sample file bank_accounts.json is included.

Run the program:

python .\main.py
