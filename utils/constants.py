from dataclasses import dataclass
from urllib.parse import quote_plus


@dataclass(frozen=True)
class Constants:
    # buckets path
    SOURCE_BUCKET: str = "buckets/source"
    SUCCESS_BUCKET: str = "buckets/success"
    FAILED_BUCKET: str = "buckets/failed"
    PROCESSING_BUCKET: str = "buckets/processing"
    BASE_PATH: str = "/home/lanius/PythonProjects/etl-pipeline-dbt-airflow-docker-kub-postgres"

    # primary keys
    PK = {
        "groups": "group_id",
        "users": "user_id",
        "venues": "venue_id",
    }

    # foreign keys
    FK = {
        "users": "group_id",
        "events": ["group_id","venue_id","user_id"],
    }

    # postgres server
    TYPE: str = "postgres"
    HOST: str = "localhost"
    USER: str = "postgres"
    PASSWORD: str = quote_plus("Pp@639493")
    PORT: str = "5432"
    DBNAME: str = "DWH"
    SCHEMA: str = "public"

C = Constants()
