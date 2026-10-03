#!/usr/bin/env python3
"""Independent read-only actual post-merge audit; unique immutable run labels.
Git/API raw gzip is private and ignored; all program outputs are complete public gzip.
Every saved gzip, including private raw evidence, receives a full inventory binding.
Only writes inside this post_merge directory. No fetch/install/Git/service mutation.
"""
from pathlib import Path,PurePosixPath
import argparse,base64,concurrent.futures,datetime,gzip,hashlib,json,os,re,shutil,subprocess,threading,traceback,urllib.request
F=Path(__file__).resolve().parent;OWN=F.parent;A=OWN.parent;R=A.parents[2];AP=A.relative_to(R).as_posix()
MERGE='2da0adc1c56dbb15e53be162489eb001cfa83e03';MERGED_AT='2026-10-03T14:12:44Z';BASE='4b1fe16ffa841df9cefffe9479b05bbf950e423b';HEAD='e8a53a05b309bda2a7d60136d8fb5a4e21e313fd';TREE='902a46b4ec28f332f7ef0228d8e6bca3736a0031';ORIGINAL='74617174ddfb3ea726cea343a4ba915613724bdc'
BODY='99128f750a529174a631fd97600e4809f18c1054c0ef115b57e5838b4dff64fc';QSHA='aa2470313317850d2a05f8f0cf0b9523fbc73169c3c72b59074d51f7b10bc5a2';PREFIX='problems/30004320_laurent_descent';Q='unsolved_math_prioritization/QUEUE.md'
ORIGINAL_MF='bf7cece6ed2edc56f2b865baed9f0bcf9a13378511929c3f7f64d0cfb2144036';LIVE_MF='3c047d9b0663018219c9f6b4e6898a18175f75cd6e96ee6f93acfb1038d10445'
MUTABLE={AP+'/'+n for n in ['README.md','RESEARCH_LOG.md','DECISION.md','acceptance_criteria.json']}
PY=R/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
p=argparse.ArgumentParser();p.add_argument('--label',required=True);p.add_argument('--publish-run',action='store_true');arg=p.parse_args();assert re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,70}',arg.label)
RUN=F/('runs' if arg.publish_run else 'private_runs')/arg.label;RUN.mkdir(parents=True,exist_ok=False);PRIVATE=RUN/'private';PRIVATE.mkdir();RAW=PRIVATE/'raw_streams';RAW.mkdir();OUTPUT=RUN/'program_streams';OUTPUT.mkdir();CAND=PRIVATE/'candidate';CAND.mkdir();SOURCE=PRIVATE/'sources';SOURCE.mkdir()
checks=[];captures=[];jsons=[];gzip_records=[];replays=[];lock=threading.Lock();seq=0;start=datetime.datetime.now(datetime.timezone.utc).isoformat()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def ck(name,v,detail=None):
 checks.append({'check':name,'pass':bool(v),'detail':detail})
 if not v:raise AssertionError(name)
def parsed(b,name):
 j=json.loads(b);leaves=[]
 def walk(v,path):
  if isinstance(v,dict):
   for k,x in sorted(v.items()):walk(x,path+[k])
  elif isinstance(v,list):
   for i,x in enumerate(v):walk(x,path+[i])
  else:leaves.append([path,type(v).__name__,v])
 walk(j,[]);jsons.append({'reference':name,'bytes':len(b),'sha256':sha(b),'scalar_leaves':len(leaves),'complete_leaf_digest':sha(canon(leaves))});return j
def save_gzip(parent,name,b,kind):
 f=parent/(name+'.gz');f.write_bytes(gzip.compress(b,mtime=0));row={'path':f.relative_to(RUN).as_posix(),'classification':kind,'public':parent==OUTPUT,'bytes':len(b),'sha256':sha(b),'gzip_bytes':f.stat().st_size,'gzip_sha256':sha(f.read_bytes())}
 with lock:gzip_records.append(row)
 return row
def capture(cmd,kind='private Git/API raw',cwd=R,retain=True,allow_failure=False):
 global seq
 with lock:seq+=1;n=seq
 t0=now();r=subprocess.run(list(map(str,cmd)),cwd=cwd,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});t1=now();parent=OUTPUT if kind=='complete program output' else RAW
 out=save_gzip(parent,f'{n:05d}_stdout',r.stdout,kind) if retain else {'bytes':len(r.stdout),'sha256':sha(r.stdout),'retained':False,'reason':'Full huge recursive Git leaf map compared in memory with retained complete API chunks; avoid duplicate raw listings.'}
 err=save_gzip(parent,f'{n:05d}_stderr',r.stderr,kind);row={'id':n,'command':list(map(str,cmd)),'cwd':str(cwd),'start_utc':t0,'end_utc':t1,'exit_code':r.returncode,'stdout':out,'stderr':err}
 with lock:captures.append(row)
 if r.returncode and not allow_failure:raise RuntimeError({'command':row['command'],'exit_code':r.returncode,'stderr':r.stderr.decode(errors='replace')})
 return r.stdout

def git(*argv,retain=True):return capture(['git',*argv],retain=retain)
def api(end):return parsed(capture(['gh','api','--method','GET','-H','Cache-Control: no-cache','repos/AlecKriebel/Math/'+end]),'API '+end)
get_cache={};trees={};api_maps={};chunks=[];blobs={};current_validated={};current_protected={};availability={}
def known(rev):
 if rev not in availability:
  capture(['git','cat-file','-e',rev+'^{commit}'],allow_failure=True);availability[rev]=captures[-1]['exit_code']==0
 return availability[rev]
def get(rev,path):
 key=(rev,path)
 if key not in get_cache:
  if known(rev):get_cache[key]=git('show',rev+':'+path)
  else:
   # Unknown descendant objects are read directly from their complete API map;
   # immutable entries still match the literal merge/base's actual Git map.
   if rev not in trees:trees[rev]=api_map(api('git/commits/'+rev)['tree']['sha'])
   oid=trees[rev][path]['sha'];batch_blobs([oid]);get_cache[key]=blobs[oid]
 return get_cache[key]
def tree(rev):
 if rev not in trees:
  out={}
  for line in git('ls-tree','-r','-z','--full-tree',rev,retain=False).split(b'\0'):
   if line:
    meta,path=line.split(b'\t',1);mode,typ,oid=meta.decode().split();out[path.decode()]={'mode':mode,'type':typ,'sha':oid}
  trees[rev]=out
 return trees[rev]
def api_map(oid):
 if oid in api_maps:return api_maps[oid]
 j=api('git/trees/'+oid+'?recursive=1');ck('actual API tree identity '+oid,j['sha']==oid)
 if not j['truncated']:
  out={r['path']:{k:r[k] for k in ['mode','type','sha']} for r in j['tree'] if r['type']!='tree'};chunks.append({'tree':oid,'recursive':True,'entries':len(j['tree']),'truncated':False})
 else:
  j=api('git/trees/'+oid);ck('full nonrecursive API tree '+oid,j['sha']==oid and not j['truncated']);out={};chunks.append({'tree':oid,'recursive':False,'entries':len(j['tree']),'truncated':False,'truncated_recursive_not_credited':True})
  for r in j['tree']:
   if r['type']=='tree':out.update({r['path']+'/'+q:v for q,v in api_map(r['sha']).items()})
   else:out[r['path']]={k:r[k] for k in ['mode','type','sha']}
 api_maps[oid]=out;return out
def api_blob(oid):
 j=api('git/blobs/'+oid);b=base64.b64decode(j['content']);ck('actual raw API blob '+oid,j['encoding']=='base64' and j['sha']==oid and j['size']==len(b) and blob(b)==oid);return b
def batch_blobs(oids):
 missing=sorted(set(oids)-blobs.keys())
 with concurrent.futures.ThreadPoolExecutor(6) as pool:
  for oid,b in zip(missing,pool.map(api_blob,missing)):blobs[oid]=b

def manifest(root,literal,count):
 raw=(root/'PUBLIC_MANIFEST.json').read_bytes();j=parsed(raw,'sealed '+str(root.relative_to(A))+'/PUBLIC_MANIFEST.json');ck('literal immutable manifest '+root.name,sha(raw)==literal and len(j['files'])==count)
 seen=set()
 for r in j['files']:
  q=PurePosixPath(r['path']);ck('safe unique immutable binding '+str(root.name)+'/'+r['path'],not q.is_absolute() and '..' not in q.parts and q.as_posix()==r['path'] and r['path'] not in seen);seen.add(r['path']);f=root/q;b=f.read_bytes();ck('immutable full sealed binding '+str(root.name)+'/'+r['path'],not f.is_symlink() and f.resolve().is_relative_to(root.resolve()) and len(b)==r['bytes'] and sha(b)==r['sha256'])
 return {'root':root.relative_to(A).as_posix(),'files':count,'manifest_bytes':len(raw),'manifest_sha256':sha(raw)}
def row_of(q):
 rows=[line for line in q.splitlines(keepends=True) if len(line.split(b'|'))>9 and line.split(b'|')[2].strip().split()[:1]==[b'30004320']];ck('unique current own queue row',len(rows)==1);return rows[0]
def ancestry(older,newer):
 j=api('compare/'+older+'...'+newer);ck('actual API descendant comparison '+older+'/'+newer,j['base_commit']['sha']==older and j['merge_base_commit']['sha']==older and j['behind_by']==0 and j['status'] in ['ahead','identical'])
 # Local object availability is required so Git independently reproduces ancestry.
 if known(older) and known(newer):ck('actual Git descendant comparison '+older+'/'+newer,git('merge-base',older,newer).decode().strip()==older)
 return {'older':older,'newer':newer,'status':j['status'],'ahead_by':j['ahead_by'],'behind_by':j['behind_by'],'merge_base':j['merge_base_commit']['sha'],'local_Git_comparison_available':known(older) and known(newer)}
def validate_criteria(j):
 for k,v in [('accepted_status','unsolved'),('author_turns','5/5'),('original_problem_resolution_percent',0),('original_head',ORIGINAL),('body_sha256',BODY),('root_frozen_checks',501),('root_family_binding_and_control_checks',3310),('nested_manifest_bindings',130),('primary_historical_pdf_identities',11),('root_replayed_new_controls',13339),('root_replayed_drift_negative_controls',14),('no_paper_zenodo_doi_tracker_release',True)]:ck('new current acceptance criteria '+k,j.get(k)==v)
 # Exact literal merge must be present under an unambiguous merge-specific key.
 ck('new criteria literal actual merge',any(k in j and j[k]==MERGE for k in ['actual_merge','actual_merge_commit','actual_merge_sha','merge_commit','merge_commit_sha']))
 if 'actual_merge_pending' in j:ck('new criteria actual merge no longer pending',j['actual_merge_pending'] is False)
def validate_current(rev):
 if rev in current_validated:return current_validated[rev]
 aj=api('git/commits/'+rev);am=api_map(aj['tree']['sha']);available=known(rev)
 if available:gt=tree(rev);ck('full current actual Git/API map '+rev,am==gt and git('show','-s','--format=%T',rev).decode().strip()==aj['tree']['sha'])
 else:gt=am;trees[rev]=am;ck('complete API current descendant map '+rev,aj['sha']==rev and bool(am))
 ck('entire current53 target scope/modes/blobs '+rev,{p for p in gt if p.startswith(PREFIX+'/')}==set(expected)-{Q} and all(gt[p]==mt[p] for p in expected if p!=Q))
 ck('entire current immutable232 checkpoint map '+rev,all(gt.get(p)==v for p,v in published.items() if p not in MUTABLE))
 # Full scope equality is stronger than selected path projections: only the four
 # explicitly authorized root progress texts may change in the old236-file scope.
 q=get(rev,Q);batch_blobs([gt[Q]['sha']]);ck('current full queue Git/API equality '+rev,blobs[gt[Q]['sha']]==q and row_of(q)==row_of(qmerge))
 for p in expected:
  if p!=Q:ck('current target actual bytes '+rev+'/'+p,get(rev,p)==get(MERGE,p))
 mutable=[]
 for p in sorted(MUTABLE):
  ck('current mutable root file retained '+p,p in gt and gt[p]['mode']=='100644' and gt[p]['type']=='blob');b=get(rev,p);batch_blobs([gt[p]['sha']]);ck('full current mutable root Git/API '+p,b==blobs[gt[p]['sha']]);old=get(BASE,p);record={'path':p,'literal_checkpoint_sha256':sha(old),'current_sha256':sha(b),'changed':b!=old,'literal_checkpoint_complete_text':old.decode(),'current_complete_text':b.decode()}
  if p.endswith('acceptance_criteria.json') and b!=old:validate_criteria(parsed(b,'new current criteria '+rev))
  mutable.append(record)
 additions=[]
 for p in sorted(gt):
  if p.startswith(AP+'/') and p not in published and ('ACTUAL_ACCEPTANCE' in p.upper() or 'ACTUAL_MERGE_VERIFICATION' in p.upper()) and p.endswith('.json'):
   b=get(rev,p);batch_blobs([gt[p]['sha']]);ck('new actual acceptance receipt Git/API '+p,b==blobs[gt[p]['sha']]);j=parsed(b,'new actual receipt '+p);ck('new actual acceptance literal merge '+p,j.get('actual_merge',j.get('merge_commit_sha'))==MERGE and j.get('merged_at')==MERGED_AT and j.get('reviewed_head',j.get('head'))==HEAD and j.get('actual_parents',j.get('parents'))==[BASE,HEAD])
   if 'body_sha256' in j:ck('new actual receipt literal body '+p,j['body_sha256']==BODY)
   additions.append({'path':p,'bytes':len(b),'sha256':sha(b),'complete_json':j})
 record={'commit':rev,'actual_current_Git_map_available':available,'tree':aj['tree']['sha'],'full_leaf_entries':len(gt),'canonical_leaf_map_sha256':sha(canon(gt)),'full_queue_bytes':len(q),'full_queue_sha256':sha(q),'own_row':row_of(q).decode(),'immutable232_root_checkpoint_files_preserved':True,'all53_target_paths_preserved':True,'four_mutable_root_files':mutable,'new_actual_acceptance_receipts':additions};current_validated[rev]=record;return record

def observe(phase):
 ck(phase+' no active MERGE_HEAD',not (R/git('rev-parse','--git-path','MERGE_HEAD').decode().strip()).exists());ck(phase+' local main branch',git('branch','--show-current').decode().strip()=='main')
 local={x:git('rev-parse',x).decode().strip() for x in ['HEAD','refs/heads/main','refs/remotes/origin/main']};ck(phase+' local checkout matches local main',local['HEAD']==local['refs/heads/main'])
 remote=git('ls-remote','origin','refs/heads/main').decode().strip().split();ck(phase+' actual remote main ref',len(remote)==2 and remote[1]=='refs/heads/main');main=api('git/ref/heads/main');currents={**local,'actual_remote_main':remote[0],'actual_API_main':main['object']['sha']};lineages=[]
 for rev in sorted(set(currents.values())):lineages.append(ancestry(MERGE,rev));validate_current(rev)
 pull=api('pulls/368');ck(phase+' actual merged PR literal metadata',pull['number']==368 and pull['state']=='closed' and pull['merged'] is True and pull['draft'] is False and pull['merge_commit_sha']==MERGE and pull['head']['sha']==HEAD and pull['base']['sha']==BASE and pull['base']['ref']=='main' and pull['merged_at']==MERGED_AT and pull['closed_at']==MERGED_AT and pull['changed_files']==54 and sha(pull['body'].encode())==BODY)
 mj=api('git/commits/'+MERGE);ck(phase+' actual merge API tree ordered parents',mj['sha']==MERGE and mj['tree']['sha']==TREE and [p['sha'] for p in mj['parents']]==[BASE,HEAD]);ck(phase+' actual merge Git tree ordered parents',git('show','-s','--format=%T',MERGE).decode().strip()==TREE and git('show','-s','--format=%P',MERGE).decode().strip().split()==[BASE,HEAD])
 return {'phase':phase,'utc':now(),'current_main_observations':currents,'proved_merge_ancestry':lineages,'actual_merge_API_identity':{'sha':mj['sha'],'tree':mj['tree']['sha'],'ordered_parents':[p['sha'] for p in mj['parents']],'author':mj['author'],'committer':mj['committer']},'actual_PR_semantics':{k:pull[k] for k in ['number','state','merged','draft','merge_commit_sha','merged_at','closed_at','changed_files']},'actual_PR_head':pull['head']['sha'],'actual_PR_literal_base':pull['base']['sha'],'body_bytes':len(pull['body'].encode()),'body_sha256':sha(pull['body'].encode()),'body_complete_text':pull['body']}
def run(label,argv,expected_stdout=None):
 b=capture([str(PY),'-B',*map(str,argv)],kind='complete program output',cwd=PRIVATE);cap=captures[-1];ck('new full successful replay '+label,cap['exit_code']==0 and cap['stderr']['bytes']==0 and (expected_stdout is None or b==expected_stdout));replays.append({'label':label,'capture_id':cap['id'],'command':cap['command'],'start_utc':cap['start_utc'],'end_utc':cap['end_utc'],'stdout':cap['stdout'],'stderr':cap['stderr'],'exit_code':0});return b

def inventory():
 listed={r['path']:r for r in gzip_records};actual={p.relative_to(RUN).as_posix() for p in RUN.rglob('*.gz') if p.is_file()};ck('EVERY saved gzip closed inventory',set(listed)==actual and len(listed)==len(gzip_records))
 rows=[]
 for path in sorted(actual):
  r=listed[path];z=(RUN/path).read_bytes();b=gzip.decompress(z);ck('every complete gzip binding '+path,len(z)==r['gzip_bytes'] and sha(z)==r['gzip_sha256'] and len(b)==r['bytes'] and sha(b)==r['sha256']);rows.append(r)
 out={'status':'PASS','utc':now(),'saved_gzip_streams':len(rows),'private_raw_streams':sum(not r['public'] for r in rows),'public_complete_program_streams':sum(r['public'] for r in rows),'all_files':rows};(RUN/'EVERY_SAVED_GZIP.json').write_text(json.dumps(out,indent=2)+'\n');return out
try:
 mt=tree(MERGE);bt=tree(BASE);ot=tree(ORIGINAL);snap=parsed((A/'snapshot_manifest.json').read_bytes(),'original snapshot');expected={r['path']:r for r in snap['files']};published={p:v for p,v in bt.items() if p.startswith(AP+'/')}
 ck('all236 original root publication checkpoint entries',len(published)==236 and len(MUTABLE)==4 and sum(p not in MUTABLE for p in published)==232)
 ck('all54 actual merged delta',len(expected)==54 and {p for p in mt.keys()|bt.keys() if mt.get(p)!=bt.get(p)}==set(expected))
 ck('merge actual tree exactly reviewed tree',git('show','-s','--format=%T',MERGE).decode().strip()==TREE and mt==tree(HEAD));ck('all53 original target entries retained',all(mt[p]==ot[p] for p in expected if p!=Q))
 qbase=get(BASE,Q);qmerge=get(MERGE,Q);ck('literal complete premerge base queue hash',sha(qbase)==QSHA);ql=qbase.splitlines(keepends=True);ix=[i for i,l in enumerate(ql) if len(l.split(b'|'))>9 and l.split(b'|')[2].strip().split()[:1]==[b'30004320']];ck('own original queue physical399',ix==[398]);qc=ql[398].split(b'|');ck('own queued0 cells before merge',qc[8].strip()==b'queued' and qc[9].strip()==b'0/5');qc[8:10]=[b' unsolved ',b' 5/5 '];ql[398]=b'|'.join(qc);ck('actual complete merge queue only cells8/9',b''.join(ql)==qmerge)
 before=observe('before')
 seals=[manifest(OWN,ORIGINAL_MF,47),manifest(OWN/'final_live',LIVE_MF,1635)]
 files=api('pulls/368/files?per_page=100&page=1');ck('full actual merged54 API file scope',len(files)==54 and {r['filename'] for r in files}==set(expected));ck('actual merged API pagination exhaustion',api('pulls/368/files?per_page=100&page=2')==[])
 batch_blobs(mt[p]['sha'] for p in expected);merged_files=[]
 for p in sorted(expected):
  b=get(MERGE,p);entry=mt[p];ck('actual merged54 bytes and modes '+p,entry['mode']=='100644' and entry['type']=='blob' and blobs[entry['sha']]==b and blob(b)==entry['sha']);fr=next(r for r in files if r['filename']==p);ck('actual merged API status/blob '+p,fr['status']==('modified' if p==Q else 'added') and fr['sha']==entry['sha'])
  if p!=Q:
   r=expected[p];ck('complete original target bytes '+p,b==(A/'snapshot'/p).read_bytes() and len(b)==r['bytes'] and sha(b)==r['sha256']);f=CAND/p.removeprefix(PREFIX+'/');f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
  if p.endswith('.json'):parsed(b,'actual merge '+p)
  merged_files.append({'path':p,**entry,'bytes':len(b),'sha256':sha(b)})
 batch_blobs(v['sha'] for v in published.values());pubfiles=[]
 for p,v in sorted(published.items()):
  b=get(BASE,p);ck('all236 literal root checkpoint actual Git/API '+p,b==blobs[v['sha']] and mt[p]==v and v['mode']=='100644');pubfiles.append({'path':p,**v,'bytes':len(b),'sha256':sha(b),'mutable_authorized':p in MUTABLE})
  if p.endswith('.json'):parsed(b,'literal checkpoint '+p)
 nested=[]
 for n in [f'TURN_{i}_MANIFEST.json' for i in range(1,6)]+['FINAL_AUTHOR_MANIFEST.json','review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']:
  j=parsed((CAND/n).read_bytes(),'candidate manifest '+n);seen=set()
  for r in j['files']:
   pp=PurePosixPath(r['path']);ck('safe unique nested '+n+'/'+r['path'],not pp.is_absolute() and '..' not in pp.parts and r['path'] not in seen);seen.add(r['path']);b=(CAND/n).parent.joinpath(pp).read_bytes();ck('all nested bound bytes '+n+'/'+r['path'],len(b)==r['bytes'] and sha(b)==r['sha256']);nested.append({'manifest':n,**r})
  if n.startswith('TURN_') and int(n.split('_')[1])>1:
   i=int(n.split('_')[1]);ck('nested chain '+n,j['previous_manifest_sha256']==sha((CAND/f'TURN_{i-1}_MANIFEST.json').read_bytes()))
 ck('all130 nested8 manifests',len(nested)==130)
 pub=parsed((CAND/'PUBLICATION_MANIFEST.json').read_bytes(),'candidate full public scope');ck('exact52 manifest scope and unsolved5',set(r['path'] for r in pub['files'])=={p.relative_to(CAND).as_posix() for p in CAND.rglob('*') if p.is_file()}-{'PUBLICATION_MANIFEST.json'} and pub['status']=='unsolved' and pub['turns']=='5/5')
 authors=['5e2eb63fd571f2f660ff9ebb436440029b5d1268','d7d898ba23e9d024e79b938e3e0e305d91bb125b','c800217d22d329d6ca397f3c18e5115c77688fb9','24ecf1f2f0ab62082f328545180e4b2ba1640ab7','b08662a16499edf37f0c0eae850cfa00b7778ed6'];prior='efd29c05204703acca9a0860812f54b94fae54b1';hist=[]
 for i,c in enumerate(authors,1):
  cj=api('git/commits/'+c);ck('actual five author parent/tree '+str(i),[r['sha'] for r in cj['parents']]==[prior] and git('show','-s','--format=%P',c).decode().strip()==prior and git('show','-s','--format=%T',c).decode().strip()==cj['tree']['sha']);mj=parsed((CAND/f'TURN_{i}_MANIFEST.json').read_bytes(),'actual author'+str(i))
  for p in [f'TURN_{i}_MANIFEST.json']+[r['path'] for r in mj['files']]:ck('actual author checkpoint bytes '+str(i)+'/'+p,get(c,PREFIX+'/'+p)==(CAND/p).read_bytes())
  hist.append({'turn':i,'sha':c,'parents':[r['sha'] for r in cj['parents']],'tree':cj['tree']['sha'],'author':cj['author'],'committer':cj['committer']});prior=c
 rb=parsed((CAND/'review/REMOTE_BINDING.json').read_bytes(),'all42 historical binding');ck('exact old42 author checkpoint',rb['head']==authors[-1] and len(rb['files'])==42)
 for r in rb['files']:
  b=get(authors[-1],PREFIX+'/'+r['path']);ck('actual42 old raw byte binding '+r['path'],b==(CAND/r['path']).read_bytes() and len(b)==r['size'] and blob(b)==r['git_blob_sha'])
 # New post-merge source retrieval is explicit and does not alter prior source chronology.
 routes=[]
 for n in ['SOURCE_MANIFEST.json','SOURCE_ADDITION_T1.json','SOURCE_ADDITION_T4.json','SOURCE_ADDITION_T5.json']:routes+=parsed((CAND/n).read_bytes(),'source routing '+n)['files']
 def fetch(r):
  t0=now();ck('safe primary filename '+r['name'],Path(r['name']).name==r['name']);request=urllib.request.Request(r['url'],headers={'User-Agent':'Independent actual post-merge mathematics audit'})
  with urllib.request.urlopen(request,timeout=60) as response:b=response.read();final=response.geturl()
  (SOURCE/r['name']).write_bytes(b);return {**r,'download_started_utc':t0,'download_finished_utc':now(),'final_url':final,'actual_bytes':len(b),'actual_sha256':sha(b)}
 with concurrent.futures.ThreadPoolExecutor(5) as pool:sources=list(pool.map(fetch,routes))
 for r in sources:ck('all fresh postmerge original PDF hashes '+r['name'],r['actual_bytes']==r['bytes'] and r['actual_sha256']==r['sha256'])
 ck('eleven unique postmerge originals',len(sources)==len({r['name'] for r in sources})==11)
 s=(CAND/'review/AUTHOR_REPLAY.json').read_bytes();ns=json.loads(s);ns.update(source_check='not requested; raw sources are not distributed',source_pdfs_checked=0);n=(json.dumps(ns,indent=2,sort_keys=True)+'\n').encode();rv=b'PASS: review hashes, frozen author/remote binding, and independent replay\n';end=b'PASS: all publication bytes, frozen author proofs and independent review; original unsolved 5/5\n'
 commands=[(f'author{i}',[CAND/f'check_turn_{i}.py'],(CAND/f'TURN_{i}_CHECKS.json').read_bytes()) for i in range(1,6)]+[('historical_review',[CAND/'review/independent_checks.py'],(CAND/'review/INDEPENDENT_CHECKS.json').read_bytes()),('packet_with_sources',[CAND/'verify_packet.py','--source-dir',SOURCE],s),('packet_without_sources',[CAND/'verify_packet.py'],n),('review_wrapper',[CAND/'review/verify_review.py','--author-dir',CAND],rv),('publication_with_sources',[CAND/'verify_publication.py','--source-dir',SOURCE],s+rv+end),('publication_without_sources',[CAND/'verify_publication.py'],n+rv+end)]
 for label,argv,out in commands:run(label,argv,out)
 controls=[]
 for fam,program,out,count,verifier in [('descent_cohomology_review','ADVERSARIAL_CONTROLS.py','ADVERSARIAL_CONTROLS.stdout',1923,'verify_family_manifest.py'),('residue_valuation_review','residue_valuation_controls.py','RESIDUE_VALUATION_CONTROLS.json',3029,'verify_manifest.py'),('clean_final_adversary','adversarial_controls.py','ADVERSARIAL_CONTROLS.json',8387,'verify_manifest.py')]:
  D=A/fam;b=run('controls_'+fam,[D/program],(D/out).read_bytes());j=parsed(b,'new postmerge controls '+fam);ck('actual new exact control count '+fam,j['status']=='PASS' and j['exact_assertions']==count);controls.append({'family':fam,'exact_assertions':count,'complete_output':j});v=run('manifest_'+fam,[D/verifier]);ck('actual immutable original manifest utility '+fam,json.loads(v)['status']=='PASS')
 run('final_live_manifest',[OWN/'final_live/verify_live_manifest.py'])
 # Fourteen old negatives remain auxiliary frozen predicates; six actual post-merge
 # predicates below use literal merged-state/head/base/tree/body/merge identity.
 original=parsed((OWN/'DRIFT_NEGATIVES.json').read_bytes(),'old14 full negatives');code=(OWN/'drift_negatives.py').read_text();needle="HERE=Path(__file__).resolve().parent;REPO=HERE.parents[3];CAND=HERE.parent/'snapshot/problems/30004320_laurent_descent';PYTHON=REPO/";ck('unique old negative path adaptation',code.count(needle)==1);code=code.replace(needle,f"HERE=Path({str(PRIVATE)!r});REPO=Path({str(R)!r});CAND=Path({str(CAND)!r});PYTHON=REPO/");needle="(HERE.parent/'snapshot'/Q)";ck('unique old negative queue path adaptation',code.count(needle)==1);code=code.replace(needle,f"(Path({str(A/'snapshot')!r})/Q)");shadow=PRIVATE/'drift_negatives.py';shadow.write_text(code);negative=parsed(run('drift14_private',[shadow]),'new postmerge14 negatives')
 negcap=replays[-1];ck('new negative UTC actual command interval',negcap['start_utc']<=negative['utc']<=negcap['end_utc'] and negative['negative_controls']==14 and len(negative['results'])==14)
 for x,y in zip(original['results'],negative['results']):
  ck('same whole negative record shape '+x['control'],x.keys()==y.keys() and x['rejected'] is y['rejected'] is True)
  for k in x:
   if k not in ['stderr_bytes','stderr_sha256']:ck('whole negative metadata '+x['control']+'/'+k,x[k]==y[k])
  if 'exit_code' in x:
   label=x['control'];ob=(OWN/(label+'.stderr')).read_bytes();nb=(PRIVATE/(label+'.stderr')).read_bytes();ck('entire negative traceback only owned root differs '+label,len(nb)==y['stderr_bytes'] and sha(nb)==y['stderr_sha256'] and ob.replace(str(OWN/'private_controls').encode(),b'OWN_PRIVATE')==nb.replace(str(PRIVATE/'private_controls').encode(),b'OWN_PRIVATE'));save_gzip(OUTPUT,'negative_'+label+'_stderr',nb,'complete rejected-verifier stderr');save_gzip(OUTPUT,'negative_'+label+'_stdout',(PRIVATE/(label+'.stdout')).read_bytes(),'complete rejected-verifier stdout')
 def post_pins(state,merged,head,base,merge,tree,body):return state=='closed' and merged is True and head==HEAD and base==BASE and merge==MERGE and tree==TREE and body==BODY
 pos=('closed',True,HEAD,BASE,MERGE,TREE,BODY);ck('actual literal postmerge predicate',post_pins(*pos));negatives=[]
 for index,name,bad in [(0,'state','open'),(1,'merged',False),(2,'head','0'*40),(3,'base','0'*40),(4,'actual merge','0'*40),(5,'tree','0'*40),(6,'body','0'*64)]:
  v=list(pos);v[index]=bad;ck('literal actual postmerge negative '+name,not post_pins(*v));negatives.append({'mutation':name,'rejected':True})
 after=observe('after');forward=ancestry(before['current_main_observations']['actual_API_main'],after['current_main_observations']['actual_API_main'])
 ck('literal immutable root families/proof publication on disk',all(p in MUTABLE or (R/p).read_bytes()==get(BASE,p) for p in published))
 # All live-case raw bytes still exist and all completed candidate bytes are unchanged.
 for f in CAND.rglob('*'):
  if f.is_file():ck('replay candidate immutable after programs '+f.relative_to(CAND).as_posix(),f.read_bytes()==get(MERGE,PREFIX+'/'+f.relative_to(CAND).as_posix()))
 seals2=[manifest(OWN,ORIGINAL_MF,47),manifest(OWN/'final_live',LIVE_MF,1635)];ck('original47 and live1635 seals immutable start/end',seals2==seals)
 inv=inventory();endtime=now()
 result={'status':'PASS_ACTUAL_POST_MERGE_UNSOLVED5','start_utc':start,'end_utc':endtime,'literal_merge':{'commit':MERGE,'merged_at':MERGED_AT,'ordered_parents':[BASE,HEAD],'tree':TREE,'body_sha256':BODY,'original_head':ORIGINAL},'before':before,'after':after,'proved_current_main_forward_interval':forward,'all_current_main_versions':list(current_validated.values()),'check_count':len(checks),'checks':checks,'all54_actual_merged_files':merged_files,'all54_actual_API_file_metadata':[{k:r[k] for k in ['filename','status','sha','additions','deletions','changes'] if k in r} for r in files], 'complete_API_file_raw_reference':next({'capture_id':r['id'],'private_stdout':r['stdout']} for r in captures if r['command'][-1]=='repos/AlecKriebel/Math/pulls/368/files?per_page=100&page=1'),'literal_queue':{'physical_line':399,'cells':[8,9],'base_bytes':len(qbase),'merge_bytes':len(qmerge),'base_sha256':sha(qbase),'merge_sha256':sha(qmerge),'base_row':row_of(qbase).decode(),'accepted_row':row_of(qmerge).decode(),'all_other_queue_bytes_preserved':True},'all236_literal_published_checkpoint_files':pubfiles,'authorized_mutable_root_paths':sorted(MUTABLE),'all232_immutable_root_paths_preserved':True,'all130_nested_instances':nested,'all5_actual_author_checkpoint_identities':hist,'all42_historical_author_remote_bindings':rb,'prior_sealed_manifest_identities':seals,'all11_fresh_postmerge_sources':sources,'complete_controls':controls,'full14_drift_negative_output':negative,'literal_postmerge_negative_controls':negatives,'all_complete_program_replays':replays,'all_complete_command_captures':sorted(captures,key=lambda r:r['id']),'all_complete_JSON_parse_identity_records':jsons,'all_complete_API_tree_chunks':chunks,'EVERY_saved_gzip_inventory':{'path':'EVERY_SAVED_GZIP.json','bytes':len((RUN/'EVERY_SAVED_GZIP.json').read_bytes()),'sha256':sha((RUN/'EVERY_SAVED_GZIP.json').read_bytes()),'saved_gzip_streams':inv['saved_gzip_streams'],'private_raw_streams':inv['private_raw_streams'],'public_program_streams':inv['public_complete_program_streams']},'finite_assertions':{'author':128694,'historical':8664,'new_distinct_families':13339,'own':8387,'old_negatives':14,'literal_postmerge_negatives':7},'prior_source_math_final_seals_unchanged':True,'source_chronology':'All eleven new downloads occur during this post-merge audit only; original pre/post-seal access chronology is unchanged.','original_question':'unsolved5/5; only exact previously reviewed smooth-group/smooth-homogeneous/stabilizer classes accepted; no admissible counterexample or unrestricted solution','novelty_current_global_openness_or_human_review_certified':False,'no_paper_zenodo_doi_tracker_or_release':True,'read_only_git_API_and_no_external_person_contact':True,'review_subtask_completion_percent':100,'acceptance_publication_workflow_percent':98,'original_unrestricted_resolution_percent':0,'program_sha256':sha(Path(__file__).read_bytes())}
 result['check_count']=len(checks)
 (RUN/'RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','check_count','literal_merge','EVERY_saved_gzip_inventory','finite_assertions']},indent=2));print('RECEIPT_SHA256',sha((RUN/'RECEIPT.json').read_bytes()))
except BaseException:
 failure={'status':'FAIL_POST_AUDIT_NO_PASS_CREDIT','start_utc':start,'failed_utc':now(),'program_sha256':sha(Path(__file__).read_bytes()),'traceback':traceback.format_exc(),'checks':checks,'complete_captures':sorted(captures,key=lambda r:r['id']),'complete_json_records':jsons}
 try:failure['gzip_inventory']=inventory()
 except BaseException:failure['inventory_failure']=traceback.format_exc()
 (RUN/'FAILURE.json').write_text(json.dumps(failure,indent=2)+'\n');raise
