import re
import networkx
import itertools

regex = re.compile('([0-9]+) kB: (.*)(?=\()')


network_list = []
current_network = []

with open('memory.log', 'r') as memlog:
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
        if int(i[0]) > 1000: #if it's using more than 1 MB of memory
            if i[1] not in G.nodes():
                #include it in the summary graph
                G.add_node(i[1])
                for j in n.neighbors(i):
                    if int(j[0]) > 1000:
                        w = int(i[0])+int(j[0])
                        if ([i[1]],[j[1]]) in G.edges():
                            G[i[1]][j[1]]['weight'] += w
                        elif ([j[1]],[i[1]]) in G.edges():
                            G[j[1]][i[1]]['weight'] += w
                        else:
                            G.add_edge(i[1],j[1],weight=w)

networkx.write_edgelist(G, "example.edgelist", data=['weight'])