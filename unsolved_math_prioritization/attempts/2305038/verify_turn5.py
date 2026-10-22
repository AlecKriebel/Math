#!/usr/bin/env python3
"""Exact certificate for the uniform stronger hyperbolic derivative bound."""
import sympy as s,json
from pathlib import Path
a,v,t,K,d=s.symbols('a v t K d',real=True)
checks=0
def ck(z):
 global checks
 assert s.factor(z)==0,z
 checks+=1
D=1+a*v;B=1-a*a;M=(1-a)**2*(1-v);W=32*D+M
P=(1+a)**2*W-(1-v)*(9*D**2-4*B)**2
qs=[16*t,s.Rational(2,3)*(30*t*t-43*t+50),s.Rational(4,9)*(46*t**3-48*t*t-35*t+110),s.Rational(16,3)*(3*t**4+t**3-9*t*t-t+12),s.Rational(32,3)*(1-t)*(1+t)*(6+t-2*t*t-t**3)]
ck(P.subs(v,(2*t-1)/3)-sum(s.binomial(4,i)*a**i*(1-a)**(4-i)*qs[i] for i in range(5)))
ck((4-3*K)**2-(1-K)*(4-K)**2-K**3)
ck((1-a/3)**2-8*(1-a*a)/9-(a-s.Rational(1,3))**2)
kap=8*B/(9*D*D)
ck(kap**2-4*M/W*(4-2*kap)**2-64*(1-a)**2*P/(81*D**4*W))
ck((1-d)**2*(1+2*d)-(1-2*d)*(1+d)**2-4*d**3)
# Rewrite each positive bracket as a nonnegative constant plus nonnegative pieces.
ck(30*t*t-43*t+50-(7+43*(1-t)+30*t*t))
ck(46*t**3-48*t*t-35*t+110-(27+48*(1-t*t)+35*(1-t)+46*t**3))
ck(3*t**4+t**3-9*t*t-t+12-(2+9*(1-t*t)+(1-t)+3*t**4+t**3))
ck(6+t-2*t*t-t**3-(3+t+2*(1-t*t)+(1-t**3)))
out={'status':'PASS','exact_symbolic_identities':checks,'certificate':'Five nonnegative Bernstein-in-a coefficient polynomials; each sign proved by explicit nonnegative terms on 0<=t<=1','scope':'Uniform stronger boundary bound, propagated through the exact interior-defect lemma; no finite sampling used','source_qualitative_goal':'unverified','substantive_author_turns':5}
print(json.dumps(out,indent=2));Path(__file__).with_name('TURN_5_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
