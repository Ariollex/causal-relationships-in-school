import pandas
import numpy
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import os

import error
import calculations
import print_data
import graphs
from strings import print_on_language, set_language, set_variables

# Disable warnings
pandas.options.mode.chained_assignment = None

# Configuration
configuration = open("configuration", 'r').read().split('\n')
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
if len(errors) != 0:
    error.error('Incorrect parameter values:', 0)
    print(*['- ' + errors[i] for i in range(len(errors))], sep='\n')
    error.broken_configuration()

# Version
version = calculations.read_from_configuration(0)
prefix = calculations.read_from_configuration(1)
version = 'v' + version + '-' + prefix

# Language
language = calculations.read_from_configuration(2)
delayed_start = []
if not set_language(language):
    delayed_start.append('language')

# Dataset
file_loc = calculations.read_from_configuration(10)


def set_dataset_parameters(file_location):
    dataset = pandas.read_excel(file_location)
    dataset_name_columns = list(dataset)
    dataset.columns = range(dataset.columns.size)
    dataset.replace(numpy.nan, 0, inplace=True)
    return dataset, dataset_name_columns


data, name_columns = set_dataset_parameters(file_loc)

# Dataset settings
dataset_parameters = ['name', 'sex', 'parallel', 'letter', 'causes', 'time_causes', 'previous_causes']
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


def exit_button(column_btn, count_row, translated=True):
    if not translated:
        exit_btn = Button(button_frame, text='Exit', command=exit)
    else:
        exit_btn = Button(button_frame, text=print_on_language(1, 21), command=exit)
    exit_btn.grid(column=column_btn, row=count_row, padx=5, pady=5)


def change_configuration(option, line, argument):
    lines = open("configuration", 'r').readlines()
    lines[line] = option + " = '" + argument + "'\n"
    out = open("configuration", 'w')
    out.writelines(lines)
    out.close()


def change_language(back_btn=None):
    files = os.listdir('languages')
    clear_window()
    Label(window, text='Available languages:').grid(column=0, row=0)
    count_row = 1
    for i in range(len(files)):
        Button(window, text=files[i].replace('strings_', '').replace('.xlsx', ''),
               command=lambda j=i: change_language_process(files, j)).grid(column=0, row=count_row)
        count_row = count_row + 1
    Label(window, text='Please note that if the dataset and the program language are different, there may be errors.') \
        .grid(column=0, row=count_row + 1)
    column_btn = 0
    translated = False
    if back_btn:
        back_button(column_btn, count_row + 2)
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


def change_language_process(files, index_language):
    new_language = files[index_language].replace('strings_', '').replace('.xlsx', '')
    set_language(new_language)
    exit_screen(print_on_language(1, 14))


def exit_screen(message=None):
    if message is not None:
        clear_window(message)
    exit_button(0, 1)


def apply_dataset(changes):
    supported_parameters = calculations.get_supported_parameters()
    for i in range(len(dataset_parameters)):
        if not changes[i].get().isdigit() or not 0 < int(changes[i].get()) < len(dataset_parameters) + 1:
            messagebox.showerror("Error", "Incorrect column values")
            return
        else:
            change_configuration(supported_parameters[3 + i], indexes[3 + i], changes[i].get())
    if len(calculations.check_configuration(only_dataset=True)) != 0:
        messagebox.showerror("Error", "Incorrect column values or incorrect dataset")
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
    mode_selection()


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
            messagebox.showerror("Error", "Broken dataset")
            return
        data, name_columns = set_dataset_parameters(new_file_loc)
        change_configuration('dataset_path', indexes[10], new_file_loc)
        file_loc = new_file_loc
    window.winfo_children()[-2].destroy()
    Label(window, text='Current dataset: ' + file_loc).grid(column=0, row=count_row + 1)
    Button(window, text='Change', command=lambda: change_dataset(count_row)).grid(column=1, row=count_row + 1)


def read_value(entries):
    return [e.get() for e in entries]


def settings_dataset():
    clear_window()
    Label(window, text='Column numbers in dataset:').grid(column=0, row=0)
    count_row = 1
    entries = []
    for i in range(len(dataset_parameters)):
        v = StringVar(root, value=str(configuration[indexes[3 + i]][str(configuration[indexes[3 + i]]).find("'") + 1:
                                                                    str(configuration[indexes[3 + i]]).rfind("'")]))
        Label(window, text=dataset_parameters[i]).grid(column=0, row=count_row, sticky=W)
        value_entry = Entry(window, textvariable=v)
        entries.append(value_entry)
        value_entry.grid(column=0, row=count_row)
        count_row = count_row + 1
    Label(window, text='Current dataset: ' + file_loc).grid(column=0, row=count_row + 1)
    Button(window, text='Change', command=lambda: change_dataset(count_row)).grid(column=1, row=count_row + 1)
    back_button(0, count_row + 2, back_command=lambda: apply_dataset(entries))
    exit_button(1, count_row + 2)


def settings():
    clear_window()
    Button(window, text='Dataset settings', command=settings_dataset).grid(column=0, row=0)
    Button(window, text=print_on_language(1, 20), command=lambda: change_language(True)).grid(column=0, row=1)
    back_button(0, 1)
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
    back_button(0, 2)
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


root = Tk()
root.minsize(400, 150)
window = Frame(root)
window.pack(expand=True)
button_frame = Frame(root)
button_frame.pack()

if len(delayed_start) != 0:
    root.title('Causal relationships in school ' + version)
    for i in range(len(delayed_start)):
        if i == len(delayed_start):
            break
        if delayed_start[i] == 'language':
            change_language()
            delayed_start.remove('language')
else:
    # Modes
    modes = [print_on_language(1, 8), print_on_language(1, 9)]

    # Available graphs
    available_graphs = [print_on_language(1, 5), print_on_language(1, 18), print_on_language(1, 19)]

    # Creating a list of incidents
    list_incidents = calculations.make_list_incidents(data, name, sex, parallel, letter, causes,
                                                      time_causes, previous_causes)

    root.title(print_on_language(1, 15) + ' ' + version)
    mode_selection()

root.mainloop()
