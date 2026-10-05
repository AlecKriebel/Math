#!/usr/bin/env python3
"""Read-only binding check; exact controls and optional FEM replay in temporary copies."""
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile, zipfile

ap = argparse.ArgumentParser()
ap.add_argument('--packet', type=Path, required=True)
ap.add_argument('--archive', type=Path, required=True)
ap.add_argument('--numerical', action='store_true')
args = ap.parse_args()
p = args.packet.resolve()
expected_zip = '02d7ebf85303b54d4643a79c266f0273d7881d80cddc0ddd215db2be2d35e6d9'
expected_manifest = '63fb043ce525074d79d5731b8f8cf583df52cf8cdb029bfa22531bc31644952e'
hash_bytes = lambda b: hashlib.sha256(b).hexdigest()
assert hash_bytes(args.archive.read_bytes()) == expected_zip
assert hash_bytes((p/'MANIFEST.json').read_bytes()) == expected_manifest
manifest = json.loads((p/'MANIFEST.json').read_text())
for entry in manifest['files']:
    data = (p/entry['path']).read_bytes()
    assert len(data) == entry['bytes']
    assert hash_bytes(data) == entry['sha256']
with zipfile.ZipFile(args.archive) as z:
    names = z.namelist()
    expected = {'packet/MANIFEST.json'} | {'packet/'+e['path'] for e in manifest['files']}
    assert set(names) == expected and len(names) == len(expected)
    for name in names:
        assert z.read(name) == (p/Path(name).name).read_bytes()

# Reconstruct Bessel signs using different truncation orders from the author.
def bessel(n, z, last):
    term = (z/2)**n/Q(factorial(n))
    total = term
    for k in range(1,last+1):
        term *= -z*z / (4*k*(k+n))
        total += term
    return total
signs = []
for n,z,sign in [(0,Q(12,5),1),(0,Q(241,100),-1),
                 (1,Q(383,100),1),(1,Q(96,25),-1)]:
    assert z*z/4 < 2*(n+2)  # From k=1 onward, terms strictly decrease.
    lower,upper = bessel(n,z,21),bessel(n,z,22)
    assert lower < upper
    assert lower > 0 if sign > 0 else upper < 0
    signs.append({'n':n,'z':str(z),'certified_sign':sign})
assert Q(241,100)**2 < 8

# Recover Bernstein coefficients through rational interpolation and elimination,
# rather than the author's power-basis conversion formula.
a,b = Q(241,100)**2/4,Q(96,25)**2/4
matrix=[]
for j in range(9):
    s=Q(j,8); t=a+(b-a)*s
    value=sum((-1)**k*t**k/Q(factorial(k)**2) for k in range(9))
    matrix.append([Q(comb(8,k))*s**k*(1-s)**(8-k) for k in range(9)]+[value])
for col in range(9):
    pivot=next(row for row in range(col,9) if matrix[row][col])
    matrix[col],matrix[pivot]=matrix[pivot],matrix[col]
    divisor=matrix[col][col]
    matrix[col]=[v/divisor for v in matrix[col]]
    for row in range(9):
        if row != col:
            factor=matrix[row][col]
            matrix[row]=[x-factor*y for x,y in zip(matrix[row],matrix[col])]
beta=[row[-1] for row in matrix]
assert all(x<0 for x in beta)
record=json.loads((p/'exact_results.json').read_text())
assert [str(x) for x in beta] == record['bernstein_coefficients']

# Independent pi bracket via the classical Machin identity and alternating bounds.
def atan(z,n):
    return sum((-1)**k*z**(2*k+1)/Q(2*k+1) for k in range(n+1))
pi_lower=16*atan(Q(1,5),7)-4*atan(Q(1,239),8)
pi_upper=16*atan(Q(1,5),8)-4*atan(Q(1,239),7)
assert Q(157,50)<pi_lower<pi_upper<Q(22,7)
x_upper=Q(241,100)**2; y_upper=Q(96,25)**2
D_lower=Q(383,100)**2-x_upper
D_upper=y_upper-Q(12,5)**2
pi_lo,pi_hi=Q(157,50),Q(22,7)
assert D_lower>3*pi_hi*pi_hi/4 and D_upper<3*pi_lo*pi_lo/2
assert pi_lo*pi_lo>8
th_upper=1-3*pi_lo*pi_lo/(4*D_upper)
margin=D_lower-3*pi_hi*pi_hi/4-3*pi_hi*pi_hi*x_upper/(16*D_lower)-th_upper*y_upper/16
assert margin==Q(273124119,3618160000)>0

with tempfile.TemporaryDirectory(prefix='area-gap-audit-') as temp:
    copy=Path(temp)/'packet'
    shutil.copytree(p,copy,ignore=shutil.ignore_patterns('__pycache__'))
    exact=subprocess.check_output([sys.executable,'-B','verify_exact.py'],cwd=copy)
    assert exact==(p/'exact_results.json').read_bytes()
    assert json.loads(exact)['assertions']==2031
    manifest_output=json.loads(subprocess.check_output([sys.executable,'-B','verify_manifest.py'],cwd=copy))
    numerical=None
    if args.numerical:
        env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'}
        for script,output in [('numerical_challenge.py','numerical_results.json'),
                              ('refine_stadium.py','stadium_refinement.json')]:
            subprocess.run([sys.executable,'-B',script],cwd=copy,env=env,check=True,stdout=subprocess.DEVNULL)
            assert (copy/output).read_bytes()==(p/output).read_bytes()
        runs=json.loads((copy/'numerical_results.json').read_text())['results']+json.loads((copy/'stadium_refinement.json').read_text())['results']
        assert len(runs)==28 and all(r['margin']>0 for r in runs)
        numerical={'runs':28,'byte_identical_to_frozen_outputs':True,
            'minimum_ritz_gap_margin':min(r['margin'] for r in runs),
            'maximum_matrix_relative_residual':max(v for r in runs for v in r['matrix_relative_residuals']),
            'stadium_normalized_gaps':[r['normalized_gap'] for r in runs if r['kind']=='stadium' and r['param']==10],
            'certified_pde_gap_bounds':False}

print(json.dumps({'status':'PASS_SCOPED_CONTROLS','archive_sha256':expected_zip,
    'manifest_sha256':expected_manifest,'manifest_replay':manifest_output,
    'archive_entries':14,'author_exact_assertions':2031,'author_exact_output_byte_identical':True,
    'independent_bessel_signs':signs,'independent_bernstein_reconstruction_matches':True,
    'independent_pi_bracket':'157/50 < pi < 22/7',
    'independent_ellipse_margin':str(margin),'numerical_replay':numerical,
    'scope':'Artifact and scoped-control checks; not an unrestricted conjecture proof.'},indent=2))
