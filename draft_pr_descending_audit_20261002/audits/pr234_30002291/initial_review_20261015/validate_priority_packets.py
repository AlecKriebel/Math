"""Root integrity/replay of five completed priority packets; no provider writes."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,subprocess,sys

D=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
families=[
 ('priority_history_citations_01','SAFE_AUTHORED_MANIFEST.json'),
 ('priority_classical_coverage_01','AUTHORED_MANIFEST.json'),
 ('priority_novelty_scope_challenge_01','AUTHORED_MANIFEST.json'),
 ('priority_boundary_class_01','SAFE_ARTIFACT_MANIFEST.json'),
 ('priority_general_volterra_01','AUTHORED_MANIFEST.json'),
]

def verify_safe():
    out=[]
    for family,name in families:
        base=D/family;manifest=base/name;m=json.loads(manifest.read_text())
        rows=m.get('files',m.get('safe_authored_artifacts'))
        for row in rows:
            q=Path(row['path']);q=q if q.is_absolute() else base/q
            raw=q.read_bytes()
            assert q.resolve().is_relative_to(base.resolve()) and not q.is_symlink()
            assert len(raw)==row['bytes'] and sha(q)==row['sha256'],str(q)
            assert not any(x in q.parts for x in ['private','private_reading','private_sources','__pycache__'])
            # Whole provider challenge payloads belong in private evidence only.
            assert '__cf_chl_tk=' not in raw.decode() and '__cf_chl_rt_tk=' not in raw.decode(),str(q)
        out.append(dict(family=family,manifest_sha256=sha(manifest),verified_safe_entries=len(rows)))
    return out

def check_pin(q,row,hkey='sha256',bkey='bytes'):
    raw=q.read_bytes();assert hashlib.sha256(raw).hexdigest()==row[hkey],str(q)
    if bkey in row:assert len(raw)==row[bkey],str(q)

def evidence():
    count=0
    h=D/'priority_history_citations_01'
    for r in json.loads((h/'SOURCE_PROVENANCE.json').read_text()):
        if 'private_path' in r and 'sha256' in r:check_pin(Path(r['private_path']),r);count+=1
    c=D/'priority_classical_coverage_01'
    for r in json.loads((c/'private_sources/private_source_inventory.json').read_text())['files']:
        check_pin(c/r['path'],r);count+=1
    n=D/'priority_novelty_scope_challenge_01';m=json.loads((n/'READING_PROVENANCE.json').read_text())
    for key,name in [('original','owr-fresh.pdf'),('predecessor','lss-v2-fresh.pdf')]:
        check_pin(n/'private_reading'/name,m[key]);count+=1
    for r in m['candidate_inputs'].values():check_pin(n/r['relative_path'],r)
    b=D/'priority_boundary_class_01';m=json.loads((b/'SAFE_ARTIFACT_MANIFEST.json').read_text())
    for r in m['ignored_private_inventory_hashes_only']:check_pin(b/r['path'],r);count+=1
    g=D/'priority_general_volterra_01'
    # Match recorded scientific PDF/text identities to actual private bytes;
    # SOURCE_HASHES uses source IDs, not paths.
    identities={sha(q):q for q in (g/'private').rglob('*') if q.is_file() and q.suffix in ['.pdf','.txt']}
    for r in json.loads((g/'SOURCE_HASHES.json').read_text()):
        for key in ['pdf_sha256','text_sha256']:
            assert r[key] in identities,(r['source_id'],key);count+=1
        assert identities[r['pdf_sha256']].stat().st_size==r['pdf_bytes']
    return count

def replay(family,script,receipt,timestamp=None):
    w=D/'root_reproduction'/('priority_'+family.removeprefix('priority_'))
    w.mkdir(exist_ok=False)
    q=w/Path(script).name;shutil.copyfile(D/family/script,q)
    assert sha(q)==sha(D/family/script)
    run=subprocess.run([sys.executable,'-I','-B',str(q)],cwd=w,capture_output=True,timeout=90)
    (w/'root_stdout.txt').write_bytes(run.stdout);(w/'root_stderr.txt').write_bytes(run.stderr)
    assert run.returncode==0 and not run.stderr
    actual=json.loads((w/receipt).read_text()) if (w/receipt).exists() else json.loads(run.stdout)
    expected=json.loads((D/family/receipt).read_text())
    if timestamp:
        actual.pop(timestamp);expected.pop(timestamp)
    assert actual==expected,family
    return dict(family=family,source_sha256=sha(q),exit_code=run.returncode,
                time_independent_receipt_fields_equal=True,
                interpretation='finite scope controls, not theorem or novelty certification')

before=verify_safe();source_count=evidence()
assert json.loads((D/'ROOT_PARTIAL_PRIORITY_VALIDATION.json').read_text())['classical_exact_check_root_replay'].startswith('PASS')
replays=[replay('priority_boundary_class_01','check_scope_separators.py','SCOPE_CHECKS.json','created_utc'),
         replay('priority_general_volterra_01','scope_checks.py','SCOPE_CHECKS.json')]
after=verify_safe();assert before==after
intake=json.loads((D/'INTAKE.json').read_text())
for row in intake['original_source_files']:
    q=D/'submitted'/row['native_path'];check_pin(q,row)
out=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS_FIVE_COMPLETED_PRIORITY_PACKETS',
         manifests=after,verified_safe_entries=sum(x['verified_safe_entries'] for x in after),
         actual_private_evidence_pins_verified=source_count,
         root_replays=replays,prior_classical_replay_accepted_without_unnecessary_repeat=True,
         all_five_reports_and_all_executable_scope_checks_read=True,
         original_17_source_files_unchanged=True,
         exact_whole_candidate_novelty_or_anticipation='unresolved',
         original_request_has_substantive_prior_sufficient_answer=True,
         proposed_native_classification_or_publication_cleared=False,
         final_independent_synthesis_and_packet_review_pending=True)
(D/'ROOT_FULL_PRIORITY_PACKET_VALIDATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
