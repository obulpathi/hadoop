SHOW DATABASES;
CREATE DATABASE financials;
CREATE DATABASE IF NOT EXISTS financials;
CREATE DATABASE financials COMMENT 'Holds all financial tables';
DESCRIBE DATABASE financials;
USE financials;
DROP DATABASE IF EXISTS financials;
DROP DATABASE IF EXISTS financials CASCADE;
ALTER DATABASE financials SET DBPROPERTIES ('edited-by' = 'Joe Dba');


CREATE TABLE IF NOT EXISTS mydb.employees (
    name STRING COMMENT 'Employee name',
    salary FLOAT COMMENT 'Employee salary',
    subordinates ARRAY<STRING> COMMENT 'Names of subordinates',
    deductions MAP<STRING, FLOAT> COMMENT 'Keys are deductions names, values are percentages',
    address STRUCT<street:STRING, city:STRING, state:STRING, zip:INT> COMMENT 'Home address')
COMMENT 'Description of the table'
TBLPROPERTIES ('creator'='me', 'created_at'='2012-01-02 10:00:00', ...)
LOCATION '/user/hive/warehouse/mydb.db/employees';


CREATE TABLE some_data (
first FLOAT,
second FLOAT,
third FLOAT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',';


CREATE TABLE some_data (
first FLOAT,
second FLOAT,
third FLOAT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t';


CREATE TABLE employees (
    name STRING,
    salary FLOAT,
    subordinates ARRAY<STRING>,
    deductions MAP<STRING, FLOAT>,
    address STRUCT<street:STRING, city:STRING, state:STRING, zip:INT>)
PARTITIONED BY (country STRING, state STRING);


LOAD DATA [LOCAL] INPATH 'filepath' [OVERWRITE] INTO TABLE tablename.
INSERT INTO TABLE tablename1 select columnlist FROM secondtable;


SELECT name, salary FROM employees;
SELECT name, subordinates[0] FROM employees;
SELECT name, deductions["State Taxes"] FROM employees;
SELECT symbol, `price.*` FROM stocks;
SELECT upper(name), salary, deductions["Federal Taxes"], round(salary * (1 - deductions["Federal Taxes"])) FROM employees;
SELECT count(*), avg(salary) FROM employees;
SELECT count(DISTINCT ymd), count(DISTINCT volume) FROM stocks;
Nested SELECT
SELECT * FROM employees WHERE country = 'US' AND state = 'CA';
SELECT year(ymd), avg(price_close) FROM stocks WHERE exchange = 'NASDAQ' AND symbol = 'AAPL' GROUP BY year(ymd);
SELECT a.ymd, a.price_close, b.price_close FROM stocks a JOIN stocks b ON a.ymd = b.ymd WHERE a.symbol = 'AAPL' AND b.symbol = 'IBM';

SELECT s.ymd, s.symbol, s.price_close FROM stocks s ORDER BY s.ymd ASC, s.symbol DESC;

Hive offers no support for row level inserts, updates, and deletes.
Hive doesn’t support transactions.
Hive adds extensions to provide better performance in the context of Hadoop and to integrate with custom extensions and even external programs.

-- This is a Hive program. Hive is an SQL-like language that compiles
-- into Hadoop Map/Reduce jobs. It's very popular among data analysts
-- because it allows them to query enormous Hadoop data stores using
-- a language much like SQL.

-- Our logs are stored on the Hadoop Distributed File System, in the
-- directory /logs/randomhacks.net/access.  They're ordinary Apache
-- logs in *.gz format.
--
-- We want to pretend that these gzipped log files are a database table,
-- and use a regular expression to split lines into database columns.

CREATE EXTERNAL TABLE access(
  host STRING,
  identity STRING,
  user STRING,
  time STRING,
  request STRING,
  status STRING,
  size STRING,
  referer STRING,
  agent STRING)
ROW FORMAT SERDE 'org.apache.hadoop.hive.contrib.serde2.RegexSerDe'
WITH SERDEPROPERTIES (
  "input.regex" = "([^ ]*) ([^ ]*) ([^ ]*) (-|\\[[^\\]]*\\]) ([^ \"]*|\"[^\"]*\") (-|[0-9]*) (-|[0-9]*)(?: ([^ \"]*|\"[^\"]*\") ([^ \"]*|\"[^\"]*\"))?",
  "output.format.string" = "%1$s %2$s %3$s %4$s %5$s %6$s %7$s %8$s %9$s"
)
STORED AS TEXTFILE
LOCATION '/logs/randomhacks.net/access';

-- We want to store our logs in HBase, which is designed to hold tables
-- with billions of rows and millions of columns. HBase stores rows
-- sorted by primary key, so you can efficiently read all records within
-- a given range of keys.
--
-- Here, our key is a Unix time stamp, and we assume that it always has
-- the same number of digits (hey, this was a dodgy late night hack).
-- So we could easily grab all the records from a specific time period.
--
-- We store our data in 3 column families: "m" for metadata, "r" for
-- referrer data, and "a" for user-agent data. This allows us to only
-- load a subset of columns for a given query.
CREATE EXTERNAL TABLE access_hbase(
  key STRING,          -- Unix time + ":" + unique identifier.
  host STRING,         -- The IP address of the host making the request.
  identity STRING,     -- ??? (raw log data)
  user STRING,         -- ??? (raw log data)
  time BIGINT,         -- Unix time, UTC.
  method STRING,       -- "GET", etc.
  path STRING,         -- "/logo.png", etc.
  protocol STRING,     -- "HTTP/1.1", etc.
  status SMALLINT,     -- 200, 404, etc.
  size BIGINT,         -- Response size, in bytes.
  referer_host STRING, -- "www.google.com", etc.
  referer STRING,      -- Full referrer string.
  agent STRING)        -- Full agent string.
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES (
  "hbase.columns.mapping" = ":key,m:host,m:identity,m:user,m:time,m:method,m:path,m:protocol,m:status,m:size,r:referer_host,r:referer,a:agent"
)
TBLPROPERTIES ("hbase.table.name" = "randomhacks_access");

-- Copy our data from raw Apache log files to HBase, cleaning it up as we go.  This is basically
-- a pseudo-SQL query which calls a few Java helpers.
--
-- Note the "TABLESAMPLE" clause, which says to pick one of every 20 records at random.
INSERT OVERWRITE TABLE access_hbase
  SELECT concat(cast(unix_timestamp(time, "[dd/MMM/yyyy:HH:mm:ss Z]") AS STRING), ":", guid()) AS key,
         host,
         unquote_apache(identity),
         unquote_apache(user),
         unix_timestamp(time, "[dd/MMM/yyyy:HH:mm:ss Z]"),
         re_extract(unquote_apache(request), "([^ ]*) ([^ ]*) ([^\"]*)", 1) AS method,
         re_extract(unquote_apache(request), "([^ ]*) ([^ ]*) ([^\"]*)", 2) AS path,
         re_extract(unquote_apache(request), "([^ ]*) ([^ ]*) ([^\"]*)", 3) AS protocol,
         cast(status AS SMALLINT) AS status,
         cast(size AS BIGINT) AS size,
         re_extract(unquote_apache(referer), "[^:]+:?/+([^/]*).*", 1) AS referer_host,
         unquote_apache(referer) AS referer,
         unquote_apache(agent)
    FROM access TABLESAMPLE(BUCKET 1 OUT OF 20 ON rand())
    WHERE unix_timestamp(time, "[dd/MMM/yyyy:HH:mm:ss Z]") IS NOT NULL;

-- Find the 50 most popular pages on the site.
SELECT path, count(*) AS cnt
  FROM access_hbase GROUP BY path
  ORDER BY cnt DESC LIMIT 50;

-- Categorize our articles by year and count how many hits each year received.
SELECT pubyear, count(*)
  FROM (SELECT re_extract(path, "/articles/([0-9]+)/.*", 1) AS pubyear
          FROM access_hbase) access
  WHERE pubyear IS NOT NULL
  GROUP BY pubyear;
