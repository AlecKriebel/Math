"""Full private reproduction of four distinct additive family packages."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime, hashlib, json, os, subprocess

A=Path(__file__).resolve().parent
W=A/'tmp/root_family_reproduction'
assert not W.exists(), 'Preserve previous runs.'
W.mkdir(parents=True)
PY=A.parent/'pr378_30004322/sources_effective_review/private_runtime/bin/python'
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(p,e):
    b=p.read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'],str(p)
    return b
specs=[('probability_review/public','PUBLIC_EVIDENCE_MANIFEST.json',31),('moments_review','MANIFEST.json',28),('diagonal_review','PUBLIC_MANIFEST.json',29),('probability_review/extension_adversary/public','PUBLIC_EVIDENCE_MANIFEST.json',12)]
members=[];before={};seals=[]
for folder,name,count in specs:
    D=A/folder;mf=json.loads((D/name).read_text());assert len(mf['files'])==count
    before[str(D/name)]=sha((D/name).read_bytes())
    C=W/folder;C.mkdir(parents=True,exist_ok=True);(C/name).write_bytes((D/name).read_bytes())
    for e in mf['files']:
        assert not {'tmp','raw_sources'} & set(Path(e['path']).parts)
        p=D/e['path'];b=bind(p,e);before[str(p)]=sha(b)
        q=C/e['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
    members.append(dict(folder=folder,manifest=name,sha256=sha((D/name).read_bytes()),members=count))
# JSON seals have their original relative-path bases.
for name in ['independent_seal_manifest.json','candidate_verdict_seal.json']:
    D=A/'probability_review'
    for e in json.loads((D/'public'/name).read_text())['files']:
        bind(D/e['path'],e);seals.append(dict(seal=name,path=e['path'],sha256=e['sha256']))
for e in json.loads((A/'diagonal_review/INDEPENDENCE_SEAL.json').read_text())['sealed_files']:
    bind(A/'diagonal_review'/e['path'],e);seals.append(dict(seal='diagonal',path=e['path'],sha256=e['sha256']))
D=A/'moments_review'
for name in ['PRE_CANDIDATE_SEAL.sha256','MATHEMATICAL_VERDICT.sha256']:
    h,p=(D/name).read_text().split(None,1);assert sha((D/p.strip()).read_bytes())==h
    seals.append(dict(seal=name,path=p.strip(),sha256=h))
original=(D/'tmp/MATHEMATICAL_VERDICT.original_sealed.md').read_bytes()
assert sha(original)==(D/'MATHEMATICAL_VERDICT.original_sealed.sha256').read_text().split()[0]
lines=original.splitlines(keepends=True);current=(D/'MATHEMATICAL_VERDICT.md').read_bytes().splitlines(keepends=True)
assert lines[:2]==current[:2] and lines[3:]==current[3:]
# Verify that every family author/historical complete stream equals root's
# previously reproduced stream, without repeating successful author checks.
pairs=[]
for i in range(1,6):
    for folder,name in [('probability_review/public',f'candidate_turn{i}.stdout'),('diagonal_review',f'author_turn_{i}.stdout')]:
        b=(A/f'root_turn{i}.stdout').read_bytes();assert b==(A/folder/name).read_bytes()
        pairs.append(dict(family=folder,file=name,sha256=sha(b)))
for folder,name in [('probability_review/public','historical_independent_checks.stdout'),('diagonal_review','historical_independent.stdout')]:
    b=(A/'root_historical_independent.stdout').read_bytes();assert b==(A/folder/name).read_bytes()
    pairs.append(dict(family=folder,file=name,sha256=sha(b)))
assert (D/'author_turn5.stdout').read_bytes()==(A/'root_turn5.stdout').read_bytes()
source_names=['OWR_2019_50.pdf','FGK_2022_arxiv.pdf','FGK_2023_published.pdf','Mao_Song_2026.pdf','de_la_Breteche_Tenenbaum_2026.pdf']
sources=json.loads((A/'snapshot/unsolved_math_prioritization/attempts/30004293/SOURCE_MANIFEST.json').read_text())
source_bindings=[]
for name in source_names:
    b=(A/'raw_sources'/name).read_bytes()
    source_bindings.append(dict(file=name,bytes=len(b),sha256=sha(b)))
for item,name in zip(json.loads((D/'SOURCE_IDENTITY.json').read_text())['sources'],source_names):
    assert sha((D/'tmp/sources'/(item['identity']+'.pdf')).read_bytes())==item['sha256']==sha((A/'raw_sources'/name).read_bytes())
jobs=[
 ('probability_independent','probability_review/public','independent_controls.py','independent_controls.stdout',()),
 ('probability_cross','probability_review/public','cross_boundary_controls.py','cross_boundary_controls.stdout',()),
 ('moments_independent','moments_review','independent_controls.py','independent_controls.stdout',()),
 ('diagonal_independent','diagonal_review','independent_controls.py','independent_controls.stdout',('utc','runtime')),
 ('diagonal_insertion','diagonal_review','insertion_kernel_controls.py','insertion_kernel_controls.stdout',('utc',)),
 ('extension_independent','probability_review/extension_adversary/public','independent_rank_controls.py','independent_rank_controls.stdout',()),
 ('probability_integrity','probability_review/public','verify_public_evidence.py',None,()),
 ('extension_integrity','probability_review/extension_adversary/public','verify_extension.py',None,())]
def run(job):
    label,folder,program,expected,volatile=job;C=W/folder
    r=subprocess.run([str(PY),'-B',str(C/program)],cwd=C,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    (A/('root_family_'+label+'.stdout')).write_bytes(r.stdout);(A/('root_family_'+label+'.stderr')).write_bytes(r.stderr)
    assert r.returncode==0 and not r.stderr,(label,r.stderr.decode())
    actual=json.loads(r.stdout)
    if expected is not None:
        wanted=(A/folder/expected).read_bytes()
        if volatile:
            compare=json.loads(wanted)
            for key in volatile:actual.pop(key);compare.pop(key)
            assert actual==compare,label
        else:assert r.stdout==wanted,label
    else:
        mf=json.loads((A/folder/'PUBLIC_EVIDENCE_MANIFEST.json').read_text())
        assert r.stdout==mf['integrity_execution']['stdout'].encode(),label
    return dict(label=label,program=folder+'/'+program,exit_code=0,stderr_empty=True,stdout_bytes=len(r.stdout),stdout_sha256=sha(r.stdout),full_stdout_byte_exact=not volatile,all_json_fields_except=list(volatile))
with ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(run,jobs))
# The moment report has variable clock fields; compare its entire mathematics.
actual=json.loads((W/'moments_review/INDEPENDENT_CONTROLS.json').read_text());wanted=json.loads((D/'INDEPENDENT_CONTROLS.json').read_text())
for key in ['started_utc','ended_utc']:actual.pop(key);wanted.pop(key)
assert actual==wanted
assert all(sha(Path(p).read_bytes())==h for p,h in before.items())
receipt=dict(status='PASS',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),workflow_percent=80,original_resolution_percent=0,manifests=members,seals=seals,original_moments_mathematical_body_unchanged=True,complete_author_historical_stream_bindings=pairs,moments_author_turn5_byte_exact=True,five_root_primary_bindings=source_bindings,programs=results,complete_moments_report_equal_except_two_utc_fields=True,all_reviewer_members_unchanged=True,stronger_extension='Universal rank restriction/greedy support/cube quotient/unique root/exact odds/occupancy/count/summability proof directly read and reconstructed; not sharp-prefix resolution or novelty')
(A/'root_family_reproduction_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
