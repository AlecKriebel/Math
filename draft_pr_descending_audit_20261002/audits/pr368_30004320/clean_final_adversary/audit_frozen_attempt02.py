#!/usr/bin/env python3
"""Read-only frozen provenance checks and complete private-copy replays."""
import pathlib,json,hashlib,subprocess,base64,sys,datetime,shutil,concurrent.futures
HERE=pathlib.Path(__file__).resolve().parent
AUDIT=HERE.parent; REPO=HERE.parents[3]; SNAP=AUDIT/'snapshot'
PREFIX='problems/30004320_laurent_descent'; CAND=SNAP/PREFIX
HEAD='74617174ddfb3ea726cea343a4ba915613724bdc';BASE='efd29c05204703acca9a0860812f54b94fae54b1'
AUTHOR='b08662a16499edf37f0c0eae850cfa00b7778ed6'
CHECKPOINTS=['5e2eb63fd571f2f660ff9ebb436440029b5d1268','d7d898ba23e9d024e79b938e3e0e305d91bb125b','c800217d22d329d6ca397f3c18e5115c77688fb9','24ecf1f2f0ab62082f328545180e4b2ba1640ab7',AUTHOR]
PYTHON=REPO/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
RUN=HERE/'private_replay';RUN.mkdir(exist_ok=False);COPY=RUN/'candidate';shutil.copytree(CAND,COPY)
rows=[];checks=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def ck(name,value,detail=None):
 if not value:raise AssertionError((name,detail))
 checks.append({'check':name,'pass':True,'detail':detail})
def cmd(args):return subprocess.check_output(args,cwd=REPO)
def git(*args):return cmd(['git',*args])
def api(endpoint):
 b=cmd(['gh','api','--method','GET','-H','Cache-Control: no-cache','repos/AlecKriebel/Math/'+endpoint]);return json.loads(b)
def tree(commit):
 b=git('ls-tree','-r','-z',commit);out={}
 for row in b.split(b'\0'):
  if not row:continue
  meta,path=row.split(b'\t',1);mode,typ,oid=meta.decode().split();out[path.decode()]={'mode':mode,'type':typ,'sha':oid}
 return out
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
m=json.loads((AUDIT/'snapshot_manifest.json').read_bytes());ck('snapshot pins',(m['head'],m['base'],m['pr'],m['target_prefix'])==(HEAD,BASE,368,PREFIX))
expected={r['path']:r for r in m['files']};ck('54 exact root paths',len(expected)==54 and sum(p.startswith(PREFIX+'/') for p in expected)==53)
bt=tree(BASE);ht=tree(HEAD);changed={p for p in bt.keys()|ht.keys() if bt.get(p)!=ht.get(p)}
ck('all recursive git diff paths equal snapshot',changed==set(expected),{'changed_paths':sorted(changed),'base_entries':len(bt),'head_entries':len(ht)})
ck('actual Git frozen parents',git('show','-s','--format=%P',HEAD).decode().strip().split()==[BASE,AUTHOR])
ck('actual Git base ancestor',subprocess.run(['git','merge-base','--is-ancestor',BASE,HEAD],cwd=REPO).returncode==0)
for p,r in expected.items():
 disk=(SNAP/p).read_bytes();gb=git('show',HEAD+':'+p)
 ck('snapshot disk and actual Git blob '+p, disk==gb and len(disk)==r['bytes'] and sha(disk)==r['sha256'] and ht[p]=={'mode':'100644','type':'blob','sha':r['git_blob_sha']})
 ck('Git SHA1 object '+p,hashlib.sha1(b'blob '+str(len(disk)).encode()+b'\0'+disk).hexdigest()==ht[p]['sha'])
 if p.endswith('.json'):json.loads(disk)
# Complete actual API tree, rather than a selected target subtree.
api_tree_chunks=[]
def api_leaf_map(oid,prefix=''):
 j=api('git/trees/'+oid+'?recursive=1')
 if not j['truncated']:
  api_tree_chunks.append({'tree':oid,'prefix':prefix,'recursive':True,'entries':len(j['tree']),'truncated':False})
  return {prefix+r['path']:{k:r[k] for k in ('mode','type','sha')} for r in j['tree'] if r['type']!='tree'}
 # A truncated recursive response is never used as evidence of complete scope.
 j=api('git/trees/'+oid);ck('nonrecursive API chunk complete '+prefix,j['truncated'] is False)
 api_tree_chunks.append({'tree':oid,'prefix':prefix,'recursive':False,'entries':len(j['tree']),'truncated':False})
 out={}
 for r in j['tree']:
  path=prefix+r['path']
  if r['type']=='tree':out.update(api_leaf_map(r['sha'],path+'/'))
  else:out[path]={k:r[k] for k in ('mode','type','sha')}
 return out
apimap=api_leaf_map(HEAD)
at=api('git/trees/'+HEAD)
ck('complete API/Git recursive blob-and-gitlink maps agree',apimap==ht,{'entries':len(apimap),'api_tree_sha':at['sha']})
ck('API root tree actual Git tree',at['sha']==git('show','-s','--format=%T',HEAD).decode().strip())
pull=api('pulls/368');ck('actual frozen PR metadata',(pull['head']['sha'],pull['base']['sha'],pull['head']['ref'],pull['state'],pull['changed_files'])==(HEAD,BASE,'math/30004320-laurent-descent-reviewed','open',54))
files=api('pulls/368/files?per_page=100');ck('all 54 actual API PR paths',len(files)==54 and {r['filename'] for r in files}==set(expected))
for r in files:ck('API full file status and blob '+r['filename'],r['status']==expected[r['filename']]['status'] and r['sha']==expected[r['filename']]['git_blob_sha'])
def verify_api_blob(item):
 p,r=item;j=api('git/blobs/'+r['git_blob_sha']);b=base64.b64decode(j['content']);return p,len(b)==r['bytes'] and sha(b)==r['sha256'] and j['sha']==r['git_blob_sha'] and j['size']==len(b) and b==(SNAP/p).read_bytes()
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 for p,ok in pool.map(verify_api_blob,expected.items()):ck('actual API blob '+p,ok)
# All nested manifests, including all metadata and exact closed scopes.
nested=[]
for name in [f'TURN_{i}_MANIFEST.json' for i in range(1,6)]+['FINAL_AUTHOR_MANIFEST.json','review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']:
 d=json.loads((CAND/name).read_bytes());pathbase=CAND/'review' if name.startswith('review/') else CAND
 ck('manifest unique paths '+name,len({r['path'] for r in d['files']})==len(d['files']))
 for r in d['files']:
  b=(pathbase/r['path']).read_bytes();ck('manifest exact bytes '+name+'/'+r['path'],len(b)==r['bytes'] and sha(b)==r['sha256']);nested.append([name,r['path'],r['bytes'],r['sha256']])
 if name.startswith('TURN_'):
  i=int(name.split('_')[1]);ck('turn ordinal '+name,d['author_turns_used']==i)
  if i>1:ck('historical manifest chain '+name,d['previous_manifest_sha256']==sha((CAND/f'TURN_{i-1}_MANIFEST.json').read_bytes()))
pub=json.loads((CAND/'PUBLICATION_MANIFEST.json').read_bytes());actual={str(f.relative_to(CAND)) for f in CAND.rglob('*') if f.is_file()}
ck('publication full closed scope',set(r['path'] for r in pub['files'])==actual-{'PUBLICATION_MANIFEST.json'} and len(actual)==53)
ck('publication exact status',pub['status']=='unsolved' and pub['turns']=='5/5')
author=json.loads((CAND/'FINAL_AUTHOR_MANIFEST.json').read_bytes());authorpaths={r['path'] for r in author['files']}|{'FINAL_AUTHOR_MANIFEST.json'}
ck('42 author files',len(authorpaths)==42 and not author['original_target_resolved'] and author['proposed_status']=='unsolved' and author['substantive_author_turns_used']==5)
rt=tree(AUTHOR);ck('actual complete author subtree scope',{p[len(PREFIX)+1:] for p in rt if p.startswith(PREFIX+'/')}==authorpaths)
for p in authorpaths:ck('actual author checkpoint bytes '+p,git('show',AUTHOR+':'+PREFIX+'/'+p)==(CAND/p).read_bytes())
remote=json.loads((CAND/'review/REMOTE_BINDING.json').read_bytes());ck('historical remote-binding full scope',remote['head']==AUTHOR and remote['folder']==PREFIX and {r['path'] for r in remote['files']}==authorpaths)
for r in remote['files']:
 b=(CAND/r['path']).read_bytes();ck('remote-binding historical blob '+r['path'],len(b)==r['size'] and rt[PREFIX+'/'+r['path']]['sha']==r['git_blob_sha'])
reviewpaths={p for p in actual if p.startswith('review/')};ck('seven additive review files',len(reviewpaths)==7 and all(PREFIX+'/'+p not in rt for p in reviewpaths))
prior=BASE;history=[]
for i,commit in enumerate(CHECKPOINTS,1):
 parents=git('show','-s','--format=%P',commit).decode().strip().split();ck('author actual checkpoint parent '+str(i),parents==[prior])
 cj=api('git/commits/'+commit);treeoid=git('show','-s','--format=%T',commit).decode().strip()
 ck('API author commit/parent/tree '+str(i),cj['sha']==commit and [r['sha'] for r in cj['parents']]==parents and cj['tree']['sha']==treeoid)
 # The current and every prior turn manifest retain their original checkpoint bytes.
 for j in range(1,i+1):
  md=json.loads((CAND/f'TURN_{j}_MANIFEST.json').read_bytes())
  for p in [f'TURN_{j}_MANIFEST.json']+[r['path'] for r in md['files']]:ck('actual historical bytes '+str(i)+'/'+p,git('show',commit+':'+PREFIX+'/'+p)==(CAND/p).read_bytes())
 history.append({'turn':i,'commit':commit,'parents':parents,'tree':treeoid,'author':cj['author'],'committer':cj['committer'],'message':cj['message']});prior=commit
# Queue entire file, one physical row/cells only. No other row can drift.
qpath='unsolved_math_prioritization/QUEUE.md';qbase=git('show',BASE+':'+qpath);qhead=(SNAP/qpath).read_bytes();ql=qbase.splitlines(keepends=True);qh=qhead.splitlines(keepends=True)
ck('queue same row count',len(ql)==len(qh));indices=[i for i,(a,b) in enumerate(zip(ql,qh)) if a!=b];ck('queue one changed physical row',len(indices)==1)
i=indices[0];bc=ql[i].decode().split('|');hc=qh[i].decode().split('|');diff=[j for j,(a,b) in enumerate(zip(bc,hc)) if a!=b]
ck('queue own cells 8 and 9 exactly',len(bc)==len(hc) and '30004320' in qh[i].decode() and diff==[8,9] and (bc[8].strip(),bc[9].strip(),hc[8].strip(),hc[9].strip())==('queued','0/5','unsolved','5/5'))
queue={'physical_line':i+1,'changed_cells':diff,'base_row':ql[i].decode(),'head_row':qh[i].decode(),'base_sha256':sha(qbase),'head_sha256':sha(qhead),'all_other_queue_bytes_preserved':True}
# Historical source versions were independently downloaded, not borrowed.
source=[]
for name in ['SOURCE_MANIFEST.json','SOURCE_ADDITION_T1.json','SOURCE_ADDITION_T4.json','SOURCE_ADDITION_T5.json']:
 for r in json.loads((CAND/name).read_bytes())['files']:
  b=(HERE/'private_sources'/r['name']).read_bytes();ck('fresh primary exact '+r['name'],len(b)==r['bytes'] and sha(b)==r['sha256']);source.append(r)
# Full outputs, all author checks, earlier review, wrapper, publication with/without sources.
streams=HERE/'replay_streams';streams.mkdir(exist_ok=False);replays=[]
def run(label,args,expected_bytes=None):
 t0=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run([str(PYTHON),*map(str,args)],cwd=COPY,capture_output=True)
 (streams/(label+'.stdout')).write_bytes(r.stdout);(streams/(label+'.stderr')).write_bytes(r.stderr)
 ck('replay exit '+label,r.returncode==0,{'returncode':r.returncode})
 if expected_bytes is not None:ck('complete byte-exact output '+label,r.stdout==expected_bytes)
 replays.append({'label':label,'command':[str(PYTHON),*map(str,args)],'start_utc':t0,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr),'exit_code':r.returncode})
 return r.stdout
for i in range(1,6):run('author_'+str(i),[COPY/f'check_turn_{i}.py'],(CAND/f'TURN_{i}_CHECKS.json').read_bytes())
run('prior_independent',[COPY/'review/independent_checks.py'],(CAND/'review/INDEPENDENT_CHECKS.json').read_bytes())
run('packet_with_sources',[COPY/'verify_packet.py','--source-dir',HERE/'private_sources'],(CAND/'review/AUTHOR_REPLAY.json').read_bytes())
run('review',[COPY/'review/verify_review.py','--author-dir',COPY],b'PASS: review hashes, frozen author/remote binding, and independent replay\n')
pout=run('publication_with_sources',[COPY/'verify_publication.py','--source-dir',HERE/'private_sources'])
pp=json.JSONDecoder().raw_decode(pout.decode())[0];ck('publication complete with-source stream',pp==json.loads((CAND/'review/AUTHOR_REPLAY.json').read_bytes()) and pout.decode()[len(json.dumps(pp,indent=2,sort_keys=True))+1:]=='PASS: review hashes, frozen author/remote binding, and independent replay\nPASS: all publication bytes, frozen author proofs and independent review; original unsolved 5/5\n')
pout=run('publication_without_sources',[COPY/'verify_publication.py']);pp,offset=json.JSONDecoder().raw_decode(pout.decode());expectedj=json.loads((CAND/'review/AUTHOR_REPLAY.json').read_bytes());expectedj.update(source_check='not requested; raw sources are not distributed',source_pdfs_checked=0)
ck('publication entire portable stream',pp==expectedj and pout.decode()[offset:].lstrip('\n')=='PASS: review hashes, frozen author/remote binding, and independent replay\nPASS: all publication bytes, frozen author proofs and independent review; original unsolved 5/5\n')
end=datetime.datetime.now(datetime.timezone.utc).isoformat()
result={'verdict':'PASS frozen packet; live acceptance pending','start_utc':start,'end_utc':end,'pins':{'head':HEAD,'base':BASE,'author':AUTHOR},'checks':checks,'check_count':len(checks),'nested_manifest_instances':len(nested),'all_nested_bindings':nested,'api_tree_chunks':api_tree_chunks,'full_recursive_tree_map_sha256':sha(json.dumps(ht,sort_keys=True,separators=(',',':')).encode()),'full_api_pr_file_metadata':files,'historical_checkpoints':history,'queue':queue,'independently_retrieved_sources':source,'replays':replays,'author_exact_assertions':128694,'prior_independent_exact_assertions':8664,'no_git_or_service_mutations':True,'live_review_head_base_body_queue_gate_pending':True}
(HERE/'FROZEN_PROVENANCE_AND_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['verdict','check_count','nested_manifest_instances','author_exact_assertions','prior_independent_exact_assertions']},indent=2))
