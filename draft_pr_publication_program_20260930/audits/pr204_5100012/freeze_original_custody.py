"""Authenticate original PR204 tree, complete delta, QUEUE row and all blobs before semantics."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import base64,datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;P=A.parent.parent
I=P/'ordered_intakes_after_PR203_20261016/PR204_ORIGINAL_STATUS_INTAKE.json'
HEAD='551a524e2db65fec90684485ef676d0b4179378d';NATIVE='unsolved_math_prioritization/attempts/5100012/';Q='unsolved_math_prioritization/QUEUE.md'
TREES={}
def require(c,msg):
 if not c:raise RuntimeError(msg)
def pin(b):
 return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def enc(j):return (json.dumps(j,indent=2)+'\n').encode()
def api(path):
 r=subprocess.run(['gh','api','repos/AlecKriebel/Math/'+path],capture_output=True)
 require(r.returncode==0,'Authenticated read failed '+path)
 return json.loads(r.stdout)
def save(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 p.chmod(0o444)
def tree(sha):
 if sha in TREES:return TREES[sha]
 j=api('git/trees/'+sha);require(j['sha']==sha and not j['truncated'],'tree identity/truncation')
 raw=b''.join(x['mode'].lstrip('0').encode()+b' '+x['path'].encode()+b'\0'+bytes.fromhex(x['sha']) for x in sorted(j['tree'],key=lambda x:x['path'].encode()+(b'/' if x['type']=='tree' else b'')))
 require(hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==sha,'native tree SHA')
 TREES[sha]=j;return j
def lookup(root,path):
 t=root
 for index,name in enumerate(path.split('/')):
  xs=[x for x in tree(t)['tree'] if x['path']==name];require(len(xs)==1,'missing/ambiguous '+path);x=xs[0]
  if index==len(path.split('/'))-1:return x
  require(x['type']=='tree','non-directory');t=x['sha']
def walk(root,prefix=''):
 out={}
 for x in tree(root)['tree']:
  rel=prefix+x['path']
  if x['type']=='tree':out.update(walk(x['sha'],rel+'/'))
  else:require(x['type']=='blob' and x['mode']=='100644','nonregular original');out[rel]=x
 return out
def delta(a,b,prefix=''):
 if a==b:return []
 left={x['path']:x for x in tree(a)['tree']} if a else {};right={x['path']:x for x in tree(b)['tree']} if b else {};out=[]
 for name in sorted(left.keys()|right.keys()):
  x=left.get(name);y=right.get(name)
  if x==y:continue
  if (x is None or x['type']=='tree') and (y is None or y['type']=='tree'):out+=delta(x['sha'] if x else None,y['sha'] if y else None,prefix+name+'/')
  else:require((x is None or x['type']=='blob') and (y is None or y['type']=='blob'),'type-change');out.append(prefix+name)
 return out
def blob(x):
 j=api('git/blobs/'+x['sha']);require(j['encoding']=='base64','blob encoding');b=base64.b64decode(j['content'])
 require(j['sha']==pin(b)['git_blob']==x['sha'] and j['size']==len(b),'native blob identity')
 if 'size' in x:require(x['size']==len(b),'blob tree size')
 return b
def main():
 intake=I.read_bytes();i=json.loads(intake)
 require(pin(intake)['sha256']=='508788878ec0fb4b42c791813a28a53a400d70359bd0ab1411d378fac618862d','intake pin')
 require(i['eligible'] and i['original_QUEUE_status']=='claimed_solved' and i['PR']==204 and i['problem_id']==5100012 and i['original_submitted_head']==HEAD,'eligibility')
 pr=api('pulls/204');co=api('git/commits/'+HEAD);base=api('git/commits/'+i['original_range_base'])
 require(pr['head']['sha']==HEAD and pr['state']=='open' and pr['draft'] and not pr['merged'] and pr['created_at']==pr['updated_at']==i['created_at'],'original PR unchanged')
 require(co['tree']['sha']==i['head_tree'] and [x['sha'] for x in co['parents']]==[i['head_sole_parent']],'original commit containment')
 require(pr['commits']==i['original_author_commit_count']==2,'original chain count')
 meta=lookup(co['tree']['sha'],NATIVE.rstrip('/'));require(meta['type']=='tree','native root')
 files=walk(meta['sha']);changes=delta(base['tree']['sha'],co['tree']['sha'])
 require(set(changes)=={Q}|{NATIVE+n for n in files},'complete original delta contains foreign path')
 qb=blob(lookup(base['tree']['sha'],Q));qn=blob(lookup(co['tree']['sha'],Q));require(pin(qn)==i['original_QUEUE_blob'],'original QUEUE blob intake')
 old=qb.splitlines(keepends=True);new=qn.splitlines(keepends=True);require(len(old)==len(new),'QUEUE shape')
 ix=[k for k,(x,y) in enumerate(zip(old,new)) if x!=y];require(len(ix)==1,'foreign QUEUE changes')
 k=ix[0];require(b'| 5100012 / AMR-050-0012 |' in old[k] and b'| 5100012 / AMR-050-0012 |' in new[k],'own QUEUE identity')
 require({z:pin(new[k])[z] for z in ['bytes','sha256']}==i['original_QUEUE_row'],'original row intake')
 require(old[k].decode().split('|')[8].strip()=='queued' and old[k].decode().split('|')[9].strip()=='0/5','original base row')
 require(new[k].decode().split('|')[8].strip()=='claimed_solved' and new[k].decode().split('|')[9].strip()=='1/5','original outcome row')
 with ThreadPoolExecutor(max_workers=4) as pool:bodies=dict(zip(files,pool.map(blob,files.values())))
 current=api('pulls/204');require(current['head']['sha']==HEAD and current['state']=='open' and current['draft'] and current['created_at']==current['updated_at']==i['created_at'],'end custody race')
 save(A/'ORIGINAL_STATUS_INTAKE.json',intake);pins={}
 for rel,b in bodies.items():
  require(not Path(rel).is_absolute() and '..' not in Path(rel).parts,'unsafe path')
  save(A/'original_submitted_head'/rel,b);pins[rel]={**pin(b),'mode':'100644'}
 meta={k:pr[k] for k in ['number','title','body','state','draft','merged','created_at','updated_at','commits','changed_files']};meta['original_head']=HEAD
 save(A/'ORIGINAL_PR_METADATA.json',enc(meta))
 save(A/'original_git_metadata/ORIGINAL_COMMIT.json',enc(co));save(A/'original_git_metadata/RANGE_BASE_COMMIT.json',enc(base))
 save(A/'original_git_metadata/ALL_AUTHENTICATED_NONRECURSIVE_TREES.json',enc(TREES))
 qr={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'range_base':i['original_range_base'],'original_head':HEAD,'base_QUEUE_blob':pin(qb),'original_QUEUE_blob':pin(qn),'base_own_row':{**pin(old[k]),'text':old[k].decode()},'original_QUEUE_row':{**pin(new[k]),'text':new[k].decode()},'one_based_row':k+1,'foreign_QUEUE_rows_identical':True,'own_only_changed_row':True,'all_queue_bytes_retrievable_by_immutable_native_blob_ID':True}
 save(A/'ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json',enc(qr))
 r={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':204,'problem_id':5100012,'original_head':HEAD,'original_tree':co['tree']['sha'],'original_sole_parent':co['parents'][0]['sha'],'original_range_base':i['original_range_base'],'original_author_commit_count':2,'original_QUEUE_status':'claimed_solved','original_QUEUE_effort_cell':'1/5','files':pins,'file_count':len(pins),'total_native_bytes':sum(len(b) for b in bodies.values()),'complete_original_delta':changes,'complete_delta_is_exact_native_archive_plus_one_QUEUE_row':True,'foreign_QUEUE_rows_unchanged_at_original_submission':True,'original_QUEUE_blob':pin(qn),'original_QUEUE_row':{z:pin(new[k])[z] for z in ['bytes','sha256']},'original_PR_metadata':{z:pin((A/'ORIGINAL_PR_METADATA.json').read_bytes())[z] for z in ['bytes','sha256']},'authenticated_nonrecursive_trees':len(TREES),'all_nonrecursive_Git_tree_native_identities_verified':True,'all_blob_native_identities_and_bytes_verified':True,'source_and_mathematical_clearance':False,'no_PR_or_native_MAIN_mutation':True,'custody_before_semantic_candidate_review':True,'transport':'Authenticated read-only GitHub native Git trees/blobs; native tree and blob SHA1 plus byte lengths and SHA256 recomputed. No local Git/index/ref/branch/checkout command.'}
 save(A/'ORIGINAL_SUBMISSION_CUSTODY.json',enc(r))
 save(A/'RESEARCH_LOG.md',('# PR204 /5100012 audit\n\n'+r['UTC']+' — Originalclaimed_solved1/5 eligibility and complete authenticated custody accepted. Case estimate10%; source contract, mathematical audit and all publication/integration work pending. No semantic proof evaluation, novelty acceptance or publication performed.\n').encode())
 print(json.dumps({k:r[k] for k in ['UTC','PR','original_head','file_count','total_native_bytes','authenticated_nonrecursive_trees','complete_delta_is_exact_native_archive_plus_one_QUEUE_row','source_and_mathematical_clearance']}))
if __name__=='__main__':main()

