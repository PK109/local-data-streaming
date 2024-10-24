-- streaming mode in Flink SQL
-- set 'execution.runtime-mode' = 'streaming';
-- DDL statements for Flink table creation
CREATE TABLE zones (
   `LocationID` INT,
   `Borough` STRING,
   `Zone` STRING,
   `service_zone` STRING
 ) WITH (
   'connector' = 'kafka',
   'topic' = 'postgres_cdc.public.taxi_zones',
   'properties.bootstrap.servers' = 'kafka1:29092,kafka2:29092,kafka3:29092',
   'properties.group.id' = 'ConsumerID',
   'scan.startup.mode' = 'earliest-offset',
   'format' = 'debezium-json'
 );

 CREATE TABLE yellow_taxi (
    `VendorID` INT,
    `tpep_pickup_datetime` BIGINT,
    `tpep_dropoff_datetime` BIGINT,
    `passenger_count` DOUBLE,
    `trip_distance` DOUBLE,
    `RatecodeID` DOUBLE,
    `store_and_fwd_flag` STRING,
    `PULocationID` INT,
    `DOLocationID` INT,
    `payment_type` BIGINT,
    `fare_amount` DOUBLE,
    `extra` DOUBLE,
    `mta_tax` DOUBLE,
    `tip_amount` DOUBLE,
    `tolls_amount` DOUBLE,
    `improvement_surcharge` DOUBLE,
    `total_amount` DOUBLE,
    `congestion_surcharge` DOUBLE,
    `Airport_fee` DOUBLE
  ) WITH (
    'connector' = 'kafka',
    'topic' = 'postgres_cdc.public.yellow_taxi',
    'properties.bootstrap.servers' = 'kafka1:29092,kafka2:29092,kafka3:29092',
    'properties.group.id' = 'ConsumerID',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'debezium-json'
  );

 CREATE TABLE joined_yellow_taxi (
    `tpep_pickup_datetime` BIGINT,
    `trip_distance` DOUBLE,
    `PULocationID` INT,
    `LocationID` INT,
    `Zone` STRING,
    `Borough` STRING
  ) WITH (
    'connector' = 'kafka',
    'topic' = 'postgres_cdc.public.joined_yellow_taxi',
    'properties.bootstrap.servers' = 'kafka1:29092,kafka2:29092,kafka3:29092',
    'properties.group.id' = 'ConsumerID',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'debezium-json'
  );

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