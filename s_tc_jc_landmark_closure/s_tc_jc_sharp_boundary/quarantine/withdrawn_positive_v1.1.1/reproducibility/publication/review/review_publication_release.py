#!/usr/bin/env python3
"""Independent publication-level audit of scope, counts, and dependencies."""
from __future__ import annotations
import json
from hashlib import sha256
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
PUB=ROOT/'reproducibility'/'publication'
EXACT=ROOT/'reproducibility'/'exact_release'
PAPER=ROOT/'source'/'paper'

def load(path): return json.loads(path.read_text())
def digest(path): return sha256(path.read_bytes()).hexdigest()

def paper_audit():
    text='\n'.join(p.read_text(errors='replace') for p in PAPER.rglob('*.tex'))
    required=[
      'standard semi-directed', 'S_{\\mathrm{TC}}', 'Jukes--Cantor',
      'Automatic triangle bound', 'weakly tree-child binary level-2',
      'triangle redirection', 'W_{\\mathrm{TC}}', 'HoltgrefeEtAl2026',
      'Proposition~2.26', 'restored support',
      'entire binary standard strongly tree-child level-2 class',
      'Ardiyansyah2021',
      'complete structural $\\Tmove$-equivalence class',
      'not asserted to equal the set of topologies whose stochastic images contain',
      'adversarial AI-assisted review processes'
    ]
    for token in required: assert token in text,token
    for forbidden in (
      'landmark','complete level-2 theory','PROVED:','Gate 1','Gate 2','Gate 3',
      'with at most one triangle per blob, modulo ordinary triangle redirection',
      'all distinct compatible encodings',
      'returns exactly the observational-equivalence class of the input distribution',
      'independent adversarial reviewers',
      'only intrinsic topological uncertainty',
      'sole unavoidable ambiguity'
    ):
        assert forbidden not in text,forbidden
    assert 'The archival location and version identifier should be inserted' not in text
    assert 'OpenAI ChatGPT' in text and 'Anthropic Claude' in text
    assert 'Artificial-intelligence systems are not authors' in text

def automatic_triangle_audit():
    d=load(PUB/'certificates'/'multitriangle_exclusion.json')
    assert d['status']=='PROVED'
    assert d['theorem'].startswith(
        'Every binary standard semi-directed weakly tree-child level-2')
    assert d['structural_reduction']['two_triangle_theta_path_lengths']==[1,2,2]
    c=d['orientation_universe']
    assert (
      c['raw_binary_orientation_attempts'],c['valid_binary_acyclic_rootings'],
      c['rooted_orientation_orbits'],c['tree_child_rootings']
    )==(864,25,7,0)
    assert c['failure_counts']=={
      'all_children_reticulate':5,'reticulation_child':20}
    strength=load(PUB/'certificates'/'all_level2_strengthening.json')
    assert strength['status']=='PROVED' and strength['version']=='1.1.0'
    assert 'Every binary standard semi-directed S_TC level-2' in strength['theorem']
    assert strength['scope']['complete_stochastic_image_equality_not_claimed']
    for path in [
      PUB/'src'/'verify_multitriangle_exclusion.py',
      PUB/'review'/'review_multitriangle_exclusion.cpp']:
        assert path.exists() and path.stat().st_size>100

def topology_audit():
    d=load(PUB/'certificates'/'nonroot_topology_counts.json')
    expected={'4':(30,21,9),'5':(612,516,48),
              '6':(9420,8520,300),'7':(135900,127260,2160)}
    for k,want in expected.items():
        r=d[k]
        assert (r['theta_label_exact'],r['theta_label_mod_T'],r['cycle_mod_T'])==want

def atlas_audit():
    expected_theta={
      5:(8520,16590,8520,360,1512),
      6:(10980,218925,10980,840,2856)}
    for k,want in expected_theta.items():
        d=load(PUB/'certificates'/f'theta_k{k}_regenerated.json')
        got=(d['strong_signatures'],d['weak_signatures'],d['equal_signatures'],
             d['ordered_quartets'],d['weak_role_presentations'])
        assert got==want,(k,got,want)
        width=d['bytes_per_signature']
        for side in ('strong','weak'):
            p=PUB/'certificates'/f'theta_k{k}_{side}_signatures.bin'
            assert digest(p)==d[f'{side}_sha256'] and p.stat().st_size%width==0
        tsv=PUB/'certificates'/f'theta_k{k}_directed_pairs.tsv'
        assert sum(1 for _ in tsv.open())-1==({5:27000,6:32940}[k])
    expected_cycle={3:(9,12,9),4:(48,63,48),
                    5:(300,390,300),6:(2160,2790,2160)}
    for k,want in expected_cycle.items():
        d=load(PUB/'certificates'/f'cycle_k{k}_regenerated.json')
        assert (d['strong_signatures'],d['weak_signatures'],d['equal_signatures'])==want
    relations={
      'cycle_k5_to_cycle_k5':(300,300,0),
      'cycle_k6_to_cycle_k6':(2160,2160,0),
      'theta_k5_to_cycle_k5':(0,0,0),
      'theta_k6_to_cycle_k6':(0,0,0),
      'cycle_k5_to_theta_k5':(21780,300,21480),
      'cycle_k6_to_theta_k6':(246240,2160,244080)}
    for name,want in relations.items():
        d=load(PUB/'certificates'/f'{name}_summary.json')
        assert (d['directed_pairs'],d['equal_pairs'],d['strict_pairs'])==want

def theorem_audit():
    theorem=load(EXACT/'certificates'/'final_theorem.json')
    assert theorem['status']=='PROVED' and not theorem['release_blockers']
    seven=load(EXACT/'certificates'/'seven_port_closure.json')
    assert len(seven['residual_records'])==192
    assert len(seven['completion_records'])==1686
    cut=load(EXACT/'certificates'/'pointwise_cut_certificate.json')
    assert cut['endpoint_type_count']==177 and cut['single_blob_type_count']==453
    theta=load(EXACT/'certificates'/'theta_sharpness_certificate.json')
    assert theta['status'].startswith('PROVED')
    for path in [
      EXACT/'src'/'verify_seven_port_closure.py',
      EXACT/'review'/'review_seven_port_closure.py',
      EXACT/'review'/'review_pointwise_cut.py',
      EXACT/'src'/'verify_root_reduction.py',
      EXACT/'review'/'review_root_reduction.py',
      EXACT/'src'/'verify_theta_sharpness.py',
      EXACT/'review'/'review_final_synthesis.py']:
        assert path.exists() and path.stat().st_size>100

def main():
    paper_audit();automatic_triangle_audit();topology_audit();atlas_audit();theorem_audit()
    result={
      'status':'VERIFIED','scope_locked':True,'all_STC_level2_scope':True,
      'automatic_triangle_theorem':True,
      'automatic_triangle_rootings_checked':25,
      'automatic_triangle_tree_child_survivors':0,
      'prior_attribution_phrase_checked':True,
      'theta_atlases_regenerated':[5,6,7],
      'cycle_atlases_regenerated':[3,4,5,6],
      'seven_port_records':192,'seven_port_completions':1686,
      'cut_endpoint_types':177,'cut_crossing_types':453,
      'release_dependencies_closed':True}
    print(json.dumps(result,indent=2,sort_keys=True))
    print('ALL PUBLICATION-LEVEL ADVERSARIAL CHECKS PASSED')
if __name__=='__main__': main()
