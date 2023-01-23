import os
import numpy
import pandas
import input_data
import error

configuration, indexes, language_texts = [], [], []


def set_variables(configuration_file, indexes_in_conf_file):
    global configuration, indexes
    configuration = configuration_file
    indexes = indexes_in_conf_file


def set_language(language):
    global language_texts
    if language != configuration[indexes[2]][
                   str(configuration[indexes[2]]).find("'") + 1:str(configuration[indexes[2]]).rfind("'")]:
        lines = open("configuration", 'r').readlines()
        lines[2] = "language = '" + language + "'"
        out = open("configuration", 'w')
        out.writelines(lines)
        out.close()
    if os.path.exists('languages/strings_' + language + '.xlsx'):
        language_texts = pandas.read_excel('languages/strings_' + language + '.xlsx')
        language_texts.replace(numpy.nan, 0, inplace=True)
        language_texts.columns = range(language_texts.columns.size)
    else:
        error.error(language + ' language is not supported. \n'
                               'Make sure that you downloaded the program from '
                               'https://github.com/Ariollex/causal-relationships-in-school/releases '
                               'and did not make any changes to the code. \n', 0)
        print('Supported languages:')
        files = os.listdir('languages')
        for i in range(len(files)):
            print(files[i].replace('strings_', '').replace('.xlsx', ''), sep='')
        print('\033[91mConfigure this in "configuration" or reinstall the program.\033[0m')
        exit('Broken configuration!')


def change_language():
    files = os.listdir('languages')
    print('Available languages:')
    for i in range(len(files)):
        print(i + 1, ') ', files[i].replace('strings_', '').replace('.xlsx', ''), sep='')
    print('Please note that if the dataset and the program language are different, there may be errors.')
    print('Enter the number: ', end='')
    language = input_data.make_user_choice(files)
    language = files[language].replace('strings_', '').replace('.xlsx', '')
    set_language(language)
    exit(print_on_language(1, 14))


def print_on_language(column, line):
    return language_texts[column][line]
