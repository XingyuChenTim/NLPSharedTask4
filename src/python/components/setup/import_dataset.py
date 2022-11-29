import traceback
import pandas as pd
import json


class MissingColumnError(AttributeError):
    """Error indicating that an imported DataFrame lacks necessary columns"""
    pass


def load_json_file(filepath):
    """Load content of json-file from `filepath`"""
    with open(filepath, 'r') as  json_file:
        return json.load(json_file)


def load_values_from_json(filepath):
    """Load values per level from json-file from `filepath`"""
    json_values = load_json_file(filepath)
    values = {"2":set() }
    for key in json_values.keys():
        values["2"].add(key)
    values["2"] = sorted(values["2"])
    return values


def load_arguments_from_tsv(filepath, default_usage='test'):
    """
        Reads arguments from tsv file

        Parameters
        ----------
        filepath : str
            The path to the tsv file
        default_usage : str, optional
            The default value if the column "Usage" is missing

        Returns
        -------
        pd.DataFrame
            the DataFrame with all arguments

        Raises
        ------
        MissingColumnError
            if the required columns "Argument ID" or "Premise" are missing in the read data
        IOError
            if the file can't be read
        """
    try:
        dataframe = pd.read_csv(filepath, encoding='utf-8', sep='\t', header=0)
        if not {'Argument ID', 'Premise'}.issubset(set(dataframe.columns.values)):
            raise MissingColumnError('The argument "%s" file does not contain the minimum required columns [Argument ID, Premise].' % filepath)
        if 'Usage' not in dataframe.columns.values:
            dataframe['Usage'] = [default_usage] * len(dataframe)
        return dataframe
    except IOError:
        traceback.print_exc()
        raise


def load_labels_from_tsv(filepath, label_order):
    """
        Reads label annotations from tsv file

        Parameters
        ----------
        filepath : str
            The path to the tsv file
        label_order : list[str]
            The listing and order of the labels to use from the read data

        Returns
        -------
        pd.DataFrame
            the DataFrame with the annotations

        Raises
        ------
        MissingColumnError
            if the required columns "Argument ID" or names from `label_order` are missing in the read data
        IOError
            if the file can't be read
        """
    try:
        dataframe = pd.read_csv(filepath, encoding='utf-8', sep='\t', header=0)
        dataframe = dataframe[['Argument ID'] + label_order]
        return dataframe
    except IOError:
        traceback.print_exc()
        raise
    except KeyError:
        raise MissingColumnError('The file "%s" does not contain the required columns for its level.' % filepath)
