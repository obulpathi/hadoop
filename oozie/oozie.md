# Oozie Examples

Examples of the cron-like scheduler introduced in OOZIE-1306. The following
examples have been tested on Hartonworks HDP 2.1 Sandbox

## Usage

Copy files to local filesystem on your Hadoop cluster or sandbox.

### Place the files into HDFS.
* hadoop fs -put oozie

### Every 15 minutes example:
* oozie job -oozie http://localhost:11000/oozie -config oozie/every-fifteen-minutes/job.properties -run

### First day of every month example:
* oozie job -oozie http://localhost:11000/oozie -config oozie/first-day-of-the-month/job.properties -run

### Weekdays at 2 am example.
* oozie job -oozie http://localhost:11000/oozie -config oozie/weekdays-at-two-am/job.properties -run

### Kill a job
* oozie job -oozie http://localhost:11000/oozie -kill 0000310-150206075957529-oozie-oozi-C

### Note
If you are not running on Hortonworks Sandbox (2.0+) you will need to edit job properties to specify your name node, job tracker and username.

Apache Oozie is a workflow scheduling engine for the Hadoop platform. The
framework facilitates coordination among interdependent, recurring jobs using
the Oozie coordinator, which you can trigger by either a prescheduled time or
data availability.


## Workflow.xml
Workflow control nodes
The start control node, as shown in Listing 1, is the entry point for a workflow job. When a workflow starts, it automatically transitions to the node specified in the start.
Listing 1. Start control node
<workflow-app xmlns="uri:oozie:workflow:0.2" name="ooziedemo-wf">
    <start to="timeCheck"/>
</workflow-app>
The end control node, as shown in Listing 2, is the end of the workflow job. It indicates the workflow actions have completed successfully. A workflow definition must have an end node.
Listing 2. End control node
<workflow-app xmlns="uri:oozie:workflow:0.2" name="ooziedemo-wf">
    <end name="end"/>
</workflow-app>
The kill control node , as shown in Listing 3, enables the workflow job to stop itself. When one or more actions started by the workflow job are running when the kill node is reached, all the actions that are currently running are stopped. A workflow definition can have zero or more kill nodes.
Listing 3. Kill control code
<workflow-app xmlns="uri:oozie:workflow:0.2" name="ooziedemo-wf">
    <kill name="fail">
        <message>Sqoop failed, error message[${wf:errorMessage(wf:lastErrorNode())}]</message>
   </kill>
</workflow-app>
The decision control node, as shown in Listing 4, enables a workflow to decide on the execution path to follow. The decision node works similar to a switch-case block that has a set of predicates-transition pairs and a default transition. Predicates are evaluated in order, until one of them evaluates to true, and the corresponding transition is taken. If none of the predicates evaluates to true, the default transition is taken.
Listing 4. Decision control node
<workflow-app xmlns="uri:oozie:workflow:0.2" name="ooziedemo-wf">
    <decision name="master-decision">
       <switch>
         <case to="sqoopMerge1">
                 ${wf:actionData('hiveSwitch')['paramNum'] eq 1}
         </case>
         <default to="sqoopMerge2"/>
       </switch>
   </decision>
</workflow-app>
The fork node splits one execution path into multiple concurrent paths. The join node waits until all concurrent execution paths of the precursory fork node arrive at the join node. You must use the fork and join nodes, as shown in Listing 5, in pairs.
Listing 5. Fork-join control node
<workflow-app xmlns="uri:oozie:workflow:0.2" name="ooziedemo-wf">
    <fork name="forking">
        <path start="sqoopMerge1"/>
        <path start="sqoopMerge2"/>
    </fork>
    <join name="joining" to="hiveSwitch"/>
</workflow-app>
