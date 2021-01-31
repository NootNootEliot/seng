import sys
import os
import shutil

# Check if user is requesting help on this script
if len(sys.argv) > 1:
    if sys.argv[1].lower() in ['help', 'h']:
        print(
            'This script will populate the seng directory with blank template '
            'files/directories. If a file/directory already exists, you will '
            'be asked if you\'d like that file/directory to be replaced. To '
            'load in a data_pack, please use load_data_pack.py instead.'
        )
        sys.exit()
    else:
        print('I didn\'t recognise that argument.')
        print('Exiting.')
        sys.exit()

# Check that the script is being ran in the seng directory
if os.path.basename(os.path.normpath(os.getcwd())) != 'seng':
    print('Error: Script must be ran inside \'seng/\' directory.')
    print('Exiting.')
    sys.exit()

# Directories needed for specific, individual files
required_directories = [
    'server_specific',
    'server_specific/welcome_blocks',
    'private'
]

# Create the required directories
print('Creating required directories:')
for req_dir in required_directories:
    try:
        os.mkdir(req_dir)
        yes_no = 'no'  # Set to 'no' to ignore conditional below
    except FileExistsError:
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

# Copy files from template directory to the correct location
for root, dirs, files in os.walk('./config/template_files'):
    for name in files:
        # Get the file's path for the current file
        file_path = os.path.join(root, name)

        # Modify file path to model seng's filetree
        insert_path = file_path.replace('config/template_files/', '')

        # Check if file already exists in seng filetree
        if os.path.isfile(insert_path):
            # Ask user if they'd like to replace the file
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
                shutil.copyfile(file_path, insert_path)
        else:
            # File does not already exist - replace it
            shutil.copyfile(file_path, insert_path)
print('\nSuccess - templates file have been loaded in. Please now edit the '
      'template files within seng, with the correct details. You can run '
      'file_check.py to help ensure that things have been set-up correctly.')
