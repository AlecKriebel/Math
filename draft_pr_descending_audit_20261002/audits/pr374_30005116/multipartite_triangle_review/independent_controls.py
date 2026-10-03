"""Source-free exact controls, authored before opening candidate files."""
from fractions import Fraction as Q
from itertools import product, combinations
from math import prod

def densities(weights, edges):
    edges = {frozenset(e) for e in edges}
    def adj(i,j): return i != j and frozenset((i,j)) in edges
    p = sum(weights[i]*weights[j] for i,j in product(range(len(weights)),repeat=2) if adj(i,j))
    values = {'edge':p,'triangle':Q(0),'C4':Q(0),'paw':Q(0)}
    for labels in product(range(len(weights)),repeat=3):
        if all(adj(labels[i],labels[j]) for i,j in combinations(range(3),2)):
            values['triangle'] += prod(weights[i] for i in labels)
    for labels in product(range(len(weights)),repeat=4):
        deg=[sum(adj(labels[i],labels[j]) for j in range(4) if i!=j) for i in range(4)]
        term=prod(weights[i] for i in labels)
        if sorted(deg)==[2,2,2,2]: values['C4']+=term
        if sorted(deg)==[1,2,2,3]: values['paw']+=term
    return values

def mp(weights): return densities(weights, list(combinations(range(len(weights)),2)))

count=0
for m in range(2,10):
    for a in range(1,11):
        x=Q(10*(m-1)+a,10*m*(m-1))
        y=1-(m-1)*x
        if y < 0: continue
        w=[x]*(m-1)+[y]
        actual=mp(w)
        q=sum(z*z for z in w)
        expected=3*(q*q-sum(z**4 for z in w))
        assert actual['edge']==1-q and actual['C4']==expected
        count+=1
for r in range(2,15):
    assert 3*(Q(1,r)**2-r*Q(1,r)**4)==Q(3*(r-1),r**3)
    left=[Q(1,r)]*r
    right=[Q(1,r)]*r+[Q(0)]
    assert sum(z*z for z in left)==sum(z*z for z in right)
    assert sum(z**4 for z in left)==sum(z**4 for z in right)

weights=[Q(2,5),Q(3,10),Q(4,15),Q(1,30)]
paw=densities(weights,[(0,1),(0,2),(0,3),(1,2)])
canonical=mp([Q(2,5),Q(2,5),Q(1,5)])
assert {k:paw[k] for k in ['edge','triangle','C4']}=={k:canonical[k] for k in ['edge','triangle','C4']}
assert paw=={'edge':Q(16,25),'triangle':Q(24,125),'C4':Q(144,625),'paw':Q(16,625)}
assert canonical['paw']==0
print('Exact independent controls PASS')
print('Multipartite ordered-enumeration cases:',count)
print('Critical densities and zero-class junctions: 13 each')
print('Nonmultipartite tie:',{k:str(v) for k,v in paw.items()})
print('Edit fraction lower bound:',str(paw['paw']/6))

# General exact join identity controls for arbitrary 0/1 internal blocks.
join_cases=0
for internal_edges in [[],[(0,1)],[(0,1),(1,2)],[(0,1),(0,2),(1,2)]]:
    outer=[Q(1,5),Q(1,4)]
    s=1-sum(outer)
    hweights=[Q(1,6),Q(1,3),Q(1,2)]
    inside=densities(hweights,internal_edges)
    allweights=outer+[s*z for z in hweights]
    edges=[(0,1)]+[(i,j) for i in range(2) for j in range(2,5)]+[(i+2,j+2) for i,j in internal_edges]
    actual=densities(allweights,edges)
    osq=sum(z*z for z in outer)
    expected_c=6*outer[0]**2*outer[1]**2+6*s*s*(1-inside['edge'])*osq+s**4*inside['C4']
    expected_p=1-osq-s*s*(1-inside['edge'])
    assert actual['C4']==expected_c and actual['edge']==expected_p
    join_cases+=1
print('Arbitrary internal-block join identity cases:',join_cases)
print('External PDFs consulted by this executable: 0')
