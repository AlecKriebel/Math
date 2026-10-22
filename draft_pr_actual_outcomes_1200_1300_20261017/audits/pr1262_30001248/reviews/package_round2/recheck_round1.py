#!/usr/bin/env python3
"""After independent assessment, authenticate and cross-check prior actual evidence."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
R=Path(__file__).resolve().parent;A=R.parents[1];Q=A/'reviews/package_round1'
def need(x,m):
 if not x:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((Q/'MANIFEST.json').read_text());files=[]
for e in m['authored_files']:
 p=Q/e['path'];need(len(p.read_bytes())==e['bytes'] and sha(p)==e['sha256'],'prior manifest member '+e['path']);files.append(e['path'])
# Compare semantic replay outputs and exact actual release anchors, not prose alone.
ours=json.loads((R/'PORTABLE_REPLAYS.json').read_text())
for x,n in zip(ours['runs'],['PORTABLE_NORMAL.json','PORTABLE_O.json','PORTABLE_OO.json']):need(x['result']==json.loads((Q/n).read_text()),'prior portable evidence differs')
ours_workflow=json.loads((R/'WORKFLOW_REPLAYS.json').read_text())
for x,n in zip(ours_workflow['runs'],['WORKFLOW_NORMAL.json','WORKFLOW_O.json','WORKFLOW_OO.json']):need(x['result']==json.loads((Q/n).read_text()),'prior workflow evidence differs')
source=Q/'independent_safeguards.py';original=source.read_text();needle='R=Path(__file__).resolve().parent; A=R.parents[1];';need(original.count(needle)==1,'unknown prior layout')
# Path-only adaptation: use own scratch instead of the immutable prior family.
replacement='R=Path('+repr(str(R))+'); A=R.parents[1];';code=original.replace(needle,replacement)
p=R/'_local/prior_safeguards_pathonly_replay.py';p.write_text(code)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
r=subprocess.run([sys.executable,'-B',str(p)],env=env,capture_output=True,text=True,timeout=180);need(r.returncode==0,r.stderr);result=json.loads(r.stdout)
prior=json.loads((Q/'INDEPENDENT_SAFEGUARDS.json').read_text());need(result==prior,'prior safeguards evidence differs')
out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','read_only_after_independent_assessment':True,'prior_manifest_sha256':sha(Q/'MANIFEST.json'),'prior_authored_members_authenticated':files,'portable_all_three_semantic_outputs_identical':True,'workflow_all_three_semantic_outputs_identical':True,'prior_safeguards_source_sha256':sha(source),'scratch_path_only_adaptation':{'exact_old':needle,'exact_new':replacement},'prior_safeguards_actual_kit_and_postmerge_replayed':result,'same_as_prior_saved_evidence':True,'scope':'This is cross-check/replay of prior reviewer authored controls AFTER independent analysis; not an independent authorship claim for those controls. All service/Git/compiler I/O mocked, writes only own scratch.'}
(R/'ROUND1_CROSSCHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','prior_authored_members':len(files),'prior_safeguards_matches':True}))
