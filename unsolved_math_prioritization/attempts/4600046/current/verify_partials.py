#!/usr/bin/env python3
"""Independent deterministic finite checks. Never certifies an unrestricted antecedent.
No assert statements; all failed checks raise, under normal, -O and -OO alike.
The --mutant flag selects an actual wrong mathematical algorithm/hypothesis.
"""
import argparse
import hashlib
import itertools as it
import json
import math
import os
import sys
from pathlib import Path

class AuditFailure(Exception):
    pass

def need(condition, message):
    if not condition:
        raise AuditFailure(message)

PUBLIC_PINS_SHA256 = '93ac449bf3aa79dc1ccd43546078d1bee41124e35c107a10a49e84b424c4e909'
MUTANT = None

def gauss(succ, target):
    """Independent GF(2) elimination, including cancellation of loop coefficients."""
    n = len(succ)
    rows = []
    for i, j in enumerate(succ):
        mask = 1 << i
        if j is not None:
            mask ^= 1 << j
        rows.append(mask | (int(target[i]) << n))
    pivot = 0
    cols = []
    for col in range(n):
        k = next((k for k in range(pivot, n) if (rows[k] >> col) & 1), None)
        if k is None:
            continue
        rows[pivot], rows[k] = rows[k], rows[pivot]
        for k in range(n):
            if k != pivot and ((rows[k] >> col) & 1):
                rows[k] ^= rows[pivot]
        cols.append(col)
        pivot += 1
    if any((r & ((1 << n) - 1)) == 0 and ((r >> n) & 1) for r in rows):
        return None
    ans = [0] * n
    for k, col in enumerate(cols):
        ans[col] = (rows[k] >> n) & 1
    return ans


def parity_dsu(succ, target):
    """Solve edge parity constraints with a disjoint-set forest and constant node.
Unlike the author's solver, this does not inspect directed cycles or route topology.
"""
    n = len(succ)
    parent = list(range(n + 1))
    rank = [0] * (n + 1)
    parity = [0] * (n + 1)
    def find(v):
        if parent[v] != v:
            root, p = find(parent[v])
            parity[v] ^= p
            parent[v] = root
        return parent[v], parity[v]
    for i, j in enumerate(succ):
        if MUTANT == 'ignore_loops' and j == i:
            j = None
        j = n if j is None else j
        ri, pi = find(i)
        rj, pj = find(j)
        if ri == rj:
            if pi ^ pj != target[i]:
                if MUTANT == 'ignore_cycle_parity':
                    continue
                return None
        else:
            if rank[ri] > rank[rj]:
                ri, rj = rj, ri
            parent[ri] = rj
            parity[ri] = pi ^ pj ^ target[i]
            if rank[ri] == rank[rj]:
                rank[rj] += 1
    const_root, const_parity = find(n)
    result = []
    for i in range(n):
        r, p = find(i)
        result.append(p ^ (const_parity if r == const_root else 0))
    return result


def valid(succ, target, sol):
    return sol is not None and len(sol) == len(succ) and all(
        sol[i] ^ (0 if j is None else sol[j]) == target[i]
        for i, j in enumerate(succ))


def finite_graph_checks():
    graphs = targets = 0
    for n in range(1, 5):
        for succ in it.product((None,) + tuple(range(n)), repeat=n):
            graphs += 1
            for target in it.product((0, 1), repeat=n):
                targets += 1
                reference = gauss(succ, target)
                candidate = parity_dsu(succ, target)
                need((reference is None) == (candidate is None),
                     f'finite graph consistency mismatch: {succ}, {target}')
                if candidate is not None:
                    need(valid(succ, target, candidate), 'DSU returned invalid assignment')
    return {'graphs': graphs, 'target_assignments': targets,
            'includes': ['loops', 'reciprocal directed edges', 'merging incoming trees', 'terminals']}


def cycles_with_winding(route, n, d):
    vertices = tuple(it.product(range(n), repeat=d))
    successor = {v: None if route[v] is None else tuple((v[j] + route[v][j]) % n for j in range(d))
                 for v in vertices}
    # Independently identify cycle vertices by pruning all indegree-zero vertices.
    indegree = {v: 0 for v in vertices}
    for v in vertices:
        if successor[v] is not None:
            indegree[successor[v]] += 1
    stack = [v for v in vertices if indegree[v] == 0]
    while stack:
        v = stack.pop()
        w = successor[v]
        if w is not None:
            indegree[w] -= 1
            if indegree[w] == 0:
                stack.append(w)
    remaining = {v for v in vertices if indegree[v] > 0 and successor[v] is not None}
    answer = []
    while remaining:
        start = min(remaining)
        cyc, v = [], start
        while not cyc or v != start:
            need(v in remaining, 'pruned cycle detection inconsistency')
            remaining.remove(v)
            cyc.append(v)
            v = successor[v]
        delta = tuple(sum(route[v][j] for v in cyc) for j in range(d))
        need(all(x % n == 0 for x in delta), 'cycle displacement not lattice divisible')
        answer.append((cyc, tuple(x // n for x in delta)))
    return answer


def make_lift(route, target, n, d, m):
    vertices = tuple(it.product(range(n * m), repeat=d))
    index = {v: i for i, v in enumerate(vertices)}
    succ, rhs = [], []
    for v in vertices:
        base = tuple(x % n for x in v)
        s = route[base]
        succ.append(None if s is None else index[tuple((v[j] + s[j]) % (n*m) for j in range(d))])
        rhs.append(target[base])
    return succ, rhs


def multiplier(R, n, d):
    m = 1
    if MUTANT == 'odd_multiplier':
        return 3
    if MUTANT == 'arbitrary_even_multiplier':
        return 6
    while m < R * n ** (d-1) if MUTANT == 'nonstrict_bound' else m <= R * n ** (d-1):
        m *= 2
    return m


def routing_checks():
    # Long steps separate nonzero winding from nonzero residue and odd order.
    stress = []
    for d, n, shift in [(2,1,(1,0)), (2,1,(2,0)), (2,1,(-4,3)),
                        (3,1,(1,0,-1)), (3,2,(1,0,0))]:
        vs = tuple(it.product(range(n), repeat=d))
        route = dict.fromkeys(vs, shift)
        target = dict.fromkeys(vs, 1)
        R = max(1, *map(abs, shift))
        m = multiplier(R,n,d)
        cs = cycles_with_winding(route,n,d)
        need(all(any(k) for _,k in cs), 'stress route accidentally zero winding')
        for cyc,k in cs:
            order = math.lcm(*(m // math.gcd(m, x) for x in k))
            need(order % 2 == 0, f'power-of-two winding failed: m={m}, k={k}, order={order}')
        succ, rhs = make_lift(route,target,n,d,m)
        sol = parity_dsu(succ,rhs)
        need(valid(succ,rhs,sol), 'long-step/dimensional periodic lift invalid')
        stress.append({'d':d,'n':n,'step':shift,'m':m,'vertices':len(succ)})
    vs = tuple(it.product(range(2), repeat=2))
    options = (None,(0,0),(1,0),(-1,0),(0,1),(0,-1))
    accepted = rejected = targets = oddbase = 0
    for steps in it.product(options, repeat=4):
        route = dict(zip(vs,steps))
        cs = cycles_with_winding(route,2,2)
        zero = any(not any(k) for _,k in cs)
        if zero and MUTANT != 'ignore_zero_winding':
            rejected += 1
            # Build a cycle-specific odd target on a larger cover. Zero winding must stay obstructed.
            odd_cycle = next(c for c,k in cs if not any(k))
            target = dict.fromkeys(vs,0)
            target[odd_cycle[0]] = 1
            succ,rhs = make_lift(route,target,2,2,4)
            need(parity_dsu(succ,rhs) is None, 'zero-winding obstruction unexpectedly solvable')
            continue
        accepted += 1
        m = multiplier(1,2,2)
        for bits in it.product((0,1),repeat=4):
            target = dict(zip(vs,bits))
            oddbase += any(sum(target[v] for v in cy)%2 for cy,k in cs)
            succ,rhs = make_lift(route,target,2,2,m)
            sol = parity_dsu(succ,rhs)
            need(valid(succ,rhs,sol), 'accepted periodic routing target has no verified lift')
            need((gauss(succ,rhs) is None) == (sol is None), 'lift elimination disagrees with DSU')
            targets += 1
    need((accepted,rejected,targets,oddbase)==(425,871,6800,1632), 'exhaustive routing census changed')
    return {'patterns_including_zero_steps':6**4,'accepted':accepted,'rejected':rejected,
            'lifted_targets':targets,'odd_base_cycle_targets':oddbase,'theorem_multiplier':4,
            'long_step_and_dimension_stress':stress,
            'interpretation':'Conditional graph tests; no universal CA antecedent inferred.'}


def marker_image(x, v):
    a = x.get(v,2)
    nxt = (v[0]+1,v[1])
    return 2 if a == 2 else a ^ (x.get(nxt,2) % 2)


def marker_inverse(y):
    result = {}
    for v in sorted(y,reverse=True):
        result[v] = y[v] ^ (result.get((v[0]+1,v[1]),2)%2)
    return result


def marker_and_q_checks():
    sites = tuple(it.product(range(-1,2),range(2)))
    count = 0
    for word in it.product(range(3),repeat=len(sites)):
        target={v:a for v,a in zip(sites,word) if a != 2}
        ans = marker_inverse(target)
        need(set(ans)==set(target),'marker support changed')
        for v in it.product(range(-2,3),range(-1,3)):
            need(marker_image(ans,v)==target.get(v,2),'marker inverse equation failed')
        # Independently brute-force all binary assignments on the exact marker support.
        solutions = 0
        for bits in it.product((0,1),repeat=len(target)):
            x=dict(zip(target,bits))
            if all(marker_image(x,v)==target[v] for v in target):
                solutions += 1
        need(solutions==1,'marker finite fibre was not unique')
        count += 1
    for m in (1,2,7,40):
        y={(i,0):0 for i in range(-m,m+1)}
        z=dict(y);z[(m,0)]=1
        a,b=marker_inverse(y),marker_inverse(z)
        need(a[(0,0)]==0 and b[(0,0)]==1,'marker nonuniformity witness disappeared')
        if MUTANT == 'uniform_inverse_radius':
            need(a[(0,0)]==b[(0,0)],'same finite input window does not determine inverse origin')
    # Fixed q=(0,1), control active iff c(v)=1 and c(v+e1)=0, pointing +e1.
    # All active vertices have inactive successors for every control configuration.
    n=5
    control=[1,0,0,0,0]
    succ=[(i+1)%n if control[i]==1 and control[(i+1)%n]==0 else None for i in range(n)]
    target=[1]*n
    b=parity_dsu(succ,target)
    if MUTANT == 'replace_specified_q':
        b=[0 if succ[i] is None else b[i] for i in range(n)]
    need(valid(succ,target,b),'specified beta=1 target was replaced by zero background')
    need(b==[0,1,1,1,1],'beta=1 finite lift has wrong boundary')
    return {'two_dimensional_marker_words':count,'brute_force_unique_support_fibres':count,
            'nonuniformity_radii':[1,2,7,40],'nonzero_q_verified':True}


def collar_checks():
    # Exhaust the geometry used by both collar proofs, including output centers outside Q_L.
    pairs=0
    for d,r,L in [(1,1,3),(1,2,5),(2,1,3),(2,2,5),(3,1,3)]:
        R=tuple(range(-r,r+1))
        offsets=tuple(it.product(R,repeat=d))
        thickness = r if MUTANT == 'thin_fibre_collar' else 2*r
        for v in it.product(range(-L-r,L+r+1),repeat=d):
            neigh=[tuple(v[j]+u[j] for j in range(d)) for u in offsets]
            inside=[u for u in neigh if max(map(abs,u))<=L]
            outside=[u for u in neigh if max(map(abs,u))>L]
            if inside and outside:
                for u in inside:
                    need(max(map(abs,u))>L-thickness,'crossing input is outside the proposed collar')
                    pairs+=1
    # Explicit counterexample to the one-r collar for arbitrary equal-image fibres.
    L=2
    def xprime(i,j): return int(j==0 and i%2==1)
    def patched(i,j): return xprime(i,j) if max(abs(i),abs(j))<=L else 0
    need(all(xprime(i,j)==0 for i,j in it.product(range(-L,L+1),repeat=2)
             if max(abs(i),abs(j))==L),'thin collar counterexample malformed')
    need(all((xprime(i-1,j)^xprime(i+1,j))==0 for i,j in it.product(range(-5,6),repeat=2)),
         'full fibre counterexample not in zero fibre')
    need(patched(1,0)^patched(3,0)==1,'thin-collar patch did not produce boundary error')
    return {'crossing_input_pairs_checked':pairs,'thin_fibre_collar_counterexample':True,
            'note':'Width 2r suffices. No optimality claim is made for Proposition 1.'}


def expose_cycle(n, alphabet, offsets, topindex, target, local):
    # Already in unimodular coordinates (transverse x, longitudinal h).
    a=min(h for x,h in offsets); b=max(h for x,h in offsets); w=b-a
    need(offsets[topindex][1]==b and sum(h==b for x,h in offsets)==1,
         'strict exposedness required for scalar top-slice inversion')
    slices=tuple(it.product(range(alphabet),repeat=n))
    if w==0:
        period=n
        top=offsets[topindex]
        values={}
        for h in range(n):
            for x in range(n):
                candidates=[v for v in range(alphabet) if local((v,))==target[h][x]]
                need(len(candidates)==1,'singleton rule not permutive')
                values[((x+top[0])%n,(h+top[1])%n)]=candidates[0]
        sequence=tuple(tuple(values[x,h] for x in range(n)) for h in range(n))
        start=0
    else:
        phase=(-a)%n
        window=(slices[0],)*w
        seen={};history=[]; k=0
        while True:
            key=window if MUTANT == 'omit_target_phase' else (window,phase)
            if key in seen:
                start=seen[key];period=k-start
                break
            seen[key]=k;history.append((window,phase))
            desired=target[phase]
            candidate_top=[]
            for top in slices:
                out=[]
                for x in range(n):
                    args=[]
                    for dx,h in offsets:
                        args.append((top if h==b else window[h-a])[(x+dx)%n])
                    out.append(local(tuple(args)))
                if tuple(out)==desired:
                    candidate_top.append(top)
            need(len(candidate_top)==1,'top slice map was not a permutation')
            window=window[1:]+(candidate_top[0],)
            phase=(phase+1)%n
            k+=1
        sequence=tuple(history[j][0][0] for j in range(start,start+period))
        need(period<=n*alphabet**(w*n),'finite-state bound exceeded')
    need(period%n==0,'cycle period lost target phase')
    def value(x,h): return sequence[(h-start)%period][x%n]
    for h in range(math.lcm(period,n)):
        for x in range(n):
            args=tuple(value(x+dx,h+dh) for dx,dh in offsets)
            need(local(args)==target[h%n][x],'cycle has incorrect absolute target alignment')
    return period


def exposed_checks():
    count=0;maxT=0
    # Dummy lower input is legitimate. This target kills omission of the phase.
    target=((0,0,0),(1,1,1),(0,0,0))
    T=expose_cycle(3,2,((0,0),(0,1)),1,target,lambda v:v[1])
    need(T%3==0,'phase stress failed')
    for n in (1,2):
        for bits in it.product((0,1),repeat=n*n):
            target=tuple(tuple(bits[h*n+x] for x in range(n)) for h in range(n))
            for truth in it.product((0,1),repeat=2):
                for offsets in [((0,0),(1,1)),((1,-2),(-1,0)),((0,-1),(1,1))]:
                    T=expose_cycle(n,2,offsets,1,target,lambda v,g=truth:v[1]^g[v[0]])
                    maxT=max(maxT,T);count+=1
    # Primitive lambda=(2,3), columns (3,-2),(-1,1): determinant 1.
    need(3*1-(-1)*(-2)==1 and 2*3+3*(-2)==0 and 2*(-1)+3==1,
         'coordinate basis is not unimodular with prescribed lambda')
    # Old offsets (0,0),(0,-1),(1,0) transform via inverse [[1,1],[2,3]].
    offsets=((0,0),(-1,-3),(1,2))
    for bits in it.product((0,1),repeat=4):
        target=(bits[:2],bits[2:])
        T=expose_cycle(2,2,offsets,2,target,lambda v:v[2]^v[0]^v[1])
        maxT=max(maxT,T);count+=1
    # Singleton height and spatial offset, all alphabet permutations.
    for permutation in it.permutations(range(3)):
        target=((0,1),(2,0))
        expose_cycle(2,3,((3,-2),),0,target,lambda v,p=permutation:p[v[0]])
        count+=1
    # Two co-highest inputs can each be permutive while top slice map is singular.
    topmap=[tuple(word[x]^word[(x+1)%2] for x in range(2)) for word in it.product((0,1),repeat=2)]
    need(len(set(topmap))==2,'nonexposed singularity witness disappeared')
    if MUTANT=='drop_strict_exposedness':
        need(len(set(topmap))==4,'two co-highest permutive inputs do not give a slice permutation')
    return {'constructed_periodic_lifts':count+1,'maximum_observed_T':maxT,
            'absolute_phase_offsets_checked':True,'unimodular_lambda':[2,3],
            'singleton_permutations':6,'nonexposed_negative_control':True}


def check_inputs(root):
    # Public-only authored input pins; no excluded source or historical inputs read.
    raw=(root/'PUBLIC_INPUT_PINS.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==PUBLIC_PINS_SHA256, 'public input pin manifest changed')
    manifest=json.loads(raw)
    for name,rec in manifest['files'].items():
        data=(root/name).read_bytes()
        need(len(data)==rec['bytes'] and hashlib.sha256(data).hexdigest()==rec['sha256'],
             'public authored input changed: '+name)
    return {'public_files_verified':len(manifest['files']),
            'excluded_original_input_replay':'NOT_RUN'}


def main():
    global MUTANT
    p=argparse.ArgumentParser()
    p.add_argument('--mutant',choices=['ignore_loops','ignore_cycle_parity','odd_multiplier',
       'arbitrary_even_multiplier','nonstrict_bound','ignore_zero_winding','uniform_inverse_radius',
       'replace_specified_q','thin_fibre_collar','omit_target_phase','drop_strict_exposedness'])
    args=p.parse_args();MUTANT=args.mutant
    need(os.getuid()==os.geteuid()==1000, 'UID=EUID=1000')
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode, '-I -S -B required')
    result={'uid':os.getuid(),'scope':'finite checks and public authored-input integrity; not unrestricted A/B/C',
            'input_integrity':check_inputs(Path(__file__).resolve().parents[1]),
            'finite_graphs':finite_graph_checks(),
            'routing':routing_checks(),
            'marker_and_q':marker_and_q_checks(),
            'collars':collar_checks(),
            'exposed_vertex':exposed_checks(),
            'status':'PASS','mutant':MUTANT}
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps({'status':'FAIL','error_type':type(error).__name__,'reason':str(error),
                          'mutant':MUTANT,'uid':os.getuid()},sort_keys=True))
        raise SystemExit(1)
