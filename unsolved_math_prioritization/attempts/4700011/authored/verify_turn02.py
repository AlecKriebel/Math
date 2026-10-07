#!/usr/bin/env python3
"""Exact certificates for the order-six classification in author Turn 2.
No floating-point arithmetic, random search, or external source data is used.
"""
from pathlib import Path
import json
import sympy as sp

ROOT=Path(__file__).resolve().parent
I=sp.eye(6)
t=sp.Symbol('t')

def step(state,support,constant):
    opts=[(state[j],j) for j in support]+([(0,-1)] if constant else [])
    opts.sort(reverse=True)
    win=opts[0][1]
    A=sp.zeros(6)
    for j in range(5): A[j,j+1]=1
    A[5,0]=-1
    if win>=0: A[5,win]=1
    return state[1:]+(opts[0][0]-state[0],),win,opts[0][0]-opts[1][0],A

cases=[
    {'name':'bd_no_constant','support':(1,3,5),'constant':False,'initial':(4,5,-8,-6,9,8),'period':99,'kind':'expanding_cubic'},
    {'name':'bd_with_constant','support':(1,3,5),'constant':True,'initial':(8,-1,3,1,-4,2),'period':47,'kind':'contracting_cubic'},
    {'name':'bcd_no_constant','support':(1,2,3,4,5),'constant':False,'initial':(4,3,-1,10,-4,-5),'period':65,'kind':'nontrivial_unipotent'},
    {'name':'bcd_with_constant','support':(1,2,3,4,5),'constant':True,'initial':(1,8,2,-6,2,6),'period':65,'kind':'nontrivial_unipotent'},
]
certificates=[]
for case in cases:
    z=case['initial'];M=I;winners=[];margins=[]
    for _ in range(case['period']):
        z,w,g,A=step(z,case['support'],case['constant'])
        assert g>0
        M=A*M;winners.append(w);margins.append(g)
    assert z==case['initial']
    char=sp.factor(M.charpoly(t).as_expr())
    if case['kind']=='expanding_cubic':
        g=t**3-4*t**2+3*t-1
        assert sp.expand(char-(t-1)**3*g)==0
        assert g.subs(t,3)<0 and g.subs(t,4)>0
    elif case['kind']=='contracting_cubic':
        g=t**3+7*t-1
        assert sp.expand(char-(t-1)**3*g)==0
        assert g.subs(t,0)<0 and g.subs(t,1)>0
    else:
        N=M-I
        assert N!=sp.zeros(6) and N*N==sp.zeros(6)
        assert N.rank()==1
    certificates.append({**case,'winners':winners,'minimum_strict_margin':min(margins),
                         'return_matrix':[[int(e) for e in row] for row in M.tolist()],
                         'characteristic_polynomial':str(char),'verified':True})

# The 5-step tangent drift at support {1,5}, with or without a constant.
def R(w,constant):
    a,b,c,d,e,f=w
    m=max([b,f]+([0] if constant else []))
    return (f,m-a,c-b,-b,e-d,-d)
w=(0,0,0,-1,0,0);drift=(0,0,-1,0,1,0)
for const in [False,True]:
    z=w
    for _ in range(3): z=R(z,const)
    assert z==tuple(w[i]+drift[i] for i in range(6))
    # Symbolic equivariance in the two inactive coordinates proves iteration.
    a,b,c,d,e,f,n,m=sp.symbols('a b c d e f n m')
    symbolic=sp.Matrix([f,m-a,c-b,-b,e-d,-d])
    shifted=symbolic.subs({c:c-n,e:e+n}, simultaneous=True)
    assert shifted-symbolic==n*sp.Matrix(drift)

# Exact four-step expanding tangent rays for supports bc and cd.
a=sp.Symbol('a')
minimal=a**3-a**2-1
reduce=lambda x:sp.rem(sp.expand(x),minimal,a)
w_bc=sp.Matrix([a-1,0,-1,0,a*a-a,0])
w_cd=sp.Matrix([0,a-1,0,-1,0,a*a-a])
ray_reports=[]
for name,support,w,winners in [
    ('bc',(1,2,4,5),w_bc,(2,2,1,4)),
    ('cd',(2,3,4),w_cd,(2,2,4,3)),
]:
    base=(0,0,1,1,0,0);z=base;v=w;gaps=[]
    for win in winners:
        mx=max(z[j] for j in support)
        ties=[j for j in support if z[j]==mx]
        assert z[win]==mx and mx>0  # adding a zero constant does not change ties
        for other in ties:
            if other!=win:
                gap=reduce(v[win]-v[other]);gaps.append(str(gap))
                # All gaps in these explicit certificates are 0, 1, or a.
                assert gap in [0,1,a]
        A=sp.zeros(6)
        for j in range(5):A[j,j+1]=1
        A[5,0]=-1;A[5,win]=1
        v=A*v;z=z[1:]+(mx-z[0],)
    assert z==base
    assert all(reduce(v[i]-a*w[i])==0 for i in range(6))
    ray_reports.append({'support':support,'winners':winners,'tied_comparison_gaps':gaps,
                        'return_multiplier_polynomial':'a**3-a**2-1','verified':True})
assert minimal.subs(a,1)<0 and minimal.subs(a,sp.Rational(3,2))>0

# Order-two boundary return: F_a^5 extends to (0,y) -> (0,a*y).
x,y,a=sp.symbols('x y a',positive=True)
seq=[x,y]
for _ in range(5):seq.append(sp.factor(sp.cancel((a+seq[-1])/seq[-2])))
f5x,f5y=seq[5],seq[6]
assert sp.cancel(f5x).subs(x,0)==0
assert sp.cancel(sp.cancel(f5y).subs(x,0)-a*y)==0
assert sp.cancel(sp.cancel(f5x/x).subs(x,0)-(a*y+1)/(a+y))==0

result={'all_passed':True,'arithmetic':'exact integers and SymPy polynomial identities',
        'strict_cycle_certificates':certificates,'expanding_tangent_rays':ray_reports,
        'drift_certificate':{'base':[0,0,1,0,1,0],'base_return':5,'initial_tangent':[0,0,0,-1,0,0],
                             'three_return_drift':drift,'constant_options':[False,True],'verified':True},
        'order_two_boundary_return':{'first_coordinate':str(f5x),'second_coordinate':str(f5y),
                                     'boundary_image':['0','a*y'],'verified':True}}
(ROOT/'turn02_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'all_passed':True,'strict_cycles':[{k:c[k] for k in ['name','period','minimum_strict_margin','characteristic_polynomial']} for c in certificates],
                  'tangent_rays':ray_reports,'boundary_return_verified':True},indent=2))
