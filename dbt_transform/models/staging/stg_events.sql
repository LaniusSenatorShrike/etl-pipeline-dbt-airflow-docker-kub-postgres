
WITH events_dedup AS (
    SELECT *
    FROM ({{ remove_duplicates('raw_events', 'event_id') }}) as base_dedup
)
SELECT  group_id,
        name,
        {{ convert_unix_timestamp('created') }} AS created_datetime,
        {{ convert_unix_timestamp('time') }} AS time,
        duration/3600 AS duration_hr,
        rsvp_limit,
        venue_id,
        status,
        event_id,
        rsvps,
        description
FROM    events_dedup