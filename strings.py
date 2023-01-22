import os
import numpy
import pandas
import input_data

language_texts = []


def set_language(language):
    global language_texts
    if language != open("current_language", 'r').read():
        lines = open("current_language", 'r').readlines()
        lines[0] = language
        out = open("current_language", 'w')
        out.writelines(lines)
        out.close()
    language_texts = pandas.read_excel('languages/strings_' + language + '.xlsx')
    language_texts.replace(numpy.nan, 0, inplace=True)
    language_texts.columns = range(language_texts.columns.size)


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
