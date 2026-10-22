#!/usr/bin/env python3
"""Run the current source-bound exact package controls, never the old asserts."""
from pathlib import Path
import runpy,shutil,json
root=Path(__file__).resolve().parent
out=root/'verification.json'
if out.exists():out.unlink()
script=root/'publication_package/verification/verify_exact.py'
runpy.run_path(str(script),run_name='__main__')
receipt=script.with_name('verification.json')
j=json.loads(receipt.read_text())
if j.get('status')!='PASS' or j.get('exact_checks')!=19458:
    raise RuntimeError('Current package did not return the accepted exact controls')
shutil.copyfile(receipt,out)
