-- job details for Flink Cluster
INSERT INTO 
  joined_yellow_taxi
SELECT 
  `tpep_pickup_datetime`, `trip_distance`, `PULocationID`, `LocationID`, `Zone`, `Borough` 
FROM 
  yellow_taxi AS y
LEFT JOIN 
  zones AS z
ON
y.PULocationID = z.LocationID;