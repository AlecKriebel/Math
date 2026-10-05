"""Externally close the held full review without changing its namespace."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, stat, zipfile
A=Path(__file__).resolve().parent; N=A/'preprint_review_01'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def pin(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=sha(b),mode=f'{stat.S_IMODE(p.stat().st_mode):04o}')
def inventory():
    files={};dirs={'.':f'{stat.S_IMODE(N.stat().st_mode):04o}'}
    for p in sorted(N.rglob('*')):
        assert not p.is_symlink(),p
        rel=str(p.relative_to(N))
        if p.is_file():files[rel]=pin(p)
        elif p.is_dir():dirs[rel]=f'{stat.S_IMODE(p.stat().st_mode):04o}'
        else:raise AssertionError(p)
    return files,dirs
assert not (A/'ROOT_PREPRINT01_CLOSURE.json').exists()
before,dirs=inventory()
assert len(before)==905 and len(dirs)==80 and dirs['.']=='0755'
assert before['FULL_PREPRINT_REVIEW.md']['sha256']=='8ff882c7caa1de126a203c1d8a7cbcc9151d0cecfdeac8500081a348cfb8295c'
assert before['COMPLETE_INVENTORY.json']['sha256']=='3886185a6d6def086627036222f12fb105b47b2666f83cae8882d4467f285373'
m=load(N/'COMPLETE_INVENTORY.json')
assert m['status']=='COMPLETE_UNSEALED_HOLD_FOR_PARENT_EXTERNAL_AUDIT' and not m['self_sealed'] and not m['publication_clearance']
payload={x['path']:{k:x[k] for k in ['bytes','sha256','mode']} for x in m['payloads']}
assert len(payload)==m['payload_file_count']==900
exclusions=set(m['exclusions_sorted'])
assert len(exclusions)==5 and set(before)==set(payload)|exclusions
assert {k:v for k,v in before.items() if k not in exclusions}==payload
assert {k:v for k,v in dirs.items() if k!='.'}=={x['path']:x['mode'] for x in m['directory_modes']}
for name in ['ROOT_PREPRINT01_SOURCE_GATE.json','ROOT_PREPRINT01_FIRST_CANDIDATE_GATE.json']:
    gate=load(A/name)
    assert (N/'evidence/stage_integrity'/name).read_bytes()==(A/name).read_bytes()
    for row in gate['payloads']:
        p=N/row['path'];b=p.read_bytes()
        assert stat.S_IMODE(p.stat().st_mode)==row['mode_decimal']
        if row['path']=='RESEARCH_LOG.md':assert len(b)>=row['bytes'] and sha(b[:row['bytes']])==row['sha256']
        else:assert len(b)==row['bytes'] and sha(b)==row['sha256']
    for rel,mode in gate['directory_modes'].items():assert stat.S_IMODE((N/rel).stat().st_mode)==mode
pattern=r'^\| ([A-Z][0-9]{2}) \|'
ids=set(re.findall(pattern,(N/'FIRST_CANDIDATE_ASSESSMENT.md').read_text(),re.M))
assert ids==set(re.findall(pattern,(N/'FULL_PREPRINT_REVIEW.md').read_text(),re.M))==set(m['body_claim_ids']) and len(ids)==47
assert len(m['exact_release_pins'])==9
for row in m['exact_release_pins']:
    source=Path(row['source']);copy=Path(row['copy']);b=copy.read_bytes()
    assert source.read_bytes()==b and len(b)==row['bytes'] and sha(b)==row['sha256']
P=N/'evidence/candidate_full/archive';manifest=load(P/'MANIFEST.json')
assert len(manifest['files'])==50
actual={str(p.relative_to(P)):pin(p) for p in P.rglob('*') if p.is_file()}
assert actual==manifest['files']|{'MANIFEST.json':pin(P/'MANIFEST.json')}
with zipfile.ZipFile(N/'evidence/candidate_full/inputs/verification.zip') as z:
    assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==54
    assert set(z.namelist())==set(actual)|{d+'/' for d in manifest['directory_modes']}
    for info in z.infolist():
        assert stat.S_IMODE(info.external_attr>>16)==(0o755 if info.is_dir() else 0o644)
        assert z.read(info)==(b'' if info.is_dir() else (P/info.filename).read_bytes())
snapshot=load(A/'snapshot_manifest.json');prefix='unsolved_math_prioritization/attempts/20000450/'
rows=[x for x in snapshot['files'] if x['path'].startswith(prefix)];assert len(rows)==21
for row in rows:
    b=(N/'evidence/original_pr_scope'/row['path'][len(prefix):]).read_bytes()
    assert (A/'snapshot'/row['path']).read_bytes()==b and len(b)==row['bytes'] and sha(b)==row['sha256']
receipts=m['actual_native_receipts'];assert len(receipts)==89
for rec in receipts:
    assert (N/rec['stdout']).is_file() and (N/rec['stderr']).is_file()
    if 'argv_record' in rec:
        spec=load(N/rec['argv_record']);assert spec['argv'] and spec['cwd']
        txt=(N/rec['native_clock']).read_text()
        assert txt==f"START {rec['start_native_utc']}\nEND {rec['end_native_utc']}\nEXIT {rec['exit']}\n"
        assert rec['start_native_utc']<=rec['end_native_utc']
    else:
        r=load(N/rec['record'])
        if rec['kind'].startswith('geometry'):
            assert r['argv'] and r['exit']==rec['exit']
            for key in ['start_native_date','end_native_date']:assert r[key]==rec[key] and r[key]['exit']==0 and not r[key]['stderr']
        elif rec['kind'].startswith('primary'):
            assert r['argv'] and r['exit_code']==rec['exit']==0 and r['start_utc']<=r['end_utc']
            assert (N/rec['headers']).is_file()
        else:
            assert r['exit']==rec['exit']==1
            assert (N/rec['native_start']).read_text().strip()==r['start_native_utc']
            assert (N/rec['native_end']).read_text().strip()==r['end_native_utc']
            assert not (N/rec['stdout']).read_bytes() and r['expected_error'].encode() in (N/rec['stderr']).read_bytes()
        if 'stdout_bytes' in r:
            assert len((N/rec['stdout']).read_bytes())==r['stdout_bytes']
            assert len((N/rec['stderr']).read_bytes())==r['stderr_bytes']
close=N/'evidence/closing/complete_inventory_01'
assert close.with_suffix('.native-time.txt').read_text()=='START 2026-10-04T11:50:09Z\nEND 2026-10-04T11:50:09Z\nEXIT 0\n'
assert close.with_suffix('.stderr').read_bytes()==b''
closed=load(close.with_suffix('.stdout'))
assert closed['inventory_sha256']==sha((N/'COMPLETE_INVENTORY.json').read_bytes()) and closed['covered_payload_files']==900 and closed['body_claims']==47
assert sha(close.with_suffix('.stdout').read_bytes())=='71298aa7d419ab957e94240828a95d06c3a7a79df204138ef82752541881e3ac'
comparisons={
 'geometry':'geometry_family_assessed_01','pentagon':'pentagon_family_assessed_01',
 'inverse':'inverse_family_assessed_01','tate':'tate_boundary_family_assessed_01',
 'primary_arithmetic':'primary_arithmetic_01','torsion':'torsion_02'}
replays={}
for key,stem in comparisons.items():
    d=A/'root_runs_private'/('review01_'+key+'_external001');r=load(d/'execution.json')
    out=(d/'stdout.bin').read_bytes();assert r['exit_code']==0 and (d/'stderr.bin').read_bytes()==b'' and sha(out)==r['stdout_sha256']
    for p in r['programs']:
        b=Path(p['path']).read_bytes();assert len(b)==p['bytes'] and sha(b)==p['sha256']
    prior=N/'evidence/independent'/stem
    assert prior.with_suffix('.stderr').read_bytes()==b'' and 'EXIT 0\n' in prior.with_suffix('.native-time.txt').read_text()
    assert out==prior.with_suffix('.stdout').read_bytes()
    replays[key]=dict(execution=r,complete_output_equal=True)
assert load(N/'evidence/independent/package_provenance_02.stdout')['checks']==225
assert load(N/'evidence/independent/package_guards_01.stdout')['negative_controls']==6
for stem,suite,count in [('full_verify_01','all',11),('bundled_arithmetic_suite_01','arithmetic',2)]:
    rec=N/'evidence/replays'/stem;v=load(rec.with_suffix('.stdout'))
    assert 'EXIT 0\n' in rec.with_suffix('.native-time.txt').read_text() and rec.with_suffix('.stderr').read_bytes()==b''
    assert v['status']=='PASS' and v['suite']==suite and v['positive_programs']==count and v['negative_mutants']==4
    assert len(v['results'])==count+4 and all(x['complete_mathematical_output_equal'] and x['stderr_bytes']==0 for x in v['results'])
assert inventory()==(before,dirs),'Held namespace changed during external verification'
now=datetime.now(timezone.utc).isoformat()
external=dict(utc=now,status='ROOT_EXTERNALLY_BOUND_COMPLETE_HELD_PREPRINT_REVIEW01',payloads=before,directory_modes=dirs,agent_manifest=pin(N/'COMPLETE_INVENTORY.json'),early_freezes_verified=True,namespace_unchanged_during_root_verification=True)
(A/'ROOT_PREPRINT01_NAMESPACE_MANIFEST.json').write_text(json.dumps(external,indent=2)+'\n')
result=dict(utc=now,status='PASS_ROOT_EXTERNALLY_CLOSED_FULL_PREPRINT_REVIEW01_WITH_WORDING_REPAIR',agent='/root/pr329_preprint_01',qualified_candidate='v02',review_report=pin(N/'FULL_PREPRINT_REVIEW.md'),whole_namespace_files=905,whole_namespace_directories=79,actual_native_receipts_checked=89,body_claims_checked=47,root_actual_independent_replays=replays,exact_complete_outputs_equal=True,original21_unchanged=True,early31_and69_bodies_modes_and_append_only_logs_exact=True,findings=[dict(id='R01-SOURCE-ATTRIBUTION',severity='minor',required_action='Remove attribution of local conditions to Q17 remarks from manuscript and matching current priority prose; regenerate source-bound PDF/current ZIP and qualify a new candidate.')],evidence_limits=m['evidence_limits'],historical_failed_programs='No blanket historical-program-binding certificate: native receipt/stream records checked as recorded; disclosed subordinate exploratory failure has no contemporaneously saved body/UTC. Current corrected programs and six root actual replays support the proof independently.',mathematical_verification_percent=100,priority_percent=100,workflow_percent=65,preprint_ready=False,merge_ready=False,publication_ready=False,persistent_goal_complete=False)
(A/'ROOT_PREPRINT01_CLOSURE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(utc=now,status=result['status'],namespace_files=905,body_claims=47,actual_native_receipts=89,root_independent_replays=6,wording_repairs_required=1,publication_ready=False),indent=2))
