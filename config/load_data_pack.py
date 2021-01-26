import sys
import os
import shutil
from pathlib import Path

required_directories = [
    'server_specific',
    'server_specific/welcome_blocks'
]

# Capture a possible 'help' command, otherwise, don't recognise
if len(sys.argv) > 1:
    if sys.argv[1].lower() in ['help', 'h']:
        print(
            'Requirements:\n'
            ' - data_pack.tar.gz.age should be present within the seng '
            'directory.\n'
            ' - No other files with \'data_pack\' in the name should exist '
            'anywhere else witin the file tree.\n'
            'This script attempts decryption of the encrypted data_pack file, '
            'ultimately followed by loading of files within the data_pack '
            'into their corresponding locations.'
        )
    else:
        print('I didn\'t recognise that argument.')

# Check that the user dedfinitely wants to load in a data pack
while True:
    yes_no = input('Would you like to load in the data pack? y/n: ')
    if yes_no.lower() in ['y', 'n', 'yes', 'no']:
        break
    print('Please enter either \'y\' or \'n\'')

# They do not want to load in a data pack, so exit
if yes_no.lower() in ['n', 'no']:
    print('Exiting.')
    sys.exit()

# Must be within seng directory to run the script
if os.path.basename(os.path.normpath(os.getcwd())) != 'seng':
    print('Error: Script must be ran inside \'seng/\' directory.')
    print('Exiting.')
    sys.exit()

# Check if there's already a data_pack folder, which would be strange
if os.path.exists('./data_pack'):
    print('Error: data_pack directory already exists. Please remove it and '
          'decrypt from an encrypted data pack.')
    print('Exiting.')
    sys.exit()

# Check if encrypted data pack exists
if os.path.exists('./data_pack.tar.gz.age'):
    print('Encrypted data_pack found.')
    if os.path.exists('./private/key.txt'):
        print('Found key.')
    else:
        print('I could not find the private key. Ensure that the key.txt file'
              'is kept within the /private directory.')
        print('Exiting.')
        sys.exit()
    print('Attempting decryption..')
    subprocess.call(['sh', './decrypt_data_pack.sh'])

# Check that the data_pack directory exists
if os.path.exists('./data_pack'):
    # Check that data_pack is a directory
    if not os.path.isdir('./data_pack'):
        print('Error: data_pack is not a directory.')
        print('Exiting.')
        sys.exit()
else:
    print(
        'Error: Could not locate data_pack. Is it inside the \'seng\' '
        'directory? Have you decrypted the data_pack?'
    )
    print('Exiting.')
    sys.exit()

# Make the directories necessary for Seng to put files from the data_pack
for req_dir in required_directories:
    try:
        os.mkdir(req_dir)
    except FileExistsError:
        # The directory already exists, so we ask the user if they'd like it
        # replaced 
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
        # Remove the directory
        shutil.rmtree(req_dir)
        os.mkdir(req_dir)

# Walk through data_pack, and effectively replicate the file tree, but within
# 'seng'
for root, dirs, files in os.walk(Path('./data_pack')):
    for name in files:
        data_path = os.path.join(root, name)  # File in data_pack's path
        # Destination in 'seng' directory for file to go
        insert_path = data_path.replace('data_pack/', '')
        
        # Check if the file already exists
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
                # Replace the file
                shutil.copyfile(data_path, insert_path)
        else:
            shutil.copyfile(data_path, insert_path)
print('\nSuccess - data loading complete.')
print('Deleting the data_pack directory:')
shutil.rmtree('./data_pack')
print('Data pack loading complete.')
