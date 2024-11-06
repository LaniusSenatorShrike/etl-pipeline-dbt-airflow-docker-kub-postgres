import re

from utils.data_transform import DataTransformer
from utils.constants import C
from utils.database_engine_connection import DatabaseEngineConnection
from utils.file_handler import FileHandler
from utils.logger import get_logger, setup_logging

# Setup logging
setup_logging()

# Get a logger for this module
logger = get_logger(__name__)


def main():
    """
    main function to start data processing and ingestion
    """
    file_handler = FileHandler()
    transformer = DataTransformer()
    ingest_data = DatabaseEngineConnection().ingest_data

    logger.info("Checking source bucket contents")
    contents = file_handler.get_contents(C.SOURCE_BUCKET)

    for file in contents:
        filename = re.sub(r"\.json$", "", file)
        try:
            logger.info(f"Bucket and file validation initiated for {file}")
            file_handler.validate_bucket_and_file(C.SOURCE_BUCKET, file)

            logger.info(f"Processing initiated for {file}")
            file_handler.move_file(C.SOURCE_BUCKET, C.PROCESSING_BUCKET, file)

            data = transformer.read_data(file)
            data = transformer.clean_column_names(data)
            std_data = transformer.standardize_date(data)
            handled_std_data = transformer.handle_missing_and_duplicates(std_data)

            primary_key = C.PK.get(filename)
            foreign_keys = C.FK.get(filename, [])

            # if primary key dict is not empty
            if primary_key:
                logger.info(
                    f"Applying relational schema for {file} with primary key {primary_key} and foreign keys {foreign_keys}"
                )
                # Check and print the schema information with transformer.check_relational_schema
                handled_std_data_idx = transformer.create_relational_schema(handled_std_data, primary_key, foreign_keys)
            else:
                logger.info(f"No primary key found for {file}")
                handled_std_data_idx = handled_std_data

            # checking the connection
            logger.info(f"Ingesting data into table: {filename}")
            ingest_data(filename, handled_std_data_idx)

            file_handler.move_file(C.PROCESSING_BUCKET, C.SUCCESS_BUCKET, file)
            logger.info(f"Processing ended for {file}")

        except Exception as e:
            logger.error(f"File moved to failed bucket due to error: {e}")
            file_handler.move_file(C.PROCESSING_BUCKET, C.FAILED_BUCKET, file)


if __name__ == "__main__":
    main()
