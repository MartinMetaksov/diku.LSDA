## to run in the shell :
cat data.txt | ./mapper.py | sort | ./reducer.py
#### with combiner
cat data.txt | ./mapper.py | sort | ./combiner.py | ./reducer.py

#### multiple files
cat data_1.txt data_2.txt | ./mapper.py | sort | ./reducer.py

#### with globbing
cat data_*.txt | ./mapper.py | sort | ./reducer.py

#### or just 10 lines
head -10 data.txt | ./mapper.py | sort | ./reducer.py
#### you may need to ensure the files are executable first
chmod +x mapper.py reducer.py & cat data.txt | ./mapper.py | sort | ./reducer.py

## to run on the hadoop cluster:
#### Start/stop 
~/.start_hadoop
~/.stop_hadoop

## Add data to hadoop filesystem:
hadoop fs -ls
hadoop fs -put data.txt
hadoop fs -get data.txt
hadoop fs -rm data.txt

## Useful aliases
alias hfs="hadoop fs"
alias hls="hfs -ls"

run_mapreduce() {
    
    hadoop jar /srv/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -mapper $1 -reducer $2 -file $1 -file $2 -input $3 -output $4

}

run_mapcombinereduce() {
    
    hadoop jar /srv/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -mapper $1 -combiner $2 -reducer $3 -file $1 -file $2 -file $3 -input $4 -output $5

}

alias hrunc=run_mapcombinereduce

#### after setting aliases run to apply onto current terminal
source ~/.bashrc