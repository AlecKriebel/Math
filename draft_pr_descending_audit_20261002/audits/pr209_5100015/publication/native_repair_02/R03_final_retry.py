"""Run only the previously unrecorded frozen-six R03 regression, additively."""
from pathlib import Path
import json
import probes_joint_compact as C

HERE = Path(__file__).resolve().parent
OUT = HERE / 'R03_final_retry'
OUT.mkdir(exist_ok=False)
C.HERE = OUT
C.H.HERE = OUT
C.H.L.HERE = OUT
C.H.L.b.HERE = OUT
C.H.L.b.RUNS = OUT / 'fixtures'
C.record('R03_two_safe_advances_exactly_one_main_write', C.H.L.safe_advance_recovery)
receipt = C.H.archive_completed_group(OUT, C.H.L.b.RUNS, 'R03_retry')
print(json.dumps(dict(fixture_archive=receipt)), flush=True)
summary = dict(groups=len(C.RESULTS), all_pass=all(x['PASS'] for x in C.RESULTS),
    root_freeze_utc=C.H.FREEZE['root_freeze_utc'], case_completion_percent=65,
    no_release_authority=True, combined_with_36_complete_groups=True)
C.H.L.b.dump(OUT / 'SUMMARY.json', summary)
print(json.dumps(summary), flush=True)
raise SystemExit(0 if summary['all_pass'] else 1)
