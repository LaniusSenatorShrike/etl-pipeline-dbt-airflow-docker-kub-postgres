import pandas as pd
import json

from utils.constants import C


class DataTransformer:
    def __init__(self):
        pass

    def read_data(self, file_name):
        """
        Reads a file into a pandas DataFrame.

        :param file_path: Path to the CSV file
        :return: DataFrame containing the CSV data
        """
        file_path = f"{C.BASE_PATH}/{C.PROCESSING_BUCKET}/{file_name}"
        return pd.read_json(file_path)

    def clean_column_names(self, data):
        """
        Replaces spaces and () in column names with underscores and converts them to lowercase.

        :param data: Input data as a pandas DataFrame
        :return: DataFrame with cleaned column names
        """
        data.columns = data.columns.str.replace(" ", "_").str.replace("(", "").str.replace(")", "").str.lower()

        return data

    def standardize_date(self, data):
        """
        Automatically detects columns with date-like values and standardizes the formats.

        :param data: Input data as a pandas DataFrame
        :return: DataFrame with standardized date columns
        """
        for column in data.columns:
            if "date" in column.lower() or "create" in column.lower():  # Check if 'date/create' is in the column name (case-insensitive)
                try:
                    # Try to convert the column to datetime format
                    data[column] = pd.to_datetime(data[column], format="%m/%d/%y %H:%M", errors="raise")
                except (ValueError, TypeError):
                    # If conversion fails, skip the column and leave it unchanged
                    pass

        return data

    def handle_missing_and_duplicates(self, data):
        """
        Handles missing and duplicate records.

        - Fills missing values
        - Removes duplicate records

        :param data: Input data as a pandas DataFrame
        :return: Cleaned DataFrame
        """

        # Filling missing values with forward fill
        data = data.fillna("NULL")

        # drop_duplicates() can't operate on DataFrame that contains "list" and "dictionary"
        # that's bc they're= not hashable. Also changing dict > fronzset doesn't work as postgres can't handle frozenset
        # Solution: Convert lists and dictionaries to JSON strings
        def convert_values(value):
            if isinstance(value, (list, dict)):
                return json.dumps(value)  # Convert lists and dicts to JSON strings
            return value

        data = data.map(convert_values)

        # Removing duplicate records
        data = data.drop_duplicates()

        return data

    def create_relational_schema(self, data, primary_key, foreign_keys):
        """
        Establishes primary and foreign keys in the DataFrame.

        :param data: Input data as a pandas DataFrame
        :param primary_key: Column to be set as the primary key
        :param foreign_keys: List of columns to be set as foreign keys
        :return: DataFrame with primary and foreign keys
        """
        # Set the primary key
        # normally, after indexing a column its dropped bc it's not a column anymore, its an index
        # drop = False is being used to avoid dropping column while indexing it.
        # if it's removed, the indexed column is not ingested bc it's an index and not a column anymore
        data.set_index(primary_key, drop=False, inplace=True)

        # Store the primary key and foreign keys in a dictionary in _metadata
        data._metadata = {"primary_key": primary_key, "foreign_keys": foreign_keys}

        return data

    def check_relational_schema(self, data):
        """
        Check the primary and foreign keys for the given DataFrame.

        :param data: Input data as a pandas DataFrame
        :return: Dictionary with primary key and foreign keys
        """
        # Retrieve the primary key and foreign keys from _metadata
        primary_key = data._metadata.get("primary_key", None)
        foreign_keys = data._metadata.get("foreign_keys", [])

        # Print or return the relational schema information
        schema_info = {"Primary Key": primary_key, "Foreign Keys": foreign_keys}

        return schema_info

