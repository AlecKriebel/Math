"""Preserve failed own literal-replacement authoring and repair its whitespace anchor only."""
from pathlib import Path
import os,json,datetime as dt
F=Path(__file__).absolute().parent
p=F/'author_v2.py';old=p.read_bytes();s=old.decode()
a="script.parent==A/'acceptance_preparation_family'";b="script.parent == A / 'acceptance_preparation_family'"
c="script.parent==A/'acceptance_preparation_family_v2'";d="script.parent == A / 'acceptance_preparation_family_v2'"
if s.count(a)!=1 or s.count(c)!=1:raise ValueError('Exact own author anchors')
s=s.replace(a,b,1).replace(c,d,1)
folder=F/'historical_failed_authoring';folder.mkdir()
names=['ORIGINAL_UNCLOSED_FAMILY_BINDINGS.json','SCIENTIFIC_SCOPE.json','EXPECTED_ORIGINAL_LEDGER.json','EXPECTED_CURRENT_ADMIN.json','EXPECTED_NATIVE_TRANSITION.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FINAL_PLAN.json','DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_SCOPE_CERTIFICATE.json','pr49_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py']
with (folder/'author_v2_failed.py').open('xb') as q:q.write(old)
for n in names:os.rename(F/n,folder/n)
p.write_text(s)
print(json.dumps(dict(status='PRESERVED_FAILED_84412_AND_REPAIRED_ONLY_AUTHOR_WHITESPACE_ANCHOR',actual_pid=os.getpid(),utc=dt.datetime.now(dt.timezone.utc).isoformat(),retained_partial_files=names,production_imported_compiled_executed=False)))
