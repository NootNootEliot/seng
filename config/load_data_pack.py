import sys
import os
import shutil
from pathlib import Path

required_directories = [
    'server_specific',
    'server_specific/welcome_blocks'
]

if len(sys.argv) > 1:
    if sys.argv[1].lower() in ['help', 'h']:
        print(
            'This script will load the \'data_pack\' directory, and will then '
            'load those files contained within \'data_pack\' to seng\'s '
            'directory. Typically, this script should be ran after a \'git '
            'clone \' is performed.'
        )
    else:
        print('I didn\'t recognise that argument.')

while True:
    yes_no = input('Would you like to load in the data pack? y/n: ')
    if yes_no.lower() in ['y', 'n', 'yes', 'no']:
        break
    print('Please enter either \'y\' or \'n\'')

if yes_no.lower() in ['n', 'no']:
    print('Exiting.')
    sys.exit()

if os.path.basename(os.path.normpath(os.getcwd())) != 'seng':
    print('Error: Script must be ran inside \'seng/\' directory.')
    print('Exiting.')
    sys.exit()

if os.path.exists('./data_pack'):
    if not os.path.isdir('./data_pack'):
        print('Error: data_pack is not a directory.')
        print('Exiting.')
        sys.exit()
else:
    print(
        'Error: Could not locate data_pack. Is it inside the \'seng\' '
        'directory?'
    )
    print('Exiting.')
    sys.exit()

for req_dir in required_directories:
    try:
        os.mkdir(req_dir)
    except FileExistsError:
        while True:
            yes_no = input(
                'The directory \'{}\' already exists. Would you like to '
                'replace it? y/n: '.format(req_dir)
            )
            if yes_no.lower() in ['y', 'n', 'yes', 'no']:
                break
            else:
                print('Please enter either \'y\' or \'n\'.')
    if yes_no.lower() in ['y', 'yes']:
        shutil.rmtree(req_dir)
        os.mkdir(req_dir)


for root, dirs, files in os.walk(Path('./data_pack')):
    for name in files:
        data_path = os.path.join(root, name)  # File in data_pack's path
        # Destination in Seng for file to go
        insert_path = data_path.replace('data_pack/', '')
        if os.path.isfile(insert_path):
            while True:
                yes_no = input(
                    'The file \'{}\' already exists. Would you like to '
                    'replace it? y/n: '.format(insert_path)
                )
                if yes_no.lower() in ['y', 'n', 'yes', 'no']:
                    break
                else:
                    print('Please enter either \'y\' or \'n\'.')
            if yes_no.lower() in ['y', 'yes']:
                shutil.copyfile(data_path, insert_path)
        else:
            shutil.copyfile(data_path, insert_path)
print('\nSuccess - data loading complete.')
