import operator
import time
from math import sqrt
from datetime import *
from processing_file import *


def separate_values(line):
    """Divides line in format [-97654323456787643, 9889, 9999, 9978, 9971, 9495, 9974, 9810, 9987..., N]"""
    return (int(line[0]), *(int(x) for x in line[1].split(',')[1:]))


def generate_rows(first_line, content):
    """Function returns expression generator iteratively and first line of file separately"""
    yield separate_values(first_line)
    try:
        for line in content:
            yield separate_values(line)
    except Exception as e:
        print(e)


def calc_z_score(mean, std, test_file):
    """Final processing, calculation Z-score index and write into test_proc.tsv file"""
    reader_file, content = tsv_reader(test_file)
    columns_content = next(content)
    first_line = next(content)
    values = generate_rows(first_line, content)
    with open('test_proc.tsv', 'a', newline='') as f:
        writer = csv.writer(f, delimiter="\t")
        try:
            for (N, row) in enumerate(values, start=1):
                scoring = map(lambda value, mean, std: (value - mean) / std, row[1:], mean, std)
                max_index, value = max(enumerate(row[1:]), key=operator.itemgetter(1))
                writer.writerow([row[0], *scoring, max_index, abs(value - mean[max_index])])
        except Exception as e:
            print(e)
    reader_file.close()


def mean_std_calc(content, len_elements):
    """"Calculation mean and standard deviation for {len_elements} columns"""
    summa = [0] * len_elements
    square_sum = [0] * len_elements
    try:
        for (N, row) in enumerate(content, start=1):
            summa = list(float(x) for x in map(lambda x, y: x + y, summa, row[1:]))
            # sum 256 columns of train's rows
            square_sum = list(float(x) for x in map(lambda x, y: x + (y ** 2), square_sum, row[1:]))
            # squaresum 256 columns of train's rows
        mean = list(element / N for element in summa)
        std = list(map(lambda square_sum_n, mean_n:
                       sqrt((square_sum_n - (N * (mean_n ** 2))) / (N - 1)), square_sum, mean))
        return mean, std
    except Exception as e:
        print(e)


def z_score(file_train, file_test):
    """"Main function, data preparation and their further processing Z-score index in subfunctions"""
    start_time = datetime.now()
    file_train, content = tsv_reader(file_train)
    columns_content, first_line, code_element, len_elements = parse_tsv(content)
    values = generate_rows(first_line, content)
    mean, std = mean_std_calc(values, len_elements)
    print("Mean_std calc. Time:", datetime.now() - start_time)
    file_train.close()
    create_file_tsv(columns_content, code_element, len_elements)
    calc_z_score(mean, std, file_test)
    print("End z-score calc. Time:", datetime.now() - start_time)
    print("Finished")


if __name__ == '__main__':
    z_score("testgen.tsv", "test.tsv")  # z_score(train_file, calculation_file)
