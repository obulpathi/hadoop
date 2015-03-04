# Notes on Flume

## What is Flume?
A service for streaming logs into Hadoop. Apache Flume is a distributed, reliable, and available service for efficiently collecting, aggregating, and moving large amounts of streaming data into the Hadoop Distributed File System (HDFS). It has a simple and flexible architecture based on streaming data flows; and is robust and fault tolerant with tunable reliability mechanisms for failover and recovery.

## What Flume does?
* Stream data from multiple sources into Hadoop for analysis
* Collect high-volume Web logsin real time
* Insulate themselves from transient spikes when the rate of incoming data exceeds the rate at which data can be written to the destination
* Guarantee data delivery
* Scale horizontally to handle additional data volume

##  How Flume Works.
* Event – a singular unit of data that is transported by Flume (typically a single log entry)
* Source – the entity through which data enters into Flume. Sources either actively poll for data or passively wait for data to be delivered to them. A variety of sources allow data to be collected, such as log4j logs and syslogs.
* Sink – the entity that delivers the data to the destination. A variety of sinks allow data to be streamed to a range of destinations. One example is the HDFS sink that writes events to HDFS.
* Channel – the conduit between the Source and the Sink. Sources ingest events into the channel and the sinks drain the channel.
* Agent – any physical Java virtual machine running Flume. It is a collection of sources, sinks and channels.
* Client – produces and transmits the Event to the Source operating within the Agent

## Reliability & Scaling.
Flume is designed to be highly reliable, thereby no data is lost during normal operation. Flume also supports dynamic reconfiguration without the need for a restart, which allows for reduction in the downtime for flume agents. Flume is architected to be fully distributed with no central coordination point. Each agent runs independent of others with no inherent single point of failure. Flume also features built-in support for load balancing and failover. Flume's fully decentralized architecture also plays a key role in its ability to scale. Since each agent runs independently, Flume can be scaled horizontally with ease.
