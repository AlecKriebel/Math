"""Independent presentation controls; requires SymPy. No Floer computation."""
from pathlib import Path
from itertools import product
import hashlib,json
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
root=Path(__file__).resolve().parent
EXPECTED='c064e0d83d682f206098835741553c946bd9f62efaddc4c6ebe5aee42a186522'
assert hashlib.sha256((root/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest()==EXPECTED
counts={}
def ck(v,k):
    assert bool(v),k
    counts[k]=counts.get(k,0)+1
def invs(M):
    D=smith_normal_form(M,domain=s.ZZ)
    return tuple(abs(D[i,i]) for i in range(min(D.rows,D.cols)))

# Include both internal torsion relations and genuine free summands.
for seed in range(72):
    rx=[0,2,3,4][seed%4]; ry=[0,2,5][(seed//4)%3]
    R=s.diag(rx,0,ry,6 if seed%2 else 0)
    A=s.Matrix(2,4,lambda i,j:((seed+3*i+2*j)%7)-3)
    B=s.Matrix(2,4,lambda i,j:((2*seed+i+3*j)%9)-4)
    P=R.row_join(A.col_join(-B))
    Pm=R.row_join(A.col_join(B))
    U=s.diag(1,1,-1,-1)
    V=s.diag(1,1,-1,-1,1,1,1,1)
    ck(U*P==Pm*V,'integral_presentation_intertwiner')
    ck(abs(U.det())==abs(V.det())==1,'unimodular_changes')
    ck(invs(P)==invs(Pm),'smith_factors_with_torsion_and_free_parts')
    ck(P.applyfunc(lambda x:x%2)==Pm.applyfunc(lambda x:x%2),'mod_two_presentations')

# Explicit finite-group quotient check, without matrix normal forms.
mods=(2,3,4,5)
G=list(product(*(range(m) for m in mods)))
def add(x,y):return tuple((a+b)%m for a,b,m in zip(x,y,mods))
def negY(x):return (x[0],x[1],(-x[2])%4,(-x[3])%5)
def generated(vs):
    out={(0,0,0,0)}; todo=[(0,0,0,0)]
    while todo:
        x=todo.pop()
        for v in vs:
            y=add(x,v)
            if y not in out:out.add(y);todo.append(y)
    return out
for seed in range(12):
    vs=[tuple((seed*(j+1)+i*i+2*j)%m for i,m in enumerate(mods)) for j in range(2)]
    H=generated(vs);Hm=generated([negY(v) for v in vs])
    ck({negY(v) for v in H}==Hm,'finite_relation_subgroup')
    for x in G:
        ck(negY(negY(x))==x,'finite_target_involution')
        ck((x in H)==(negY(x) in Hm),'finite_quotient_bijection')

# Wang-sequence action matrices for the two actual mapping tori in the proof.
I=s.eye(4);h=-I
ck(h*h==I and h.trace()==-4,'hyperelliptic_action_control')
ck(invs(I-I)==(0,0,0,0),'identity_mapping_torus_cokernel')
ck(invs(h-I)==(2,2,2,2),'involution_mapping_torus_cokernel')
ck((h-I).applyfunc(lambda x:x%2)==s.zeros(4),'mapping_tori_mod_two')
ck(s.Matrix([[1],[-1]]).rank()==1,'separating_H0_injectivity')

r={'all_pass':True,'assertions':sum(counts.values()),'counts':counts,
   'artifact_sha256':EXPECTED,
   'scope':'Integral and finite-group cokernel controls and mapping-torus action matrices only; no Floer ranks or executable geometric realization.'}
(root/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
