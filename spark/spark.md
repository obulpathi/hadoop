# Notes on Spark

## Limitations of Hadoop
* Lack of iteration support
* High latency due to persisting intermediate data onto disk


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

## References
* http://horicky.blogspot.com/2013/12/spark-low-latency-massively-parallel.html
* https://github.com/apache/spark/tree/master/examples/src/main/python
