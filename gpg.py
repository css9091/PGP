import json

def has(node, states):
    for st in states:
        if node == st[0]: return True
    return False

class GPG:
    def __init__(self):
        with open('gpg.json') as json_file: 
            data = json.load(json_file)

        self.data = data

        # load Global Product Graph (GPG) from json file 
        import networkx as nx
        self.G = nx.DiGraph()
        for u, v in data['edges']:
            self.G.add_edge(u, v)

        self.verified_false = False

        
    def verify(self, node, cp, ing = None, msg = None):
        if self.verified_false: 
            return # No need to verify anymore since the CP must be wrong

        states = []
        for t in self.data['nodes']: 
            for n in t:
                if n[0] == node: # n[0] is the node_id, n[1] is the state_id
                    states.append(n)

        frules = cp.get_rules_group_by_output()
        if msg is None: 
            # scan the actions in FIB
            for eg_node in [frules[node]]:
                # print(node, "-?->", eg_node) 
                # print(states)

                flag = False
                ing_states = dict() # (key: ing_node, value: ing_state_id)

                for state in states:
                    # check if this state DOES NOT allow this action,
                    # which means this state may have problem
                    if not has(eg_node, self.G.successors(state)):
                        for ing in self.G.predecessors(state): # retrieve ingress for this problemaitc state
                            if not ing[0] in ing_states.keys(): # ing[0] is the id of node
                                ing_states[ing[0]] = []
                            # elif not ing[1] in ing_states[ing[0]]: 
                            #    ing_states[ing[0]].append() # ing[1] is the id of states
                    else: flag = True


                if flag:  # On the other hand side, if all states do not allow this action; 
                          # there is no need to send message because we already know the CP must be wrong.
                    # print("!!!", ing_states.keys())
                    for ing in ing_states.keys(): # send message to every ing node
                        m = { 
                            'cpid': cp.id,
                            'src': node,
                            'data': {
                                'type': 'ec',
                                'route': [node, eg_node]
                            }
                        }
                        cp.unicast(m, self, ing, node)
                else:
                    pass
                    # self.verified_false = True # acutally, we can stop verification here 
        else:
            route = msg['data']['route']
            frules = cp.get_rules_group_by_output()
            if node == 'D': return
            if not ing == frules[node]: return
            if node in route: return

            ing_states = dict()
            for state in states:
                if not has(ing, self.G.successors(state)):
                    if not ing[0] in ing_states.keys():
                        ing_states[ing[0]] = []
                    # elif not ing[1] in ing_states[ing[0]]: 
                    #    ing_states[ing[0]].append()

            for ing in ing_states.keys(): 
                m = {
                    'cpid': cp.id,
                    'src': node,
                    'data': {
                        'type': 'ec',
                        'route': [ing].append(route),
                    }
                }
                cp.unicast(m, self, ing, node)
