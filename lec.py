import json

class LEC:
    def __init__(self):
        pass

    def verify(self, node, cp, eg = None, msg = None):
        if msg is None:
            m = {
                'cpid': cp.id,
                'src': node,
                'data': {
                    'type': 'ec',
                    'route': [node]
                }
            }
            cp.flood(m, self, node)
        else:
            route = msg['data']['route']
            frules = cp.get_rules_group_by_output()
            if node == 'D': return
            if not eg in frules[node]: return
            if node in route: return
            # space = Space(areas=msg['data']['space'])
            # space.multiply(frules[in_port])
            # if len(space.areas) == 0:
            #     log('empty')
            #     return
            route.insert(0, node)
            # cp.add_ec(route, space)
            m = {
                'cpid': cp.id,
                'src': node,
                'data': {
                    'type': 'ec',
                    'route': route
                }
            }
            cp.flood(m, self, node, eg)
