"""Externally bind a held priority namespace and actual independent replays."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat
A=Path(__file__).resolve().parent;N=A/'priority_audit';S=N/'stage3_current_priority'
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p,base=None):
    assert p.is_file() and not p.is_symlink()
    b=p.read_bytes();return dict(path=str(p.relative_to(base)) if base else str(p),bytes=len(b),sha256=sha(b),mode_decimal=stat.S_IMODE(p.stat().st_mode))
def inventory():
    files=[];dirs={}
    for p in sorted(N.rglob('*')):
        assert not p.is_symlink(),str(p)
        if p.is_file():files.append(pin(p,N))
        elif p.is_dir():dirs[str(p.relative_to(N))]=stat.S_IMODE(p.stat().st_mode)
    return dict(payloads=files,directory_modes=dirs,root_mode_decimal=stat.S_IMODE(N.stat().st_mode))
before=inventory();assert len(before['payloads'])==809
expected={'priority_final_comparison_system001':(1197,25),'priority_final_comparison_bundled001':(1197,25),'priority_final_public001':(335,25),'priority_final_whole001':(553,25)}
replays={}
for name,(size,count) in expected.items():
    D=A/'root_runs_private'/name;r=json.loads((D/'execution.json').read_bytes())
    assert r['exit_code']==0 and r['stderr_bytes']==0 and (D/'stderr.bin').read_bytes()==b''
    out=(D/'stdout.bin').read_bytes();assert len(out)==size==r['stdout_bytes'] and sha(out)==r['stdout_sha256']
    for program in r['programs']:
        p=Path(program['path']);assert p.is_relative_to(S)
        assert p.stat().st_size==program['bytes'] and sha(p.read_bytes())==program['sha256']
    value=json.loads(out);assert value['result']=='PASS' and value['exact_comparisons']==count
    replays[name]=dict(receipt=pin(D/'execution.json',A),complete_result=value)
assert replays['priority_final_comparison_system001']['complete_result']==replays['priority_final_comparison_bundled001']['complete_result']
whole=replays['priority_final_whole001']['complete_result']
assert whole['namespace_payloads']==805 and whole['external_pins']==25 and whole['native_receipts_checked']==167
assert whole['whole_manifest_sha256']==sha((S/'WHOLE_NAMESPACE_MANIFEST.json').read_bytes())
original=S/'private_evidence/final_whole_replay001'
r=json.loads((original/'receipt.json').read_bytes());assert r['actual_exit_code']==0
for channel in ['stdout','stderr']:
    b=(original/channel).read_bytes();assert len(b)==r[channel+'_bytes'] and sha(b)==r[channel+'_sha256']
assert (original/'stderr').read_bytes()==b'' and json.loads((original/'stdout').read_bytes())==whole
sources=json.loads((S/'SOURCE_INVENTORY.json').read_bytes())['sources']
reading=json.loads((S/'READING_LEDGER.json').read_bytes())['entries']
assert len(sources)==len(reading)==50
for source,read in zip(sources,reading):
    assert read=={k:source.get(k) for k in ['id','source_sha256','actual_pdf_page_count','read_scope','operative_role_or_limit']}
    if source['id']=='original_aim_pdf_source_stage':
        p=N/'private_source_evidence/official_current.retrieval_receipt.json'
        r=json.loads(p.read_bytes());assert source['retrieval_started_utc']==r['started_utc'] and source['retrieval_finished_utc']==r['finished_utc'] and source['actual_native_exit_code']==r['exit_code']==0
    else:
        D=S/'private_evidence'/source['id'];r=json.loads((D/'retrieval.receipt.json').read_bytes())
        su=json.loads((D/'SUMMARY.json').read_bytes())
        assert source['canonical_url']==su['url'] and source['actual_http_status_from_curl']==su['http_status']
        assert source['retrieval_started_utc']==r['started_utc'] and source['retrieval_finished_utc']==r['finished_utc'] and source['actual_native_exit_code']==r['actual_exit_code']
        p=D/'source.bytes';b=p.read_bytes() if p.exists() else None
        assert source['source_sha256']==(sha(b) if b is not None else None) and source['retrieved_source_bytes']==(len(b) if b is not None else None)
manifest=json.loads((S/'WHOLE_NAMESPACE_MANIFEST.json').read_bytes())
for row in manifest['external_pins']:
    assert pin(Path(row['path']))=={k:row[k] for k in ['path','bytes','sha256','mode_decimal']}
assert inventory()==before
utc=datetime.now(timezone.utc).isoformat()
external=dict(utc=utc,namespace='priority_audit',**before,external_pins=manifest['external_pins'],held_namespace_unchanged=True)
p=A/'ROOT_PRIORITY_NAMESPACE_MANIFEST.json';assert not p.exists();p.write_text(json.dumps(external,indent=2)+'\n')
j=dict(utc=utc,status='PASS_ROOT_EXTERNALLY_CLOSED_PRIORITY_AUDIT_PR329',namespace_manifest=pin(p,A),
    independent_report=pin(S/'PRIORITY_REPORT.md',A),public_manifest=pin(S/'PUBLIC_MANIFEST.json',A),
    actual_root_replays=replays,source_ledger_rows=50,exact_formula_comparisons=25,
    historical_scope='Prior Tate/modular inputs, universal division table/radical and every-specialization field criterion credited. No earlier exact complete pencil answer found in the inspected corpus; no firstness or continuing-openness certificate.',
    root_reading_scope='Full final reports, chronology, gaps, public instructions and critical verifier/ledger/capture code; all 50 source/read scopes and 35 web query texts/25 native endpoint scopes. Decisive original primary pages independently read as recorded in ROOT priority report.',
    priority_percent=100,mathematical_verification_percent=100,workflow_percent=55,
    preprint_ready=False,merge_ready=False,publication_ready=False,persistent_goal_complete=False)
p=A/'ROOT_PRIORITY_CLOSURE.json';assert not p.exists();p.write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(dict(utc=utc,status=j['status'],namespace_files=len(before['payloads']),source_rows=50,comparisons=25,priority_percent=100,workflow_percent=55),indent=2))
