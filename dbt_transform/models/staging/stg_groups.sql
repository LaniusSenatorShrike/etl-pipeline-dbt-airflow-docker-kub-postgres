WITH groups_dedup AS (
    SELECT *
    FROM ({{ remove_duplicates('raw_groups', 'group_id') }}) as base_dedup
)
SELECT  group_id,
        city,
        name,
        lat,
        lon,
        link,
        topics,
        description,
        {{ convert_unix_timestamp('"created"') }} AS created_datetime
FROM    groups_dedup

