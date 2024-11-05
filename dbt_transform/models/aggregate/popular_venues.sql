{{ config(
    materialized = 'materialized_view',
    on_configuration_change = 'apply'
    )
}}

WITH high_rsvp_events AS (
    SELECT
        e.event_id,
        e.venue_id,
        COUNT(*) AS rsvp_count
    FROM
        public_agg.agg_events e
    JOIN
        LATERAL jsonb_array_elements(e.rsvps::jsonb) AS r ON TRUE
    WHERE
        (r ->> 'response')::text = 'yes' AND event_id is NOT NULL -- I witnesses some null event_ids as a result of aggregation
    	-- AND group_id = 'Amsterdam-Python-Meetup-Group'
	GROUP BY
        e.event_id, e.venue_id
    HAVING
        COUNT(*) > 100  -- Adjust threshold for "high" RSVPs
	ORDER BY
		rsvp_count DESC
),
venue_rsvp_summary AS (
    SELECT
        hre.venue_id,
        ae.city,
        ae.name AS venue_name,
        ae.lat AS venue_lat,
        ae.lon AS venue_lon,
        SUM(hre.rsvp_count) AS total_rsvp_count,
        ROW_NUMBER() OVER (PARTITION BY ae.city ORDER BY SUM(hre.rsvp_count) DESC) AS venue_rank
    FROM
        high_rsvp_events hre
    INNER JOIN
        public_agg.agg_venues ae ON hre.venue_id = ae.venue_id
    GROUP BY
        hre.venue_id, ae.city, ae.name, ae.lat, ae.lon
)
SELECT
    city,
    venue_name,
    CAST(venue_lat AS FLOAT) AS latitude,
    CAST(venue_lon AS FLOAT) AS longitude,
    total_rsvp_count
FROM
    venue_rsvp_summary
WHERE
    venue_rank = 1
ORDER BY
	total_rsvp_count DESC, city