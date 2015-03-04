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

## Flume Agent

Flume deploys as one or more agents, each contained within its own instance of the Java Virtual Machine (JVM). Agents consist of three pluggable components: sources, sinks, and channels. An agent must have at least one of each in order to run. Sources collect incoming data as events. Sinks write events out, and channels provide a queue to connect the source and sink.

## Sources

Put simply, Flume sources listen for and consume events. Events can range from newline-terminated strings in stdout to HTTP POSTs and RPC calls — it all depends on what sources the agent is configured to use. Flume agents may have more than one source, but must have at least one. Sources require a name and a type; the type then dictates additional configuration parameters.

On consuming an event, Flume sources write the event to a channel. Importantly, sources write to their channels as transactions. By dealing in events and transactions, Flume agents maintain end-to-end flow reliability. Events are not dropped inside a Flume agent unless the channel is explicitly allowed to discard them due to a full queue.

## Channels

Channels are the mechanism by which Flume agents transfer events from their sources to their sinks. Events written to the channel by a source are not removed from the channel until a sink removes that event in a transaction. This allows Flume sinks to retry writes in the event of a failure in the external repository (such as HDFS or an outgoing network connection). For example, if the network between a Flume agent and a Hadoop cluster goes down, the channel will keep all events queued until the sink can correctly write to the cluster and close its transactions with the channel.

Channels are typically of two types: in-memory queues and durable disk-backed queues. In-memory channels provide high throughput but no recovery if an agent fails. File or database-backed channels, on the other hand, are durable. They support full recovery and event replay in the case of agent failure.

## Reliability & Scaling.
Flume is designed to be highly reliable, thereby no data is lost during normal operation. Flume also supports dynamic reconfiguration without the need for a restart, which allows for reduction in the downtime for flume agents. Flume is architected to be fully distributed with no central coordination point. Each agent runs independent of others with no inherent single point of failure. Flume also features built-in support for load balancing and failover. Flume's fully decentralized architecture also plays a key role in its ability to scale. Since each agent runs independently, Flume can be scaled horizontally with ease.

## Interceptors
Flume has the capability to modify/drop events in-flight. This is done with the help of interceptors. Interceptors are classes that implement org.apache.flume.interceptor.Interceptor interface. An interceptor can modify or even drop events based on any criteria chosen by the developer of the interceptor. Flume supports chaining of interceptors. This is made possible through by specifying the list of interceptor builder class names in the configuration. Interceptors are specified as a whitespace separated list in the source configuration. The order in which the interceptors are specified is the order in which they are invoked. The list of events returned by one interceptor is passed to the next interceptor in the chain. Interceptors can modify or drop events. If an interceptor needs to drop events, it just does not return that event in the list that it returns. If it is to drop all events, then it simply returns an empty list.

## Multiplexers
Flume supports multiplexing the event flow to one or more destinations. This is achieved by defining a flow multiplexer that can replicate or selectively route an event to one or more channels. The above example shows a source from agent “foo” fanning out the flow to three different channels. This fan out can be replicating or multiplexing. In case of replicating flow, each event is sent to all three channels. For the multiplexing case, an event is delivered to a subset of available channels when an event’s attribute matches a preconfigured value. For example, if an event attribute called “txnType” is set to “customer”, then it should go to channel1 and channel3, if it’s “vendor” then it should go to channel2, otherwise channel3. The mapping can be set in the agent’s configuration file.

## Start Flume
* flume-ng agent -c /etc/flume/conf -f /etc/flume/conf/flume.conf -n sandbox
