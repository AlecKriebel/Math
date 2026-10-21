"""One exact-candidate prior R03 control; no source or state rewrites."""
from pathlib import Path
import contextlib, io, json
import receipt_controls as T

HERE = Path(__file__).resolve().parent
T.H.L.b.RUNS = HERE / 'R03_runs_01'
T.check('R03_two_safe_advances_one_main_write', T.H.L.safe_advance_recovery)
archive = T.H.archive_completed_group(HERE, T.H.L.b.RUNS, 'R03_01')
summary = dict(controls=len(T.RESULTS), all_pass=all(r['PASS'] for r in T.RESULTS),
    fixture_archive=archive, case_completion_percent=65, release_authority=False)
print(json.dumps(summary), flush=True)
T.dump(HERE / 'R03_SUMMARY_01.json', summary)
raise SystemExit(0 if summary['all_pass'] else 1)
