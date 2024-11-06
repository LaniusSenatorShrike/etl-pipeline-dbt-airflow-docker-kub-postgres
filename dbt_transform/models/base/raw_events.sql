{{ config(
    materialized='incremental',
    unique_key='event_id',
    on_schema_change='append_new_columns'
    )
}}

WITH raw_data AS (
    SELECT      *
    FROM        ({{raw_data_layer('events')}}) AS base_table
)
SELECT      group_id,
            name,
            created,
            -- converting 'NULL' string to real NULL and converting it to FLOAT for conversion in the next layer
            COALESCE(CASE WHEN time = 'NULL' THEN NULL ELSE CAST(time AS FLOAT) END, 0) AS time,
            COALESCE(CASE WHEN duration = 'NULL' THEN NULL ELSE CAST(duration AS FLOAT) END, 0) AS duration,
            COALESCE(CASE WHEN rsvp_limit = 'NULL' THEN NULL ELSE CAST(rsvp_limit AS FLOAT) END, 0) AS rsvp_limit,
            venue_id,
            status,
            rsvps,
            {{ dbt_utils.generate_surrogate_key(['group_id', 'venue_id', 'time', 'name', 'created']) }} AS event_id,
            description
FROM        raw_data



