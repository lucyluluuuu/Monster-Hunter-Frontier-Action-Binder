# MHFActionBinder

A GUI tool for remapping controller buttons in Monster Hunter Frontier's `keyconfig.cfg` file.

## Features

- **Visual controller layout** - See all available buttons and their hex values
- **English translations** - Japanese action names are displayed in English while preserving original Japanese in the config file
- **Button combinations** - Support for multi-button bindings (e.g., Y+B)
- **Dual-button bindings** - Primary button (key) + Secondary button (subkey)
- **Shift-JIS encoding** - Preserves the original Japanese encoding required by the game
- **Automatic backups** - Creates timestamped backups before saving
- **Only saves changes** - Only modified actions are written to the file

## Requirements

- Python 3.6 or higher
- Tkinter (comes with Python)


## How It Works

- The tool parses the <controller> tag attributes (line ~8) to understand which hex values correspond to each physical button.

- Then it updates the keydata key= and subkey= values for each action in the selected category.

## Usage

- Load your config - Click "Load Config" and select your keyconfig.cfg file

- Select a category - Choose a weapon category from the dropdown (Basic Actions, Great Sword, etc.)

- Rebind actions - Use the dropdown menus to select which button each action should use

- Save changes - Click "Save Changes" to write modifications back to the file


## Installation

- Simply take the release, and place the main.py into your MH Frontier folder in it's own folder i.e. C:\Games\Frontier\MHFActionBinder\main.py  

- It is recommended to copy and paste your keycfg into the MHFActionBinder folder and then copy and paste it back after your binds are set but the program does do it's own backups if you're feeling brave.

- Create a txt file and name it e.g. run.bat and edit it and add "py main.py" and save it. NOTE: YOU MUST INSTALL PYTHON FROM HERE: https://www.python.org/downloads/release/python-3146/ use the 64 bit installer make sure global py gets installed as well as the Python environment variables

## Questions/Concerns/Bug Reports

- Contact me on Discord if you have issues: .LuluKitty
