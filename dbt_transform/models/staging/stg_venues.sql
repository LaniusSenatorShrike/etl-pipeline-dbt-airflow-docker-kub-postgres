WITH venues_dedup AS (
    SELECT *
    FROM ({{ remove_duplicates('raw_venues', 'venue_id') }}) as base_dedup
)
SELECT      venue_id,
            name,
            city,
            country,
            lat,
            lon
FROM        venues_dedup
