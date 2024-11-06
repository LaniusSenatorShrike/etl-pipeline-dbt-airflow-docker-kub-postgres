{{ config(
    materialized='incremental',
    unique_key='group_id',
    on_schema_change='append_new_columns'
    )
}}

WITH raw_data AS (
    SELECT      *
    FROM        ({{raw_data_layer('groups')}}) AS base_table
)
SELECT  group_id,
        city,
        name,
        lat,
        lon,
        link,
        topics,
        description,
        created
FROM    raw_data
