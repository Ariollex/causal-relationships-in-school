import os
import numpy
import pandas

configuration, indexes, language_texts = [], [], []


def set_variables(configuration_file, indexes_in_conf_file):
    global configuration, indexes
    configuration = configuration_file
    indexes = indexes_in_conf_file


def set_language(language):
    global language_texts
    if language != configuration[indexes[0]][
                   str(configuration[indexes[0]]).find("'") + 1:str(configuration[indexes[0]]).rfind("'")]:
        lines = open("configuration", 'r').readlines()
        lines[indexes[0]] = "language = '" + language + "'\n"
        out = open("configuration", 'w')
        out.writelines(lines)
        out.close()
    if os.path.exists('languages/strings_' + language + '.xlsx'):
        language_texts = pandas.read_excel('languages/strings_' + language + '.xlsx')
        language_texts.replace(numpy.nan, 0, inplace=True)
        language_texts.columns = range(language_texts.columns.size)
        return True
    else:
        return False


def print_on_language(column, line):
    return language_texts[column][line]
