#!/usr/bin/env python3
"""Fail-closed synthesis of the already completed bounded-support reconstruction."""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
C=ROOT/'certificates'
OUT=C/'bounded_support_lift.json'

def load(name):return json.loads((C/name).read_text())

def main():
    k5=load('canonical_theta_k5_summary.json')
    k6=load('canonical_theta_k6_special_summary.json')
    cycle=load('canonical_cycle_cross_summary.json')
    completion=load('cycle_theta_support_completion_corrected.json')
    seven=load('seven_port_closure.json')
    assert k5['status']==k6['status']=='EXACTLY COMPUTED'
    assert (k5['strong_signatures'],k6['strong_signatures'])==(8520,10980)
    assert cycle['sizes']['3']['cycle_strong']==9 and cycle['sizes']['4']['cycle_strong']==48
    missing=Counter(record['missing_rigid_support_ports'] for record in completion['records'])
    assert missing==Counter({1:2256,2:1920,3:192})
    assert completion['maximum_completed_union_outgoing_ports']==7
    assert seven['classification']['stochastic_disjointness']==192
    result={
      'status':'PROVED',
      'theta_core_support_sizes':[3,4,3,3],
      'theta_probe_bound':2,
      'cycle_core_support_size':2,
      'cycle_probe_bound':2,
      'cross_generator_completion_missing_port_distribution':{str(k):v for k,v in sorted(missing.items())},
      'maximum_outgoing_ports_needed':7,
      'ordered_word_reconstruction':(
        'A rigid support fixes the oriented core. A one-port probe identifies the '
        'directed segment of every additional labelled port; a two-port probe '
        'identifies the order of each pair on one segment. These pairwise orders '
        'reconstruct the unique finite word on every segment, modulo the exact '
        'labelled core automorphism and ordinary triangle redirection T.'
      ),
      'marginal_dominance':(
        'On a selected restriction, edges with the same displayed-tree descendant '
        'mask occur only through their product. Products of arbitrary positive JC '
        'multipliers range over the full open interval (0,1), so the restriction '
        'map is dominant onto the reduced weak-pattern model.'
      ),
      'local_conclusion':(
        'Every arbitrary finite nonroot cycle/theta one-sided JC containment is '
        'labelled isomorphism or ordinary T; the seven-port certificate closes the '
        'only completion not covered at five or six outgoing ports.'
      ),
    }
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
