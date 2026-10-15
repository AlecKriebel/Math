#!/usr/bin/env python3
"""Read-only exact-live PR372 gate. Writes only fresh receipts/private data under this audit.
No normalization, mutations, checkout, fetch, Git/service writes or installations.
The reviewed body/target directory/head/main are explicit inputs, never inferred approvals.
"""
from pathlib import Path,PurePosixPath
from concurrent.futures import ThreadPoolExecutor
import argparse,base64,datetime,hashlib,json,subprocess,sys,urllib.request
OWN=Path(__file__).resolve().parent; TARGET='problems/9700034_sirsn_maximal_routes'; QUEUE='unsolved_math_prioritization/QUEUE.md'; REPO='AlecKriebel/Math'
p=argparse.ArgumentParser();p.add_argument('--expected-head',required=True);p.add_argument('--expected-main',required=True);p.add_argument('--expected-body',type=Path,required=True);p.add_argument('--expected-target',type=Path,required=True);p.add_argument('--protected-original',type=Path,required=True);p.add_argument('--fresh-output-name',required=True);p.add_argument('--git-repo',type=Path,default=Path('/Users/alec/Documents/Math'));a=p.parse_args()
if not a.fresh_output_name.replace('-','').replace('_','').isalnum():raise SystemExit('unsafe fresh output name')
out=OWN/'private_live'/a.fresh_output_name;out.mkdir(parents=True,exist_ok=False); api_dir=out/'api';api_dir.mkdir();packet=out/'packet';packet.mkdir();sources=out/'sources';sources.mkdir();runs=out/'runs';runs.mkdir();checks=[];failures=[];api_receipts=[]
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def ck(ok,label,detail=None):
 row={'label':label,'pass':bool(ok),'detail':detail};checks.append(row)
 if not ok:failures.append(row)
 return bool(ok)
def api(endpoint,label):
 r=subprocess.run(['gh','api',endpoint],capture_output=True);(api_dir/(label+'.stdout')).write_bytes(r.stdout);(api_dir/(label+'.stderr')).write_bytes(r.stderr);api_receipts.append({'label':label,'endpoint':endpoint,'utc':utc(),'exit':r.returncode,'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr)})
 if r.returncode or r.stderr:raise RuntimeError('read API failure '+label)
 return json.loads(r.stdout)
def tree(commit,label):
 c=api(f'repos/{REPO}/git/commits/{commit}',label+'_commit')
 # A complete immutable local Git tree is an alternate to GitHub's truncated
 # recursive endpoint. Its object identity is anchored in the fresh API commit.
 def git(*args):return subprocess.check_output(['git','-C',str(a.git_repo),*args])
 gc=git('show','-s','--format=%T%n%P',commit).decode().splitlines()
 ck(gc[0]==c['tree']['sha'] and gc[1].split()==[x['sha'] for x in c['parents']],'actual raw Git commit tree/parents equal immutable API '+label)
 raw=git('ls-tree','-rtz','--full-tree',commit);(api_dir/(label+'_complete_git_tree.raw')).write_bytes(raw);entries={}
 for item in raw.split(b'\0'):
  if item:
   meta,path=item.split(b'\t',1);mode,typ,sh=meta.decode().split();entries[path.decode()]={'mode':mode,'type':typ,'sha':sh}
 ck(bool(entries),'complete full literal raw Git root tree '+label,{'entries':len(entries),'raw_bytes':len(raw),'raw_sha256':sha(raw)})
 d=api(f'repos/{REPO}/git/trees/{c["tree"]["sha"]}',label+'_nonrecursive_api_root');ck(not d.get('truncated',True),'complete nonrecursive API root '+label)
 root={n:e for n,e in entries.items() if '/' not in n};ck(root=={x['path']:{k:x[k] for k in ['mode','type','sha']} for x in d['tree']},'entire API root entry set equals complete raw Git root '+label)
 groups={}
 for path,entry in entries.items():
  parent,name=path.rsplit('/',1) if '/' in path else ('',path);groups.setdefault(parent,[]).append((name,entry))
 computed={}
 for parent in sorted(groups,key=lambda x:x.count('/'),reverse=True):
  data=b''
  for name,entry in sorted(groups[parent],key=lambda x:(x[0]+('/' if x[1]['type']=='tree' else '')).encode()):
   child=parent+'/'+name if parent else name
   raw_mode='40000' if entry['type']=='tree' else entry['mode']
   raw_sha=computed.get(child,entry['sha']);ck(raw_sha==entry['sha'],'recomputed subtree Git SHA '+label+' '+child) if entry['type']=='tree' else None
   data+=raw_mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(raw_sha)
  computed[parent]=hashlib.sha1(b'tree '+str(len(data)).encode()+b'\0'+data).hexdigest()
 ck(computed.get('')==c['tree']['sha'],'recomputed entire raw Git tree SHA '+label)
 return c,entries
blob_cache={}
def read_blob(entry,label):
 if entry['sha'] not in blob_cache:
  d=api(f'repos/{REPO}/git/blobs/{entry["sha"]}',label);b=base64.b64decode(d['content']);ck(d['encoding']=='base64' and len(b)==d['size'],'API raw blob size '+label);ck(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==entry['sha']==d['sha'],'API raw Git blob hash '+label);blob_cache[entry['sha']]=b
 return blob_cache[entry['sha']]
def local_files(d):return {str(f.relative_to(d)):f.read_bytes() for f in d.rglob('*') if f.is_file()}
def run(label,cmd,expected=None,expected_json=None):
 r=subprocess.run(cmd,cwd=packet,capture_output=True);(runs/(label+'.stdout')).write_bytes(r.stdout);(runs/(label+'.stderr')).write_bytes(r.stderr)
 try:j=json.loads(r.stdout)
 except:j=None
 row={'label':label,'command':cmd,'exit':r.returncode,'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'complete_stdout_utf8':r.stdout.decode(),'complete_stderr_utf8':r.stderr.decode(),'whole_json':j};replays.append(row);ck(r.returncode==0 and not r.stderr,'zero exit and complete empty stderr '+label)
 if expected is not None:ck(r.stdout==expected,'complete literal stdout byte equality '+label)
 if expected_json is not None:ck(j==expected_json,'complete whole JSON equality '+label)
 return r.stdout
start=utc();replays=[];summary={}
try:
 expected=local_files(a.expected_target.resolve());protected=local_files(a.protected_original.resolve());body=a.expected_body.read_bytes();ck(all(expected.get(n)==b for n,b in protected.items()),'all protected original target bytes preserved in reviewed target input',{'original_paths':len(protected),'reviewed_paths':len(expected)})
 pr=api(f'repos/{REPO}/pulls/372','initial_pr');main=api(f'repos/{REPO}/git/ref/heads/main','initial_main');mr=api(f'repos/{REPO}/git/ref/pull/372/merge','initial_testmerge');head=pr['head']['sha'];mainsha=main['object']['sha'];merge=mr['object']['sha']
 ck(pr['state']=='open' and pr['draft'] is False,'PR is open and ready');ck(pr['head']['repo']['full_name']==REPO and pr['base']['repo']['full_name']==REPO,'exact repository identities');ck(head==a.expected_head,'actual PR head equals reviewed head',head);ck(mainsha==a.expected_main,'current remote main equals reviewed main',mainsha);ck(pr['base']['sha']==mainsha and pr['base']['ref']=='main','API base is actual fresh main',pr['base']['sha']);ck(pr['body'].encode()==body,'full literal PR body equals reviewed body bytes');ck(pr['mergeable'] is True and pr['mergeable_state']=='clean','PR API mergeability is clean',{'mergeable':pr['mergeable'],'mergeable_state':pr['mergeable_state']});ck(pr['merge_commit_sha']==merge,'PR API test merge agrees with current pull merge ref')
 hc,ht=tree(head,'actual_head');mc,mt=tree(mainsha,'actual_main');xc,xt=tree(merge,'actual_testmerge');parents=[x['sha'] for x in xc['parents']];ck(parents==[mainsha,head],'current test merge exact ordered parents',parents);ancestry=api(f'repos/{REPO}/compare/{mainsha}...{head}','main_head_ancestry');ck(ancestry['merge_base_commit']['sha']==mainsha,'fresh main is an actual head ancestor',ancestry['merge_base_commit']['sha']);ck(ht==xt,'complete test-merge tree equals reviewed head tree')
 own={n:entry for n,entry in ht.items() if n.startswith(TARGET+'/') and entry['type']!='tree'};ck(set(own)=={TARGET+'/'+n for n in expected},'complete actual target path set equals all reviewed target files',{'actual':len(own),'expected':len(expected)})
 changed={n for n in ht.keys()|mt.keys() if ht.get(n)!=mt.get(n)};leaves={n for n in changed if (ht.get(n) or mt.get(n))['type']!='tree'};ck(all(n.startswith(TARGET+'/') or n==QUEUE for n in leaves),'every other root-tree leaf path preserved against actual current main',sorted(n for n in leaves if not n.startswith(TARGET+'/') and n!=QUEUE))
 filelist=[]
 for page in range(1,100):
  part=api(f'repos/{REPO}/pulls/372/files?per_page=100&page={page}','pr_files_'+str(page));filelist.extend(part)
  if len(part)<100:break
 else:raise RuntimeError('files pagination did not terminate')
 ck(len(filelist)==pr['changed_files'] and len({x['filename'] for x in filelist})==len(filelist),'complete unique API changed-file list');ck({x['filename'] for x in filelist}==leaves,'full API changed-path set equals full actual root-tree diff')
 for i,n in enumerate(sorted(own)):
  b=read_blob(own[n],'target_blob_'+str(i));rel=n[len(TARGET)+1:];ck(b==expected.get(rel),'literal target bytes at actual head '+rel);q=packet/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
  ck(own[n]['mode']=='100644' and own[n]['type']=='blob','target file ordinary raw Git blob '+rel)
  listed=[x for x in filelist if x['filename']==n]
  if listed:ck(listed[0]['sha']==own[n]['sha'],'API changed-file blob identity '+rel)
 mainq=read_blob(mt[QUEUE],'main_queue_blob');headq=read_blob(ht[QUEUE],'head_queue_blob');prefix=b'| 397 | 9700034 / AMR-096-0034 |';lines=mainq.splitlines(keepends=True);idx=[i for i,b in enumerate(lines) if b.startswith(prefix)];ck(len(idx)==1,'full literal own queue row unique in current main')
 if len(idx)!=1:raise RuntimeError('own row missing/nonunique')
 i=idx[0];before=lines[i];after=before.replace(b'| queued | 0/5 |',b'| unsolved | 5/5 |');ck(after!=before and before.count(b'| queued | 0/5 |')==1,'sole literal own two queue cells queued0/5 to unsolved5/5');lines[i]=after;ck(headq==b''.join(lines),'entire queue bytes preserve all other cells/rows and make only own two-cell edit');qrows=[b for b in headq.splitlines(keepends=True) if b.startswith(prefix)];ck(qrows==[after],'complete own target row literal after edit');summary['own_queue_before_utf8']=before.decode();summary['own_queue_after_utf8']=after.decode()
 # Verify every declared historical, final, review and publication binding, with safe exact paths.
 manifests=[]
 for path in sorted(packet.rglob('*MANIFEST.json')):
  if path.name=='SOURCE_MANIFEST.json':continue
  m=json.loads(path.read_bytes());seen=set();base=path.parent if path.parent.name=='review' else packet
  for f in m.get('files',[]):
   if 'path' not in f:continue
   rel=f['path'];pp=PurePosixPath(rel);ck(not pp.is_absolute() and '..' not in pp.parts and rel not in seen,'manifest safe unique path '+str(path.relative_to(packet))+' '+rel);seen.add(rel);b=(base/rel).read_bytes();ck(len(b)==f['bytes'] and sha(b)==f['sha256'],'complete manifest binding '+str(path.relative_to(packet))+' '+rel)
  manifests.append({'path':str(path.relative_to(packet)),'sha256':sha(path.read_bytes()),'bindings':len(seen)})
 # Preserve historical closure in the original publication manifest; added files are bound by exact reviewed input.
 pm=json.loads((packet/'PUBLICATION_MANIFEST.json').read_bytes());ck({f['path'] for f in pm['files']}|{'PUBLICATION_MANIFEST.json'}==set(protected),'publication manifest complete historical closure')
 for k in range(2,6):ck(json.loads((packet/f'TURN_{k}_MANIFEST.json').read_bytes())['previous_manifest_sha256']==sha((packet/f'TURN_{k-1}_MANIFEST.json').read_bytes()),'historical chain link '+str(k))
 sm=json.loads((packet/'SOURCE_MANIFEST.json').read_bytes());source_receipts=[]
 for f in sm['files']:
  begin=utc()
  with urllib.request.urlopen(f['url'],timeout=60) as r:b=r.read();status=r.status;url=r.geturl()
  (sources/f['name']).write_bytes(b);ck(status==200 and len(b)==f['bytes'] and sha(b)==f['sha256'],'fresh primary inputs re-fetched and bound '+f['name']);source_receipts.append({'name':f['name'],'url':f['url'],'final_url':url,'status':status,'started_utc':begin,'completed_utc':utc(),'bytes':len(b),'sha256':sha(b)})
 for k in range(1,6):run('author_'+str(k),[sys.executable,str(packet/f'check_turn_{k}.py')],(packet/f'TURN_{k}_CHECKS.json').read_bytes())
 run('review_independent',[sys.executable,str(packet/'review/independent_check.py')],(packet/'review/INDEPENDENT_CHECKS.json').read_bytes())
 expected_v={'status':'PASS','public_bindings_checked':64,'replays':[{'turn':k,'exact_assertions':json.loads((packet/f'TURN_{k}_CHECKS.json').read_bytes())['exact_assertions'],'stdout_byte_exact':True} for k in range(1,6)],'total_exact_assertions':503419,'source_files_checked':4,'source_check':'verified'}
 vb=(json.dumps(expected_v,indent=2,sort_keys=True)+'\n').encode();run('verify_packet_fresh_sources',[sys.executable,str(packet/'verify_packet.py'),'--source-dir',str(sources)],vb,expected_v);run('verify_publication_fresh_sources',[sys.executable,str(packet/'verify_publication.py'),'--source-dir',str(sources)],vb+b'PASS: all publication bytes, frozen author replays and 2507 independent controls; original unsolved 5/5\n')
 # The actual author WIP is read through immutable API tree/blob data; it is not the publication folder.
 rm=json.loads((packet/'review/REVIEW_MANIFEST.json').read_bytes());wip=rm['author_wip'];wc,wt=tree(wip,'actual_author_wip');author=out/'actual_author_wip';author.mkdir();authors={n:e for n,e in wt.items() if n.startswith(TARGET+'/') and e['type']!='tree'};am=json.loads((packet/'FINAL_AUTHOR_MANIFEST.json').read_bytes());anames={f['path'] for f in am['files']}|{'FINAL_AUTHOR_MANIFEST.json'};ck(set(authors)=={TARGET+'/'+n for n in anames} and len(authors)==38,'actual final author WIP exact38 path closure')
 for j,n in enumerate(sorted(authors)):
  b=read_blob(authors[n],'wip_blob_'+str(j));rel=n[len(TARGET)+1:];ck(b==(packet/rel).read_bytes(),'actual author WIP bytes preserved '+rel);q=author/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 run('historical_review_author_actual_wip',[sys.executable,str(packet/'review/replay_author.py'),str(author)],(packet/'review/AUTHOR_REPLAY.json').read_bytes(),json.loads((packet/'review/AUTHOR_REPLAY.json').read_bytes()))
 # Exact late stability, without refreshing or silently accepting changed expectations.
 late=api(f'repos/{REPO}/pulls/372','late_pr');lm=api(f'repos/{REPO}/git/ref/heads/main','late_main');lx=api(f'repos/{REPO}/git/ref/pull/372/merge','late_testmerge')
 keys=['state','draft','body','mergeable','mergeable_state','merge_commit_sha','changed_files'];ck(all(late[k]==pr[k] for k in keys) and late['head']['sha']==head and late['base']['sha']==pr['base']['sha'],'late PR ready/body/head/base/merge stability');ck(lm['object']['sha']==mainsha,'late current-main stability');ck(lx['object']['sha']==merge,'late current-test-merge stability');lxc=api(f'repos/{REPO}/git/commits/{lx["object"]["sha"]}','late_testmerge_commit');ck([x['sha'] for x in lxc['parents']]==[mainsha,head] and lxc['tree']['sha']==xc['tree']['sha'],'late test-merge parents and complete tree identity')
 summary.update({'actual_head':head,'actual_main':mainsha,'api_base':pr['base']['sha'],'actual_test_merge':merge,'test_merge_parents':parents,'complete_head_tree_entries':len(ht),'complete_main_tree_entries':len(mt),'complete_merge_tree_entries':len(xt),'target_paths':len(own),'changed_leaf_paths':len(leaves),'manifests':manifests,'fresh_primary_inputs':source_receipts})
except Exception as e:failures.append({'label':'execution exception','pass':False,'detail':repr(e)})
result={'status':'PASS_EXACT_LIVE_SCOPED_GATE' if not failures else 'FAIL_EXACT_LIVE_GATE','started_utc':start,'completed_utc':utc(),'expected_head':a.expected_head,'expected_main':a.expected_main,'expected_body_sha256':sha(a.expected_body.read_bytes()),'gate_code_sha256':sha(Path(__file__).read_bytes()),'checks':checks,'failures':failures,'summary':summary,'complete_replays':replays,'api_receipts':sorted(api_receipts,key=lambda x:x['label']),'claim_scope':'Exact bounded live gate only; not universal resolution, novelty, overall merge or approval certification.'}
(out/'RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');public=OWN/(a.fresh_output_name+'_RECEIPT.json');public.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'checks':len(checks),'failed_checks':len(failures),'receipt':str(public)},indent=2));sys.exit(0 if not failures else 1)
