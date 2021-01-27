import os
import json
from pathlib import Path

test_dict = {}
print('-'*10 + '\nERRORS\n' + '-'*10)
#####################
# General Path Test #
#####################
paths = [
    'private/priv_data.json',
    'server_specific/moderators.txt',
    'server_specific/channel_ids.json',
    'server_specific/welcome_blocks/',
    'server_specific/welcome_blocks/_block_queue'
]

# Test that the paths above exist
fails = 0
for some_path in paths:
    if not os.path.exists(some_path):
        fails += 1
        print('General Path Test Error: Failed to find path: ' + some_path)

max_passes = len(paths)
attained_passes = max_passes - fails
test_dict['General Path Test'] = (attained_passes, max_passes)


#########################
# channel_ids.json Test #
#########################
if not os.path.exists('server_specific/channel_ids.json'):
    pass  # Do nothing, as this is covered by General Path Test

# Get the dictionary
with open('server_specific/channel_ids.json', 'r') as channel_ids_file:
    channel_dict = json.loads(channel_ids_file.read())

# Keys to test for
expected_keys = [
    'GUILD',
    'MOD_COMMANDS',
    'WELCOME',
    'MEET_OUR_MEMBERS'
]

# Test that the above keys exist in channel_ids.json
fails = 0
for key in expected_keys:
    if key not in channel_dict.keys():
        fails += 1
        print('channel_ids.json Test Error: Could not find the {} key within '
              'chanel_ids.json'.format(key))

max_passes = len(expected_keys)
attained_passes = max_passes - fails
test_dict['channel_ids.json Test'] = (attained_passes, max_passes)


###########
# RESULTS #
###########
total_attained_passes = 0
total_max_passes = 0
print('\n'+ '-'*25 + '\nTEST RESULTS OVERVIEW\n' + '-'*25)

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
