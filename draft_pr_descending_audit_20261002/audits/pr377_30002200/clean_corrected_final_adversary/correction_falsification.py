"""Mechanism controls for graded Ext and source Hessian, independent of packet code."""
from itertools import product
import json
import sympy as s

# K_(b,r-1) has presentation R[2b] -> R^r -> K -> 0,
# relation column (signed t_i^b). Duality gives Ext^1=R/(t_i^b)[-2b].
# A quotient shift q and target shift l leave degree-zero classes precisely
# at monomials with 2 sum exponent = 2b+q-l.
def ext_dim(r,b,q,l):
    return sum(2*sum(exps)==2*b+q-l for exps in product(range(b),repeat=r))
result=[]
for l in [0,3,10,11,13]:
    count=ext_dim(5,1,9,l)
    assert count==(1 if l==11 else 0)
    result.append({'rank':5,'b':1,'quotient_shift':9,'target_shift':l,'degree_zero_Ext1_dimension':count})
assert ext_dim(5,2,0,0)==10
result.append({'negative_control':'b=2 blanket l-q!=2b splitting inference fails','degree_zero_Ext1_dimension':ext_dim(5,2,0,0)})

# Obtain the quadratic form from the analytic function using a formal epsilon,
# rather than instantiating the candidate's assertion.
eps=s.symbols('epsilon',real=True)
for r,j in [(3,0),(5,2),(7,3),(9,1)]:
    theta=s.symbols('theta:'+str(r),real=True)
    x=s.symbols('x:'+str(r),real=True); y=s.symbols('y:'+str(r),real=True)
    signs=[-1]*j+[1]*(r-j)
    # expansion s_i e^(i eps theta_i) sqrt(1-eps^2*(x_i^2+y_i^2))
    real=sum(signs[i]*(1-eps**2*(theta[i]**2+x[i]**2+y[i]**2)/2) for i in range(r))
    imag=sum(signs[i]*eps*theta[i] for i in range(r))
    coeff=s.expand(-real**2-imag**2).coeff(eps,2)
    q=r-2*j
    target=q*sum(signs[i]*(theta[i]**2+x[i]**2+y[i]**2) for i in range(r))-sum(signs[i]*theta[i] for i in range(r))**2
    assert s.expand(coeff-target)==0
    H=s.hessian(coeff,theta)/2
    eig=H.eigenvals(); negative=sum(mult for val,mult in eig.items() if val<0)
    positive=sum(mult for val,mult in eig.items() if val>0)
    zeros=eig.get(s.Integer(0),0)
    assert (negative,positive,zeros)==(j,r-j-1,1)
    assert negative+2*j==3*j
    result.append({'analytic_Hessian_rank':r,'negative_subset_size':j,'angular_signature':[negative,positive,zeros],'total_Morse_index':3*j})
print(json.dumps({'status':'PASS','checks':result,'finite_control_scope':True},indent=2))
