{{ config(
    materialized='incremental',
    unique_key='venue_id',
    on_schema_change='append_new_columns'
    )
}}

WITH raw_data AS (
    SELECT      *
    FROM        ({{raw_data_layer('venues')}}) AS base_table
)
SELECT      venue_id,
            name,
            city,
            country,
            lat,
            lon
FROM        raw_data



