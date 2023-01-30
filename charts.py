import matplotlib.pyplot as plt
import pandas
import seaborn as sns
from strings import print_on_language
from calculations import read_from_configuration

list_incidents, causes, parallel, name_columns, language_texts, previous_causes = [], [], [], [], [], []


def set_variables(example_list_incidents, example_causes, example_parallel, example_name_columns,
                  example_previous_causes):
    global list_incidents, causes, parallel, name_columns, previous_causes
    name_columns = example_name_columns
    list_incidents, causes, parallel, = example_list_incidents, example_causes, example_parallel
    previous_causes = example_previous_causes


def chart_selection(choice_graph, data):
    plt.close('all')
    if choice_graph == 0:
        chart_number_of_incidents_to_students(data)
    elif choice_graph == 1:
        chart_incidents_on_parallel(data)
    elif choice_graph == 2:
        correlation_chart(data)
    elif choice_graph == 3:
        chart_boxplot(data)


def chart_number_of_incidents_to_students(data):
    plt.hist(causes, bins=2, label=print_on_language(1, 12) + ' / ' + print_on_language(1, 13) + ', %: ' + str(
        round((len(list_incidents) / data.shape[0] * 100), 3)))
    plt.xlabel(print_on_language(1, 12))
    plt.ylabel(print_on_language(1, 13))
    plt.locator_params(axis='y', nbins=10)
    plt.locator_params(axis='x', nbins=2)
    plt.legend()
    plt.show()


def chart_incidents_on_parallel(data):
    causes_df = data[[4] + [2]]
    causes_df.groupby(2).sum().plot(kind='bar', rot=0)
    plt.xlabel(print_on_language(1, 17))
    plt.ylabel(print_on_language(1, 12))
    plt.locator_params(axis='y', nbins=max(causes_df) + 1)
    plt.locator_params(axis='x', nbins=max(parallel) + 1)
    plt.legend([], loc='upper right', title=print_on_language(1, 16) + ': ' + str(len(list_incidents)))
    plt.show()


def correlation_chart(data):
    name_index = int(read_from_configuration(1)) - 1
    sex_index = int(read_from_configuration(2)) - 1
    parallel_index = int(read_from_configuration(3)) - 1
    letter_index = int(read_from_configuration(4)) - 1
    incidents_index = int(read_from_configuration(5)) - 1
    time_index = int(read_from_configuration(6)) - 1
    previous_causes_index = int(read_from_configuration(7)) - 1
    sns.heatmap(data.drop([name_index, sex_index, letter_index], axis=1).corr(method='pearson', min_periods=1,
                                                                              numeric_only=False),
                linewidths=0.1, annot=True)
    plt.legend([], loc='upper right',
               title=str(parallel_index) + ' - ' + str(name_columns[parallel_index]) + '\n' +
                       str(incidents_index) + ' - ' + str(name_columns[incidents_index]) + '\n' +
                       str(time_index) + ' - ' + str(name_columns[time_index]) + '\n' +
                       str(previous_causes_index) + ' - ' + str(name_columns[previous_causes_index]))
    plt.show()


def chart_boxplot(data):
    global previous_causes, parallel
    previous_causes_index = int(read_from_configuration(7)) - 1
    parallel_index = int(read_from_configuration(3)) - 1
    previous_causes = pandas.Index(previous_causes)
    incident_count = previous_causes.value_counts().sort_values(ascending=False).index.values
    sns.boxplot(y=previous_causes, x=parallel, data=data[previous_causes.isin(incident_count)], orient="h")
    plt.locator_params(axis='x', nbins=max(parallel) + 1)
    plt.legend([], loc='upper right',
               title=str(parallel_index) + ' - ' + str(name_columns[parallel_index]) + '\n' +
                       str(previous_causes_index) + ' - ' + str(name_columns[previous_causes_index]))
    plt.show()
