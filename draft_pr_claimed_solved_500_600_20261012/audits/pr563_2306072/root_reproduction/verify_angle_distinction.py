#!/usr/bin/env python3
"""Audit-only exact margins for ANGLE_DISTINCTION.md; no support realizability claim."""
from fractions import Fraction as Q
import json
checks={}
def require(name,value):
    if not value: raise RuntimeError(name)
    checks[name]=True
x=Q(3,4);p=Q(6,5)
sin_lower=x-x**3/6
cos_upper=1-x*x/2+x**4/24
require('positive cosine lower bound at tip',1-x*x/2>0)
require('positive cosine upper bound at tip',cos_upper>0)
require('strict positive tangent sign at tip',sin_lower>p*x*cos_upper)
x2=Q(1,2)
cos_lower=1-x2*x2/2
require('positive cosine lower bound at second point',cos_lower>0)
require('strict negative tangent sign at second point',x2/cos_lower<p*x2)
require('strict angle bound from pi greater than three',4*x==3)
require('positive decay exponent',p>0)
require('second point lies outward of tip',Q(3,2)>1)
print(json.dumps({'status':'PASS','exact_checks':len(checks),'checks':checks,'b_at_tip':'3/4','p':'6/5','positive_tangent_sign_margin':str(sin_lower-p*x*cos_upper),'negative_tangent_sign_margin':str(p*x2-x2/cos_lower),'scope':'Trigonometric-series margins supplement the analytic curve construction; no realizability as a support omitted slit or unread-source exclusion is claimed.'},indent=2))
