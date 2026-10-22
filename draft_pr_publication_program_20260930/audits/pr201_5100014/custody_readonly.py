from pathlib import Path
import importlib.util,json,hashlib,base64,datetime
A=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr201_5100014");P=A.parent.parent
s=importlib.util.spec_from_file_location('completed200',P/'audits/pr200_5100007/publication_lifecycle_01/finish200.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v);c,h,rv,n=v.load();h.m.TREE_CACHE_PATH=A/'PRIVATE_ORIGINAL_TREE_CACHE.json'
HEAD='90bdb85235979f2ffa7496b9b689036654e55200';NATIVE='unsolved_math_prioritization/attempts/5100014/';Q='unsolved_math_prioritization/QUEUE.md'
i=json.loads((A/'ORIGINAL_STATUS_INTAKE.json').read_bytes());assert i['eligible'] and i['original_QUEUE_status']=='claimed_solved' and i['original_submitted_head']==HEAD
pr=h.api('pulls/201');assert pr['head']['sha']==HEAD and pr['state']=='open' and pr['draft'] and not pr['merged'] and pr['created_at']==pr['updated_at']==i['created_at']
co=h.api('git/commits/'+HEAD);assert co['tree']['sha']==i['head_tree'] and [x['sha'] for x in co['parents']]==[i['head_sole_parent']]
node=h.lookup(co['tree']['sha'],NATIVE.rstrip('/'));assert node and node[1]=='tree'
leaves={}
def walk(sha,prefix):
 for x in h.api('git/trees/'+sha)['tree']:
  name=x['path'];assert '/' not in name and name not in ['.','..']
  k=prefix+name
  if x['type']=='tree':walk(x['sha'],k+'/')
  else:
   assert x['type']=='blob' and x['mode']=='100644',x
   j=h.api('git/blobs/'+x['sha']);assert j['encoding']=='base64'
   b=base64.b64decode(j['content'],validate=False);assert len(b)==j['size'] and c.byte_pin(b)['git_blob']==x['sha']
   leaves[k]=(b,x)
walk(node[2],'')
base=h.api('git/commits/'+i['original_range_base'])['tree']['sha']
changed=h.changed_leaves(base,co['tree']['sha'])
assert changed=={NATIVE+k for k in leaves}|{Q},changed
oldq=h.body_at(Q,i['original_range_base']);newq=h.body_at(Q,HEAD);assert c.byte_pin(newq)==i['original_QUEUE_blob']
oldlines=oldq.splitlines(keepends=True);newlines=newq.splitlines(keepends=True);assert len(oldlines)==len(newlines)
different=[(x,y) for x,y in zip(oldlines,newlines) if x!=y];assert len(different)==1 and b'| 5100014 / ' in different[0][0] and b'| 5100014 / ' in different[0][1]
assert v.m.pin(different[0][1])==i['original_QUEUE_row']
pins={}
for k,(b,x) in leaves.items():
 f=A/'original_submitted_head'/k;f.parent.mkdir(parents=True,exist_ok=True)
 if f.exists():assert f.read_bytes()==b
 else:
  with f.open('xb') as out:out.write(b)
 f.chmod(0o444);pins[k]=c.byte_pin(b)|{'mode':x['mode']}
meta={k:pr[k] for k in ['number','title','body','state','draft','merged','created_at','updated_at','commits','changed_files']};meta['original_head']=HEAD;v.m.save(A/'ORIGINAL_PR_METADATA.json',v.m.enc(meta))
r={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':201,'problem_id':5100014,'original_head':HEAD,'original_tree':co['tree']['sha'],'original_sole_parent':co['parents'][0]['sha'],'original_QUEUE_status':'claimed_solved','original_QUEUE_effort_cell':i['original_QUEUE_effort_cell'],'files':pins,'file_count':len(pins),'total_native_bytes':sum(len(b) for b,x in leaves.values()),'complete_original_delta':sorted(changed),'complete_delta_is_exact_native_archive_plus_one_QUEUE_row':True,'foreign_QUEUE_rows_unchanged_at_original_submission':True,'original_QUEUE_blob':c.byte_pin(newq),'original_QUEUE_row':v.m.pin(different[0][1]),'original_PR_metadata':v.m.pin((A/'ORIGINAL_PR_METADATA.json').read_bytes()),'source_and_mathematical_clearance':False,'no_PR_or_native_MAIN_mutation':True,'custody_before_semantic_candidate_review':True}
v.m.save(A/'ORIGINAL_SUBMISSION_CUSTODY.json',v.m.enc(r))
print(json.dumps({k:r[k] for k in ['UTC','PR','original_head','file_count','total_native_bytes','complete_original_delta','complete_delta_is_exact_native_archive_plus_one_QUEUE_row']}))
