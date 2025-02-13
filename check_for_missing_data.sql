WITH missing_data AS (
    SELECT 
        COUNT(*) AS total_rows,
        COUNTIF(player_id IS NULL OR player_id = '') AS missing_player_id,
        COUNTIF(session_id IS NULL OR session_id = '') AS missing_session_id,
        COUNTIF(date IS NULL) AS missing_date,
        COUNTIF(session_length IS NULL) AS missing_session_length,
        COUNTIF(session_count IS NULL) AS missing_session_count,
        COUNTIF(retention_day IS NULL) AS missing_retention_day,
        COUNTIF(churned IS NULL) AS missing_churned,
        COUNTIF(in_game_purchases IS NULL) AS missing_in_game_purchases,
        COUNTIF(ad_revenue IS NULL) AS missing_ad_revenue,
        COUNTIF(crashes IS NULL) AS missing_crashes,
        COUNTIF(frame_rate IS NULL) AS missing_frame_rate,
        COUNTIF(acquisition_source IS NULL OR acquisition_source = '') AS missing_acquisition_source,
        COUNTIF(cpi IS NULL) AS missing_cpi,
        COUNTIF(roas IS NULL) AS missing_roas
    FROM game_analytics_sql.game_analytics_table
)
SELECT 
    column_name,
    missing_values,
    ROUND((missing_values / total_rows) * 100, 2) AS missing_percentage
FROM missing_data,
  UNNEST([
    STRUCT('player_id' AS column_name, missing_player_id AS missing_values),
    STRUCT('session_id' AS column_name, missing_session_id AS missing_values),
    STRUCT('date' AS column_name, missing_date AS missing_values),
    STRUCT('session_length' AS column_name, missing_session_length AS missing_values),
    STRUCT('session_count' AS column_name, missing_session_count AS missing_values),
    STRUCT('retention_day' AS column_name, missing_retention_day AS missing_values),
    STRUCT('churned' AS column_name, missing_churned AS missing_values),
    STRUCT('in_game_purchases' AS column_name, missing_in_game_purchases AS missing_values),
    STRUCT('ad_revenue' AS column_name, missing_ad_revenue AS missing_values),
    STRUCT('crashes' AS column_name, missing_crashes AS missing_values),
    STRUCT('frame_rate' AS column_name, missing_frame_rate AS missing_values),
    STRUCT('acquisition_source' AS column_name, missing_acquisition_source AS missing_values),
    STRUCT('cpi' AS column_name, missing_cpi AS missing_values),
    STRUCT('roas' AS column_name, missing_roas AS missing_values)
  ]) AS unpivoted_data
ORDER BY missing_values DESC;
