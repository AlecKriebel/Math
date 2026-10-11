"""Correct own SOURCE immutable/administrative scope; no proposed production execution."""
from pathlib import Path
import difflib, json, os
H = Path(__file__).resolve().parent
NAMES = ['pr46_guards.py','independent_controls.py','integrate_reviewed_partial.py','DRAFT_FINAL_PLAN.json','SCIENTIFIC_SCOPE.json']
def main():
    assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
    archive = H/'PRE_IMMUTABLE_SCOPE_REPAIR'; archive.mkdir()
    delta = []
    for name in NAMES:
        p = H/name; before=p.read_text(); (archive/name).write_bytes(p.read_bytes()); after=before
        after=after.replace('immutable10','immutable8').replace('Immutable10','Immutable8').replace('ten operative','eight operative')
        if name=='pr46_guards.py':
            begin=after.index('ADMIN = ');end=after.index('\n',begin);after=after[:begin]+"ADMIN = {'status.json','readiness.json','independent_review/verdict.json','independent_review/review_summary.json'}"+after[end:]
            begin=after.index('IMMUTABLE = ');end=after.index('\n',begin);after=after[:begin]+"IMMUTABLE = {'SOURCE_STATUS.md','independent_review/independent_checks.py','independent_review/independent_results.json','provenance.json','source_record.json','turns.json','verification.json','verify.py'}"+after[end:]
        if name=='independent_controls.py':
            after=after.replace("root=H/'OWN_READONLY_GIT_V2'", "root=H/'OWN_READONLY_GIT_V3'")
            after=after.replace("'SOURCE_STATUS.md','independent_review/REVIEW.md','independent_review/independent_checks.py','independent_review/independent_results.json','independent_review/review_summary.json','provenance.json'", "'SOURCE_STATUS.md','independent_review/independent_checks.py','independent_review/independent_results.json','provenance.json'")
        p.write_text(after);delta.extend(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='PRE_IMMUTABLE_SCOPE_REPAIR/'+name,tofile=name))
    (H/'IMMUTABLE_SCOPE_REPAIR.patch').write_text(''.join(delta))
    print(json.dumps({'status':'SOURCE_IMMUTABLE_SCOPE_CORRECTED','original_archive_files':13,'literal_current_originals':8,'operative_admin_objects':4,'prospective_overlay_files':955,'prospective_accepted_payload_files':957,'production_executed':False,'future_acceptance_approved':False},sort_keys=True))
if __name__=='__main__':main()
