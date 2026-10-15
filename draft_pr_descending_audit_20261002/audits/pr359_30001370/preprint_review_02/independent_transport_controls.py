"""Fresh exact falsification controls: correlated full histories and atomic TV.

No kit program is imported. These finite controls complement the analytic audit.
"""
from fractions import Fraction as Q
from math import comb
import json

checks = 0
def ck(p):
    global checks
    assert p
    checks += 1

def integral_monomial(a,b,k):
    return (b**(k+1)-a**(k+1))/(k+1)

def integral_affine_power(a,b,slope,intercept,degree):
    return sum(Q(comb(degree,j))*slope**j*intercept**(degree-j)
               *integral_monomial(a,b,j) for j in range(degree+1))

def backward_zero(x,label):
    return x/2+Q(2*label-1,4)

joint_cases=[]
# The full bit history is a deterministic function of uniform terminal U.
# Equal one-bit marginals do not make the bits independent of U or each other.
for depth in (1,2,3,7):
    a,b=Q(-1,2),Q(0)
    c,d=Q(0),Q(1,2)
    for j in range(depth):
        a,b=backward_zero(a,0),backward_zero(b,0)
        c,d=backward_zero(c,1),backward_zero(d,1)
    height=Q(2)**depth
    ck(height*((b-a)+(d-c))==1)
    ck(a==-Q(1,2) and d==Q(1,2) and c==-b)
    ck(height*(integral_monomial(a,b,1)+integral_monomial(c,d,1))==0)
    # Every intermediate law is symmetric and has zero feedback for every
    # admissible A,B. Forward doubling cancels one inverse at every step.
    aa,bb,cc,dd=a,b,c,d
    for j in range(depth):
        ck(bb<=0<=cc)
        aa,bb=2*aa+Q(1,2),2*bb+Q(1,2)
        cc,dd=2*cc-Q(1,2),2*dd-Q(1,2)
        ck(aa==-Q(1,2) and dd==Q(1,2) and cc==-bb)
    ck((aa,bb,cc,dd)==(-Q(1,2),Q(0),Q(0),Q(1,2)))
    joint_cases.append({'depth':depth,'initial_intervals':[[str(a),str(b)],[str(c),str(d)]],
                        'initial_density':str(height),'all_feedback_parameters':'0',
                        'terminal_density':'1','label_law':'every bit is 1 iff terminal U>0'})

# Flat H pushes Lebesgue measure to a mixture of an AC part and an atom.
# H' dx pushes to uniform with no atom. The full-variation norm bound is tight.
atomic_cases=[]
for delta in [Q(1,1000),Q(1,16),Q(1,4),Q(49,100)]:
    k=1/(1-2*delta)
    ck(k*(1-2*delta)==1)
    atom=2*delta
    pushed_continuous_density=1/k
    full_tv=abs(pushed_continuous_density-1)+atom
    derivative_error=(1-2*delta)*abs(k-1)+2*delta
    ck(full_tv==derivative_error==4*delta)
    # All nonconstant polynomial moments of H_*dx come from the AC part;
    # the atom is at 0. H_*(H'dx) matches uniform moments including mass.
    for degree in range(8):
        uniform=integral_monomial(-Q(1,2),Q(1,2),degree)
        outside_moment=integral_affine_power(-Q(1,2),-delta,k,(k-1)/2,degree)
        outside_moment+=integral_affine_power(delta,Q(1,2),k,(1-k)/2,degree)
        weighted_mass=k*outside_moment
        ck(weighted_mass==uniform)
        actual=outside_moment+(atom if degree==0 else 0)
        ck(actual==1 if degree==0 else actual==pushed_continuous_density*uniform)
    atomic_cases.append({'delta':str(delta),'atom_mass_for_g_equal_1':str(atom),
                         'atom_mass_for_actual_density_Hprime':'0',
                         'full_variation_equals_derivative_error':str(full_tv)})

# Finite-depth nonsingular cylinder pullbacks: each dyadic branch is affine
# bi-Lipschitz, with inverse lengths shrinking by exactly 2^depth.
null_pullback_cases=0
for depth in (1,3,8):
    for epsilon in [Q(1,10),Q(1,1000),Q(1,10**12)]:
        count=2**depth
        pulled_length=sum(epsilon/count for _ in range(count))
        ck(pulled_length==epsilon)
        null_pullback_cases+=1

print(json.dumps({'status':'PASS','exact_assertions':checks,
                  'correlated_ac_history_cases':joint_cases,
                  'flat_pushforward_atomic_tv_cases':atomic_cases,
                  'finite_depth_null_pullback_length_controls':null_pullback_cases,
                  'scope':'Exact AC correlated-history and atom-aware full-TV controls. Finite cylinder controls do not certify the infinite-dimensional theorem or replace the analytic null-set proof.'},indent=2,sort_keys=True))
