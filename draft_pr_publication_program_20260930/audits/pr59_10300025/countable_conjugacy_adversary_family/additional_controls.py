#!/usr/bin/env python3
"""Strengthened inverse-omission control retaining all other radius premises."""
from fractions import Fraction as Q
import hashlib,json,pathlib
rows=[]
for n in (2,3,10,100,1000):
    r=2*n-1; following=2*(n+1)-1
    assert following>r+1
    assert r<following**3  # cuberoot(r)<following, no floating arithmetic
    x=r**3; h_x=Q(x+1,2); h_fx=Q(n)
    assert h_x-h_fx>n
    rows.append({'n':n,'r_n':r,'r_next':following,'x':x,'signed_displacement':str(h_x-h_fx)})
out={'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
     'assertions_passed':15,'rows':rows,'global_reason':'((2n-1)^3+1)/2-n tends to infinity',
     'all_other_radius_premises_retained':True}
pathlib.Path(__file__).with_name('additional_controls_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
