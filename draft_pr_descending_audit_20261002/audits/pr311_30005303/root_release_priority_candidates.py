"""Bind already fully read source-first criteria before a named candidate release."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat
A = Path(__file__).resolve().parent
sha = lambda b: hashlib.sha256(b).hexdigest()
criteria = [
    ('priority_factorization/source_only_comparison_criteria.md', 'c2a8d9d9b670144d00337d1e96b293b38700c6720c1334564faab82aca00fe0f'),
    ('priority_closure/SOURCE_ONLY_COMPARISON_CRITERIA.md', '2d64e9634cb8f05bc606257dd88f7aaef08350a78c33a6810f94c14a910161d4'),
]
bound=[]
for rel, expected in criteria:
    p=A/rel; b=p.read_bytes(); mode=stat.S_IMODE(p.stat().st_mode)
    assert sha(b)==expected and mode==0o444
    bound.append(dict(path=rel, bytes=len(b), sha256=sha(b), observed_mode=oct(mode), root_full_read_completed=True))
T='snapshot/unsolved_math_prioritization/attempts/30005303/'
common=[T+x for x in ['TURN_1.md','TURN_2.md','SOURCE_GATE.md','SOURCE_RECHECK_2.md']]
def pins(paths):
    return [dict(path=x,bytes=len((A/x).read_bytes()),sha256=sha((A/x).read_bytes())) for x in paths]
prior=A/'priority_factorization/first_independent_priority_conclusion.md'
assert sha(prior.read_bytes())=='dc669902706171eee3d9bd1dbe16351dac884b857ce00aabee9bfca974638ff8'
assert stat.S_IMODE(prior.stat().st_mode)==0o444
j=dict(actual_gate_utc=datetime.now(timezone.utc).isoformat(),status='PASS_SOURCE_CRITERIA_FULL_ROOT_READ_BEFORE_NAMED_RELEASE',criteria=bound,
       factorization_first_historical_conclusion=dict(path=str(prior.relative_to(A)),sha256=sha(prior.read_bytes()),root_full_read_completed=True,candidate_read_at_freeze=False),
       released_factorization=pins(common),released_closure=pins(common+['lattice_factorization/ALTERNATIVE_SUPPORT_CLOSURE_DERIVATION.md']),
       excluded=['all inherited reviews and controls','PUBLICATION_SUMMARY.md','all root conclusions','other-family conclusions','other candidate files until explicit later release'],
       priority_verdict='pending; no publication clearance',mathematical_completion_percent=100,workflow_completion_percent=35)
p=A/'ROOT_PRIORITY_SOURCE_GATE.json';assert not p.exists();p.write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(j,indent=2))
