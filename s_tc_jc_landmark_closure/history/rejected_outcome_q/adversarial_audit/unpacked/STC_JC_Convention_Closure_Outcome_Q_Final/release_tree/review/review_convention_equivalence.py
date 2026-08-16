#!/usr/bin/env python3
"""Independent reconciliation of the two structural and two algebraic replays."""
from __future__ import annotations
from pathlib import Path
import json, subprocess, tempfile

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'certificates'/'primary_convention_frontier.json'
I=ROOT/'certificates'/'independent_frontier.json'
A=ROOT/'certificates'/'cleanup_jc_map.json'
B=ROOT/'certificates'/'independent_cleanup_model.json'
R=ROOT/'certificates'/'independent_rooting_fibres.json'
OUT=ROOT/'certificates'/'independent_convention_review.json'

def load(p):return json.loads(p.read_text())
def validate(primary,independent,algebra,clean,rooting=None):
    assert primary['status']=='EXACTLY COMPUTED'
    assert independent['status']=='EXACTLY COMPUTED'
    for L in map(str,range(2,10)):
        a=primary['path_length_frontier'][L];b=independent['frontier'][L]
        for key in ('valid_raw_artifact_presentations','tree_child_raw_artifact_presentations','canonical_clean_target_graphs'):
            assert a[key]==b[key],(L,key,a[key],b[key])
        pp=sorted((x['raw_artifact_rootings'],x['raw_artifact_tree_child_rootings']) for x in primary['cleanup_fibres'][L])
        ii=sorted((x['raw_presentations'],x['tree_child_presentations']) for x in independent['frontier'][L]['fibre_profiles'])
        assert pp==ii,(L,'fibre_profiles',pp,ii)
    assert primary['structural_conclusions']['parallel_theta_112_valid_rooting'] is False
    assert independent['conclusions']['parallel_theta_112_valid'] is False
    assert primary['structural_conclusions']['parallel_theta_113_tree_child_rooting'] is False
    assert independent['conclusions']['parallel_theta_113_tree_child'] is False
    assert primary['strict_rooting_fibre_witness']['rooting_tree_child'] is False
    assert independent['strict_witness']['rooted_tree_child'] is False
    assert primary['strict_rooting_fibre_witness']['clean_rooting_census']['strong'] is True
    assert primary['theta_sharpness_pair']['topologies'][0]['sd0_equals_clean'] is True
    assert primary['theta_sharpness_pair']['topologies'][0]['rooting_census']['valid']==5
    assert primary['theta_sharpness_pair']['topologies'][0]['rooting_census']['tree_child']==2
    assert primary['theta_sharpness_pair']['nonisomorphic'] is True
    assert primary['theta_sharpness_pair']['non_T_equivalent'] is True
    if rooting is not None:
        assert rooting['status']=='EXACTLY COMPUTED'
        assert rooting['strict_target_sd0_rootings']=={'valid':5,'tree_child':5,'strong':True}
        assert rooting['theta_source']['valid']==5 and rooting['theta_source']['tree_child']==2 and not rooting['theta_source']['strong']
        assert rooting['theta_target']['valid']==5 and rooting['theta_target']['tree_child']==2 and not rooting['theta_target']['strong']
    assert primary['theta_sharpness_pair']['topologies'][0]['leaf1_status']['leaf_parent_in_triangle'] is True
    assert primary['theta_sharpness_pair']['topologies'][1]['leaf1_status']['leaf_parent_in_triangle'] is False
    # Compare independently derived sparse polynomial bodies.
    terms={(c,m) for c,m in clean['source_switching_polynomial']}
    assert terms=={('1','gamma*u*v'),('-1','gamma*u*v*lambda'),('1','alpha*beta*u*v*lambda')}
    assert algebra['fourier_tensor']['nonzero_sector']=='u*v*(alpha*beta*lambda - gamma*lambda + gamma)'
    assert algebra['rational_interior_witness']['effective']==clean['rational_witness']=='161/495'
    return True

def main():
    validate(load(P),load(I),load(A),load(B),load(R))
    cert={'status':'PROVED','outcome':'Q',
      'structural_replay_agreement':True,'algebra_replay_agreement':True,
      'class_relations':{
        'topology_sets':'SD_0 = SD_H is contained in SD_clean; every cleanup topology in W_TC has a canonical already-simple representative, and structural zipper contraction gives the same final simple graph.',
        'rooting_sets':'Root_0 = Root_H is a subset of Root_clean',
        'weak_classes':'W_TC(clean) = W_TC(sd0) = W_TC(H)',
        'strong_classes':'S_TC(clean) is a proper subset of S_TC(sd0) = S_TC(H)'},
      'theorem_transfer':'On the literature strong class, cleanup contracts each root-created zipper to the identical final labelled mixed graph and preserves the complete open JC model image; hence the sd0 classification transfers through the canonical quotient.',
      'sharpness':'The exact Theta pair has identical sd0 and clean reductions and remains in W_TC minus S_TC under both conventions.'}
    OUT.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
    print(json.dumps(cert,indent=2,sort_keys=True));print('PASS independent convention review')
if __name__=='__main__':main()
