"""Primary-first exact controls. Finite cases do not certify all-D assertions."""
from fractions import Fraction as Q
import json

def h(r, y, branch):
    z = y + branch
    return (2*z-r-1)/(r+4-2*r*z)

def dr_h(r, y, branch):
    z = y + branch
    n, d = 2*z-r-1, r+4-2*r*z
    return (-d-n*(1-2*z))/(d*d)

def dy_h(r,y,branch):
    z=y+branch
    n,d=2*z-r-1,r+4-2*r*z
    return (2*d+2*r*n)/(d*d)

results={}
cases=0
for r in [Q(-2,5), Q(-1,10),Q(0),Q(1,10),Q(2,5)]:
    for y in [Q(-1,2),Q(-1,3),Q(0),Q(1,3),Q(1,2)]:
        for branch in (0,1):
            x=h(r,y,branch)
            assert dr_h(r,y,branch)==(4*x*x-1)/(4-r*r)
            assert dr_h(r,y,branch)<=0
            assert Q(-1,2)<=x<=Q(1,2)
            assert 0<dy_h(r,y,branch)<=Q(3,4)
            cases+=1
    assert h(r,Q(-1,2),0)==Q(-1,2)
    assert h(r,Q(1,2),0)==-r/4
    assert h(r,Q(-1,2),1)==-r/4
    assert h(r,Q(1,2),1)==Q(1,2)
results['inverse_branch_exact_fraction_cases']=cases
results['inverse_parameter_identity']='d_r h=(4 h^2-1)/(4-r^2); 50 exact finite cases, not a symbolic universal proof'

# A symmetric density with a CDF plateau and a separate unbounded central law.
def plateau_cdf(x):
    if x<=Q(-1,2): return Q(0)
    if x<Q(-1,4): return 2*(x+Q(1,2))
    if x<=Q(1,4): return Q(1,2)
    if x<Q(1,2): return Q(1,2)+2*(x-Q(1,4))
    return Q(1)
assert plateau_cdf(Q(-1,4))==plateau_cdf(Q(1,4))==Q(1,2)
results['cdf_plateau']='u=2 on [-1/2,-1/4] union [1/4,1/2], zero elsewhere; CDF is constant on [-1/4,1/4]. This u is symmetric and thus in W0 by the primary-source symmetry argument.'
results['canonical_nondensity_lower_bound']='Every canonical kernel is >=1/2. Against the plateau law the L1 distance is >=(1/2)*(1/2)=1/4 from its central zero interval alone.'
results['unbounded_central_law']='u(x)=(1/(2 sqrt(2))) |x|^(-1/2) for x!=0. Its integral is one and it is symmetric; hence it is an admissible unbounded W0 density. The point value at zero is immaterial.'

# Label correlation is decisive even when both coordinate marginals agree.
independent={(0,0):Q(1,4),(0,1):Q(1,4),(1,0):Q(1,4),(1,1):Q(1,4)}
correlated={(0,0):Q(1,2),(0,1):Q(0),(1,0):Q(0),(1,1):Q(1,2)}
r1,r2,y=Q(0),Q(0),Q(0)
def x_for_labels(a,b): return h(r1,h(r2,y,b),a)
def second_moment(law): return sum(p*x_for_labels(*ab)**2 for ab,p in law.items())
assert second_moment(independent)!=second_moment(correlated)
results['correlated_label_second_moments']={
    'independent':str(second_moment(independent)),
    'perfectly_correlated':str(second_moment(correlated)),
    'meaning':'Both one-bit marginals are fair, while reconstructed second moments differ. This discrete finite control warns against replacing joint label laws by marginals; these terminal atoms are not asserted to belong to D.'}
print(json.dumps(results,indent=2,sort_keys=True))
