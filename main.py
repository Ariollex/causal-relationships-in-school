import pandas
import numpy
import input_data
import calculations
import print_data
import graphs
from strings import print_on_language, set_language, set_variables

# Disable warnings
pandas.options.mode.chained_assignment = None

# Configuration
configuration = open("configuration", 'r').read().split('\n')
calculations.set_variables(configuration)
indexes = calculations.check_configuration()
set_variables(configuration, indexes)
calculations.check_parameters()

# Version
version = calculations.read_from_configuration(0)
prefix = calculations.read_from_configuration(1)
version = 'v' + version + '-' + prefix

# Language
language = calculations.read_from_configuration(2)
set_language(language)
print(print_on_language(1, 15), version, '\n')

# Dataset
file_loc = calculations.read_from_configuration(10)
data = pandas.read_excel(file_loc)
name_columns = list(data)
data.columns = range(data.columns.size)
data.replace(numpy.nan, 0, inplace=True)

# Dataset settings
name = data[int(calculations.read_from_configuration(3)) - 1]
sex = data[int(calculations.read_from_configuration(4)) - 1]
parallel = data[int(calculations.read_from_configuration(5)) - 1]
letter = data[int(calculations.read_from_configuration(6)) - 1]
causes = data[int(calculations.read_from_configuration(7)) - 1]
time_causes = data[int(calculations.read_from_configuration(8)) - 1]
previous_causes = data[int(calculations.read_from_configuration(9)) - 1]

# Convert time
for i in range(data.shape[0]):
    if time_causes[i] != 0:
        time_causes[i] = int(str(time_causes[i]).replace(':', ''))
    else:
        time_causes[i] = int(time_causes[i])

# Available graphs
available_graphs = [print_on_language(1, 5), print_on_language(1, 18), print_on_language(1, 19)]

# Program operation mode selection
functions = [print_on_language(1, 8), print_on_language(1, 9)]
print(print_on_language(1, 6) + ':')
print_data.print_selection_list(functions)
print('L)', print_on_language(1, 20))
print('E)', print_on_language(1, 21))
print(print_on_language(1, 7) + ':', end=' ')
choice_mode = input_data.make_user_choice(functions)
# Creating a list of incidents
list_incidents = calculations.make_list_incidents(data, name, sex, parallel, letter, causes,
                                                  time_causes, previous_causes)

if choice_mode == 0:
    info = []

    print_data.print_list_incidents(list_incidents)
    # Incident selection
    user_selection = input_data.make_user_choice(list_incidents)

    if list_incidents[user_selection][1] == print_on_language(1, 4) or (print_on_language(3, 2) == 0):
        print(print_on_language(1, 2), ' ', user_selection + 1, '. ' + print_on_language(2, 2) + ': ',
              list_incidents[user_selection][0], sep='')
    else:
        print(print_on_language(1, 2), ' ', user_selection + 1, '. ' + print_on_language(3, 2) + ': ',
              list_incidents[user_selection][0], sep='')

    # Calculations: search for matching information
    calculations.intersection_of_classes(list_incidents, user_selection, info, 0)
    calculations.intersection_of_time(list_incidents, user_selection, info, 0)

    # Calculations: conclusions
    print(calculations.conclusions(list_incidents, user_selection, info))

elif choice_mode == 1:
    print(print_on_language(1, 10) + ':')
    print_data.print_selection_list(available_graphs)
    print(print_on_language(1, 11) + ':', end=' ')
    # Graph selection
    choice_graph = input_data.make_user_choice(available_graphs)
    if choice_graph == 0:
        graphs.graph_1(data, causes, list_incidents)
    elif choice_graph == 1:
        graphs.graph_2(data, list_incidents, parallel)
    elif choice_graph == 2:
        graphs.graph_3(data, name_columns)
