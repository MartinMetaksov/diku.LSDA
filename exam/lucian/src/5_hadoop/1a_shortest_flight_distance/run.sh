#!/bin/bash

# A script to run map reduce either locally or on the virtual cluster
combine=0
local=0
copydata=0
# process input 
while [ "$1" != "" ]; do
    case $1 in
        -datadir ) shift
                   DATAPATH=$1
                   ;;
        -c )    combine=1
                ;;
        -copydata )     copydata=1
                        ;;
        -lo  )  local=1  
                ;;
        * )     echo "invalid arguments; supported : -datadir , -c , -lo -copydata"
                exit 1
    esac
    shift
done

####### Constants 
OPNAME=$(basename "$PWD")
echo "Running operation $OPNAME"
DATADIR=$(basename "$DATAPATH")
echo "Using data from $DATAPATH in $DATADIR"



####### Functions
function ensure_runnable {
    if [ "$combine" -eq "0" ]; then
        chmod +x mapper.py reducer.py
    fi
    if [ "$combine" -eq "1" ]; then
        chmod +x mapper.py reducer.py combiner.py
    fi
} # end of ensure_runnable

function ensure_hdfs_ready {
    if [ "$copydata" -eq "1" ]; then
        # ensure the correct files are in hdfs
        hadoop fs -rm -r -f data/$DATADIR
		hadoop fs -mkdir data/$DATADIR
        hadoop fs -put $DATAPATH/* data/$DATADIR
    fi
   
    # ensure the output directory is empty
    hadoop fs -mkdir out
    hadoop fs -rm -r -f out/$OPNAME
} # end of ensure_hdfs_data

function run_mapreduce() {
    if [ "$combine" -eq "0" ]; then
    hadoop jar $HADOOP_STREAMING -mapper $1 -reducer $2 -file $1 -file $2 -input $3 -output $4
    fi
    if [ "$combine" -eq "1" ]; then
    hadoop jar $HADOOP_STREAMING -mapper $1 -combiner $2 -reducer $3 -file $1 -file $2 -file $3 -input $4 -output $5
    fi
}


function run_hadoop {
    if [ "$combine" -eq "0" ]; then
        run_mapreduce mapper.py reducer.py data/$DATADIR/* out/$OPNAME 2>&1 | tee hrun.out
    fi
    if [ "$combine" -eq "1" ]; then
        run_mapreduce mapper.py combiner.py reducer.py data/$DATADIR/* out/$OPNAME 2>&1 | tee hrun.out
    fi
    hadoop fs -get out/$OPNAME ./out
    echo "===== HADOOP RESULTS ======"
    cat ./out/*
} #end of run_hadoop

function run_local {
    if [ "$combine" -eq "0" ]; then
        cat $DATAPATH/*  | ./mapper.py | sort | ./reducer.py
    fi
    if [ "$combine" -eq "1" ]; then
        cat $DATAPATH/*  | ./mapper.py | sort | ./combiner.py | ./reducer.py
    fi
} # end of run_local


###### Main
if [ "$local" -eq "0" ]; then
    rm ./hrun.out
    rm -rf ./out
    echo "running on hadoop cluster"
    ensure_hdfs_ready
    run_hadoop
fi

if [ "$local" -eq "1" ]; then
    echo "running on local machine"
    ensure_runnable
    run_local
fi