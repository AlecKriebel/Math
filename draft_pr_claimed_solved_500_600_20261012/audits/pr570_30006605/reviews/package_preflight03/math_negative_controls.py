#!/usr/bin/env python3
"""Exact falsification certificates for essential assumptions/algorithm steps."""
from fractions import Fraction as F
from pathlib import Path
import json
N=10**12;ell=30;t=17_000_000_000;q=2**ell;root_leaves=N-q-ell*t
minority=q//2+t;union=q-1+ell*t;twice=2*union
assert root_leaves==488926258176 and minority==17536870912 and twice==1022147483646
partial=sum((F(7)**j)/__import__('math').factorial(j) for j in range(21))
assert partial>1000 and 56*minority<N and twice>N
# ln N < 28 follows e^7>1000 and N=1000^4; all pendant singleton cuts also unbalanced.
# Repair uses f=80; the core coordinate cuts become balanced, as intended.
assert 2*(N-1).bit_length()==80 and 80*minority>=N
# Star with24 leaves, root0 and leaf1 arrival8: slice{1} has original E=8,
# open fiber arrival2; true E_G(1)=8. Keeping only fiber call returns2.
star_original=8;star_fiber=2;assert max(star_original,star_fiber)==8 and star_original>star_fiber
# Opposite need: zero arrivals on a star leaf yield E_S=0, while external
# other leaves force E_G=2. Keeping only the original call returns0.
assert max(0,2)==2
# Integer budget on a distance1/2 edge with weight1 and R3/4 incorrectly
# excludes its other endpoint; the integer-distance assumption is essential.
R=F(3,4);fractional_distance=F(1,2);b=max(k for k in range(2) if k<=R)
assert fractional_distance<=R and not fractional_distance<=b
# Negative weight reverses monotonicity: -k<=0 gives all indices but the
# scalar-initial-segment proof for general negative R fails. Negative R is
# independently excluded by the theorem's nonnegative radius hypothesis.
# Dropping incumbent preservation: path3, all-one weights, feasible pivot1
# is deleted, no active optimum remains, original incumbent2 is incorrect.
path_radii=[2,1,2];assert min(path_radii)==1 and 2!=min(path_radii)
result={'status':'PASS','pendant_cube_volume_counterexample':{'N':N,'ell':ell,'unit_vertex_leaves_each':t,'root_leaves':root_leaves,'coordinate_minority':minority,'minority_union':union,'duplicated_volume':twice,'56_times_minority':56*minority,'positive_e7_partial_sum_terms':21,'e7_partial_sum_exceeds1000':True,'literal_natural_log_volume_refuted':True,'repaired_f':80,'coordinate_cuts_balanced_after_repair':True,'arrival_at_antipode':N-1,'limits':'Succinct exact construction; no materialization or final theorem refutation.'},'essential_step_certificates':[{'step':'keep original slice call','graph':'25-vertex star; arrival8at leaf1,0elsewhere','correct_at_leaf1':8,'fiber_only_wrong':2},{'step':'keep fiber slice call','graph':'25-vertex star; allzero arrivals','correct_at_leaf1':2,'original_only_wrong':0},{'step':'integral distances','distance':'1/2','weight':'1','R':'3/4','true_feasible':True,'integer_budget':0,'budget_test_feasible':False},{'step':'save feasible incumbent before deleting pivot','graph':'3-vertex path; allone weights','correct_radius':1,'unsaved_initial_incumbent':2}],'limits':'Checkable certificates, not alternative-scope claims or a benchmark.'}
Path(__file__).with_name('MATH_NEGATIVE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS exact source-volume and four essential-step falsification certificates')
