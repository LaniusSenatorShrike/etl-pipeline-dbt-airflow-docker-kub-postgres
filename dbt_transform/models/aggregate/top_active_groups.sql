{{ config(
    materialized = 'materialized_view',
    on_configuration_change = 'apply'
    )
}}

SELECT
    g.name AS group_name,
    COUNT(e.event_id) AS event_count
FROM
    public_agg.agg_events e
JOIN
    public_agg.agg_groups g ON e.group_id = g.group_id
WHERE
    e.time >= '2010-08-01 07:00:00'
GROUP BY
    g.name
ORDER BY
    event_count DESC
LIMIT 5;
