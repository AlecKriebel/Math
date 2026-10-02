"""Pure-Python exact checker for the universal outer-span<=6 theorem."""
from pathlib import Path
from collections import Counter
import json

C=Counter()
def check(k,v):
    assert v,k
    C[k]+=1
def const(c):return {(0,0):c} if c else {}
def add(a,b):
    d=dict(a)
    for k,v in b.items():d[k]=d.get(k,0)+v
    return {k:v for k,v in d.items() if v}
def scale(a,c):return {k:v*c for k,v in a.items() if v*c}
def mul(a,b):
    d={}
    for (i,j),v in a.items():
        for (k,l),w in b.items():d[i+k,j+l]=d.get((i+k,j+l),0)+v*w
    return {k:v for k,v in d.items() if v}
def power(a,n):
    b=const(1)
    while n:
        if n&1:b=mul(b,a)
        a=mul(a,a);n//=2
    return b
def rising(a,n):
    b=const(1)
    for i in range(1,n+1):b=mul(b,add(a,const(i)))
    return b
def val(a,x,t):return sum(v*x**i*t**j for (i,j),v in a.items())

D=json.loads(Path(__file__).with_name('TURN_2_CERTIFICATES.json').read_text())
expected={(r,u,v) for r in range(3,7) for u in range(1,r) for v in range(1,r-u)}
check('complete_case_set',{(z['r'],z['u'],z['v']) for z in D['cases']}==expected)
for z in D['cases']:
    r,u,v,w,shift=(z[k] for k in ('r','u','v','s','A_shift'))
    check('correct_inner_width',w==r-u-v and w>=1)
    check('correct_domain_shift',shift==(1 if (r,u,v)==(6,2,3) else 0))
    A=add({(1,0):1},const(shift));B=add(add(A,const(1)),{(0,1):1})
    target=add(mul(power(rising(A,r),w),power(rising(add(B,const(v)),w),r)),
               scale(mul(power(rising(B,r),w),power(rising(add(A,const(u)),w),r)),-1))
    result=const(z['prefactor'])
    check('nonzero_prefactor',z['prefactor']!=0)
    for f in z['positive_factors']:
        q={(a,b):c for a,b,c in f['terms']}
        check('nonnegative_factor_coefficients',all(c>=0 for c in q.values()))
        check('strict_positive_constant',q.get((0,0),0)>0)
        check('positive_integer_factor_power',isinstance(f['power'],int) and f['power']>=1)
        result=mul(result,power(q,f['power']))
    check('exact_formal_factor_identity',result==target)
    for a in range(4):
        for t in (0,1,3,25):
            check('nonzero_sample_integer_sign',val(result,a,t)*z['prefactor']>0)

# The omitted A=0 case is a literal univariate polynomial identity.
B={(1,0):1};Q={(i,0):c for i,c in enumerate(D['boundary_quartic_coefficients_ascending'])}
target=add(scale(power(add(B,const(4)),6),720),scale(rising(B,6),-729))
rhs=scale(mul(mul(add(B,const(4)),add(B,const(7))),Q),-9)
check('boundary_exact_factor_identity',target==rhs)
check('quartic_leading_coefficient',Q[(4,0)]==1)
check('quartic_all_lower_coefficients_negative',all(Q[(j,0)]<0 for j in range(4)))
check('quartic_root_interval_left',val(Q,240,0)<0)
check('quartic_root_interval_right',val(Q,241,0)>0)
out={'status':'PASS','universal_cases':len(expected),'exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),
     'boundary_Q240':val(Q,240,0),'boundary_Q241':val(Q,241,0),
     'scope':'Formal coefficient identities and positive-cone certificates prove exclusion for every n when outer span<=6. No all-span resolution is inferred.'}
print(json.dumps(out,indent=2,sort_keys=True))
