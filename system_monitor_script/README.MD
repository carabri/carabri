# build_network.py
Parses the memory.log file produced by the system monitor script to produce a network.
The script first constructs complete graphs of the processes at each time step.
It then combines these to create a network of the most demanding processes linked to
one another if they appeared together in a time interval.  The edges are weighted based
on the combined memory usage of the nodes.  This might be useful for looking at which
*combinations* of processes cause the system to slow down.