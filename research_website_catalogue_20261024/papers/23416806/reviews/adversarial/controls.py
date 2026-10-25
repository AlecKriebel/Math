"""Independent finite automaton/profile controls; no source-package execution.

Run --verify-only to repeat without writes. Default writes one fresh own receipt.
These finite examples do not verify the universal bound or general procedure.
"""
from collections import Counter, deque
from itertools import product
from pathlib import Path
import datetime
import json
import sys

if sys.argv[1:] not in ([], ['--verify-only']):
    raise SystemExit('usage: controls.py [--verify-only]')
results = []


def need(name, ok, evidence=None):
    if not ok:
        raise RuntimeError(name + ': ' + str(evidence))
    results.append({'name': name, 'verified': True, 'evidence': evidence})


def words(n):
    return [''.join(t) for t in product('01', repeat=n)]


# Even-shift paths start in either E or O and end in either state.
# Every finite path extends bi-infinitely because this graph is strongly connected.
edges = {('E','0'):'E', ('E','1'):'O', ('O','1'):'E'}


def read(states, w):
    for a in w:
        states = frozenset(edges[q,a] for q in states if (q,a) in edges)
    return states


def allowed(w):
    return bool(read(frozenset(['E','O']), w))


def actual_join(left, right):
    start = read(frozenset(['E','O']), left)
    queue = deque([(start, '')])
    seen = {start}
    while queue:
        state, c = queue.popleft()
        if read(state, right):
            return c
        for a in '01':
            nxt = read(state, a)
            if nxt and nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, c+a))
    raise RuntimeError('irreducible join unexpectedly absent')


def graph(n):
    vertices = [w for w in words(n-1) if allowed(w)]
    adj = {v: [] for v in vertices}
    for w in words(n):
        if allowed(w):
            adj[w[:-1]].append((w[-1], w[1:]))
    return vertices, adj


def graph_read(adj, state, w):
    for a in w:
        nxt = [q for label,q in adj[state] if label == a]
        if not nxt:
            return None
        state = nxt[0]
    return state


def path_to(adj, start, predicate):
    queue = deque([(start,'')])
    seen = {start}
    while queue:
        q,w = queue.popleft()
        if predicate(q):
            return w,q
        for a,r in adj[q]:
            if r not in seen:
                seen.add(r)
                queue.append((r,w+a))
    raise RuntimeError('finite reachable target absent')


def factors(w,k):
    return {w[i:i+k] for i in range(len(w)-k+1)}


def profile_list(w,k):
    left = k//2
    right = k-left
    return [(w[max(0,i-left):i],w[i:min(len(w),i+right)]) for i in range(len(w))]


examples = []
for n,k in [(2,2),(3,2),(3,3),(4,3),(4,4)]:
    vertices,adj = graph(n)
    ln = [w for w in words(n) if allowed(w)]
    for q in vertices:
        for r in vertices:
            path_to(adj,q,lambda z:z==r)
    U = ''
    for w in ln:
        U += actual_join(U,w)+w
    while len(U) < n+k:
        U += actual_join(U,'0')+'0'
    need('U allowed and covers all n-words '+str((n,k)), allowed(U) and factors(U,n)==set(ln))
    m = 2*n+1
    bad = '0'+'1'*m+'0'
    need('odd-gap locally allowed but bad '+str(n), not allowed(bad) and factors(bad,n)<=set(ln), {'m':m})
    start = U[-n+1:]
    c,q = path_to(adj,start,lambda z:graph_read(adj,z,bad) is not None)
    q = graph_read(adj,q,bad)
    d,r = path_to(adj,q,lambda z:graph_read(adj,z,U) is not None)
    W = U+c+bad+d+U
    e = actual_join(U,U)
    V = U+e+U
    lk = {w for w in words(k) if allowed(w)}
    need('saturated words and local factors '+str((n,k)), allowed(V) and not allowed(W)
         and factors(W,n)<=set(ln) and factors(W,k)==factors(V,k)==lk)
    need('saturated endpoints and profile sets '+str((n,k)), V[:k-1]==W[:k-1] and V[-k+1:]==W[-k+1:]
         and set(profile_list(V,k))==set(profile_list(W,k)))
    need('set/count negative control '+str((n,k)), Counter(profile_list(V,k))!=Counter(profile_list(W,k)))
    examples.append({'n':n,'k':k,'U':U,'bad_word':bad,'c':c,'d':d,'e':e,'V':V,'W':W,
                     'profile_set_size':len(set(profile_list(V,k))), 'N_from_imported_bound_tested':False})

need('factors alone insufficient', factors('010',2)==factors('101',2)
     and set(profile_list('010',2))!=set(profile_list('101',2)))
need('short-word epsilon control', ''.join([])=='' and allowed(''))

# All-radius even-shift witness construction sampled at these n only; the proof
# for arbitrary n is in DERIVATIONS.md and uses the same inequality, not this list.
for n in [2,3,4,7,12]:
    m=2*n+1
    period='0'+'1'*m
    cyclic=(period*3)
    need('periodic witness finite diagnostic n='+str(n), m%2==1 and m+2>n
         and all(allowed(cyclic[i:i+n]) for i in range(len(period)))
         and not allowed('0'+'1'*m+'0'))

# An exact finite reachability instance at the actual bound: T={0^Z} in the
# alphabet {0,1}, identity local rule, L=0*, B=words containing1. A common
# transition monoid has precisely id and the constant-dead transformation.
idmap=(0,1)
deadmap=(1,1)
monoid={idmap,deadmap}
need('common recognizing monoid closed', all(tuple(b[a[q]] for q in range(2)) in monoid for a in monoid for b in monoid))
k=4*(len(monoid)+1)
N=max(2,1,k)
vertex='0'*(N-1)
seen={(vertex,0)}
queue=deque(seen)
bad_reached=False
while queue:
    q,state=queue.popleft()
    bad_reached |= state==1
    # The only allowed N-edge appends0, and the B-DFA remains in state0.
    nxt=(q[1:]+'0',state)
    if nxt not in seen:
        seen.add(nxt);queue.append(nxt)
need('actual-bound positive reachability control', N==12 and not bad_reached and len(seen)==1, {'M_size':2,'k':k,'N':N})
need('nononto equality negative control', {'0'} < {'0','1'}, 'Constant full-shift code has singleton image, yet extends from full shift.')
need('reducible U obstruction control', not any('00' in w and '11' in w for w in ['0'*8,'1'*8]),
     'The two-fixed-point shift has no word visiting both components. This diagnoses the strong-connectivity step only.')

out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'EXACT_FINITE_CONTROLS_COMPLETED',
     'checks':results,'saturation_examples':examples,'universal_bound_verified_by_finite_tests':False,
     'profile_position_convention':'0<=i<|w|; left floor(k/2), right ceil(k/2), endpoint truncation',
     'independent_universal_proofs':'DERIVATIONS.md','supplied_code_executed':False}
if sys.argv[1:] != ['--verify-only']:
    with (Path(__file__).resolve().parent/'CONTROL_RESULTS.json').open('x') as f:
        json.dump(out,f,indent=2);f.write('\n')
print(json.dumps({'status':out['status'],'checks':len(results),'saturation_examples':len(examples)}))
