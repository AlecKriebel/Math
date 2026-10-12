#!/usr/bin/env python3
"""Independent finite polymer-model and critical-curve controls (standard library)."""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
from hashlib import sha256
import json
counts={}
def ck(name,ok):
    assert ok,name
    counts[name]=counts.get(name,0)+1
steps={'E':(1,0),'N':(0,1),'S':(0,-1)}
def build(word):
    pts=[(0,0)];seen={(0,0)};contact=0
    for symbol in word:
        dx,dy=steps[symbol];x,y=pts[-1];new=(x+dx,y+dy)
        ck('self_avoiding',new not in seen)
        # Count previously occupied lattice neighbours other than predecessor.
        contact+=sum((new[0]+a,new[1]+b) in seen for a,b in ((1,0),(-1,0),(0,1),(0,-1)))-1
        seen.add(new);pts.append(new)
    return pts,contact
def columns(pts):
    out=defaultdict(set)
    for x,y in pts:out[x].add(y)
    return out
def column_contacts(pts):
    cols=columns(pts)
    return sum(len(cols[x]&cols[x+1]) for x in range(max(cols)))-max(cols)
words=['E'];histograms={};total=0
for n in range(1,8):
    histogram=defaultdict(int);reverse_set=set()
    for word in words:
        total+=1;p,k=build(word);east=word.count('E')
        ck('contact_column_identity',k==column_contacts(p)>=0)
        ck('span_equals_E_steps',p[-1][0]==east)
        eta=[(p[-1][0]-p[-1-i][0],p[-1][1]-p[-1-i][1]) for i in range(n+1)]
        reverse=word[::-1];rp,rk=build(reverse)
        ck('exact_endpoint_reversal',eta==rp)
        ck('contact_and_span_preserved',rk==k and rp[-1][0]==east)
        ck('last_E_convention',reverse[-1]=='E')
        reverse_set.add(reverse);histogram[k,east]+=1
    ck('endpoint_bijection_injective',len(reverse_set)==len(words))
    histograms[n]=dict(histogram)
    words=[w+c for w in words for c in ('E','N','S') if w[-1]+c not in ('NS','SN')]
# No-interaction generating function: G=hz(1+z)/(1-(1+h)z-hz²).
for h in [F(1,3),F(1),F(5,2)]:
    a={1:h,2:h*h+2*h}
    for n in range(3,8):a[n]=(1+h)*a[n-1]+h*a[n-2]
    for n,H in histograms.items():
        ck('independent_no_interaction_recurrence',sum(v*h**span for (k,span),v in H.items())==a[n])
# Positive variance identity without differentiating a log numerically.
for n,H in histograms.items():
    terms=[(F(number)*F(3)**k*F(5,4)**span,span) for (k,span),number in H.items()]
    z=sum(w for w,s in terms);first=sum(w*s for w,s in terms);second=sum(w*s*s for w,s in terms)
    pair=sum(terms[i][0]*terms[j][0]*(terms[i][1]-terms[j][1])**2 for i in range(len(terms)) for j in range(i+1,len(terms)))
    ck('exact_convexity_covariance_identity',z*second-first*first==pair>=0)
for denominator in range(1,8):
    for numerator in range(denominator+1,3*denominator+1):
        a=F(numerator,denominator);omega=a*a;h=omega*(a-1)/(a+1)
        ck('physical_critical_branch',0<h<omega)
        ck('critical_equation',omega*(omega-h)**2==(omega+h)**2)
        ck('force_formula_equivalence',h==(a-1)/(1/a+1/(a*a)))
        ck('theta_polynomial_equivalence',h-1==(a**3-a*a-a-1)/(a+1))
        ck('theta_strict_monotonicity',(3*a+1)*(a-1)==3*a*a-2*a-1>0)
ck('theta_root_bracket',F(1839,1000)**3-F(1839,1000)**2-F(1839,1000)-1<0<F(184,100)**3-F(184,100)**2-F(184,100)-1)
for r in [F(1,4),F(1,2),F(2,3),F(9,10)]:
    ck('backward_secant_factor',1-3*r*r+2*r**3==(1-r)**2*(2*r+1)>0)
for b in [F(11,10),F(4,3),F(2),F(4)]:
    ck('forward_secant_factor',2*b**3-3*b*b+1==(b-1)**2*(2*b+1)>0)
root=Path(__file__).resolve().parent
out={'status':'PASS','artifact_sha256':sha256((root/'author_replay/SOURCE_STATUS.md').read_bytes()).hexdigest(),'exact_assertions':sum(counts.values()),'categories':counts,'walks_through_length_7':total,'scope':'Finite exact endpoint, contact, force-normalization, critical-curve and convexity diagnostics. Published asymptotic exponent is not inferred numerically.'}
text=json.dumps(out,indent=2,sort_keys=True)+'\n';(root/'independent_results.json').write_text(text);print(text,end='')

