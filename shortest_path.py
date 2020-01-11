d = dict()
d[S] = 0
# Run a single source shortest-path alg
# d[n] notates the distance from S to n

St = 0 
DFA.insert_as_initial_state(St)
for dis in range(0, d[D]): # destination D
    DFA.insert_state(St + 1)
    for n in N:
        if d[n] == dis:
            St.add_transition(n, St + 1)
    St += 1
DFA.insert_as_final_state(St + 1)
St.add_transition(D, St + 1)
