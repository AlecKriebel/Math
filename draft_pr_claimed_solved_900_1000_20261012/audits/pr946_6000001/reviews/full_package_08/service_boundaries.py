"""Candidate06 positive operations and new boundary controls; fake services only."""
import sys
if not sys.flags.isolated or sys.flags.optimize:raise RuntimeError('Use -I -B')
from pathlib import Path
import json,hashlib,copy,types,io,contextlib
O=Path(__file__).resolve().parent;R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';root=O/'private/current08_context';p=root/P.name;a=p/'audits/pr946_6000001';d=a/'preprint'
N={'__name__':'_candidate06_service_boundaries_','__file__':str(P/'accept_pr946.py')};raw=(P/'accept_pr946.py').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8e1a0d7b3ca6e5d72e76415541b393fbfbe52e307368bc86b9e7982d5be27cd7';exec(compile(raw,N['__file__'],'exec'),N)
N.update(ROOT=root,P=p,A=a,D=d);N['freeze_check'].__defaults__=(d,False);N['archive_check'].__defaults__=(d,)
enc=lambda x:json.dumps(x,indent=2)+'\n';sha=lambda b:hashlib.sha1(b).hexdigest();ctx=N['capture_inventory'](json.loads((d/'FREEZE.json').read_text())['operations_inventory_sha256']);accepted=json.loads((a/'ACCEPTANCE.json').read_text());freeze=json.loads((d/'FREEZE.json').read_text());originals=json.loads((O/'AUTHENTICATION_START.json').read_text())['originals'];HEAD=N['HEAD'];MERGE='b'*40;BEFORE='a'*40;MAIN=['c'*40];commits={};objects={};trees={};cases=[];calls=[];source_reads=[]
queue=json.loads((A/'reviews/full_package_05/AUTHENTICATION_START.json').read_text())['immutable_queue_row'].encode();catalog=json.dumps([x for x in json.loads((R/N['CATALOG']).read_text()) if str(x.get('id'))=='6000001']).encode();related=b'{"groups":[]}'
native_files={N['QUEUE']:queue,N['STATE']:b'{ "unrelated" : {"keep" : [1, 2]}, "6000001" : {"turns_used":0} }\n',N['HISTORY']:b'{"old" : "literal keep"}\n'}
def gitblob(b):h=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();objects[h]=b;return h
def initial_tree(files):
 child={k.rsplit('/',1)[1]:(b'100644',b'blob',gitblob(v).encode()) for k,v in files.items()};ch='d'*40;trees[ch]=child;trees[MAIN[0]]={b'unsolved_math_prioritization':(b'040000',b'tree',ch.encode())};trees[ch]={k.encode() if type(k)is str else k:v for k,v in child.items()};return MAIN[0]
initial_tree(native_files);commits[MAIN[0]]=copy.deepcopy(native_files);commits[MERGE]=copy.deepcopy(native_files);commits[BEFORE]=copy.deepcopy(native_files)
def blob(ref,name):
 if name in originals:return (a/'original'/name).read_bytes()
 if name==N['CATALOG']:source_reads.append(ref);return catalog
 if name==N['RELATED']:return related
 if name in native_files:return commits.get(ref,native_files)[name]
 raise RuntimeError('Unexpected fake blob '+name)
def flatten(tree,prefix=''):
 result={}
 for name,(mode,typ,oid) in trees[tree].items():
  path=prefix+name.decode()
  if typ==b'tree':result.update(flatten(oid.decode(),path+'/'))
  else:result[path]=objects[oid.decode()]
 return result
def run(argv,raw=False,**kw):
 if argv[:2]==['git','fetch']:return b'' if raw else ''
 if argv[:3]==['git','merge-base','--is-ancestor']:return ''
 if argv[:2]==['git','ls-tree']:
  ref=argv[2]
  if '-z' in argv:ref=argv[-1];return b''.join(b' '.join(v)+b'\t'+k+b'\0' for k,v in trees[ref].items())
  name=argv[-1]
  if name in originals:return '100644 blob '+originals[name]['git_blob']+'\t'+name+'\n'
  return '100644 blob '+gitblob(blob(ref,name))+'\t'+name+'\n'
 if argv[:2]==['git','show'] and '--format=%P' in argv:
  return BEFORE+' '+HEAD if argv[-1]==MERGE else commitparents[argv[-1]]
 if argv[:2]==['git','hash-object']:return gitblob(kw['input'].encode())+'\n'
 if argv[:2]==['git','mktree']:
  b=kw['input'];ident=sha(b);trees[ident]={}
  for line in b.split(b'\0'):
   if line:header,name=line.split(b'\t',1);trees[ident][name]=tuple(header.split(b' '))
  return (ident+'\n').encode() if raw else ident+'\n'
 if argv[:3]==['git','diff','--name-only']:
  before=commits[argv[3]];after=commits[argv[4]] if argv[4] in commits else flatten(argv[4]);return '\n'.join(k for k in before if before[k]!=after[k])+'\n'
 if argv[:2]==['git','commit-tree']:
  tree=argv[2];parent=argv[4];ident=sha((tree+parent).encode());commits[ident]=flatten(tree);commitparents[ident]=parent;trees[ident]=trees[tree];return ident+'\n'
 raise RuntimeError('Unexpected fake command '+repr(argv))
commitparents={};N.update(blob=blob,run=run,remote_main=lambda:MAIN[0]);current={'number':946,'state':'MERGED','isDraft':False,'baseRefName':'main','headRefOid':HEAD,'mergeCommit':{'oid':MERGE},'body':(d/'ORIGINAL_PR_DESCRIPTION.md').read_text(),'title':'original'};N['pr_view']=lambda:copy.deepcopy(current);N['save'](a/'PR_MERGE_RECEIPT.json',current)
descriptor,expected=N['descriptor_check'](freeze);stage={'environment':'production','title':descriptor['metadata']['title'],'files':expected,'id':123,'state':'ready_to_publish'};publication={**stage,'state':'published','doi':'10.5281/zenodo.123','record_url':'https://zenodo.org/records/123'}
# Captured kit bytes and stable runtime argument are checked at the subprocess boundary.
def kit(argv,**kw):
 assert kw['input']==ctx['captured'][N['KIT']];assert argv[1:4]==['-I','-S','-B'];action=argv[-2] if argv[-1].endswith('zenodo-deposit.json') else None
 args=argv[7:];action=args[0];manifest=Path(args[1]);assert manifest==a/'operations_runtime/zenodo-deposit.json'
 if action=='publish':assert args[2:]==['--confirm-id','123']
 if action=='inspect':assert args[2:]==['--check-doi']
 calls.append(['captured_kit',action]);return types.SimpleNamespace(returncode=0,stdout=json.dumps(stage if action=='stage' else publication).encode(),stderr=b'')
N['subprocess']=types.SimpleNamespace(run=kit)
def call(fn):
 with contextlib.redirect_stdout(io.StringIO()):return fn()
for action in ['stage','publish','inspect']:
 for path in d.glob('ZENODO_'+action.upper()+'*'):path.unlink()
 call(lambda:N['zenodo'](types.SimpleNamespace(action=action),ctx));cases.append({'case':'positive_actual_'+action+'_captured_kit_dispatch','pass':True})
# Actual tracker links, gid/header/quoted ranges, one append and dedup recovery.
table=[['Original Problem','Solution Chat URL','DOI','Notes']];append_count=[0]
def gws(argv):
 params=json.loads(argv[argv.index('--params')+1]);assert params['spreadsheetId']==N['SID']
 if argv[1:3]==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':1254632077,'title':'Math Puzzles'}}]}
 if argv[3]=='get':
  q=params['range'];return {'range':q,'values':copy.deepcopy(table if q=="'Math Puzzles'!A:D" else [table[-1]])}
 assert argv[3]=='append' and params['range']=="'Math Puzzles'!A:D";row=json.loads(argv[argv.index('--json')+1])['values'][0];assert len(row)==4;table.append(row);append_count[0]+=1;return {'updates':{'updatedRows':1,'updatedCells':4,'updatedRange':"'Math Puzzles'!A2:D2"}}
N['gws']=gws;(a/'TRACKER_APPEND_INTENT.json').unlink(missing_ok=True)
call(lambda:N['tracker_append'](types.SimpleNamespace(),ctx));call(lambda:N['tracker_append'](types.SimpleNamespace(),ctx));assert append_count[0]==1;cases.append({'case':'positive_actual_tracker_append_readback_dedup_recovery','pass':True,'append_count':1})
# Mutate only fake-service readbacks to test gid, headers, multirow and lost readback.
real_gws=N['gws']
for kind in ['gid','header','multiple_rows','row_content']:
 def corrupt(argv):
  result=copy.deepcopy(real_gws(argv))
  if kind=='gid' and 'sheets' in result:result['sheets'][0]['properties']['sheetId']=7
  elif kind=='header' and result.get('range')=="'Math Puzzles'!A:D":result['values'][0][0]='wrong'
  elif kind=='multiple_rows' and result.get('range')=="'Math Puzzles'!A2:D2":result['values'].append(result['values'][0])
  elif kind=='row_content' and result.get('range')=="'Math Puzzles'!A2:D2":result['values'][0][3]='wrong'
  return result
 N['gws']=corrupt
 try:call(lambda:N['tracker_append'](types.SimpleNamespace(),ctx))
 except RuntimeError as ex:cases.append({'case':'tracker_'+kind,'rejected':True,'reason':str(ex)})
 else:raise RuntimeError('tracker accepted '+kind)
N['gws']=real_gws;call(lambda:N['tracker_append'](types.SimpleNamespace(),ctx))
# Native real tree construction, one explicit non-fast-forward then fresh parent CAS.
(a/'NATIVE_PUBLICATION_RECEIPT.json').unlink(missing_ok=True)
for path in a.glob('NATIVE_PUBLICATION_CAS_*'):path.unlink()
pushes=[]
def push(argv,**kw):
 assert argv[:3]==['git','push','origin'];ident=argv[3].split(':')[0];pushes.append(ident)
 if len(pushes)==1:
  old=MAIN[0];MAIN[0]='9'*40;commits[MAIN[0]]=copy.deepcopy(commits[old]);trees[MAIN[0]]=trees[old];return types.SimpleNamespace(returncode=1,stdout='',stderr='non-fast-forward')
 MAIN[0]=ident;return types.SimpleNamespace(returncode=0,stdout='fake',stderr='')
N['subprocess'].run=push;call(lambda:N['native_write'](types.SimpleNamespace(),ctx));assert len(pushes)==2
native=json.loads((a/'NATIVE_PUBLICATION_RECEIPT.json').read_text());tracker=json.loads((a/'TRACKER_RECEIPT.json').read_text());N['native_verify'](publication,current,tracker,accepted,native);assert len(set(source_reads))>=2;cases.append({'case':'positive_actual_native_tree_CAS_retry_ancestry_literal_bytes_verify','pass':True,'push_count':2,'source_parent_reads':source_reads})
# Final metadata mutation, exact readback, local completion and already-finalized recovery.
(p/'CURRENT_STATE.json').write_text(enc({'active_pr':946,'active_problem_id':'6000001','eligible_prs':[946],'completed_prs':[],'completed_results':[],'portable_release_tooling':'retired'}));(p/'inventory.json').write_text(enc([{'number':946}]))
for name in [p/'README.md',p/'RESEARCH_LOG.md',a/'RESEARCH_LOG.md']:name.write_text('Synthetic fixture.\n')
def edit(argv,**kw):
 assert argv[:3]==['gh','pr','edit'];current['title']=argv[argv.index('--title')+1];current['body']=Path(argv[argv.index('--body-file')+1]).read_text();calls.append(['gh','pr','edit']);return types.SimpleNamespace(returncode=0,stdout='fake',stderr='')
N['subprocess'].run=edit;(a/'PR_FINAL_METADATA_INTENT.json').unlink(missing_ok=True)
call(lambda:N['finalize'](types.SimpleNamespace(),ctx));state=json.loads((p/'CURRENT_STATE.json').read_text());assert state['completed_prs']==[946] and state['active_pr'] is None and 'portable_release_tooling' not in state
call(lambda:N['finalize'](types.SimpleNamespace(),ctx));assert calls.count(['gh','pr','edit'])==1;cases.append({'case':'positive_full_actual_finalize_metadata_readback_completion_and_repeat','pass':True,'metadata_edit_count':1})
# Exact late sealed-review mutations: guard returns, while a fresh entry rejects.
actual_review=N['review_check']
for kind,name in [('payload','FULL_AUDIT.md'),('seal','MANIFEST.json')]:
 path=a/'reviews/full_package_08'/name;old=path.read_bytes();fired=[False]
 def drift(*args,**kw):
  value=actual_review(*args,**kw)
  if not fired[0]:fired[0]=True;path.write_bytes(old+b'\n')
  return value
 N['review_check']=drift;error=None
 try:call(lambda:N['accepted_review_check'](accepted,freeze,ctx))
 except RuntimeError as caught:error=str(caught)
 finally:N['review_check']=actual_review
 assert fired[0] and error is not None,error
 try:call(lambda:N['accepted_package'](ctx))
 except RuntimeError as ex:cases.append({'case':'late_review_'+kind+'_rejected_by_shared_guard_and_fresh_entry','rejected_by_closing_guard':True,'closing_error':error,'fresh_entry_error':str(ex)})
 else:raise RuntimeError('late drift did not invalidate new entry')
 path.write_bytes(old)
(O/'SERVICE_BOUNDARIES.json').write_text(enc({'status':'PASS','candidate_revision':6,'actual_current08_context':True,'real_control_flow':['zenodo','publication_links','tracker_append','explicit_tree','native_write','native_verify','finalize','all_shared_guards'],'fake_services_and_inmemory_Git_only':True,'terminal_review_synthetic':True,'cases':cases,'calls':calls,'actual_external_mutations':0}));print(json.dumps({'status':'PASS','cases':len(cases),'external_mutations':0}))
