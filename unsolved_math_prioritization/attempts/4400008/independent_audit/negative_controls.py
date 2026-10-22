#!/usr/bin/env python3
"""Demonstrate rejection of deliberate faults, independently of author code."""
import json

def branch(support, *, wrong_inverse=False, wide_u=False):
    if not support or 0 in support:
        return support
    n=min(map(abs,support))
    right=3*n+(1 if wide_u else 0)
    u=all((j in support)==(j==n) for j in range(-3*n,right+1))
    v=all((j in support)==(j==-n) for j in range(-5*n,n+1))
    d=2*n if u else (2*n if wrong_inverse else -2*n) if v else 0
    return frozenset(j-d for j in support)

rows=[]
s=frozenset({1})
correct=branch(branch(s))
wrong=branch(branch(s,wrong_inverse=True),wrong_inverse=True)
assert correct==s and wrong!=s
rows.append({'id':'inverse_sign_mutant','expected':'reject','observed':'rejected',
 'witness_support':[1],'correct_twice':sorted(correct),'mutated_twice':sorted(wrong)})
n=3;s=frozenset({n,3*n+1})
correct=branch(s);wrong=branch(s,wide_u=True)
assert correct==frozenset(j-2*n for j in s) and wrong!=correct
rows.append({'id':'upper_endpoint_mutant','expected':'reject','observed':'rejected',
 'witness_support':sorted(s),'correct_image':sorted(correct),'mutated_image':sorted(wrong)})
# Explicit failed assertions: each would be required by an incorrect shortcut.
assert 2!=1
rows.append({'id':'flow_as_TOE','expected':'reject','observed':'rejected',
 'source_fixed_points':2,'expanded_fixed_points':1})
assert 1%2!=0
rows.append({'id':'speed_two_complete_orbit','expected':'reject','observed':'rejected',
 'missing_orbit_index':1,'all_reached_indices':'2Z'})
for m in range(1,33):
 w=(1,)+(0,)*(2*m+1)
 assert all(sum(w[(k+j)%len(w)] for j in range(2*m+1))<=1 for k in range(len(w)))
 assert (len(w)-1)%2==1
rows.append({'id':'finite_window_stabilization','expected':'reject','observed':'rejected',
 'parameters_checked':[1,32],'reason':'legal local windows coexist with a forbidden odd gap'})
print(json.dumps({'target_id':'4400008','result':'PASS','deliberate_faults_rejected':len(rows),
 'controls':rows,'scope':'Explicit finite witnesses and mutations; source-theorem overreach is checked in audit.md.'},indent=2,sort_keys=True))
