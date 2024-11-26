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
    `VendorID` INT,
    `proc_time` AS PROCTIME(),
    `tpep_pickup_datetime` BIGINT,
    `tpep_pickup_ts` TIMESTAMP_LTZ(3),
    WATERMARK FOR `tpep_pickup_ts` AS `tpep_pickup_ts` - INTERVAL '1' HOUR,
    `tpep_dropoff_datetime` BIGINT,
    `tpep_dropoff_ts` TIMESTAMP_LTZ(3),
    `passenger_count` DOUBLE,
    `trip_distance` DOUBLE,
    `RatecodeID` DOUBLE,
    `store_and_fwd_flag` STRING,
    `PULocationID` INT,
    `PUZone` STRING,
    `PUBorough` STRING,
    `DOLocationID` INT,
    `DOZone` STRING,
    `DOBorough` STRING,
    `payment_type` BIGINT,
    `fare_amount` DOUBLE,
    `extra` DOUBLE,
    `mta_tax` DOUBLE,
    `tip_amount` DOUBLE,
    `tolls_amount` DOUBLE,
    `improvement_surcharge` DOUBLE,
    `total_amount` DOUBLE ,
    `congestion_surcharge` DOUBLE,
    `Airport_fee` DOUBLE
  ) WITH (
    'connector' = 'kafka',
    'topic' = 'postgres_cdc.public.joined_yellow_taxi',
    'properties.bootstrap.servers' = 'kafka1:29092,kafka2:29092,kafka3:29092',
    'properties.group.id' = 'ConsumerID',
    'scan.startup.mode' = 'latest-offset',
    'format' = 'debezium-json'
  );

 CREATE TABLE yellow_zones_stats(
    `window_start` TIMESTAMP(3) NOT NULL,
    `zone name` STRING NOT NULL,
    `trips count` BIGINT NOT NULL,
    `last ride` TIMESTAMP_LTZ(3),
    WATERMARK FOR `last ride` as `last ride` - INTERVAL '1' HOUR,
    `tumble earn` DOUBLE
  ) WITH (
    'connector' = 'kafka',
    'topic' = 'postgres_cdc.public.yellow_zones_stats',
    'properties.bootstrap.servers' = 'kafka1:29092,kafka2:29092,kafka3:29092',
    'properties.group.id' = 'ConsumerID',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'debezium-json'
  );
