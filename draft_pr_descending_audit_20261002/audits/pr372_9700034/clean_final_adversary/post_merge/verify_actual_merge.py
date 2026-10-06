#!/usr/bin/env python3
"""Read-only post-merge verification. No open-PR gate; no Git/service writes.
Raw responses and Git data go beneath the previously ignored private_api path.
Public receipt contains only generated validation, immutable identifiers and scoped hashes.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,base64,datetime,hashlib,json,subprocess,sys
OWN=Path(__file__).resolve().parent.parent; A=OWN.parent
M='329e7303d4616ebcf060a3c8731bd62ed1fa339a'; B='9562c80156ce25415888c4429064138cfb245fde'; H='f67440150ac3c5d2d2ad369991a8243d5eeea953'; T='8fc7458eabcacab97f82cb87fed213703f97bd49'; TARGET='problems/9700034_sirsn_maximal_routes'; QUEUE='unsolved_math_prioritization/QUEUE.md'; REPO='AlecKriebel/Math'
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('/Users/alec/Documents/Math'));p.add_argument('--fresh-name',required=True);args=p.parse_args()
if not args.fresh_name.replace('_','').replace('-','').isalnum():raise SystemExit('unsafe fresh name')
private=OWN/'private_api'/'post_merge'/args.fresh_name;private.mkdir(parents=True,exist_ok=False);checks=[];blobs=[];started=datetime.datetime.now(datetime.timezone.utc).isoformat()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sh(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git','-C',str(args.repo),*a])
def ck(ok,label,detail=None):
 checks.append({'pass':bool(ok),'label':label,'detail':detail})
 if not ok:raise RuntimeError(label)
def api(endpoint,label):
 r=subprocess.run(['gh','api',endpoint],capture_output=True);(private/(label+'.stdout')).write_bytes(r.stdout);(private/(label+'.stderr')).write_bytes(r.stderr);ck(r.returncode==0 and not r.stderr,'read-only API success '+label,{'stdout_sha256':sh(r.stdout),'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr)})
 return json.loads(r.stdout)
def tree(rev,label):
 raw=git('ls-tree','-rtz','--full-tree',rev);(private/(label+'.raw_git_tree')).write_bytes(raw);entries={}
 for item in raw.split(b'\0'):
  if item:
   meta,path=item.split(b'\t',1);mode,typ,s=meta.decode().split();entries[path.decode()]={'mode':mode,'type':typ,'sha':s}
 groups={'':[]}
 for path,e in entries.items():
  if e['type']=='tree':groups.setdefault(path,[])
  parent,name=path.rsplit('/',1) if '/' in path else ('',path);groups.setdefault(parent,[]).append((name,e))
 computed={};bad=[]
 for parent in sorted(groups,key=lambda x:x.count('/')+(1 if x else 0),reverse=True):
  data=b''
  for name,e in sorted(groups[parent],key=lambda x:(x[0]+('/' if x[1]['type']=='tree' else '')).encode()):
   child=parent+'/'+name if parent else name
   if e['type']=='tree':
    if child not in computed:raise RuntimeError('uncomputed subtree '+child)
    s=computed[child]
    if s!=e['sha']:bad.append(child)
    mode='40000'
   else:s=e['sha'];mode=e['mode']
   data+=mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(s)
  computed[parent]=hashlib.sha1(b'tree '+str(len(data)).encode()+b'\0'+data).hexdigest()
 ck(not bad,'every explicit raw Git subtree independently hashes '+label,{'computed_directory_trees':len(computed),'mismatches':bad});ck(computed['']==git('show','-s','--format=%T',rev).decode().strip(),'full raw Git root hashes '+label,{'root_sha':computed[''],'entries':len(entries),'raw_git_tree_bytes':len(raw),'raw_git_tree_sha256':sh(raw)})
 return entries
summary={}
try:
 body=(A/'accepted_pr_body.txt').read_bytes();pr=api(f'repos/{REPO}/pulls/372','initial_pr');remote=api(f'repos/{REPO}/git/ref/heads/main','initial_remote_main');mc=api(f'repos/{REPO}/git/commits/{M}','actual_merge_commit')
 ck(pr['state']=='closed' and pr['merged'] is True and pr['draft'] is False,'actual PR closed and merged from ready state');ck(pr['merge_commit_sha']==M and pr['head']['sha']==H,'actual merge and exact accepted head');ck(pr['merged_at']=='2026-10-03T10:36:42Z','actual merged UTC');ck(pr['body'].encode()==body and sh(body)=='bb978a8f085568ab6f97b68119e8ea4288f8c8bc0b3c0bf7be173b433f650b34','entire accepted literal body exactly preserved');ck(pr['base']['ref']=='main' and pr['head']['repo']['full_name']==REPO and pr['base']['repo']['full_name']==REPO,'actual repository/base identities')
 ck([x['sha'] for x in mc['parents']]==[B,H] and mc['tree']['sha']==T,'actual immutable merge API exact parents and tree');localparents=git('show','-s','--format=%P',M).decode().strip().split();ck(localparents==[B,H] and git('show','-s','--format=%T',M).decode().strip()==T,'actual raw Git merge exact parents and tree')
 mt=tree(M,'actual_merge');bt=tree(B,'accepted_base');ht=tree(H,'accepted_head');ck(mt==ht,'actual full merged tree equals exact accepted head tree')
 root=api(f'repos/{REPO}/git/trees/{T}','actual_merge_api_root');ck(root.get('truncated') is False and {x['path']:{k:x[k] for k in ['mode','type','sha']} for x in root['tree']}=={n:e for n,e in mt.items() if '/' not in n},'complete nonrecursive actual merge API root equals complete raw Git root')
 originals={str(f.relative_to(A/'snapshot'/TARGET)):f.read_bytes() for f in (A/'snapshot'/TARGET).rglob('*') if f.is_file()};reviewed={str(f.relative_to(A/'repaired_snapshot'/TARGET)):f.read_bytes() for f in (A/'repaired_snapshot'/TARGET).rglob('*') if f.is_file()};targets={n:e for n,e in mt.items() if n.startswith(TARGET+'/') and e['type']!='tree'};ck(len(originals)==len(reviewed)==len(targets)==48 and originals==reviewed and set(targets)=={TARGET+'/'+n for n in originals},'full literal original/reviewed/actual target48 closure')
 changed={n for n in mt.keys()|bt.keys() if mt.get(n)!=bt.get(n)};leaves={n for n in changed if (mt.get(n) or bt.get(n))['type']!='tree'};ck(leaves==set(targets)|{QUEUE} and len(leaves)==49,'actual merge exact full49 changed leaves');allowed_ancestors={TARGET,'problems',QUEUE,'unsolved_math_prioritization'};bad=[n for n in mt.keys()|bt.keys() if not n.startswith(TARGET+'/') and n not in allowed_ancestors and mt.get(n)!=bt.get(n)];ck(not bad,'every unrelated literal root mode/type/blob/tree entry preserved',{'bad_paths':bad})
 filelist=[]
 for page in range(1,100):
  part=api(f'repos/{REPO}/pulls/372/files?per_page=100&page={page}','actual_pr_files_'+str(page));filelist.extend(part)
  if len(part)<100:break
 else:raise RuntimeError('unbounded file pagination')
 ck(len(filelist)==pr['changed_files']==49 and {x['filename'] for x in filelist}==leaves and len({x['filename'] for x in filelist})==len(filelist),'actual complete unique API changed-file scope49')
 filemap={x['filename']:x for x in filelist}
 def blobread(pair):
  i,n=pair;e=mt[n];r=subprocess.run(['gh','api',f'repos/{REPO}/git/blobs/{e["sha"]}'],capture_output=True);(private/f'blob_{i}.stdout').write_bytes(r.stdout);(private/f'blob_{i}.stderr').write_bytes(r.stderr)
  if r.returncode or r.stderr:raise RuntimeError('immutable blob API failure '+n)
  d=json.loads(r.stdout);b=base64.b64decode(d['content']);g=git('show',M+':'+n);rawsha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();ok=d['encoding']=='base64' and len(b)==d['size'] and rawsha==e['sha']==d['sha']==filemap[n]['sha'] and b==g and e['mode']=='100644' and e['type']=='blob'
  if n.startswith(TARGET+'/'):ok=ok and b==originals[n[len(TARGET)+1:]]==reviewed[n[len(TARGET)+1:]]
  return {'path':n,'mode':e['mode'],'type':e['type'],'bytes':len(b),'sha256':sh(b),'api_file_sha':filemap[n]['sha'],'api_blob_sha':d['sha'],'raw_git_blob_sha':rawsha,'literal_bytes_and_mode_type_hash_pass':ok}
 with ThreadPoolExecutor(max_workers=6) as ex:blobs=list(ex.map(blobread,enumerate(sorted(leaves))))
 ck(all(x['literal_bytes_and_mode_type_hash_pass'] for x in blobs),'all49 actual immutable API/raw Git blob/mode/type/bytes comparisons',{'target_count':48,'queue_count':1})
 baseq=git('show',B+':'+QUEUE);mergedq=git('show',M+':'+QUEUE);lines=baseq.splitlines(keepends=True);prefix=b'| 397 | 9700034 / AMR-096-0034 |';idx=[i for i,b in enumerate(lines) if b.startswith(prefix)];ck(len(idx)==1,'actual full queue own row unique');i=idx[0];before=lines[i];ck(i+1==408 and before.count(b'| queued | 0/5 |')==1,'actual complete own queue row literal baseline and line408');after=before.replace(b'| queued | 0/5 |',b'| unsolved | 5/5 |');lines[i]=after;ck(mergedq==b''.join(lines),'entire actual merged queue changes only own two literal cells');bcells=before.split(b'|');acells=after.split(b'|');ck([j for j,(x,y) in enumerate(zip(bcells,acells)) if x!=y]==[8,9] and len(bcells)==len(acells),'actual own row only exact cells8,9');ck(mt[QUEUE]['mode']==bt[QUEUE]['mode']=='100644' and mt[QUEUE]['type']==bt[QUEUE]['type']=='blob','actual queue ordinary100644 blob mode/type preserved')
 prior=0
 for manifest in [OWN/'PUBLIC_MANIFEST.json',OWN/'final_live/PUBLIC_MANIFEST.json']:
  d=json.loads(manifest.read_bytes())
  for f in d['files']:
   b=(OWN/f['path']).read_bytes();ck(len(b)==f['bytes'] and sh(b)==f['sha256'],'all previously sealed artifact preserved '+f['path']);prior+=1
 ck(prior==34,'all original26 plus final_live8 manifest-bound artifacts unchanged')
 # Reachability, not equality: continuing unrelated repository work may advance main.
 remote_sha=remote['object']['sha'];local_main=git('rev-parse','main').decode().strip();local_head=git('rev-parse','HEAD').decode().strip();ck(git('branch','--show-current').decode().strip()=='main','local main branch retained')
 for name,ancestor,desc in [('accepted main in merge',B,M),('accepted head in merge',H,M),('actual merge in local main',M,local_main),('actual merge in local HEAD',M,local_head)]:
  r=subprocess.run(['git','-C',str(args.repo),'merge-base','--is-ancestor',ancestor,desc],capture_output=True);ck(r.returncode==0 and not r.stderr,'actual local ancestry '+name,{'ancestor':ancestor,'descendant':desc})
 compare=api(f'repos/{REPO}/compare/{M}...{remote_sha}','actual_remote_main_ancestry');ck(compare['merge_base_commit']['sha']==M,'actual remote main descends from actual merge',remote_sha)
 late=api(f'repos/{REPO}/pulls/372','late_pr');lm=api(f'repos/{REPO}/git/ref/heads/main','late_remote_main');lc=api(f'repos/{REPO}/git/commits/{M}','late_actual_merge');ck(late['state']=='closed' and late['merged'] is True and late['head']['sha']==H and late['merge_commit_sha']==M and late['merged_at']==pr['merged_at'] and late['body'].encode()==body,'late actual merged status/head/body/time immutable');ck([x['sha'] for x in lc['parents']]==[B,H] and lc['tree']['sha']==T,'late actual merge parents/tree immutable')
 if lm['object']['sha']!=remote_sha:
  c=api(f'repos/{REPO}/compare/{M}...{lm["object"]["sha"]}','late_remote_main_ancestry');ck(c['merge_base_commit']['sha']==M,'advanced late remote main preserves actual merge ancestry')
 summary={'actual_merge':M,'merged_utc':pr['merged_at'],'actual_parents':[B,H],'accepted_head':H,'accepted_base':B,'actual_tree':T,'accepted_body_sha256':sh(body),'complete_merge_entries':len(mt),'complete_base_entries':len(bt),'complete_head_entries':len(ht),'changed_leaves':49,'target_files':48,'own_queue_line_1_based':408,'own_queue_changed_cells':[8,9],'own_queue_before_utf8':before.decode(),'own_queue_after_utf8':after.decode(),'full_base_queue_sha256':sh(baseq),'full_merged_queue_sha256':sh(mergedq),'observed_local_main':local_main,'observed_local_head':local_head,'initial_remote_main':remote_sha,'late_remote_main':lm['object']['sha'],'previous_manifest_bindings_unchanged':prior}
 result={'status':'PASS_ACTUAL_MERGED_SCOPED_PACKET','started_utc':started,'completed_utc':utc(),'code_sha256':sh(Path(__file__).read_bytes()),'checks':checks,'summary':summary,'complete_immutable_blob_validations':blobs,'scope':'Independent actual merged packet and ancestry verification only. Original remains unsolved partial5/5; no novel full solution, paper, DOI, release, or overall merge/novelty certification.'}
except Exception as e:result={'status':'FAIL_ACTUAL_MERGE_VERIFICATION','started_utc':started,'completed_utc':utc(),'error':repr(e),'code_sha256':sh(Path(__file__).read_bytes()),'checks':checks,'summary':summary,'complete_immutable_blob_validations':blobs}
output=OWN/'post_merge'/(args.fresh_name+'_RECEIPT.json');output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'checks':len(checks),'failed':sum(not x['pass'] for x in checks),'receipt':str(output)},indent=2));sys.exit(0 if result['status'].startswith('PASS') else 1)
