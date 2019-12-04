import json
import networkx as nx
import matplotlib.pyplot as plt

filename = 'data.json'
sources = ["S"]

links = []
if True: # constructing fat tree in "A Scalable, Commodity Data Center Network Architecture"
    C = 4 # number of core
    A = 4 # number of aggregation block
    M = 4 # number of switch in each block
    E = 0 # number of servers per block

    C_id = 0
    A_id = C_id + C
    E_id = A_id + A * M

    h = int(M / 2)
    for i in range(C):
        for j in range(A):
            t = A_id + j * M # connecting core to first 2 switches in each block
            # FIXME hardcoded
            if i < int(C / 2):
                links.append((i, t))
                links.append((t, i))
            else:
                links.append((i, t + 1))
                links.append((t + 1, i))

    for i in range(A):
        t = A_id + i * M
        for j in range(h): # first half switches
            for k in range(h): # late half switches
                links.append((t + j, t + h + k))
                links.append((t + h + k, t + j))
    
    for i in range(A):
        for j in range(h): # late half switches
            t = A_id + i * M + j
            for k in range(E):
                s = E_id + i * E + k
                links.append((t, s))
                links.append((s, t))

G = nx.DiGraph()
for u, v in links:
    G.add_edge(chr(ord('A') + u), chr(ord('A') + v))

pos = nx.layout.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size = 500)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=True)
plt.show()

N = 26

data = {}

links = {}
for u in G.nodes():
    links[u] = [v for v in G.successors(u)]
topology = {}
topology['links'] = links
data['Topology'] = topology

reachability = {}
reachability['init'] = "0"
reachability['acceptance'] = ["1"]
links = {}
links["1"] = {}
links["0"] = dict()
for u in G.nodes():
    if not u == 'D': 
        links["0"][u] = "0" 
    else:
        links["0"][u] = "1"
reachability['links'] = links
data['Reachability'] = reachability

for u in G.nodes():
    loop = {}
    loop['init'] = "0"
    loop['acceptance'] = ["0", "1"]

    links = {}
    links["0"], links["1"] = {}, {}
    for v in G.nodes():
        if v == u: 
            links["0"][v] = "1" 
        else:
            links["0"][v], links["1"][v] = "0", "1"
    loop['links'] = links
    data["loop-free-" + u] = loop

with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
