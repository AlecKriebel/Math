"""Independent read-only imports and bounded mocked action preflights; no mains."""
import ast,copy,hashlib,importlib.util,json,os,shutil,sys,types
from pathlib import Path
from datetime import datetime,timezone
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;P=R.parents[3];A=R.parents[1];D=A/'publication';S=R/'private/helpers';S.mkdir(exist_ok=True)
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def mod(name):
 if name=='update_pr938_publication_ledger' and sys.flags.optimize:
  # The whole ledger module explicitly forbids optimized operational use.
  # Extract only its verbatim imports/constants/pure definitions for tests.
  tree=ast.parse((P/(name+'.py')).read_text());nodes=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.Assign,ast.FunctionDef))]
  m=types.ModuleType(name);m.__file__=str(P/(name+'.py'));exec(compile(ast.Module(body=nodes,type_ignores=[]),str(P/(name+'.py')),'exec'),m.__dict__);return m
 spec=importlib.util.spec_from_file_location(name,P/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
ac=mod('accept_pr938');me=mod('merge_pr938');ze=mod('run_pr938_zenodo');tr=mod('append_pr938_tracker');le=mod('update_pr938_publication_ledger')
rows=[]
def test(name,call,reject=False):
 try:call()
 except Exception as e:
  if not reject:raise
  rows.append({'case':name,'rejected':True,'error':str(e)});return
 if reject:raise RuntimeError('Adverse case accepted '+name)
 rows.append({'case':name,'passed':True})
valid=['01:'+'a'*64,'02:'+'b'*64,'03:'+'c'*64]
test('R1_R4_complete_canonical',lambda:ac.validate_review_sequence(valid))
for label,seq in [('skip',[valid[0],valid[2]]),('reverse',valid[::-1]),('duplicate',[valid[0],valid[0]]),('alias001',['001:'+'a'*64,'002:'+'b'*64]),('no01',valid[1:]),('missing_history',[valid[0]])]:test('R1_R4_'+label,lambda seq=seq:ac.validate_review_sequence(seq),True)
mandatory=['RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json']
for i in [1,2]:
 f=A/'reviews'/('full_package_'+str(i).zfill(2));mapping=load(f/'MANIFEST.json');result=load(f/'RESULT.json');base=D/'reviewed_candidates'/('candidate'+str(i).zfill(2));freeze=load(base/'PREPUBLICATION_FREEZE.json')
 test('R2_genuine_sealed_inventory_'+str(i),lambda f=f,mapping=mapping:ac.authenticate_review_records(f,mapping))
 test('R5_genuine_full_evidence_'+str(i),lambda f=f,result=result,base=base,freeze=freeze:ac.validate_review_evidence(f,result,freeze,base))
base=D/'reviewed_candidates/candidate02';freeze=load(base/'PREPUBLICATION_FREEZE.json');source=A/'reviews/full_package_02';result=load(source/'RESULT.json');F=S/'evidence';F.mkdir(exist_ok=True)
for n in mandatory:shutil.copyfile(source/n,F/n)
def reset():
 for n in mandatory:shutil.copyfile(source/n,F/n)
def evidence():ac.validate_review_evidence(F,result,freeze,base)
changes=[('head','AUTHENTICATION_START.json',lambda x:x.update(original_pr_head='0'*40)),('freeze','AUTHENTICATION_START.json',lambda x:x.update(freeze_sha256='0'*64)),('helper','AUTHENTICATION_END.json',lambda x:x['future_helpers'].pop('merge_pr938.py')),('archive','AUTHENTICATION_START.json',lambda x:x.update(archive_members=1)),('payload_bool','AUTHENTICATION_END.json',lambda x:x.update(payloads=True)),('time','AUTHENTICATION_END.json',lambda x:x.update(utc='2000-01-01T00:00:00+00:00')),('end_status','AUTHENTICATION_END.json',lambda x:x.update(status='FAIL')),('cold_status','COLD_REPLAY.json',lambda x:x.update(status='FAIL')),('cold_pin','COLD_REPLAY.json',lambda x:x.update(externally_pinned_verifier_sha256='0'*64)),('cold_fresh','COLD_REPLAY.json',lambda x:x.update(fresh_archive_extraction=False)),('cold_modes','COLD_REPLAY.json',lambda x:x['modes'].pop()),('cold_result','COLD_REPLAY.json',lambda x:x['modes'][0]['result'].update(pr=True))]
# Resolve historical field names explicitly, then alter original records.
for label in ['missing_original','blob','mode','bytes_bool','disk_mode','archive_mode','matching_false']:
 def mutate(x,label=label):
  key='all_actual_git_blob_mode_disk_archive_checks' if 'all_actual_git_blob_mode_disk_archive_checks' in x else 'originals';o=x[key];n=next(iter(o))
  if label=='missing_original':o.pop(n)
  else:o[n][{'blob':'git_blob','mode':'git_mode','bytes_bool':'bytes','disk_mode':'disk_mode','archive_mode':'archive_mode','matching_false':'disk_and_archive_match'}[label]]={'blob':'0'*40,'mode':'100755','bytes_bool':True,'disk_mode':'0755','archive_mode':'100755','matching_false':False}[label]
 changes.append((label,'AUTHENTICATION_END.json',mutate))
for label,name,fn in changes:
 reset();x=load(F/name);fn(x);write(F/name,x);test('R5_'+label,evidence,True)
reset()
for name in mandatory:
 reset();(F/name).write_text(' \n');mapping={'files':{n:dict(bytes=(F/n).stat().st_size,sha256=sha((F/n).read_bytes())) for n in mandatory},'explicit_public_allowlist':mandatory}
 test('R2_R5_empty_'+name,lambda mapping=mapping:ac.authenticate_review_records(F,mapping),True)
reset();mapping={'files':{},'explicit_public_allowlist':[]};test('R2_empty_map',lambda:ac.authenticate_review_records(F,mapping),True)
for raw in ['{"a":1,"a":2}','{"x":NaN}','{"x":Infinity}']:test('R5_strictJSON_'+raw,lambda raw=raw:ac.strict_json(raw),True)
reset();mapping={'files':{n:dict(bytes=(F/n).stat().st_size,sha256=sha((F/n).read_bytes())) for n in mandatory},'explicit_public_allowlist':mandatory};(F/'RESULT.json').write_text('{}');test('R2_postseal_verdict_mutation',lambda:ac.authenticate_review_records(F,mapping),True)
freeze3=load(D/'PREPUBLICATION_FREEZE.json');body=(A/'PR_DESCRIPTION_CORRECTED.md').read_text()
if sha(body.encode())!=freeze3['pr_description_sha256']:raise RuntimeError('Actual reviewed body pin mismatch')
test('R3_exact_body',lambda:me.require_reviewed_description({'body':body},freeze3))
for label,b in [('changed',body+' '),('missing',None)]:test('R3_'+label,lambda b=b:me.require_reviewed_description({'body':b},freeze3),True)
# comparator is imported from externally authenticated verifier, not reimplemented.
spec=importlib.util.spec_from_file_location('verifier',D/'verify_package.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
for actual,expected in [({'n':True},{'n':1}),({'m':3.0},{'m':3}),({'nullity':False},{'nullity':0}),({'v':[False]},{'v':[0]})]:test('O1_type_exact_'+repr(actual),lambda actual=actual,expected=expected:v.equivalent(actual,expected),True)
worker=ast.parse((D/'verify_package.py').read_text());test('O1_actual_worker_uses_equivalent',lambda: (_ for _ in ()).throw(RuntimeError('Missing actual call')) if "equivalent(author, author_expected" not in (D/'verify_package.py').read_text() else None)
# Complete linked-receipt fixtures, with only reviewer-scoped copied uploads.
T=S/'receipts';(T/'publication/output/pdf').mkdir(parents=True,exist_ok=True)
for n in ['PREPUBLICATION_FREEZE.json','zenodo-deposit.json','output/pdf/note.pdf','deep-derived-pure-braids-source-verification-v1.0.zip']:shutil.copyfile(D/n,T/'publication'/n)
pin=sha((T/'publication/PREPUBLICATION_FREEZE.json').read_bytes());acc=dict(accepted=True,original_pr_head=ac.HEAD,full_package_reviews=[{},{}],freeze_sha256=pin,files=freeze3['files']);merge=dict(number=938,state='MERGED',headRefOid=ac.HEAD,mergeCommit={'oid':'b'*40});desc=load(T/'publication/zenodo-deposit.json');files=[dict(name=i['name'],size=freeze3['files'][i['path']]['bytes'],sha256=freeze3['files'][i['path']]['sha256']) for i in desc['files']];pub=dict(id=123,state='published',doi='10.5281/zenodo.123',record_url='https://zenodo.org/records/123',files=files)
intent=dict(action='publish',pr=938,accepted_freeze_sha256=pin,merged_commit='b'*40,descriptor_sha256=sha((T/'publication/zenodo-deposit.json').read_bytes()));write(T/'publication/ZENODO_PUBLISH_INTENT.json',intent);write(T/'publication/ZENODO_STAGE.json',pub);write(T/'publication/ZENODO_INSPECT.json',pub)
tracker=dict(confirmed=True,readback_matches=True,pr=938,problem_id='30003634',original_pr_head=ac.HEAD,merged_head=ac.HEAD,merge_commit='b'*40,accepted_freeze_sha256=pin,doi=pub['doi'],zenodo_record_id=123,spreadsheet_id=tr.SID,gid=1254632077,tab_title='Math Puzzles',updated_range="'Math Puzzles'!A10:D10",row=['primary','','https://doi.org/'+pub['doi'],'note'])
def readback(t=tracker):write(T/'TRACKER_READBACK.json',dict(range=t['updated_range'],values=[t['row']]))
readback()
for m in [tr,le]:
 test('O2_full_receipt_positive_'+m.__name__,lambda m=m:m.verify_receipt_links(T,pub,merge,acc,tracker))
 wrong_base=copy.deepcopy(merge);wrong_base['baseRefName']='unreviewed-other-branch'
 test('NEW_R6_downstream_accepts_wrong_base_'+m.__name__,lambda m=m:m.verify_receipt_links(T,pub,wrong_base,acc,tracker))
 for range_ in ["'Other tab'!A10:D10","'Math Puzzles'!B10:E10","'Math Puzzles'!A10:D11","'Math Puzzles'!A1:D1","'Math Puzzles'!A0:D0","'Math Puzzles'!A01:D01"]:
  t=copy.deepcopy(tracker);t['updated_range']=range_;readback(t);test('O2_range_'+m.__name__+range_,lambda t=t,m=m:m.verify_receipt_links(T,pub,merge,acc,t),True)
 readback();write(T/'TRACKER_READBACK.json',dict(range="'Math Puzzles'!A11:D11",values=[tracker['row']]));test('O2_exact_readback_'+m.__name__,lambda m=m:m.verify_receipt_links(T,pub,merge,acc,tracker),True);readback()
 for key,value in [('id',True),('doi','10.5281/zenodo.124'),('record_url','https://zenodo.org/records/124'),('files',files[::-1])]:
  p=copy.deepcopy(pub);p[key]=value;test('receipt_'+m.__name__+'_'+key,lambda p=p,m=m:m.verify_receipt_links(T,p,merge,acc,tracker),True)
 for key,value in [('original_pr_head','0'*40),('freeze_sha256','0'*64)]:
  a=copy.deepcopy(acc);a[key]=value;test('receipt_'+m.__name__+'_'+key,lambda a=a,m=m:m.verify_receipt_links(T,pub,merge,a,tracker),True)
 for key,value in [('gid',1),('tab_title','Other'),('merged_head','0'*40),('doi','bad')]:
  t=copy.deepcopy(tracker);t[key]=value;test('receipt_'+m.__name__+'_'+key,lambda t=t,m=m:m.verify_receipt_links(T,pub,merge,acc,t),True)
# Selected-state byte preservation without invoking tree writer.
raw='{\n  "other": { "unusual": [1, 2] },\n  "30003634": {"turns_used": 1},\n  "last" : 7\n}\n';changed=le.replace_entry(raw,'30003634',{'turns_used':2})
if '"other": { "unusual": [1, 2] }' not in changed or '"last" : 7' not in changed:raise RuntimeError('Unrelated state bytes changed')
rows.append(dict(case='selected_state_other_entries_byte_preserved',passed=True))
# Actual merge preflight, stopping BEFORE its first save or action. All reads mocked.
M=S/'mergefixture';M.mkdir(exist_ok=True);shutil.copytree(D,M/'publication',dirs_exist_ok=True,ignore=shutil.ignore_patterns('tmp','reviewed_candidates','__pycache__'))
for name in ['PUBLICATION_DISPOSITION.json','ORIGINAL_SNAPSHOT.json','TARGET_IDENTITY_PREFLIGHT.json']:shutil.copyfile(A/name,M/name)
write(M/'ACCEPTANCE.json',dict(acc,files=freeze3['files']))
fn=next(n for n in ast.parse((P/'merge_pr938.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='main')
block=[]
for node in fn.body:
 if isinstance(node,ast.If) and ast.unparse(node.test)=="pr['state'] != 'MERGED'":
  sub=[]
  for x in node.body:
   if isinstance(x,ast.Assign) and any(isinstance(y,ast.Name) and y.id=='intent' for y in x.targets):break
   sub.append(x)
  block.extend(sub);break
 block.append(node)
code=compile(ast.fix_missing_locations(ast.Module(body=block,type_ignores=[])),'bounded_actual_merge_preflight','exec')
orig=load(A/'ORIGINAL_SNAPSHOT.json');target=load(A/'TARGET_IDENTITY_PREFLIGHT.json');catalog=dict(id='30003634',present=True,holds=[],statement_hash=target['statement_hash'],review_hash=target['review_hash'])
queue='| x | 30003634 / x | x | x | x | x | x | claimed_solved | 1/5 | x |\n'
def mocked_run(args):
 if args[:3]==['gh','api','repos/AlecKriebel/Math/pulls/938/files']:return '\n'.join(orig['files'])
 if args[:2]==['git','fetch']:return ''
 if args[:2]==['git','ls-remote']:return 'a'*40+' refs/heads/main\n'
 if args[:2]==['gh','api'] and args[2].startswith('repos/AlecKriebel/Math/contents/'):return queue
 raise RuntimeError('Unmocked call '+repr(args))
def blob(ref,name):
 if name=='unsolved_math_prioritization/catalog.json':return json.dumps([catalog]).encode()
 return (A/'original'/name).read_bytes()
for base_name in ['main','unreviewed-other-branch']:
 pr=dict(number=938,state='OPEN',isDraft=True,headRefOid=ac.HEAD,body=body,baseRefName=base_name)
 ns=dict(me.__dict__,A=M,view=lambda pr=pr:pr,run=mocked_run,rawblob=blob)
 exec(code,ns)
 rows.append(dict(case='NEW_R6_actual_bounded_merge_base_'+base_name,preflight_accepted=True,network_or_write_actions=False))
# view() itself fails to request baseRefName.
requested=[];old=me.run;me.run=lambda args:requested.append(args) or '{}';me.view();me.run=old
rows.append(dict(case='NEW_R6_view_fields',fields=requested[0][-1],baseRefName_requested='baseRefName' in requested[0][-1]))
# Actual Zenodo preflight only, before intent creation or repository kit calls.
zf=next(n for n in ast.parse((P/'run_pr938_zenodo.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='main');zb=[]
for n in zf.body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='intent' for t in n.targets):break
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('ap','args') for t in n.targets):continue
 if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and isinstance(n.value.func.value,ast.Name) and n.value.func.value.id=='ap':continue
 zb.append(n)
zc=compile(ast.Module(body=zb,type_ignores=[]),'bounded_actual_zenodo_preflight','exec')
for base_name in ['main','unreviewed-other-branch']:
 write(M/'PR_MERGE_RECEIPT.json',dict(merge,baseRefName=base_name));write(M/'publication/ZENODO_STAGE.json',pub)
 ns=dict(ze.__dict__,A=M,D=M/'publication',args=types.SimpleNamespace(action='publish'))
 exec(zc,ns)
 rows.append(dict(case='NEW_R6_actual_bounded_publish_base_'+base_name,preflight_accepted=True,network_or_write_actions=False))
# Actual append/recovery boundary without invoking main or a connected service.
tree=ast.parse((P/'append_pr938_tracker.py').read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');section=[];taking=False
for n in fn.body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='hits' for t in n.targets):taking=True
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='receipt' for t in n.targets):break
 if taking:section.append(n)
append_code=compile(ast.Module(body=section,type_ignores=[]),'bounded_actual_append_recovery','exec')
for recovered in [False,True]:
 for range_ in [tracker['updated_range'],"'Other tab'!A10:D10","'Math Puzzles'!A10:D11"]:
  def run_append(recovered=recovered,range_=range_):
   def fake_gws(args):
    if 'append' in args:return {'updates':{'updatedRange':range_,'updatedRows':1,'updatedCells':4}}
    return {'range':range_,'values':[tracker['row']]}
   existing={'values':[['header']]+([['filler']]*8+[tracker['row']] if recovered else [])}
   ns=dict(tr.__dict__,doi=pub['doi'],row=tracker['row'],existing=existing,table="'Math Puzzles'!A:D",gws=fake_gws,save=lambda *args:None)
   exec(append_code,ns)
  # Recovery derives the canonical A1 range, so false readback ranges reject.
  test('O2_actual_'+('recovery' if recovered else 'append')+'_'+range_,run_append,range_!=tracker['updated_range'])
out=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS_CONTROLS_WITH_NEW_FINDING_R6',actual_parent_optimization=sys.flags.optimize,rows=rows,operational_main_called=False,ledger_optimized_guard_respected=True,all_fixture_mutations_scoped_to=str(S),new_R6='Live base branch is neither requested nor checked by actual merge preflight; unchanged accepted head/body can be merged into a changed PR base.')
label=sys.argv[1] if len(sys.argv)>1 else 'normal'
(R/('HELPER_CONTROLS_'+label+'.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'cases':len(rows),'R6_reproduced':True,'actual_parent_optimization':sys.flags.optimize}))
