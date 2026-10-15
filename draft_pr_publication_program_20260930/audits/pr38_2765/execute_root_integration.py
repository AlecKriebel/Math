#!/usr/bin/env python3
"""Root actual execution capture for the reviewed PR38 acceptance helpers."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import subprocess
import sys

R=Path('/Users/alec/Documents/Math')
A=R/'draft_pr_publication_program_20260930/audits/pr38_2765'
S=A/'acceptance_preparation_family/integration_source_revision'
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def write_new(p,b):
    with p.open('xb') as f:f.write(b)
phase=sys.argv[1]
assert phase in ('preflight','overlay','prepush','finalize','mirror','post')
filename={'mirror':'state_mirror_reconciliation.py','post':'verify_post_acceptance.py'}.get(phase,'integrate_reviewed_partial.py')
source=S/filename
prefix='draft_pr_publication_program_20260930/audits/pr38_2765/'
argv=['/usr/bin/python3','-B',str(source)]
if phase not in ('mirror','post'):argv.append(phase)
argv+=['--execute','--preparation-manifest-sha256','7d2871247eafe91c348562caf1f30c2d76911f87d50653f36d22c6fab1ce6ad1',
    '--whole-manifest',prefix+'whole_current_alias_followup_family/FAMILY_MANIFEST.json',
    '--whole-manifest-sha256','3afb995feb3de8d62406cef0b772f0c18a6c5128543a731d8e7a29617592d37a',
    '--root-final-receipt',prefix+'final_evidence_reconciliation/ROOT_FINAL_GATE.json',
    '--root-final-receipt-sha256','c3596c64131348fe7a280ea63d10e9bbfa00f48d6bb03aecfa78d84ca81f5cba',
    '--whole-scope-contract',prefix+'final_evidence_reconciliation/WHOLE_SCOPE_CONTRACT.json',
    '--whole-scope-contract-sha256','b656c4fd940ccb8e2207f464e5dc09033b8da69a662648fddcae95590b04f065',
    '--root-final-manifest',prefix+'final_evidence_reconciliation/FINAL_MANIFEST.json',
    '--root-final-manifest-sha256','bf53f032dd89907eb4b58e12657653e370cde95279c30bee55b5dc0ae309cc92',
    '--reconciliation-capture',prefix+'root_final_reconciliation_actual_capture/CAPTURE.json',
    '--reconciliation-capture-sha256','8ca56ccddd71678c73ac343dfbb9044f1d24bab94ed5be6ceabc70dc6e3c9998']
if phase in ('preflight','overlay'):
    queue=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes()
    if phase=='preflight':
        assert sha(queue)=='87509c0d95c4323a4f35d8a098cd76cfbe2d4af5aecfb88d073806ced94d035a'
        patch=json.loads((A/'reviewed_candidate_v2/CURRENT_QUEUE_PATCH.json').read_bytes())
        assert queue.count(patch['row_before'].encode())==1
        assert subprocess.run(['git','show','HEAD:unsolved_math_prioritization/QUEUE.md'],cwd=R,check=True,stdout=subprocess.PIPE).stdout==queue
    argv+=['--'+('fresh-queue' if phase=='preflight' else 'merge-queue')+'-preimage-sha256',sha(queue)]
capture=A/('root_integration_'+phase+'_actual_capture');capture.mkdir(exist_ok=False)
raw=source.read_bytes();write_new(capture/'prelaunch_source.py',raw)
guardraw=(S/'pr38_guards.py').read_bytes();write_new(capture/'prelaunch_guards.py',guardraw)
record={'schema':'pr38-root-actual-integration-phase-capture/v1','phase':phase,'started_utc':now(),'argv':argv,
    'cwd':str(A),'source_sha256':sha(raw),'guards_sha256':sha(guardraw),'actual_execution':True}
child=subprocess.Popen(argv,cwd=A,stdout=subprocess.PIPE,stderr=subprocess.PIPE);record['pid']=child.pid
out,err=child.communicate(timeout=120)
write_new(capture/'stdout.bin',out);write_new(capture/'stderr.bin',err)
record.update(finished_utc=now(),completed=True,exit_code=child.returncode,status='PASS' if child.returncode==0 else 'FAIL',
    stdout={'path':'stdout.bin','size':len(out),'sha256':sha(out)},stderr={'path':'stderr.bin','size':len(err),'sha256':sha(err)})
write_new(capture/'CAPTURE.json',(json.dumps(record,indent=2)+'\n').encode())
print(json.dumps({'phase':phase,'status':record['status'],'pid':child.pid,'exit_code':child.returncode,
    'capture_sha256':sha((capture/'CAPTURE.json').read_bytes()),'stdout':out.decode(),'stderr':err.decode()}))
sys.exit(child.returncode)
