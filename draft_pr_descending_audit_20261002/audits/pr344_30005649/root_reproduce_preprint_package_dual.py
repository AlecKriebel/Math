#!/usr/bin/env python3
"""Fresh extracted-package replay on two runtimes, with exact derivative checks."""
from pathlib import Path
import datetime,hashlib,json,os,stat,subprocess,sys,zipfile
A=Path(__file__).resolve().parent;HERE=A/'preprint'
assert len(sys.argv)==2 and sys.argv[1].isdigit()
OUT=A/'root_preprint_private'/('dual_replay_v'+sys.argv[1])
assert not OUT.exists();OUT.mkdir()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=stat.S_IMODE(p.stat().st_mode))
def files(root):
    result={}
    for p in root.rglob('*'):
        assert not p.is_symlink()
        if p.is_file():result[p.relative_to(root).as_posix()]=pin(p)
    return result
closed_names=['honda_lifting','intrinsic_invariants','semilinear_modules',
              'priority_supersingular_mechanism','priority_audit','preprint_review_01']
closed={name:files(A/name) for name in closed_names}
math=json.loads((A/'ROOT_MATHEMATICAL_ACCEPTANCE.json').read_bytes())
for family in ('honda_lifting','intrinsic_invariants','semilinear_modules'):
    assert closed[family]==math['families'][family]['whole_current_namespace']
review=json.loads((A/'ROOT_PREPRINT_REVIEW01_SEAL.json').read_bytes())
assert review['status']=='HISTORICAL_ADVERSE_REVIEW_CLOSED_REPAIR_REQUIRED'
assert closed['preprint_review_01']=={name:dict(row,mode=int(row['mode'],8)) for name,row in review['namespace_inventory']['files'].items()}
input_names=('qss-self-duality-note.tex','qss-self-duality-note.pdf','qss-self-duality-verification.zip',
             'zenodo-deposit.json','build_supplement.py','verify_supplement.py')
inputs={name:pin(HERE/name) for name in input_names}
with zipfile.ZipFile(HERE/'qss-self-duality-verification.zip') as archive:
    names=archive.namelist();assert len(names)==32 and len(set(names))==32
    for row in archive.infolist():
        p=Path(row.filename);assert not p.is_absolute() and '..' not in p.parts
        assert p.parts[0]=='qss-self-duality-verification' and row.external_attr>>16==0o100644
    archive.extractall(OUT/'extracted')
ROOT=OUT/'extracted/qss-self-duality-verification'
for p in ROOT.rglob('*'):
    if p.is_file():p.chmod(0o644)
assert (ROOT/'manuscript.tex').read_bytes()==(HERE/'qss-self-duality-note.tex').read_bytes()
assert (ROOT/'zenodo-deposit.json').read_bytes()==(HERE/'zenodo-deposit.json').read_bytes()
assert (ROOT/'verify_supplement.py').read_bytes()==(HERE/'verify_supplement.py').read_bytes()
identity=json.loads((ROOT/'SOURCE_IDENTITY.json').read_bytes())
origins={'controls/check_realization.py':A/'honda_lifting/check_realization.py',
         'controls/verify_semilinear.py':A/'semilinear_modules/verify_semilinear.py',
         'controls/verify_intrinsic.py':A/'intrinsic_invariants/public/verify_intrinsic.py',
         'controls/construction.json':A/'intrinsic_invariants/public/construction.json',
         'controls/check_integral_flag.py':A/'priority_supersingular_mechanism/check_integral_flag.py'}
for name,p in origins.items():
    original=p.read_bytes();bound=identity['reviewed_original_control_pins'][name]
    assert bound=={k:pin(p)[k] for k in ('bytes','sha256')}
    if name in identity['control_derivations']:
        derivation=identity['control_derivations'][name];text=original.decode()
        assert derivation['reviewed_original']==bound
        for edit in derivation['edits']:
            assert text.count(edit['literal_old'])==edit['occurrences']
            text=text.replace(edit['literal_old'],edit['literal_new'])
        assert text.encode()==(ROOT/name).read_bytes()
        assert derivation['public_derivative']==identity['control_source_pins'][name]
    else:assert original==(ROOT/name).read_bytes()
before=files(ROOT);outputs={};receipts=[]
interpreters=[sys.executable,'/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3']
for i,interpreter in enumerate(interpreters):
    for label,flags in [('integrity',[]),('full',['--full'])]:
        tag=str(i)+'_'+label;argv=[interpreter,'-B',str(ROOT/'verify_supplement.py'),*flags]
        pre=dict(utc=utc(),argv=argv,cwd=str(ROOT),orchestrator=pin(Path(__file__)),input_pins=inputs,
                 interpreter=pin(Path(interpreter).resolve()),environment_overrides={'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'})
        (OUT/(tag+'.preexecution.json')).write_text(json.dumps(pre,indent=2)+'\n')
        r=subprocess.run(argv,cwd=ROOT,capture_output=True,env=dict(os.environ,**pre['environment_overrides']))
        (OUT/(tag+'.stdout')).write_bytes(r.stdout);(OUT/(tag+'.stderr')).write_bytes(r.stderr)
        rec=dict(pre,completed_utc=utc(),exit_status=r.returncode,stdout=pin(OUT/(tag+'.stdout')),stderr=pin(OUT/(tag+'.stderr')))
        (OUT/(tag+'.native_receipt.json')).write_text(json.dumps(rec,indent=2)+'\n');receipts.append(rec)
        assert r.returncode==0 and not r.stderr and files(ROOT)==before
        v=json.loads(r.stdout);assert v['status']=='PASS' and v['package_bytes_inventory_unchanged']
        assert v['payload_files']==31 and len(v['runs'])==(5 if label=='full' else 1)
        outputs[(i,label)]=r.stdout
assert outputs[(0,'integrity')]==outputs[(1,'integrity')] and outputs[(0,'full')]==outputs[(1,'full')]
assert {name:pin(HERE/name) for name in input_names}==inputs
assert {name:files(A/name) for name in closed_names}==closed
summary=dict(utc=utc(),status='ROOT_TWO_RUNTIME_EXTRACTED_PACKAGE_REPLAY_PASS',inputs=inputs,
    zip_members=32,payload_files=31,complete_output_bytes_equal_between_runtimes=True,
    exact_public_derivations_verified=True,all_original_closed_namespaces_unchanged={k:len(v) for k,v in closed.items()},
    actual_native_receipts=receipts,publication_authorized_by_this_check=False,
    math_percent=100,priority_percent=100,publication_workflow_percent=60)
(OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='actual_native_receipts'},indent=2))
