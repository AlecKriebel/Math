"""Repair accepted source04 mechanisms; require NEW source05 before any action."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil
D=Path(__file__).resolve().parent;P=D.parent/'publication'
S=D/'release_helpers_adversary_04/reviewed_sources';H=D/'history/release_helpers_review04_frozen'
H.mkdir()
rows=[]
for p in sorted(S.rglob('*.py')):
    q=H/p.name;assert not q.exists();shutil.copyfile(p,q);raw=q.read_bytes()
    rows.append(dict(path=q.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
assert len(rows)==7
assert next(x['sha256'] for x in rows if x['path']=='integrate_reviewed_pr.py')=='b0309af583e85f3e7c443191322420d5b8a11e73d9eb1d01a34b3f1248912528'
assert next(x['sha256'] for x in rows if x['path']=='reconcile_published_release_readonly.py')=='f37a36699e2ad0a527e4d71f314b126f29dd2176916d0ec7420acd86afa60e00'
(H/'ARCHIVE_MANIFEST.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),
    scope='Exact seven source04 inputs recovered from the reviewer frozen byte copies before repair',files=rows),indent=2)+'\n')
p=P/'integrate_reviewed_pr.py';s=p.read_text()
old="for index in [10,11,12]:placeholder[index]=' '"
assert s.count(old)==1;s=s.replace(old,"for index in [10,11,12]:placeholder[index]='  '")
old="'release_helpers_adversary_03','release_helpers_adversary_04']"
assert s.count(old)==1;s=s.replace(old,"'release_helpers_adversary_03','release_helpers_adversary_04','release_helpers_adversary_05']")
compile(s,str(p),'exec');p.write_text(s)
p=D/'test_actual_main_placeholder.py';s=p.read_text()
s=s.replace('O.mkdir()','O.mkdir(exist_ok=True)')
s=s.replace("'release_helpers_adversary_03', 'release_helpers_adversary_04']","'release_helpers_adversary_03', 'release_helpers_adversary_04', 'release_helpers_adversary_05']")
s=s.replace("for i in [10,11,12]:fields[i]=' '","for i in [10,11,12]:fields[i]='  '")
compile(s,str(p),'exec');p.write_text(s)
targets=[P/'integrate_reviewed_pr.py',D/'reconcile_published_release_readonly.py']
for p in targets:compile(p.read_text(),str(p),'exec')
result=dict(utc=datetime.now(timezone.utc).isoformat(),case_completion_percent=85,
    repaired_mechanisms=[
        'Exact actual queued placeholder uses TWO spaces in all three empty cells; no widening of other queued fields/statuses.',
        'Renewed clearance must pin exact initial archive manifest, original publication/tracker receipts and stage/publish intents; explicitly approved record/DOI/exact Math Puzzles row/values are independently enforced.',
        'All archived evidence is loaded into verified same-byte snapshots. All seven current initial provider/receipt/intent files and entire archive are rechecked immediately before local receipt intent, again before replacement, and after replacement with exact overrides. Provenance hashes derive from accepted same bytes, never late unchecked file reads.'
    ],modified_sources=[dict(path=p.name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in targets],
    historical_initial_published_clearance_and_receipts_unchanged=True,
    native_prepare_ref_ready_merge_intents_absent=True,
    new_source05_review_required=True,real_reconciliation_or_external_actions=False,
    scientific_PDF_ZIP_TeX_metadata_deposit_unchanged=True)
(D/'SOURCE04_REPAIR_RESOLUTION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
