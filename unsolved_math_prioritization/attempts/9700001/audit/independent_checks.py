#!/usr/bin/env python3
"""Independent finite exact controls. Does not import the author checker."""
from fractions import Fraction as Q
from itertools import product
from collections import Counter
import json
import random

C = Counter()
rng = random.Random(20261003211039)

def demand(group, condition):
    if not condition:
        raise AssertionError(group)
    C[group] += 1

def average(xs, ps):
    return sum((x*p for x,p in zip(xs,ps)), Q(0))

def all_times(tags, n):
    """Enumerate stopping maps directly by assigning every alive atom at each time."""
    ans = []
    def visit(t, alive, vals):
        if t == n:
            out = vals[:]
            for i in alive:
                out[i] = n
            ans.append(tuple(out))
            return
        atoms = sorted({tags[t][i] for i in alive})
        for flags in product((False, True), repeat=len(atoms)):
            stops = {a for a,f in zip(atoms,flags) if f}
            out = vals[:]
            more = []
            for i in alive:
                if tags[t][i] in stops:
                    out[i] = t
                else:
                    more.append(i)
            visit(t+1, more, out)
    visit(0, list(range(len(tags[0]))), [-1]*len(tags[0]))
    return sorted(set(ans))

def finite_and_features():
    n = 3
    leaves = list(product((0,1), repeat=n))
    variants = [list(range(n+1)), [0,0,1,2], [0,0,0,0], [0,1,1,3]]
    for reveals in variants:
        tags = [[w[:reveals[t]] for w in leaves] for t in range(n+1)]
        times = all_times(tags,n)
        for trial in range(36):
            weights = [rng.randrange(5) for _ in leaves]
            if not any(weights): weights[0] = 1
            ps = [Q(w,sum(weights)) for w in weights]
            xnode = {v: Q(rng.randrange(-10,11), rng.randrange(1,6))
                     for t in range(n+1) for v in product((0,1), repeat=t)}
            # Every fourth trial is a genuine martingale, including nonzero X_0.
            if trial % 4 == 0:
                for t in range(n-1,-1,-1):
                    for v in product((0,1), repeat=t):
                        ix = [i for i,w in enumerate(leaves) if w[:t] == v]
                        mass = sum(ps[i] for i in ix)
                        xnode[v] = sum((ps[i]*xnode[leaves[i][:t+1]] for i in ix),Q(0))/mass if mass else Q(0)
            x = [[xnode[w[:t]] for w in leaves] for t in range(n+1)]
            b = [average(xt,ps)-average(x[0],ps) for xt in x]
            q = {}
            y = []
            for t in range(n+1):
                means = {}
                for atom in set(tags[t]):
                    ix = [i for i,a in enumerate(tags[t]) if a == atom]
                    mass = sum(ps[i] for i in ix)
                    means[atom] = sum((ps[i]*x[t][i] for i in ix),Q(0))/mass if mass else Q(0)
                    if t<n:
                        q[t,atom] = sum((ps[i]*(x[t+1][i]-x[t][i]) for i in ix),Q(0))
                y.append([means[a] for a in tags[t]])
            tests = b[1:n]+[b[t]+value for (t,a),value in q.items()]
            projection = [sum((ps[i]*(y[t+1][i]-y[t][i]) for i,a in enumerate(tags[t]) if a == atom),Q(0))
                          for t in range(n) for atom in set(tags[t])]
            deviations = [average([x[t][i] for i,t in enumerate(T)],ps)-average(x[0],ps) for T in times]
            demand('finite_four_way_equivalence', len({all(z == 0 for z in obj) for obj in (tests,list(q.values()),projection,deviations)}) == 1)
            pos = sum((z for z in q.values() if z>0),Q(0))
            neg = -sum((z for z in q.values() if z<0),Q(0))
            for T,a in zip(times,deviations):
                demand('projection_at_stopping', average([x[t][i]-y[t][i] for i,t in enumerate(T)],ps) == 0)
                demand('sharper_drift_bound', abs(a)<=max(pos,neg))
                # Random signed, adapted features and deterministic rational coefficients.
                total = Q(0)
                for t in range(n):
                    delta = [x[t+1][i]-x[t][i] for i in range(len(leaves))]
                    phi = []
                    for j in range(2):
                        table = {v:Q(rng.randrange(-3,4),2) for v in set(tags[t])}
                        phi.append([table[v] for v in tags[t]])
                    coeff = [Q(rng.randrange(-3,4),3) for _ in range(2)]
                    f = [sum(coeff[j]*phi[j][i] for j in range(2)) for i in range(len(leaves))]
                    residual = average([abs(Q(T[i]>t)-f[i])*abs(delta[i]) for i in range(len(leaves))],ps)
                    eta = [abs(average([phi[j][i]*delta[i] for i in range(len(leaves))],ps)) for j in range(2)]
                    total += residual+sum(abs(coeff[j])*eta[j] for j in range(2))
                demand('signed_feature_approximation', abs(a)<=total)
            for (t,atom),z in q.items():
                demand('local_witness_factor', max(abs(b[t]),abs(b[t]+z))>=abs(z)/2)

# Fraction-free-style row dependence is not needed at these tiny sizes; this
# independent solver fixes the last free column and back-substitutes only.
def kernel(A,k):
    E = [list(map(Q,row)) for row in A]
    pivot = []
    r = 0
    for c in range(k):
        hit = next((i for i in range(r,len(E)) if E[i][c]),None)
        if hit is None: continue
        E[r],E[hit] = E[hit],E[r]
        for i in range(r+1,len(E)):
            if E[i][c]:
                ratio = E[i][c]/E[r][c]
                E[i] = [a-ratio*b for a,b in zip(E[i],E[r])]
        pivot.append(c)
        r += 1
        if r == len(E): break
    free = [c for c in range(k) if c not in pivot][-1]
    out = [Q(0)]*k
    out[free] = Q(1)
    for i,c in reversed(list(enumerate(pivot))):
        out[c] = -sum((E[i][j]*out[j] for j in range(c+1,k)),Q(0))/E[i][c]
    return out, len(pivot)

def fixed_library():
    examples = []
    for n in range(1,7):
        nodes = [v for t in range(n) for v in product((0,1),repeat=t)]
        leaves = list(product((0,1),repeat=n))
        ps = [Q(1,len(leaves))]*len(leaves)
        for trial in range(24):
            m = trial % min(len(nodes),13)
            decisions = [{v:rng.choice((False,True)) for v in nodes} for _ in range(m)]
            def survives(D,v):
                return all(not D[v[:t]] for t in range(len(v)+1))
            selected = rng.sample(nodes,m+1)
            A = [[int(survives(D,v)) for v in selected] for D in decisions]
            u, rank = kernel(A,m+1)
            d = [a*2**len(v) for a,v in zip(u,selected)]
            norm = sum(map(abs,d))
            d = [a/norm for a in d]
            eps = Q(1,2**(n+3))
            z = {}
            for t in range(n+1):
                observed = set()
                for v in product((0,1),repeat=t):
                    W = sum((a for a,w in zip(d,selected) if len(w)<t and v[:len(w)] == w),Q(0))
                    M = sum(((Q(b)-Q(1,2))*Q(1,2**(j+1)) for j,b in enumerate(v)),Q(0))
                    z[v] = M+eps*W
                    demand('bounded_natural_process', abs(z[v])<1 and abs(W)<=1)
                    observed.add(z[v])
                    shifted = 2**t*(z[v]+Q(1-Q(1,2**t),2))
                    rounded = (shifted+Q(1,2)).numerator//(shifted+Q(1,2)).denominator
                    integer = sum(bit*2**(t-j-1) for j,bit in enumerate(v))
                    demand('exact_price_decoder', rounded == integer)
                demand('natural_filtration_injectivity', len(observed) == 2**t)
            for D in decisions:
                stopped = []
                for leaf in leaves:
                    t = next((s for s in range(n) if D[leaf[:s]]),n)
                    stopped.append(z[leaf[:t]])
                demand('fixed_stopping_equalities', average(stopped,ps) == 0)
            for v in nodes:
                actual = (z[v+(0,)]+z[v+(1,)])/2-z[v]
                expected = eps*sum((a for a,w in zip(d,selected) if v==w),Q(0))
                demand('all_node_conditional_drifts', actual == expected)
            v = next(v for a,v in zip(d,selected) if a)
            t = len(v)
            mean = average([z[w[:t]] for w in leaves],ps)
            stopped = [z[w[:t if mean else t+int(w[:t]==v)]] for w in leaves]
            witness = average(stopped,ps)
            demand('simple_missed_witness', witness != 0)
            # W-basis drift rows are the identity, independently of stopping tests.
            if trial == 0:
                for v in nodes:
                    for w in nodes:
                        def B(prefix): return int(len(prefix)>len(w) and prefix[:len(w)]==w)
                        drift = Q(B(v+(0,))+B(v+(1,)),2)-B(v)
                        demand('drift_dimension_identity', drift == int(v==w))
            if trial == 23:
                examples.append({'n':n,'m':m,'matrix_rank':rank,'selected_depths':[len(v) for v in selected],
                                 'witness_expectation':str(witness),'largest_coefficient_bits':max(max(a.numerator.bit_length(),a.denominator.bit_length()) for a in d)})
    return examples

def stopping_constraint_ranks():
    for n in range(1,5):
        leaves = list(product((0,1), repeat=n))
        tags = [[w[:t] for w in leaves] for t in range(n+1)]
        times = all_times(tags,n)
        nodes = [v for t in range(n) for v in product((0,1),repeat=t)]
        # Zero augmentation permits the independent elimination helper to return
        # rank even if the unaugmented stopping matrix has full column rank.
        A = []
        for T in times:
            row = []
            for v in nodes:
                i = next(i for i,w in enumerate(leaves) if w[:len(v)]==v)
                row.append(int(T[i]>len(v)))
            A.append(row+[0])
        _,rank = kernel(A,len(nodes)+1)
        demand('full_stopping_constraint_rank', rank==2**n-1)

def markov_random_initial():
    n = 2
    for k,number in [(2,24),(3,3)]:
        histories = list(product(range(k),repeat=n+1))
        tags = [[w[:t+1] for w in histories] for t in range(n+1)]
        times = all_times(tags,n)
        for trial in range(number):
            def distribution():
                weights = [rng.randrange(4) for _ in range(k)]
                if not any(weights): weights[0] = 1
                return [Q(w,sum(weights)) for w in weights]
            pi = distribution()
            P = [[distribution() for _ in range(k)] for _ in range(n)]
            g = [[Q(rng.randrange(-8,9),rng.randrange(1,8)) for _ in range(k)] for _ in range(n+1)]
            if trial%6 == 0:
                for t in range(n-1,-1,-1):
                    g[t] = [sum(P[t][s][u]*g[t+1][u] for u in range(k)) for s in range(k)]
            probabilities = [pi[w[0]]*P[0][w[0]][w[1]]*P[1][w[1]][w[2]] for w in histories]
            baseline = sum(pi[s]*g[0][s] for s in range(k))
            vals = [average([g[t][w[t]] for w,t in zip(histories,T)],probabilities) for T in times]
            upper = g[-1][:]
            lower = upper[:]
            top_policy = {}
            bottom_policy = {}
            for t in range(n-1,-1,-1):
                up = [sum(P[t][s][u]*upper[u] for u in range(k)) for s in range(k)]
                lo = [sum(P[t][s][u]*lower[u] for u in range(k)) for s in range(k)]
                for s in range(k):
                    top_policy[t,s] = g[t][s]>=up[s]
                    bottom_policy[t,s] = g[t][s]<=lo[s]
                upper = [max(g[t][s],up[s]) for s in range(k)]
                lower = [min(g[t][s],lo[s]) for s in range(k)]
            demand('markov_full_history_extrema', max(vals)==sum(pi[s]*upper[s] for s in range(k)) and min(vals)==sum(pi[s]*lower[s] for s in range(k)))
            for policy, optimum in ((top_policy,max(vals)),(bottom_policy,min(vals))):
                rewards = []
                for w in histories:
                    t = next((t for t in range(n) if policy[t,w[t]]),n)
                    rewards.append(g[t][w[t]])
                demand('markov_constructed_policy', average(rewards,probabilities)==optimum)
            q = []
            now = pi[:]
            for t in range(n):
                q += [now[s]*(sum(P[t][s][u]*g[t+1][u] for u in range(k))-g[t][s]) for s in range(k)]
                now = [sum(now[s]*P[t][s][u] for s in range(k)) for u in range(k)]
            demand('markov_zero_drift_equivalence', all(a==baseline for a in vals)==all(a==0 for a in q))
            for value in vals:
                demand('markov_deviation_bound', abs(value-baseline)<=sum(map(abs,q)))

def statistics():
    for numerator in range(1,12):
        theta = Q(numerator,13)
        for K in range(1,9):
            probs = [theta**sum(w)*(1-theta)**(K-sum(w)) for w in product((0,1),repeat=K)]
            tv = (abs(probs[0]-1)+sum(probs[1:]))/2
            demand('enumerated_sample_total_variation', tv==1-(1-theta)**K and tv<=K*theta)
            # Tests that randomize independently on the finite sample space.
            for _ in range(4):
                test = [Q(rng.randrange(8),7) for _ in probs]
                difference = abs(sum(p*a for p,a in zip(probs,test))-test[0])
                demand('randomized_test_tv_bound', difference<=tv)
    for _ in range(5000):
        epsilon = Q(rng.randrange(40),7)
        radius = Q(rng.randrange(30),11)
        a = Q(rng.randrange(-100,101),13)
        hat = a+radius*Q(rng.randrange(-17,18),17)
        demand('statistical_threshold_implications',
               (not(abs(hat)>epsilon+radius) or abs(a)>epsilon) and
               (not(abs(hat)<=epsilon-radius) or abs(a)<=epsilon) and
               (not(abs(a)>epsilon+2*radius) or abs(hat)>epsilon+radius))

if __name__ == '__main__':
    finite_and_features()
    examples = fixed_library()
    stopping_constraint_ranks()
    markov_random_initial()
    statistics()
    print(json.dumps({'status':'PASS','arithmetic':'fractions.Fraction','seed':20261003211039,
                      'total_assertions':sum(C.values()),'counts':dict(sorted(C.items())),
                      'obstruction_examples':examples,
                      'scope':'Independent finite boundary controls, not a proof of universal statements or of historical novelty.'},indent=2,sort_keys=True))
