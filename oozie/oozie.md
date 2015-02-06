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

### Note
If you are not running on Hortonworks Sandbox (2.0+) you will need to edit job properties to specify your name node, job tracker and username.
