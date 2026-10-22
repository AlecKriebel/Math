"""Publish exact owned completion evidence after native PR254 merge, without checkout/index mutations."""
from pathlib import Path
from datetime import datetime,timezone
import json,subprocess
HERE=Path(__file__).resolve().parent; ROOT=Path('/Users/alec/Documents/Math'); P=ROOT/'draft_pr_descending_audit_20261002'; D=HERE.parent/'initial_review_20261013'; PUB=HERE.parent/'publication'
OUT=PUB/('completion-publication-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));OUT.mkdir(exist_ok=False)
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'; seq=0; BASE='repos/AlecKriebel/Math/'
def api(method,path,payload=None):
 global seq
 seq+=1;args=[GH,'api','--method',method,BASE+path]
 if payload is not None:
  f=OUT/f'{seq:02d}-request.json';f.write_text(json.dumps(payload));args+=['--input',str(f)]
 r=subprocess.run(args,capture_output=True);(OUT/f'{seq:02d}-stdout.json').write_bytes(r.stdout);(OUT/f'{seq:02d}-stderr.txt').write_bytes(r.stderr)
 if r.returncode:raise RuntimeError('Native completion call failed; reconcile receipts before retry')
 return json.loads(r.stdout)
m=json.loads((PUB/'PR_MERGED.json').read_text());assert m['PR']==254 and m['merged'] and m['case_completion_percent']==100
pr=api('GET','pulls/254');assert pr['merged'] and pr['merge_commit_sha']==m['merge_commit']
paths=[P/'RESEARCH_LOG.md',P/'CURRENT_GOAL_SELECTION_20261013.json',D/'RESEARCH_LOG.md',HERE/'PACKAGE_STATE.json',HERE/'FINAL_CLEARANCE.json',HERE/'publish_completion.py',PUB/'PR_MERGED.json']
entries=[{'path':f.relative_to(ROOT).as_posix(),'mode':'100644','type':'blob','content':f.read_text()} for f in paths]
for n in ['FINAL_ACCEPTANCE.json','DISPOSITION.md','final_queue_state.json','RESEARCH_LOG.md','FROZEN_MANIFEST.json','PUBLICATION_MANIFEST.json','FINAL_PACKAGE_MANIFEST.json']:
 f=HERE/'pr_update/5100020'/n;entries.append({'path':'unsolved_math_prioritization/attempts/5100020/'+n,'mode':'100644','type':'blob','content':f.read_text()})
for attempt in range(4):
 parent=api('GET','git/ref/heads/main')['object']['sha'];tree=api('GET','git/commits/'+parent)['tree']['sha'];nt=api('POST','git/trees',{'base_tree':tree,'tree':entries})['sha'];commit=api('POST','git/commits',{'message':'Record verified k403a preprint, tracker and native merge completion','tree':nt,'parents':[parent]})['sha']
 try:
  assert api('PATCH','git/refs/heads/main',{'sha':commit,'force':False})['object']['sha']==commit;break
 except RuntimeError:
  reject=json.loads((OUT/f'{seq:02d}-stdout.json').read_text());latest=api('GET','git/ref/heads/main')['object']['sha']
  if reject.get('status')!='422' or latest==parent or attempt==3:raise
current=api('GET','git/ref/heads/main')['object']['sha']
if current!=commit:assert api('GET','compare/'+commit+'...'+current)['status']=='ahead'
r={'utc':datetime.now(timezone.utc).isoformat(),'commit':commit,'parent':parent,'readback_main':current,'owned_files':len(entries),'case_completion_percent':100,'program_counts':[39,16,16,0],'goal_active_incomplete':True,'shared_checkout_and_index_mutations':0,'transport_receipts':str(OUT)};(PUB/'COMPLETION_PUBLICATION_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
