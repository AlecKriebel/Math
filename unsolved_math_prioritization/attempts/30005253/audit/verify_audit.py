#!/usr/bin/env python3
"""Independent exact audit controls. No network or third-party packages required.
Finite tests supplement, and do not replace, the proofs in AUDIT.md.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile

EXPECTED_MANIFEST = '0b6c020816320cf325c05981ba16699ecfc4e6a5a596cb46752494827c9534f4'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(packet):
    manifest = packet / 'SHA256SUMS'
    assert digest(manifest) == EXPECTED_MANIFEST
    files = {}
    for line in manifest.read_text().splitlines():
        expected, name = line.split(maxsplit=1)
        name = name.lstrip('*')
        assert Path(name).name == name
        assert digest(packet / name) == expected
        files[name] = expected
    with tempfile.TemporaryDirectory() as tmp:
        resultfile = Path(tmp) / 'replay.json'
        child = subprocess.run([sys.executable, '-B', str(packet / 'compute_controls.py'),
                                '--output', str(resultfile)], check=True, capture_output=True, text=True)
        replay = json.loads(resultfile.read_text())
        assert resultfile.read_bytes() == (packet / 'control_results.json').read_bytes()
    # Extended nonnegative profiles, including infinite risks.
    extended_profiles = minorants = 0
    values = (0, 1, 2, 3, float('inf'))
    for r in itertools.product(values, repeat=4):
        e = tuple(min(r[i:]) for i in range(4))
        assert all(e[i] <= r[i] for i in range(4))
        assert list(e) == sorted(e)
        assert e == tuple(min(e[i:]) for i in range(4))
        for h in itertools.combinations_with_replacement(values, 4):
            if all(h[i] <= r[i] for i in range(4)):
                assert all(h[i] <= e[i] for i in range(4))
                minorants += 1
        extended_profiles += 1
    stable_pairs = ordered_pairs = 0
    profiles = list(itertools.product(range(4), repeat=3))
    for r, s in itertools.product(profiles, repeat=2):
        er = tuple(min(r[i:]) for i in range(3))
        es = tuple(min(s[i:]) for i in range(3))
        assert max(abs(a-b) for a,b in zip(er,es)) <= max(abs(a-b) for a,b in zip(r,s))
        stable_pairs += 1
        if all(a <= b for a,b in zip(r,s)):
            assert all(a <= b for a,b in zip(er,es))
            ordered_pairs += 1
    # Exact saturation of both uniform lower bound and CV constant two.
    delta, err = F(1,10), F(1,5)
    d = [F(1), F(1)+2*err]
    q = [x+delta for x in d]
    hats = [q[0]+err,q[1]-err]
    assert hats[0] == hats[1]
    assert q[1] == min(d)+delta+2*err
    lower_d = [F(1),F(2)]
    lower_q = [lower_d[0]-delta,lower_d[1]]
    assert min(lower_q) == min(lower_d)-delta
    # Randomization is mixture of risks; averaging predictions is a distinct action.
    # For Y=0, constant predictors -1 and +1 each have squared risk one.
    assert (F(1)+F(1))/2 == 1
    assert ((F(-1)+F(1))/2)**2 == 0
    # Continuous torus probability is checked on a boundary-compatible finite grid.
    # Event s_m < q/m has probability 1/m exactly; <= differs on discrete grids.
    qmod, N, a = 12, 4, 2
    patterns = Counter()
    no_hit = 0
    for u in itertools.product(range(qmod), repeat=N):
        s=0; hits=[]
        for m,x in enumerate(u,1):
            s=(s+x)%qmod
            if m>=a: hits.append(s < qmod//m)
        patterns[tuple(hits)] += 1
        no_hit += not any(hits)
    for pattern,count in patterns.items():
        prob=F(1)
        for m,hit in zip(range(a,N+1),pattern):
            prob *= F(1,m) if hit else 1-F(1,m)
        assert F(count,qmod**N)==prob
    assert F(no_hit,qmod**N)==F(a-1,N)
    # All-prefix hit probabilities versus sparse grid; no independence is needed
    # for the union bound on the sparse grid's random subsamples.
    prefix=[]; sparse=[]; validation=[]
    for N in (17,65,257,1025,10001):
        a=math.isqrt(N)
        a += a*a < N
        miss=F(1)
        for m in range(a,N+1): miss *= 1-F(1,m)
        assert miss==F(a-1,N)
        b=(N+1)//2
        bounded_miss=F(1)
        for m in range(b,N+1): bounded_miss *= 1-F(1,m)
        assert bounded_miss==F(b-1,N)
        prefix.append({'N':N,'ceil_sqrt':a,'miss':str(miss),'bounded_ratio_hit':str(1-bounded_miss)})
    for k in (4,16,64,256):
        # n=k^2, nte=k, ntr=k^2-k, spacing=floor(sqrt(n))=k.
        # Paper (27): xi=1,...,ceil(ntr/k)-2=k-3; sizes 2k,...,(k-2)k.
        n=k*k; ntr=n-k
        sizes=[ntr-xi*k for xi in range(1,(ntr+k-1)//k-1)]
        assert sizes == [j*k for j in range(k-2,1,-1)]
        union=sum((F(1,m) for m in sizes), F(0))
        harmonic=sum((F(1,j) for j in range(2,k-1)),F(0))/k
        assert union==harmonic
        sparse.append({'total_n':n,'candidates':len(sizes),'any_hit_upper_bound':str(union),
                       'display_upper_bound':float(union)})
    for v in range(1,101):
        threshold=(3*v+3)//4
        direct=F(sum(math.comb(v,k) for k in range(v+1) if 2*(2*k-v)>=v),2**v)
        closed=F(sum(math.comb(v,k) for k in range(threshold,v+1)),2**v)
        assert direct==closed
        assert float(direct) <= math.exp(-v/8)+1e-15
        validation.append(str(direct))
    # Independent exact Gaussian algebra across signal energies, ratios and scales.
    gaussian_identity_checks=0
    for b in (F(1,4),F(1),F(4),F(9)):
        for z in (F(3,2),F(2),F(3),F(10)):
            signal=b/z; noise=1/(z-1); tstar=signal/(signal+noise)
            qstar=1+b-signal**2/(signal+noise)
            for t in (F(-1),F(0),F(1,3),F(2,3),F(1),F(2)):
                qt=1+b*(1-1/z)+(t-1)**2*signal+t*t*noise
                assert qt==qstar+(signal+noise)*(t-tstar)**2
                gaussian_identity_checks+=1
    moments=[]
    for m in (4,8,16,64,256,1024):
        # p=2m. beta-projection variance and exact chi-square-ratio moments.
        alpha=F(m,2); beta=F(m,2)
        projection_variance=16*alpha*beta/((alpha+beta)**2*(alpha+beta+1))
        assert projection_variance==F(4,m+1)
        noise_mean=F(m,m-1)
        noise_second=F(m*(m+2),(m-1)*(m-3))
        noise_variance=noise_second-noise_mean**2
        assert noise_variance==F(2*m*(2*m-1),(m-1)**2*(m-3))
        cross_second=F(2,m-1)
        expectation=F(11,3)+F(4,9*(m-1))
        assert expectation<4
        moments.append({'m':m,'projected_energy_variance':str(projection_variance),
                        'noise_mean':str(noise_mean),'noise_variance':str(noise_variance),
                        'cross_term_second_moment':str(cross_second),
                        'full_shrunk_risk_expectation':str(expectation)})
    # Crossovers and exact post-interpolation envelope comparison.
    for z in (F(1001,1000),F(3,2),F(2),F(5,2),F(4),F(1000)):
        risk=1+4*(1-1/z)+1/(z-1)
        assert risk-4==(z-2)**2/(z*(z-1))
        deriv=4/z**2-1/(z-1)**2
        assert deriv==(z-2)*(3*z-2)/(z*z*(z-1)**2)
    assert 1/(1-F(3,4))==4
    # Expected-risk and parameter-uniformity obstructions, distinct from U.
    ui=[]
    for n in (2,4,16,256):
        prob=F(1,n); risk_on_event=n
        assert prob*risk_on_event==1
        ui.append({'n':n,'probability_nonzero':str(prob),'expected_risk':1})
    return {'passed':True,'full_target_proved':False,'audit_kind':'independent finite controls and manual proof audit',
            'frozen_manifest_sha256':EXPECTED_MANIFEST,'frozen_files':files,
            'exact_original_replay_byte_identical':True,'original_counts':replay['finite_controls'],
            'extended_profiles':extended_profiles,'extended_admissible_minorants':minorants,
            'nonexpansiveness_pairs':stable_pairs,'order_pairs':ordered_pairs,
            'selector_bounds_sharp':True,'randomization_versus_aggregation_distinguished':True,
            'torus_grid_states':12**4,'torus_indicator_patterns':len(patterns),
            'prefix_non_square_controls':prefix,'paper_sparse_grid_union_bounds':sparse,
            'validation_threshold_cases':len(validation),'gaussian_general_identity_checks':gaussian_identity_checks,
            'gaussian_moments':moments,'non_uniform_integrability_controls':ui}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent/'audited_packet')
    parser.add_argument('--output',type=Path,default=Path('audit_results.replay.json'))
    args=parser.parse_args()
    result=run(args.packet.resolve())
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':result['passed'],'exact_original_replay_byte_identical':True,
                      'extended_profiles':result['extended_profiles'],'output':str(args.output)},sort_keys=True))
