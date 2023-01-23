def error(message, exit_message):
    print('\033[91mError! \033[0m' + message)
    if exit_message != 0:
        exit(exit_message)


def warning(message):
    print('\033[93mWarning! \033[0m' + message)
