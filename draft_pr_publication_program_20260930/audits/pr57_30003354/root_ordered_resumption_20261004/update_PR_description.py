"""Submit the reviewed description after actual publication, tracker and merge."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess

F=Path(__file__).resolve().parent; A=F.parent; R=A.parents[2]; O=A/'ordered_publication_operations_20261004'
def sha(b): return hashlib.sha256(b).hexdigest()
pub=json.loads((F/'PUBLICATION_VERIFICATION.json').read_bytes()); tracker=json.loads((F/'TRACKER_VERIFICATION.json').read_bytes()); native=json.loads((O/'NATIVE_ACCEPTANCE_RESULT.json').read_bytes())
assert pub['published'] and tracker['independent_readback_exact'] and native['DOI']==pub['DOI']
title=(O/'PR_TITLE.txt').read_text().strip()
body=(O/'PR_BODY_TEMPLATE.md').read_text().split('\n\n',1)[1]
body=body.replace('<ACTUAL_PUBLISHED_DOI>',pub['DOI']).replace('<ACTUAL_PUBLISHED_RECORD_URL>',pub['record_url']).replace('<ACTUAL_PUBLICATION_AND_TRACKER_EVIDENCE_PATHS>','`'+str((F/'PUBLICATION_VERIFICATION.json').relative_to(R))+'` and `'+str((F/'TRACKER_VERIFICATION.json').relative_to(R))+'` (spreadsheet range '+tracker['range']+')')
assert '<ACTUAL_' not in body
(F/'PREPARED_PR_BODY.md').write_text(body)
commands=[]
def run(name,argv):
    start=dt.datetime.now(dt.timezone.utc).isoformat(); child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE); out,err=child.communicate(timeout=60)
    (F/(name+'.stdout')).write_bytes(out); (F/(name+'.stderr')).write_bytes(err)
    commands.append({'argv':argv,'actual_pid':child.pid,'started_UTC':start,'finished_UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':child.returncode,'stdout_sha256':sha(out),'stderr_sha256':sha(err)})
    (F/'PR_METADATA_COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n'); assert child.returncode==0; return out
run('PR_edit',['gh','pr','edit','57','--repo','AlecKriebel/Math','--title',title,'--body-file',str(F/'PREPARED_PR_BODY.md')])
pr=json.loads(run('PR_metadata_readback',['gh','pr','view','57','--repo','AlecKriebel/Math','--json','number,state,title,body,headRefOid,mergeCommit,mergedAt,url']))
assert pr['state']=='MERGED' and pr['headRefOid']=='4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29' and pr['mergeCommit']['oid']==native['merge_commit']
assert pr['title']==title and pr['body']==body
record={'schema':'pr57-actual-current-PR-metadata-readback/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'title':title,'full_body_exact_readback':True,'state':'MERGED','merge_commit':native['merge_commit'],'DOI':pub['DOI'],'tracker_range':tracker['range'],'commands':commands,'new_central_proof_attempts':0,'PR57_ordered_workflow_percent':98,'dated_completed_program_fraction_percent':5/99*100,'goal_complete':False}
with (F/'PR_METADATA_READBACK.json').open('x') as f: json.dump(record,f,indent=2); f.write('\n')
print(json.dumps(record,indent=2))
