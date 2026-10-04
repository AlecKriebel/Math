"""Freeze this agent's prospective operation report and source-only syntax checks."""
from pathlib import Path
import ast
import datetime as dt
import hashlib
import json
import os
own=Path(__file__).resolve().parent
repo=own.parents[3]
helpers=['verify_public_files.py','integrate_qualified_note.py']
checks=[]
for name in helpers:
    source=(own/name).read_bytes()
    tree=ast.parse(source,filename=str(own/name))
    compile(tree,str(own/name),'exec')
    checks.append({'path':(own/name).relative_to(repo).as_posix(),
                   'bytes':len(source),'sha256':hashlib.sha256(source).hexdigest(),
                   'AST_parse_and_compile':True,'helper_body_executed':False})
names=['REPORT.md','HELPER_INTERFACE.md','RESEARCH_LOG.md','READINESS.json',
       'GENERATED_PATH_RECOVERY.json','read_readiness.py','restore_generated_paths.py',*helpers]
pins=[]
for name in names:
    p=own/name; body=p.read_bytes()
    pins.append({'path':p.relative_to(repo).as_posix(),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
record={'schema':'pr50-qualified-operations-audit-final-pins/v1',
        'UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),
        'pins':pins,'prepared_helper_static_checks':checks,
        'full_code_review_required_by_ROOT_before_execution':True,
        'new_helper_mutation_phases_not_executed':True,'operational_audit_percent':100,
        'actual_stage_publish_tracker_merge_percent':0,'priority_or_novelty_certification_conferred':False}
with (own/'FINAL_SOURCE_PINS.json').open('x') as stream:
    json.dump(record,stream,indent=2); stream.write('\n')
print(json.dumps(record,indent=2))
