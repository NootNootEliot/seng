# Used to initialise folders that are not on the github repository
import os
from pathlib import Path

directories_to_make = [
    'private',
    'server_specific',
]

files_to_make = [
    'private/priv_data.json',
    'server_specific/moderators.txt',
    'server_specific/channel_ids.json'
]

while True:
    yes_no = input('Do you have a data pack? ')
    if yes_no.lower() not in ['yes', 'no']:
        print('Please enter either \'yes\' or \'no\'.')
    else:
        break

if yes_no.lower() == 'yes':
    print('This feature is not yet supported!')
    pass
elif yes_no.lower() == 'no':
    input(
        'Warning. If there are existing files within this project, then they '
        'will be removed. Press ENTER to continue, or CTRL + C to cancel.'
    )
    print('\nCreating paths.')
    for directory_to_make in directories_to_make:
        try:
            os.mkdir(Path(directory_to_make))
        except FileExistsError:
            print('\tError: {} already exists.'.format(directory_to_make))

    print('\nAdding files to paths.')
    for file_to_make in files_to_make:
        open(Path(file_to_make), 'w').close()
    print('Please remember to add the appropriate data to these files.')
