{{ config(
    materialized='incremental',
    unique_key='event_id',
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
        name,
        created_datetime,
        time,
        duration_hr,
        rsvp_limit,
        venue_id,
        status,
        event_id,
        rsvps,
        description
FROM    {{ ref("stg_events") }}


