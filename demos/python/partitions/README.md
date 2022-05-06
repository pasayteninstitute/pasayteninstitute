# Partitions of a Number

In mathematics, the partitions of a positive, whole number N are simply the ways of writing it as a sum of smaller such numbers. Two partitions are considered equivalent if they differ only by the order of that sum.

This code builds a database intermally for partitions of a number. To work without any kind of storage, simply write
``` 
localPartitions = PartitionDataBase()

```
This will create an instance of the PartitionDataBase object, which builds a list of partitions of all numbers up to and including 20 upon instantiation. You can change that by adjusting the object variable PartitionDataBase.initalCount.

If you'd prefer to get to higher numbers, it is recommended that you save to disk, as the number of partitions get out of hand quickly. To that end, simply feed it a file path where you'd like that database to live:

``` 
localPartitions = PartitionDataBase("myPath/my-database-name.csv")

```
In spite the quioxtic data structure used for storing the partitions, this will read and write everything as a CSV file. Then, you need only use the method

```
localPartitions.incrementPartition()
```
For every row you'd like to add. NOTE! Using this method will automatically overwrite your old database. Not to fear, upon loading the object for the first time, a copy of the original database will be stored with a ".old" addition. Have fun!
