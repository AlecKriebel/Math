#!/usr/bin/env python3
"""Replay exact counts and produce small, checkable mathematical certificates."""
import argparse
from collections import deque
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
from math import factorial, prod
from pathlib import Path
import subprocess
import tempfile

BASE = Path(__file__).resolve().parents[1]

def adj_square(n):
    return [tuple(w for w in range(n*n)
                  if abs(v//n-w//n)+abs(v%n-w%n) == 1)
            for v in range(n*n)]

def forest_certificate(n, roots):
    """BFS spanning forest with two roots; deterministic and all edges explicit."""
    adj = adj_square(n)
    parent = [-2]*(n*n)
    q = deque(roots)
    order = list(roots)
    for r in roots:
        parent[r] = -1
    while q:
        v=q.popleft()
        for w in adj[v]:
            if parent[w] == -2:
                parent[w]=v; q.append(w); order.append(w)
    size=[1]*(n*n)
    for v in reversed(order):
        if parent[v] >= 0:
            size[parent[v]] += size[v]
    denom=prod(size[v] for v in range(n*n) if v not in roots)
    assert factorial(n*n-2) % denom == 0
    lower=2*factorial(n*n-2)//denom
    labels=[0]*(n*n)
    for rank,v in enumerate(order):
        labels[v]=n*n-rank
    found=[v for v in range(n*n) if all(labels[v]>labels[w] for w in adj[v])]
    assert sorted(found)==sorted(roots)
    return dict(n=n, roots=roots, parent=parent, subtree_sizes=size,
                certified_two_peak_labels=labels,
                top_two_root_labeling_lower_bound=lower)

def main(write=False):
    if not write and (BASE/'MANIFEST.json').exists():
        manifest=json.loads((BASE/'MANIFEST.json').read_text())
        for item in manifest['files']:
            b=(BASE/item['path']).read_bytes()
            assert len(b)==item['bytes']
            assert hashlib.sha256(b).hexdigest()==item['sha256']
    expected=json.loads((BASE/'results/exact_counts.json').read_text())
    with tempfile.TemporaryDirectory() as tmp:
        exe=str(Path(tmp)/'count_peaks')
        subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror',
                        '-pedantic',str(BASE/'code/count_peaks.cpp'),'-o',exe],check=True)
        actual=json.loads(subprocess.check_output([exe],text=True))
    assert actual==expected
    summaries=[]
    forests=[]
    for s in actual['squares']:
        n=s['n']; N=n*n; counts=s['two_peak_distance_counts']; z=sum(counts)
        assert sum(s['peak_histogram'])==factorial(N)
        assert z==s['peak_histogram'][2]
        assert all(c>=0 for c in counts)
        mean=Fraction(sum(d*c for d,c in enumerate(counts)),n*z)
        summaries.append(dict(n=n, total_two_peak_labelings=z,
                              probability_two_peaks=str(Fraction(z,factorial(N))),
                              conditional_mean_rho_over_n=str(mean),
                              conditional_tail_rho_at_least_n=str(Fraction(sum(counts[n:]),z))))
        pairs={(a,b):c for a,b,c in s['pair_counts']}
        # Every admissible pair, including maximal separation, gets an explicit
        # two-peak labeling and a valid spanning-forest lower bound.
        for roots,c in pairs.items():
            if c:
                cert=forest_certificate(n,list(roots))
                assert cert['top_two_root_labeling_lower_bound']<=c
                forests.append(cert)

    s=actual['squares'][1]
    pairs={(a,b):c for a,b,c in s['pair_counts']}
    z=sum(pairs.values())
    ma=sum(c for (a,b),c in pairs.items() if 0 in (a,b))
    mb=sum(c for (a,b),c in pairs.items() if 8 in (a,b))
    joint=Fraction(pairs[(0,8)],z)
    marginal_product=Fraction(ma*mb,z*z)
    covariance=joint-marginal_product
    assert covariance==Fraction(-7485,2244004)

    adj=adj_square(3)
    masks=[sum(1<<w for w in ns) for ns in adj]
    @lru_cache(None)
    def completions(s):
        if s==511:
            return 1
        return sum(completions(s|(1<<v)) for v in range(9)
                   if not (s>>v)&1 and masks[v]&s)
    prefix=3
    next_counts={str(v):completions(prefix|(1<<v)) for v in range(9)
                 if not (prefix>>v)&1 and masks[v]&prefix}
    assert next_counts=={'2':156,'3':180,'4':336}
    cut_labels=[4,6,7,10,12,5,1,16,14,11,13,15,3,2,8,9]
    cut_adj=adj_square(4)
    crop={4*x+y for x in range(3) for y in range(3)}
    full_peaks=[v for v in range(16) if all(cut_labels[v]>cut_labels[w] for w in cut_adj[v])]
    crop_peaks=sorted(v for v in crop if all(cut_labels[v]>cut_labels[w]
                                           for w in cut_adj[v] if w in crop))
    assert full_peaks==[7,8] and crop_peaks==[2,8,10]
    out=dict(status='PASS', graph='P_n Cartesian-product P_n; no wraparound',
             replay_matches_frozen_counts=True,
             checked_sizes=[2,3,4], brute_force_checked_sizes=[2,3],
             exact_pair_methods=['allowed roots and subtraction','direct exact roots'],
             separate_total_method='birth-count histogram dynamic program',
             summaries=summaries,
             conditioned_independence_counterexample=dict(
                 n=3,vertices=[0,8],distance=4,closed_neighborhoods_disjoint=True,
                 event='exactly two peaks',joint=str(joint),
                 marginal_product=str(marginal_product),covariance=str(covariance)),
             boundary_growth_counterexample=dict(n=3,condition='one peak at vertex 0',
                 descending_prefix=[0,1],next_completion_counts=next_counts,
                 denominator=completions(prefix),
                 next_probabilities={v:str(Fraction(c,completions(prefix))) for v,c in next_counts.items()}),
             forest_certificate_count=len(forests),
             block_restriction_counterexample=dict(n=4,labels_row_major=cut_labels,
                 whole_square_peaks=full_peaks,top_left_3_by_3_peaks=crop_peaks,
                 interpretation='Two global peaks can induce three peaks on a sub-square.'),
             asymptotic_conclusion='None; the square limit remains unresolved.')
    if write:
        (BASE/'results/verification.json').write_text(json.dumps(out,indent=2)+'\n')
        (BASE/'results/forest_certificates.json').write_text(json.dumps(forests,indent=2)+'\n')
    else:
        assert out==json.loads((BASE/'results/verification.json').read_text())
        assert forests==json.loads((BASE/'results/forest_certificates.json').read_text())
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--write',action='store_true',help='regenerate derived certificates')
    main(parser.parse_args().write)
