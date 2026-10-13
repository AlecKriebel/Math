"""Remove plain-text HTML metacharacters, rebuild and verify the exact supplement.

This is a local pre-publication repair. Preserve the original reviewed bytes
and every native command output. No API, Git, source-proof, or closed review
namespace mutation is performed.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, zipfile

A=Path(__file__).resolve().parent
P=A/'preprint'
D=P/'private/metadata_repair_001'
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.now(timezone.utc).isoformat()
load=lambda p:json.loads(p.read_bytes())
assert not D.exists()
D.mkdir(parents=True)
old=load(A/'CURRENT_PREPRINT_STATUS.json')
assert old['status']=='READY_FOR_FIRST_FRESH_PREPRINT_ADVERSARIAL_REVIEW'
for e in old['submission_files']:
    b=(P/e['path']).read_bytes()
    assert len(b)==e['bytes'] and sha(b)==e['sha256']
    (D/e['path']).write_bytes(b)
for f in [A/'CURRENT_PREPRINT_STATUS.json',P/'SUPPLEMENT_BUILD_RECEIPT.json']:
    (D/f.name).write_bytes(f.read_bytes())
before=load(P/'zenodo-deposit.json')
after=json.loads(json.dumps(before))
needle='0<A<=2/5 and 6<B<=16'
replacement='A in (0,2/5] and B in (6,16]'
assert after['metadata']['description'].count(needle)==1
after['metadata']['description']=after['metadata']['description'].replace(needle,replacement)
assert all(c not in after['metadata']['description'] for c in '<>&')
(P/'zenodo-deposit.json').write_text(json.dumps(after,indent=2)+'\n')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
captures=[]
def run(label,argv,cwd):
    start=utc();r=subprocess.run(argv,cwd=cwd,capture_output=True,env=env)
    for name,b in [('stdout',r.stdout),('stderr',r.stderr)]:
        (D/(label+'.'+name)).write_bytes(b)
    rec={'label':label,'argv':[str(x) for x in argv],'cwd':str(cwd),
         'started_utc':start,'finished_utc':utc(),'exit_code':r.returncode,
         'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),
         'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr)}
    (D/(label+'.execution.json')).write_text(json.dumps(rec,indent=2)+'\n')
    captures.append(rec)
    assert r.returncode==0 and not r.stderr,(label,rec)
    return r
run('build',['python3','-B',str(P/'build_supplement.py')],P)
Z=P/'basin-boundaries-verification.zip'
with zipfile.ZipFile(D/Z.name) as z:oldmembers={n:z.read(n) for n in z.namelist()}
with zipfile.ZipFile(Z) as z:
    members=z.infolist()
    assert len(members)==74 and len({e.filename for e in members})==74
    newmembers={e.filename:z.read(e) for e in members}
    assert oldmembers.keys()==newmembers.keys()
    changed={n for n in newmembers if oldmembers[n]!=newmembers[n]}
    assert changed=={'basin-boundaries-verification/paper/zenodo-deposit.json',
                     'basin-boundaries-verification/FILE_MANIFEST.json'}
    for e in members:
        p=Path(e.filename)
        assert not p.is_absolute() and '..' not in p.parts and p.parts[0]=='basin-boundaries-verification'
        assert not e.is_dir() and ((e.external_attr>>16)&0o170000)==0o100000
        target=D/'relocated'/p;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(newmembers[e.filename])
T=D/'relocated/basin-boundaries-verification'
assert (T/'paper/zenodo-deposit.json').read_bytes()==(P/'zenodo-deposit.json').read_bytes()
assert (T/'paper/common_basin_boundaries.tex').read_bytes()==(P/'common_basin_boundaries.tex').read_bytes()
def inventory():return {str(p.relative_to(T)):sha(p.read_bytes()) for p in T.rglob('*') if p.is_file()}
ib=inventory();results=[]
tasks=[('default',['python3','-B',str(T/'verify_supplement.py')]),
       ('full',['/opt/homebrew/bin/python3.11','-B',str(T/'verify_supplement.py'),'--full']),
       ('public_priority',['python3','-B',str(T/'audits/priority/verify_namespace.py'),'--public-only']),
       ('local_zenodo_check',['python3',str(A.parents[2]/'zenodo_deposit_tool/zenodo.py'),'check',str(P/'zenodo-deposit.json')])]
for label,args in tasks:
    r=run(label,args,T);parsed=json.loads(r.stdout)
    prior=next(x for x in old['runs'] if x['label']==label)
    if label!='local_zenodo_check':assert parsed==prior['complete_stdout']
    else:
        assert parsed['environment']=='production' and parsed['title']==after['metadata']['title']
        assert len(parsed['files'])==2
        for e in parsed['files']:
            b=(P/e['name']).read_bytes();assert (len(b),sha(b))==(e['size'],e['sha256'])
    results.append({'label':label,'native':captures[-1],'complete_stdout':parsed})
assert inventory()==ib
submission=[]
for e in old['submission_files']:
    b=(P/e['path']).read_bytes()
    submission.append({'path':e['path'],'bytes':len(b),'sha256':sha(b)})
    if e['path'].endswith(('.tex','.pdf')):assert b==(D/e['path']).read_bytes()
receipt={'utc':utc(),'status':'PASS_LOCAL_METADATA_INTERVAL_NOTATION_REPAIR',
         'old_phrase':needle,'new_phrase':replacement,
         'only_metadata_change':'description parameter notation; mathematical meaning unchanged',
         'tex_pdf_bytes_unchanged':True,'changed_zip_members':sorted(changed),
         'all_other_72_zip_members_byte_identical':True,
         'old_submission_files':old['submission_files'],'submission_files':submission,
         'relocated_package_unchanged':True,'complete_runs':results,
         'no_API_Git_or_closed_review_mutation':True,'fresh_reviewer_recheck_pending':True}
(A/'METADATA_REPAIR_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
current={**old,'utc':utc(),'submission_files':submission,'runs':results,
         'local_metadata_repair':'METADATA_REPAIR_RECEIPT.json'}
(A/'CURRENT_PREPRINT_STATUS.json').write_text(json.dumps(current,indent=2)+'\n')
with (A.parents[1]/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- '+receipt['utc']+': PR359 pre-publication metadata parameter phrase changed to equivalent interval notation to avoid HTML entity representation changes. PDF/TeX unchanged; only metadata and ZIP manifest members changed. All72 other ZIP members byte-identical; relocated default/full/priority checks reproduce complete previous results and local kit check passes. Old files and all native streams retained. First fresh reviewer notified to inspect updated package before sealing. Mathematical100%, publication workflow60%. No API or PR mutation.\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='complete_runs'},indent=2))
