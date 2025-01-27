# DataTalksClub Data Engineering ZoomCamp
Repo showing all work done on the 2025 DataTalksClub Data Engineering ZoomCamp.

The data used in this ZoomCamp is from the NYC Taxi and Limousine Commission, whcih you can view [here!](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)


⤵️ ⤵️ ⤵️ ⤵️ 

Take part in a future course [here!](https://datatalks.club/blog/guide-to-free-online-courses-at-datatalks-club.html)

⤴️ ⤴️ ⤴️ ⤴️ 

Expand the sections below to see key notes and homework answers.

<details>
<summary>Week 1</summary>
  
## Week 1: Docker, Postgres, pgAdmin, SQL, Terraform

* First week spend mostly setting up environments, loading data into the database and generally becoming familiar with the 'basics' of the tools that will be used in the course.

### Week 1: Key Learning Points ⭐

* Docker: Used for making container environments which help smooth development, putting all packages and dependancies in one place.
* PostgreSQL: Open source relational database system.
* pgAdmin: Allows you to view and investigate the database through a user-friendly web interface.
* SQL: Key for querying structured databases!
* Terraform: Used for automating infrastructure management.


### Week 1: Blog post 💻

* To read some thoughts I had whilst working through week one, as well as more detailed key learning points.
* [Read the blog here](https://thattechdive.blogspot.com/2025/01/datatalksclub-week-1-data-engineering.html)
  
***

### Week 1: Homework 📚

* Below are the non-code answers for review!

**Question 1️⃣: run docker with the python:3.12.8 image in an interactive mode, use the entrypoint bash. What's the version of pip in the image?**

Run this command in terminal:

`docker run -it --entrypoint bash python:3.12.8`

`pip --version`

Answer:

pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)


**Question 2️⃣: Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?**

[Link to full question](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/01-docker-terraform/homework.md)

Answer:

db:5432


**Question 3️⃣: During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:**

* Up to 1 mile
* In between 1 (exclusive) and 3 miles (inclusive),
* In between 3 (exclusive) and 7 miles (inclusive),
* In between 7 (exclusive) and 10 miles (inclusive),
* Over 10 miles


* To add the data for green taxi's and for zones I added these commands into the terminal:
```
# Adding green taxi data
python Week1_IngestingDataAndPostgres.py \
    --user=root \
    --password=root \
    --host=localhost\
    --port=5432 \
    --db=ny_taxi \
    --table_name=green_taxi_trips \
    --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"


# Adding zones table
python Week1_IngestingDataAndPostgres.py \
    --user=root \
    --password=root \
    --host=localhost\
    --port=5432 \
    --db=ny_taxi \
    --table_name=zones \
    --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"


# for green taxis change df.tpep_pickup_datetime to df.lpep_pickup_datetime
# for zones, remove the datestamp lines
```

* up to one mile:

```
SELECT
    -- Adding an alias
    COUNT(*) AS trips_up_to_1_mile
FROM 
    (
        -- Green taxi trips
        SELECT 1
        FROM green_taxi_trips
        WHERE lpep_pickup_datetime >= '2019-10-01'
          AND lpep_pickup_datetime < '2019-11-01'
          AND trip_distance <= 1

        UNION ALL
        
        -- Yellow taxi trips
        SELECT 1
        FROM yellow_taxi_data
        WHERE tpep_pickup_datetime >= '2019-10-01'
          AND tpep_pickup_datetime < '2019-11-01'
          AND trip_distance <= 1
    ) AS trips
```
Answer: 104830

* 3-7 miles

```
SELECT 
    COUNT(*) AS trips_3to7_miles
FROM 
    (
        SELECT 1
        FROM green_taxi_trips
        WHERE lpep_pickup_datetime >= '2019-10-01'
          AND lpep_pickup_datetime < '2019-11-01'
          AND trip_distance > 3
          AND trip_distance <= 7

        UNION ALL
        
        SELECT 1
        FROM yellow_taxi_data
        WHERE tpep_pickup_datetime >= '2019-10-01'
          AND tpep_pickup_datetime < '2019-11-01'
          AND trip_distance > 3
          AND trip_distance <= 7
    ) AS trips
```
Answer: 109642

* 7-10 miles

```
SELECT 
    COUNT(*) AS trips_7to10_miles
FROM 
    (
        SELECT 1
        FROM green_taxi_trips
        WHERE lpep_pickup_datetime >= '2019-10-01'
          AND lpep_pickup_datetime < '2019-11-01'
          AND trip_distance > 7
          AND trip_distance <= 10

        UNION ALL

        SELECT 1
        FROM yellow_taxi_data
        WHERE tpep_pickup_datetime >= '2019-10-01'
          AND tpep_pickup_datetime < '2019-11-01'
          AND trip_distance > 7
          AND trip_distance <= 10
    ) AS trips

```

Answer: 27686

* Over 10 miles

```
SELECT 
    COUNT(*) AS trips_over10_miles
FROM 
    (
        SELECT 1
        FROM green_taxi_trips
        WHERE lpep_pickup_datetime >= '2019-10-01'
          AND lpep_pickup_datetime < '2019-11-01'
          AND trip_distance > 10

        UNION ALL

        SELECT 1
        FROM yellow_taxi_data
        WHERE tpep_pickup_datetime >= '2019-10-01'
          AND tpep_pickup_datetime < '2019-11-01'
          AND trip_distance > 10
    ) AS trips

```

Answer: 35201


**Question 4️⃣: Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.**

```
WITH max_trip_per_day AS (
    -- Green taxi trips
    SELECT 
        DATE(lpep_pickup_datetime) AS pickup_day, 
        MAX(trip_distance) AS max_distance
    FROM green_taxi_trips
    WHERE lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01'
    GROUP BY pickup_day

    UNION ALL

    -- Yellow taxi trips
    SELECT 
        DATE(tpep_pickup_datetime) AS pickup_day, 
        MAX(trip_distance) AS max_distance
    FROM yellow_taxi_data
    WHERE tpep_pickup_datetime >= '2019-10-01' AND tpep_pickup_datetime < '2019-11-01'
    GROUP BY pickup_day
)

-- Find the overall day with the longest trip distance
SELECT 
    pickup_day,
    MAX(max_distance) AS longest_trip_distance
FROM max_trip_per_day
GROUP BY pickup_day
ORDER BY longest_trip_distance DESC
LIMIT 1;
```

Answer: 2019-10-31


**Question 5️⃣: Which were the top pickup locations with over 13,000 in total_amount (across all trips) for 2019-10-18?**

```
-- Had to add "" to columns in this calculation - I think because of cap letters in column names
SELECT 
    z."Zone", 
    z."Borough", 
    total_amount_per_location."PULocationID", 
    total_amount_per_location.total_amount
FROM 
    (
        -- Pickup location in green taxi trips
        SELECT 
            "PULocationID", 
            SUM(total_amount) AS total_amount
        FROM green_taxi_trips
        WHERE DATE(lpep_pickup_datetime) = '2019-10-18'
        GROUP BY "PULocationID"

        UNION ALL

        -- Pickup location in yellow taxi trips
        SELECT 
            "PULocationID", 
            SUM(total_amount) AS total_amount
        FROM yellow_taxi_data
        WHERE DATE(tpep_pickup_datetime) = '2019-10-18'
        GROUP BY "PULocationID"
    ) AS total_amount_per_location
JOIN zones z ON total_amount_per_location."PULocationID" = z."LocationID"
WHERE total_amount_per_location.total_amount > 13000
ORDER BY total_amount_per_location.total_amount DESC;
```

Answer: East Harlem North, East Harlem South, Morningside Heights

**Question 6️⃣: For the passengers picked up in October 2019 in the zone named "East Harlem North" which was the drop off zone that had the largest tip?**

```
--Again had to put column names in "" to avoid errors
SELECT 
    z_drop."Zone" AS dropoff_zone,
FROM 
    (
        -- Green taxi trips
        SELECT 
            gt."PULocationID", 
            gt."DOLocationID", 
            gt."tip_amount" AS total_tip
        FROM green_taxi_trips gt
        JOIN zones z_pickup ON gt."PULocationID" = z_pickup."LocationID"
        JOIN zones z_drop ON gt."DOLocationID" = z_drop."LocationID"
        WHERE DATE(gt."lpep_pickup_datetime") >= '2019-10-01'
          AND DATE(gt."lpep_pickup_datetime") < '2019-11-01'
          AND z_pickup."Zone" = 'East Harlem North'

        UNION ALL

        -- Yellow taxi trips
        SELECT 
            yt."PULocationID", 
            yt."DOLocationID", 
            yt."tip_amount" AS total_tip
        FROM yellow_taxi_data yt
        JOIN zones z_pickup ON yt."PULocationID" = z_pickup."LocationID"
        JOIN zones z_drop ON yt."DOLocationID" = z_drop."LocationID"
        WHERE DATE(yt."tpep_pickup_datetime") >= '2019-10-01'
          AND DATE(yt."tpep_pickup_datetime") < '2019-11-01'
          AND z_pickup."Zone" = 'East Harlem North'
    ) AS tips_per_trip
JOIN zones z_drop ON tips_per_trip."DOLocationID" = z_drop."LocationID"
GROUP BY 
    z_drop."Zone"
LIMIT 1;
```

Answer: JFK Airport


**Question 7️⃣: Which of the following sequences, respectively, describes the workflow for: Downloading the provider plugins and setting up backend, Generating proposed changes and auto-executing the plan, Remove all resources managed by terraform**

Answer: terraform init, terraform apply -auto-approve, terraform destroy. Answer deducted by working through the tutorials/lectures.

</details>

<details>
<summary>Week 2</summary>

## Week 2 

### Week 2: Key Learning Points ⭐

### Week 2: Blog Post 💻

***

### Week 2: Homework 📚

</details>

<details>
<summary>Week 3</summary>

## Week 3 

### Week 3: Key Learning Points ⭐

### Week 3: Blog Post 💻

***

### Week 3: Homework 📚

</details>

<details>
<summary>Week 3</summary>

## Week 3 

### Week 3: Key Learning Points ⭐

### Week 3: Blog Post 💻

***

### Week 3: Homework 📚

</details>

<details>
<summary>Week 4</summary>

## Week 4 

### Week 4: Key Learning Points ⭐

### Week 4: Blog Post 💻

***

### Week 4: Homework 📚

</details>

<details>
<summary>Week 5</summary>

## Week 5

### Week 5: Key Learning Points ⭐

### Week 5: Blog Post 💻

***

### Week 5: Homework 📚

</details>

<details>
<summary>Week 6</summary>

## Week 6 

### Week 6: Key Learning Points ⭐

### Week 6: Blog Post 💻

***

### Week 6: Homework 📚

</details>

<details>
<summary>Week 7</summary>

## Week 7 

### Week 7: Key Learning Points ⭐

### Week 7: Blog Post 💻

***

### Week 7: Homework 📚

</details>

<details>
<summary>Week 8</summary>

## Week 8 

### Week 8: Key Learning Points ⭐

### Week 8: Blog Post 💻

***

### Week 8: Homework 📚

</details>
