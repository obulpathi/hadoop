# Notes on Spark

## Limitations of Hadoop
* Lot of use case specific tools: MapReduce, Pig, Hive, Storm.
* High latency due to persisting intermediate data onto disk
* Lack of support for iteration (ML) and streaming (prediction).

## Spark
* Spark is a cluster computing platform designed to be fast and general purpose.
* Spark has ability to run computations in memory.
* It supports batch applications, iterative algorithms, interactive queries, and stream processing.
* It is highly accessible, offering simple APIs in Python, Java, Scala, and SQL, and rich built-in libraries.
* It integrates closely with other Big Data tools. In particular, Spark can run in Hadoop clusters and access any Hadoop data source, including Cassandra.
* Spark is a computational engine that is responsible for scheduling, distributing, and monitoring applications consisting of computational tasks across cluster.
* Spark Core: Scheduler, memory manager, fault recoverer, storage drivers and most importantly, RDD.

## Spark SQL
* Spark SQL is Spark’s package for working with structured data.
* Also supports Hive Query Language (HQL), Parquet, and JSON.
* Allows intermixing of SQL queries with the programmatic data manipulations supported by RDDs in Python, Java, and Scala.

## Spark Streaming
* Spark Streaming is a Spark component that enables processing of live streams of data.
* Spark Streaming provides an API for manipulating data streams that closely matches the Spark Core’s RDD API.

## MLlib
* Machine learning library containing common functionality
* Includes classification, regression, clustering, and collaborative filtering.

## GraphX
* GraphX is a library for manipulating graphs (e.g., a social network’s friend graph) and performing graph-parallel computations.
* It also provides various operators for manipulating graphs (e.g., subgraph and mapVertices )
* Includes a library of common graph algorithms (e.g., PageRank and triangle counting

## Cluster Managers
* Spark can run over Hadoop YARN, Apache Mesos.
* Comes with builtin cluster manager called the Standalone Scheduler.

## Storage
* Spark can create distributed datasets from any file stored in the Hadoop distributed filesystem (HDFS) or other storage systems supported by the Hadoop APIs (including your local filesystem, Amazon S3, Cassandra, Hive, HBase, etc.).
* Spark supports text files, SequenceFiles, Avro, Parquet, and any other Hadoop InputFormat.

## Resilient Distributed Datasets (RDDs)

An RDD can be thought of as a handle to a distributed dataset, with fragments of the data spread all around the cluster. Instead of relying on replication to make datasets reliable, Spark instead tracks lineage and leverages checkpointing. This allows more cluster resources to go directly toward your computations. If the cost to recover data is high you can also selectively employ replication on any dataset.

RDD provides an abstract data structure from which application logic can be expressed as a sequence of transformation processing, without worrying about the underlying distributed nature of the data. RDD can be cached.

## Narrow dependency vs Wide dependencies
"Narrow dependency" means the all partitions of an RDD will be consumed by a single child RDD (but a child RDD is allowed to have multiple parent RDDs).  "Wide dependencies" (e.g. group-by-keys, reduce-by-keys, sort-by-keys) means a parent RDD will be splitted with elements goes to different children RDDs based on their keys.

Narrow transformation: Map, FlatMap, Filter, Sample
Wide transformation: SortByKey, ReduceByKey, GroupByKey, CogroupByKey, Join, Cartesian
Action: Collect, Take(n), Reduce, ForEach, Sample, Count, Save

The scheduler will examine the type of dependencies and group the narrow dependency RDD into a unit of processing called a stage.  Wide dependencies will span across consecutive stages within the execution and require the number of partition of the child RDD to be explicitly specified.

## A typical execution sequence is as follows ...
* RDD is created originally from external data sources (e.g. HDFS, Local file ... etc)
* RDD undergoes a sequence of TRANSFORMATION (e.g. map, flatMap, filter, groupBy, join), each provide a different RDD that feed into the next transformation.
* Finally the last step is an ACTION (e.g. count, collect, save, take), which convert the last RDD into an output to external data sources

The above sequence of processing is called a lineage (outcome of the topological sort of the DAG).  Each RDD produced within the lineage is immutable.  In fact, unless if it is cached, it is used only once to feed the next transformation to produce the next RDD and finally produce some action output.

## Fault tolerance
In a classical distributed system, fault resilience is achieved by replicating data across different machines together with a active monitoring system.  In case of any machine crashes, there is always another copy of data residing in a different machine from where recovery can take place.

Fault resiliency in Spark takes a different approach.  First of all, as a large scale compute cluster, Spark is not meant to be a large scale data cluster at all. Spark makes two assumptions of its workload.
* The processing time is finite (although the longer it takes, the cost of recovery after fault will be higher)
* Data persistence is the responsibility of external data sources, which keeps the data stable within the duration of processing.
Spark has made a tradeoff decision that in case of any data lost during the execution, it will re-execute the previous steps to recover the lost data.  However, this doesn't mean everything done so far is discarded and we need to start from scratch at the beginning.  We just need to re-executed the corresponding partition in the parent RDD which is responsible for generating the lost partitions, in case of narrow dependencies, this resolved to the same machine.

Notice that the re-execution of lost partition is exactly the same as the lazy evaluation of the DAG, which starts from the leaf node of the DAG, tracing back the dependencies on what parent RDD is needed and then eventually track all the way to the source node.  Recomputing the lost partition is done is a similar way, but taking partition as an extra piece of information to determine which parent RDD partition is needed.

## Output Persistence
However, re-execution across wide dependencies can touch a lot of parent RDD across multiple machines and may cause re-execution of everything. To mitigate this, Spark persist the intermediate data output from a Map phase before it shuffle them to different machines executing the reduce phase.  In case of machine crash, the re-execution (from another surviving machine) just need to trace back to fetch the intermediate data from the corresponding partition of the mapper's persisted output.  Spark also provide a checkpoint API to explicitly persist intermediate RDD so re-execution (when crash) doesn't need to trace all the way back to the beginning.  In future, Spark will perform check-pointing automatically by figuring out a good balance between the latency of recovery and the overhead of check-pointing based on statistical result.

Spark provides a powerful processing framework for building low latency, massively parallel processing for big data analytics.  It supports API around the RDD abstraction with a set of operation for transformation and action for a number of popular programming language like Scala, Java and Python.

## Docker

### Pull image and run
* docker pull sequenceiq/spark:1.2.0
* docker run -i -t -h sandbox sequenceiq/spark:1.2.0 bash

### Configure
* cd /usr/local/spark
* cp conf/log4j.properties.templates conf/log4j.properties
* replace INFO with WARN in log4j.rootCategory=INFO

### Test run
* cd /usr/local/spark
* /bin/spark-shell --master yarn-client --driver-memory 1g --executor-memory 1g --executor-cores 1
* sc.parallelize(1 to 1000).count()

## Writing Spark code
* Spark application consists of a driver program that launches various parallel operations on a cluster.
* The driver program contains your application's main function and defines distributed datasets on the cluster, then applies operations to them.
* Driver programs access Spark through a SparkContext object
* Code can be passed to Spark through lambdas or defined functions.

## Programming
* Spark’s core abstraction for working with data, the resilient distributed dataset (RDD).
* An RDD is simply a distributed collection of elements. In Spark all work is expressed as either creating new RDDs, transforming existing RDDs, or calling operations on RDDs to compute a result.
* Under the hood, Spark automatically distributes the data contained in RDDs across your cluster and parallelizes the operations you perform on them.
* Once created, RDDs offer two types of operations: transformations and actions.
* Transformations construct a new RDD from a previous one.
* Actions compute a result based on an RDD, and either return it to the driver program or save it to an external storage system
* Spark’s RDDs are by default recomputed each time you run an action on them.
* If you would like to reuse an RDD in multiple actions, you can ask Spark to persist it using RDD.persist()


## Program Structure
1. Create some input RDDs from external data.
2. Transform them to define new RDDs using transformations like filter() .
3. Ask Spark to persist() any intermediate RDDs that will need to be reused.
4. Launch actions such as count() and first() to kick off a parallel computation, which is then optimized and executed by Spark.

* lines = sc.parallelize(["pandas", "i like pandas"])
* lines = sc.textFile("/path/to/README.md")

## Common Transformations
* map() and filter()
* flatMap()
* set operations: distinct, union, intersection, subtract
* sample()
* cartesian()

## Common Actions
* reduce()
* fold()
* aggregate()
* collect()
* take(n)
* top()
* count()
* countByValue()

## Pair RDD
* Used to store key/value pairs
* Data is partitioned across the cluster by key
* pairs = lines.map(lambda x: (x.split(" ")[0], x))
* reduceByKey(func)
* groupByKey()
* keys()
* values()
* sortByKey()
*

## References
* http://horicky.blogspot.com/2013/12/spark-low-latency-massively-parallel.html
* https://github.com/apache/spark/tree/master/examples/src/main/python
