import matplotlib.pyplot as plt
from print_data import print_on_language
import seaborn as sns


def graph_1(data, causes, example_list_incidents):
    plt.hist(causes, bins=2, label=print_on_language(1, 12) + ' / ' + print_on_language(1, 13) + ', %: ' + str(
        round((len(example_list_incidents) / data.shape[0] * 100), 3)))
    plt.xlabel(print_on_language(1, 12))
    plt.ylabel(print_on_language(1, 13))
    plt.locator_params(axis='y', nbins=10)
    plt.locator_params(axis='x', nbins=2)
    plt.legend()
    plt.show()


def graph_2(data, example_list_incidents, parallel):
    causes_df = data[[4] + [2]]
    causes_df.groupby(2).sum().plot(kind='bar', rot=0)
    plt.xlabel(print_on_language(1, 17))
    plt.ylabel(print_on_language(1, 12))
    plt.locator_params(axis='y', nbins=max(causes_df) + 1)
    plt.locator_params(axis='x', nbins=max(parallel) + 1)
    plt.legend([], loc='upper right', title=print_on_language(1, 16) + ': ' + str(len(example_list_incidents)))
    plt.show()


def graph_3(data, name_columns):
    sns.heatmap(data.drop([0, 1, 3, 5], axis=1).corr(method='pearson', min_periods=1, numeric_only=False),
                linewidths=0.1, annot=True)
    plt.legend([], loc='upper right',
               title='2 - ' + str(name_columns[2]) + '\n4 - ' + str(name_columns[4]) +
                     '\n6 - ' + str(name_columns[5]) + '\n7 - ' + str(name_columns[6]))
    plt.show()
