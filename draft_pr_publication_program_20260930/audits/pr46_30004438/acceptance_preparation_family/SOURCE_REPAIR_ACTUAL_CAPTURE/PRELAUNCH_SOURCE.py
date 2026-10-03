"""Own SOURCE precision repair only; proposed production remains unexecuted text."""
from pathlib import Path
import difflib, json, os
H = Path(__file__).resolve().parent
NAMES = ['pr46_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']
def main():
    assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
    archive = H/'INITIAL_GENERATED_SOURCE'; archive.mkdir()
    delta = []
    for name in NAMES:
        p = H/name; before=p.read_text(); (archive/name).write_bytes(p.read_bytes()); after=before
        replacements = [
            ('https://github.com/AlecKriebel/Math/pull/45','https://github.com/AlecKriebel/Math/pull/46'),
            ("splitlines())==19,'Original14 changed paths'","splitlines())==14,'Original14 changed paths'"),
            ('exact_original13_and_PARTIAL_unchanged','exact_original13_and_SOURCE_STATUS_unchanged'),
            ('Require35targets/43turns','Require36targets/44turns'),
            ('native35targets/43turns','native36targets/44turns'),
            ('Require33 complete primaries before44','Require35 complete primaries before46'),
            ('Exactly35 primary completions','Exactly36 primary completions'),
            ('Exactly36targets/44turns/35primary','Exactly37targets/44turns/36primary'),
            ('exact one-turn ledger budget','exact zero-turn object ledger budget'),
            ('Exact one-turn-ledger guard','Exact zero-turn-object-ledger guard'),
            ('original0/5 exact one-turn ledger, source, present raw prior and matching upstream dictionary remain unchanged.','original0/5 exact object ledger plus source-verification responses1 and plain raw source remain unchanged; prior-key absence and saved{} fallback remain distinct from null.'),
            ('actual accepted qualified scoped partial','actual accepted credited known-result source correction'),
            ("'original_substantive_attempts':0,'new_substantive_attempts'","'original_substantive_attempts':0,'original_source_verification_responses':1,'new_substantive_attempts'"),
            ("'original_substantive_attempts','new_substantive_attempts'","'original_substantive_attempts','original_source_verification_responses','new_substantive_attempts'"),
        ]
        for old,new in replacements:after=after.replace(old,new)
        if name=='state_mirror_reconciliation.py':
            after=after.replace("'cumulative_attempts':'0/5','new_substantive_attempts'", "'cumulative_attempts':'0/5','original_source_verification_responses':1,'new_substantive_attempts'")
        p.write_text(after);delta.extend(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='INITIAL_GENERATED_SOURCE/'+name,tofile=name))
    (H/'INITIAL_PRECISION_REPAIR.patch').write_text(''.join(delta))
    print(json.dumps({'status':'SOURCE_PRECISION_REPAIRED','production_executed':False,'future_acceptance_approved':False,'before_sources_preserved':len(NAMES)},sort_keys=True))
if __name__=='__main__':main()
