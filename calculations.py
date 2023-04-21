import print_data
import numpy
import os
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


configuration, indexes, supported_parameters, parameters_dataset = [], [], [], []
incident_time = 0
participants = []


def get_supported_parameters():
    return supported_parameters


def get_parameters_dataset():
    return parameters_dataset


def set_variables(configuration_file):
    global configuration
    configuration = configuration_file


def read_from_configuration(n):
    return configuration[indexes[n]][str(configuration[indexes[n]]).find("'") + 1:
                                     str(configuration[indexes[n]]).rfind("'")]


def auto_kmeans_clusters(list_incidents):
    data = list_incidents
    best_n_clusters = 2
    sil_score_max = -1  # this is the minimum possible score
    n = 15 if len(list_incidents) > 15 else len(list_incidents)
    for n_clusters in range(2, n):
        model = KMeans(n_clusters=n_clusters, init='k-means++', n_init='auto')
        labels = model.fit_predict(data)
        sil_score = silhouette_score(data, labels)
        if sil_score > sil_score_max:
            sil_score_max = sil_score
            best_n_clusters = n_clusters
    return best_n_clusters


def sort_by_kmeans_clusters(full_list_incidents, list_incidents, num_clusters):
    kmeans = KMeans(n_clusters=num_clusters, n_init='auto')
    kmeans.fit(list_incidents)
    labels = kmeans.predict(list_incidents)
    sorted_array = []
    for i in range(max(labels) + 1):
        sorted_array.append([full_list_incidents[j] for j in range(len(full_list_incidents)) if labels[j] == i])
    return sorted_array


def check_parameters():
    global parameters_dataset
    parameters_dataset = ['name', 'sex', 'parallel', 'letter', 'causes', 'time_causes', 'previous_causes']
    parameters_strings = ['language']
    parameters_path = ['dataset_path']
    parameters_other = ['num_clusters']
    errors, resets = [], []
    for i in range(len(supported_parameters)):
        example_parameter_name = supported_parameters[i]
        example_parameter_value = read_from_configuration(i)
        if example_parameter_name in parameters_dataset and (not example_parameter_value.isdigit() or
                                                             not (0 < int(example_parameter_value) <
                                                                  len(parameters_dataset) + 1)):
            errors.append('Parameter "' + example_parameter_name + '" has an incorrect value! It should be integer.')
        if example_parameter_name in parameters_strings and isinstance(example_parameter_value, str) is False:
            errors.append('Parameter "' + example_parameter_name + '" has an incorrect value! It should be string.')
        if example_parameter_name in parameters_path and not os.path.exists(example_parameter_value):
            errors.append('Parameter "' + example_parameter_name + '" has an incorrect path.')
        if example_parameter_name in parameters_other and (not example_parameter_value.isdigit() or
                                                           not (2 <= int(example_parameter_value) <= 15)):
            resets.append(example_parameter_name)
    return errors, resets


def check_configuration(only_dataset=False, only_indexes=False):
    global indexes, supported_parameters
    supported_parameters = ['language', 'name', 'sex', 'parallel', 'letter', 'causes',
                            'time_causes', 'previous_causes', 'dataset_path', 'beta_settings',
                            'auto_number_clusters', 'num_clusters']
    indexes = [numpy.nan] * len(supported_parameters)
    warnings = []
    missing_parameters = []
    for i in range(len(configuration)):
        parameter_name = configuration[i][:configuration[i].find(' ')]
        if configuration[i] == '' or configuration[i][0] == '#':
            continue
        elif parameter_name not in supported_parameters:
            warnings.append('Unknown parameter ' + '"' + parameter_name + '"' + ' in the configuration file. '
                                                                                'This can cause problems!')
        elif not numpy.isnan(indexes[supported_parameters.index(parameter_name)]):
            warnings.append('Duplicate parameter ' + '"' + parameter_name + '"' + ' in the configuration file. '
                                                                                  'This can cause problems!')
        else:
            indexes[supported_parameters.index(parameter_name)] = i
    if numpy.nan in indexes:
        missing_parameters = []
        for i in range(len(indexes)):
            if numpy.isnan(indexes[i]):
                missing_parameters.append(supported_parameters[i])
    if only_dataset:
        return missing_parameters
    if only_indexes:
        return indexes
    return indexes, warnings, missing_parameters


def make_list_incidents(data, name, sex, parallel, letter, causes, time_causes, previous_causes):
    example_list_incidents = []
    for i in range(0, data.shape[0]):
        if causes[i] != 0:
            school_class = str(parallel[i]) + ' "' + str(letter[i]) + '"'
            example_list_incidents.append(
                [name[i], sex[i], school_class, time_causes[i], previous_causes[i], parallel[i],
                 int(parallel[i]) + int(ord(letter[i]))])
    return example_list_incidents


def intersection_of_classes(example_list_incidents, user_selection, info, func):
    count = 0
    students = []
    for i in range(len(example_list_incidents)):
        if example_list_incidents[user_selection][2] == example_list_incidents[i][2] and user_selection != i:
            if func == 0:
                count = count + 1
            elif func == 1:
                students.append((example_list_incidents[i][0], example_list_incidents[i][2]))
    if func == 0:
        info.append([count, example_list_incidents[user_selection][2]])
    elif func == 1:
        return students


def intersection_of_time(example_list_incidents, user_selection, info, func):
    global incident_time
    count = 0
    students = []
    for i in range(len(example_list_incidents)):
        if example_list_incidents[user_selection][3] == example_list_incidents[i][3] and user_selection != i:
            if func == 0:
                count = count + 1
            elif func == 1:
                students.append((example_list_incidents[i][0], example_list_incidents[i][2]))
                incident_time = example_list_incidents[i][3]
    if func == 0:
        info.append([count, example_list_incidents[user_selection][3]])
    elif func == 1:
        return students, incident_time


def intersection_of_previous_causes(example_list_incidents):
    maximum = [0, 0]
    for i in range(len(example_list_incidents)):
        for j in range(len(participants)):
            if example_list_incidents[i][0] == participants[j][0] and example_list_incidents[i][4] > int(maximum[1]):
                maximum = [example_list_incidents[i][0], example_list_incidents[i][4]]
    return maximum


def conclusions(example_list_incidents, user_selection, info):
    global participants, incident_time
    participants, incident_time = [], 0
    student_name = example_list_incidents[user_selection][0]
    if info[1][0] != 0:
        participants, incident_time = intersection_of_time(example_list_incidents, user_selection, info, 1)
    elif info[0][0] != 0:
        participants = intersection_of_classes(example_list_incidents, user_selection, info, 1)
    maximum = (intersection_of_previous_causes(example_list_incidents) if len(participants) != 0 else [0, 0])
    count_last_incidents = example_list_incidents[user_selection][4]
    suspicious = (1 if maximum[1] > 4 else 0)
    class_matters = (1 if info[0][0] != 0 else 0)
    time_matters = (1 if info[1][0] != 0 else 0)
    return print_data.full_information(time_matters, class_matters, participants, info[0][1], suspicious, maximum,
                                       student_name, count_last_incidents, incident_time)
