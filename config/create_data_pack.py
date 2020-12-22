import sys
import os
import shutil
from pathlib import Path
from distutils.dir_util import copy_tree

# Directories needed for specific, individual files
required_directories = [
    'server_specific'
]

# Specific, individual files to save
files_to_save = [
    'server_specific/channel_ids.json',
    'server_specific/moderators.txt'
]

# Entire directories to save
directories_to_save = [
    'server_specific/welcome_blocks'
]


if len(sys.argv) > 1:
    if sys.argv[1].lower() in ['help', 'h']:
        print(
            'This script will create a directory, \'data_pack\', which will '
            'contain the necessary files to keep Seng running effectively on '
            'the ANN Discord serer.'
        )
        sys.exit()
    else:
        print('I didn\'t recognise that argument.')

while True:
    yes_no = input('Would you like to create a data pack? y/n: ')
    if yes_no.lower() in ['y', 'n', 'yes', 'no']:
        break
    print('Please enter either \'y\' or \'n\'')

if yes_no.lower() in ['n', 'no']:
    print('Exiting.')
    sys.exit()

if yes_no.lower() in ['y', 'yes']:
    if os.path.basename(os.path.normpath(os.getcwd())) != 'seng':
        print('Error: Script must be ran inside \'seng/\' directory.')
        print('Exiting.')
        sys.exit()

    try:
        os.mkdir(Path('./data_pack'))
    except FileExistsError:
        print('data_pack already exists. Please delete it and try again.')
        print('Exiting.')
        sys.exit()

    for req_dir in required_directories:
        os.mkdir(os.path.join(Path('./data_pack'), 'server_specific'))

    for file_path in files_to_save:
        dest_path = Path(os.path.join('./data_pack', file_path))
        shutil.copy(Path(file_path), dest_path)

    for dir_path in directories_to_save:
        dest_path = Path(os.path.join('./data_pack', dir_path))
        shutil.copytree(Path(dir_path), dest_path)

    print('Success - data pack created.')
