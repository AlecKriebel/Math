#!/usr/bin/env python3
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import json
from review_convention_equivalence import validate
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'certificates/primary_convention_frontier.json').read_text())
I=json.loads((ROOT/'certificates/independent_frontier.json').read_text())
A=json.loads((ROOT/'certificates/cleanup_jc_map.json').read_text())
B=json.loads((ROOT/'certificates/independent_cleanup_model.json').read_text())

mutations=[]
def test(name,why,fn):
 p,i,a,b=map(deepcopy,(P,I,A,B));fn(p,i,a,b)
 failed=False;msg=''
 try:validate(p,i,a,b)
 except Exception as e:failed=True;msg=f'{type(e).__name__}: {e}'
 assert failed,name
 mutations.append({'mutation':name,'mathematical_reason':why,'expected_failure':msg})

test('fail_to_suppress_degree_two_vertex',
     'The clean target count changes because the root-child pair is not contracted.',
     lambda p,i,a,b: p['path_length_frontier']['4'].__setitem__('canonical_clean_target_graphs',4))
test('suppress_reticulation_without_transport',
     'Removing the root-child reticulation without the root-zipper parameter map changes the certified JC polynomial.',
     lambda p,i,a,b: a['fourier_tensor'].__setitem__('nonzero_sector','u*v*gamma'))
test('identify_wrong_parallel_pair',
     'The independently generated clean target graph count no longer agrees.',
     lambda p,i,a,b: i['frontier']['5'].__setitem__('canonical_clean_target_graphs',3))
test('forget_reticulation_arrowhead',
     'The strict fibre witness ceases to be the independently generated mixed graph.',
     lambda p,i,a,b: i['strict_witness'].__setitem__('rooted_tree_child',True))
test('merge_distinct_cleanup_fibres',
     'Canonical target fibres are distinct under leaf-labelled mixed-graph isomorphism.',
     lambda p,i,a,b: p['path_length_frontier']['8'].__setitem__('canonical_clean_target_graphs',6))
test('misclassify_parallel_theta_112',
     'The complete binary LSA census contains no valid (1,1,2) presentation.',
     lambda p,i,a,b: p['structural_conclusions'].__setitem__('parallel_theta_112_valid_rooting',True))
test('test_strongness_on_one_rooting_only',
     'The strict witness has a strong sd0 target but a non-tree-child cleanup rooting.',
     lambda p,i,a,b: p['strict_rooting_fibre_witness'].__setitem__('rooting_tree_child',True))
test('collapse_theta_sharpness_pair_under_cleanup',
     'The two labelled clean mixed graphs remain nonisomorphic and differ in leaf-1 triangle adjacency.',
     lambda p,i,a,b: p['theta_sharpness_pair'].__setitem__('nonisomorphic',False))
test('change_JC_parent_choice_orientation',
     'The sparse clean-room pullback fixes the source/target mixture orientation.',
     lambda p,i,a,b: b.__setitem__('source_switching_polynomial',[['1','gamma*u*v']]))
test('replace_root_zipper_by_boundary_value',
     'The equality must have a strict open-domain section, not beta=1 or lambda in {0,1}.',
     lambda p,i,a,b: a['rational_interior_witness'].__setitem__('effective','1'))

out={'status':'ALL MUTATIONS REJECTED','count':len(mutations),'records':mutations}
(ROOT/'certificates/mutation_suite.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True));print('PASS mutation suite')
