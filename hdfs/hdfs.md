# Hadoop Distributed File System

* hadoop fs -help
* hadoop fs -ls
* hadoop fs -copyFromLocal local.log hdfs.log
* hadoop fs -copyToLocal hdfs.log local.log
* hadoop fs -appendToFile <localsrc> ... <dst>
* hadoop fs -cat [-ignoreCrc] <src> ...
* hadoop fs -count [-q] <path> ...
* hadoop fs -cp [-f] [-p] <src> ... <dst>
* hadoop fs -createSnapshot <snapshotDir> [<snapshotName>]
* hadoop fs -deleteSnapshot <snapshotDir> <snapshotName>
* hadoop fs -df [-h] [<path> ...]
* hadoop fs -du [-s] [-h] <path> ...
* hadoop fs -get [-p] [-ignoreCrc] [-crc] <src> ... <localdst>
* hadoop fs -getfacl [-R] <path>
* hadoop fs -mkdir [-p] <path> ...
* hadoop fs -moveFromLocal <localsrc> ... <dst>
* hadoop fs -moveToLocal <src> <localdst>
* hadoop fs -mv <src> ... <dst>
* hadoop fs -put [-f] [-p] <localsrc> ... <dst>
* hadoop fs -renameSnapshot <snapshotDir> <oldName> <newName>
* hadoop fs -rm [-f] [-r|-R] [-skipTrash] <src> ...
* hadoop fs -rmdir [--ignore-fail-on-non-empty] <dir> ...
* hadoop fs -setfacl [-R] [{-b|-k} {-m|-x <acl_spec>} <path>]|[--set <acl_spec> <path>]
* hadoop fs -setrep [-R] [-w] <rep> <path> ...
* hadoop fs -tail [-f] <file>
* hadoop fs -test -[defsz] <path>
* hadoop fs -text [-ignoreCrc] <src> ...
* hadoop fs -touchz <path> ...
* hadoop fs -usage [cmd ...]
