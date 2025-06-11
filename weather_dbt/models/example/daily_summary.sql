SELECT
  w.date,
  AVG(w.temp_c) AS avg_temp,
  AVG(w.humidity) AS avg_humidity,
  SUM(s.umbrellas) AS total_umbrellas,
  SUM(s.cold_drinks) AS total_cold_drinks
FROM weather_data w
JOIN sales_data s ON w.date = s.date
GROUP BY w.date
