"""Exact mixed-sign two-occurrence checks; accompanying proof is in ../proofs/03_mixed_two.md."""
import itertools,json
from collections import Counter
import sympy as S

def parity(p):
    return (-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))

def run():
    bs=S.symbols('b0:9'); B=S.Matrix(3,3,bs)
    ps=S.symbols('P0:3');qs=S.symbols('Q0:3')
    lhs=S.trace(S.diag(*ps)*B*S.diag(*qs)*B.adjugate())
    rhs=0
    for perm in itertools.permutations(range(3)):
        mon=S.prod(B[i,perm[i]] for i in range(3))
        rhs+=parity(perm)*mon*sum(ps[i]*qs[perm[i]] for i in range(3))
    assert S.expand(lhs-rhs)==0
    seen={};count=0
    for p,q in itertools.product([-3,-2,-1,1,2,3],repeat=2):
        trans=tuple(sorted(Counter([(p,q,0),(q,p,0),(0,0,p+q)]).items()))
        cycle=tuple(sorted(Counter([(p,q,0),(0,p,q),(q,0,p)]).items()))
        sig=(p+q,trans,cycle)
        assert sig not in seen or seen[sig]==(p,q)
        seen[sig]=(p,q);count+=1
    A=S.diag(2,3,S.Rational(1,6))
    b=S.Matrix([[1,1,1],[1,2,3],[0,1,3]])
    assert b.det()==A.det()==1
    traces=[S.trace(A*b*A.inv()*b.inv()),S.trace(A.inv()*b*A*b.inv())]
    assert traces[0]!=traces[1]
    return {'status':'PASS','generic_adjugate_identity':True,'ordered_gap_signature_cases':count,
            'example':{'A_diagonal':['2','3','1/6'],'B':[[int(t) for t in row] for row in b.tolist()],
                       'words':['abAB','AbaB'],'traces':list(map(str,traces))},
            'scope':'Checks for the proved unbounded two-occurrence subfamily, not the full target'}

if __name__=='__main__':print(json.dumps(run(),indent=2))
