import csv
import io

try:
    import simplejson as json
except ImportError:
    import json


def is_leaf(data):
    return not isinstance(data, (list, dict))


def flatten(data, headers=None, values=None, parent_header=None):
    """

    :param data: dict or list to flatten into a single list containing no sub dicts or lists
    :param headers: list of header values
    :param values: list of values
    :param parent_header: string to be used when a value has no corresponding header
    :return: flattened list
    """
    if values is None:
        values = []
    if headers is None:
        headers = []

    if isinstance(data, list):
        for val in data:
            if is_leaf(val):
                headers.append(parent_header)
                values.append(val)
            else:
                flatten(val, headers, values, parent_header)
    else:
        keys = data.keys()
        for key in keys:
            if is_leaf(data[key]):
                headers.append(key)
                values.append(data[key])
            else:
                flatten(data[key], headers, values, key)

    return headers, values


def to_csv(data):
    """
    Takes a list of dicts or lists and flattens them,
    then saves them to a memory-file BytesIO object in an excel csv format.

    :param data: list of data items to be flattened and then saved in csv format
    :return: BytesIO file object
    """
    temp_file = io.StringIO(newline='')
    csv_writer = csv.writer(temp_file)

    if len(data) <= 0:
        csv_writer.writerow([])
        return temp_file.seek(0)

    headers, flattened_value = flatten(data[0])
    csv_writer.writerow(headers)

    for value in data:
        headers, flattened_value = flatten(value)
        csv_writer.writerow(flattened_value)

    temp_file.seek(0)
    return temp_file
