#!/usr/bin/env python3
"""Independent root reproduction of the frozen package's interpreter-output defect."""
from pathlib import Path
import datetime, hashlib, json, os, stat, subprocess, sys, zipfile
A=Path(__file__).resolve().parent
OUT=A/'root_preprint_private/portability_original_001'
Z=A/'preprint/qss-self-duality-verification.zip'
EXPECTED='e290f930354c82dc12c229455f25a31fb6ed3819be75c938ffdf31d4e96186b0'
INTERPRETERS=[sys.executable,'/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3']
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=stat.S_IMODE(p.stat().st_mode))
assert pin(Z)['sha256']==EXPECTED and not OUT.exists()
OUT.mkdir(parents=True)
with zipfile.ZipFile(Z) as archive:
    names=archive.namelist()
    assert len(names)==32 and len(set(names))==32
    assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names)
    archive.extractall(OUT/'extracted')
ROOT=OUT/'extracted/qss-self-duality-verification'
def inventory():return {p.relative_to(ROOT).as_posix():pin(p) for p in ROOT.rglob('*') if p.is_file()}
before=inventory()
def run(tag,argv):
    pre=dict(utc=utc(),argv=argv,cwd=str(ROOT),orchestrator=pin(Path(__file__)))
    (OUT/(tag+'.preexecution.json')).write_text(json.dumps(pre,indent=2)+'\n')
    r=subprocess.run(argv,cwd=ROOT,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0'))
    (OUT/(tag+'.stdout')).write_bytes(r.stdout);(OUT/(tag+'.stderr')).write_bytes(r.stderr)
    rec=dict(pre,completed_utc=utc(),exit_status=r.returncode,stdout=pin(OUT/(tag+'.stdout')),stderr=pin(OUT/(tag+'.stderr')))
    (OUT/(tag+'.native_receipt.json')).write_text(json.dumps(rec,indent=2)+'\n')
    assert inventory()==before and pin(Z)['sha256']==EXPECTED
    return r,rec
controls=[];receipts=[]
for i,interpreter in enumerate(INTERPRETERS):
    version,vr=run('version_'+str(i),[interpreter,'-B','-c','import sys; print(sys.executable); print(sys.version)'])
    assert version.returncode==0 and not version.stderr
    integrity,ir=run('integrity_'+str(i),[interpreter,'-B',str(ROOT/'verify_supplement.py')])
    assert integrity.returncode==0 and not integrity.stderr
    full,fr=run('full_'+str(i),[interpreter,'-B',str(ROOT/'verify_supplement.py'),'--full'])
    if i==0:assert full.returncode==0 and not full.stderr
    else:assert full.returncode==1 and b'Complete stdout mismatch: intrinsic' in full.stderr
    standalone,sr=run('intrinsic_'+str(i),[interpreter,'-B',str(ROOT/'controls/verify_intrinsic.py')])
    assert standalone.returncode==0 and not standalone.stderr
    data=json.loads(standalone.stdout);provenance=data.pop('interpreter');controls.append(data)
    receipts.append(dict(interpreter_provenance=provenance,version_receipt=vr,integrity_receipt=ir,full_receipt=fr,intrinsic_receipt=sr))
assert controls[0]==controls[1]
summary=dict(utc=utc(),status='REPRODUCED_PUBLIC_OUTPUT_PORTABILITY_BLOCKER',zip_sha256=EXPECTED,
    system_full_exit=0,bundled_full_exit=1,underlying_intrinsic_mathematical_outputs_equal=True,
    source_and_package_inventory_unchanged=True,repair='Derive public intrinsic control with interpreter provenance removed from deterministic mathematical stdout; preserve original sealed source and keep interpreter provenance in native receipts.',
    actual_native_receipts=receipts,mathematics_percent=100,priority_percent=100,publication_workflow_percent=50)
(OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='actual_native_receipts'},indent=2))
