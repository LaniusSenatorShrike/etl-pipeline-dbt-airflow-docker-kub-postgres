{% macro convert_unix_timestamp(epoch_ms) %}
-- Unix epoch start date January 1, 1970, at 00:00:00 UTC.
  (TIMESTAMP 'epoch' + {{ epoch_ms }} / 1000 * INTERVAL '1 second')
{% endmacro %}
