"""Independent finite audit by all staircase crossing subsets, not divided differences."""
import sys, os, itertools, json
sys.path.insert(0, os.path.dirname(__file__))
import explore

def accumulate(out, key, value):
    out[key] = out.get(key, 0) + value
    if out[key] == 0: del out[key]

def pipe_family(n):
    cells = [(i, j) for j in range(n-2, -1, -1) for i in range(n-j-1)]
    schubert, grothendieck = {}, {}
    for mask in range(1 << len(cells)):
        w = list(range(1, n+1)); mon = [0] * n; reduced = True; crossings = 0; inv = 0
        for bit, (i,j) in enumerate(cells):
            if mask & (1 << bit):
                crossings += 1; mon[i] += 1; k = i+j
                if w[k] < w[k+1]:
                    w[k], w[k+1] = w[k+1], w[k]; inv += 1
                else: reduced = False
        w, mon = tuple(w), tuple(mon)
        accumulate(grothendieck.setdefault(w, {}), mon, (-1)**(crossings-inv))
        if reduced: accumulate(schubert.setdefault(w, {}), mon, 1)
    return schubert, grothendieck

def main(n):
    S,G = pipe_family(n)
    results = {'n': n, 'pipe_dreams': 2**(n*(n-1)//2), 'permutations': len(G), 'schubert_recurrence_mismatches': [], 'grothendieck_recurrence_mismatches': [], 'triangularity_failures': [], 'expansion_reconstruction_failures': []}
    bycode = {explore.code(w): w for w in S}
    for w in sorted(G):
        if S[w] != explore.poly(w, False): results['schubert_recurrence_mismatches'].append(w)
        if G[w] != explore.poly(w, True): results['grothendieck_recurrence_mismatches'].append(w)
        lead = min(S[w])
        if lead != explore.code(w) or S[w][lead] != 1: results['triangularity_failures'].append(w)
        coeffs = explore.expand(G[w], bycode)
        reconstruction = {}
        for u,c in coeffs.items():
            for mon,d in S[u].items(): accumulate(reconstruction, mon, c*d)
        if reconstruction != G[w]: results['expansion_reconstruction_failures'].append(w)
    special = (1,2,5,4,3)
    if n == 5:
        coeffs = explore.expand(G[special], bycode)
        results['special_expansion'] = [{'u':u, 'length':explore.length(u), 'coefficient':c} for u,c in sorted(coeffs.items())]
        for u in [(2,3,5,4,1),(2,4,5,3,1)]:
            results['supported_left_ascents_'+''.join(map(str,u))] = [{'k':k,'u':explore.left(u,k),'coefficient':coeffs[explore.left(u,k)]} for k in range(1,n) if u.index(k)<u.index(k+1) and explore.left(u,k) in coeffs]
    path = os.path.join(os.path.dirname(__file__), f'independent_pipe_audit_n{n}.json')
    with open(path,'w') as f: json.dump(results,f,indent=2)
    print(json.dumps(results, indent=2))
if __name__ == '__main__': main(int(sys.argv[1]))
