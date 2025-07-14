-- App Annie App Ratings SQL Template
-- Replace the date values when pasting your SQL from Google Sheets:
-- WHERE month BETWEEN "{{start_date}}" AND "{{end_date}}"

-- Paste your SQL content below this line: 


SELECT	
date,	
store,	
app_id,	
country_code,	
brand,	
CASE rating	
WHEN '1' THEN 'One'	
WHEN '2' THEN 'Two'	
WHEN '3' THEN 'Three'	
WHEN '4' THEN 'Four'	
WHEN '5' THEN 'Five'	
END AS rating,	
total_count	
FROM (	
SELECT	
date,	
store,	
app_id,	
country_code,	
brand,	
one AS total_count, 
'1' AS rating
FROM `wego-cloud.appannie.app_ratings_over_time*`	
WHERE _TABLE_SUFFIX BETWEEN "{{start_date}}" AND "{{end_date}}"
UNION ALL	
	
SELECT	
date,	
store,	
app_id,	
country_code,	
brand,	
two AS total_count,	
'2' AS rating	
FROM `wego-cloud.appannie.app_ratings_over_time*`	
WHERE _TABLE_SUFFIX BETWEEN "{{start_date}}" AND "{{end_date}}"
	
UNION ALL	
	
SELECT	
date,	
store,	
app_id,	
country_code,	
brand,	
three AS total_count,	
'3' AS rating	
FROM `wego-cloud.appannie.app_ratings_over_time*`	
WHERE _TABLE_SUFFIX BETWEEN "{{start_date}}" AND "{{end_date}}"	
	
UNION ALL	
	
SELECT	
date,	
store,	
app_id,	
country_code,	
brand,	
four AS total_count,	
'4' AS rating	
FROM `wego-cloud.appannie.app_ratings_over_time*`	
WHERE _TABLE_SUFFIX BETWEEN "{{start_date}}" AND "{{end_date}}"
	
UNION ALL	
	
SELECT	
date,	
store,	
app_id,	
country_code,	
brand,	
five AS total_count,	
'5' AS rating	
FROM `wego-cloud.appannie.app_ratings_over_time*`	
WHERE _TABLE_SUFFIX BETWEEN "{{start_date}}" AND "{{end_date}}"
)	
ORDER BY date, brand, rating;	
	