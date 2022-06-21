## 
import workspace_class as wc
import sys

def test_error_handling(test_function, inputs):
    """
    Test how test_function reacts to error conditions in the input
    """
    assert isinstance(test_function, function)
    try:
        w = wc.Workspace("/home/james/test_dir", "test_dir")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # Test 1.0 - Set all members using lists
    keys = ['title', 'number', 'commands', 'layout']
    values = ['Test Workspace', '1', 'test_0', 'layouts/test_layout.json']
    test_workspace_1_0 = wc.workspace(keys, values)

    attributes = test_workspace_1_0.get_attributes()
    print(attributes)

    # Test 1.1 - Set members using set_attributes
    test_workspace_1_1 = wc.workspace()

    attributes_1_1 = test_workspace_1_1.get_attributes()
    print(attributes)
    # Test add_attribute method, for every attribute 1
    keys = ['title', 'number', 'commands', 'layout']
    values = ['Test Workspace 1.1', '1', 'test_0', 'layouts/test_layout.json']

    for key, value in zip(keys, values):
        test_workspace_1_1.set_attribute(key, value)

    attributes_1_1 = test_workspace_1_1.get_attributes()
    print(attributes)

    # Test adding extra commands using string and list of strings
    command = 'test_1'
    test_workspace.set_attribute('commands', command)
    commands = ['test_2.1', 'test_2.2']
    test_workspace.set_attribute('commands', commands)

    attributes = test_workspace.get_attributes()
    print(attributes)


    # Tests that should fail
    ## Fail test1
    fail_test = wc.workspace()
    failures = []

    try:
        fail_test.set_attribute('', 'Test Workspace')
    except Exception as e:
        print("\tThe following error was raised: " + str(e))

    print("Testing broken titles")
    broken_titles = ['', 0, ['valid_name']]
    for broken_title in broken_titles:
        try:
            fail_test.set_attribute('title', broken_title)
            print(f"\tTest failed: {broken_title} should not be a valid title")
        except Exception as e:
            print("\tThe following error was raised: " + str(e))

    print("Testing broken numbers")
    broken_numbers = [0, '', 1.1, '1 text'] 
    for broken_number in broken_numbers:
        try:
            fail_test.set_attribute('number', broken_number)
            print(f"\tTest failed: {broken_number} should not be a valid number")
        except Exception as e:
            print("\tThe following error was raised: " + str(e))

    print("Testing broken commands")
    broken_commands = ['', [], 0, [0, 0], (0, 0), ['0', 0]]
    for broken_command in broken_commands:
        try:
            fail_test.set_attribute('commands', broken_command)
            print(f"\tTest failed: {broken_command} should not be a valid command")
        except Exception as e:
            print("\tThe following error was raised: " + str(e))

    broken_layouts = ['', 'layouts/does_not_exist.json', 0,
                      'test_workspace_class']

    print("Testing broken layouts")
    for broken_layout in broken_layouts:
        try:
            fail_test.set_attribute('layout', broken_layout)
            print(f"\tTest failed: {broken_layout} should not be a valid layout")
        except Exception as e:
            print("\tThe following error was raised: " + str(e))





##
