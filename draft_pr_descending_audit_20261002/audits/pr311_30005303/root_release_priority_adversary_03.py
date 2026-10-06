"""Record the completed root body reads before releasing named proof inputs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat
A = Path(__file__).resolve().parent
sha = lambda b: hashlib.sha256(b).hexdigest()
frozen = {
 'source_only_criteria.md': '5e986af08048e9bc8c9e052b2d8666c468fd000c0b3a657133c26f9d5eee04af',
 'first_independent_historical_conclusion.md': 'f2218f1f3e4f55b382cccd96973bcbb8ee81e958ac90e615591b6193da581e4a',
 'independent_boundary_bridge.md': 'a60b708fa9a4481c44670d177e516bc6d49bbb207644ebe59fabe2689d7816a8',
}
read = []
for name, expected in frozen.items():
 p = A/'closure_priority_adversary/public'/name
 b = p.read_bytes(); mode = stat.S_IMODE(p.stat().st_mode)
 assert sha(b) == expected and mode == 0o444
 read.append(dict(path=str(p), bytes=len(b), sha256=sha(b), measured_mode=oct(mode), root_full_body_read_completed=True))
T = A/'snapshot/unsolved_math_prioritization/attempts/30005303'
files = [T/x for x in ['TURN_1.md', 'TURN_2.md', 'SOURCE_GATE.md', 'SOURCE_RECHECK_2.md']]
files.append(A/'lattice_factorization/ALTERNATIVE_SUPPORT_CLOSURE_DERIVATION.md')
pins = []
for p in files:
 b = p.read_bytes()
 pins.append(dict(path=str(p), bytes=len(b), sha256=sha(b), measured_mode=oct(stat.S_IMODE(p.stat().st_mode))))
j = dict(actual_gate_utc=datetime.now(timezone.utc).isoformat(), status='PASS_SOURCE_FIRST_FULL_ROOT_READ_BEFORE_NAMED_RELEASE',
 frozen_independent_inputs=read, release=pins,
 exclusions=['root conclusions', 'sibling priority derivations and reports', 'inherited reviews', 'PUBLICATION_SUMMARY', 'all other candidate files and code'],
 remaining_work='Independent post-release mathematical/priority comparison; no publication clearance.', mathematical_completion_percent=100, priority_audit_percent=65, workflow_completion_percent=40)
out = A/'ROOT_PRIORITY_ADVERSARY_GATE_03.json'
assert not out.exists()
out.write_text(json.dumps(j, indent=2)+'\n')
print(json.dumps(j, indent=2))
