# build_network.py
Parses the memory.log file produced by the system monitor script to produce a network.
The script first constructs complete graphs of the processes at each time step.
It then combines these to create a network of the most demanding processes linked to
one another if they appeared together in a time interval.  The edges are weighted based
on the combined memory usage of the nodes.  This might be useful for looking at which
*combinations* of processes cause the system to slow down.  The resulting graph is written to
a CSV-like edge list.
# Requirements
* Python 3
* networkx
# Usage
## Parameters
* `--filename`: provide the memory log file for building the network.  Defaults to ./memory.log.sample
* `--outfile`: specify the desired path/name for the output edge list.  Defaults to ./example.edgelist
* `--threshold`: specify the minimum memory threshold (in MB) of the processes used in the final network.  Defaults to 1000