{{ config(
    materialized = 'materialized_view',
    on_configuration_change = 'apply'
    )
}}

SELECT
    e.event_id,
    e.name,
    COUNT(*) AS rsvp_count
FROM
    public_agg.agg_events e
JOIN
    LATERAL jsonb_array_elements(e.rsvps::jsonb) AS r ON TRUE
WHERE
    (r ->> 'response')::text = 'yes' AND event_id is NOT NULL -- I witnesses some null event_ids as a result of aggregation
     AND status = 'upcoming'
GROUP BY
    e.event_id, e.name
HAVING
    COUNT(*) > 100  -- Adjust threshold for "high" RSVPs
ORDER BY
    rsvp_count DESC