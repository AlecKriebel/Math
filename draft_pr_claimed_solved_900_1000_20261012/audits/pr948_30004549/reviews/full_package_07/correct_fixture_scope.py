from pathlib import Path
import json,datetime,os
R=Path(__file__).parent;H=R/'history/initial_fixture_scope';H.mkdir(parents=True)
selected=['run_inert.py','adapted_test_workflow.py','DIFF_test_workflow.py.json','INERT_WORKFLOW_01.json','INERT_ROOT_FIXES.json','INERT_BASE_CONTEXT.json','INERT_LIVE_BASE_CONTEXT.json','INERT_REVIEW_HISTORY.json','INERT_SUITE_EXECUTIONS.json','reproduce.py','COLD_REPLAY.json']+['COLD_MODE_'+x+'.json' for x in ['normal','O','OO','env2']]
files={}
for name in selected:
 b=(R/name).read_bytes()
 with (H/name).open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert (H/name).read_bytes()==b
 import hashlib
 files[name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
d={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'FAILED_REVIEWER_FOLDER_CONFINEMENT_NOT_CANDIDATE_DEFECT','observation':'Initial workflow97 adaptation changed its receipt only, missing original TemporaryDirectory(prefix=private-fixture-,dir=W). Source proves this fixture was created and automatically removed under sealed workflow directory. No production action or intended sealed-file edit occurred. Original cold checker replays also inherited default OS temporary directory; future cold replays set TMPDIR to own07. These actual first runs are retained, not retrospectively folder-confined.','independence':'Complete actual START and own saved independent attack order remain intact. This failure concerns write scope, not prior mathematical intake. Under strict work-ONLY instruction this round will preserve nonclean history unless the authorized scope is explicitly clarified.','candidate_repair':False,'first_run_files':files,'exact_temporary_path':'Unknown: TemporaryDirectory generated and cleaned its name; do not invent a path.'}
raw=(json.dumps(d,indent=2)+'\n').encode()
with (R/'FIXTURE_SCOPE_DEVIATION.json').open('wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert (R/'FIXTURE_SCOPE_DEVIATION.json').read_bytes()==raw
p=R/'run_inert.py';s=p.read_text();needle="'test_workflow.py':[(";replacement="'test_workflow.py':[(\"tempfile.TemporaryDirectory(prefix='private-fixture-',dir=W)\",\"tempfile.TemporaryDirectory(prefix='private-fixture-',dir=Path(\"+repr(str(R))+\"))\"),(";assert s.count(needle)==1;s=s.replace(needle,replacement);p.write_text(s)
p=R/'reproduce.py';s=p.read_text().replace("root=R/'private_cold'","root=R/'private_cold_rerun'").replace("env=os.environ.copy(); started=utc()","env=os.environ.copy(); tmp=R/'cold_child_tmp';tmp.mkdir(exist_ok=True);env['TMPDIR']=str(tmp);env['TMP']=str(tmp);env['TEMP']=str(tmp); started=utc()");p.write_text(s)
print('preserved initial runs and corrected only fixture/output environment paths')
