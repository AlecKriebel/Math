"""Root reproduction of the new whole-package adversary, privately and in full."""
from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess
import sympy as s

A = Path(__file__).resolve().parent
D = A / 'clean_final_adversary'
W = A / 'tmp/root_clean_math'
assert not W.exists(), 'Do not overwrite a previous run.'
W.mkdir(parents=True)
C = W / 'control'
C.mkdir()
PY = A.parent / 'pr378_30004322/sources_effective_review/private_runtime/bin/python'
def sha(b): return hashlib.sha256(b).hexdigest()
def bind(p, e):
    b=p.read_bytes()
    assert len(b)==e['bytes'] and sha(b)==e['sha256'], str(p)
    return b
mf=json.loads((D/'PUBLIC_MANIFEST.json').read_text())
before={str(D/'PUBLIC_MANIFEST.json'):sha((D/'PUBLIC_MANIFEST.json').read_bytes())}
for e in mf['files']:
    assert not {'tmp','private','raw_sources'} & set(Path(e['path']).parts)
    p=D/e['path'];b=bind(p,e);before[str(p)]=sha(b)
    q=C/e['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
seals=[]
for name in ['BASELINE_SEALED.sha256','MATHEMATICAL_VERDICT_SEALED.sha256']:
    for line in (D/name).read_text().splitlines():
        h,p=line.split(None,1);assert sha((D/p.strip()).read_bytes())==h
        seals.append({'seal':name,'path':p.strip(),'sha256':h})
snapshot=json.loads((A/'snapshot_manifest.json').read_text())
for e in snapshot['files']:
    b=bind(A/'snapshot'/e['path'],e)
    q=W/'snapshot'/e['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
shutil.copyfile(A/'snapshot_manifest.json',W/'snapshot_manifest.json')
T='unsolved_math_prioritization/attempts/7800012'
shutil.copytree(W/'snapshot'/T,C/'tmp/private_candidate')
source_bindings=[]
for e in json.loads((A/'snapshot'/T/'SOURCE_MANIFEST.json').read_text())['primary_sources']:
    b=bind(D/'tmp/private_sources/source_names'/e['file'],e)
    assert b==(A/'raw_sources'/e['file']).read_bytes()
    q=C/'tmp/private_sources/source_names'/e['file'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
    source_bindings.append({'file':e['file'],'bytes':len(b),'sha256':sha(b),'root_and_fresh_downloads_equal':True})
pairs=[(f'root_turn{i}.stdout',f'author_turn{i}'+('_correct_cwd' if i==4 else '')+'.stdout') for i in range(1,6)]
pairs += [('root_public_author_replay.stdout','author_replay.stdout'),('root_source_bound_author_replay.stdout','author_replay_sources.stdout'),('root_source_bound_author_replay.stdout','final_ignored_replay_sources.stdout'),('root_historical_independent.stdout','prior_independent.stdout'),('root_public_review_wrapper.stdout','prior_wrapper.stdout'),('root_public_review_wrapper.stdout','final_ignored_prior_wrapper.stdout')]
stream_bindings=[]
for root,other in pairs:
    b=(A/root).read_bytes();assert b==(D/'streams'/other).read_bytes(),other
    stream_bindings.append({'root':root,'reviewer':other,'bytes':len(b),'sha256':sha(b)})
programs=[]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
for label,program,expected in [('universal','independent_universal.py','independent_universal.stdout'),('boundary','independent_boundary.py','independent_boundary_reproducible.stdout'),('hessian','independent_hessian.py','final_ignored_independent_hessian.stdout'),('provenance','provenance.py','provenance.stdout')]:
    r=subprocess.run([str(PY),'-B',str(C/program)],cwd=C,env=env,capture_output=True)
    (A/f'root_clean_{label}.stdout').write_bytes(r.stdout);(A/f'root_clean_{label}.stderr').write_bytes(r.stderr)
    assert r.returncode==0 and not r.stderr,(label,r.returncode,r.stderr.decode())
    assert r.stdout==(D/'streams'/expected).read_bytes(),label
    programs.append({'label':label,'program':program,'exit_code':r.returncode,'full_stdout_byte_exact':True,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_empty':True})
    print(label+': PASS',flush=True)
for name in ['FULL_HESSIAN.json','FULL_FOURIER_BLOCKS.json']:
    assert (C/name).read_bytes()==(D/name).read_bytes(),name
a=json.loads((C/'PROVENANCE_CERTIFICATE.json').read_text());b=json.loads((D/'PROVENANCE_CERTIFICATE.json').read_text())
a.pop('at');b.pop('at');assert a==b
# Compare all independently reduced-resolvent entries to the previously root-
# reproduced four-projector derivation. Its symbolic text uses the same edge order.
h=json.loads((C/'FULL_HESSIAN.json').read_text());assert h['scale']==2304
lines=(A/'hessian_holonomy_review/public/independent_full_hessian.txt').read_text().splitlines()
assert len(lines)==128 and all(len(x.split(','))==128 for x in lines)
cache={};rad=s.sqrt(3)
for i,line in enumerate(lines):
    for j,expr in enumerate(line.split(',')):
        if expr not in cache:
            v=s.expand(s.sympify(expr)*2304);b=s.expand(v).coeff(rad);a=s.simplify(v-b*rad)
            assert a.is_Integer and b.is_Integer;cache[expr]=[int(a),int(b)]
        assert h['matrix'][i][j]==cache[expr],(i,j)
assert all(sha(Path(p).read_bytes())==v for p,v in before.items())
receipt={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'workflow_percent':90,'original_resolution_percent':0,'scope':'Whole mathematical/original-head review reproduced; later repaired-head queue gate pending','public_manifest_sha256':sha((D/'PUBLIC_MANIFEST.json').read_bytes()),'public_files':len(mf['files']),'seals':seals,'sources':source_bindings,'full_prior_streams':stream_bindings,'programs':programs,'complete_hessian_entries_byte_exact':16384,'full_fourier_blocks_byte_exact':64,'all_hessian_entries_equal_previous_root_reproduced_derivation':True,'provenance_certificate_equal_except_utc':True,'reviewer_files_unchanged':True,'literal_python':str(PY)}
(A/'root_clean_mathematical_reproduction_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'PASS','public_files':len(mf['files']),'sources':3,'streams':len(pairs),'programs':len(programs),'matrix_entries':16384,'blocks':64}))
