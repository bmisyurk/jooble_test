import csv


def parse_tsv(content):
    """Fuction returns key values from train file"""
    columns = next(content)
    first_line = next(content)
    code_element, *rest = first_line[1].split(',')
    len_elements = len(rest)
    return columns, first_line, \
        code_element, len_elements


def create_file_tsv(columns_content, code_element, len_elements):
    """Create a file with columns in test_proc file"""
    with open('test_proc.tsv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter="\t")
        content = [columns_content[0],
                   *("feature_{}_stand_{}".format(code_element, i) for i in range(len_elements)),
                   "max_feature_{}_index".format(code_element),
                   "max_feature_{}_abs_mean_diff".format(code_element)
                   ]
        writer.writerow(content)


def tsv_reader(filename):
    """"Read and returns file with content"""
    try:
        file = open(filename, 'r')
        content = csv.reader(file, delimiter="\t")
        return file, content
    except Exception as e:
        print(e)
