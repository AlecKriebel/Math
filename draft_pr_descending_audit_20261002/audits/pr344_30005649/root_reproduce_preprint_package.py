"""One-shot independent extracted-package replay with genuine native child receipts."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,zipfile
A=Path(__file__).resolve().parent
HERE=A/'preprint'
assert len(sys.argv)==2 and sys.argv[1].isdigit()
OUT=A/'root_preprint_private'/('replay_v'+sys.argv[1])
assert not OUT.exists()
OUT.mkdir()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    data=p.read_bytes()
    return dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
inputs={name:pin(HERE/name) for name in ('qss-self-duality-note.tex','qss-self-duality-note.pdf','qss-self-duality-verification.zip','zenodo-deposit.json','build_supplement.py','verify_supplement.py')}
with zipfile.ZipFile(HERE/'qss-self-duality-verification.zip') as archive:
    names=archive.namelist()
    assert len(names)==32 and len(set(names))==32
    for row in archive.infolist():
        p=Path(row.filename)
        assert not p.is_absolute() and '..' not in p.parts
        assert p.parts[0]=='qss-self-duality-verification' and row.external_attr>>16==0o100644
    archive.extractall(OUT)
ROOT=OUT/'qss-self-duality-verification'
for p in ROOT.rglob('*'):
    if p.is_file():p.chmod(0o644)
metadata=json.loads((ROOT/'zenodo-deposit.json').read_text())
assert metadata==json.loads((HERE/'zenodo-deposit.json').read_text())
assert (ROOT/'manuscript.tex').read_bytes()==(HERE/'qss-self-duality-note.tex').read_bytes()
def inventory():return {str(p.relative_to(ROOT)):pin(p) for p in ROOT.rglob('*') if p.is_file()}
before=inventory()
for label,flags in [('integrity',[]),('full',['--full'])]:
    argv=[sys.executable,'-B',str(ROOT/'verify_supplement.py'),*flags]
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
    start=utc()
    proc=subprocess.run(argv,cwd=ROOT,env=env,capture_output=True)
    (OUT/(label+'.stdout')).write_bytes(proc.stdout)
    (OUT/(label+'.stderr')).write_bytes(proc.stderr)
    rec=dict(argv=argv,cwd=str(ROOT),started_utc=start,completed_utc=utc(),actual_exit=proc.returncode,
             environment=env,interpreter=pin(Path(sys.executable).resolve()),python_version=sys.version,
             input_pins=inputs,orchestrator=pin(Path(__file__)),
             stdout=pin(OUT/(label+'.stdout')),stderr=pin(OUT/(label+'.stderr')))
    (OUT/(label+'.native_receipt.json')).write_text(json.dumps(rec,indent=2)+'\n')
    print(label,'actual exit',proc.returncode)
    print(proc.stdout.decode())
    assert proc.returncode==0 and not proc.stderr and inventory()==before
assert {name:pin(HERE/name) for name in inputs}==inputs
result=dict(utc=utc(),status='ROOT_EXTRACTED_PUBLIC_PACKAGE_REPLAY_PASS',inputs=inputs,
            zip_members=32,extracted_payloads=31,full_streams_match=True,
            package_and_source_bytes_unchanged=True,publication_authorized_by_this_check=False)
(OUT/'SUMMARY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
