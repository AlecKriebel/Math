#!/usr/bin/env python3
"""Assemble the fail-closed sharp-boundary theorem certificate.

No discovery occurs here.  The certificate is emitted only after every local,
root, cut, gluing, triangle, sharpness, and final-review dependency passes.
"""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
C=ROOT/'certificates'
REPORT=ROOT/'report'/'FINAL_SHARP_BOUNDARY_THEOREM.md'
FINAL_REVIEW=ROOT/'review'/'final_synthesis_review.json'
OUT=C/'final_theorem.json'


def load_path(path):return json.loads(path.read_text())
def load(name):return load_path(C/name)
def digest(path):return sha256(path.read_bytes()).hexdigest()


def dependency(path):
    assert path.exists(),path
    return {'path':str(path.relative_to(ROOT)),'sha256':digest(path),'bytes':path.stat().st_size}


def build():
    seven=load('seven_port_closure.json')
    seven_review=load('seven_port_adversarial_review.json')
    bounded=load('bounded_support_lift.json')
    root=load('root_reduction.json')
    root_review=load('root_reduction_adversarial_review.json')
    cut=load('pointwise_cut_certificate.json')
    cut_review=load('pointwise_cut_adversarial_review.json')
    gluing=load('positive_gluing.json')
    triangle=load('ordinary_triangle_T_certificate.json')
    theta=load('theta_sharpness_certificate.json')
    final_review=load_path(FINAL_REVIEW)
    nonroot_output=load('nonroot_dependencies_output.txt')

    assertions={
      'seven_port_primary_passes':seven['status']=='PROVED' and seven['classification']['stochastic_disjointness']==192,
      'seven_port_no_survivor':seven['classification']['lower_dimensional_or_one_sided_or_full_overlap']==0,
      'seven_port_independent_review':seven_review['status']=='VERIFIED' and seven_review['all_pairs_stochastically_disjoint'],
      'seven_port_complete_duplicate_free':seven_review['residual_records']==192 and seven_review['completed_graph_codes_independently_unique']==1686,
      'seven_port_universal_tensor_transport':seven_review['universal_reduced_tensor_checks']=={'649':270,'705':216},
      'generic_dimensions_exact':seven_review['cycle_dimensions_replayed']==7 and seven_review['theta_dimensions_replayed']==65,
      'bounded_support_lift_closed':bounded['status']=='PROVED' and bounded['maximum_outgoing_ports_needed']==7,
      'all_ordered_port_covariance':nonroot_output['all_ordered_quartets_k5']==360 and nonroot_output['all_ordered_quartets_k6']==840 and nonroot_output['auxiliary_incoming_role_covariant'],
      'root_reduction_closed':root['status']=='PROVED' and root_review['status']=='VERIFIED' and root_review['complete_JC_image_germ_preserved'],
      'retained_arrowhead_root_case_checked':root_review['retained_reticulation_switching_checks']==8,
      'pointwise_cut_closed':cut['status']=='PROVED' and cut_review['status']=='VERIFIED',
      'two_active_endpoint_closed':cut_review['two_active_endpoint_contradiction']=='VERIFIED' and cut_review['two_active_endpoint_minors_checked']==4,
      'cut_signs_independently_replayed':cut_review['distinct_factor_Bernstein_expansions_checked']==547 and cut_review['strict_wrong_split_minor_signs_checked']==421,
      'positive_gluing_closed':gluing['status']=='PROVED' and gluing['dimension_additivity'] and gluing['positive_context_contraction'],
      'ordinary_T_closed':triangle['status']=='PROVED' and triangle['all_sources_standard_S_TC'] and triangle['distinct_labelled_semi_directed_orientations']==3 and triangle['rank_minor_determinant']!='0',
      'theta_sharpness_closed':theta['status']=='PROVED_EXACTLY_COMPUTED' and theta['not_triangle_equivalent'] and theta['theta_pair_classes']['N']['W_TC'] and not theta['theta_pair_classes']['N']['S_TC'] and theta['theta_pair_classes']['N_prime']['W_TC'] and not theta['theta_pair_classes']['N_prime']['S_TC'],
      'final_adversarial_review':final_review['status']=='VERIFIED' and not final_review['quarantined_dependency'],
    }
    assert all(assertions.values()),{key:value for key,value in assertions.items() if not value}

    text=REPORT.read_text()
    assert '**PROVED.** Let \\(N,N\'\\) be leaf-labelled networks in the stated class.' in text
    assert 'S_{\\rm TC}\\text{ is generically JC-identifiable modulo }T' in text
    assert 'W_{\\rm TC}\\setminus S_{\\rm TC}' in text
    assert 'every one of the 192 residual relations has disjoint complete open' in text.lower()
    assert 'one-sided open containment therefore preserves cuts' in text.lower()

    # Fixed-leaf finiteness: tree-child paths from the root and all r
    # reticulations end at distinct leaves, so r+1<=n.  With t=n+r-2,
    # |V|=1+n+r+t=2n+2r-1<=4n-3.
    for n in range(2,101):
        for r in range(n):
            t=n+r-2
            assert 1+n+r+t==2*n+2*r-1<=4*n-3

    paths={
      'seven_port_primary':C/'seven_port_closure.json',
      'seven_port_independent_review':C/'seven_port_adversarial_review.json',
      'corrected_completion_census':C/'cycle_theta_support_completion_corrected.json',
      'theta_k5_summary':C/'canonical_theta_k5_summary.json',
      'theta_k6_summary':C/'canonical_theta_k6_special_summary.json',
      'theta_k5_signs':C/'canonical_theta_k5_strict_signs.json',
      'theta_k6_signs':C/'canonical_theta_k6_special_strict_signs.json',
      'theta_equal_replay':C/'canonical_theta_k5_equal_presentation_replay.json',
      'cycle_cross_summary':C/'canonical_cycle_cross_summary.json',
      'frozen_nonroot_dependencies':C/'nonroot_dependencies_output.txt',
      'bounded_support_lift':C/'bounded_support_lift.json',
      'root_reduction':C/'root_reduction.json',
      'root_reduction_independent_review':C/'root_reduction_adversarial_review.json',
      'pointwise_cut':C/'pointwise_cut_certificate.json',
      'pointwise_cut_independent_review':C/'pointwise_cut_adversarial_review.json',
      'positive_gluing':C/'positive_gluing.json',
      'ordinary_T':C/'ordinary_triangle_T_certificate.json',
      'theta_sharpness':C/'theta_sharpness_certificate.json',
      'final_adversarial_review':FINAL_REVIEW,
      'report':REPORT,
    }

    result={
      'status':'PROVED',
      'release_blockers':[],
      'assertions':assertions,
      'classes':{
        'R_TC':'supplied rooted DAG is tree-child',
        'W_TC':'standard semi-directed topology has at least one tree-child rooted partner',
        'S_TC':'every admissible rooted partner is tree-child',
      },
      'scope':'binary leaf-labelled standard semi-directed S_TC level-2 networks under open JC, with at most one triangle per blob',
      'primary_theorem':(
        'For binary standard semi-directed S_TC level-2 networks with at most '
        'one triangle per blob, N preceq_JC N_prime occurs if and only if the '
        'labelled homeomorphism-reduced bridge trees agree and every corresponding '
        'local factor is labelled-isomorphic or related by ordinary triangle '
        'redirection T.'
      ),
      'generic_corollary':'S_TC is generically JC-identifiable modulo T.',
      'sharpness':'For every n>=4, W_TC\\S_TC contains a non-T Theta pair with a full-dimensional regular JC overlap.',
      'seven_port':{
        'records':192,'S4_orbits':8,'canonical_completions':1686,
        'cycle_dimension':15,'theta_dimension':17,
        'classification':'all complete open stochastic images are disjoint',
      },
      'proof_chain':[
        'pointwise cut preservation forces equality of labelled bridge trees',
        'positive Fourier cut inversion extracts local projective joint tensors',
        'the complete bounded nonroot atlas and seven-port closure leave only labelled isomorphism/T',
        'root reduction places every S_TC root factor in the root-independent nonroot joint-tensor atlas',
        'positive analytic gluing localizes directed containment and composes every valid T-relative',
        'fixed-leaf finiteness makes the union of all non-T exceptional intersections algebraically proper',
      ],
      'reconstruction':[
        'recover cut splits by rank-at-most-four flattenings',
        'peel positive rank-one Fourier blocks',
        'classify local restrictions through seven outgoing ports',
        'reconstruct ordered port words from one- and two-port probes',
        'return the lexicographically least valid T-quotient mixed-graph code',
      ],
      'exceptional_locus':'finite union of proper rank/invariant degeneracy sets and proper closures of intersections with non-T topologies, pulled back by the dominant source parameterization',
      'fixed_leaf_finiteness':{'reticulation_bound':'r<=n-1','vertex_bound':'|V|<=4n-3'},
      'dependencies':{key:dependency(path) for key,path in paths.items()},
    }
    return json.loads(json.dumps(result,sort_keys=True))


def main():
    result=build()
    if '--check' in sys.argv:
        assert result==json.loads(OUT.read_text())
    else:
        OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({
      'status':result['status'],
      'primary_theorem':result['primary_theorem'],
      'sharpness':result['sharpness'],
      'release_blockers':result['release_blockers'],
    },indent=2,sort_keys=True))

if __name__=='__main__':main()
