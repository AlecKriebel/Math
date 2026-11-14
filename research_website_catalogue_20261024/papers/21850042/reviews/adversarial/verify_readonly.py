#!/usr/bin/env python3
"""Definition-level independent exact checks. Reads no deposited program; writes nothing.
Run from any directory. JSON is printed to stdout. No finite samples imply asymptotics.
"""
import json, sys
from fractions import Fraction as Q
import sympy as S
r,d = S.symbols('r delta', positive=True)
W=S.Matrix([[0,d,1],[d,0,d],[1,d,0]])
D=[sum(W[u,v] for v in range(3)) for u in range(3)]
checks=[]
def require(name,expr):
    value=S.factor(expr)
    assert value == 0,(name,value)
    checks.append(name)
def triangle(rule):
    states=list(range(1,7)); ix={s:i for i,s in enumerate(states)}
    A=S.zeros(6); b=S.zeros(6,1)
    for state in states:
        i=ix[state]; fit=[r if state>>u&1 else S.Integer(1) for u in range(3)]
        rates={}
        for u in range(3):
            for v in range(3):
                if u==v or (state>>u&1)==(state>>v&1):continue
                rate=fit[u]*W[u,v]/(D[u] if rule=='Bd' else sum(fit[k]*W[k,v] for k in range(3)))
                nxt=(state | 1<<v) if state>>u&1 else (state & ~(1<<v))
                rates[nxt]=rates.get(nxt,0)+rate
        for nxt,rate in rates.items():
            A[i,i]+=rate
            if nxt==7:b[i]+=rate
            elif nxt!=0:A[i,ix[nxt]]-=rate
    ans=A.inv(method='DM')*b
    ans=ans.applyfunc(S.factor)
    for i in range(6):require(f'{rule}_harmonic_{states[i]}',(A*ans-b)[i])
    f=[ans[ix[1<<v]] for v in range(3)]
    return f
FB=triangle('Bd'); FD=triangle('dB')
DB=9*r*r+d*(12*r**4+24*r**3+15*r*r+24*r+12)+d*d*(16*r**4+52*r**3+83*r*r+52*r+16)+d**3*(4*r**4+12*r**3+13*r*r+12*r+4)
alphaB=r*r*(3+d*(12*r*r+12*r+5)+d*d*(16*r*r+36*r+21)+d**3*(4*r*r+8*r+3))/DB
alphaD=2*r*(r+1+d*(3*r*r+3*r+1)+d*d*(5*r+1))/(3*(r+1)*(2*r+d*(3*r*r+r+3)+6*d*d*r))
YB=3*(3*r*r+d*(5*r*r+12*r+12)+d*d*(21*r*r+36*r+16)+d**3*(3*r*r+8*r+4))/DB
ID=(2*r*r+3*r+1+d*(3*r*r+7*r+5)+d*d*(r*r+8*r))/((1+d)*(r+1)*(2*r+d*(3*r*r+r+3)+6*d*d*r))
JD=r*(r*r+3*r+2+d*(5*r*r+7*r+3)+d*d*(8*r+1))/((1+d)*(r+1)*(2*r+d*(3*r*r+r+3)+6*d*d*r))
require('eq16_alpha_Bd',sum(FB)/3-alphaB)
require('eq17_alpha_dB',sum(FD)/3-alphaD)
require('eq19_YB',sum(x.subs(r,1/r) for x in FB)-YB)
require('eq20_ID',sum(x.subs(r,1/r)/dv for x,dv in zip(FD,D))-ID)
require('eq23_JD',sum(x/dv for x,dv in zip(FD,D))-JD)
require('alphaB_singular_limit',S.limit(sum(FB)/3,d,0)-S.Rational(1,3))
require('alphaD_singular_limit',S.limit(sum(FD)/3,d,0)-S.Rational(1,3))
require('YB_singular_limit',S.limit(YB,d,0)-1)
require('ID_singular_limit',S.limit(ID,d,0)-(2*r+1)/(2*r))
require('JD_singular_limit',S.limit(JD,d,0)-(r+2)/2)
for rule,f in [('Bd',FB),('dB',FD)]:
    require(rule+'_neutral_uniform_average',sum(x.subs(r,1) for x in f)-1)
    require(rule+'_unit_triangle_complete',sum(x.subs(d,1) for x in f)/3-( (1-1/r)/(1-r**-3) if rule=='Bd' else S.Rational(2,3)*(1-1/r)/(1-r**-2)))
# Complete graph dB down/up recurrence; n>=2 and 1<=i<n.
n,i=S.symbols('n i', integer=True, positive=True)
up=(n-i)*r*i/(r*i+n-i-1)
down=i*(n-i)/(r*(i-1)+n-i)
gamma=S.factor(down/up)
require('complete_dB_telescoping_ratio',gamma-(n-1+(r-1)*i)/(r*(n-1+(r-1)*(i-1))))
# Endpoint arithmetic, retaining formal inverse-size terms.
t=S.symbols('t', positive=True); q=S.Rational(1,3); h=t/(3+t)
pB=q-S.Rational(4,3)*t*t; pD=q-S.Rational(16,81)*t*t
qB=q; qD=q-q*t
rhoB=(1-h)*pB+h*qB; rhoD=(1-h)*pD+h*qD
require('endpoint_Bd_graph_coefficient',S.limit((rhoB-q)/t**2,t,0)+S.Rational(4,3))
require('endpoint_dB_graph_coefficient',S.limit((rhoD-q)/t**2,t,0)+S.Rational(25,81))
require('endpoint_dB_baseline_difference',-S.Rational(25,81)+S.Rational(1,9)+S.Rational(16,81))
# Proposition8 activation event and exact ordinary-count ratio.
c,i,Wtot,wl=S.symbols('c i W w_l',positive=True)
bi=(c-i)*r*i/(c+(r-1)*i)
di=i*(c-i+1)/(c+(r-1)*(i-1))
ai=r*i/(c+Wtot+(r-1)*i)
require('prop8_core_ratio',bi/di-r*(c-i)/(c-i+1)*(c+(r-1)*(i-1))/(c+(r-1)*i))
activation=(r*wl/(c+Wtot+(r-1)*wl))/(1+r*wl/(c+Wtot+(r-1)*wl))
require('prop8_leaf_activation',activation-r*wl/(c+Wtot+(2*r-1)*wl))
# Killed branching polynomial and sharpness algebra only, not convergence proof.
a=S.symbols('alpha', positive=True); ell=(8*a-3+S.sqrt(9+60*a-44*a*a))/(18*a); ext=1-ell
require('pendant_killed_quadratic_at_3halves',(S.Rational(9,4)*a)*ext**2-(S.Rational(9,4)*a+a+S.Rational(3,4)*(1-a))*ext+a)
require('pendant_ell_at_1over9',ell.subs(a,S.Rational(1,9))-S.Rational(8,9))
require('pendant_ell_zero_limit',S.limit(ell,a,0)-1)
print(json.dumps({'status':'PASS','scope':'exact rational-function identities and endpoint arithmetic; no universal probability-limit clearance','checks':checks,'count':len(checks),'triangle_singleton_limits':{'Bd':[str(S.limit(x,d,0)) for x in FB],'dB':[str(S.limit(x,d,0)) for x in FD]},'python':sys.version.split()[0],'sympy':S.__version__},indent=2))
