{{ config(
    materialized='incremental',
    unique_key='group_id',
    on_schema_change='append_new_columns',
    partition_by={
          "field": "created_datetime",
          "data_type": "timestamp",
          "granularity": "day"
    },
    partition_expiration_days = 14,
    cluster_by = "group_id"
    )
}}

SELECT  group_id,
        city,
        name,
        lat,
        lon,
        link,
        topics,
        description,
        created_datetime
FROM    {{ ref("stg_groups") }}
