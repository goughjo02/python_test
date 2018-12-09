"""Funtion to apply transformations from mapping.csv."""
import csv
from numpy import genfromtxt, int64, zeros, append as np_append, delete as np_delete


class Mapper:
    """Class to perform mapping transformation as described in a csv."""

    def __init__(self, path_to_csv):
        """Constructor."""
        self.mappings = []
        with open(path_to_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for i in csv_reader:
                # Do nothing with the header
                if csv_reader.line_num == 1:
                    continue
                # grab the four variables
                pre_transform = i[0]
                post_transform = i[1]
                source_types = i[2].split('|')
                destination_type = i[3]
                # check if the source destination already has mapping transformations
                if(source_types not in [e["sources"] for e in self.mappings]):
                    # if not add a new mapping
                    self.mappings.append({
                        "sources": source_types,
                        "destination": destination_type,
                        "transforms": [{
                            "source": pre_transform,
                            "destination": post_transform
                        }]
                    })
                else:
                    # Else add to transformations of an existing mapping
                    for e in self.mappings:
                        if (source_types == e["sources"]):
                            e["transforms"].append({
                                "source": pre_transform,
                                "destination": post_transform
                            })

    def translate_string(self, string):
        """Function to assist in translating country codes."""
        if string == 'EU':
            return 'European Size '
        elif string == 'US':
            return 'United States Size'
        else:
            return string

    def delete_empty_columns(self, nd_array):
        """Function to delete columns with empty values."""
        indexes = []
        for (num, item) in enumerate(nd_array[1, :]):
            if item == "":
                indexes.append(num)
        return np_delete(nd_array, indexes, 1)

    def perform_mapping(self, path_to_target_file):
        """Perform the mappings."""
        result = genfromtxt(path_to_target_file,
                            delimiter=';',
                            dtype=None, encoding="utf8")
        result = self.delete_empty_columns(result)
        column_list = result[0, :].tolist()
        # Apply each of the mappings
        for i in self.mappings:
            # If there is only one source column
            if (len(i["sources"]) == 1):
                # Get the index of the target column
                source_str = i["sources"][0]
                index_of_column = column_list.index(source_str)
                # for each for of the nd_array
                for (num, obj) in enumerate(result):
                    # change header
                    if num == 0:
                        result[num, index_of_column] = i["destination"]
                    # change value
                    else:
                        desired_transforms = i["transforms"]
                        for transform in desired_transforms:
                            if transform["source"] == result[num, index_of_column]:
                                result[num, index_of_column] = transform["destination"]
                                continue
            # If there are multiple source columns to be combined
            elif (len(i["sources"]) > 1):
                source_strings = i["sources"]
                indexes_of_column = [column_list.index(e) for e in source_strings]
                height, width = result.shape
                z = zeros((height, 1), dtype=int64)
                result = np_append(result, z, axis=1)
                # for each for of the nd_array
                for (num, obj) in enumerate(result):
                    # change header
                    if num == 0:
                        result[0, -1] = i["destination"]
                    # change value
                    else:
                        desired_transforms = i["transforms"]
                        for transform in desired_transforms:
                            new_value = ""
                            for index in indexes_of_column:
                                new_value += self.translate_string(result[num, index])
                            result[num, -1] = new_value
                result = np_delete(result, indexes_of_column, 1)
        return result
