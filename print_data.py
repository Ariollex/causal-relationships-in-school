from strings import print_on_language


def print_list_incidents(example_list_incidents):
    for i in range(len(example_list_incidents)):
        print(i + 1, ') ', example_list_incidents[i][0], ' ', example_list_incidents[i][2], sep='')
    print(print_on_language(1, 0), end=': ')


def print_selection_list(example_list):
    for i in range(len(example_list)):
        print(i + 1, ') ', example_list[i], sep='')


def is_fight(in_class, participants, student_class, suspicious, maximum, student_name):
    result = print_on_language(1, 22) + ': '
    if in_class == 0:
        result = result + print_on_language(1, 23).lower()
        if suspicious != 0:
            result = result + '\n' + print_on_language(1, 24) + ' ' + maximum[0] + ' ' + \
                     ', ' + print_on_language(2, 24) + ' ' + str(maximum[1]) + ' ' + print_on_language(3, 24)
    else:
        result = result + print_on_language(1, 23).lower() + ' ' + print_on_language(2, 23) + ' ' + student_class
        if suspicious != 0:
            result = result + '\n' + print_on_language(1, 24) + ' ' + maximum[0] + ' ' + \
                     ', ' + print_on_language(2, 24) + ' ' + str(maximum[1]) + ' ' + print_on_language(3, 24)
    result = result + '\n' + print_on_language(1, 25) + ' ' + str(len(participants) + 1) + ' ' + \
        print_on_language(2, 25) + ':' + '\n' + student_name + '\n' + '\n'.join(participants)
    return result


def is_incident_in_classroom(participants, student_class, suspicious, maximum, student_name):
    result = print_on_language(1, 22) + ': '
    result = result + print_on_language(1, 26).lower() + ' ' + print_on_language(2, 23) + ' ' + student_class
    if suspicious != 0:
        result = result + '\n' + print_on_language(1, 24) + ' ' + maximum[0] + ' ' + \
                 print_on_language(2, 24) + ' ' + str(maximum[1]) + ' ' + print_on_language(3, 24)
    result = result + '\n' + print_on_language(1, 27) + ' ' + str(len(participants) + 1) + ' ' + \
        print_on_language(2, 27) + ':' + '\n' + student_name + '\n' + '\n'.join(participants)
    return result


def is_personal_incident(student_name, student_class):
    result = print_on_language(1, 28) + ': '
    result = result + print_on_language(1, 29).lower() + ' ' + student_class + ' ' + \
        print_on_language(2, 29) + ' ' + student_name + '\n' + print_on_language(3, 29)
    return result
