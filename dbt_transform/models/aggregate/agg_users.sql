{{ config(
    materialized='incremental',
    unique_key='user_id',
    on_schema_change='append_new_columns',
    cluster_by = "user_id"
    )
}}

SELECT  user_id,
        city,
        country,
        hometown,
        memberships
FROM    {{ ref("stg_users") }}