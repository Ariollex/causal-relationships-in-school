import print_data


def make_list_incidents(data, name, sex, parallel, letter, causes, time_causes, previous_causes):
    example_list_incidents = []
    for i in range(0, data.shape[0]):
        if causes[i] != 0:
            school_class = str(parallel[i]) + ' "' + letter[i] + '"'
            example_list_incidents.append(
                [name[i], sex[i], school_class, time_causes[i], previous_causes[i]])
    return example_list_incidents


def intersection_of_classes(example_list_incidents, user_selection, info, func):
    count = 0
    students = []
    for i in range(len(example_list_incidents)):
        if example_list_incidents[user_selection][2] == example_list_incidents[i][2] and user_selection != i:
            if func == 0:
                count = count + 1
            elif func == 1:
                students.append(example_list_incidents[i][0])
    if func == 0:
        info.append([count, example_list_incidents[user_selection][2]])
    elif func == 1:
        return students


def intersection_of_time(example_list_incidents, user_selection, info, func):
    count = 0
    students = []
    for i in range(len(example_list_incidents)):
        if example_list_incidents[user_selection][3] == example_list_incidents[i][3] and user_selection != i:
            if func == 0:
                count = count + 1
            elif func == 1:
                students.append(example_list_incidents[i][0])
    if func == 0:
        info.append([count, example_list_incidents[user_selection][3]])
    elif func == 1:
        return students


def intersection_of_previous_causes(example_list_incidents, participants):
    maximum = [0, 0]
    for i in range(len(example_list_incidents)):
        for j in range(len(participants)):
            if example_list_incidents[i][0] == participants[j] and example_list_incidents[0][4] > int(maximum[1]):
                maximum = [example_list_incidents[i][0], example_list_incidents[i][4]]
    return maximum


def conclusions(example_list_incidents, user_selection, info):
    student_name = example_list_incidents[user_selection][0]
    participants = None
    if info[1][0] != 0:
        participants = intersection_of_time(example_list_incidents, user_selection, info, 1)
    elif info[0][0] != 0:
        participants = intersection_of_classes(example_list_incidents, user_selection, info, 1)
    maximum = (intersection_of_previous_causes(example_list_incidents, participants) if participants is not None else [0, 0])
    suspicious = (1 if maximum[1] > 4 else 0)
    class_matters = (1 if info[0][0] != 0 else 0)
    time_matters = (1 if info[1][0] != 0 else 0)
    if time_matters == 1 and class_matters == 1:
        return print_data.is_fight(1, participants, info[0][1], suspicious, maximum, student_name)
    elif time_matters == 1 and class_matters == 0:
        return print_data.is_fight(0, participants, 0, suspicious, maximum, student_name)
    elif time_matters == 0 and class_matters == 1:
        return print_data.is_incident_in_classroom(participants, info[0][1], suspicious, maximum, student_name)
    else:
        return print_data.is_personal_incident(student_name, info[0][1])
