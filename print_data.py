from strings import print_on_language


def print_list_incidents(example_list_incidents):
    return [str(i + 1) + ') ' + str(example_list_incidents[i][0]) + ' ' + str(example_list_incidents[i][2])
            for i in range(len(example_list_incidents))]


def print_selection_list(example_list):
    return [str(i + 1) + ') ' + example_list[i] for i in range(len(example_list))]


def full_information(is_fight, in_class, participants, student_class, suspicious, maximum, student_name,
                     count_last_incidents, incident_time=0):
    student_result, incident_result = str(), str()
    student_result = student_result + print_on_language(1, 36) + ': ' + str(student_name) + '\n'
    student_result = student_result + print_on_language(1, 63) + ': ' + str(student_class) + '\n'
    student_result = student_result + print_on_language(1, 40) + ': ' + str(count_last_incidents) + '\n'
    incident_result = incident_result + print_on_language(1, 64) + ': ' + (print_on_language(1, 67)
                                                                           if in_class
                                                                           else print_on_language(1, 68)) + '\n'
    incident_result = incident_result + print_on_language(1, 28) + ': ' + (print_on_language(1, 67)
                                                                           if not in_class and not is_fight
                                                                           else print_on_language(1, 68)) + '\n'
    incident_result = incident_result + print_on_language(1, 23) + ': ' + (print_on_language(1, 67) if is_fight
                                                                           else print_on_language(1, 68)) + '\n'
    if incident_time:
        incident_result = incident_result + print_on_language(1, 39) + ': ' + \
                          ':'.join([str(incident_time)[i:i + 2] for i in range(0, len(str(incident_time)), 2)]) + '\n'
    if len(participants) != 0:
        incident_result = incident_result + print_on_language(1, 27) + ' ' + str(len(participants) + 1) + ' ' + \
                          print_on_language(2, 27) + ':' + '\n'
        for i in range(len(participants)):
            incident_result = incident_result + participants[i][0] + ' ' + participants[i][1] + '\n'
    if suspicious:
        incident_result = incident_result + '\n' + print_on_language(1, 24) + ' ' + str(maximum[0]) + ' ' + \
                          ', ' + print_on_language(2, 24) + '\n' + str(maximum[1]) + ' ' + print_on_language(3,
                                                                                                             24) + '\n'
    return student_result, incident_result
