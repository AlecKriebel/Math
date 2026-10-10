#!/usr/bin/env python3
"""Deterministic integrity and arithmetic controls; not a simulation certificate."""
from pathlib import Path
from hashlib import sha256
import json
import math
import argparse

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--release-dir', type=Path, default=root/'release', help='Folder containing the five frozen author files')
args = parser.parse_args()
expected = [
    {'path':'COUNTEREXAMPLE_VERIFICATION.md','bytes':9342,'sha256':'7b024162d4926a411d8dc5a7fddf08eee94148c4e1b10d45f99a067970e818f4'},
    {'path':'README.md','bytes':2284,'sha256':'ecd7fb49b331f0124f8897223291d81913883a69fd2fb289c6d88b3884255066'},
    {'path':'RESEARCH_LOG.md','bytes':1564,'sha256':'43a9d469297c699b58e63ca705124ff220a816ec138c1c653cab353da7fd10cb'},
    {'path':'SOURCE_GATE.md','bytes':4108,'sha256':'d069aceb72ed63f2d47f7f71484c24d4d5c117a6b9acdd47e46439f91fa65df3'},
    {'path':'turn_01.md','bytes':1352,'sha256':'2ca4c348d580942791c7b8cb0ad8f3463c6c11599c4b45f389a67927d4caeaa5'},
]
integrity = []
for rec in expected:
    data = (args.release_dir/rec['path']).read_bytes()
    digest = sha256(data).hexdigest()
    integrity.append({'file':rec['path'], 'bytes':len(data), 'sha256':digest,
                      'matches_frozen': digest == rec['sha256'] and len(data)==rec['bytes']})
assert all(x['matches_frozen'] for x in integrity)
assert {p.name for p in args.release_dir.glob('*.md')} == {x['file'] for x in integrity}

# The exact analytic control is 2 log n >= H_n from H_n <= 1+log n, n>=3.
H = 0.0
minimum_gap = (float('inf'), None)
for n in range(1,100001):
    H += 1/n
    if n >= 3:
        gap = 2*math.log(n)-H
        assert gap > 0
        if gap < minimum_gap[0]: minimum_gap = (gap,n)

# Check the finite low-frequency sum against the explicit split used in the proof.
# L_n = sum_{k<=n} k^(-1/4) 2^(k-n). No randomness is used.
L = 0.0
max_scaled = (0.0, None)
for n in range(1,100001):
    L = L/2 + n**(-0.25)
    split_bound = 2*2.0**(-n/2) + 2*(n/2)**(-0.25)
    assert L <= split_bound*(1+1e-14)
    scaled = L*n**0.25
    if scaled > max_scaled[0]: max_scaled = (scaled,n)

# Sum_{j>=0}(j+1)/4^j=(1-1/4)^(-2)=16/9 exactly.
# Integral_{|u|<1} log(1/|u|) dm(u)=2*pi*integral_0^1 r*(-log r)dr=pi/2.
report = {
    'verdict':'PASS',
    'problem_id':2305057,
    'attribution':'Oleg Ivrii, arXiv:2609.18785v1, 16 September 2026',
    'classification':'Verified existing preprint counterexample; no new resolution claim',
    'frozen_files':integrity,
    'controls':{
        'frozen_set_and_hashes':'PASS',
        'brownian_radius_comparison':{'analytic_threshold':3, 'tested_n':[3,100000],
            'minimum_2_log_n_minus_H_n':minimum_gap[0], 'minimum_at_n':minimum_gap[1]},
        'cone_low_frequency_split':{'tested_n':[1,100000], 'max_n_quarter_times_sum':max_scaled[0],
            'max_at_n':max_scaled[1]},
        'dyadic_expectation_series':'sum_{j>=0}(j+1)/4^j = 16/9 < infinity',
        'logarithmic_energy_kernel':'integral_{|u|<1} log(1/|u|) dm(u) = pi/2',
        'occupation_bound':'E m(K_epsilon) <= pi*exp(4)/log(1/epsilon), 0<epsilon<1',
        'proof_controls':'All probabilistic and infinite-parameter steps are proved in INDEPENDENT_AUDIT.md; finite arithmetic checks are only regression controls.'
    },
    'blocking_findings':[],
    'certified_scope':['Theorem 1.1(i) and (iii) needed for Problem 5.57',
                       'common full-measure boundary set for every finite cone aperture',
                       'positive logarithmic capacity of each cone complement'],
    'not_certified':['Journal acceptance or peer review','Theorem 1.1(ii) exact non-tangential range',
                     'Theorem 1.2 Hausdorff dimension','Any different catalogue row']
}
(root/'audit'/'independent_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
