import json
filename = 'data.json'
sources = ['S']

import sys
sys.setrecursionlimit(3000)

def bits_count(msg):
    return len(json.dumps(msg))
        
class Simulation:
    def __init__(self):
        with open(filename) as json_file:
            data = json.load(json_file)
        self.L = data['Topology']['links']
        self.N = self.L.keys()
        self.frule = dict()
        self.id = 0 # fake id

    def get_rules_group_by_output(self):
        return self.frule

    def clear_route(self):
        self.frule = dict()

    def test(self, protos):
        self.protos = protos
        self.data = dict()
        for p in self.protos:
            self.data[p] = (0, 0)
        self.reroute()
        return self.data

    def unicast(self, msg, p, v, ing):
        pkts, bits = self.data[p]
        self.data[p] = (pkts + 1, bits + bits_count(msg))
        p.verify(v, self, ing, msg)

    def flood(self, msg, p, n, ing = None):
        for v in self.L[n]:
            if not v == ing: self.unicast(msg, p, v, n)

    def reroute(self):
        w = len(self.N)
        d = dict()

        for u in self.L.keys():
            d[u] = dict()
            for v in self.L.keys(): d[u][v] = -1
            for v in self.L[u]: d[u][v] = 1
            d[u][u] = 0


        for w in self.N:
            for u in self.N:
                for v in self.N:
                    if d[u][w] >=0 and d[w][v] >= 0: 
                        t = d[u][w] + d[w][v]
                        if d[u][v] < 0 or d[u][v] > t: d[u][v] = t

        s = sources[0]
        dst = 'D'
        verify_list = []
        for u in self.N:
            if u in self.frule.keys():
                v = self.frule[u][0] # FIXME
                if d[u][v] + d[v][dst] == d[u][dst]: 
                    continue
            for v in self.L[u]:
                if (not v == u) and d[u][v] + d[v][dst] == d[u][dst]:
                    self.frule[u] = [v]
                    verify_list.append(u)
                    print("frule:", u, "->", v)
                    break

        for u in verify_list:
            for p in self.protos:
                p.verify(u, self) # everytime set a new rule

    def random_rule(self):
        import random
        secure_random = random.SystemRandom()
        u = secure_random.choice([u for u in self.N])

        secure_random = random.SystemRandom()
        v = secure_random.choice([v for v in self.L[u]])

        self.frule[u] = [v]
        # print("frule:", u, "->", v)

        for p in self.protos:
            p.verify(u, self)
            
        return self.data
        
def main():
    network = Simulation()

    from lec import LEC
    lec_ins = LEC()

    from gpg import GPG
    gpg_ins = GPG()
    gpg_wek = GPG(weak = True)

    d = network.test([lec_ins, gpg_ins, gpg_wek])
    # print("Result: ", d[lec_ins], d[gpg_ins])
    
    u, v = d[lec_ins]
    d_lec = [v]

    u, v = d[gpg_ins]
    d_gpg = [v]

    u, v = d[gpg_wek]
    d_gpg_w = [v]

    i = 1
    while i < 100:
        d = network.random_rule()
        # print("Result: ", d[lec_ins], d[gpg_ins])

        #import time
        #time.sleep(3)
        
        i = i + 1

        u, v = d[lec_ins]
        d_lec.append(v)

        u, v = d[gpg_ins]
        d_gpg.append(v)

        u, v = d[gpg_wek]
        d_gpg_w.append(v)
    
    import matplotlib.pyplot as plt 
    cases = [u for u in range(i)]


    d_lec_d = [d_lec[0]]
    d_gpg_d = [d_gpg[0]]
    d_gpg_wd = [d_gpg_w[0]]
    for u in range(1, i):
        d_lec_d.append(d_lec[u] - d_lec[u - 1])
        d_gpg_d.append(d_gpg[u] - d_gpg[u - 1])
        d_gpg_wd.append(d_gpg_w[u] - d_gpg_w[u - 1])

    plt.plot(cases, d_lec_d, color='g')
    plt.plot(cases, d_gpg_d, color='orange')
    plt.plot(cases, d_gpg_wd, color='b')
    plt.xlabel('Cases')
    plt.ylabel('throughput in each update')
    plt.title('Quick Simulation')
    plt.show()


    plt.plot(cases, d_lec, color='g')
    plt.plot(cases, d_gpg, color='orange')
    plt.plot(cases, d_gpg_w, color='b')
    plt.xlabel('Cases')
    plt.ylabel('throughput in total')
    plt.title('Quick Simulation')
    plt.show()

if __name__ == '__main__':
    main()
