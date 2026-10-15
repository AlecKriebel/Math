"""Independent finite permission predicates; no builder import/compile/execution."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import stat

P = Path(__file__).resolve().parent
work = P / 'private_mode_controls'
work.mkdir(exist_ok=False)
result = []
for mode in [0o4444, 0o2444, 0o1444, 0o444]:
    path = work / ('mode_' + format(mode, '05o'))
    path.write_bytes(b'Own finite permission control; never a candidate artifact.\n')
    path.chmod(mode)
    actual = path.stat().st_mode
    full = stat.S_IMODE(actual)
    assert full == mode
    old_accepts = actual & 0o777 == 0o444
    repaired_accepts = stat.S_IMODE(actual) == 0o444
    assert old_accepts is True
    assert repaired_accepts is (mode == 0o444)
    raw = path.read_bytes()
    result.append(dict(path=path.relative_to(P).as_posix(), requested_permission=oct(mode),
                       observed_st_mode=oct(actual), observed_full_permission=oct(full),
                       old_predicate_accepts=old_accepts, full_permission_predicate_accepts=repaired_accepts,
                       bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
receipt = dict(schema='PR42_OWN_ACTUAL_FINITE_PERMISSION_CONTROLS_v1', utc=dt.datetime.now(dt.timezone.utc).isoformat(),
               cases=result, wrong_mode_cases_rejected=3, ordinary_0444_accepted=True,
               builder_imported_executed_compiled=False, candidate_created=False,
               full_problem_solved=False, future_whole_current_verdict=None,
               original_substantive_attempts=2, new_substantive_attempts=0, audit_turns=0)
(P / 'PERMISSION_CONTROL_RESULTS.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
