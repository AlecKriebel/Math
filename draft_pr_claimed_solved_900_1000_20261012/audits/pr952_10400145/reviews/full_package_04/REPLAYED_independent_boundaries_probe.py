"""Actual merge, final metadata, and later filename/status-only functions; inert I/O."""
import argparse,contextlib,copy,hashlib,io,json,pathlib,sys,types
P=pathlib.Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012');A=P/'audits/pr952_10400145';R=A/'reviews/full_package_04/private/flows'
def need(x,m):
 if not x:raise RuntimeError(m)
raw=(P/'accept_pr952.py').read_bytes();need(hashlib.sha256(raw).hexdigest()=='14ac4e7009a1f4973f81aed776d5c6afd344dea93ff369dd65175427e0492eec','core pin')
n={'__name__':'own_inert_boundaries','__file__':str(P/'accept_pr952.py')};exec(compile(raw,str(P/'accept_pr952.py'),'exec',dont_inherit=True,optimize=sys.flags.optimize),n)
w=R/('private_boundary_'+str(sys.flags.optimize));w.mkdir();n['W']=w;n['READ_ONLY']=True;events=[];calls=[]
def yes(label,f):v=f();events.append({'test':label,'status':'PASS'});return v
def no(label,f):
 try:f()
 except Exception as e:events.append({'test':label,'status':'REJECTED_EXPECTED','guard':str(e)});return
 raise RuntimeError('ADVERSE ACCEPTED '+label)
def forbidden(*a,**k):raise RuntimeError('REAL I/O FORBIDDEN')
n['run']=forbidden;n['subprocess']=types.SimpleNamespace(run=forbidden);n['gws']=forbidden;n['bounded_public_get']=forbidden
pr={'number':952,'state':'MERGED','isDraft':False,'headRefOid':n['HEAD'],'headRefName':'inert','baseRefName':'main','url':'https://github.com/AlecKriebel/Math/pull/952','mergeCommit':{'oid':'b'*40},'mergedAt':'2026-10-16T00:00:00Z','currentBaseRefOid':'c'*40}
n['save'](w/'PR_MERGE_RECEIPT.json',pr);n['pr_view']=lambda *a:copy.deepcopy(pr);n['remote_main']=lambda:'c'*40
q=b'P\n| 10400145 / AMR-103-0145 | b | c | d | e | f | g | claimed_solved | 1/5 | j | note | link |\nS\n'
n['blob']=lambda ref,path: q if path==n['QUEUE'] else b'{}' if path==n['STATE'] else b'' if path==n['HISTORY'] else (_ for _ in ()).throw(RuntimeError('unexpected blob'))
n['source_gate']=lambda p:{'inert_source_boundary':p};n['original_check']=lambda *a:{'separately_authenticated_33':True}
cfg={'parents':'a'*40+' '+n['HEAD']}
def run(args,**kwargs):
 calls.append(args)
 if args[:3]==['git','merge-base','--is-ancestor']:return ''
 if args[:4]==['git','show','-s','--format=%P']:return cfg['parents']
 raise RuntimeError('unexpected inert command '+repr(args))
n['run']=run
yes('actual_merged_gate_two_parent_exact_head',lambda:n['merged_gate']({},{}))
for label,parents in [('squash','a'*40),('wrong_second_head','a'*40+' '+'d'*40),('octopus','a'*40+' '+n['HEAD']+' '+'d'*40)]:
 cfg['parents']=parents;no('actual_merged_gate_rejects_'+label,lambda:n['merged_gate']({},{}))
cfg['parents']='a'*40+' '+n['HEAD']
freeze=json.loads((A/'preprint/FREEZE.json').read_bytes());accepted={'freeze_sha256':'ab027971f0245481783e2afa106292543c41f06a93c3c83a0cf8dcea4cff9d77','full_package_reviews':[{},{}]}
pr.update(title='inert original title',body=(A/'PR_DESCRIPTION_ANCHOR.md').read_text());n['merged_gate']=lambda *a:{'inert_merged_boundary':True};n['accepted_review_check']=lambda *a:None
mutations=[];publication={'doi':'10.5281/zenodo.17','record_url':'https://zenodo.org/records/17'};tracker={'updated_range':"'Math Puzzles'!A2:D2"}
def metadata_action(args,**kwargs):
 need(args[:3]==['gh','pr','edit'],'unexpected mutation');mutations.append(args);pr['title']=args[args.index('--title')+1];pr['body']=pathlib.Path(args[args.index('--body-file')+1]).read_text();raise RuntimeError('INERT_METADATA_APPLIED_RESPONSE_LOST')
n['subprocess']=types.SimpleNamespace(run=metadata_action)
no('actual_final_metadata_response_lost_after_apply',lambda:n['finalize_pr_metadata'](accepted,freeze,publication,pr,tracker,{}))
yes('actual_final_metadata_exact_readback_recovery_no_second_edit',lambda:n['finalize_pr_metadata'](accepted,freeze,publication,pr,tracker,{}));need(len(mutations)==1,'metadata duplicate mutation')
pr['body']+='INERT_DRIFT';no('actual_final_metadata_conflicting_body_rejected',lambda:n['finalize_pr_metadata'](accepted,freeze,publication,pr,tracker,{}));need(len(mutations)==1,'conflicting metadata edit reached service')
# Later PR control runs actual full filename pages and actual immutable QUEUE fetch.
def nextpr(number,state='OPEN',draft=True):
 return {'number':number,'state':state,'isDraft':draft,'headRefOid':str(number%10)*40,'headRefName':'inert','baseRefName':'main','baseRefOid':'1'*40,'currentBaseRefOid':'c'*40,'url':f'https://github.com/AlecKriebel/Math/pull/{number}'}
nexts={953:nextpr(953),954:nextpr(954,'CLOSED'),955:nextpr(955)};reads=[];mode={'drift':False,'ambiguous':False,'bad_size':False}
n['pr_view']=lambda number:copy.deepcopy(nexts[number])
def later_run(args,**kwargs):
 need(args[:3]==['gh','api','graphql'],'non-GraphQL later operation');query=next(x[6:] for x in args if x.startswith('query='))
 if 'pullRequest(number:' in query:
  num=int(next(x.split('=',1)[1] for x in args if x.startswith('number=')));before=nexts[num];key='200'+str(num)
  paths=[n['QUEUE'],'unsolved_math_prioritization/attempts/'+key+'/PROOF_AND_STATUS.md']
  if mode['ambiguous']:paths.append('unsolved_math_prioritization/attempts/99999/another.md')
  node={k:v for k,v in before.items() if k!='currentBaseRefOid'};node.update(baseRef={'name':'main','target':{'oid':'d'*40 if mode['drift'] else 'c'*40}},changedFiles=len(paths),files={'nodes':[{'path':p} for p in paths],'pageInfo':{'hasNextPage':False,'endCursor':None}});reads.append(('filenames',num,paths));return json.dumps({'data':{'repository':{'pullRequest':node}}})
 expr=next(x[5:] for x in args if x.startswith('expr='));need(expr.endswith(':'+n['QUEUE']),'later mathematical body read');num=953 if expr.startswith('3'*40) else 955;key='200'+str(num);status='blocked' if num==953 else 'claimed_solved';queue=f'| {key} / AMR | b | c | d | e | f | g | {status} | 1/5 | j | note | link |\n';reads.append(('queue_only',num));return json.dumps({'data':{'repository':{'object':{'text':queue,'isBinary':False,'byteSize':True if mode['bad_size'] else len(queue.encode()),'oid':'f'*40}}}})
n['run']=later_run;n['blob']=forbidden
skipped,selected=yes('actual_later_closed_and_nonclaim_skip_then_claimed_selection',lambda:n['gate_next']([{'number':x} for x in [953,954,955]]))
need(selected['number']==955 and selected['math_source_read'] is False and len(skipped)==2 and all(r[1]!=954 for r in reads),'later exclusion/selection incorrect')
for key in ['drift','ambiguous','bad_size']:
 mode[key]=True;no('actual_later_rejects_'+key,lambda:n['gate_next']([{'number':953}]));mode[key]=False
need(all(r[0] in ['filenames','queue_only'] for r in reads),'later math/source read')
print(json.dumps({'status':'PASS_INDEPENDENT_ACTUAL_BOUNDARIES','outer_optimization':sys.flags.optimize,'core_compile_optimize':sys.flags.optimize,'events':events,'event_count':len(events),'inert_metadata_edit_count':len(mutations),'later_read_classes':sorted({r[0] for r in reads}),'scope':'Actual merged_gate/native_safety, finalize_pr_metadata, gate_next/next_identity/complete_changed_paths. Explicit synthetic acceptance, source/original and service/Git boundaries, no real mutation. Source/original guards are independently exercised in other suites and full authentication.'},sort_keys=True))
