"""All nontrivial pair-product sign vertices of two fixed rational boxes."""
import json,time
from fractions import Fraction
from pathlib import Path
from certify_entropy_quadrature import certify
OUT=Path(__file__).parent
cases=[{'name':'intermediate_center_mixed_roots','c':'9/10','a':['1','4/5'],'b':['2/5','3/10']},{'name':'unequal_ellipse_mixed_roots','c':'2/5','a':['1','7/8'],'b':['7/10','1/5']}]
res=[]
for case in cases:
 out={'case':case,'sign_certificates':[]}
 for s in [[-1,1],[1,-1],[-1,-1]]:
  cert=certify(Fraction(case['c']),list(map(Fraction,case['a'])),list(map(Fraction,case['b'])),s,256)
  out['sign_certificates'].append({'signs':s,**cert})
 lower=min(Fraction(r['normalized_entropy_gap']['lower']) for r in out['sign_certificates'])
 out['minimum_certified_delta']=str(lower)
 # Use e^2 > 7, proved by exp series, for an entirely rational power interval.
 width=7*lower;out['rational_power_upper_endpoint']=str(2+width)
 res.append(out);print(json.dumps(out),flush=True)
(OUT/'rational_box_certificates.json').write_text(json.dumps(res,indent=2)+'\n')
