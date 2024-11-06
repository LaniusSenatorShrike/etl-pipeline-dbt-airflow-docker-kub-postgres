{{ config(
    materialized='incremental',
    unique_key='venue_id',
    on_schema_change='append_new_columns',
    cluster_by = "venue_id"
    )
}}

SELECT  venue_id,
        name,
        city,
        country,
        lat,
        lon
FROM    {{ ref("stg_venues") }}