WITH users_dedup AS (
    SELECT *
    FROM ({{ remove_duplicates('raw_users', 'user_id') }}) as base_dedup
)
SELECT      user_id,
            city,
            country,
            hometown,
            memberships
FROM        users_dedup
