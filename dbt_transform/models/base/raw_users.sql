{{ config(
    materialized='incremental',
    unique_key='user_id',
    on_schema_change='append_new_columns'
    )
}}

WITH raw_data AS (
    SELECT      *
    FROM        ({{raw_data_layer('users')}}) AS base_table
)
SELECT      user_id,
            city,
            country,
            hometown,
            memberships
FROM        raw_data
