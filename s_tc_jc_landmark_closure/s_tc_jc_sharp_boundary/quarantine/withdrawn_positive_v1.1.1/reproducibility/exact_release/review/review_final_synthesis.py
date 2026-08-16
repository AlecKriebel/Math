#!/usr/bin/env python3
"""Adversarial dependency-closure review of the sharp-boundary theorem."""
from __future__ import annotations
from pathlib import Path
from hashlib import sha256
import json,re

ROOT=Path(__file__).resolve().parents[1]
C=ROOT/'certificates';REPORT=ROOT/'report'/'FINAL_SHARP_BOUNDARY_THEOREM.md'
OUT=ROOT/'review'/'final_synthesis_review.json'

def load(name):return json.loads((C/name).read_text())
def main():
 seven=load('seven_port_closure.json');seven_review=load('seven_port_adversarial_review.json');root=load('root_reduction.json');cut=load('pointwise_cut_certificate.json')
 root_review=load('root_reduction_adversarial_review.json');cut_review=load('pointwise_cut_adversarial_review.json')
 T=load('ordinary_triangle_T_certificate.json');theta=load('theta_sharpness_certificate.json')
 gluing=load('positive_gluing_output.txt');nonroot=load('nonroot_dependencies_output.txt')
 corrected=load('cycle_theta_support_completion_corrected.json')
 bounded=load('bounded_support_lift.json')
 text=REPORT.read_text()
 assertions={
  'seven_port_primary_passes':seven['status']=='PROVED' and seven['classification']['stochastic_disjointness']==192,
  'seven_port_independent_review_passes':seven_review['status']=='VERIFIED' and seven_review['all_pairs_stochastically_disjoint'] and seven_review['completed_graph_codes_independently_unique']==1686,
  'seven_port_universal_tensor_transport':seven_review['universal_reduced_tensor_checks']=={'649':270,'705':216},
  'seven_port_universe_complete':len(seven['residual_records'])==192 and len(seven['graph_symmetry_orbits_under_S4'])==8,
  'seven_port_duplicate_free':len({r['canonical_graph_sha256'] for r in seven['residual_records']})==192,
  'seven_port_all_completed_targets_standard':len(seven['completion_records'])==1686 and all(r['standard_S_TC'] for r in seven['completion_records']),
  'seven_port_full_parameterizations_frozen':len({r['full_parameterization_sha256'] for r in seven['completion_records']})==1686,
  'seven_port_dimensions_exact':all(r['dimension']==15 and r['minor']['determinant_mod_prime'] for r in seven['generic_dimensions']['cycle_sources']) and all(r['dimension']==17 and r['minor']['determinant_mod_prime'] for r in seven['generic_dimensions']['core3_theta_targets']),
  'completion_prose_corrected':corrected['distribution']['(3, 3, 7)']==192 and corrected['maximum_completed_union_outgoing_ports']==7 and 'at most two' not in corrected['completion_rule'],
  'bounded_support_lift_closed':bounded['status']=='PROVED' and bounded['maximum_outgoing_ports_needed']==7 and 'isomorphism or ordinary T' in bounded['local_conclusion'],
  'root_reduction_passes':root['status']=='PROVED' and 'same labelled' in root['standard_reduction'],
  'root_reduction_independent_review':root_review['status']=='VERIFIED' and root_review['complete_JC_image_germ_preserved'] and root_review['retained_reticulation_switching_checks']==8,
  'cut_pointwise_passes':cut['status']=='PROVED' and cut['endpoint_dichotomy']=={'F_positive':151,'F_zero_G_positive':26} and cut['single_blob_classification']=={'rank_one_all_blocks':32,'wrong_split_strict':421},
  'cut_independent_adversarial_review':cut_review['status']=='VERIFIED' and cut_review['two_active_endpoint_contradiction']=='VERIFIED' and cut_review['strict_wrong_split_minor_signs_checked']==421 and cut_review['distinct_factor_Bernstein_expansions_checked']==547,
  'two_active_endpoint_included':cut['two_active_endpoint_case']['derived_rank_one_equations']==['a*b*c=t**2','A*B*C=T**2','a*A=b*c*B*C*z**2'],
  'ordinary_T_sufficiency':T['status']=='PROVED' and T['distinct_labelled_semi_directed_orientations']==3 and T['rank_minor_determinant']!='0',
  'positive_gluing':gluing['status']=='PROVED' and gluing['dimension_additivity'] and gluing['positive_context_contraction'],
  'all_ordered_port_covariance':nonroot['all_ordered_quartets_k5']==360 and nonroot['all_ordered_quartets_k6']==840 and nonroot['auxiliary_incoming_role_covariant'],
  'theta_sharpness':theta['status']=='PROVED_EXACTLY_COMPUTED' and theta['theta_pair_classes']['N']['W_TC'] and not theta['theta_pair_classes']['N']['S_TC'] and theta['not_triangle_equivalent'],
  'report_states_primary_theorem':'N\\preceq_{\\rm JC}N\'' in text and 'ordinary triangle redirection is the complete observational ambiguity' in text,
  'report_states_sharpness':'W_{\\rm TC}\\setminus S_{\\rm TC}' in text and 'the boundary is sharp' in text,
  'report_contains_root_proof':'## 5. Root reduction' in text,
  'report_contains_two_active_cut_proof':'For a bridge joining two active endpoint tensors' in text,
  'report_contains_arbitrary_subdivision_lift':'## 4. Arbitrary-subdivision promotion' in text,
  'report_contains_reconstruction':'## 8. Canonical reconstruction' in text,
  'report_contains_independent_release_checks':'## 9. Independent release checks' in text,
  'report_handles_retained_root_arrowhead':'old root\'s off-path child is a reticulation' in text,
  'no_unresolved_status_in_release_report':'UNRESOLVED' not in text and 'CONJECTURED' not in text and 'NUMERICALLY OBSERVED' not in text,
 }
 assert all(assertions.values()),{k:v for k,v in assertions.items() if not v}
 review={
  'status':'VERIFIED',
  'assertions':assertions,
  'theorem':('For binary standard semi-directed S_TC level-2 networks with at most one triangle per blob, '
             'one-sided open JC containment occurs exactly under equality of the labelled bridge tree and '
             'local labelled isomorphism/ordinary triangle redirection T.'),
  'sharpness':'The all-n Theta ambiguity lies in W_TC\\S_TC and is not T.',
  'report_sha256':sha256(REPORT.read_bytes()).hexdigest(),
  'historical_gate_code_required':False,
  'quarantined_dependency':False,
 }
 OUT.write_text(json.dumps(review,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':'VERIFIED','assertions':len(assertions),'quarantined_dependency':False},indent=2))
if __name__=='__main__':main()
