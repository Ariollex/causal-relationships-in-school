from sys import exit
import pandas
import numpy
import platform
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import webbrowser
import requests
import random
import zipfile
import json
import os

import error
import debug
import calculations
import print_data
import charts
from strings import set_language, set_variables, print_on_language

# Version
version = '0.3'
prefix = 'alpha'
is_debug = True
if prefix == '':
    version = 'v' + version
else:
    version = 'v' + version + '-' + prefix + ('-debug' if is_debug else '')

# Disable warnings
pandas.options.mode.chained_assignment = None

# Delayed start
delayed_start = []
modes, available_charts, list_incidents, parameters_dataset, parameters_dataset_translated = [], [], [], [], []

if is_debug:
    print(debug.i(), 'Starting... \n' + debug.i(), 'Version:', version, 'with debug.')

# Configuration
if not os.path.exists(os.getcwd() + '/configuration'):
    if prefix == '':
        url_configuration = \
            'https://raw.githubusercontent.com/Ariollex/causal-relationships-in-school/main/configuration'
    else:
        url_configuration = \
            'https://raw.githubusercontent.com/Ariollex/causal-relationships-in-school/dev/configuration'
    if is_debug:
        print(debug.w(), 'Missing configuration file! Trying to get a file from', url_configuration)
    messagebox.showwarning('Warning!', 'The configuration file was not found.\nDownloading from ' + url_configuration)
    response = requests.get(url_configuration, timeout=None)
    with open(os.getcwd() + '/configuration', "wb") as file:
        file.write(response.content)
    if is_debug:
        print(debug.s(), 'Configuration has been successfully restored.')

if is_debug:
    print(debug.i(), 'Opening configuration...')
configuration = open(os.getcwd() + '/configuration', 'r').read().split('\n')
calculations.set_variables(configuration)
indexes, warnings, missing_parameters = calculations.check_configuration()
if len(warnings) != 0:
    if is_debug:
        [debug.w() + error.warning(warnings[i]) for i in range(len(warnings))]
if len(missing_parameters) != 0:
    error.error('These required parameters are not defined:', 0)
    print(*['- ' + missing_parameters[i] for i in range(len(missing_parameters))], sep='\n')
    error.broken_configuration()
set_variables(configuration, indexes)


def update_configuration():
    global configuration
    configuration = open(os.getcwd() + '/configuration', 'r').read().split('\n')
    calculations.set_variables(configuration)


def change_configuration(option, line, argument):
    lines = open("configuration", 'r').readlines()
    lines[line] = option + " = '" + argument + "'\n"
    try:
        out = open("configuration", 'w')
        out.writelines(lines)
        out.close()
    except PermissionError:
        messagebox.showwarning(print_on_language(1, 41), print_on_language(1, 74))


def reset_variables(resets_array):
    if 'num_clusters' in resets_array:
        if calculations.read_from_configuration(11).isdigit():
            num = int(calculations.read_from_configuration(11))
            if num < 2:
                num = 2
            else:
                num = 15
        else:
            num = 2
        change_configuration('num_clusters', indexes[11], str(num))
    update_configuration()


errors, resets = calculations.check_parameters()
if len(errors) > 0:
    if is_debug:
        [str(error.warning(errors[i])) for i in range(len(errors))]
    delayed_start.append('invalid_parameters_values')
if len(resets) > 0:
    if is_debug:
        [error.warning('Resetting ' + str(resets[i]) + ' value!') for i in range(len(resets))]
    reset_variables(resets)

# Language
if not os.path.exists(os.getcwd() + '/languages') or not os.listdir(os.getcwd() + '/languages'):
    global language
    if prefix == '':
        url_languages = \
            'https://raw.githubusercontent.com/Ariollex/causal-relationships-in-school/main/languages/languages.zip'
    else:
        url_languages = \
            'https://raw.githubusercontent.com/Ariollex/causal-relationships-in-school/dev/languages/languages.zip'
    if is_debug:
        print(debug.w(), 'Missing language file! Trying to get a file from', url_languages)
    messagebox.showwarning('Warning!', 'The language files was not found.\nDownloading from ' + url_languages)
    response = requests.get(url_languages, timeout=None)
    with open(os.getcwd() + '/languages-' + version, "wb") as file:
        file.write(response.content)
    archive = os.getcwd() + '/languages-' + version
    with zipfile.ZipFile(archive, 'r') as zip_file:
        zip_file.extractall('languages')
    os.remove(archive)
    set_language(str(None))
    calculations.set_variables(open(os.getcwd() + '/configuration', 'r').read().split('\n'))
    if is_debug:
        print(debug.s(), 'Languages has been successfully restored.')

language = calculations.read_from_configuration(0)
if not set_language(language):
    if is_debug:
        print(debug.w(), 'Incorrect language is selected! Trying to give a choice later')
    delayed_start.append('invalid_language')
    language_status = 'undefined'
else:
    language_status = 'active'
    if is_debug:
        print(debug.i(), 'Language successfully applied')

# Dataset
file_loc = calculations.read_from_configuration(8)
if not os.path.exists(file_loc):
    delayed_start.append('invalid_path_dataset')
    file_loc = None

if is_debug:
    if len(delayed_start) != 0:
        print(debug.w(), 'Delayed start is enabled!')
    else:
        print(debug.i(), 'Data from configuration has been successfully applied')


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


def set_dataset_columns():
    global name, sex, parallel, letter, causes, time_causes, previous_causes
    name = data[int(calculations.read_from_configuration(1)) - 1]
    sex = data[int(calculations.read_from_configuration(2)) - 1]
    parallel = data[int(calculations.read_from_configuration(3)) - 1]
    letter = data[int(calculations.read_from_configuration(4)) - 1]
    causes = data[int(calculations.read_from_configuration(5)) - 1]
    time_causes = data[int(calculations.read_from_configuration(6)) - 1]
    previous_causes = data[int(calculations.read_from_configuration(7)) - 1]


name, sex, parallel, letter, causes, time_causes, previous_causes = \
    pandas.Index([]), pandas.Index([]), pandas.Index([]), pandas.Index([]), pandas.Index([]), pandas.Index([]), \
    pandas.Index([])

# Dataset settings
if 'invalid_parameters_values' not in delayed_start and data is not None:
    set_dataset_columns()
    # Convert time
    for i in range(data.shape[0]):
        if str(time_causes[i]).replace(':', '').isdigit():
            if time_causes[i] != 0:
                time_causes[i] = int(str(time_causes[i]).replace(':', ''))
                if len(str(time_causes[i])) < 6:
                    time_causes[i] = str(0) + str(time_causes[i])
            else:
                time_causes[i] = int(time_causes[i])


def apply_constants(open_main_menu=True):
    global modes, available_charts, parameters_dataset_translated, list_incidents
    # Modes
    modes = [print_on_language(1, 8), print_on_language(1, 9)]

    # Available graphs
    available_charts = [print_on_language(1, 5), print_on_language(1, 18), print_on_language(1, 19),
                        print_on_language(1, 56)]

    # Translated dataset parameters
    parameters_dataset_translated = [print_on_language(1, 36), print_on_language(1, 37), print_on_language(1, 17),
                                     print_on_language(1, 38), print_on_language(1, 12), print_on_language(1, 39),
                                     print_on_language(1, 40)]

    root.title(print_on_language(1, 15) + ', ' + version)

    if configuration_status == 'normal':
        # Creating a list of incidents
        list_incidents = calculations.make_list_incidents(data, name, sex, parallel, letter, causes,
                                                          time_causes, previous_causes)
        if open_main_menu:
            menu_main()
        else:
            menu_language(back_btn=True)
    else:
        fix_configuration()


def open_link(link):
    if is_debug:
        print(debug.i(), 'Opening link', link)
    webbrowser.open_new(link)


def get_int(text):
    return int(''.join([s for s in text.split() if s.isdigit()]))


def fix_configuration():
    global list_incidents, language_status, configuration_status
    # Language
    if 'invalid_language' in delayed_start:
        messagebox.showwarning('Warning', 'The language is not defined. Please select a language.')
        menu_language(delayed_start_var=True)
    elif language_status != 'active':
        language_status = 'active'
        apply_constants()
    # Invalid path dataset
    elif 'invalid_path_dataset' in delayed_start:
        messagebox.showwarning(print_on_language(1, 47), print_on_language(1, 48))
        menu_settings_dataset(buttons=False)
        delayed_start.remove('invalid_path_dataset')
        delayed_start.remove('invalid_parameters_values')
    # Invalid parameters_values
    elif 'invalid_parameters_values' in delayed_start:
        messagebox.showwarning(print_on_language(1, 47), print_on_language(1, 49))
        menu_settings_dataset(buttons=False)
        delayed_start.remove('invalid_parameters_values')
    # check for normal status
    elif len(delayed_start) == 0:
        # Creating a list of incidents
        list_incidents = calculations.make_list_incidents(data, name, sex, parallel, letter, causes,
                                                          time_causes, previous_causes)
        configuration_status = 'normal'
        menu_main()


def setup_scroll():
    global container, canvas, v_scrollbar, h_scrollbar, scrollable_frame
    container = Frame(root)
    canvas = Canvas(container, highlightthickness=0)
    v_scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)


def active_scroll():
    global canvas_frame, status_scroll
    setup_scroll()
    container.pack(fill='both', expand=True)
    canvas.configure(yscrollcommand=v_scrollbar.set)
    canvas.bind("<Configure>", on_canvas_configure)
    canvas.bind_all("<MouseWheel>", scroll_canvas)
    canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas.pack(side='left', fill='both', expand=True, padx=70, pady=5)
    v_scrollbar.pack(side="right", fill="y")
    status_scroll = 'active'


def disable_scroll():
    global status_scroll
    canvas.delete('all')
    scrollable_frame.pack_forget()
    v_scrollbar.pack_forget()
    container.pack_forget()
    status_scroll = 'disabled'


def on_canvas_configure(event):
    canvas.configure(scrollregion=height_window())
    canvas.itemconfig(canvas_frame, width=event.width - 4)


def height_window():
    if scrollable_frame.winfo_height() > canvas.winfo_height():
        height = scrollable_frame.winfo_height()
    else:
        height = canvas.winfo_height()
    return 0, 0, height, height


# Для scroll_canvas
last_event = 0
count_drop = 0


# Привязка прокрутки к мыши
def scroll_canvas(event):
    global last_event, count_drop
    if platform.system() == 'Windows':
        canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
    elif platform.system() == 'Darwin':
        v_event = last_event
        count_drop = count_drop + abs(int(-1 * event.delta)) // int(-1 * event.delta)
        if v_event == 0:
            v_event = count_drop
        if abs(count_drop) > 2:
            count_drop = (abs(count_drop) // count_drop) * 2
        elif count_drop == 0:
            count_drop = abs(int(-1 * event.delta)) // int(-1 * event.delta)
            v_event = count_drop
        canvas.yview_scroll(v_event, 'units')
        last_event = v_event
    else:
        if event.num == 4:
            canvas.yview_scroll(-1, 'units')
        elif event.num == 5:
            canvas.yview_scroll(1, 'units')


def clear_window(message=None):
    if is_debug:
        print(debug.i(), 'Clearing the screen')
    if status_scroll == 'active':
        disable_scroll()
    for widget in button_frame.winfo_children() + head.winfo_children() + window.winfo_children():
        widget.destroy()
    head.pack_forget()
    window.pack(expand=True)
    if message is not None:
        Label(window, text=message, fg='red').grid(column=0, row=0)


def back_button(column_btn, count_row, translated=True, back_command=lambda: menu_main()):
    if not translated:
        exit_btn = Button(button_frame, text='Back', command=back_command)
    else:
        exit_btn = Button(button_frame, text=print_on_language(1, 30), command=back_command)
    exit_btn.grid(column=column_btn, row=count_row, padx=5, pady=5)


def exit_button(column_btn, count_row, translated=True, exit_command=lambda: exit(debug.i() + ' Exiting...' if is_debug
                                                                                  else '')):
    if not translated:
        exit_btn = Button(button_frame, text='Exit', command=exit_command)
    else:
        exit_btn = Button(button_frame, text=print_on_language(1, 21), command=exit_command)
    exit_btn.grid(column=column_btn, row=count_row, padx=5, pady=5)


def menu_main():
    clear_window()
    root.update()
    if is_debug:
        print(debug.i(), 'The main menu is open')
    Label(window, text=print_on_language(1, 6) + '. ' + print_on_language(1, 7) + ':').grid(column=0, row=0)

    # Program operation mode selection
    Button(window, text=modes[0], command=menu_causal_relationship).grid(column=0, row=1)
    Button(window, text=modes[1], command=menu_charts).grid(column=0, row=2)
    Button(window, text=print_on_language(1, 31), command=menu_settings).grid(column=0, row=3)
    exit_button(0, 4)


def menu_causal_relationship():
    global gen_best_variant, sorted_list
    clear_window()
    window.pack_forget()
    head.pack(side='top')
    if is_debug:
        print(debug.i(), 'The causal relationship menu is open')
    info = []
    cropped_list = make_cropped_list(list_incidents)
    if auto_number_clusters:
        if gen_best_variant is None:
            gen_best_variant = calculations.auto_kmeans_clusters(cropped_list)
        clusters = gen_best_variant
    else:
        clusters = int(calculations.read_from_configuration(11))
    if sorted_list is None:
        sorted_list = calculations.sort_by_kmeans_clusters(list_incidents, cropped_list, clusters)
    list_incidents_numbered = print_data.print_list_incidents(list_incidents)
    Label(head, text=print_on_language(1, 0)).grid(column=0, row=0)
    if beta_settings:
        if kmeans_group:
            v = 'KMeans'
        else:
            v = print_on_language(1, 76)
        Label(head, text=print_on_language(1, 75) + ': ').grid(column=0, row=1, sticky='w')
        Button(head, text=v, command=group_by_kmeans).grid(column=0, row=1, sticky='e')
    active_scroll()
    scrollable_frame.grid_columnconfigure(0, weight=1)
    if kmeans_group:
        Button(head, text=print_on_language(1, 77), command=regen_sorted_list).grid(column=0, row=2)
        count_row = len(sorted_list)
        count = 0
        for i in range(count_row):
            for j in range(len(sorted_list[i])):
                Button(scrollable_frame, text=sorted_list[i][j][0] + ' ' + sorted_list[i][j][2],
                       command=lambda k=i: menu_causal_relationship_information(k, info)).grid(column=0, row=count + 1,
                                                                                               sticky='w')
                count = count + 1
            Label(scrollable_frame).grid(column=0, row=count + 1)
            count = count + 1
    else:
        count_row = len(list_incidents_numbered)
        for i in range(count_row):
            Button(scrollable_frame, text=list_incidents_numbered[i],
                   command=lambda k=i: menu_causal_relationship_information(k, info)).grid(column=0, row=i + 1,
                                                                                           sticky='w')
    back_button(0, count_row + 1)
    exit_button(1, count_row + 1)


def regen_sorted_list():
    global gen_best_variant, sorted_list, kmeans_group
    gen_best_variant, sorted_list = None, None
    kmeans_group = True
    menu_causal_relationship()
    root.update()


def group_by_kmeans():
    global kmeans_group
    kmeans_group = not kmeans_group
    root.update()
    menu_causal_relationship()


def make_cropped_list(example_list):
    return pandas.DataFrame(example_list).drop([0, 1, 2], axis=1)


def menu_causal_relationship_information(user_selection, info):
    clear_window()
    window.pack_forget()
    head.pack(side='top')
    if is_debug:
        print(debug.i(), 'The causal relationship menu about student is open')
    active_scroll()
    scrollable_frame.grid_columnconfigure(0, weight=1, minsize=300)
    if list_incidents[user_selection][1] == print_on_language(1, 4) or (print_on_language(3, 2) == 0):
        user_choice_text = print_on_language(1, 2) + ' ' + str(user_selection + 1) + '. ' + print_on_language(2, 2) + \
                           ': ' + str(list_incidents[user_selection][0])
    else:
        user_choice_text = print_on_language(1, 2) + ' ' + str(user_selection + 1) + '. ' + print_on_language(3, 2) + \
                           ': ' + str(list_incidents[user_selection][0])
    Label(head, text=user_choice_text).grid(column=0, row=0, sticky='w')
    Label(scrollable_frame, text=print_on_language(1, 65), background='#DCDCDC').grid(column=0, row=1, sticky='w')

    # Calculations: search for matching information
    calculations.intersection_of_classes(list_incidents, user_selection, info, 0)
    calculations.intersection_of_time(list_incidents, user_selection, info, 0)
    student_text, incident_text = calculations.conclusions(list_incidents, user_selection, info)
    # Calculations: conclusions
    Label(scrollable_frame, text=student_text).grid(column=0, row=2)
    Label(scrollable_frame).grid(column=0, row=3)
    ttk.Separator(scrollable_frame, orient='horizontal').grid(column=0, row=3, columnspan=4, sticky='we')
    Label(scrollable_frame, text=print_on_language(1, 66), background='#DCDCDC').grid(column=0, row=4, sticky='w')
    Label(scrollable_frame, text=incident_text).grid(column=0, row=5)
    back_button(0, 4, back_command=menu_causal_relationship)
    exit_button(1, 4)


def menu_charts():
    clear_window()
    if is_debug:
        print(debug.i(), 'The charts menu is open')
    list_graphs_numbered = print_data.print_selection_list(available_charts)
    Label(window, text=print_on_language(1, 10) + ':')
    count_row = len(list_graphs_numbered)
    for i in range(count_row):
        if i == 3:
            if len(parallel.value_counts().values) < 7 or len(previous_causes.value_counts().values) < 7:
                continue
        Button(window, text=list_graphs_numbered[i], command=lambda j=i: mode_chart_process(j)) \
            .grid(column=0, row=i + 1, sticky=W)
    back_button(0, count_row + 1)
    exit_button(1, count_row + 1)


def mode_chart_process(choice_chart):
    if is_debug:
        print(debug.i(), 'Displaying a chart...')
    charts.set_variables(list_incidents, causes, parallel, name_columns, previous_causes)
    charts.chart_selection(choice_chart, data)
    count_row = len(available_charts)
    back_button(0, count_row + 1)
    exit_button(1, count_row + 1)


def menu_settings():
    clear_window()
    if is_debug:
        print(debug.i(), 'The settings are open')
    window.columnconfigure(0, minsize=140)
    width = max([len(print_on_language(1, 32)), len(print_on_language(1, 82)), len(print_on_language(1, 20)),
                 len(print_on_language(1, 43))])
    Button(window, text=print_on_language(1, 32), command=menu_settings_dataset, width=width).grid(column=0, row=0,
                                                                                                   sticky='w')
    if beta_settings:
        Button(window, text=print_on_language(1, 82), command=menu_settings_causal_rel_mode, width=width)\
            .grid(column=0, row=1, sticky='w')
    Button(window, text=print_on_language(1, 20), command=lambda: menu_language(True), width=width)\
        .grid(column=0, row=2, sticky='w')
    Button(window, text=print_on_language(1, 43), command=menu_about_program, width=width)\
        .grid(column=0, row=3, sticky='w')
    Label(window, text=print_on_language(1, 83)).grid(column=0, row=4, sticky='w')
    v = StringVar()
    Button(window, textvariable=v, command=lambda: active_beta_settings(v)).grid(column=0, row=4, sticky='e')
    if beta_settings:
        v.set(print_on_language(1, 80))
    else:
        v.set(print_on_language(1, 81))
    back_button(0, 1)
    exit_button(1, 1)


def active_beta_settings(text):
    global beta_settings
    if beta_settings:
        beta_settings = False
        change_configuration('beta_settings', indexes[9], str(0))
        text.set(print_on_language(1, 81))
    else:
        beta_settings = True
        change_configuration('beta_settings', indexes[9], str(1))
        text.set(print_on_language(1, 80))
    if debug:
        print(debug.i(), 'Beta settings:', beta_settings)
    root.update()
    menu_settings()


def menu_settings_dataset(buttons=True):
    global parameters_dataset
    root.update()
    clear_window()
    active_scroll()
    head.pack_forget()
    window.pack_forget()
    scrollable_frame.grid_columnconfigure(0, weight=1, minsize=300)
    scrollable_frame.grid_columnconfigure(1, weight=2)
    if is_debug:
        print(debug.i(), 'The dataset settings are open')
    Label(scrollable_frame, text=print_on_language(1, 59), background='#DCDCDC').grid(column=0, row=0, sticky='w')
    file_btn_text = StringVar()
    Button(scrollable_frame, textvariable=file_btn_text, command=lambda: show_path(file_loc)) \
        .grid(column=0, row=1, sticky='w')
    file_btn_text.set(print_on_language(1, 34) + ': ' + short_filename(file_loc))
    Button(scrollable_frame, text=print_on_language(1, 35), command=lambda: change_dataset(file_btn_text)) \
        .grid(column=1, row=1, sticky='e')
    Label(scrollable_frame).grid(column=0, row=2)
    ttk.Separator(scrollable_frame, orient='horizontal').grid(column=0, row=2, columnspan=4, sticky='we')
    Label(scrollable_frame, text=print_on_language(1, 33), background='#DCDCDC').grid(column=0, row=3, sticky='w')
    Label(scrollable_frame, text=print_on_language(1, 61)).grid(column=0, row=4, sticky='w')
    Label(scrollable_frame, text=print_on_language(1, 60)).grid(column=1, row=4, sticky='e')
    count_row = 5
    parameters_dataset = calculations.get_parameters_dataset()
    entries = []
    for i in range(len(parameters_dataset)):
        v = StringVar(root, value=str(configuration[indexes[1 + i]][str(configuration[indexes[1 + i]]).find("'") + 1:
                                                                    str(configuration[indexes[1 + i]]).rfind("'")]))
        Label(scrollable_frame, text=parameters_dataset_translated[i]).grid(column=0, row=count_row, sticky='w')
        value_entry = Entry(scrollable_frame, textvariable=v, width=10)
        entries.append(value_entry)
        value_entry.grid(column=1, row=count_row, sticky='e')
        count_row = count_row + 1
    if not buttons:
        Button(button_frame, text=print_on_language(1, 50),
               command=lambda: apply_dataset(entries, delayed_start_var=True)).grid(column=0, row=count_row + 1)
    else:
        back_button(0, count_row + 1, back_command=lambda: apply_dataset(entries))
    exit_button(1, count_row + 1, exit_command=lambda: apply_dataset(entries, apply_exit=True))


def apply_dataset(changes, delayed_start_var=False, apply_exit=None):
    if file_loc is None:
        if apply_exit:
            exit()
        else:
            messagebox.showerror(print_on_language(1, 41), print_on_language(1, 55))
        return
    supported_parameters = calculations.get_supported_parameters()
    for i in range(len(parameters_dataset)):
        if not changes[i].get().isdigit() or not 0 < int(changes[i].get()) < len(parameters_dataset) + 1:
            messagebox.showerror(print_on_language(1, 41), print_on_language(1, 53))
            return
        else:
            change_configuration(supported_parameters[1 + i], indexes[1 + i], changes[i].get())
    if len(calculations.check_configuration(only_dataset=True)) != 0:
        messagebox.showerror(print_on_language(1, 41), print_on_language(1, 54))
        return
    else:
        global list_incidents, name, sex, parallel, letter, causes, time_causes, previous_causes, configuration
        configuration = open("configuration", 'r').read().split('\n')
        calculations.set_variables(configuration)
        set_dataset_columns()
        # Convert time
        for i in range(data.shape[0]):
            if str(time_causes[i]).replace(':', '').isdigit():
                if time_causes[i] != 0:
                    time_causes[i] = int(str(time_causes[i]).replace(':', ''))
                    if len(str(time_causes[i])) < 6:
                        time_causes[i] = str(0) + str(time_causes[i])
                else:
                    time_causes[i] = int(time_causes[i])
            else:
                messagebox.showerror(print_on_language(1, 41), print_on_language(1, 53))
                return

        # Re-creating a list of incidents
        list_incidents = calculations.make_list_incidents(data, name, sex, parallel, letter, causes,
                                                          time_causes, previous_causes)
    if apply_exit:
        exit(debug.i() + ' Exiting...' if is_debug else '')
    elif not delayed_start_var:
        menu_settings()
    else:
        apply_constants()
        messagebox.showinfo(title=print_on_language(1, 51), message=print_on_language(1, 52))
        fix_configuration()


def check_dataset(new_file_loc):
    try:
        pandas.read_excel(new_file_loc)
    except ValueError:
        if is_debug:
            print(debug.e, 'Incorrect dataset is selected')
        return False
    if len(list(pandas.read_excel(new_file_loc))) < 7:
        if is_debug:
            print(debug.e, 'The selected dataset contains too little data')
        return False
    return True


def change_dataset(file_btn_text):
    global data, name_columns, file_loc
    new_file_loc = askopenfilename(filetypes=[("Excel file", "*.xlsx"), ("Excel file 97-2003", "*.xls")])
    if new_file_loc != '':
        if not check_dataset(new_file_loc):
            messagebox.showerror(print_on_language(1, 41), print_on_language(1, 42))
            return
        data, name_columns = set_dataset_parameters(new_file_loc)
        change_configuration('dataset_path', indexes[8], new_file_loc)
        file_loc = new_file_loc
        if file_loc is not None and '/' in file_loc:
            file_btn_text.set(print_on_language(1, 34) + ': ' + short_filename(file_loc))
        else:
            file_btn_text.set(print_on_language(1, 34) + ': ' + str(None))


def show_path(file_location):
    if file_location is not None:
        messagebox.showinfo(print_on_language(1, 59), file_location)
    else:
        messagebox.showinfo(print_on_language(1, 59), print_on_language(1, 62))


def short_filename(file_path):
    if file_path is not None and '/' in file_path:
        filename = str(file_path[file_path.rfind('/') + 1:])
        filename = (filename[:46 - len(print_on_language(1, 59))] + '...') \
            if len(filename) + len(print_on_language(1, 59)) > 45 else filename
        return filename
    else:
        return str(None)


def menu_settings_causal_rel_mode():
    clear_window()
    v = StringVar()
    Label(window, text='KMeans', background='#DCDCDC').grid(column=0, row=0, sticky='w')
    Label(window, text=print_on_language(1, 78)).grid(column=0, row=1)
    Button(window, textvariable=v, command=lambda: active_auto_number_clusters(v, entries)).grid(column=1, row=1)
    entries = []
    if auto_number_clusters:
        v.set(print_on_language(1, 80))
        back_button(0, 2, back_command=menu_settings)
        exit_button(1, 2)
    else:
        v.set(print_on_language(1, 81))
        current_v = StringVar(root, value=calculations.read_from_configuration(11))
        Label(window, text=print_on_language(1, 79)).grid(column=0, row=2, sticky='w')
        value_entry = Entry(window, textvariable=current_v, width=9)
        entries.append(value_entry)
        value_entry.grid(column=1, row=2)
        back_button(0, 2, back_command=lambda: apply_clusters(entries))
        exit_button(1, 2, exit_command=lambda: apply_clusters(entries, v_exit=True))


def apply_clusters(entries, v_exit=False, action=1):
    global configuration
    if len(entries) == 0:
        return
    elif entries[0].get().isdigit() and 2 <= int(str(entries[0].get())) <= 15:
        change_configuration('num_clusters', indexes[11], str(entries[0].get()))
        update_configuration()
        if action:
            if v_exit:
                exit('I Exiting')
            else:
                menu_settings()
    else:
        messagebox.showerror(print_on_language(1, 41), print_on_language(1, 84))


def active_auto_number_clusters(text, entries):
    apply_clusters(entries, action=0)
    global auto_number_clusters
    if auto_number_clusters:
        auto_number_clusters = False
        change_configuration('auto_number_clusters', indexes[10], str(0))
        text.set(print_on_language(1, 80))
    else:
        auto_number_clusters = True
        change_configuration('auto_number_clusters', indexes[10], str(1))
        text.set(print_on_language(1, 81))
    if debug:
        print(debug.i(), 'auto number clusters:', auto_number_clusters)
    root.update()
    menu_settings_causal_rel_mode()


def menu_language(back_btn=None, delayed_start_var=False):
    clear_window()
    files = os.listdir(os.getcwd() + '/languages')
    if is_debug:
        print(debug.i(), 'The language menu are open')
    Label(window, text='Available languages:').grid(column=0, row=0)
    count_row = 1
    for i in range(len(files)):
        if files[i][:8] == 'strings_':
            if language == files[i].replace('strings_', '').replace('.xlsx', ''):
                if delayed_start_var:
                    text = ' ' + '(selected)'
                else:
                    text = ' (' + print_on_language(1, 57) + ')'
            else:
                text = ''
            Button(window, text=files[i].replace('strings_', '').replace('.xlsx', '') + text,
                   command=lambda j=i: change_language_process(files, j, delayed_start_var)) \
                .grid(column=0, row=count_row)
            count_row = count_row + 1
    column_btn = 0
    translated = False
    if back_btn:
        back_button(column_btn, count_row + 2, back_command=menu_settings)
        column_btn = column_btn + 1
        translated = True
    exit_button(column_btn, count_row + 2, translated)


def change_language_process(files, index_language, delayed_start_var=False):
    global language_status, delayed_start, language
    new_language = files[index_language].replace('strings_', '').replace('.xlsx', '')
    set_language(new_language)
    language_status = 'active'
    if delayed_start_var:
        delayed_start.remove('invalid_language')
    language = new_language
    apply_constants(open_main_menu=False)


def menu_about_program():
    clear_window()
    if is_debug:
        print(debug.i(), 'The "About program" menu is open')
    Label(window, text=print_on_language(1, 15)).grid(column=0, row=0)
    Button(window, text=print_on_language(1, 44) + ': ' + version,
           command=check_updates) \
        .grid(column=0, row=1)
    Button(window, text=print_on_language(1, 45) + ': Artem Agapkin',
           command=lambda: open_link('https://github.com/Ariollex')) \
        .grid(column=0, row=2)
    Button(window, text=print_on_language(1, 46) + ': ' + 'https://github.com/Ariollex/causal-relationships-in-school',
           command=lambda: open_link('https://github.com/Ariollex/causal-relationships-in-school')) \
        .grid(column=0, row=3)
    back_button(0, 1, back_command=menu_settings)
    exit_button(1, 1)


def check_updates():
    global count_click_ee
    url = 'https://api.github.com/repos/ariollex/causal-relationships-in-school/releases/latest'
    latest_response = requests.get(url)
    if is_debug:
        print(debug.i(), 'Checking for updates...')
    if latest_response.status_code == 200:
        if is_debug:
            print(debug.i(), 'Server response received...')
        response_data = json.loads(latest_response.text or latest_response.content)
        latest_version = response_data['tag_name']
        if latest_version <= version:
            count_click_ee = count_click_ee + 1
            if is_debug:
                print(debug.i(), 'The latest update is already installed!')
            if count_click_ee == 5:
                count_click_ee = 0
                easter_egg()
            else:
                messagebox.showinfo(print_on_language(1, 73), print_on_language(1, 69))
        elif get_int(latest_version) > get_int(version):
            if is_debug:
                print(debug.i(), 'Update available!')
            messagebox.showinfo(print_on_language(1, 73), print_on_language(1, 72) +
                                'https://github.com/Ariollex/causal-relationships-in-school/releases/latest')
    else:
        if is_debug:
            print(debug.e(), 'Update check error!')
        messagebox.showinfo(print_on_language(1, 73), print_on_language(1, 71))


def easter_egg():
    quotes = [
        '"Talk is cheap. Show me the code", - Linus Torvalds',
        '"Programs must be written for people to read, and only incidentally for machines to execute", '
        '- Harold Abelson',
        '"Any fool can write code that a computer can understand. Good programmers write code that humans can '
        'understand", - Martin Fowler',
        '"If debugging is the process of removing software bugs, then programming must be the process of putting '
        'them in", - Edsger W. Dijkstra',
        '"The best way to predict the future is to invent it", - Alan Kay'
    ]
    messagebox.showinfo("Easter egg", 'Congratulations! \nYou found an Easter egg!\n\n' + random.choice(quotes))


if is_debug:
    print(debug.i(), 'Creating a window...')
root = Tk()
root.minsize(600, 250)
window = Frame(root)
head = Frame(root)
head.pack(side='top')
window.pack(expand=True)
container, canvas, v_scrollbar, h_scrollbar, scrollable_frame, canvas_frame = \
    Frame(), Canvas(), Scrollbar(), Scrollbar(), Frame(), int()
status_scroll = 'disabled'
button_frame = Frame(root)
button_frame.pack(side="bottom")
count_click_ee = 0
beta_settings = bool(int(calculations.read_from_configuration(9)))
auto_number_clusters = bool(int(calculations.read_from_configuration(10)))
gen_best_variant = None
sorted_list = None
kmeans_group = False

if len(delayed_start) != 0:
    root.title('Causal relationships in school, ' + version)
    configuration_status = 'break'
    language_status = 'break'
    if is_debug:
        print(debug.i(), 'Launch a window for correction')
    fix_configuration()
else:
    configuration_status = 'normal'
    if is_debug:
        print(debug.i(), 'Applying constants...')
    apply_constants()
root.mainloop()
