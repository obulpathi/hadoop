# Notes on Pig Latin

## Pig Philosophy
* Pigs eat anything
* Pigs live anywhere
* Pigs are domestic animals
* Pigs fly

## Names
* Pig Latin for a language
* Grunt for a shell
* Piggybank for shared repository

## How to run pig
* pig script.pig
* pig -file script.pig
* pig -check script.pig
* pig -dryrun script.pig
* pig -execute 'command'
* pig -x local script.pig
* pig -propertyFile file script.pig

## Data types
* Scalar: int, long, float, double, chararray, bytearray
* Complex:
* * map: ['name'#'Obulpathi', 'age': 30]
* * tuple: ('Obulpathi', 30)
* * bag: {('Obulpathi', 30), ('Dheeraj': 28)}
* Map and tuple should fit into memory, a bag need not.
* As a rule of thumb, pig required about 4 times disk pace to raw size.
* Map, tuple and bag can have optional schemas associated with them.
* If not, pig will try to infer them at run time. Not suggested.

## Comments
-- This is a comment
-- Pig also has multi-line comments

## Input
* divs = LOAD 'NYSE_dividends';
* divs = LOAD 'NYSE_dividends' USING PigStorage(',');
* divs = LOAD 'NYSE_dividends' AS (exchange, symbol, date, dividends);
* divs = LOAD 'NYSE_dividends' USING PigStorage(',') AS (exchange, symbol, date, dividends);
* divs = LOAD 'NYSE_dividends' USING PigStorage(',') (exchange: chararray, symbol: chararray, date: chararray, dividends: float);

* records = load 'records.json' using JsonLoader();
* logs = LOAD 'user.log' USING LogLoader AS (remoteAddr, project, user, time, method, uri, proto, status, bytes, referer, userAgent);
* students = LOAD 'student' USING PigStorage('\t') AS (name: chararray, age:int, gpa: float);
* divs = load 'NYSE_dividends' as (exchange:chararray, symbol:chararray, date:chararray, dividends:float);
* fields = LOAD 'fields.txt' USING PigStorage('\t') AS (f1,f2,f3);

## Pig Storage
* PigStorage is the default storage interface.
* It parses a line of input into fields using a character delimiter.
* The default delimiter is a tab.
* To specify a custom character delimiter, use PigStorage(',')

## File location in local mode
* stocks = LOAD '/root/stocks' AS (exchange, symbol, date, dividends);
* stocks = LOAD '/root/logs/' AS (exchange, symbol, date, dividends);

## File location in distributed mode
* stocks = LOAD 'stocks' AS (exchange, symbol, date, dividends);
* stocks = LOAD 'logs/' AS (exchange, symbol, date, dividends);

## Output
* Output is always a directory
* STORE processed INTO '/data/examples/processed';
* STORE processed INTO 'processed' using PigStorage(',');
* By default, PigStorage is used for writing output with tab delimited format.
* DUMP processed;

## Operations: Sorting, Grouping, Joining, Projecting, and Filtering

## Projection
* basics = FOREACH records GENERATE username, age;
* gains = FOREACH stocks GENERATE stock, close - open AS gain;
* prices = load 'NYSE_daily' as (exchange, symbol, date, open, high, low, close, volume, adj_close);
* beginning = foreach prices generate ..open; -- produces exchange, symbol, date, open
* middle = foreach prices generate open..close; -- produces open, high, low, close
* end = foreach prices generate volume..; -- produces volume, adj_close

## Filtering
* more = FILTER stocks BY price >= 5;
* less = FILTER stocks BY price < 5;
* startswithcm = FILTER stocks BY symbol MATCHES 'CM...';

## Grouping
* grouped = GROUP logs BY user;
* The grouped records have two fields, the key and the bag of collected records.
* The key field is named group. The word group is overloaded and confusing.
* The bag is named with the grouped relation.
* Grouping will result in reduce operation.

## Order
* ordered = ORDER stocks BY date, symbol;
* ordered = ORDER stocks BY date desc, symbol;
* Ordering will result in reduce operation.

## Distinct
* unique = DISTINCT records

## Join
* joined = JOIN daily BY symbol, divs BY symbol;
* joined = JOIN daily BY (symbol, date), divs BY (symbol, date);

## Limit
* first10 = LIMIT records 10;
* frist5 = FILTER stocks BY price >= 5 LIMIT 5;

## Sample
* some = SAMPLE records 0.1;

## Parallel
* Set reduce level parallelism
* Only applies to GROUP, ORDER, DISTINCT, JOIN, LIMIT, COGROUP, CROSS
* bysymbol = GROUP stocks BY symbol PARALLEL 10;

## UDFs
* REGISTER /usr/lib/pig/piggybank.jar;

* DEFINE LogLoader org.apache.pig.piggybank.storage.apachelog.CombinedLogLoader();
* DEFINE DayExtractor org.apache.pig.piggybank.evaluation.util.apachelogparser.DateExtractor('yyyy-MM-dd');
* DEFINE HostExtractor org.apache.pig.piggybank.evaluation.util.apachelogparser.HostExtractor();

## Fragment-replicated join: (Hadoop Distributed Cache)
* joined = JOIN daily BY (exchange, symbol), divs BY (exchange, symbol) USING 'replicated';
* The using 'replicated' tells Pig to use the fragment-replicate algorithm to execute this join.
* Because no reduce phase is necessary, all of this can be done in the map task.

## Mergejoin
* joined = JOIN daily BY symbol, divs BY symbol USING 'merge';

## Set
* The set command is used to set the environment in which Pig runs the MapReduce jobs.
* set default_parallel 10;
* set job.name my_job;
* set opt.multiquery false;
* set io.sort.mb 2048; --give it 2G

## Preprocessor
### Parameters
* pig -p DATE=2009-12-17 daily.pig
* pig -param_file daily.params daily.pig
* yesterday = filter daily by date == '$DATE';
* %default parallel_factor 10;
* %declare and %default

### Debugging
* DESCRIBE relation;
* EXPLAIN relation;
* bin/pig -x local -e 'explain -script explain.pig'
* ILLUSTRATE relation;
