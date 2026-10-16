"""Independent closure-invariant checks. No author-checker imports.
Letters are integers: +/-i classical, 100+i virtual. Fox checks use rank of
a linear closure system; component/crossing checks use union-find of diagram
endpoints, rather than the author's color enumeration or permutation cycles.
These are falsification diagnostics, never completeness certificates.
"""
import collections, hashlib, itertools, json, pathlib, random

def idx(x): return x-100 if x>100 else abs(x)
def reverse(w): return tuple(x if x>100 else -x for x in reversed(w))
def shift(w): return tuple(x+1 if x>0 else x-1 for x in w)

def diagram(n,w):
    parent=list(range(n))
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]]; i=parent[i]
        return i
    strands=list(range(n)); events=[]
    for letter in w:
        i=idx(letter)-1
        assert 0<=i<n-1
        x,y=strands[i:i+2]
        if letter<=100:
            events.append((x,y,1) if letter>0 else (y,x,-1))
        strands[i:i+2]=[y,x]
    for position,top in enumerate(strands):
        parent[find(position)]=find(top)
    classes=sorted({find(i) for i in range(n)})
    at={c:k for k,c in enumerate(classes)}
    matrix=[[0]*len(classes) for _ in classes]
    for x,y,sign in events:
        a,b=at[find(x)],at[find(y)]
        if a!=b: matrix[a][b]+=sign
    return tuple(map(tuple,matrix))

def canonical(matrix):
    active=[i for i in range(len(matrix)) if any(matrix[i]) or any(row[i] for row in matrix)]
    if not active: return len(matrix),()
    return len(matrix),min(tuple(matrix[i][j] for i in p for j in p) for p in itertools.permutations(active))

def fox(n,w):
    rows=[[int(i==j) for j in range(n)] for i in range(n)]
    for x in w:
        assert x<=100
        i=abs(x)-1; left,right=rows[i:i+2]
        rows[i:i+2]=[[ (2*a-b)%3 for a,b in zip(left,right)],left] if x>0 else [right,[(2*b-a)%3 for a,b in zip(left,right)]]
    matrix=[[(rows[i][j]-int(i==j))%3 for j in range(n)] for i in range(n)]
    pivot=0
    for col in range(n):
        choose=next((r for r in range(pivot,n) if matrix[r][col]),None)
        if choose is None: continue
        matrix[pivot],matrix[choose]=matrix[choose],matrix[pivot]
        factor=pow(matrix[pivot][col],-1,3)
        matrix[pivot]=[factor*v%3 for v in matrix[pivot]]
        for r in range(n):
            if r!=pivot:
                factor=matrix[r][col]
                matrix[r]=[(x-factor*y)%3 for x,y in zip(matrix[r],matrix[pivot])]
        pivot+=1
    return 3**(n-pivot)

def endpoints(name,n,a,b,g):
    if name=='C': return (n,b),(n,a+b+reverse(a))
    if name=='BC': return (n,b+(n-1,)),(n,a+b+reverse(a)+(n-1,))
    if name=='T': return (n,b+(n-1,)),(n,b+(g,))
    if name=='D': return (n,b),(n+2,b+(g,n+1))
    if name=='R': return (n,a+(-(n-1),)+b+(n-1,)),(n,a+(100+n-1,)+b+(100+n-1,))
    if name=='L': return (n,shift(a)+(-1,)+shift(b)+(1,)),(n,shift(a)+(101,)+shift(b)+(101,))
    if name=='BR': return (n,a+(-(n-2),)+b+(n-2,n-1)),(n,a+(100+n-2,)+b+(100+n-2,n-1))
    if name=='BL': return (n,shift(a)+(-1,)+shift(b)+(1,n-1)),(n,shift(a)+(101,)+shift(b)+(101,n-1))
    raise ValueError(name)

def main():
    rng=random.Random(5092026)
    checked=collections.Counter(); foxchecked=collections.Counter()
    for virtual in (False,True):
        names=('C','BC','T','D')+(('R','L','BR','BL') if virtual else ())
        for n in (2,4,6):
            for name in names:
                if name in ('BR','BL') and n==2: continue
                bound=n-1 if name in ('C','D') else n-3 if name in ('BR','BL') else n-2
                alphabet=tuple(range(1,bound+1))+tuple(range(-bound,0))+(tuple(range(101,101+bound)) if virtual else ())
                words=[()]+[(x,) for x in alphabet]
                if n<=4: words += list(itertools.product(alphabet,repeat=2))
                if alphabet: words += [tuple(rng.choice(alphabet) for _ in range(rng.randint(3,8))) for _ in range(10)]
                pairs=itertools.product(words,repeat=2) if name in ('C','BC','R','L','BR','BL') else (((),b) for b in words)
                for a,b in pairs:
                    terminal=n if name=='D' else n-1
                    gs=(terminal,-terminal)+( (100+terminal,) if virtual else ()) if name in ('T','D') else (0,)
                    for g in gs:
                        e=endpoints(name,n,a,b,g)
                        left,right=(canonical(diagram(*x)) for x in e)
                        assert left==right, ('ordered crossing invariant',virtual,name,n,a,b,g,e,left,right)
                        checked[('virtual_' if virtual else 'classical_')+name]+=1
                        if not virtual:
                            assert fox(*e[0])==fox(*e[1]), ('Fox',name,n,a,b,g)
                            foxchecked[name]+=1
    controls={
        'illicit_T': {'fox_counts':[fox(2,(1,1,1)),fox(2,(1,))]},
        'illicit_R': {'matrices':[diagram(2,(1,1)),diagram(2,(1,101,1,101))]},
        'illicit_BR': {'matrices':[diagram(4,(2,2,3)),diagram(4,(2,102,2,102,3))]},
        'idle_padding': {'components':[len(diagram(1,())),len(diagram(2,()))]},
        'BL_buffer_omission': {'components':[len(diagram(3,(-1,1))),len(diagram(4,(-1,1)))]},
    }
    assert controls['illicit_T']['fox_counts']==[9,3]
    assert canonical(controls['illicit_R']['matrices'][0])!=canonical(controls['illicit_R']['matrices'][1])
    assert canonical(controls['illicit_BR']['matrices'][0])!=canonical(controls['illicit_BR']['matrices'][1])
    assert controls['idle_padding']['components']==[1,2]
    assert controls['BL_buffer_omission']['components']==[3,4]
    output={'status':'PASS_INDEPENDENT_CLOSURE_INVARIANT_FALSIFICATION',
            'scheme_instances':dict(sorted(checked.items())), 'total_scheme_instances':sum(checked.values()),
            'fox_instances':dict(sorted(foxchecked.items())), 'total_fox_instances':sum(foxchecked.values()),
            'controls':controls,'author_checker_imports':False,
            'limitations':['Closure invariants are necessary, not sufficient, for equivalence',
                           'Universal completeness is the written edge-lifting proof, not finite sampling']}
    print(json.dumps(output,indent=2,sort_keys=True))

if __name__=='__main__': main()
