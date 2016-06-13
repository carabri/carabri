import re
import networkx
import itertools
import argparse
import json



def build_network(filename,outfile,mb_threshold):

    regex = re.compile('([0-9]+) kB: (.*)(?=\()')


    network_list = []
    current_network = []

    with open(filename, 'r') as memlog:
        ignore_line = True
        for line in memlog.readlines():
            if not ignore_line:
                result = regex.search(line)
                if (result is not None):
                    current_network.append((result.group(1), result.group(2),))
            if 'Total PSS by process:' in line:
                ignore_line = False
            if 'Total PSS by OOM adjustment:' in line:
                ignore_line = True
            if 'SAMPLE_TIME:' in line:
                edges = itertools.combinations(current_network,2)
                g = networkx.Graph()
                g.add_nodes_from(current_network)
                g.add_edges_from(edges)
                current_network = []
                network_list.append(g)


    G = networkx.Graph()
    for n in network_list:
        for i in n.nodes():
            if int(i[0]) > mb_threshold: #if it's using more than the memory threshold
                if i[1] not in G.nodes():
                    #include it in the summary graph
                    G.add_node(i[1])
                    for j in n.neighbors(i):
                        if int(j[0]) > mb_threshold:
                            w = int(i[0])+int(j[0])
                            if ([i[1]],[j[1]]) in G.edges():
                                G[i[1]][j[1]]['weight'] += w
                            elif ([j[1]],[i[1]]) in G.edges():
                                G[j[1]][i[1]]['weight'] += w
                            else:
                                G.add_edge(i[1],j[1],weight=w)

    # write result to edge list (CSV-type file)
    networkx.write_edgelist(G, outfile, data=['weight'])

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Build a network from the given usage log file, then write it to an edge list.')
    argparser.add_argument('--filename',type=str,help='provide the memory log file for building the network.  Defaults to ./memory.log.sample',default='./memory.log.sample')
    argparser.add_argument('--outfile',type=str,help='specify the desired path/name for the output edge list.  Defaults to ./example.edgelist',default='./example.edgelist')
    argparser.add_argument('--threshold',type=int,help='specify the minimum memory threshold (in MB) of the processes used in the final network.  Defaults to 1000',default=1000)
    args = argparser.parse_args()
    
    build_network(args.filename,args.outfile,args.threshold)