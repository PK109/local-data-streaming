-- job details for Flink Cluster

INSERT INTO joined_yellow_taxi
  SELECT 
      `VendorID`
    , `tpep_pickup_datetime` 
    , TO_TIMESTAMP_LTZ(tpep_pickup_datetime/1000, 3) as `tpep_pickup_ts`
    , `tpep_dropoff_datetime`
    , TO_TIMESTAMP_LTZ(tpep_dropoff_datetime/1000, 3) as `tpep_dropoff_ts`
    , `passenger_count`
    , `trip_distance`
    , `RatecodeID`
    , `store_and_fwd_flag`
    , `PULocationID`
    , zPU.`Zone` as `PUZone`
    , zPU.`Borough` as `PUBorough`
    , `DOLocationID`
    , zDO.`Zone` as `DOZone`
    , zDO.`Borough` as `DOBorough`
    , `payment_type`
    , `fare_amount`
    , `extra`
    , `mta_tax`
    , `tip_amount`
    , `tolls_amount`
    , `improvement_surcharge`
    , `total_amount` 
    , `congestion_surcharge`
    , `Airport_fee`
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


INSERT INTO yellow_zones_stats
  SELECT 
      window_start,
      MIN(PUZone) AS `zone name`,
      COUNT(`VendorID`) as `trips count`,
      MAX(`tpep_pickup_ts`) AS `last ride`,
      ROUND(SUM(`total_amount`)) as `tumble earn`
  FROM TABLE(
    TUMBLE(TABLE joined_yellow_taxi, DESCRIPTOR(tpep_pickup_ts), INTERVAL '1' HOUR ) )
  WHERE 
    TIMESTAMPDIFF(HOUR,CURRENT_WATERMARK(`tpep_pickup_ts`),`tpep_pickup_ts`) <2
  GROUP BY 
    window_start, PULocationID
  HAVING
    COUNT(`VendorID`) >= 10;
    