import sys
import os
import json
from pathlib import Path

# Check if user is requesting help on this script
if len(sys.argv) > 1:
    if sys.argv[1].lower() in ['help', 'h']:
        print(
            'This script is used to conduct multiple tests within the Seng '
            'directory, to try and help ensure that the necessary files exist '
            'and are set-up correctly. The script must be ran within the root '
            'directory of Seng, and the script will output the errors it '
            'encounters. It\'s recommended to run the load_data_pack.py '
            'script before running this script, if you have a data_pack, as '
            'loading the data pack\'s files will likely fix some errors '
            'you\'d encounter without loading the data pack.'
        )
        sys.exit()
    else:
        print('I didn\'t recognise that argument.')
        print('Exiting.')
        sys.exit()

test_dict = {}
# Print Error information overview
print('-'*42 + '\nERRORS: \n - Solving errors in order from top to bottom is '
      'recommended.\n - Not all errors need to be solved, but the more errors '
      'solved, the better Seng\'s functionality is likely to work.\n - Errors '
      'which are not vital to solve are labelled as \'Warning\'s.\n\n')


#####################
# General Path Test #
#####################
general_paths = [
    'private/priv_data.json',
    'private/key.txt',
    'private/priv_data.json',
    'server_specific/moderators.txt',
    'server_specific/channel_ids.json',
    'server_specific/welcome_blocks/',
    'server_specific/welcome_blocks/_block_queue'
]

# Test that the paths above exist
fails = 0
for some_path in general_paths:
    if not os.path.exists(some_path):
        fails += 1
        print('General Path Test Error: Failed to find path: ' + some_path)

max_passes = len(general_paths)
attained_passes = max_passes - fails
test_dict['General Path Test'] = (attained_passes, max_passes)


###################
# Crypto Key Test #
###################
key_paths = [
    'private/key.txt',
    'private/public_key.txt'
]

# Tests that the paths above exist
fails = 0
for key_path in key_paths:
    if not os.path.exists(key_path):
        fails += 1
        print('Crypto Key Test Warning: Failed to find: ' + key_path)

max_passes = len(key_paths)
attained_passes = max_passes - fails
test_dict['Crypto Key Test'] = (attained_passes, max_passes)


#########################
# channel_ids.json Test #
#########################
if not os.path.exists('server_specific/channel_ids.json'):
    pass  # Do nothing, as this is covered by General Path Test

# Keys to test for
expected_keys = [
    'GUILD',
    'MOD_COMMANDS',
    'WELCOME',
    'MEET_OUR_MEMBERS'
]

# Get the dictionary
fails = 0
try:
    with open('server_specific/channel_ids.json', 'r') as channel_ids_file:
        # Be wary of incorrectly formatted json files
        try:
            channel_dict = json.loads(channel_ids_file.read())
        except json.decoder.JSONDecodeError:
            print('channel_ids.json Test Error: Unable to load channel_ids.json')
            channel_dict = {}  # Empty dictionary for fails later
except FileNotFoundError:
    print('channel_ids.json Test Error: Unable to locate channel_ids.json')
    channel_dict = {}  # Empty dictionoary for fails later

# Test that the above keys exist in channel_ids.json
for key in expected_keys:
    if key not in channel_dict.keys():
        fails += 1
        print('channel_ids.json Test Error: Could not find the {} key within '
              'chanel_ids.json'.format(key))

max_passes = len(expected_keys)
attained_passes = max_passes - fails
test_dict['channel_ids.json Test'] = (attained_passes, max_passes)


##########################
# Default Template Test #
##########################
# Checks if user has changed template files from the default or not

# moderators.txt
fails = 0
if os.path.exists('server_specific/moderators.txt'):
    with open('server_specific/moderators.txt') as moderators_file:
        mod_list = moderators_file.readlines()
        if '<Moderator_ID_1>\n' in mod_list:
            print('Default Template Test Error: Possible template file '
                  'detected for server_specific/moderators.txt. Please amend '
                  'it with the correct data.')
            fails += 1
else:
    print('Default Template Test Error: Unable to locate '
          'server_specific/moderators.txt')
    fails += 1

# channel_ids.json
if os.path.exists('server_specific/channel_ids.json'):
    with open('server_specific/channel_ids.json') as moderators_file:
        if "<id>" in moderators_file.read():
            print('Default Template Test Error: Possible template file '
                  'detected for server_specific/channel_ids.json. Please '
                  'amend it with the correct data.')
            fails += 1
else:
    print('Default Template Test Error: Unable to locate '
          'server_specific/channel_ids.json')
    fails += 1

# private/priv_data.json
if os.path.exists('private/priv_data.json'):
    with open('private/priv_data.json') as private_data_file:
        if "<token>" in private_data_file.read():
            print('Default Template Test Error: Possible template file '
                  'detected for private/priv_data.json. Please '
                  'amend it with the correct data.')
            fails += 1
else:
    print('Default Template Test Error: Unable to locate '
          'private/priv_data.json')
    fails += 1

max_passes = 3  # Manually edit
attained_passes = max_passes - fails
test_dict['Default Template Test'] = (attained_passes, max_passes)


###########
# RESULTS #
###########
total_attained_passes = 0
total_max_passes = 0
print('\n'+ '-'*42 + '\nTEST RESULTS OVERVIEW\n' + '-'*42)

# Print out pass information for each test type
for test_type, pass_info in test_dict.items():
    print('Test Type: ' + test_type)
    print('\tPassed {} out of {} tests.\n'.format(str(pass_info[0]),
                                                  str(pass_info[1])))
    total_attained_passes += pass_info[0]
    total_max_passes += pass_info[1]

# Print overview for all tests
print('Total Tests: ')
print('\tPassed {} out of {} total tests.'.format(str(total_attained_passes),
                                                  str(total_max_passes)))
print('-'*42)
