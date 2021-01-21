import sys
import os
import shutil
import subprocess
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
    # Help command requested
    if sys.argv[1].lower() in ['help', 'h']:
        print(
            'This script will create a directory, \'data_pack\', which will '
            'contain the necessary files to keep Seng running effectively on '
            'the ANN Discord serer.'
        )
        sys.exit()
    else:  # Otherwise, unrecognised
        print('I didn\'t recognise that argument.')

# Ensure that user wants to create a data pack
while True:
    yes_no = input('Would you like to create a data pack? y/n: ')
    if yes_no.lower() in ['y', 'n', 'yes', 'no']:
        break
    print('Please enter either \'y\' or \'n\'')

# Exit if user does not want to create data pack
if yes_no.lower() in ['n', 'no']:
    print('Exiting.')
    sys.exit()

# Must be within seng directory to run the script
if os.path.basename(os.path.normpath(os.getcwd())) != 'seng':
    print('Error: Script must be ran inside \'seng/\' directory.')
    print('Exiting.')
    sys.exit()

# Check for the existence of the public key
if os.exists(Path('./private/public_key.txt')):
    print('Public key found.')
else:
    print('Could not find public_key.txt. Please place it in the \'private\'
          'directory.')
    print('Exiting.')
    sys.exit()

# Try to make a new data pack
try:
    os.mkdir(Path('./data_pack'))
except FileExistsError:  # Only one data pack allowed
    print('data_pack already exists - only one data pack allowed!. Please 
          'delete it and try again.')
    print('Exiting.')
    sys.exit()

# Create all required, preliminary directories, within the data pack
for req_dir in required_directories:
    os.mkdir(os.path.join(Path('./data_pack'), 'server_specific'))

# Save individual files to the data pack
for file_path in files_to_save:
    dest_path = Path(os.path.join('./data_pack', file_path))
    shutil.copy(Path(file_path), dest_path)

# Save entire folders to the data pack
for dir_path in directories_to_save:
    dest_path = Path(os.path.join('./data_pack', dir_path))
    shutil.copytree(Path(dir_path), dest_path)

print('Success - data pack created. Now preparing to encrypt..')
# Run script which encrypts data pack immediately using the public key.
subprocess.call(['sh', './encrypt_data_pack.sh'])
