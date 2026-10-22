#!/usr/bin/env python3
"""Independent replay and provenance audit; no source document redistribution."""
import hashlib, json, subprocess, sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
PUBLIC=BASE/'public'
EXPECTED='adc5a1fd1921cd735eb6b02266e76e7748b79cffc73d2c49be6560b42877498a'
def info(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def run(p):
 q=subprocess.run([sys.executable,str(p)],capture_output=True,text=True,check=True)
 return json.loads(q.stdout)
m=json.loads((PUBLIC/'SHA256SUMS.json').read_text())
assert info(PUBLIC/'SHA256SUMS.json')['sha256']==EXPECTED
actual={str(p.relative_to(PUBLIC)) for p in PUBLIC.rglob('*') if p.is_file() and p.name!='SHA256SUMS.json' and '__pycache__' not in p.parts}
assert actual==set(m['files'])
for f,v in m['files'].items():assert info(PUBLIC/f)==v
before={f:info(PUBLIC/f) for f in sorted(actual)}
controls=run(PUBLIC/'verify.py')
assert controls==json.loads((PUBLIC/'CHECKS.json').read_text())
manifest=run(PUBLIC/'verify_manifest.py')
assert manifest['manifest_sha256']==EXPECTED
assert controls['inverse_pair_checks']==controls['disk_defect_identity_checks']==controls['difference_identity_checks']==4761
# Independent symbolic verification, without importing author code.
p,q,x,y=sp.symbols('p q x y',real=True)
a=p+sp.I*q;u=x+sp.I*y;bar=p-sp.I*q
phi=(u-a)/(1-bar*u)
psi=(phi+a)/(1+bar*phi)
assert sp.cancel(psi-u)==0
D=(1-bar*u)*(1-a*sp.conjugate(u))
N=(u-a)*(sp.conjugate(u)-bar)
assert sp.expand(D-N-(1-p*p-q*q)*(1-x*x-y*y))==0
assert sp.cancel(phi+a-(1-p*p-q*q)*u/(1-bar*u))==0
s=sp.symbols('s',positive=True)
# Evaluates the radial integrals after taking the angular means.
primitive=lambda t:t*t*sp.log(t)/2-t*t/4
potential=-2*sp.pi*(s*s*sp.log(s)/2+primitive(sp.Integer(1))-primitive(s))
assert sp.simplify(potential-sp.pi*(1-s*s)/2)==0
assert sp.limit(potential,s,0,dir='+')==sp.pi/2
src=json.loads((PUBLIC/'SOURCE_MANIFEST.json').read_text())
files=['hayman-lingham-2018.pdf','stephenson-1988-web.json','bishop-1993.pdf']
source_observations={}
for f,e in zip(files,src['sources']):
 observed=info(BASE/'private'/f)
 assert observed=={'bytes':e['observed_content_bytes'],'sha256':e['observed_content_sha256']}
 source_observations[f]=observed
source_observations['stephenson-independent-web.json']=info(HERE/'private'/'stephenson-independent-web.json')
corpus=BASE.parent/'rank548-6200007'/'sources'/'problems.json'
cobs=info(corpus)
cmeta=src['corpus_provenance']['problems']
assert cobs=={'bytes':cmeta['observed_bytes'],'sha256':cmeta['observed_sha256']}
assert cobs['sha256']!=cmeta['repository_manifest_sha256']
records=json.loads(corpus.read_text())
selected=[r for r in records if r.get('id')==2305066]
assert selected==json.loads((BASE/'private'/'selected-problems.json').read_text())
assert len(selected)==1
assert before=={f:info(PUBLIC/f) for f in sorted(actual)}
assert info(PUBLIC/'SHA256SUMS.json')['sha256']==EXPECTED
out={
 'result':'pass', 'frozen_public_manifest_sha256':EXPECTED,
 'public_files_checked':len(actual),'frozen_package_unchanged':True,
 'author_controls_replayed':controls, 'author_manifest_replayed':manifest,
 'independent_symbolic_checks':['automorphism inverse','disk-defect polynomial identity','difference identity','Green-kernel radial integral','Green-kernel s=0 limit'],
 'source_artifact_hashes_replayed':source_observations,
 'recovered_problems_corpus':cobs,
 'selected_recovered_record_matches':True,
 'problems_corpus_matches_repository_snapshot':False,
 'research_results_full_corpus_rehash':'not independently reproduced; full 80334822-byte file unavailable to auditor',
 'mathematical_verdict':'pass at published-theorem dependency level',
 'classification_recommendation':'already_solved', 'turns_recommendation':'1/5',
 'remote_writes':False,
 'limitations':['Symbolic and finite controls do not prove the Riemann-surface construction or infinite limit arguments.','Stephenson readable complete article is OCR-bearing web text; publisher PDF not obtained or visually checked.','Source PDF bytes and private web-response artifacts are not part of the public audit manifest.','Live duplicate checks were not repeated; author point-in-time artifacts were inspected.']
}
print(json.dumps(out,indent=2,sort_keys=True))
