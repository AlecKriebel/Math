"""Externally bind reviewer 02's held assessment before full-packet exposure."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,re,stat,subprocess,sys

A=Path(__file__).resolve().parent;N=A/'preprint_review_02';Q=A/'preprint/qualification_v03'
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.now(timezone.utc).isoformat()
assert __debug__ and sys.flags.optimize==0

def inventory():
    rows=[]
    for p in sorted([N]+list(N.rglob('*')),key=lambda p:str(p.relative_to(N))):
        assert not p.is_symlink() and (p.is_file() or p.is_dir()),p
        row=dict(path='.' if p==N else str(p.relative_to(N)),type='directory' if p.is_dir() else 'file',mode_octal=f'{stat.S_IMODE(p.stat().st_mode):04o}')
        if p.is_file():
            b=p.read_bytes();row.update(bytes=len(b),sha256=sha(b))
        rows.append(row)
    return rows

def check_native(rec,rows):
    assert rec['exit_status']==0 and rec['stderr']=='' and rec['utc_start']<=rec['utc_end']
    assert rec['cwd']==str(N)
    if rec['argv'][0]=='/usr/bin/shasum':
        files=[r for r in rows if r['type']=='file']
        assert rec['stdout']==''.join(r['sha256']+'  '+r['path']+'\n' for r in files)
        assert rec['argv']==['/usr/bin/shasum','-a','256',*[r['path'] for r in files]]
    else:
        assert rec['argv']==['/usr/bin/stat','-f','%N|%HT|%OLp|%z',*[r['path'] for r in rows]]
        lines=rec['stdout'].splitlines();assert len(lines)==len(rows)
        for row,line in zip(rows,lines):
            name,kind,mode,size=line.split('|')
            assert name==row['path'] and int(mode,8)==int(row['mode_octal'],8)
            assert kind==('Directory' if row['type']=='directory' else 'Regular File')
            if row['type']=='file':assert int(size)==row['bytes']

rows=inventory();files=[r for r in rows if r['type']=='file'];dirs=[r for r in rows if r['type']=='directory']
assert len(files)==102 and len(dirs)==4
canonical=(json.dumps(rows,sort_keys=True,separators=(',',':'))+'\n').encode()
assert sha(canonical)=='a466ff827670548d5451a52b5249830d388f53ca8caf581e1211a1332a0444f2'
assert sha((N/'FIRST_CANDIDATE_FREEZE.json').read_bytes())=='6c5de9d15e585f9469cc161533efe135401a356239c333e6a6e8457f45dfd174'
freeze=json.loads((N/'FIRST_CANDIDATE_FREEZE.json').read_bytes())
before=[r for r in rows if r['path']!='FIRST_CANDIDATE_FREEZE.json']
assert freeze['objects_before_manifest_creation']==before
assert freeze['stage']=='first-candidate-assessment' and not freeze['publication_approval']
assert freeze['candidate_exposure']==['released manuscript.tex','released manuscript.pdf','released zenodo-deposit.json']
for key in ['native_file_hash_receipt','native_modes_receipt']:check_native(freeze[key],before)
source=json.loads((A/'ROOT_PREPRINT02_SOURCE_GATE.json').read_bytes())
byname={r['path']:r for r in rows}
prefix=(N/'phase2/source_only_log_prefix.md').read_bytes()
for old in source['objects']:
    current=byname[old['path']]
    if old['path']=='RESEARCH_LOG.md':
        assert sha(prefix)==old['sha256'] and len(prefix)==old['bytes']
        assert (N/old['path']).read_bytes().startswith(prefix) and current['mode_octal']==old['mode_octal']
    else:assert current==old,(old,current)
input_pins=[]
for name in ['manuscript.tex','manuscript.pdf','zenodo-deposit.json']:
    p=N/'phase2'/name;q=Q/'inputs'/name
    assert p.read_bytes()==q.read_bytes() and stat.S_IMODE(p.stat().st_mode)==stat.S_IMODE(q.stat().st_mode)==0o644
    input_pins.append(byname['phase2/'+name])
assessment=(N/'FIRST_CANDIDATE_ASSESSMENT.md').read_bytes()
assert sha(assessment)=='eced93c50a8afc19fa454b96c8ee2e956805c81560d7940a4004f86c6395206e'
claimids=re.findall(r'^\| ([CSM]\d{3}) \|',assessment.decode(),re.M)
assert claimids==[f'C{i:03}' for i in range(1,62)]+[f'S{i:03}' for i in range(1,10)]+[f'M{i:03}' for i in range(1,5)]
receipts=[]
expected_failures={'independent_initial_exact_checks':'TypeError: argument should be a string or a Rational','initial_symbolic_dependency':"ModuleNotFoundError: No module named 'sympy'",'initial_symbolic_dependency_system':"ModuleNotFoundError: No module named 'sympy'"}
for p in sorted((N/'phase2/native_receipts').glob('*.json')):
    rec=json.loads(p.read_bytes());out=p.with_suffix('.stdout').read_bytes();err=p.with_suffix('.stderr').read_bytes()
    assert rec['state']=='completed' and rec['utc_start']<=rec['utc_end'] and rec['cwd']==str(N/'phase2')
    assert rec['stdout_file']==p.with_suffix('.stdout').name and rec['stderr_file']==p.with_suffix('.stderr').name
    if p.stem in expected_failures:assert rec['exit_status']==1 and expected_failures[p.stem] in err.decode()
    else:assert rec['exit_status']==0 and err==b''
    receipts.append(dict(path=str(p.relative_to(N)),record=rec,stdout_sha256=sha(out),stderr_sha256=sha(err)))
assert len(receipts)==13
run=A/'root_runs_private/preprint02_initial_exact_root001'
replay=json.loads((run/'execution.json').read_bytes())
assert replay['exit_code']==0 and (run/'stderr.bin').read_bytes()==b''
assert (run/'stdout.bin').read_bytes()==(N/'phase2/native_receipts/independent_initial_exact_checks_v02.stdout').read_bytes()
assert replay['programs'][0]['sha256']==byname['phase2/independent_initial_exact_checks.py']['sha256']
capture=A/'root_preprint_private/preprint02_first_candidate_external';capture.mkdir(parents=True,exist_ok=False)
native=[]
for label,argv in [('hashes',['/usr/bin/shasum','-a','256',*[r['path'] for r in files]]),('modes',['/usr/bin/stat','-f','%N|%HT|%OLp|%z',*[r['path'] for r in rows]])]:
    start=utc();run=subprocess.run(argv,cwd=N,capture_output=True)
    (capture/(label+'.stdout')).write_bytes(run.stdout);(capture/(label+'.stderr')).write_bytes(run.stderr)
    rec=dict(argv=argv,cwd=str(N),utc_start=start,utc_end=utc(),exit_status=run.returncode,stdout=run.stdout.decode(),stderr=run.stderr.decode())
    check_native(rec,rows)
    (capture/(label+'.json')).write_text(json.dumps(rec,indent=2)+'\n')
    native.append(dict(path=str((capture/(label+'.json')).relative_to(A)),sha256=sha((capture/(label+'.json')).read_bytes()),record=rec))
assert inventory()==rows
gate=dict(utc=utc(),status='PASS_INDEPENDENT_FIRST_CANDIDATE_ASSESSMENT_EXTERNALLY_BOUND_BEFORE_FULL_PACKET_RELEASE',agent='/root/pr329_preprint_02',
    native_assessment_freeze_utc=freeze['freeze_checkpoint_utc'],objects=rows,canonical_inventory_sha256=sha(canonical),
    candidate_inputs=input_pins,source_only_gate_sha256=sha((A/'ROOT_PREPRINT02_SOURCE_GATE.json').read_bytes()),source_only_41_files_preserved=True,source_log_append_only=True,
    stable_claim_ids=claimids,actual_phase2_receipts=receipts,root_independent_exact_replay=replay,root_actual_hash_and_mode_captures=native,
    root_read_scope='Entire 31381-byte assessment, 74-ID ledger, corrected exact checker and complete failed-to-corrected diff, native receipt driver and freezer, source-preservation program/results, append-only log, all thirteen actual phase2 receipts and complete streams. The previous source-only read and candidate/root PDF QA remain separately bound.',
    historical_evidence_boundary='Root has not read the entire additional self-inclusive final native tool stdout that the reviewer saved in its own tool store. Its reported canonical digest agrees with all 102 unchanged files and four directories now externally captured by root native SHA/stat. The stored first-candidate manifest contains complete pre-manifest native receipts. Phase2 execution records were made contemporaneously, but do not pin historical script bodies; the retained failed body and explicit correction diff are inspected as evidence without claiming blanket historical execution attestation.',
    root_current_runtime=dict(python=sys.version,optimize=sys.flags.optimize,PYTHONOPTIMIZE=os.environ.get('PYTHONOPTIMIZE')),
    later_mutability='All early source and assessment bodies immutable; RESEARCH_LOG.md may append; new full-review evidence may be added.',
    mathematical_verdict='Initial exact identities pass; central normalization/kernel/all-specialization/source/package obligations remain open in the independent ledger. This gate certifies exposure chronology and retained evidence, not a clean mathematical verdict.',
    full_packet_release_authorized_next=True,publication_clearance=False)
out=A/'ROOT_PREPRINT02_FIRST_CANDIDATE_GATE.json';assert not out.exists();out.write_text(json.dumps(gate,indent=2)+'\n')
print(json.dumps(dict(utc=gate['utc'],status=gate['status'],files=len(files),directories=len(dirs),claims=len(claimids),prior_phase2_receipts=len(receipts),root_exact_replay_output_equal=True,canonical_inventory_sha256=sha(canonical),gate_sha256=sha(out.read_bytes()),publication_clearance=False),indent=2))
