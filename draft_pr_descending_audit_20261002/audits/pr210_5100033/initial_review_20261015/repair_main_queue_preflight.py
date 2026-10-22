"""Preserve the released workflow v3 evidence, then repair only native preflight."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil
D=Path(__file__).resolve().parent;C=D.parent;P=C/'publication';R=C/'preprint'
H=D/'history/release_helpers_review03_frozen';H.mkdir()
files=[*sorted(P.glob('*.py')),R/'FINAL_CLEARANCE.json',P/'ZENODO_VERIFIED_PUBLICATION.json',
       P/'TRACKER_VERIFIED_APPEND.json',P/'STAGE_ATTEMPT.json',P/'PUBLISH_ATTEMPT.json',
       P/'ZENODO_STAGED_VERIFIED.json',P/'ZENODO_TOOL_PUBLICATION_RECEIPT.json',
       P/'ZENODO_PROVIDER_CONFIRMED_PUBLICATION.json']
rows=[]
for p in files:
    q=H/p.name;shutil.copyfile(p,q);raw=q.read_bytes()
    rows.append(dict(path=q.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
(H/'ARCHIVE_MANIFEST.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),
    scope='Exact third-source-review helper/clearance and actual initial publication/tracker evidence; original once-only intents remain in publication unchanged',files=rows),indent=2)+'\n')
p=P/'integrate_reviewed_pr.py';source=p.read_text()
old="assert fields[8].strip() == 'claimed_solved', 'Fresh MAIN status changed: reconcile before integration'"
new="""# Eligibility is determined at the exact frozen PR head above. MAIN can still
# contain this problem's untouched queued placeholder until this PR is merged.
# Permit only that exact placeholder or the previously supported claimed state.
placeholder=original_row[0].split('|')
placeholder[8]=' queued ';placeholder[9]=' 0/5 '
for index in [10,11,12]:placeholder[index]=' '
require(fields[8].strip()=='claimed_solved' or rows[0]=='|'.join(placeholder),
        'Fresh MAIN row is neither claimed_solved nor the exact untouched queued placeholder; reconcile before integration')"""
assert source.count(old)==1
source=source.replace(old,new)
oldfamily="'release_helpers_adversary_02','release_helpers_adversary_03']"
assert source.count(oldfamily)==1
source=source.replace(oldfamily,"'release_helpers_adversary_02','release_helpers_adversary_03','release_helpers_adversary_04']")
compile(source,str(p),'exec');p.write_text(source)
receipt=dict(utc=datetime.now(timezone.utc).isoformat(),case_completion_percent=85,
    failure='Original native integration stopped at fresh MAIN queued/0-of-5 placeholder before any source copy, Git object mutation, ref intent or update.',
    eligibility='Frozen live PR210 head2180d64 remains claimed_solved/1-of-5. Fresh MAIN placeholder does not change this scoped eligibility.',
    repair='Allow only the exact untouched queued placeholder reconstructed from the original frozen target row with queued/0-of-5 and three empty release columns; preserve existing claimed_solved route. Other statuses or any changed placeholder refuse.',
    changed_helper=dict(path=p.name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()),
    original_release_archive=str(H.relative_to(D)),
    manuscript_PDF_ZIP_TeX_metadata_deposit_unchanged=True,
    actual_published_DOI='10.5281/zenodo.23398175',actual_tracker_range="'Math Puzzles'!A113:D113",
    provider_deposit_publish_append_actions_to_repeat=0,
    new_independent_supporting_review_required=True,current_old_clearance_intentionally_fails_current_helper_pin=True,
    read_only_receipt_reconciliation_required_after_new_clearance=True,
    mandatory_findings_resolved_pending_review=['Actual MAIN queued fixture was missing from prior synthetic controls'],
    unresolved_optional_findings=[])
(D/'MAIN_QUEUE_GUARD_REPAIR.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
