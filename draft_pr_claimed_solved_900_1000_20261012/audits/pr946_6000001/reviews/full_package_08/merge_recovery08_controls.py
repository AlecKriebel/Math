"""Actual06 merge/readiness and uncertain-action recovery; all Git/services fake."""
import sys
if not sys.flags.isolated or sys.flags.optimize:raise RuntimeError('Use -I -B')
from pathlib import Path
import json,copy,types,contextlib,io,shutil,hashlib
from datetime import datetime,timezone
O=Path(__file__).resolve().parent;s=(O/'closure08_controls.py').read_text();ns={'__file__':str(O/'closure08_controls.py'),'__name__':'_merge_setup_'};exec(compile(s[:s.index('\ntargets=')],str(O/'closure08_controls.py'),'exec'),ns);N=ns['N'];a=ns['a'];d=ns['d'];ctx=ns['ctx'];F=ns['F'];accepted=ns['accepted'];baseview=N['pr_view'];baserun=N['run'];oldacc=(a/'ACCEPTANCE.json').read_bytes();tex=d/'research_note.tex';oldtex=tex.read_bytes();review=a/'reviews/full_package_08/FULL_AUDIT.md';oldreview=review.read_bytes();extra=a/'reviews/full_package_09';records=[];mergeid='b'*40;initial=baseview();state=copy.deepcopy(initial);dispatch=[]
def run(argv,**kw):
 if argv[:2]==['git','show'] and '--format=%P' in argv:return 'a'*40+' '+N['HEAD']+'\n'
 return baserun(argv,**kw)
N['run']=run;N['pr_view']=lambda:copy.deepcopy(state)
def restore():
 global state
 state=copy.deepcopy(initial);dispatch.clear();tex.write_bytes(oldtex);review.write_bytes(oldreview);(a/'ACCEPTANCE.json').write_bytes(oldacc)
 if extra.exists():shutil.rmtree(extra)
 for q in list(a.glob('PR_MERGE*json'))+list(a.glob('PR_READY_ACTION.json')):q.unlink()
def call(fn):
 with contextlib.redirect_stdout(io.StringIO()):return fn()
def reject(label,fn):
 try:call(fn)
 except (RuntimeError,OSError,ValueError,KeyError) as e:
  assert 'Unexpected fake' not in str(e) and 'Forbidden external' not in str(e);records.append({'case':label,'rejected':True,'reason':str(e)[:450]});return
 raise RuntimeError('INVALID ACCEPTED '+label)
for kind in ['valid','pending','adverse','revocation','tex','sealed_review','head_drift','uncertain_merge']:
 restore()
 def action(argv,**kw):
  dispatch.append(argv[:3]);assert argv[:3] in [['gh','pr','ready'],['gh','pr','merge']]
  if argv[2]=='ready':
   state['isDraft']=False
   if kind in ['pending','adverse']:
    extra.mkdir()
    if kind=='adverse':(extra/'RESULT.json').write_text('{"optional_issues":[{"id":"SYNTHETIC_ADVERSE"}]}')
   elif kind=='revocation':j=json.loads(oldacc);j['accepted']=False;(a/'ACCEPTANCE.json').write_text(json.dumps(j))
   elif kind=='tex':tex.write_bytes(oldtex+b'\n')
   elif kind=='sealed_review':review.write_bytes(oldreview+b'\n')
   elif kind=='head_drift':state['headRefOid']='0'*40
   return types.SimpleNamespace(returncode=0,stdout='fake',stderr='')
  assert '--match-head-commit' in argv and argv[-1]==N['HEAD'] and '--merge' in argv
  if kind=='uncertain_merge':return types.SimpleNamespace(returncode=1,stdout='',stderr='network outcome uncertain')
  state.update(state='MERGED',mergeCommit={'oid':mergeid});return types.SimpleNamespace(returncode=0,stdout='fake',stderr='')
 N['subprocess'].run=action
 if kind=='valid':
  call(lambda:N['merge'](types.SimpleNamespace(),ctx));assert dispatch==[['gh','pr','ready'],['gh','pr','merge']];assert N['load'](a/'PR_MERGE_RECEIPT.json')['mergeCommit']['oid']==mergeid;records.append({'case':'positive_actual_ready_exact_head_ordinary_merge_and_readback','pass':True})
 else:
  reject('after_ready_'+kind,lambda:N['merge'](types.SimpleNamespace(),ctx));assert dispatch==([['gh','pr','ready'],['gh','pr','merge']] if kind=='uncertain_merge' else [['gh','pr','ready']])
  if kind=='uncertain_merge':before=list(dispatch);reject('uncertain_merge_reentry_no_blind_dispatch',lambda:N['merge'](types.SimpleNamespace(),ctx));assert dispatch==before
restore()
# The actual kit helper persists failures and refuses a blind retry of a writing intent.
state.update(state='MERGED',isDraft=False,mergeCommit={'oid':mergeid});N['save'](a/'PR_MERGE_RECEIPT.json',state)
for name in d.glob('ZENODO_STAGE*'):name.unlink()
calls=[0]
def failedkit(argv,**kw):
 calls[0]+=1;assert kw['input']==ctx['captured'][N['KIT']] and argv[1:4]==['-I','-S','-B'];return types.SimpleNamespace(returncode=1,stdout=b'',stderr=b'SYNTHETIC lost response')
N['subprocess'].run=failedkit;reject('actual_helper_stage_uncertain_failure',lambda:N['zenodo'](types.SimpleNamespace(action='stage'),ctx));assert N['load'](d/'ZENODO_STAGE_FAILURE.json')['blind_retry_permitted'] is False;reject('actual_helper_stage_reentry_no_blind_dispatch',lambda:N['zenodo'](types.SimpleNamespace(action='stage'),ctx));assert calls[0]==1
for name in d.glob('ZENODO_STAGE*'):name.unlink()
(O/'MERGE_RECOVERY08_CONTROLS.json').write_text(json.dumps({'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'actual_current08_context':True,'terminal08_explicitly_synthetic':True,'actual_merge_premerge_source_merged_gate_and_all_shared_guards':True,'only_Git_PR_kit_transport_fake':True,'actual_external_mutations':0,'cases':records,'case_count':len(records)},indent=2)+'\n');print(json.dumps({'status':'PASS','cases':len(records)}))
