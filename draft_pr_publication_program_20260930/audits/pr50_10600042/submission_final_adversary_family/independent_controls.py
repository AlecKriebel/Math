#!/usr/bin/env python3
"""Independent final-review diagnostics; no author module imported.
Uses integer words, union-find closure components and finite-field matrix rank.
This tests finite instances and countercontrols, not the imported Markov theorem.
"""
from itertools import product, permutations
from collections import Counter
import json, random

checks = 0
def need(ok, why):
    global checks
    if not ok: raise AssertionError(why)
    checks += 1

def ix(c): return c-1000 if c > 1000 else abs(c)
def virt(c): return c > 1000
def inverse(w): return tuple(c if virt(c) else -c for c in w[::-1])
def shift(w): return tuple(c+1 if c>0 else c-1 for c in w)
def valid(n,w): return n >= 1 and all(1 <= ix(c) < n for c in w)
def padding(state):
    n,w=state
    return (n+1,w+(n,)) if n%2 else state

def partition(n,w):
    labels=list(range(n)); parent=list(range(n))
    def find(x):
        while x!=parent[x]:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    for c in w:
        i=ix(c)-1; labels[i],labels[i+1]=labels[i+1],labels[i]
    for i,j in enumerate(labels): parent[find(i)]=find(j)
    blocks={}
    for i in range(n): blocks.setdefault(find(i),[]).append(i)
    return sorted(blocks.values())

def crossing_matrix(n,w):
    blocks=partition(n,w); members={x:i for i,b in enumerate(blocks) for x in b}
    labels=list(range(n)); out=[[0]*len(blocks) for _ in blocks]
    for c in w:
        i=ix(c)-1; x,y=labels[i:i+2]
        if not virt(c):
            over,under=(x,y) if c>0 else (y,x)
            a,b=members[over],members[under]
            if a!=b: out[a][b] += 1 if c>0 else -1
        labels[i],labels[i+1]=y,x
    return tuple(tuple(row) for row in out)

def matrix_signature(mat):
    n=len(mat)
    if n<=5:
        return min(tuple(mat[p[i]][p[j]] for i in range(n) for j in range(n)) for p in permutations(range(n)))
    # A weaker necessary invariant at larger component count, explicitly not an isomorphism oracle.
    return tuple(sorted(Counter(x for row in mat for x in row).items()))

def color_matrix(n,w,q):
    out=[[int(i==j) for j in range(n)] for i in range(n)]
    for c in w:
        i=ix(c)-1; x,y=out[i:i+2]
        if virt(c): a,b=y,x
        elif c>0: a,b=[(2*xj-yj)%q for xj,yj in zip(x,y)],x
        else: a,b=y,[(2*yj-xj)%q for xj,yj in zip(x,y)]
        out[i],out[i+1]=a,b
    return out

def colors(n,w,q):
    a=color_matrix(n,w,q)
    for i in range(n): a[i][i]=(a[i][i]-1)%q
    rank=0
    for j in range(n):
        pick=next((i for i in range(rank,n) if a[i][j]%q),None)
        if pick is None: continue
        a[rank],a[pick]=a[pick],a[rank]
        scale=pow(a[rank][j],-1,q)
        a[rank]=[(x*scale)%q for x in a[rank]]
        for i in range(n):
            if i==rank: continue
            factor=a[i][j]
            a[i]=[(x-factor*y)%q for x,y in zip(a[i],a[rank])]
        rank+=1
    return q**(n-rank)

def brute_colors(n,w,q):
    mat=color_matrix(n,w,q)
    return sum(all(sum(a*b for a,b in zip(row,x))%q==x[i] for i,row in enumerate(mat))
               for x in product(range(q),repeat=n))

def schemes(name,n,a,b,g=()):
    # This transcription uses integer words and has no dependence on the author implementation.
    if name=='C': return (n,b),(n,a+b+inverse(a))
    if name=='BC': return (n,b+(n-1,)),(n,a+b+inverse(a)+(n-1,))
    if name=='T': return (n,b+(n-1,)),(n,b+g)
    if name=='D': return (n,b),(n+2,b+g+(n+1,))
    if name in ('R','BR'):
        k=n-1 if name=='R' else n-2
        tail=() if name=='R' else (n-1,)
        return (n,a+(-k,)+b+(k,)+tail),(n,a+(1000+k,)+b+(1000+k,)+tail)
    if name in ('L','BL'):
        tail=() if name=='L' else (n-1,)
        return (n,shift(a)+(-1,)+shift(b)+(1,)+tail),(n,shift(a)+(1001,)+shift(b)+(1001,)+tail)
    raise ValueError(name)

def main():
    rng=random.Random(501026)
    def word(k,v,length):
        alphabet=list(range(1,k+1))+list(range(-k,0))
        if v: alphabet+=list(range(1001,1001+k))
        return tuple(rng.choice(alphabet) for _ in range(length)) if alphabet else ()
    cover=Counter(); legal=0; lifted=0; relations=0
    for virtual in (False,True):
        for n in (2,4,6,8,10):
            names=('C','BC','T','D')+(('R','L','BR','BL') if virtual else ())
            for name in names:
                if name in ('BR','BL') and n<4: continue
                limit=n-1 if name in ('C','D') else n-3 if name in ('BR','BL') else n-2
                for t in range(40):
                    a,b=word(limit,virtual,t%7),word(limit,virtual,(3*t)%11)
                    k=n if name=='D' else n-1
                    opts=(k,-k,1000+k) if virtual else (k,-k)
                    g=(opts[t%len(opts)],)
                    if name in ('T','D'): a=()
                    left,right=schemes(name,n,a,b,g)
                    need(all(m%2==0 and valid(m,w) for m,w in (left,right)), 'actual endpoint tags/support')
                    need(len(partition(*left))==len(partition(*right)), 'closure component soundness')
                    for q in (3,5,7): need(colors(*left,q)==colors(*right,q), 'independent rank-color soundness')
                    need(matrix_signature(crossing_matrix(*left))==matrix_signature(crossing_matrix(*right)), 'ordered crossing necessary invariant')
                    cover[('virtual_' if virtual else 'classical_')+name]+=1; legal+=1
    # Lift original generators separately: source parity determines family, not inference from examples.
    for m in range(1,18):
        for virtual in (False,True):
            for t in range(7):
                a,b=word(m-1,virtual,t),word(m-1,virtual,6-t)
                old=((m,b),(m,a+b+inverse(a)))
                n=m+m%2
                need(tuple(map(padding,old))==schemes('BC' if m%2 else 'C',n,a,b), 'conjugation lift')
                need(tuple(map(padding,old))[::-1]==schemes('BC' if m%2 else 'C',n,a,b)[::-1], 'conjugation reverse')
                lifted+=1
                for g in ((m,),(-m,))+(((1000+m,),) if virtual else ()):
                    old=((m,b),(m+1,b+g))
                    got=tuple(map(padding,old))
                    need(got==schemes('T' if m%2 else 'D',n,(),b,g), 'stabilization lift')
                    need(max(x[0] for x in got)==2*((m+2)//2), 'stabilization height')
                    lifted+=1
                if virtual and m>=2:
                    a,b=word(m-2,True,t),word(m-2,True,6-t)
                    for side in ('R','L'):
                        old=schemes(side,m,a,b)
                        need(tuple(map(padding,old))==schemes(('B'+side) if m%2 else side,n,a,b), 'both exchange lifts')
                        lifted+=1
    # Every relation family, arbitrary contexts and inverses: matrix and syntactic lift checks.
    for m in range(1,9):
        pairs=[]
        for i in range(1,m): pairs += [((i,-i),()),((-i,i),()),((1000+i,1000+i),())]
        for i in range(1,m-1):
            pairs += [((i,i+1,i),(i+1,i,i+1)),
                      ((1000+i,1001+i,1000+i),(1001+i,1000+i,1001+i)),
                      ((i,1001+i,1000+i),(1001+i,1000+i,i+1))]
        for i in range(1,m):
            for j in range(i+2,m):
                pairs += [((i,j),(j,i)),((1000+i,1000+j),(1000+j,1000+i)),
                          ((i,1000+j),(1000+j,i)),((j,1000+i),(1000+i,j))]
        for lhs,rhs in pairs:
            for u,v in ((lhs,rhs),(rhs,lhs),(inverse(lhs),inverse(rhs))):
                left,right=word(m-1,True,3),word(m-1,True,4)
                old=((m,left+u+right),(m,left+v+right))
                tail=(m,) if m%2 else ()
                need(tuple(map(padding,old))==((m+m%2,left+u+right+tail),(m+m%2,left+v+right+tail)), 'whole context and tail')
                for q in (3,5,7): need(color_matrix(m,old[0][1],q)==color_matrix(m,old[1][1],q), 'defining relation matrix equality')
                relations+=1
    # Validate rank counting against literal assignments on independent small cases.
    for n in range(1,4):
        for t in range(12):
            w=word(n-1,True,t%6)
            for q in (3,5): need(colors(n,w,q)==brute_colors(n,w,q), 'rank algorithm vs exhaustive assignments')
    negatives={
        'enlarged_T_Fox3': [colors(2,(1,)*3,3),colors(2,(1,),3)],
        'new_enlarged_T_Fox5': [colors(2,(1,)*5,5),colors(2,(1,)*3,5)],
        'idle_strand_padding': [len(partition(1,())),len(partition(2,()))],
        'ordinary_vs_plat': [len(partition(2,())),1],
    }
    for label,(a,b) in negatives.items(): need(a!=b,label)
    badR=(crossing_matrix(2,(1,1)),crossing_matrix(2,(1,1001,1,1001)))
    need(matrix_signature(badR[0])!=matrix_signature(badR[1]), 'illegal R exact ordered obstruction')
    badBR=(crossing_matrix(4,(2,2,3)),crossing_matrix(4,(2,1002,2,1002,3)))
    need(matrix_signature(badBR[0])!=matrix_signature(badBR[1]), 'illegal BR exact ordered obstruction')
    need(padding((1,()))==(2,(1,)), 'one-strand empty unknot')
    need(schemes('L',2,(),())[0][1]==(-1,1) and schemes('L',2,(),())[1][1]==(1001,1001), 'N2 left exchange trivial words')
    # Positive padding fixes every even word exactly; no negative-tail or shifted-tail replacement hidden.
    for m in range(1,102):
        need(m+m%2==2*((m+1)//2), 'vertex height formula')
        if m%2==0: need(padding((m,()))==(m,()), 'even endpoint fixed')
    print(json.dumps({'status':'PASS_INDEPENDENT_FINAL_CONTROLS','checks':checks,
                      'legal_scheme_cases':legal,'lifted_edge_cases':lifted,
                      'relation_context_cases':relations,'scheme_coverage':dict(sorted(cover.items())),
                      'negative_controls':negatives,'illegal_R_matrices':badR,'illegal_BR_matrices':badBR,
                      'limits':['Finite diagnostics, not universal theorem proof',
                                'Rank-color and crossing invariants are necessary only',
                                'At more than five components the crossing signature is weaker than full relabeling',
                                'No author code or previous reviewer code imported']},indent=2,sort_keys=True))

if __name__=='__main__': main()
