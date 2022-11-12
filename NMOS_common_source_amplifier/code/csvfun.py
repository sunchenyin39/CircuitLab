import pandas as pd
from pandas import DataFrame
import numpy as np


def main():
    """This main function is a test of data_to_csv function.
    """
    a = [1, 2, 3, 4, 5, 6]
    b = [7, 8, 9, 10, 11, 12]
    c = [1, 2, 3, 4, 5, 6]
    # set the data of a and b to row
    frequence_array = np.array(a)[:, np.newaxis]
    amplitude_array = np.array(b)[:, np.newaxis]
    time_array = np.array(c)[:, np.newaxis]

    # put the frequence_array and amplitude_array together
    concatenate_array = np.concatenate(
        (frequence_array, amplitude_array), axis=1)
    concatenate_array = np.concatenate(
        (concatenate_array, time_array), axis=1)

    data = DataFrame(concatenate_array, columns=[
                     "frequence", "amplitude", "time"])
    data.to_csv("test.csv", index=None)


def data_to_csv(csv_file_name, data_name_list, data_list_list):
    """The function converting list[list[float]] to csv file.

    Args:
        csv_file_name (str): The name of output csv file.
        data_name_list (list[str]): Name list.
        data_list_list (list[list[float]]): Data list.
    """
    if len(data_name_list) != len(data_list_list):
        print("label number is unequal to the number of data list")
        return 0
    elif len(data_name_list) == 0:
        print("there is no data")
        return 0
    else:
        data = np.array(data_list_list[0])[:, np.newaxis]
        for i in range(len(data_name_list)):
            if i > 0:
                data_temp = np.array(data_list_list[i])[:, np.newaxis]
                data = np.concatenate((data, data_temp), axis=1)
        data = DataFrame(data, columns=data_name_list)
        data.to_csv(csv_file_name, index=None)
        return 0


if __name__ == '__main__':
    main()
