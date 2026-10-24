#!/usr/bin/env python3
"""Exact recurrence certificates for the abstract EDT0L mechanism countermodel."""
from fractions import Fraction
from pathlib import Path
import json

u,v=1,0
rows=[]
previous=None
for n in range(1,101):
    u,v=2*u+v,u+v
    ratio=Fraction(u,v)
    if previous is not None:
        assert ratio<previous
    assert u*u-u*v-v*v==1
    rows.append({'n':n,'a_count':u,'b_count':v,'ratio':str(ratio),
                 'golden_polynomial_numerator':1})
    previous=ratio
result={'scope':'abstract finite-endomorphism example, not RAAG genus data',
        'cases':rows,'all_checks_passed':True}
Path(__file__).with_name('FORMAL_LANGUAGE_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print('100 exact recurrence and monotonicity checks passed')
