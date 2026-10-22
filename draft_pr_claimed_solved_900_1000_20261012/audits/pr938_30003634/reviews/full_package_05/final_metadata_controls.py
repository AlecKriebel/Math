"""Actual finalizer metadata statements; every service call is mocked."""
import ast,copy,importlib.util,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parents[3];T=R/'private/final_metadata';T.mkdir(exist_ok=True);rows=[]
spec=importlib.util.spec_from_file_location('review05metadata',P/'finalize_pr938_and_gate_next.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
fn=next(n for n in ast.parse((P/'finalize_pr938_and_gate_next.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='main');block=[]
for n in fn.body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='state' for t in n.targets):break
 block.append(n)
code=compile(ast.fix_missing_locations(ast.Module(body=block,type_ignores=[])),'actual_final_metadata_prefix','exec')
pub={'doi':'10.5281/zenodo.123','record_url':'https://zenodo.org/records/123'};merge={'headRefOid':m.HEAD,'mergeCommit':{'oid':'b'*40}};tracker={'updated_range':"'Math Puzzles'!A10:D10"};native={'commit':'d'*40};accepted={'full_package_reviews':[{}, {}, {}, {}, {'manifest_sha256':'a'*64}]}
def need(v,s):
 if not v:raise RuntimeError(s)
for initial in ['different','already_exact']:
 for drift in [None,'state','headRefOid','mergeCommit','body','title']:
  captures=[];calls=[];state={'body':None,'title':None};ns=dict(m.__dict__,A=T,D=T,verify_completed=lambda:(pub,merge,tracker,native,accepted),load=lambda p:{'revision_candidate':5},save=lambda p,v:captures.append((p.name,v)))
  def read(args):
   calls.append(args)
   if args[:3]==['gh','pr','edit']:
    state['body']=Path(args[args.index('--body-file')+1]).read_text();state['title']=args[args.index('--title')+1];return ''
   if args[:3]==['gh','pr','view']:
    if args[-1]=='title,body':
     if initial=='already_exact':return json.dumps({'title':'30003634: accepted all-depth pure-braid counterexamples and published preprint','body':ns['body']})
     return json.dumps({'title':'old','body':'old'})
    v={'number':938,'state':'MERGED','headRefOid':merge['headRefOid'],'mergeCommit':merge['mergeCommit'],'body':ns['body'],'title':ns['title']}
    if drift:v[drift]={'state':'OPEN','headRefOid':'0'*40,'mergeCommit':{'oid':'0'*40},'body':'drift','title':'drift'}[drift]
    return json.dumps(v)
   raise RuntimeError('Unmocked service action')
  ns['run']=read;label=initial+'_'+str(drift)
  try:exec(code,ns)
  except RuntimeError as e:
   need(drift is not None and 'metadata readback differs' in str(e),str(e));need(not any(n=='PR_PUBLISHED_METADATA.json' for n,v in captures),'bad confirmation saved');rows.append({'case':label,'rejected_final_readback':True});continue
  need(drift is None,'adverse accepted');need(any(n=='PR_PUBLISHED_METADATA.json' for n,v in captures),'confirmation absent');need(sum(c[:3]==['gh','pr','edit'] for c in calls)==(initial=='different'),'idempotence');need('known combined2/5' in ns['body'] and 'unrefereed' in ns['body'] and 'Kawasaki' in ns['body'] and 'finite' in ns['body'],'summary scope');rows.append({'case':label,'passed':True,'all_service_actions_mocked':True})
# Execute exact completed/active-target early-return guard as a tiny function.
start=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='state' for t in n.targets));guard=[]
for node in fn.body[start:]:
 guard.append(node)
 if isinstance(node,ast.If):break
# The first statement also assigns already and validates active target; second is return conditional.
gf=ast.FunctionDef(name='guard',args=ast.arguments(posonlyargs=[],args=[],kwonlyargs=[],kw_defaults=[],defaults=[]),body=guard+[ast.Return(value=ast.Constant('CONTINUE'))],decorator_list=[]);gcode=compile(ast.fix_missing_locations(ast.Module(body=[gf],type_ignores=[])),'actual_completion_idempotence','exec')
for completed,active,want in [(True,939,None),(True,None,'CONTINUE'),(False,938,'CONTINUE'),(False,939,'REJECT')]:
 ns=dict(m.__dict__,load=lambda p,c=completed,a=active:{'completed_prs':[938] if c else [],'active_pr':a},print=lambda *a,**k:None);exec(gcode,ns)
 try:value=ns['guard']()
 except RuntimeError:need(want=='REJECT','unrelated rejection');rows.append({'case':'active_guard_'+str(completed)+'_'+str(active),'rejected':True});continue
 need(value==want,'active guard');rows.append({'case':'active_guard_'+str(completed)+'_'+str(active),'passed':True})
result={'status':'PASS','cases':len(rows),'rows':rows,'real_external_calls':0,'operational_mains_called':False};(R/'FINAL_METADATA_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','cases':len(rows)}))
