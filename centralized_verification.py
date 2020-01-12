# DFA: nx.DiGraph()
# FIB: list of rules/dicts?
def centralized_verification(DFA, FIB):
    # Local check
    for vnode in DFA.nodes():
        vnode.violation = set()
        for entry in get_fib(FIB, vnode.node):
            if entry.action not in vnode.next_hop:
                vnode.violation.add(entry.match)

    # Back propagation. Reverse topological sort.
    degrees = dict()
    queue = []
    for vnode in DFA.nodes():
        degrees[vnode] = len(DFA.successors(vnode))
        if degrees[vnode] == 0:
            queue.append(vnode)
    while queue:
        cur = queue.pop(0)
        # Update violation set from next_hop
        for entry in get_fib(FIB, vnode.node):
            if entry.action in vnode.next_hop:
                vnode.violation = vnode.violation \
                    .union( vnode.next_hop[entry.action].violation
                    .intersection(entry.match) )
        # Decrease the remaining out-degrees of predecessors
        for pred in DFA.predecessors(vnode):
            degrees[pred] = degrees[pred] - 1
            # Add to queue when all successors are done
            if degrees[pred] == 0:
                queue.append(pred)
