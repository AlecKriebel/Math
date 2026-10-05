#!/usr/bin/env python3
"""Bounded displacement does not imply Lipschitz: exact all-interval family."""
from fractions import Fraction as Q
import hashlib,json,pathlib
rows=[]
for n in (1,2,10,100,1000):
    width=Q(1,(n+1)**2); slope=Q(1,2)/width
    return_slope=Q(1,2)/(1-width); max_displacement=Q(1,2)-width
    assert slope>0 and return_slope>0
    assert 0<=max_displacement<=Q(1,2)
    assert slope==Q((n+1)**2,2)
    rows.append({'n':n,'first_width':str(width),'first_slope':str(slope),
                 'second_slope':str(return_slope),'max_displacement':str(max_displacement)})
out={'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
     'assertions_passed':15,'rows':rows,
     'universal_reason':'positive slopes; fixed integer endpoints; global displacement <=1/2; slopes -> infinity'}
pathlib.Path(__file__).with_name('boundary_controls_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
