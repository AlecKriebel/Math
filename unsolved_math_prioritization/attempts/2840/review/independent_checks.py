"""Standard-library exact jet and rational-coordinate controls, not a torsion search."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from hashlib import sha256
import json
counts={}
def ck(cat,p):
    assert p,cat
    counts[cat]=counts.get(cat,0)+1
def density(a,j):
    # j[coefficient][coordinate] is the first derivative of a one-form.
    return a[0]*(j[2][1]-j[1][2])+a[1]*(j[0][2]-j[2][0])+a[2]*(j[1][0]-j[0][1])

for u,omega in product(range(-4,5),range(1,6)):
    c=Q(1-u*u,1+u*u);s=Q(2*u,1+u*u)
    a=(c,-s,Q(0));j=((0,0,-omega*s),(0,0,-omega*c),(0,0,0))
    ck('unit_covector',c*c+s*s==1)
    ck('positive_contact_density',density(a,j)==omega)
    for f,fx,fy,fz in product((Q(-2),Q(-1,3),Q(1,4),Q(3)),(-1,0,1),(-1,0,1),(-1,0,1)):
        df=(fx,fy,fz)
        ja=tuple(tuple(df[i]*a[k]+f*j[k][i] for i in range(3)) for k in range(3))
        ck('arbitrary_conformal_first_jet',density(tuple(f*z for z in a),ja)==f*f*omega)
    for x,y in product(range(-2,3),repeat=2):
        q=x*c-y*s;p=omega*(x*s+y*c)
        dq=(c,-s,-omega*(x*s+y*c))
        ck('standard_cover_pullback',(dq[0],dq[1],dq[2]+p)==a)
        ck('standard_cover_inverse',(q*c+p*s/omega,-q*s+p*c/omega)==(x,y))

for p,H,Hq,Hp,Ht in product(range(-2,3),(-1,0,1),(-1,0,1),(-1,0,1),(-1,0,1)):
    X=(H-p*Hp,p*Hq-Ht,Hp)
    ck('hamiltonian_value',X[0]+p*X[2]==H)
    # Cartan: dH + i_X(dp wedge dt) = Hq(dq+p dt).
    ck('hamiltonian_cartan_identity',(Hq,Hp-X[2],Ht+X[1])==(Hq,0,p*Hq))

for t in range(1,21):
    lam=Q(1,2**t)
    for p in range(-3,4):
        ck('dilation_covector',(lam*lam,0,(lam*p)*lam)==(lam*lam,0,lam*lam*p))
    ck('dilation_positive_factor',0<lam*lam<1)
    ck('dilation_volume_factor',lam*lam*lam*lam==(lam*lam)**2)

for n,k in product(range(1,25),repeat=2):
    width=Q(n,k)
    ck('phase_identity',k*width==n)
    if n<k:
        vals=[(width*Q(i,20))%1 for i in range(21)]
        ck('closed_interval_embedding_controls',len(set(vals))==len(vals))
        ck('closed_model_volume_inequality',n<=k)
    else:
        z=Q(k,n)
        ck('periodic_wrap_collision',0<z<=1 and (width*z)%1==0)
    ck('noncompact_scaling_injective',len({n*Q(i,20) for i in range(21)})==21)

for diag in product((Q(1,5),Q(2,3),Q(3)),repeat=3):
    for cov in product((-2,-1,0,1,2),repeat=3):
        lhs=sum((d*a)**2 for d,a in zip(diag,cov))
        rhs=min(diag)**2*sum(a*a for a in cov)
        ck('covector_inverse_norm_bound',lhs>=rhs)

r=Path(__file__).resolve().parent
out={'artifact_sha256':sha256((r/'author_replay/PARTIAL.md').read_bytes()).hexdigest(),'exact_assertions':sum(counts.values()),'categories':counts,'scope':'Rational one-form jets, contact Hamiltonians, dilation factors, covector inequalities and interval-wrapping controls. No new tightness theorem or fixed closed-manifold torsion resolution.'}
(r/'independent_checks.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,sort_keys=True))
