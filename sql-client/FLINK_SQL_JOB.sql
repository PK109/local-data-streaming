-- job details for Flink Cluster
INSERT INTO 
  joined_yellow_taxi
SELECT 
    `tpep_pickup_datetime`
  , `tpep_dropoff_datetime`
  , `passenger_count`
  , `trip_distance`
  -- , `RatecodeID`
  -- , `store_and_fwd_flag`
  , `PULocationID`
  , zPU.`Zone` as `PUZone`
  , zPU.`Borough` as `PUBorough`
  , `DOLocationID`
  , zDO.`Zone` as `DOZone`
  , zDO.`Borough` as `DOBorough`
  -- , `payment_type`
  -- , `fare_amount`
  -- , `extra`
  -- , `mta_tax`
  , `tip_amount`
  -- , `tolls_amount`
  -- , `improvement_surcharge`
  , `total_amount` 
  -- , `congestion_surcharge`
  -- , `Airport_fee`
FROM 
  yellow_taxi AS y
LEFT JOIN 
  zones AS zPU
ON
y.PULocationID = zPU.LocationID
LEFT JOIN 
  zones AS zDO
ON
y.DOLocationID = zDO.LocationID;