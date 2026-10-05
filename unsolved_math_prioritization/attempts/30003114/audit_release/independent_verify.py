#!/usr/bin/env python3
"""Independent exact controls and frozen-packet verifier for 30003114.

Standard library only. No network and no imports from the author's verifier.
Finite controls are not a proof of the all-degree/all-denominator target.
"""
from argparse import ArgumentParser
from bisect import bisect_left
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import comb, gcd, prod
from pathlib import Path
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import zipfile

PROBLEM = 30003114
ARCHIVE_SHA = '443d5dc030e08c32e7a758c0eb1f5ab63eb8673f0a4dfd13930f2a60f568f228'
ARCHIVE_BYTES = 16914
MANIFEST_SHA = '913457490b8f076c4a5035e6bcb32016a69dfe1a6c97a56ad396fc16882e23cf'
FROZEN = {
    'ATTEMPT_LOG.md': (2590, '6e356582e4044c379074209cf3b949b6c048133838b2d308879884e9d3aee87f'),
    'PROOF.md': (12725, '902f1a176ec7f35d20fa6f97c87c641dead4dc254bb4a1db06c179feaefeef5a'),
    'README.md': (998, '74752d1dcabebb5391b73705d3ebbad5206c1b735451e0884909cd23d9b15830'),
    'SOURCE_VERIFICATION.json': (9369, '950e36af1620afc63ed6a19d5354ff7f4619d3f7335a77f8e6409545bff5f18e'),
    'STATUS.json': (1268, '25d34970c0e4cc832dfe1e5f56064474728b1e11eb3f9b13699735a3275e2f43'),
    'VERIFICATION.json': (2782, '70fbfebc2c399f858728a6771903efdf0068e6d1fdf3779b781111050c3fd652'),
    'verify.py': (5395, 'e2d6300920765e5a63184e357163bf87f335adf9400d7376da1bfa0c5e9d9eb2'),
    'MANIFEST.json': (1186, MANIFEST_SHA),
}
A, B = F(9, 10), F(19, 20)
R, RAD = F(97, 100), F(99, 100)
GAMMA = (1 - 3 * B**22) / (1 - B**22)
BLASCHKE_A = RAD / (RAD**2 + R * B)
C0 = F(100)**(-95)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify_integrity(safe, archive=None):
    safe = Path(safe)
    entries = list(safe.rglob('*'))
    require(all(p.is_file() and not p.is_symlink() for p in entries), 'non-regular packet entry')
    require({str(p.relative_to(safe)) for p in entries} == set(FROZEN), 'packet allowlist mismatch')
    for name, (size, digest) in FROZEN.items():
        data = (safe / name).read_bytes()
        require((len(data), sha(data)) == (size, digest), 'frozen bytes mismatch: ' + name)
    manifest = json.loads((safe / 'MANIFEST.json').read_text())
    require(set(manifest['files']) == set(FROZEN) - {'MANIFEST.json'}, 'manifest file set')
    for name, record in manifest['files'].items():
        require((record['bytes'], record['sha256']) == FROZEN[name], 'manifest entry: ' + name)
    status = json.loads((safe / 'STATUS.json').read_text())
    require(status['status'] == 'no_resolution' and status['intended_problem_solved'] is False,
            'status overclaim')
    if archive is not None:
        data = Path(archive).read_bytes()
        require((len(data), sha(data)) == (ARCHIVE_BYTES, ARCHIVE_SHA), 'archive freeze mismatch')
        with zipfile.ZipFile(archive) as z:
            expected = {'safe/' + n for n in FROZEN}
            require(len(z.infolist()) == len(expected) and set(z.namelist()) == expected,
                    'archive member set')
            for info in z.infolist():
                require(not info.is_dir(), 'unexpected archive directory')
                require((info.external_attr >> 16) & 0o170000 != 0o120000, 'archive symlink')
                name = info.filename.removeprefix('safe/')
                require(z.read(info) == (safe / name).read_bytes(), 'archive/directory mismatch')
    return {'pass': True, 'safe_file_count': len(FROZEN), 'archive_checked': archive is not None,
            'manifest_sha256': MANIFEST_SHA, 'archive_sha256': ARCHIVE_SHA}


def numerators(p, q, d, alphabet=(-1, 0, 1)):
    # Independent Horner recursion; values have denominator q**d at completion.
    vals = [0]
    qpower = 1
    for _ in range(d + 1):
        vals = [p * v + c * qpower for v in vals for c in alphabet]
        qpower *= q
    return vals


def arithmetic_controls():
    parameters = sorted({(p, q) for q in range(1, 51) for p in range(1, q)
                         if gcd(p, q) == 1 and A <= F(p, q) <= B}
                        | {(91, 100), (101, 110), (9001, 10000), (9499, 10000)})
    cases = total = thresholds = 0
    for p, q in parameters:
        require(q >= 10, 'minimum denominator')
        maxd = 9 if (p, q) in ((9, 10), (19, 20)) else 6
        for d in range(maxd + 1):
            vals = numerators(p, q, d)
            av = sorted(map(abs, vals))
            require(len(vals) == len(set(vals)) == 3**(d+1), 'rational injectivity')
            require(vals.count(0) == 1 and min(v for v in av if v) >= 1, 'rational separation')
            for s in (F(1, 2), F(1), F(3, 2), F(2), F(10), F(q**d, 10)):
                n = bisect_left(av, s)
                ceil = -(-s.numerator // s.denominator)
                require(n <= 2 * ceil - 1 <= 2 * s + 1, 'strict lattice inequality')
                thresholds += 1
            require(bisect_left(av, 1) == 1, 'strict lattice unit threshold')
            for cap in (q, max(q, 50), max(q, 10000)):
                require(bisect_left(av, F(q, cap)**d) == 1, 'bounded denominator corollary')
            cases += 1
            total += len(vals)
    return {'pass': True, 'reduced_parameters': len(parameters), 'polynomial_families': cases,
            'polynomial_evaluations': total, 'threshold_checks': thresholds,
            'degrees': '0..9 at interval endpoints; 0..6 otherwise',
            'parameter_scope': 'all reduced target rationals q<=50 plus four listed larger-denominator points',
            'larger_denominator_points': ['91/100', '101/110', '9001/10000', '9499/10000']}


def collision_controls():
    parameters = [(1, 100), (1, 3), (1, 2), (2, 3), (9, 10), (19, 20), (99, 100)]
    thresholds = families = 0
    for p, q in parameters:
        for d in range(9):
            av = sorted(map(abs, numerators(p, q, d)))
            for v in sorted(set(av) - {0}):
                count = bisect_left(av, v)
                # t=v/q**d. Cross-multiplied collision bound, entirely integral.
                require((count + 1) * (q**(d+1) + v * (q-p))
                        >= 2**(d+2) * v * (q-p), 'collision bound at critical threshold')
                thresholds += 1
            require(len(av) >= 2**(d+2) - 1, 'collision bound at infinite threshold limit')
            families += 1
    # Independently enumerate ordered pairs, preserving coefficient vectors, not values.
    pairs = 0
    for n in range(1, 9):
        words = list(product((0, 1), repeat=n))
        c = Counter(tuple(a-b for a, b in zip(u, v)) for u in words for v in words if u != v)
        require(len(c) == 3**n - 1, 'every nonzero ternary difference realized')
        for diff, multiplicity in c.items():
            require(multiplicity == 2**diff.count(0) <= 2**(n-1), 'collision multiplicity')
        require(max(c.values()) == 2**(n-1), 'multiplicity upper bound attained')
        pairs += len(words) * (len(words)-1)
    # Check bin occupancy, ordered collision count and polynomial map jointly.
    partitions = 0
    for x in (F(1,2), A, B):
        T = 1/(1-x)
        for n in range(1, 7):
            words = list(product((0,1), repeat=n))
            vals = [sum(bit*x**i for i,bit in enumerate(w)) for w in words]
            for t in (F(1,100), F(1,3), T/3, T, 2*T):
                K = -(-(T/t).numerator // (T/t).denominator)
                bins = Counter(v//t for v in vals)
                require(max(bins) < K and all(0 <= v < T for v in vals), 'half-open bin endpoints')
                require(sum(m*m for m in bins.values()) * K >= len(words)**2, 'Cauchy occupancy')
                good = [(u,v) for u in range(len(words)) for v in range(len(words))
                        if u != v and vals[u]//t == vals[v]//t]
                require(all(abs(vals[u]-vals[v]) < t for u,v in good), 'strict same-bin differences')
                distinct = {tuple(a-b for a,b in zip(words[u],words[v])) for u,v in good}
                require(len(distinct)*2**(n-1) >= len(good), 'collision quotient')
                partitions += 1
    return {'pass': True, 'families': families, 'critical_thresholds': thresholds,
            'all_positive_thresholds_for_each_tested_family': True,
            'all_threshold_reason': 'count is constant between critical values; RHS increases; infinite tail checked by limit',
            'ordered_binary_pairs': pairs, 'word_lengths': [1,8], 'bin_partitions': partitions}


def lacunary_controls():
    require(GAMMA > 0 and 3*19**22 < 20**22, 'L22 positivity')
    cases = digits = 0
    for x, L, degs in [(A,22,(21,22,43,44,66,110)), (B,22,(21,22,43,44,66,110)),
                        (F(37,40),22,(44,88)), (F(1,2),2,(4,8,12))]:
        for d in degs:
            m = d//L+1
            weights = [x**(i*L) for i in range(m)]
            vals = sorted(sum(c*w for c,w in zip(cs,weights))
                          for cs in product((-1,0,1),repeat=m))
            gamma = GAMMA if L == 22 else (1-3*x**L)/(1-x**L)
            low = (A if L == 22 else x)**d * gamma
            require(low > 0 and len(vals) == len(set(vals)), 'lacunary distinctness')
            require(min(v-u for u,v in zip(vals,vals[1:])) >= low, 'lacunary spacing')
            # Every open interval of length low contains at most one selected-digit value.
            # Strictness is necessary if the minimum spacing equals low.
            cases += 1
            digits += len(vals)
    return {'pass': True, 'selected_digit_families': cases, 'assignments': digits,
            'gamma': str(GAMMA), 'maximum_target_degree': 110,
            'limitation': 'Only selected coefficient blocks are enumerated; conditioning extension is mathematical.'}


def sqnorm(z):
    return z[0]**2 + z[1]**2


def analytic_constants_controls():
    require(F(99,97)**225 < 100 < F(99,97)**226, 'Jensen K=226')
    require((R+B)/(R-B) == 96, 'Harnack constant')
    require(BLASCHKE_A == F(2475,4754) and 0 < BLASCHKE_A < 1, 'Blaschke A')
    require(C0 == F(1,100**95), 'positive Harnack prefactor')
    alphas = [(F(i,10),F(j,10)) for i in range(-9,10,3) for j in range(-9,10,3)
              if 0 < F(i*i+j*j,100) <= R**2] + [(R,F(0)),(F(0),R)]
    boundaries = lower = 0
    for ar,ai in alphas:
        require(sqnorm((ar,ai)) < RAD**2, 'Blaschke pole lies outside radius r')
        for u in map(F,range(-4,5)):
            zr = RAD*(1-u*u)/(1+u*u)
            zi = RAD*2*u/(1+u*u)
            numerator = RAD**2 * sqnorm((zr-ar,zi-ai))
            denominator = sqnorm((RAD**2-ar*zr-ai*zi, ar*zi-ai*zr))
            require(numerator == denominator > 0, 'Blaschke unit boundary modulus')
            boundaries += 1
        for x in (A,F(37,40),B):
            denominator = (RAD**2-ar*x)**2+(ai*x)**2
            require(denominator <= (RAD**2+R*B)**2, 'Blaschke factor denominator bound')
            distance2 = (x-ar)**2+ai*ai
            require(RAD**2*distance2 >= BLASCHKE_A**2*distance2*denominator,
                    'squared Blaschke distance bound')
            lower += 1
    return {'pass': True, 'K':226, 'H':96, 'A':str(BLASCHKE_A),
            'boundary_identities':boundaries,'distance_bounds':lower,
            'limitation':'Exact constant and factor controls, not executable verification of Jensen or Harnack.'}


def expand_product(exponents):
    c = {0:1}
    for m in exponents:
        out = Counter(c)
        for k,v in c.items():
            out[k+m] -= v
        c = {k:v for k,v in out.items() if v}
    return c


def product_controls():
    randomizer = random.Random(30003114)
    sequences = [[],[1],[1,2,4,8,16,32,64,128],[3,7,12,25]]
    for length in range(1,8):
        for _ in range(6):
            seq=[]
            for j in range(length):
                seq.append(sum(seq)+randomizer.randint(1,5))
            sequences.append(seq)
    for seq in sequences:
        require(all(m > sum(seq[:j]) for j,m in enumerate(seq)), 'superincreasing input')
        c = expand_product(seq)
        require(set(c.values()) <= {-1,1} and len(c) == 2**len(seq), 'subset sum uniqueness')
        require(all(m >= 2**j >= j+1 for j,m in enumerate(seq)), 'exponent growth')
        for order in range(len(seq)):
            require(sum(v*comb(k,order) for k,v in c.items()) == 0, 'vanishing Taylor coefficient')
        lead = sum(v*comb(k,len(seq)) for k,v in c.items())
        require(lead == (-1)**len(seq)*prod(seq) != 0, 'exact multiplicity')
        for x in (A,F(37,40),B):
            value = sum(v*x**k for k,v in c.items())
            require(value == prod(1-x**m for m in seq) > 0, 'product polynomial identity')
            rational_log_upper = sum(x**m/(1-x**m) for m in seq)
            require(rational_log_upper <= B/(1-B)**2 == 380, 'logarithmic majorant')
    return {'pass':True,'superincreasing_sequences':len(sequences),
            'maximum_number_of_factors':max(map(len,sequences)),
            'multiplicity_check':'all Taylor coefficients through the asserted order; leading coefficient exact'}


def negative_controls():
    out=[]
    def detected(name,condition,witness):
        require(condition, 'negative control failed: '+name)
        out.append({'mutation':name,'detected':True,'witness':witness})
    vals=numerators(9,10,1)
    detected('remove_modulus',sum(v<0 for v in vals)==4 and F(100,99)<4,
             'Four negative polynomials at d=1; exp(.01)<=100/99<4.')
    detected('allow_d_zero_strict_target',sum(abs(v)<F(1,2) for v in (-1,0,1))==1,
             'The zero polynomial gives 1, whereas exp(0)=1.')
    detected('change_strict_threshold_to_closed',sum(abs(v)<1 for v in vals)==1
             and sum(abs(v)<=1 for v in vals)==3,
             'At x=9/10,d=1,t=1/10: strict count 1; closed count 3.')
    detected('replace_ternary_alphabet',len(numerators(9,10,1))==9
             and len(numerators(9,10,1,(-1,1)))==4,'Nine ternary versus four signed-binary vectors at d=1.')
    half=numerators(1,2,1)
    detected('drop_q_greater_than_two_for_injectivity',len(set(half))<len(half),
             'At 1/2 the different ternary polynomials x and 1-x evaluate equally.')
    detected('claim_binary_difference_map_is_injective',8*7>3**3-1,
             'For three bits, 56 distinct ordered pairs produce only 26 nonzero ternary differences.')
    detected('halve_maximum_difference_multiplicity',2**(8-1)>2**(8-2),
             'Difference vector (1,0,...,0), length 8, has exactly 128 realizations, not at most 64.')
    detected('use_L21_with_positive_gamma',(1-3*B**21)/(1-B**21)<0,
             'At 19/20 the proposed L=21 gamma is negative; its required positive threshold disappears.')
    detected('drop_product_separation',expand_product([1,1])=={0:1,1:-2,2:1},
             '(1-x)^2 has coefficient -2.')
    detected('drop_origin_factor_from_localization',A**10000<C0*BLASCHKE_A**226,
             'P=x^10000 at x=9/10 has f=1 and delta=1, but violates the lower bound with a^d deleted.')
    detected('claim_fewer_than_226_zeros_without_removing_origin',10000>226,
             'P=x^10000 has 10000 zeros at the origin; Jensen must be applied to f, not P.')
    detected('apply_Harnack_on_r_instead_of_zero_free_R',(R+B)/(R-B)>(RAD+B)/(RAD-B),
             'Positive harmonic h(z)=Re((R+z)/(R-z)) has h(b)/h(0)=96, above the r-disk factor 97/2.')
    detected('claim_bound_denominator_independent_by_prefactor',F(100,20)**20>10**12,
             '(q/Q)^d=5^d grows without bound; this refutes the estimate manipulation, not the target.')
    detected('read_probability_as_count',3**45*F(1,3**3)==3**42 > 1,
             'The missing conversion factor is 3^(d+1); at d=44,m=3 the actual bound is 3^42.')
    return out


def replay_author(safe):
    env=dict(os.environ)
    env.pop('PYTHONOPTIMIZE',None)
    env['PYTHONDONTWRITEBYTECODE']='1'
    require(subprocess.check_output([sys.executable,'-c','print(__debug__)'],env=env).strip()==b'True',
            'assertions disabled in author subprocess')
    result=subprocess.run([sys.executable,str(Path(safe)/'verify.py')],env=env,capture_output=True,check=False)
    require(result.returncode==0,'author verification failed')
    require(result.stdout==(Path(safe)/'VERIFICATION.json').read_bytes(),'author output differs')
    return {'pass':True,'assertions_enabled':True,'returncode':result.returncode,
            'byte_exact_output_match':True,'output_sha256':sha(result.stdout)}


def corruption_controls(safe):
    outcomes=[]
    with tempfile.TemporaryDirectory(prefix='littlewood-integrity-controls-') as tmp:
        tmp=Path(tmp)
        for name in ('edited_proof','missing_file','extra_source_file','manifest_change','symlink_entry'):
            target=tmp/name
            shutil.copytree(safe,target)
            if name=='edited_proof':
                p=target/'PROOF.md';p.write_bytes(p.read_bytes()+b'\n')
            elif name=='missing_file':
                (target/'STATUS.json').unlink()
            elif name=='extra_source_file':
                (target/'source_extract.txt').write_text('synthetic unsafe extra; no source text')
            elif name=='manifest_change':
                p=target/'MANIFEST.json';p.write_bytes(p.read_bytes()+b' ')
            else:
                (target/'README.md').unlink();(target/'README.md').symlink_to(Path(safe)/'README.md')
            caught=False
            try:
                verify_integrity(target)
            except RuntimeError:
                caught=True
            require(caught,'corruption not rejected: '+name)
            outcomes.append({'mutation':name,'rejected':True})
    return outcomes


def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--safe',type=Path)
    parser.add_argument('--archive',type=Path)
    args=parser.parse_args()
    require(__debug__ and sys.flags.optimize==0,'Run without -O/-OO/PYTHONOPTIMIZE; disabled assertions are not verification.')
    require(args.archive is None or args.safe is not None,'--archive requires --safe')
    result={'problem_id':PROBLEM,'verdict':'PASS_FOR_SCOPED_PARTIALS','target_resolved':False,
            'assertions_enabled':True,'arithmetic':'exact integers and fractions; standard library only',
            'arithmetic_controls':arithmetic_controls(),'collision_controls':collision_controls(),
            'lacunary_controls':lacunary_controls(),'analytic_constants':analytic_constants_controls(),
            'product_controls':product_controls(),'negative_controls':negative_controls(),
            'limits':['Finite enumeration does not prove the target or its all-degree partial theorems.',
                      'Jensen, maximum principle, and Harnack are verified by mathematical audit, not this script.',
                      'Public-source bytes are separately corroborated; this offline script does not access the web.']}
    if args.safe is not None:
        result['frozen_integrity']=verify_integrity(args.safe,args.archive)
        result['author_replay']=replay_author(args.safe)
        result['corruption_controls']=corruption_controls(args.safe)
        result['frozen_integrity_after_replay']=verify_integrity(args.safe,args.archive)
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
