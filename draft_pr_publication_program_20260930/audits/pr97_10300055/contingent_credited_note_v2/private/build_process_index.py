"""Index actual process receipts; controlled linked sentinels are not JSON journals."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
base = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(base/'publicfiles/support'))
from safe_output import write_new, json_bytes

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
index = []
def add(path,scope):
    content = json.loads(path.read_text())
    values = content if isinstance(content,list) else [content]
    for i,r in enumerate(values):
        if 'pid' not in r:
            continue
        row = dict(scope=scope,receipt_path=path.relative_to(base).as_posix(),
                   receipt_sha256=sha(path),record_index=i)
        for k in ['label','family','mode','optimized','command','cwd','pid','started_utc',
                  'finished_utc','wall_seconds','exit_code','expected_exit_code','expected_reason',
                  'accepted','stdout_sha256','stderr_sha256','input_script_sha256','script_sha256',
                  'input_source_hashes','candidate_sha256','rejection_reason','parse_error']:
            if k in r:
                row[k] = r[k]
        index.append(row)
for p in sorted((base/'private/actual_runs').glob('*.json')):
    add(p,'preparation subprocess')
add(base/'private/diagnostics_current/PROCESS_RECEIPTS.json',
    'unchanged mathematical diagnostics and explicit false-check guards')
add(base/'private/custody_current/PROCESS_RECEIPTS.json','synthetic wrapper/utility controls')
for label in ['author_malformed_zero','author_nonzero','author_wrong_structure',
              'independent_malformed_zero']:
    for mode in ['normal','O']:
        add(base/('private/custody_current/'+label+'_'+mode+'/results/PROCESS_RECEIPTS.json'),
            'synthetic failed-child custody only')
add(base/'private/integrity_current/PROCESS_RECEIPTS.json','payload/ZIP path integrity only')
add(base/'private/actual_reuse_controls/PROCESS_RECEIPTS.json',
    'actual successful output reuse rejection; no mathematical runs')
if len(index) != 111:
    raise ValueError('Unexpected number of pre-aggregation actual process records')
value = dict(schema='pr97-v2-actual-process-index/v1',
             utc=dt.datetime.now(dt.timezone.utc).isoformat(),process_records=len(index),records=index,
             scope='Actual argv/PID/UTC/exit/stream hashes; synthetic roles separated; no fabricated IDs.',
             this_aggregation_process_receipt='private/actual_runs/process_index.json',
             inline_preparation_failure_limitations='private/PROCESS_INDEX_AGGREGATION_FAILURE.json')
write_new(base/'PROCESS_INDEX.json',json_bytes(value))
print(json.dumps(dict(status='PASS',process_records=len(index),index_sha256=sha(base/'PROCESS_INDEX.json')),
                 indent=2))
