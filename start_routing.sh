#!/bin/bash
/usr/bin/java -D"dw.graphhopper.datareader.file=/home/jetson/graphhopper/den.pbf" -jar /home/jetson/graphhopper/graphhopper*.jar server /home/jetson/graphhopper/config-example.yml