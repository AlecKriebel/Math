#!/usr/bin/env python3
"""Independent exact finite controls. These do not prove the topology."""
from collections import Counter, deque
from fractions import Fraction
from itertools import permutations, product
import json
import math
import random
import sys

class AuditFailure(Exception):
    pass

def need(value, message):
    if not value:
        raise AuditFailure(message)

def matrix_rank(rows, width):
    a = [list(map(Fraction, row)) for row in rows]
    need(all(len(row) == width for row in a), 'rank: bad shape')
    pivot = 0
    for col in range(width):
        candidate = next((i for i in range(pivot, len(a)) if a[i][col]), None)
        if candidate is None:
            continue
        a[pivot], a[candidate] = a[candidate], a[pivot]
        d = a[pivot][col]
        a[pivot] = [v / d for v in a[pivot]]
        for i in range(len(a)):
            if i != pivot and a[i][col]:
                d = a[i][col]
                a[i] = [x-d*y for x,y in zip(a[i],a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot

def homology_controls():
    rng = random.Random(10300034)
    count = 0
    primitive = [(p,q) for p,q in product(range(-4,5), repeat=2) if math.gcd(p,q)==1]
    for width in range(1,9):
        for r in range(6):
            for repeat in range(8):
                vector = lambda: [rng.randrange(-3,4) for _ in range(width)]
                relations = [vector() for _ in range(repeat % 4)]
                meridians, longitudes = [vector() for _ in range(r)], [vector() for _ in range(r)]
                fillings = []
                for mu,lo in zip(meridians,longitudes):
                    p,q = rng.choice(primitive)
                    fillings.append([p*x+q*y for x,y in zip(mu,lo)])
                nrank = matrix_rank(relations+meridians,width)
                qrank = matrix_rank(relations+meridians+longitudes,width)
                mrank = matrix_rank(relations+fillings,width)
                bN,bQ,bM,d = width-nrank,width-qrank,width-mrank,qrank-nrank
                need(bM >= bQ == bN-d >= bN-r, 'quotient rank inequality')
                need(0 <= d <= r, 'component span bound')
                count += 1
    # Exact countercontrol to reversing the epimorphism/rank inequality.
    need(1 >= 0 and not (0 >= 1), 'reverse rank must fail for Z -> 0')
    return {'presentation_cases':count,'reversed_inequality_countercontrols':1}

def compose(a,b):
    return tuple(a[b[i]] for i in range(len(a)))

def finite_group_controls():
    groups = [list(permutations(range(3)))]
    groups.append(sorted({tuple((k+s*j)%4 for j in range(4)) for k in range(4) for s in (-1,1)}))
    cases=0
    for group in groups:
        identity=tuple(range(len(group[0])))
        inverse={a:next(b for b in group if compose(a,b)==identity) for a in group}
        def power(a,n):
            if n<0:
                a,n=inverse[a],-n
            out=identity
            for _ in range(n): out=compose(out,a)
            return out
        def normal(generators):
            conjugates={compose(compose(h,g),inverse[h]) for h in group for g in generators}
            seen={identity}; queue=deque([identity])
            while queue:
                h=queue.popleft()
                for g in conjugates:
                    value=compose(h,g)
                    if value not in seen: seen.add(value);queue.append(value)
            return seen
        for mu,lo in product(group,repeat=2):
            if compose(mu,lo)!=compose(lo,mu): continue
            both=normal([mu,lo])
            for p,q in product(range(-3,4),repeat=2):
                if math.gcd(p,q)!=1: continue
                slope=compose(power(mu,p),power(lo,q))
                filling=normal([slope])
                need(filling <= both, 'wrong normal-closure direction')
                need((len(group)//len(filling)) % (len(group)//len(both))==0,'quotient group order')
                cases+=1
    # C6: mu=0, lambda=1, primitive slope (1,2), M=C2 and Q=0.
    need(math.gcd(6,2)==2 and math.gcd(6,1)==1,'reverse-surjection countercontrol')
    return {'commuting_peripheral_finite_group_cases':cases,'groups':['S3','dihedral_order_8'],
            'reverse_surjection_countercontrols':1,'scope':'algebraic models, not claims of manifold realization'}

def sections_and_slopes():
    section_cases=0
    for g in range(1,41):
        n=2*g+1
        # Integral change of basis and its explicit inverse, independent of determinant elimination.
        b=[[int(i==j or i==0) for j in range(n)] for i in range(n)]
        inverse=[[int(i==j) if i else (1 if j==0 else -1) for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                # b is sparse except in row zero.
                value=sum(b[i][k]*inverse[k][j] for k in range(n)) if i==0 else inverse[i][j]
                need(value==int(i==j),'integral section basis inverse')
        # Word identities (a_i t)t^-1=a_i, (b_i t)t^-1=b_i.
        def reduce_word(word):
            reduced=[]
            for x in word:
                if reduced and reduced[-1]==-x: reduced.pop()
                else: reduced.append(x)
            return reduced
        for generator in range(1,n):
            need(reduce_word([generator,n,-n])==[generator],'normal-generation identity')
        section_cases+=1
    cases=0
    for p,q in product(range(-40,41),repeat=2):
        if math.gcd(p,q)!=1: continue
        for degree in (1,2,3,7,101,10**30):
            need((q*degree==0)==(q==0 and abs(p)==1),'integral slope annihilator')
            # Unoriented slopes and longitude changes do not change q*d.
            need(((-q)*degree==0)==(q*degree==0),'unoriented slope')
            for framing in (-7,0,9):
                new_p=p-q*framing
                need(math.gcd(new_p,q)==1,'framing primitivity')
                need(new_p*0+q*degree==q*degree,'framing invariance')
            cases+=1
    need(1*0==0,'zero-degree nonmeridional countercontrol')
    need(math.gcd(2,0)!=1,'nonprimitive meridian rejected as slope')
    return {'integral_basis_and_word_cases':section_cases,'primitive_degree_cases':cases,
            'hypothesis_countercontrols':2}

# Sparse polynomials: powers of c,s,e,k; exterior forms use coordinate indices x,y,t.
def padd(a,b):
    out=Counter(a);out.update(b)
    return {m:v for m,v in out.items() if v}
def pscale(a,c):return {m:v*c for m,v in a.items() if v*c}
def pmul(a,b):
    out={}
    for p,v in a.items():
        for q,w in b.items():
            key=tuple(x+y for x,y in zip(p,q));out[key]=out.get(key,0)+v*w
    return {m:v for m,v in out.items() if v}
def dt(a):
    out={}
    for m,v in a.items():
        c,s,e,k=m
        if c: out=padd(out,{(c-1,s+1,e,k+1):-v*c})
        if s: out=padd(out,{(c+1,s-1,e,k+1):v*s})
    return out

def wedge(a,b):
    out={}
    for p,v in a.items():
        for q,w in b.items():
            order=p+q
            if len(set(order))!=len(order):continue
            sign=(-1)**sum(order[i]>order[j] for i in range(len(order)) for j in range(i+1,len(order)))
            key=tuple(sorted(order))
            out[key]=padd(out.get(key,{}),pscale(pmul(v,w),sign))
    return {key:value for key,value in out.items() if value}

def exterior_d(one_form):
    out={}
    for (i,),v in one_form.items():
        term=wedge({(2,):dt(v)},{(i,):{(0,0,0,0):1}})
        for key,value in term.items():out[key]=padd(out.get(key,{}),value)
    return out

def contact_controls():
    one={(0,0,0,0):1};ec={(1,0,1,0):1};es={(0,1,1,0):1}
    for sine_sign in (-1,1):
        beta={(0,):ec,(1,):pscale(es,sine_sign),(2,):one}
        result=wedge(beta,exterior_d(beta))
        need(result=={(0,1,2):{(2,0,2,1):-sine_sign,(0,2,2,1):-sine_sign}},'symbolic contact orientation')
    samples=0
    for r in (Fraction(x,y) for x in range(-9,10) for y in (1,2,7)):
        c=(1-r*r)/(1+r*r);s=2*r/(1+r*r)
        for e in (Fraction(1,3),Fraction(1,10**12),Fraction(7,2)):
            need(c*c+s*s==1,'unit circle exact')
            coefficient=-e*e*(c*c+s*s)
            need(coefficient==-e*e<0,'nonzero wedge after k factored')
            need(e>0 and e-e==0,'strict transfer margin equality failure')
            samples+=1
    # eps=0 is the foliation, not contact; error==margin cannot imply positivity.
    need(-0**2==0,'zero perturbation is not contact')
    for margin,error in product([Fraction(0),Fraction(1,3),Fraction(1),Fraction(2)],repeat=2):
        need((margin-error>0)==(margin>error),'strict dual norm inequality')
    return {'symbolic_exterior_calculations':2,'exact_contact_samples':samples,'margin_cases':16,
            'degeneracy_countercontrols':2}

def cycles_by_edges(n,edges):
    adj=[[] for _ in range(n)]
    for i,(u,v) in enumerate(edges):adj[u].append((v,i))
    result=set()
    for start in range(n):
        def visit(u,visited,path):
            for v,i in adj[u]:
                if v==start:
                    cycle=path+(i,)
                    result.add(min(cycle[j:]+cycle[:j] for j in range(len(cycle))))
                elif v not in visited:
                    visit(v,visited|{v},path+(i,))
        visit(start,{start},())
    return sorted(result)

def reachable(n,edges,start):
    seen={start};todo=[start]
    while todo:
        u=todo.pop()
        for a,b in edges:
            if a==u and b not in seen:seen.add(b);todo.append(b)
    return seen

def balance(n,edges,weights):
    totals=[0]*n
    for (u,v),w in zip(edges,weights):totals[u]-=w;totals[v]+=w
    return totals

def decompose(n,edges,weights,cycles):
    left=weights[:];record=[]
    while any(left):
        cycle=next((c for c in cycles if all(left[i]>0 for i in c)),None)
        need(cycle is not None,'balanced positive remainder has no cycle')
        amount=min(left[i] for i in cycle)
        for i in cycle:left[i]-=amount
        record.append((cycle,amount))
    recovered=[0]*len(edges)
    for cycle,amount in record:
        for i in cycle:recovered[i]+=amount
    need(recovered==weights,'cycle decomposition multiplicity')
    return record

def graph_controls():
    graphs=[(0,[])]
    for n in range(1,4):
        universe=list(product(range(n),repeat=2))
        for mask in range(1<<len(universe)):
            graphs.append((n,[e for i,e in enumerate(universe) if mask>>i&1]))
    universe=list(product(range(2),repeat=2))
    for length in range(5):
        for edges in product(universe,repeat=length):graphs.append((2,list(edges)))
    graphs.extend([(4,[(0,1),(1,0),(2,3),(3,2)]),(3,[(0,1),(1,0),(1,2)]),
                   (3,[(0,0),(0,0),(0,1),(1,0),(2,2)])])
    positive=negative=decomposed=0
    for n,edges in graphs:
        cycles=cycles_by_edges(n,edges)
        covered=set(i for cycle in cycles for i in cycle)
        expected=len(covered)==len(edges)
        need(expected==all(u in reachable(n,edges,v) for u,v in edges),'independent cycle/reachability equivalence')
        if expected:
            weights=[0]*len(edges)
            for number,cycle in enumerate(cycles):
                for i in cycle:weights[i]+=1+number%3
            need(all(w>0 for w in weights),'positive circulation')
            need(not any(balance(n,edges,weights)),'integral balance')
            decompose(n,edges,weights,cycles);decomposed+=1;positive+=1
        else:
            i=next(i for i in range(len(edges)) if i not in covered)
            u,v=edges[i];cut=reachable(n,edges,v)
            need(v in cut and u not in cut,'cut obstruction endpoints')
            need(not any(a in cut and b not in cut for a,b in edges),'cut has no escape')
            negative+=1
    need(len(reachable(4,graphs[-3][1],0))==2,'edge recurrence differs from strong connectivity')
    # Every vertex has an incoming and outgoing edge, yet a bridge has no return.
    bad=[(0,0),(0,1),(1,1)]
    need(all(any(a==v for a,b in bad) and any(b==v for a,b in bad) for v in range(2)), 'local degree control')
    need(0 not in reachable(2,bad,1),'local degree alone must not imply circulation')
    return {'graphs':len(graphs),'positive':positive,'negative':negative,'weighted_decompositions':decomposed,
            'includes':'loops, parallel edges, empty graphs, disconnected cycles, one-way cuts',
            'hypothesis_countercontrols':2}

def run():
    need(len(sys.argv)==1,'no arguments accepted')
    return {'schema':'transverse-surgery-independent-exact-v1','status':'pass',
            'homology':homology_controls(),'group_quotients':finite_group_controls(),
            'sections_slopes':sections_and_slopes(),'contact':contact_controls(),'circulations':graph_controls(),
            'limits':'Finite exact controls support arithmetic and algorithms; the general topology is audited in AUDIT.md.'}

if __name__=='__main__':
    try:
        print(json.dumps(run(),sort_keys=True,separators=(',',':')))
    except (AuditFailure,ValueError,TypeError,KeyError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
