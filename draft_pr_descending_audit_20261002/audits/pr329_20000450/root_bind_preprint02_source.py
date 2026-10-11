"""Externally bind the held new source-only baseline before releasing candidate."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,stat,subprocess
A=Path(__file__).resolve().parent;N=A/'preprint_review_02'
sha=lambda b:hashlib.sha256(b).hexdigest()
def inventory():
    rows=[]
    for p in sorted([N]+list(N.rglob('*')),key=lambda p:str(p.relative_to(N))):
        assert not p.is_symlink()
        n='.' if p==N else str(p.relative_to(N))
        row=dict(path=n,type='directory' if p.is_dir() else 'file',mode_octal=f'{stat.S_IMODE(p.stat().st_mode):04o}')
        if p.is_file():
            b=p.read_bytes();row.update(bytes=len(b),sha256=sha(b))
        rows.append(row)
    return rows
rows=inventory();files=[r for r in rows if r['type']=='file'];dirs=[r for r in rows if r['type']=='directory']
assert len(files)==41 and len(dirs)==2
canonical=(json.dumps(rows,sort_keys=True,separators=(',',':'))+'\n').encode()
assert sha(canonical)=='81e32cbc9346fa3fe956afbec6bdc3d2c14fae9f6c89429bee4939abf8b5601f'
manifest=json.loads((N/'SOURCE_ONLY_FREEZE.json').read_bytes())
assert manifest['stage']=='source-only' and manifest['candidate_exposure']=='none' and not manifest['publication_approval']
assert manifest['objects_before_manifest_creation']==[r for r in rows if r['path']!='SOURCE_ONLY_FREEZE.json']
assert sha((N/'SOURCE_ONLY_BASELINE.md').read_bytes())=='c81b03d0fe28b8f16abb86df3553cb6ed53fc554c8cf7bffec347382e699475b'
assert sha((N/'SOURCE_ONLY_FREEZE.json').read_bytes())=='858dc31c2ce1f49d3e2c4dfc59d13c76c2d36cb3011954e7ecf6129a1a3c7637'
for k in ['native_file_hash_receipt','native_modes_receipt']:
    rec=manifest[k];assert rec['exit_status']==0 and rec['stderr']=='' and rec['utc_start']<=rec['utc_end']
expected=''.join(r['sha256']+'  '+r['path']+'\n' for r in files if r['path']!='SOURCE_ONLY_FREEZE.json')
assert manifest['native_file_hash_receipt']['stdout']==expected
receipts=[]
for p in sorted((N/'native_receipts').glob('*.json')):
    rec=json.loads(p.read_bytes());assert rec['state']=='completed' and rec['exit_status']==0
    assert rec['utc_start']<=rec['utc_end'] and rec['cwd']==str(N)
    assert p.with_suffix('.stderr').read_bytes()==b''
    assert rec['stdout_file']==p.with_suffix('.stdout').name
    receipts.append(dict(path=str(p.relative_to(N)),record=rec,stdout_sha256=sha(p.with_suffix('.stdout').read_bytes())))
assert len(receipts)==9
assert 'Pages:           59\n' in (N/'native_receipts/source_pdfinfo.stdout').read_text()
assert 'http_code=200\n' in (N/'native_receipts/source_download.stdout').read_text()
assert sha((N/'qptsurface2.pdf').read_bytes())=='8b64d2f6b91f791c35afae10b2ef79c15a927a94c2142a56386f80c8b8a596e6'
capture=A/'root_preprint_private/preprint02_source_external';capture.mkdir(parents=True,exist_ok=False)
native=[]
for label,argv in [('hashes',['/usr/bin/shasum','-a','256',*[r['path'] for r in files]]),
    ('modes',['/usr/bin/stat','-f','%N|%HT|%OLp|%z',*[r['path'] for r in rows]])]:
    start=datetime.now(timezone.utc).isoformat();run=subprocess.run(argv,cwd=N,capture_output=True)
    (capture/(label+'.stdout')).write_bytes(run.stdout);(capture/(label+'.stderr')).write_bytes(run.stderr)
    rec=dict(argv=argv,cwd=str(N),started_utc=start,ended_utc=datetime.now(timezone.utc).isoformat(),
        exit_code=run.returncode,stdout_sha256=sha(run.stdout),stderr_sha256=sha(run.stderr))
    assert run.returncode==0 and not run.stderr
    if label=='hashes':assert run.stdout.decode()==''.join(r['sha256']+'  '+r['path']+'\n' for r in files)
    else:
        lines=run.stdout.decode().splitlines();assert len(lines)==len(rows)
        for row,line in zip(rows,lines):
            name,kind,mode,size=line.split('|')
            assert name==row['path'] and int(mode,8)==int(row['mode_octal'],8)
            assert kind==('Directory' if row['type']=='directory' else 'Regular File')
            if row['type']=='file':assert int(size)==row['bytes']
    (capture/(label+'.json')).write_text(json.dumps(rec,indent=2)+'\n');native.append(rec)
assert inventory()==rows
gate=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS_SOURCE_ONLY_INDEPENDENCE_BASELINE_BEFORE_CANDIDATE_RELEASE',
    agent='/root/pr329_preprint_02',native_source_freeze_utc=manifest['freeze_checkpoint_utc'],objects=rows,
    canonical_inventory_sha256=sha(canonical),actual_prior_receipts=receipts,root_actual_hash_and_mode_captures=native,
    root_read_scope='Complete source-only baseline, log, source provenance, native driver and freeze code; nine actual prior receipts/complete streams; actual frontmatter and Q17/all four remarks text and pixels.',
    evidence_boundary='The agent reported an additional final self-inclusive native stdout in its tool output. Root does not claim to have read that entire historical tool output; its reported canonical digest matches these 41 unchanged file bodies and two directory modes, which are independently bound by actual root-native hash/stat captures now.',
    later_mutability='Existing baseline and source evidence immutable; log may append, new candidate evidence may be added.',
    candidate_exposure_authorized_next=True,publication_clearance=False)
out=A/'ROOT_PREPRINT02_SOURCE_GATE.json';assert not out.exists();out.write_text(json.dumps(gate,indent=2)+'\n')
print(json.dumps(dict(utc=gate['utc'],status=gate['status'],files=len(files),directories=len(dirs),canonical_inventory_sha256=sha(canonical),source_pdf_pages=59,operative_page=51,gate_sha256=sha(out.read_bytes())),indent=2))
