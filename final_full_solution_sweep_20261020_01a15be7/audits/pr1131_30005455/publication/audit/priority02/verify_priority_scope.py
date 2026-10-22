#!/usr/bin/env python3
"""New independent, read-only and offline priority/scope arithmetic verifier.
Reads only captured files. No network, writes, subprocesses, or original scripts.
This does not establish exhaustive mathematical priority or prove the candidate.
"""
import argparse
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import hashlib
import json
import sys

IMMUTABLE_EXPECTED = {'ACCEPTANCE.json': '5da38bc25bed7fcbb91d0fde4ace8c52feb93173fa4a2bf2c97e32d35b207363', 'MANIFEST.json': 'd030ce2db4fc2369e608763b79dea99cd0f3a51fa299ff8876b05a140c8dd05d', 'MATHEMATICAL_AUDIT.md': '621bded8b4a04118ae17a16930f53e022216ac51223dc5d562c65319826de515', 'PROOF.md': '791ec6c1f849840785afd8ce15e4460b396e108bc2b203d93993cfb0a6103340', 'README.md': 'f2d3e8b6bb0a2bcecf6bf92e72f5116d0659d99161fa48259c73b46fb94ba58f', 'SOURCE_METADATA.json': '329c9bd69659b547020c18a27a25a94b8327811ec37b359f5a5417ae90c138d3', 'SOURCE_REVIEW.md': '828e9b07e7e99ea77add25acb3c6fc256245dca6f83cb2be0dc6cebf8556b55e', 'STATUS.json': '65c99756dfe11e57f15ab7cd4c37fedf33f73adc542f851e5a1bc17ecbb11be3'}
SOURCE_EXPECTED = {'HK2017.pdf': '4c0376677b4aceaa17b88fb8631bf559a4e95e6694296292746e21f9d875199b', 'OWR2023.pdf': '320d7e903924249d1f57536cdf67491b3b5f89de8401c9a7c07800b09ee750c7', 'VHHKR2016.pdf': '2cc51bf8a50a6721a7978c278fc232f84b6ae16d8de885c032dd896871d4d551', 'HHK2021_author.pdf': '600c2e45ebd2db8ea073e046c5cd5dedb77d4b3b932630b3466a7b6165d23f12', 'VHHKR2016_published.pdf': '4cadff8e2160310dd2b10668cc63a153758e82773c7c32061d2ad439ebea7686', 'RuszelThacker2024.pdf': 'ee6e2be7c95a9e0037ccdcd249033391d447847c9e9b2729eea6cbc8158426d0', 'Holmes_author_page.html': 'a1b9c26595336c79f982113a5eea84f2840a8dd7d93667718a96ef57b071a605', 'Hirsch_author_page.html': '3a6a441e73b198f7f675cda9645f7eb982745b90ed6f6a020afdeef9259e1f6b', 'BasuBenaim_withdrawal.html': '7b5d517969c77a49a8b201fc35dd23e67868d767f1591568c67bd66b16b75d8e', 'VHHKR_arxiv_history.html': 'f6eaad8d059cfd282e6dc46859acf242f724235a7f1f4846f88d08a1c980f85c', 'BBCL2015_arxiv.pdf': 'b4837c7e397f74d53591d0c94d2823963f1daa5b536eb848bb9e2fb3f8cad70f', 'BBCL_arxiv_history.html': 'c21f729789b8c9b36dfff346c112b10855abfc39ed3ad32f51b98bac5486dd23', 'HHK2023.pdf': 'ea5801394f0f50c8a6fd28296787091d9607b50deb7931ad3b3a068092d001cd'}

def demand(ok, message):
    if not ok:
        raise ValueError(message)

def verify(root, negative):
    for name, digest in IMMUTABLE_EXPECTED.items():
        data = (root / 'immutable_head' / name).read_bytes()
        if negative == 'immutable_tamper' and name == 'PROOF.md':
            data = data + b'corruption'
        demand(hashlib.sha256(data).hexdigest() == digest, 'immutable capture changed: ' + name)
    for name, digest in SOURCE_EXPECTED.items():
        demand(hashlib.sha256((root / 'private_sources' / name).read_bytes()).hexdigest() == digest,
               'primary capture changed: ' + name)
    # Independent rational exponential upper bound, not a float approximation.
    c = F(9, 4)
    partial = sum((c**k / factorial(k) for k in range(13)), F(0))
    first_tail = c**13 / factorial(13)
    ratio = c / 14
    upper = partial + first_tail / (1 - ratio)
    demand(upper < F(29, 3), 'cannot certify exp(9/4) < 29/3')
    alpha = F(17, 4) if negative == 'old_bound_at_17_4' else F(24)
    demand(alpha > F(81, 4), 'old Lemma 5 prerequisite fails')
    demand(alpha > c * (upper + 1), 'old small edge proof prerequisite fails')
    demand(F(2) - F(9, 2) / alpha > F(3, 2), 'old large edge matching prerequisite fails')
    # Demonstrates that the inherited diagonal test does NOT itself exclude
    # the equal-rate triangle in the new forest interval.
    trial_alpha = F(3, 2)
    q = F(1, 2)
    demand(2*q*q >= (1-1/trial_alpha)*2*q, 'diagonal-test gap control failed')
    demand(3*trial_alpha/4-1 > 0, 'triangle full Hessian instability control failed')
    # The scopes are quantified independently; this flag must not be promoted.
    sharp_whisker_claim = negative == 'sharp_whisker_claim'
    demand(not sharp_whisker_claim, 'sharp whisker target is unsupported')
    candidate_forest = F(4, 3)
    candidate_whisker = F(17, 4)
    demand(candidate_forest < 2 and candidate_whisker < 24 < 25,
           'literal target comparison failed')
    # Uniform weights on a triangle with rates (1,2,3) are not an equilibrium:
    # endpoint reinforcement totals at common positive edge weights are unequal.
    endpoint_totals = [F(1+2,2), F(2+3,2), F(3+1,2)]
    demand(len(set(endpoint_totals)) > 1, 'unequal-rate uniform reduction control failed')
    return {'verdict':'PASS_BOUNDED_PRIORITY_AND_SCOPE_CONTROLS',
            'immutable_files':len(IMMUTABLE_EXPECTED),'fresh_primary_files':len(SOURCE_EXPECTED),
            'old_proof_whisker_threshold_upper':str(c*(upper+1)),
            'old_proof_implies_alpha_ge_24':True,
            'candidate_improves_even_old_implicit_bound':True,
            'uniform_odd_cycle_not_all_equilibria':True,
            'sharp_whisker_4_3_not_established':True,
            'novelty_certified':False,'candidate_mathematics_certified_by_this_script':False}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--negative-control', choices=['immutable_tamper','old_bound_at_17_4','sharp_whisker_claim'])
    args = parser.parse_args()
    try:
        result = verify(args.root, args.negative_control)
    except Exception as exc:
        print(json.dumps({'verdict':'FAIL','reason':str(exc)},sort_keys=True))
        return 1
    print(json.dumps(result,sort_keys=True))
    return 0
if __name__ == '__main__':
    sys.exit(main())
