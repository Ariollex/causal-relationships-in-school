from sys import exit
import pandas
import numpy
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import webbrowser
import requests
import os

import error
import calculations
import print_data
import graphs
from strings import set_language, set_variables, print_on_language

# Disable warnings
pandas.options.mode.chained_assignment = None

# Delayed start
delayed_start = []
modes, available_graphs, list_incidents, parameters_dataset, parameters_dataset_translated = [], [], [], [], []

# Configuration
if not os.path.exists('configuration'):
    url_configuration = 'https://raw.githubusercontent.com/Ariollex/causal-relationships-in-school/main/configuration'
    messagebox.showwarning('Warning!', 'The configuration file was not found. Downloading from ' + url_configuration)
    response = requests.get(url_configuration)
    with open('configuration', "wb") as file:
        file.write(response.content)

configuration = open('configuration', 'r').read().split('\n')
calculations.set_variables(configuration)
indexes, warnings, missing_parameters = calculations.check_configuration()
if len(warnings) != 0:
    [error.warning(warnings[i]) for i in range(len(warnings))]
if len(missing_parameters) != 0:
    error.error('These required parameters are not defined:', 0)
    print(*['- ' + missing_parameters[i] for i in range(len(missing_parameters))], sep='\n')
    error.broken_configuration()
set_variables(configuration, indexes)
errors = calculations.check_parameters()
if len(errors) > 0:
    [error.warning(errors[i]) for i in range(len(errors))]
    delayed_start.append('invalid_parameters_values')

# Version
version = calculations.read_from_configuration(0)
prefix = calculations.read_from_configuration(1)
version = 'v' + version + '-' + prefix

# Language
if not os.path.exists('languages') or not os.listdir('languages'):
    messagebox.showerror('Error', 'Missing language files')
    exit()

language = calculations.read_from_configuration(2)
if not set_language(language):
    delayed_start.insert(0, 'invalid_language')
    language_status = 'undefined'
else:
    language_status = 'active'

# Dataset
file_loc = calculations.read_from_configuration(10)
if not os.path.exists(file_loc):
    delayed_start.append('invalid_path_dataset')
    file_loc = None


def set_dataset_parameters(file_location):
    dataset = pandas.read_excel(file_location)
    dataset_name_columns = list(dataset)
    dataset.columns = range(dataset.columns.size)
    dataset.replace(numpy.nan, 0, inplace=True)
    return dataset, dataset_name_columns


if 'invalid_path_dataset' not in delayed_start:
    data, name_columns = set_dataset_parameters(file_loc)
else:
    data = None

# Dataset settings
if 'invalid_parameters_values' not in delayed_start and data is not None:
    name = data[int(calculations.read_from_configuration(3)) - 1]
    sex = data[int(calculations.read_from_configuration(4)) - 1]
    parallel = data[int(calculations.read_from_configuration(5)) - 1]
    letter = data[int(calculations.read_from_configuration(6)) - 1]
    causes = data[int(calculations.read_from_configuration(7)) - 1]
    time_causes = data[int(calculations.read_from_configuration(8)) - 1]
    previous_causes = data[int(calculations.read_from_configuration(9)) - 1]

    # Convert time
    for i in range(data.shape[0]):
        time_causes[i] = int(str(time_causes[i]).replace(':', '')) if time_causes[i] != 0 else int(time_causes[i])


def back_button(column_btn, count_row, translated=True, back_command=lambda: mode_selection()):
    if not translated:
        exit_btn = Button(button_frame, text='Back', command=back_command)
    else:
        exit_btn = Button(button_frame, text=print_on_language(1, 30), command=back_command)
    exit_btn.grid(column=column_btn, row=count_row, padx=5, pady=5)


def exit_button(column_btn, count_row, translated=True, exit_command=lambda: exit()):
    if not translated:
        exit_btn = Button(button_frame, text='Exit', command=exit_command)
    else:
        exit_btn = Button(button_frame, text=print_on_language(1, 21), command=exit_command)
    exit_btn.grid(column=column_btn, row=count_row, padx=5, pady=5)


def change_configuration(option, line, argument):
    lines = open("configuration", 'r').readlines()
    lines[line] = option + " = '" + argument + "'\n"
    out = open("configuration", 'w')
    out.writelines(lines)
    out.close()


def change_language(back_btn=None, delayed_start_var=False):
    files = os.listdir('languages')
    clear_window()
    Label(window, text='Available languages:').grid(column=0, row=0)
    count_row = 1
    for i in range(len(files)):
        Button(window, text=files[i].replace('strings_', '').replace('.xlsx', ''),
               command=lambda j=i: change_language_process(files, j, delayed_start_var)).grid(column=0, row=count_row)
        count_row = count_row + 1
    Label(window, text='Please note that if the dataset and the program language are different, there may be errors.') \
        .grid(column=0, row=count_row + 1)
    column_btn = 0
    translated = False
    if back_btn:
        back_button(column_btn, count_row + 2, back_command=lambda: settings())
        column_btn = column_btn + 1
        translated = True
    exit_button(column_btn, count_row + 2, translated)


def clear_window(message=None):
    for widget in button_frame.winfo_children():
        widget.destroy()
    for widget in window.winfo_children():
        widget.destroy()
    if message is not None:
        Label(window, text=message, fg='red').grid(column=0, row=0)


def change_language_process(files, index_language, delayed_start_var=False):
    global language_status, delayed_start
    new_language = files[index_language].replace('strings_', '').replace('.xlsx', '')
    set_language(new_language)
    language_status = 'active'
    if delayed_start_var:
        delayed_start.remove('invalid_language')
    start_variables()


def apply_dataset(changes, delayed_start_var=False, apply_exit=None):
    if file_loc is None:
        messagebox.showerror(print_on_language(1, 41), print_on_language(1, 55))
        return
    supported_parameters = calculations.get_supported_parameters()
    for i in range(len(parameters_dataset)):
        if not changes[i].get().isdigit() or not 0 < int(changes[i].get()) < len(parameters_dataset) + 1:
            messagebox.showerror(print_on_language(1, 41), print_on_language(1, 53))
            return
        else:
            change_configuration(supported_parameters[3 + i], indexes[3 + i], changes[i].get())
    if len(calculations.check_configuration(only_dataset=True)) != 0:
        messagebox.showerror(print_on_language(1, 41), print_on_language(1, 54))
        return
    else:
        global list_incidents, name, sex, parallel, letter, causes, time_causes, previous_causes, configuration
        configuration = open("configuration", 'r').read().split('\n')
        name = data[int(configuration[indexes[3]][str(configuration[indexes[3]]).find("'") + 1:
                                                  str(configuration[indexes[3]]).rfind("'")]) - 1]
        sex = data[int(configuration[indexes[4]][str(configuration[indexes[4]]).find("'") + 1:
                                                 str(configuration[indexes[4]]).rfind("'")]) - 1]
        parallel = data[int(configuration[indexes[5]][str(configuration[indexes[5]]).find("'") + 1:
                                                      str(configuration[indexes[5]]).rfind("'")]) - 1]
        letter = data[int(configuration[indexes[6]][str(configuration[indexes[6]]).find("'") + 1:
                                                    str(configuration[indexes[6]]).rfind("'")]) - 1]
        causes = data[int(configuration[indexes[7]][str(configuration[indexes[7]]).find("'") + 1:
                                                    str(configuration[indexes[7]]).rfind("'")]) - 1]
        time_causes = data[int(configuration[indexes[8]][str(configuration[indexes[8]]).find("'") + 1:
                                                         str(configuration[indexes[8]]).rfind("'")]) - 1]
        previous_causes = data[int(configuration[indexes[9]][str(configuration[indexes[9]]).find("'") + 1:
                                                             str(configuration[indexes[9]]).rfind("'")]) - 1]
        # Convert time
        for i in range(data.shape[0]):
            time_causes[i] = int(str(time_causes[i]).replace(':', '')) if time_causes[i] != 0 else int(time_causes[i])
        # Re-creating a list of incidents
        list_incidents = calculations.make_list_incidents(data, name, sex, parallel, letter, causes,
                                                          time_causes, previous_causes)
    if apply_exit:
        exit()
    elif not delayed_start_var:
        settings()
    else:
        start_variables()
        messagebox.showinfo(title=print_on_language(1, 51), message=print_on_language(1, 52))
        fix_configuration()


def check_dataset(new_file_loc):
    try:
        pandas.read_excel(new_file_loc)
    except ValueError:
        return False
    if len(list(pandas.read_excel(new_file_loc))) < 7:
        return False
    return True


def change_dataset(count_row):
    global data, name_columns, file_loc
    new_file_loc = askopenfilename()
    if new_file_loc != '':
        if not check_dataset(new_file_loc):
            messagebox.showerror(print_on_language(1, 41), print_on_language(1, 42))
            return
        data, name_columns = set_dataset_parameters(new_file_loc)
        change_configuration('dataset_path', indexes[10], new_file_loc)
        file_loc = new_file_loc
    window.winfo_children()[-2].destroy()
    Label(window, text=print_on_language(1, 34) + ': ' + str(file_loc)).grid(column=0, row=count_row + 1)
    Button(window, text=print_on_language(1, 35), command=lambda: change_dataset(count_row)) \
        .grid(column=1, row=count_row + 1)


def settings_dataset(buttons=True):
    global parameters_dataset
    clear_window()
    Label(window, text=print_on_language(1, 33)).grid(column=0, row=0)
    count_row = 1
    parameters_dataset = calculations.get_parameters_dataset()
    entries = []
    for i in range(len(parameters_dataset)):
        v = StringVar(root, value=str(configuration[indexes[3 + i]][str(configuration[indexes[3 + i]]).find("'") + 1:
                                                                    str(configuration[indexes[3 + i]]).rfind("'")]))
        Label(window, text=parameters_dataset_translated[i]).grid(column=0, row=count_row, sticky=W)
        value_entry = Entry(window, textvariable=v)
        entries.append(value_entry)
        value_entry.grid(column=1, row=count_row)
        count_row = count_row + 1
    Label(window, text=print_on_language(1, 34) + ': ' + str(file_loc)).grid(column=0, row=count_row + 1)
    Button(window, text=print_on_language(1, 35), command=lambda: change_dataset(count_row)) \
        .grid(column=1, row=count_row + 1)
    if not buttons:
        Button(button_frame, text=print_on_language(1, 50),
               command=lambda: apply_dataset(entries, delayed_start_var=True)).grid(column=0, row=count_row + 2)
    else:
        back_button(0, count_row + 2, back_command=lambda: apply_dataset(entries))
    exit_button(1, count_row + 2, exit_command=lambda: apply_dataset(entries, apply_exit=True))


def settings():
    clear_window()
    Button(window, text=print_on_language(1, 32), command=settings_dataset).grid(column=0, row=0)
    Button(window, text=print_on_language(1, 20), command=lambda: change_language(True)).grid(column=0, row=1)
    Button(window, text=print_on_language(1, 43), command=about_program).grid(column=0, row=2)
    back_button(0, 1)
    exit_button(1, 1)


def open_source_code():
    webbrowser.open_new('https://github.com/Ariollex/causal-relationships-in-school')


def about_program():
    clear_window()
    Label(window, text=print_on_language(1, 15)).grid(column=0, row=0)
    Label(window, text=print_on_language(1, 44) + ': ' + version).grid(column=0, row=1)
    Label(window, text=print_on_language(1, 45) + ': ' + 'Artem Agapkin').grid(column=0, row=2)
    Button(window, text=print_on_language(1, 46) + ': ' + 'https://github.com/Ariollex/causal-relationships-in-school',
           command=open_source_code).grid(column=0, row=3)
    back_button(0, 1, back_command=lambda: settings())
    exit_button(1, 1)


def mode_selection():
    clear_window()
    Label(window, text=print_on_language(1, 6) + '. ' + print_on_language(1, 7) + ':').grid(column=0, row=0)

    # Program operation mode selection
    Button(window, text=modes[0], command=mode_causal_relationship).grid(column=0, row=1)
    Button(window, text=modes[1], command=mode_graph).grid(column=0, row=2)
    Button(window, text=print_on_language(1, 31), command=settings).grid(column=0, row=3)
    exit_button(0, 4)


def mode_causal_relationship():
    clear_window()
    info = []
    list_incidents_numbered = print_data.print_list_incidents(list_incidents)
    Label(window, text=print_on_language(1, 0)).grid(column=0, row=0)
    count_row = len(list_incidents_numbered)
    for i in range(count_row):
        Button(window, text=list_incidents_numbered[i], command=lambda j=i: mode_causal_relationship_process(j, info)) \
            .grid(column=0, row=i + 1, sticky=W)
    back_button(0, count_row + 1)
    exit_button(1, count_row + 1)


def mode_causal_relationship_process(user_selection, info):
    clear_window()
    if list_incidents[user_selection][1] == print_on_language(1, 4) or (print_on_language(3, 2) == 0):
        user_choice_text = print_on_language(1, 2) + ' ' + str(user_selection + 1) + '. ' + print_on_language(2, 2) + \
                           ': ' + str(list_incidents[user_selection][0])
    else:
        user_choice_text = print_on_language(1, 2) + ' ' + str(user_selection + 1) + '. ' + print_on_language(3, 2) + \
                           ': ' + str(list_incidents[user_selection][0])
    Label(window, text=user_choice_text).grid(column=0, row=0, sticky=W)

    # Calculations: search for matching information
    calculations.intersection_of_classes(list_incidents, user_selection, info, 0)
    calculations.intersection_of_time(list_incidents, user_selection, info, 0)

    # Calculations: conclusions
    Label(window, text=calculations.conclusions(list_incidents, user_selection, info)).grid(column=0, row=1)
    back_button(0, 2, back_command=lambda: mode_causal_relationship())
    exit_button(1, 2)


def mode_graph():
    clear_window()
    list_graphs_numbered = print_data.print_selection_list(available_graphs)
    Label(window, text=print_on_language(1, 10) + ':')
    count_row = len(list_graphs_numbered)
    for i in range(count_row):
        Button(window, text=list_graphs_numbered[i], command=lambda j=i: mode_graph_process(j)) \
            .grid(column=0, row=i + 1, sticky=W)
    back_button(0, count_row + 1)
    exit_button(1, count_row + 1)


def mode_graph_process(choice_graph):
    graphs.set_variables(list_incidents, causes, parallel, name_columns)
    graphs.graph_selection(choice_graph, data)
    count_row = len(available_graphs)
    back_button(0, count_row + 1)
    exit_button(1, count_row + 1)


def start_variables():
    global modes, available_graphs, parameters_dataset_translated, list_incidents
    # Modes
    modes = [print_on_language(1, 8), print_on_language(1, 9)]

    # Available graphs
    available_graphs = [print_on_language(1, 5), print_on_language(1, 18), print_on_language(1, 19)]

    # Translated dataset parameters
    parameters_dataset_translated = [print_on_language(1, 36), print_on_language(1, 37), print_on_language(1, 17),
                                     print_on_language(1, 38), print_on_language(1, 12), print_on_language(1, 39),
                                     print_on_language(1, 40)]

    root.title(print_on_language(1, 15) + ', ' + version)

    if configuration_status == 'normal':
        # Creating a list of incidents
        list_incidents = calculations.make_list_incidents(data, name, sex, parallel, letter, causes,
                                                          time_causes, previous_causes)
        mode_selection()
    else:
        fix_configuration()


def fix_configuration():
    global list_incidents, language_status, configuration_status
    # Language
    if 'invalid_language' in delayed_start:
        root.update()
        messagebox.showwarning('Warning', 'The language is not defined. Please select a language.')
        change_language(delayed_start_var=True)
    elif language_status != 'active':
        language_status = 'active'
        start_variables()
    # Invalid path dataset
    elif 'invalid_path_dataset' in delayed_start:
        root.update()
        messagebox.showwarning(print_on_language(1, 47), print_on_language(1, 48))
        settings_dataset(buttons=False)
        delayed_start.remove('invalid_path_dataset')
        delayed_start.remove('invalid_parameters_values')
    # Invalid parameters_values
    elif 'invalid_parameters_values' in delayed_start:
        root.update()
        messagebox.showwarning(print_on_language(1, 47), print_on_language(1, 49))
        settings_dataset(buttons=False)
        delayed_start.remove('invalid_parameters_values')
    # check for normal status
    elif len(delayed_start) == 0:
        # Creating a list of incidents
        list_incidents = calculations.make_list_incidents(data, name, sex, parallel, letter, causes,
                                                          time_causes, previous_causes)
        configuration_status = 'normal'
        mode_selection()


root = Tk()
root.minsize(500, 150)
window = Frame(root)
window.pack(expand=True)
button_frame = Frame(root)
button_frame.pack()

if len(delayed_start) != 0:
    root.title('Causal relationships in school, ' + version)
    configuration_status = 'break'
    language_status = 'break'
    fix_configuration()
else:
    configuration_status = 'normal'
    start_variables()
root.mainloop()
