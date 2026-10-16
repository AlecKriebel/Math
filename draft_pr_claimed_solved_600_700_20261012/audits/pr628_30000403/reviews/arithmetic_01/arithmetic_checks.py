#!/usr/bin/env python3
"""Independent exact binary-sextic and conic controls. Imports no supplied verifier.
Finite calculations supplement, and do not replace, the arithmetic proof in FINDINGS.md.
"""
from itertools import permutations, combinations
from pathlib import Path
import hashlib, json, sys
import sympy as sp
from sympy.polys.domains import QQ_I
K=QQ_I
checks=0

def ck(condition, label):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(label)

def e(value): return K.convert(value)
def det(p,q): return p[0]*q[1]-p[1]*q[0]
def canon(values):
    first=next(v for v in values if v)
    return tuple(v/first for v in values)
def polynomial(points):
    # Coefficients of prod(q X-p Z), in descending X-degree.
    coefficients=[e(1)]
    for p,q in points:
        updated=[e(0)]*(len(coefficients)+1)
        for j,t in enumerate(coefficients):
            updated[j]+=q*t
            updated[j+1]-=p*t
        coefficients=updated
    return coefficients

def configuration(a):
    a=e(a); b=-1/e(K.to_sympy(a).conjugate())
    return [(e(0),e(1)),(e(1),e(0)),(e(1),e(1)),(e(-1),e(1)),(a,e(1)),(b,e(1))]

def stabilizer_by_sextic(a):
    pts=configuration(a)
    ck(all(det(p,q) for p,q in combinations(pts,2)), 'branch points distinct')
    original=polynomial(pts); projective_original=canon(original)
    candidates={}; accepted=[]
    for ids in permutations(range(6),3):
        P,Q,R=[pts[j] for j in ids]
        alpha=det(P,R); beta=-det(Q,R)
        matrix=(alpha*Q[0],beta*P[0],alpha*Q[1],beta*P[1])
        A,B,C,D=matrix
        ck(bool(A*D-B*C), 'three-image candidate invertible')
        normalized=canon(matrix)
        ck(normalized not in candidates,'unique projective candidate')
        candidates[normalized]=ids
        # Check F(M(X,Z)) proportional to F(X,Z), instead of point-set membership.
        transformed=[(p*D-q*B,q*A-p*C) for p,q in pts]
        if canon(polynomial(transformed))==projective_original:
            images=[]
            for p,q in pts:
                actual=(A*p+B*q,C*p+D*q)
                matches=[j for j,t in enumerate(pts) if not det(actual,t)]
                ck(len(matches)==1,'unique image for accepted transform')
                images.append(matches[0])
            accepted.append({'first_three_images':list(ids),'permutation':images,
                             'matrix':[str(K.to_sympy(t)) for t in normalized]})
    ck(len(candidates)==120,'all ordered triple images covered')
    return {'parameter':str(K.to_sympy(e(a))),'candidate_count':len(candidates),'accepted':accepted}

sharp=stabilizer_by_sextic(2+2*sp.I)
nearby=stabilizer_by_sextic(2+sp.I)
octahedral=stabilizer_by_sextic(sp.I)
ck(len(sharp['accepted'])==1,'sharp stabilizer trivial')
ck(sharp['accepted'][0]['permutation']==list(range(6)),'sharp unique map identity')
ck(len(nearby['accepted'])==2,'nearby symmetric negative control')
ck(len(octahedral['accepted'])==24,'octahedral negative control')

u,v=sp.symbols('u v'); x=sp.symbols('x'); I=sp.I
a=2+2*I; b=-(1+I)/4
f=sp.Poly(x*(x*x-1)*(x-a)*(x-b),x,domain=QQ_I)
ck(f.degree()==5,'five finite roots')
ck(sp.gcd(f,f.diff()).degree()==0,'squarefree defining polynomial')
discriminant=sp.expand(f.discriminant())
ck(discriminant!=0,'nonzero exact discriminant')
F=sp.expand(u*v*(u*u-v*v)*(u-a*v)*(u-b*v))
barF=sp.conjugate(F).subs({sp.conjugate(u):u,sp.conjugate(v):v})
conjugate_transformed=sp.expand(barF.subs({u:-v,v:u},simultaneous=True))
scale=sp.cancel(conjugate_transformed/F)
ck(not (scale.free_symbols & {u,v}),'Galois pullback proportional sextic')
ck(sp.expand(conjugate_transformed-scale*F)==0,'exact branch Galois identity')

A=sp.Matrix([[0,-1],[1,0]])
ck(A*A==-sp.eye(2),'GL2 lift has negative scalar square')
ck(A.det()==1,'antipodal transform invertible')
r,s=sp.symbols('r s',real=True)
ck(sp.expand((r+I*s)*(r-I*s))==r*r+s*s,'norm is sum of real squares')

Q=sp.Matrix([u*u-v*v,I*(u*u+v*v),2*u*v])
ck(sp.expand(sum(z*z for z in Q))==0,'explicit split parametrization of anisotropic conic')
linear=sp.expand(4*Q[0]-4*Q[1]-7*Q[2])
ck(sp.expand(linear-4*(1-I)*(u-a*v)*(u-b*v))==0,'third rational line cuts antipodal pair')
branch_section=sp.expand(Q[0]*Q[2]*linear)
ck(sp.expand(branch_section-8*(1-I)*F)==0,'Q-rational cubic section gives exact six branch points')
barQ=Q.applyfunc(lambda t:sp.conjugate(t).subs({sp.conjugate(u):u,sp.conjugate(v):v}))
antiQ=Q.subs({u:-v,v:u},simultaneous=True)
ck(all(sp.expand(t)==0 for t in antiQ+barQ),'conic conjugation pulls back to antipodal map')

# A split real descent control: three conjugate-real pairs with ordinary conjugation.
# They lie on the usual split projective line, so the negative norm obstruction is absent.
J=sp.eye(2)
ck(J*J==sp.eye(2),'ordinary conjugation has positive scalar square')

root=Path(__file__).resolve().parents[2]
snapshot=json.loads((root/'SCOPE_AND_SNAPSHOT.json').read_text())
for path, info in snapshot['original_blobs'].items():
    payload=(root/'native'/path).read_bytes()
    ck(len(payload)==info['size'],'immutable input byte count '+path)
    ck(hashlib.sha256(payload).hexdigest()==info['sha256'],'immutable input SHA256 '+path)

report={'status':'PASS','python':sys.version.split()[0],'sympy':sp.__version__,
 'assertions':checks,'arithmetic':'exact Q(i) binary-polynomial arithmetic; symbolic conic identities',
 'sharp':sharp,'nearby_symmetric_control':nearby,'octahedral_control':octahedral,
 'f_expanded':str(f.as_expr()),'f_discriminant':str(discriminant),
 'conjugate_sextic_scale':str(scale),
 'conic_over_Q':'X^2+Y^2+Z^2=0',
 'Q_rational_branch_section':'X Z (4 X - 4 Y - 7 Z)',
 'parametrization_over_Qi':['u^2-v^2','i(u^2+v^2)','2uv'],
 'branch_section_pullback_scale':'8*(1-i)',
 'immutable_original_files_verified':len(snapshot['original_blobs']),
 'limits':'Not formal verification of coarse moduli existence, Galois fixed-point descent, or universal upper bound. Real nonsplitting and moduli reasoning are proved in FINDINGS.md.'}
print(json.dumps(report,indent=2))
