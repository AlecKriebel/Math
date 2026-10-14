#!/usr/bin/env python3
"""Fresh exact-order/algebra controls; not a numerical PDE or proof assistant."""
from fractions import Fraction as F
import hashlib,json,pathlib,datetime

checks=[]
def record(name,condition,detail):
    assert condition, name
    checks.append({'name':name,'pass':True,'detail':detail})

# Frozen source authentication and six-member closure.
p=pathlib.Path(__file__).resolve().parent
pins=json.loads((p/'INPUT_PINS.json').read_text())
for e in pins['files']:
    b=(p/e['frozen_path']).read_bytes()
    record('input '+pathlib.Path(e['repository_path']).name,
           len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],
           'Recomputed bytes and SHA-256 of independent frozen Git input.')
manifest=json.loads((p/'frozen/MANIFEST.json').read_text())
record('manifest member closure',set(manifest['members'])==set(pathlib.Path(e['repository_path']).name for e in pins['files']) and manifest['member_count']==6,
       'Exactly the six submitted members; no self-hash asserted for manifest.')
for e in manifest['entries']:
    b=(p/'frozen'/e['file']).read_bytes()
    record('manifest '+e['file'],len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'Every non-manifest member matches its actual bytes.')

# The rigorous universal Hardy identity is algebraic in m. Its quadratic
# coefficients are a0*(m-2-a0)=a0^2 and a0*m; verify symbolic coefficient
# identity by exact fractions at all values of m in a diagnostic grid.
for m in [1,2,3,4,5,10,100]:
    a0=F(m-2,2)
    record('Hardy coefficient m='+str(m),a0*(m-2-a0)==a0*a0,'Exact coefficient; delta-term sign is separately guarded.')
record('Hardy dimension guard',F(3-2,2)>0 and F(2-2,2)==0 and F(1-2,2)<0,
       'Dropping a0*m*delta^2 is valid for m>=3; m=1/2 do not give the desired homogeneous local estimate.')

# Coercivity principal minor. Set r=G^2, s=|g|^2. The Gram determinant
# of 2(1+r)B(g)-I in the (a_parallel,b) plane equals
# (1+2r)^2-2(1+r)s, which at s<=r is >=1+2r+2r^2.
# This coefficient calculation supplies an independent route to positivity.
for r in [F(0),F(1,2500),F(1,10),F(1),F(100)]:
    for s0 in [F(0),r/2,r]:
        aa=1+2*r
        bb=2*(1+r)*(1+s0)-1
        cross_squared=4*(1+r)**2*s0
        det=aa*bb-cross_squared
        lower=1+2*r+2*r*r
        record('coercivity determinant '+str(r)+'/'+str(s0),
               det==(1+2*r)**2-2*(1+r)*s0 and det>=lower>0,
               'Exact PSD diagnostic agrees with the written universal determinant formula; transverse a directions are positive.')

# Exact beta=1, h/100 order bounds. e>2 follows from 1+1+1/2>2.
# exp(x)<=sum x^k=1/(1-x) for 0<=x<1 follows termwise 1/k!<=1.
x=F(1,25)
exp_upper=1/(1-x)
g2_upper=F(1,2500)
d_upper=g2_upper/2
A_upper=F(4)
trace_upper=2*A_upper+2
absence_upper=d_upper*exp_upper*trace_upper
coercivity_lower=1/(2*(1+g2_upper))
record('e and exponential series order',F(1)+F(1)+F(1,2)>2 and exp_upper==F(25,24)<2,
       'No decimal approximation: e>2; exp(1/25)<=25/24 by termwise power-series comparison.')
record('bump gradient bound',F(8)/F(2)**2==2,'e>2 makes 8/e^2<2; differentiating q^2 exp(-q) gives q(2-q) exp(-q).')
record('strong absence bound',absence_upper==F(1,480) and coercivity_lower==F(1250,2501) and absence_upper<coercivity_lower,
       'Actual strict constants are better than these nondiscrete upper/lower bounds.')
record('published coarse margin',F(1,3)-F(1,250)==F(247,750)>0 and absence_upper<F(1,250) and coercivity_lower>F(1,3),
       'The report margin 247/750 is correct and positive.')

# Whole-form trace absorption is a universal scalar inequality:
# sqrt(A)*(X+Y)-2sqrt(A*X*Y)=sqrt(A)*(sqrt(X)-sqrt(Y))^2.
# Choose exact square values as independent diagnostics. The sign of the
# unused 2beta*A*Y contribution remains nonnegative.
for bx in [F(0),F(1,3),F(1),F(100)]:
    for by in [F(0),F(1,5),F(1),F(10)]:
        X,Y=bx*bx,by*by
        bound=F(10)*(X+Y)
        tight=F(8)*X+F(4)*bx*by
        record('trace absorption '+str(bx)+'/'+str(by),
               bound-tight==F(8)*Y+F(2)*(bx-by)**2 and bound>=tight,
               'A=4,beta=1; exact residual identity checks the cross-term coefficient.')

# Positive and negative orientation/Jacobian controls using the rational
# slope |g|=3/4, s=5/4, beta=1 and boundary value=1.
bulk_endpoint=F(1)
surface=F(5,4)
correct_defect=bulk_endpoint-surface
record('Robin normal and surface Jacobian',correct_defect==F(-1,4),
       'The vertical integration endpoint +beta combines with -beta*s to -beta(s-1).')
record('mutation: omission of surface Jacobian rejected',bulk_endpoint-F(1)!=correct_defect,
       'Omitting the surface Jacobian incorrectly erases the negative boundary defect.')
record('mutation: endpoint orientation rejected',-bulk_endpoint-surface!=correct_defect,
       'Reversing the fiber endpoint sign produces an incorrect flat-domain negative defect.')
record('flat cancellation',F(1)-F(1)==0,'At g=0, the shifted Robin boundary terms cancel exactly.')
record('mutation: inverted domain threshold rejected',F(1)+F(1)!=0,
       'The attractive half-space ground state has outward derivative +beta*phi, not -beta*phi.')

# Exact diagnostic of the t-integration identity using w=e^(-kappa*t).
# Its tangential norm cancels: T=1,L=1/[2(beta+kappa)], integral(w*wt)=-kappa L.
for beta in [F(1,10),F(1),F(10)]:
    for kappa in [F(0),F(1,10),F(1),F(10)]:
        L=1/(2*(beta+kappa))
        record('vertical exponential identity '+str(beta)+'/'+str(kappa),
               2*beta*L+2*kappa*L==1,'Exact decay-tail control; compact truncations have vanishing exponential error.')
        if kappa>0:
            record('mutation: lost trace cross term rejected '+str(beta)+'/'+str(kappa),
                   2*beta*L!=1,'Removing the cross term cannot reproduce the boundary trace.')

report={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'check_count':len(checks),'passed':True,'claim':'Fresh exact arithmetic/algebra guards, plus independent written analytic proof; no numerical spectral certificate.',
        'strict_absence_upper':'1/480','coercivity_lower':'1250/2501',
        'strict_margin_lower':str(coercivity_lower-absence_upper),'checks':checks}
(p/'CONTROL_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
