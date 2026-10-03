#!/usr/bin/env python3
"""Independent, standard-library adversarial controls for the frozen packet.
Does not import or alter the submitted verifier. All results are finite controls.
Run from any directory: python3 independent_verify.py --check
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
from random import Random
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT.parent / 'public'
FROZEN_MANIFEST = '0da4275483e2fdf0f0cd170feb85bf7148ed7a45d8dda16a9427c10fa326aea0'

def field(q):
    # The only extension field used is F_9=F_3[t]/(t^2+1).
    if q == 9:
        add = lambda x,y: (x%3+y%3)%3 + 3*((x//3+y//3)%3)
        mul = lambda x,y: ((x%3)*(y%3)-(x//3)*(y//3))%3 + 3*(((x%3)*(y//3)+(x//3)*(y%3))%3)
    else:
        add = lambda x,y: (x+y)%q
        mul = lambda x,y: (x*y)%q
    A = [[add(x,y) for y in range(q)] for x in range(q)]
    M = [[mul(x,y) for y in range(q)] for x in range(q)]
    neg = [next(y for y in range(q) if A[x][y]==0) for x in range(q)]
    inv = [0] + [next(y for y in range(1,q) if M[x][y]==1) for x in range(1,q)]
    return A,M,neg,inv

FIELDS = {q:field(q) for q in (3,5,7,9)}

def matrix(n,E,weights,q):
    neg = FIELDS[q][2]
    B = [[0]*n for _ in range(n)]
    for (u,v),a in zip(E,weights): B[u][v], B[v][u] = a,neg[a]
    return B

def pfaffian_rank(B,q):
    # Independent of the submission's Gaussian elimination: examine all
    # principal Pfaffians, computing each by its defining matching expansion.
    A,M,neg,_ = FIELDS[q]
    @lru_cache(None)
    def pf(S):
        if not S: return 1
        u,*rest = S
        value = 0
        for j,v in enumerate(rest):
            if not B[u][v]: continue
            term = M[B[u][v]][pf(tuple(rest[:j]+rest[j+1:]))]
            value = A[value][neg[term] if j%2 else term]
        return value
    n=len(B)
    for k in range(n//2,0,-1):
        if any(pf(S) for S in combinations(range(n),2*k)):return 2*k
    return 0

def row_rank(B,q):
    A,M,neg,inv = FIELDS[q]
    basis = {}
    for original in B:
        row=list(original)
        for j in sorted(basis):
            if row[j]:
                a=row[j]
                row=[A[x][neg[M[a][y]]] for x,y in zip(row,basis[j])]
        j=next((j for j,a in enumerate(row) if a),None)
        if j is not None:
            scale=inv[row[j]]
            basis[j]=[M[x][scale] for x in row]
    return len(basis)

def comps(n,E,S,complement=False):
    # Disjoint-set counting, distinct from the submitted flood fill.
    S=list(S); parent={v:v for v in S}; edges=set(E)
    def find(v):
        while parent[v]!=v:v=parent[v]
        return v
    for u,v in combinations(S,2):
        if (((u,v) in edges) != complement):parent[find(u)]=find(v)
    return len({find(v) for v in S})

def rank_two_value(n,E,q):
    total=0
    for mask in range(1,1<<n):
        S=[v for v in range(n) if mask>>v&1]
        c=comps(n,E,S,True)
        total+=(q-1)**len(S)*((q+1)**c-(q+1))
    assert total%(q*(q*q-1))==0
    return total//(q*(q*q-1))

def class_value(n,E,q):
    total=0
    for mask in range(1<<n):
        S={v for v in range(n) if mask>>v&1}; N=set(S)
        for u,v in E:
            if u in S:N.add(v)
            if v in S:N.add(u)
        total+=(q-1)**len(S)*q**(len(E)-len(N)+comps(n,E,S))
    return total

def match_number(n,E):
    # Brute force matching backtracking by edges, with vertex-bit pruning.
    best=0
    def rec(i,used,count):
        nonlocal best
        best=max(best,count)
        if count+(n-used.bit_count())//2<=best:return
        for j in range(i,len(E)):
            u,v=E[j]; pair=(1<<u)|(1<<v)
            if not used&pair:rec(j+1,used|pair,count+1)
    rec(0,0,0)
    return best

def special_cases():
    return {
      'C6':(6,[(i,i+1) for i in range(5)]+[(0,5)]),
      'C6_chord':(6,[(i,i+1) for i in range(5)]+[(0,5),(0,3)]),
      'two_triangles':(6,[(0,1),(1,2),(0,2),(3,4),(4,5),(3,5)]),
      'path7_two_chords':(7,[(i,i+1) for i in range(6)]+[(0,3),(2,6)]),
      'star8':(8,[(0,i) for i in range(1,8)]),
      'cover_three_8':(8,[(0,3),(0,4),(0,5),(1,4),(1,6),(1,7),(2,3),(2,6),(2,7)]),
      'matching4':(8,[(0,1),(2,3),(4,5),(6,7)])
    }

def replay(r):
    selected={}
    def check(n,E,q):
        hist=Counter(); nu=match_number(n,E)
        forest=(len(E)==n-comps(n,E,range(n)))
        for weights in product(range(q),repeat=len(E)):
            rank=pfaffian_rank(matrix(n,E,weights,q),q)
            hist[rank//2]+=1
            assert rank<=2*nu
            if forest:
                support=[e for e,a in zip(E,weights) if a]
                assert rank==2*match_number(n,support)
                r['independent_forest_weightings']+=1
            r['independent_alternating_matrices']+=1
        assert hist[0]==1 and sum(hist.values())==q**len(E)
        assert hist[1]==rank_two_value(n,E,q)
        K=class_value(n,E,q)
        assert sum(count*q**(n-2*i) for i,count in hist.items())==K
        if nu<=3:
            T=q**len(E)-1-hist[1]
            if nu<=1:assert T==0
            elif nu==2:assert hist[2]==T
            else:
                H=K-q**n-q**(n-2)*hist[1]
                numerator=H-q**(n-6)*T;denominator=q**(n-6)*(q*q-1)
                assert numerator%denominator==0
                assert hist[2]==numerator//denominator and hist[3]==T-hist[2]
            r['independent_recovery_cases']+=1
        r['independent_graph_field_cases']+=1
        return dict(sorted(hist.items()))
    for n in range(1,5):
        all_edges=list(combinations(range(n),2))
        for mask in range(1<<len(all_edges)):
            E=[e for j,e in enumerate(all_edges) if mask>>j&1]
            for q in (3,5):check(n,E,q)
    for name,(n,E) in special_cases().items():selected[name]=check(n,E,3)
    submitted=json.loads((PUBLIC/'VERIFICATION.json').read_text())
    assert json.loads(json.dumps(selected))==submitted['selected_distributions']
    for own,theirs in [('independent_alternating_matrices','matrices_enumerated'),('independent_forest_weightings','forest_weightings_checked'),('independent_graph_field_cases','graph_field_cases'),('independent_recovery_cases','polynomial_recovery_checks')]:
        assert r[own]==submitted[theirs]
    r['selected_distributions']=selected
    return check

def centralizer_controls(r):
    cases=[]
    for n in range(1,5):
        edges=list(combinations(range(n),2))
        for mask in range(1<<len(edges)):
            E=[e for j,e in enumerate(edges) if mask>>j&1]
            for q in (3,5):cases.append((n,E,q))
    cases.extend((n,E,3) for n,E in special_cases().values())
    cases.extend([(3,[(0,1),(1,2)],9),(3,[(0,1),(0,2),(1,2)],9),(4,[(0,1),(0,3),(1,2),(2,3)],9)])
    for n,E,q in cases:
        neg=FIELDS[q][2];total=0
        for vector in product(range(q),repeat=n):
            C=[]
            for u,v in E:
                row=[0]*n;row[u],row[v]=neg[vector[v]],vector[u];C.append(row)
            k=row_rank(C,q);S={j for j,a in enumerate(vector) if a};N=set(S)
            for u,v in E:
                if u in S:N.add(v)
                if v in S:N.add(u)
            assert k==len(N)-comps(n,E,S)
            total+=q**(len(E)-k)
            r['centralizer_vectors_checked']+=1
        assert total==class_value(n,E,q)
        r['centralizer_graph_field_cases']+=1

def representation_controls(r):
    # Compose actual monomial operator data, then compare with the group product.
    for q in (3,5):
        half=pow(2,-1,q)
        operator={(x,y,z):[((t+x)%q,(z+y*t+half*x*y)%q) for t in range(q)] for x,y,z in product(range(q),repeat=3)}
        for g,h in product(operator,repeat=2):
            x,y,z=g; u,v,w=h
            gh=((x+u)%q,(y+v)%q,(z+w+half*(x*v-y*u))%q)
            G,H,GH=operator[g],operator[h],operator[gh]
            for t in range(q):
                next_t,phase=G[t]; final_t,next_phase=H[next_t]
                assert (final_t,(phase+next_phase)%q)==GH[t]
                r['independent_phase_checks']+=1
    # F_9: trace pairing, additive-character indexing, and all Heisenberg pairs.
    q=9; A,M,N,I=FIELDS[q];half=I[2]
    trace=lambda x:(2*(x%3))%3
    chars={tuple(trace(M[a][x]) for x in range(q)) for a in range(q)}
    assert len(chars)==q
    for a in range(1,q): assert Counter(trace(M[a][x]) for x in range(q))=={0:3,1:3,2:3}
    ops={(x,y,z):[(A[t][x], trace(A[A[z][M[y][t]]][M[half][M[x][y]]])) for t in range(q)] for x,y,z in product(range(q),repeat=3)}
    for g,h in product(ops,repeat=2):
        x,y,z=g; u,v,w=h
        comm=A[M[x][v]][N[M[y][u]]]
        gh=(A[x][u],A[y][v],A[A[z][w]][M[half][comm]])
        G,H,GH=ops[g],ops[h],ops[gh]
        for t in range(q):
            next_t,phase=G[t];final_t,next_phase=H[next_t]
            assert (final_t,(phase+next_phase)%3)==GH[t]
            r['extension_field_phase_checks']+=1


def fibre_controls(r):
    for q,n in ((3,5),(5,3),(9,3)):
        A,M,N,_=FIELDS[q]
        fibres=Counter()
        edges=list(combinations(range(n),2))
        for values in product(range(q),repeat=2*n):
            x,y=values[:n],values[n:]
            gram=tuple(A[M[x[u]][y[v]]][N[M[x[v]][y[u]]]] for u,v in edges)
            if any(gram):fibres[gram]+=1
            r['factorizations_inspected']+=1
        assert set(fibres.values())=={q*(q*q-1)}
        assert len(fibres)==rank_two_value(n,edges,q)
        r['rank_two_fibres_checked']+=len(fibres)
        # Check the complement-component formula for every subgraph on n vertices.
        # Gram supports determine every admissible graph at once.
        by_support=Counter()
        for gram in fibres:
            mask=sum((1<<j) for j,a in enumerate(gram) if a)
            by_support[mask]+=1
        for mask in range(1<<len(edges)):
            E=[e for j,e in enumerate(edges) if mask>>j&1]
            actual=sum(count for support,count in by_support.items() if support&~mask==0)
            assert actual==rank_two_value(n,E,q)
            r['fibre_graph_formula_checks']+=1


def rectangular_pivot_controls(r):
    for q in (3,5):
        neg=FIELDS[q][2]
        for vals in product(range(q),repeat=6):
            M=[vals[:3],vals[3:]]
            B=[[0]*5 for _ in range(5)]
            for u in range(2):
                for v in range(3):B[u][v+2],B[v+2][u]=M[u][v],neg[M[u][v]]
            assert pfaffian_rank(B,q)==2*row_rank(M,q)
            r['independent_bipartite_checks']+=1
    for a in (1,2):
        for u,v,w,x,c in product(range(3),repeat=5):
            B=matrix(4,[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],(a,u,v,w,x,c),3)
            residual=(c+(w*v-u*x)*pow(a,-1,3))%3
            assert pfaffian_rank(B,3)==2+2*bool(residual)
            r['independent_pivot_checks']+=1

# Independent dense coefficient arithmetic for symbolic divisibility controls.
def trim(p):
    p=list(p)
    while len(p)>1 and p[-1]==0:p.pop()
    return p

def plus(p,q):
    out=[0]*max(len(p),len(q))
    for i,c in enumerate(p):out[i]+=c
    for i,c in enumerate(q):out[i]+=c
    return trim(out)

def times(p,q):
    out=[0]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):out[i+j]+=a*b
    return trim(out)

def negpoly(p):return [-c for c in p]
def monomial(k):return [0]*k+[1]
def peval(p,q):
    v=0
    for c in reversed(p):v=v*q+c
    return v

POWERS=[[1]]
for i in range(14):POWERS.append(times(POWERS[-1],[-1,1]))

def graph_polys(n,E):
    P=[0]; K=[0];m=len(E)
    for mask in range(1<<n):
        S=[v for v in range(n) if mask>>v&1];N=set(S)
        for u,v in E:
            if u in S:N.add(v)
            if v in S:N.add(u)
        exponent=m-len(N)+comps(n,E,S)
        assert exponent>=0
        K=plus(K,[0]*exponent+POWERS[len(S)])
        if S:
            c=comps(n,E,S,True)
            if c>=2:
                # ((Q+1)^(c-1)-1)/Q via multiplication, not binomials.
                inner=[1]
                for _ in range(c-1):inner=times(inner,[1,1])
                inner[0]-=1
                assert inner[0]==0
                P=plus(P,times(POWERS[len(S)-1],inner[1:]))
    return P,K

def monic_divide(A,B):
    A=trim(A);B=trim(B);assert B[-1]==1
    quotient=[0]*max(1,len(A)-len(B)+1)
    while len(A)>=len(B) and A!=[0]:
        k=len(A)-len(B);c=A[-1];quotient[k]=c
        for j,b in enumerate(B):A[j+k]-=c*b
        A=trim(A)
    assert A==[0]
    return trim(quotient)

def polynomial_controls(r):
    rng=Random(30004773)
    examples=[]
    # Every labelled graph with six vertices: all possible matching caps <=3.
    n=6;all_edges=list(combinations(range(n),2))
    for mask in range(1<<len(all_edges)):
        examples.append((n,[e for j,e in enumerate(all_edges) if mask>>j&1]))
    # Seven vertices, and larger graphs with a specified three-vertex cover.
    for n,count in ((7,256),(8,64),(9,64),(10,32),(12,4)):
        available=[e for e in combinations(range(n),2) if n==7 or e[0]<3]
        for _ in range(count):examples.append((n,[e for e in available if rng.randrange(2)]))
    for n,E in examples:
        P,K=graph_polys(n,E)
        T=plus(plus(monomial(len(E)),[-1]),negpoly(P))
        H=plus(plus(K,negpoly(monomial(n))),negpoly([0]*(n-2)+P))
        d=n-6
        denominator=[0]*d+[-1,0,1]
        N2=monic_divide(plus(H,negpoly([0]*d+T)),denominator)
        N3=monic_divide(plus([0]*(d+2)+T,negpoly(H)),denominator)
        assert plus(N2,N3)==T
        for q in (3,5,9):assert all(peval(p,q)>=0 for p in (P,N2,N3))
        r['independent_polynomial_divisibility_graphs']+=1


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    assert hashlib.sha256((PUBLIC/'MANIFEST.sha256').read_bytes()).hexdigest()==FROZEN_MANIFEST
    frozen={name:digest for digest,name in [line.split('  ',1) for line in (PUBLIC/'MANIFEST.sha256').read_text().splitlines()]}
    assert frozen=={name:hashlib.sha256((PUBLIC/name).read_bytes()).hexdigest() for name in frozen}
    r={key:0 for key in ['independent_alternating_matrices','independent_graph_field_cases','independent_forest_weightings','independent_phase_checks','extension_field_phase_checks','factorizations_inspected','rank_two_fibres_checked','fibre_graph_formula_checks','independent_bipartite_checks','independent_pivot_checks','independent_polynomial_divisibility_graphs','centralizer_vectors_checked','centralizer_graph_field_cases','independent_recovery_cases']}
    check=replay(r)
    print('Independent 83,201-matrix replay passed.',flush=True)
    centralizer_controls(r)
    rectangular_pivot_controls(r)
    representation_controls(r)
    print('Independent representation, bipartite, and pivot controls passed.',flush=True)
    fibre_controls(r)
    print('Independent projective-fibre controls passed.',flush=True)
    before=r['independent_alternating_matrices'];before_cases=r['independent_graph_field_cases'];before_forest=r['independent_forest_weightings'];before_recovery=r['independent_recovery_cases']
    for n,E,q in [(0,[],3),(1,[],9),(2,[(0,1)],9),(4,[(0,1),(0,3),(1,2),(2,3)],9),(6,[(0,1),(2,3),(4,5)],9),(6,[(i,i+1) for i in range(5)],9)]:check(n,E,q)
    r['supplementary_matrices']=r['independent_alternating_matrices']-before
    r['supplementary_recovery_cases']=r['independent_recovery_cases']-before_recovery
    r['independent_recovery_cases']=before_recovery
    r['supplementary_forest_weightings']=r['independent_forest_weightings']-before_forest
    r['independent_forest_weightings']=before_forest
    r['supplementary_graph_field_cases']=r['independent_graph_field_cases']-before_cases
    r['independent_alternating_matrices']=before;r['independent_graph_field_cases']=before_cases
    print('Extension-field and empty-graph controls passed.',flush=True)
    polynomial_controls(r)
    print('Independent symbolic polynomial controls passed.',flush=True)
    assert frozen=={name:hashlib.sha256((PUBLIC/name).read_bytes()).hexdigest() for name in frozen}
    assert hashlib.sha256((PUBLIC/'MANIFEST.sha256').read_bytes()).hexdigest()==FROZEN_MANIFEST
    submitted=json.loads((PUBLIC/'VERIFICATION.json').read_text())
    assert r['independent_phase_checks']==submitted['schrodinger_phase_checks']
    assert r['independent_bipartite_checks']==submitted['bipartite_rank_checks']
    assert r['independent_pivot_checks']==submitted['schur_complement_checks']
    r.update(status='PASS',frozen_manifest_sha256=FROZEN_MANIFEST,arithmetic='Exact integer, F_3, F_5, and F_9 arithmetic',scope='Finite audit controls; no proof of a general solution or historical novelty.')
    receipt=ROOT/'INDEPENDENT_VERIFICATION.json'
    data=json.dumps(r,indent=2,sort_keys=True)+'\n'
    if args.check:
        assert json.loads(receipt.read_text())==json.loads(data)
        print('PASS: independent audit receipt reproduced exactly.')
    else:receipt.write_text(data);print(data,end='')

if __name__=='__main__':main()
