#!/usr/bin/env python3
"""Deterministically report the actual corrected-author false-count mutation."""
import json,sys
from pathlib import Path
if len(sys.argv)!=2 or sys.argv[1]!='false_count_exception_guard':raise SystemExit('exact mutation required')
source=(Path(__file__).resolve().parent/'current/check_coloured_cycles.py').read_text()
old='require(len(copies)==120,'
if source.count(old)!=1:raise RuntimeError('unique mutation site required')
source=source.replace(old,'require(len(copies)==121,')
try:
 exec(compile(source,'<corrected-author-false-count>','exec'),{'__name__':'mutated_author'})
except RuntimeError as error:
 expected='Diagnostic failed: len(copies)==120'
 if str(error)!=expected:raise
 print(json.dumps(dict(status='FAIL',optimization=sys.flags.optimize,mutation=sys.argv[1],error=expected),sort_keys=True))
 sys.exit(1)
raise RuntimeError('actual false-count mutation escaped the explicit exception')
