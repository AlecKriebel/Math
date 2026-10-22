#!/usr/bin/env python3
"""Authenticate original harness and source, then execute only independent own copies."""
import argparse, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent
SHARED=HERE.parents[1]
SOURCE_NAME='resweep_draft_statuses_900_1000.py'
SUITE_NAME='test_final_status_sweep.py'
SOURCE_PIN='fc8ef5d6493c0088d94441e3a1876b9dc99bbaef84a98320647b84d15d5d048e'
SUITE_PIN='ca6e25bd7521c8a9be14259c7bcd6cc8818e5a6f6115a1e1f8bce202263b7510'
def pinned(path,digest):
 raw=path.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=digest:raise RuntimeError('External whole-file pin mismatch BEFORE compilation: '+str(path))
 return raw
source=pinned(SHARED/SOURCE_NAME,SOURCE_PIN)
initial=pinned(SHARED/SUITE_NAME,SUITE_PIN)
if pinned(HERE/SOURCE_NAME,SOURCE_PIN)!=source:raise RuntimeError('Backing source differs')
if pinned(HERE/SUITE_NAME,SUITE_PIN)!=initial:raise RuntimeError('Backing initial suite differs')
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
out=HERE/args.output
if out.parent!=HERE or out.exists():raise RuntimeError('New own output directory required')
out.mkdir()
old=b'Frozen PR948 candidate unchanged.'
new=b'No actual PR source/artifact was read; synthetic fixtures only.'
if initial.count(old)!=1:raise RuntimeError('Exact documentation-only adapter precondition')
adapted=initial.replace(old,new)
(out/SOURCE_NAME).write_bytes(source)
(out/SUITE_NAME).write_bytes(adapted)
if hashlib.sha256((out/SOURCE_NAME).read_bytes()).hexdigest()!=SOURCE_PIN:raise RuntimeError('Source copy pin mismatch BEFORE compilation')
adapter={'utc':datetime.now(timezone.utc).isoformat(),'actual_python_optimization_level':sys.flags.optimize,'source_sha256':SOURCE_PIN,'initial_suite_sha256':SUITE_PIN,'adapted_suite_sha256':hashlib.sha256(adapted).hexdigest(),'exact_adapter':{'old_utf8':old.decode(),'new_utf8':new.decode(),'occurrences':1,'purpose':'Remove historical candidate assertion from emitted scope description only; no test logic changed'},'binding':'__file__ points to this own copied suite; its SOURCE and P therefore resolve solely within its own output directory','source_and_initial_harness_authenticated_before_compile':True,'actual_live_service_calls':0}
(out/'ADAPTER.json').write_text(json.dumps(adapter,indent=2)+'\n')
namespace={'__file__':str(out/SUITE_NAME),'__name__':'__main__'}
exec(compile(adapted,str(out/SUITE_NAME),'exec'),namespace)
receipt=json.loads((out/'FINAL_STATUS_SWEEP_OFFLINE_CONTROLS_20261016_03.json').read_bytes())
if receipt.get('passed')!=49 or receipt.get('failed')!=0 or receipt.get('source_sha256')!=SOURCE_PIN or receipt.get('live_service_calls')!=0:raise RuntimeError('Expected 49 meaningful existing controls')
