#!/usr/bin/env python3
"""Reconstructed exhaustive certificates for the all-scale D<=1 theorem.
Only Python's standard library and integer arithmetic are used. This is a new
reconstruction, not an assertion that the unavailable historical bytes match.
"""
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse, copy, hashlib, json

ROOT = Path(__file__).resolve().parent

def require(value, message):
    if not value:
        raise RuntimeError(message)

def widths(X):
    out, p = [], 1
    while p <= X:
        a = 0
        while p * 2**(a+1) <= X:
            a += 1
        out.append(a)
        p *= 3
    return out

def smooth_below(limit):
    out, p = set(), 1
    while p < limit:
        n = p
        while n < limit:
            out.add(n)
            n *= 2
        p *= 3
    return sorted(out)

def vertices(A):
    return {(a,b) for b,w in enumerate(A) for a in range(w+1)}

def edges(A):
    return [((a,b),(a+1,b),(a,b+1)) for b in range(len(A)-1) for a in range(A[b+1]+1)]

def isolated(A):
    return vertices(A)-{p for e in edges(A) for p in e}

def phase(A,r):
    return [[int((a+2*b)%3==r) for a in range(w+1)] for b,w in enumerate(A)]

def adjusted_count(A,r):
    return sum((a+2*b)%3==r for a,b in vertices(A)-isolated(A))

def propagate(A,bottom,defect):
    out = [list(bottom)]
    require(len(bottom)==A[0]+1, 'wrong bottom length')
    for b in range(len(A)-1):
        row = [1+int((a,b)==defect)-out[-1][a]-out[-1][a+1] for a in range(A[b+1]+1)]
        if any(x not in (0,1) for x in row):
            return None
        out.append(row)
    return out

def changes(ar,base):
    return [[a,b,x-base[b][a]] for b,row in enumerate(ar) for a,x in enumerate(row) if x!=base[b][a]]

def stencil_checks():
    out = []
    A = list(range(7,-1,-1))
    for t in range(3):
        surviving = []
        for bottom in product((0,1),repeat=8):
            ar = propagate(A,bottom,(3,t))
            if ar is not None:
                surviving.append(list(bottom))
        require(not surviving, 'a forbidden interior stencil survives')
        out.append({'defect':[3,t],'bottom_words_checked':256,'survivors':surviving})
    return out

def left_checks():
    A, out = list(range(6,-1,-1)), []
    expected = {
        (0,0): [(1, [[0,0,1]]), (2, [[0,0,1]])],
        (0,1): [(0, [[0,0,-1],[0,1,1]])],
        (0,2): [(2, [[0,0,1],[0,1,-1],[0,2,1]])],
        (1,0): [(0, [[0,0,-1],[1,0,1]])],
        (1,1): [], (1,2): [],
        (2,0): [(1, [[0,0,1],[1,0,-1],[2,0,1]])],
        (2,1): [], (2,2): []}
    for s,t in product(range(3),repeat=2):
        candidates = []
        for bottom in product((0,1),repeat=7):
            ar = propagate(A,bottom,(s,t))
            if ar is None:
                continue
            rs = [r for r in range(3) if all(bottom[a]==int(a%3==r) for a in range(3,7))]
            require(len(rs)==1, 'left stencil has no unique right phase')
            r = rs[0]
            delta = changes(ar,phase(A,r))
            require(all(a<=2 and b<=2 for a,b,_ in delta), 'left support is not local')
            require(sum(x[2] for x in delta)>=0, 'negative left bubble')
            candidates.append({'phase':r,'bottom':list(bottom),'changes':delta,'size_difference':sum(x[2] for x in delta)})
        actual = sorted((z['phase'],z['changes']) for z in candidates)
        require(actual==sorted(expected[s,t]), 'unexpected left pattern')
        out.append({'defect':[s,t],'bottom_words_checked':128,'candidates':candidates})
    return out

def suffix_checks():
    lo, hi = 3**7, 2*3**7
    cutoffs = [x for x in smooth_below(hi) if x>=lo]
    require(cutoffs==[2187,2304,2592,2916,3072,3456,3888,4096], 'wrong normalized cutoffs')
    out = []
    for X, upper in zip(cutoffs,cutoffs[1:]+[hi]):
        A = widths(X)
        require(A[7]==0 and len(A)==8, 'wrong normalized shape')
        for r in range(3):
            base = phase(A,r)
            base_count = adjusted_count(A,r)
            configs = []
            tested = 0
            for s in range(4,A[0]):
                for t in range(3):
                    if s>A[t+1]:
                        continue
                    for tail in product((0,1),repeat=A[0]-4):
                        bottom = base[0][:5]+list(tail)
                        if any(bottom[a] for a,b in isolated(A) if b==0):
                            continue
                        tested += 1
                        ar = propagate(A,bottom,(s,t))
                        if ar is None:
                            continue
                        require(all(ar[b][0]==base[b][0] for b in range(len(A))), 'suffix leaks through its left column')
                        delta = sum(map(sum,ar))-base_count
                        epsilon = int(X==3072 and r==0)
                        require(delta>=-epsilon, 'suffix exceeds exceptional saving')
                        configs.append({'defect':[s,t],'tail':list(tail),'size_difference':delta,
                                        'left_column_agrees':True,'changes_from_raw_phase':changes(ar,base)})
            require(configs, 'empty suffix phase case')
            out.append({'interval':[X,upper],'widths':A,'phase':r,'tested':tested,
                        'minimum_difference':min(z['size_difference'] for z in configs),
                        'feasible_count':len(configs),'configurations':configs})
    require(sum(z['size_difference']<0 for case in out for z in case['configurations'])==1,
            'expected exactly one normalized improving configuration')
    return out

@lru_cache(None)
def initial_masks(h):
    # Any column with two adjacent 11 pairs already violates D<=1.
    return tuple(m for m in range(1<<h) if (m & (m>>1)).bit_count()<=1)

def exact_q1(X):
    A = widths(X)
    hs = [sum(w>=a for w in A) for a in range(A[0]+1)]
    # State (last-column mask, used excess), value (cost, witness masks).
    dp = {(m,0):(m.bit_count(),(m,)) for m in initial_masks(hs[0])}
    counts = [len(dp)]
    for h,k in zip(hs,hs[1:]+[0]):
        require(k in (h,h-1), 'unexpected column height decrease')
        nd = {}
        for (m,d),(cost,path) in dp.items():
            mandatory, optional, pair_excess = 0, [], 0
            for b in range(h-1):
                pair = ((m>>b)&1)+((m>>(b+1))&1)
                if pair==0:
                    mandatory |= 1<<b
                elif pair==1:
                    optional.append(1<<b)
                else:
                    pair_excess += 1
            remaining = 1-d-pair_excess
            if remaining<0:
                continue
            options = [(mandatory,0)]
            if remaining:
                options += [(mandatory|bit,1) for bit in optional]
            top_options = [0,1<<(h-1)] if k==h else [0]
            for low,extra in options:
                for top in top_options:
                    n, used = low|top, d+pair_excess+extra
                    require(n<1<<k, 'transition mask out of range')
                    key, new_cost = (n,used), cost+n.bit_count()
                    if key not in nd or new_cost<nd[key][0]:
                        nd[key] = (new_cost,path+(n,))
        dp = nd
        counts.append(len(dp))
    q,d,path = min((cost,d,path) for (mask,d),(cost,path) in dp.items() if mask==0)
    H = {(a,b) for a,mask in enumerate(path[:-1]) for b in range(hs[a]) if (mask>>b)&1}
    hits = [len(H&set(e)) for e in edges(A)]
    require(len(H)==q and all(h>=1 for h in hits) and sum(h-1 for h in hits)==d, 'bad exact witness')
    return {'q1':q,'defect':d,'selected_smooth_numbers':sorted(2**a*3**b for a,b in H),
            'state_counts':counts}

def candidate(X):
    A = widths(X)
    colors = [adjusted_count(A,r) for r in range(3)]
    adjusted = colors[:]
    m,p = 0,1
    while 24*p<=X:
        if X<27*p:
            adjusted[(m+2)%3] -= 1
        m,p = m+1,2*p
    return colors, adjusted

def finite_checks():
    cutoffs = smooth_below(3**18)
    require(len(cutoffs)==280, 'wrong finite cutoff count')
    out = []
    for X in cutoffs:
        answer = exact_q1(X)
        colors,adjusted = candidate(X)
        require(answer['q1']==min(adjusted), 'finite q1 mismatch at '+str(X))
        out.append({'cutoff':X,'colors':colors,'adjusted_colors':adjusted,**answer})
    return out

def verify_certificate(provided, expected):
    # The expected object is freshly recomputed by all exhaustive recurrences.
    # Complete equality also forbids omissions, altered witnesses, and unknown fields.
    require(type(provided) is dict, 'certificate is not an object')
    require(provided==expected, 'certificate differs from exhaustive recomputation')

def rejection_controls(expected):
    controls = []
    mutations = []
    wrong = copy.deepcopy(expected)
    wrong['interior_stencils'][0]['survivors'] = [[0]*8]
    mutations.append(('fabricated_interior_feasibility',wrong))
    wrong = copy.deepcopy(expected)
    del wrong['suffix_cases'][0]['configurations'][0]['left_column_agrees']
    mutations.append(('missing_suffix_interface_invariant',wrong))
    wrong = copy.deepcopy(expected)
    wrong['suffix_cases'][0]['configurations'][0]['size_difference'] = -2
    mutations.append(('fabricated_extra_suffix_saving',wrong))
    wrong = copy.deepcopy(expected)
    wrong['finite_cutoffs'][0]['q1'] += 1
    mutations.append(('wrong_small_scale_minimum',wrong))
    for name,wrong in mutations:
        try:
            verify_certificate(wrong,expected)
        except RuntimeError:
            controls.append({'name':name,'rejected':True})
        else:
            raise RuntimeError('negative control was accepted: '+name)
    verify_certificate(copy.deepcopy(expected),expected)
    return controls

if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',type=Path,help='recompute and reject any mismatch in this certificate; do not overwrite it')
    args = parser.parse_args()
    result = {'status':'PASS','artifact_type':'new exact reconstruction, not restored historical bytes',
              'scope':'All-scale q1 formula only when combined with proofs/04_SINGLE_DEFECT_THEOREM.md and the q0 structural proof.',
              'not_claimed':['unrestricted tau=q1','irrationality of the original density constant'],
              'interior_stencils':stencil_checks(),'left_stencils':left_checks(),
              'suffix_cases':suffix_checks(),'finite_cutoffs':finite_checks(),
              'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    result['rejection_controls'] = rejection_controls(result)
    if args.check:
        verify_certificate(json.loads(args.check.read_text()),result)
    print(json.dumps(result,indent=2,sort_keys=True))
