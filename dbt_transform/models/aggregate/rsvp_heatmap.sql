{{ config(
    materialized = 'materialized_view',
    on_configuration_change = 'apply'
    )
}}

SELECT 		TO_CHAR(to_timestamp((r ->> 'when')::bigint / 1000), 'Day') AS day_of_week,
    		EXTRACT(HOUR FROM to_timestamp((r ->> 'when')::bigint / 1000)) AS hour_of_day,
    		COUNT(*) AS rsvp_count
FROM 		public_agg.agg_events e
JOIN 		LATERAL jsonb_array_elements(e.rsvps::jsonb) AS r ON TRUE
WHERE 		(r ->> 'response')::text = 'yes'
GROUP BY 	day_of_week, hour_of_day
ORDER BY 	day_of_week, hour_of_day