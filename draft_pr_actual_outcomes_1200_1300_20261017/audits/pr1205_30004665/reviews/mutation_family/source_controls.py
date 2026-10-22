#!/usr/bin/env python3
"""Additional post-freeze controls against primary-source examples."""
import json
import sympy as s
import reconstruct as r

w=(2,1,3,4)*3
r.reduced_check(w)
B,F=r.seed(w); X=list(s.symbols('X1:13'))
for k in (6,3,5,4,3,1,2,7,6,8):
    k-=1;assert k not in F
    X=r.mutate_X(X,B,k);B=r.mutate_B(B,k,F)
assert all(B[8][j]<=0 for j in range(12) if j not in F)
poly=r.laurent(s.cancel(1/X[8]),12)
assert len(poly)==27
assert sorted(t['coefficient'] for t in poly)==[1]*26+[2]
double=[t for t in poly if t['coefficient']==2]
assert double==[{'coefficient':2,'exponents':[0,0,0,0,-1,-1,-1,-1,-1,0,0,0]}]
def support(a):return tuple(a)
S={support(t['exponents']) for t in poly}
assert (0,0,0,0,-2,-1,-1,-1,-1,0,0,0) in S
assert (0,0,0,0,0,-1,-1,-1,-1,0,0,0) in S
report={'published_D4_word':w,'published_D4_mutation_sequence':[6,3,5,4,3,1,2,7,6,8],
        'optimized_frozen_position':9,'support_size':len(poly),'coefficient_two_term':double,
        'half_sum_redundancy_terms_present':True,'support':poly}
(r.HERE/'source_controls.json').write_text(json.dumps(report,indent=2)+'\n')
print('Published D4 control passed: 27 terms, exactly one coefficient 2, documented half-sum relation present.')
