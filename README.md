# Seng

Seng is a Discord Bot that exists to support the Astra Nova Network.

### Installation for Development
1. Clone this repository to your local machine.
2. Install `poetry`, the dependency manager that Seng uses.
    - To install `poetry`, check their [documentation](https://python-poetry.org/)
3. `cd` into this project's main directory.
4. Run `poetry install`.
5. Run `poetry shell`.
6. You're ready to go!

### Set-Up
 - To test locally, you will need your own token and Discord bot.
 - You can run the Python scripts in config for some automated help.


If they are cloning and have a data pack, they will need to put keys into
the private folder, and then run from within the root seng directory,
load_data_pack.py followed by file_check.py, to make sure things are working.

If they are cloning and do not have a data pack, they will need to use
create_blank_files.py, follow the instructions, and tthen run file_check.py.

Running seng requires a token. Use a local token.

Further pre-requisites: Discord role called 'Tourist', and another called
'Resident'.