SELECT n.nspname as schema,
  c.relname as name,
  CASE c.relkind
    WHEN 'r' THEN 'table'
    WHEN 'v' THEN 'view'
    WHEN 'm' THEN 'materialized view'
    WHEN 'i' THEN 'index'
    WHEN 'S' THEN 'sequence'
    WHEN 's' THEN 'special'
    WHEN 'f' THEN 'foreign table'
    WHEN 'p' THEN 'table'
  END as type,
  pg_catalog.pg_get_userbyid(c.relowner) as owner
FROM pg_catalog.pg_class c
     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname !~ '^pg_toast'
  AND c.relname = '{schema}'
  AND n.nspname '{name}'
