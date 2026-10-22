import ast,copy,hashlib,importlib.util,json,sys,types
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parents[3];A=R.parents[1];rows=[];sys.dont_write_bytecode=True

def mod(name):
 spec=importlib.util.spec_from_file_location('review05extra_'+name,P/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def need(x,s):
 if not x:raise RuntimeError(s)
def expect(label,call,fragment):
 try:call()
 except RuntimeError as e:need(fragment in str(e),label+' wrong reason '+str(e));rows.append({'case':label,'rejected':True});return
 raise RuntimeError(label+' accepted')
# Execute exact append/recovery/readback statements with local mocked gws only.
m=mod('append_pr938_tracker');fn=next(n for n in ast.parse((P/'append_pr938_tracker.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='main');block=[];on=False
for n in fn.body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='hits' for t in n.targets):on=True
 if on:
  if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='print':break
  block.append(n)
code=compile(ast.fix_missing_locations(ast.Module(body=block,type_ignores=[])),'review05_actual_tracker_append_recovery','exec')
row=['primary','','https://doi.org/10.5281/zenodo.123','SYNTHETIC only'];doi='10.5281/zenodo.123'
for recovery in [False,True]:
 for returned in ["'Math Puzzles'!A2:D2","'Other tab'!A2:D2","'Math Puzzles'!A2:D3"]:
  if recovery and returned!="'Math Puzzles'!A2:D2":continue
  for wrong_rb in [False,True]:
   writes=[];calls=[]
   def gws(args):
    calls.append(args)
    if args[3]=='append':return {'updates':{'updatedRange':returned,'updatedRows':1,'updatedCells':4}}
    return {'range':"'Math Puzzles'!A3:D3" if wrong_rb else returned,'values':[row]}
   existing={'values':[['Original Problem','Solution Chat URL','DOI','Notes']]+([row] if recovery else [])}
   ns=dict(m.__dict__,row=row,doi=doi,existing=existing,target={'title':'Math Puzzles'},table="'Math Puzzles'!A:D",publication={'id':123},merge={'headRefOid':'a'*40,'mergeCommit':{'oid':'b'*40}},acceptance={'original_pr_head':'a'*40,'freeze_sha256':'0'*64},gws=gws,save=lambda n,v:writes.append(n))
   label='actual_tracker_'+str(recovery)+'_'+returned+'_'+str(wrong_rb)
   if returned=="'Math Puzzles'!A2:D2" and not wrong_rb:exec(code,ns);need('TRACKER_RECEIPT.json' in writes,'valid receipt absent');rows.append({'case':label,'passed':True});need(not recovery or all(c[3]!='append' for c in calls),'duplicate append')
   else:expect(label,lambda:exec(code,ns),'range' if returned!="'Math Puzzles'!A2:D2" else 'exact readback')
# Real merge helper's already-MERGED interpretation guard sequence (no action path).
m=mod('merge_pr938');D=A/'publication';body=(A/'PR_DESCRIPTION_CORRECTED.md').read_text();freeze=json.loads((D/'PREPUBLICATION_FREEZE.json').read_text())
for base in ['main',None,'other']:
 for changed in [False,True]:
  pr={'state':'MERGED','headRefOid':m.HEAD,'baseRefName':base,'body':body+'drift' if changed else body}
  def call():m.require_main_destination(pr);m.require(pr['headRefOid']==m.HEAD,'head');m.require_reviewed_description(pr,freeze)
  if base=='main' and not changed:call();rows.append({'case':'already_MERGED_exact_main_body','passed':True})
  else:expect('already_MERGED_'+str(base)+'_'+str(changed),call,'destination' if base!='main' else 'description')
expect('already_MERGED_missing_body',lambda:m.require_reviewed_description({'state':'MERGED','baseRefName':'main'},freeze),'description')
# Actual explicit native tree routine with a tiny fully mocked Git object store.
lm=mod('update_pr938_publication_ledger');objects={};trees={};writes=[]
def oid(kind,b):return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def puttree(entries):
 payload=b''.join(mode+b' '+kind+b' '+obj.encode()+b'\t'+name+b'\0' for name,(mode,kind,obj) in sorted(entries.items()));key=oid('mocktree',payload);trees[key]=entries;return key
oldblobs={n:oid('blob',n.encode()) for n in ['queue','state','history','other','nested']};inner=puttree({b'QUEUE.md':(b'100644',b'blob',oldblobs['queue']),b'state.json':(b'100644',b'blob',oldblobs['state']),b'history.jsonl':(b'100644',b'blob',oldblobs['history']),b'UNCHANGED':(b'100644',b'blob',oldblobs['nested'])});outer=puttree({b'unsolved_math_prioritization':(b'040000',b'tree',inner),b'UNRELATED':(b'100644',b'blob',oldblobs['other'])})
def run(args,**kwargs):
 writes.append(args)
 if args[:2]==['git','hash-object']:
  b=kwargs['input'].encode();key=oid('blob',b);objects[key]=b;return key
 if args[:2]==['git','ls-tree']:return '100644 blob '+oldblobs['queue']+'\tfixture'
 raise RuntimeError('Unmocked Git call '+repr(args))
def sub(args,**kwargs):
 writes.append(args)
 if args[:2]==['git','ls-tree']:
  entries=trees[args[-1]];return types.SimpleNamespace(stdout=b''.join(mode+b' '+kind+b' '+obj.encode()+b'\t'+name+b'\0' for name,(mode,kind,obj) in entries.items()))
 if args[:2]==['git','mktree']:
  entries={}
  for r in kwargs['input'].split(b'\0'):
   if r:
    header,name=r.split(b'\t');mode,kind,obj=header.split();entries[name]=(mode,kind,obj.decode())
  return types.SimpleNamespace(stdout=(puttree(entries)+'\n').encode())
 raise RuntimeError('Unmocked subprocess '+repr(args))
lm.run=run;lm.subprocess=types.SimpleNamespace(run=sub);replacements={'unsolved_math_prioritization/QUEUE.md':'newq','unsolved_math_prioritization/state.json':'news','unsolved_math_prioritization/history.jsonl':'newh'};new=lm.explicit_tree(outer,replacements)
need(trees[new][b'UNRELATED']==trees[outer][b'UNRELATED'],'unrelated root entry changed');newinner=trees[trees[new][b'unsolved_math_prioritization'][2]];need(newinner[b'UNCHANGED']==trees[inner][b'UNCHANGED'],'unrelated native entry changed');need(len(objects)==3 and all('index' not in str(x) and 'checkout' not in str(x) and 'update-ref' not in str(x) for x in writes),'shared state operation');rows.append({'case':'actual_explicit_three_path_tree_preserves_other_entries','passed':True,'Git_calls_fully_mocked':True})
# Actual push-failure retry classifier only: unrelated errors never treated as races.
tree=ast.parse((P/'update_pr938_publication_ledger.py').read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');loop=next(n for n in fn.body if isinstance(n,ast.For));classifier=[];on=False
for n in loop.body:
 if isinstance(n,ast.Import) and any(x.name=='re' for x in n.names):on=True
 if on:classifier.append(n)
code=compile(ast.fix_missing_locations(ast.Module(body=classifier,type_ignores=[])),'review05_actual_push_failure_classifier','exec');parent='a'*40
for stderr,accepted in [('non-fast-forward',True),('fetch first',True),("cannot lock ref 'refs/heads/main': is at "+'b'*40+' but expected '+parent,True),("cannot lock ref 'refs/heads/main': is at "+'b'*40+' but expected '+('c'*40),False),('permission denied',False),('connection timeout; outcome uncertain',False)]:
 ns={'push':types.SimpleNamespace(stderr=stderr),'parent':parent}
 if accepted:exec(code,ns);rows.append({'case':'actual_retry_classifier_'+stderr,'classified_race':True})
 else:expect('actual_no_blind_retry_'+stderr,lambda:exec(code,ns),stderr)
result={'status':'PASS','cases':len(rows),'rows':rows,'real_service_or_Git_actions':0,'operational_mains_called':False};(R/'ADDITIONAL_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','cases':len(rows)}))
