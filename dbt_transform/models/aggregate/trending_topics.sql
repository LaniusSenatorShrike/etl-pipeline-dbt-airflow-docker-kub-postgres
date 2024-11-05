{{ config(
    materialized = 'materialized_view',
    on_configuration_change = 'apply'
    )
}}

WITH high_rsvp_events AS (
    SELECT
        e.event_id,
        e.group_id,
        COUNT(*) AS rsvp_count
    FROM
        public_agg.agg_events e
    JOIN
        LATERAL jsonb_array_elements(e.rsvps::jsonb) AS r ON TRUE
    WHERE
        (r ->> 'response')::text = 'yes' AND event_id is NOT NULL -- I witnesses some null event_ids as a result of aggregation
	GROUP BY
        e.event_id, e.group_id
    HAVING
        COUNT(*) > 100  -- Adjust threshold for "high" RSVPs
	ORDER BY
		rsvp_count DESC
	LIMIT 20
),
group_topics AS (
    SELECT
        g.group_id,
        jsonb_array_elements(g.topics::jsonb) AS topic
    FROM
        public_agg.agg_groups g
)
SELECT		gt.topic as top_topics,
			COUNT(*) as topic_cnt
FROM 		high_rsvp_events hre
INNER JOIN	group_topics gt ON hre.group_id = gt.group_id
GROUP BY	1
ORDER BY	2 DESC
LIMIT 		10
