
SELECT COLUMN_NAME,
DATA_TYPE, ORDINAL_POSITION
FROM information_schema.columns
WHERE table_name = 'products'