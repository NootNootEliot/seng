import os
from pathlib import Path

paths = [
    'private/priv_data.json',
    'server_specific/moderators.txt',
    'server_specific/channel_ids.json'
]

test_fails = {
    'General Path Test': 0,
}

test_length = {
    'General Path Test': len(paths),
}

# Test General Paths
for some_path in paths:
    if not os.path.exists(some_path):
        test_fails['General Path Test'] += 1
        print("ERROR: Failed to find path: " + some_path)


# Print out individual test group results
total_successes = 0
total_tests = 0
print('\nTEST RESULTS\n' + '-'*20)
for test_type in test_fails:
    print(test_type)
    successes = test_length[test_type] - test_fails[test_type]
    print(
        '\tPassed ' + str(successes) + ''
        ' out of ' + str(test_length[test_type]) + ' tests.\n'
    )
    total_successes += successes
    total_tests += test_length[test_type] 

# Print results for all tests.
print('Total Tests: ')
print(
    '\tPassed ' + str(total_successes) + ' out of ' + str(total_tests) + ''
    ' tests.\n'
)
if total_successes != total_tests:
    print('\tHint: Are you running this python script within config?')
