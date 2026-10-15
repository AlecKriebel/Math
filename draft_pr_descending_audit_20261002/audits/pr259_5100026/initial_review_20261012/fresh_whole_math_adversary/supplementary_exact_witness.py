#!/usr/bin/env python3
"""Physical and interior-contact completion of the independently frozen witness."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib
V=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr261_5100021/initial_review_20261012/reproduction_source_adversary/vendor');sys.path.insert(0,str(V))
import sympy as s
O=Path(__file__).resolve().parent
q,x=s.symbols('q x');ideal=s.groebner([x*x-4*(1-q*q),3*q*q-8*q+1],x,q)
checks=[]
def zero(expr,name):
    num=s.fraction(s.cancel(expr))[0];remainder=ideal.reduce(s.expand(num))[1];assert remainder==0,(name,remainder);checks.append(name)
qr=(4-s.sqrt(13))/3
assert qr.is_positive and (s.Rational(1,3)-qr).is_positive
checks.extend(['q>0','q<1/3'])
LL=x*(1-3*q)/(4*q)
zero(LL**2-(x*x+(1+q)**2),'certified_positive_slant_length_square')
P=[s.Matrix([0,1]),s.Matrix([x,-q]),s.Matrix([-x,-q])]
unit_out=[s.Matrix([x,-1-q])/LL,s.Matrix([-1,0]),s.Matrix([x,1+q])/LL]
G=s.diag(s.Rational(1,4),1);H=s.diag(1/(3+q*q),1/(q*q));contacts=[]
for i,p in enumerate(P):
    incoming=unit_out[(i-1)%3];outgoing=unit_out[i];n=G*p
    zero(incoming.dot(incoming)-1,f'unit incoming {i}')
    zero(outgoing.dot(outgoing)-1,f'unit outgoing {i}')
    refl=incoming-2*incoming.dot(n)/n.dot(n)*n
    for j in (0,1):zero(refl[j]-outgoing[j],f'physical specular reflection {i}:{j}')
    edge=P[(i+1)%3]-p;tt=s.cancel(-(p.T*H*edge)[0]/(edge.T*H*edge)[0]);contact=p+tt*edge
    zero((contact.T*H*contact)[0]-1,f'exact caustic contact {i}')
    zero((contact.T*H*edge)[0],f'exact tangent derivative {i}')
    # Reduce rational contact parameter in the algebraic number field.
    num,den=s.fraction(tt);num=ideal.reduce(s.expand(num))[1];den=ideal.reduce(s.expand(den))[1];tt=s.simplify((num/den).subs(q,qr))
    assert tt.is_positive and (1-tt).is_positive,(i,tt)
    contacts.append(str(tt));checks.extend([f'interior contact {i}: t>0',f'interior contact {i}:t<1'])
report={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','exact_assertions':len(checks),'checks':checks,'contact_parameters':contacts,'slant_edge_length':'x(1-3q)/(4q)>0','ideal_generators':['x^2-4(1-q^2)','3q^2-8q+1'],'earlier_independent_freeze':str(O/'PRECOMPARISON_FREEZE.json'),'scope':'Same witness as independently frozen; adds physical reflection and interior contact checks after cross-comparison, using no other checker helper.'}
(O/'SUPPLEMENTARY_EXACT_WITNESS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
