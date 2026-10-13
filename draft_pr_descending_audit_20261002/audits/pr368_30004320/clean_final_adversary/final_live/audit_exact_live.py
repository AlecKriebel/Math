#!/usr/bin/env python3
"""Independent read-only live acceptance gate. Unique labels preserve every run.
Writes only within this final_live directory. No fetch, Git mutation, or service write.
Default reruns are private; --publish-run selects the first public evidence run.
"""
from pathlib import Path,PurePosixPath
import argparse,base64,concurrent.futures,datetime,gzip,hashlib,json,os,re,shutil,subprocess,sys,threading,traceback,urllib.request
F=Path(__file__).resolve().parent;OWN=F.parent;A=OWN.parent;R=A.parents[2]
PREFIX='problems/30004320_laurent_descent';Q='unsolved_math_prioritization/QUEUE.md';AP=A.relative_to(R).as_posix()
HEAD='e8a53a05b309bda2a7d60136d8fb5a4e21e313fd';BASE='4b1fe16ffa841df9cefffe9479b05bbf950e423b';TREE='902a46b4ec28f332f7ef0228d8e6bca3736a0031'
ORIGINAL='74617174ddfb3ea726cea343a4ba915613724bdc';OLD_BASE='efd29c05204703acca9a0860812f54b94fae54b1';AUTHOR='b08662a16499edf37f0c0eae850cfa00b7778ed6'
BODY_SHA='99128f750a529174a631fd97600e4809f18c1054c0ef115b57e5838b4dff64fc';QUEUE_BASE_SHA='aa2470313317850d2a05f8f0cf0b9523fbc73169c3c72b59074d51f7b10bc5a2'
ORIGINAL_MF_SHA='bf7cece6ed2edc56f2b865baed9f0bcf9a13378511929c3f7f64d0cfb2144036'
CHECKPOINTS=['5e2eb63fd571f2f660ff9ebb436440029b5d1268','d7d898ba23e9d024e79b938e3e0e305d91bb125b','c800217d22d329d6ca397f3c18e5115c77688fb9','24ecf1f2f0ab62082f328545180e4b2ba1640ab7',AUTHOR]
PY=R/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
parser=argparse.ArgumentParser();parser.add_argument('--label',required=True);parser.add_argument('--publish-run',action='store_true');args=parser.parse_args()
assert re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,70}',args.label)
RUN=F/('runs' if args.publish_run else 'private_runs')/args.label;RUN.mkdir(parents=True,exist_ok=False)
STREAMS=RUN/'streams';STREAMS.mkdir();PRIVATE=RUN/'private';PRIVATE.mkdir();CAND=PRIVATE/'candidate';CAND.mkdir();SOURCE=PRIVATE/'sources';SOURCE.mkdir()
checks=[];captures=[];replays=[];json_reads=[];lock=threading.Lock();serial=0;started=datetime.datetime.now(datetime.timezone.utc).isoformat()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def ck(name,v,detail=None):
 row={'check':name,'pass':bool(v),'detail':detail};checks.append(row)
 if not v:raise AssertionError(name)
def full_json(b,label):
 j=json.loads(b);leaves=[]
 def walk(x,path):
  if isinstance(x,dict):
   for k,v in sorted(x.items()):walk(v,path+[k])
  elif isinstance(x,list):
   for i,v in enumerate(x):walk(v,path+[i])
  else:leaves.append([path,type(x).__name__,x])
 walk(j,[]);json_reads.append({'path':label,'bytes':len(b),'sha256':sha(b),'scalar_leaves':len(leaves),'all_scalar_leaf_map_sha256':sha(json.dumps(leaves,sort_keys=True,separators=(',',':')).encode())});return j
def stream_record(label,b):
 path=STREAMS/(label+'.gz');path.write_bytes(gzip.compress(b,mtime=0))
 return {'path':path.relative_to(RUN).as_posix(),'bytes':len(b),'sha256':sha(b),'gzip_bytes':path.stat().st_size,'gzip_sha256':sha(path.read_bytes())}
def capture(cmd,cwd=R,keep=True):
 global serial
 with lock:serial+=1;n=serial
 t0=now();p=subprocess.run(list(map(str,cmd)),cwd=cwd,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});t1=now()
 row={'id':n,'command':list(map(str,cmd)),'cwd':str(cwd),'start_utc':t0,'end_utc':t1,'exit_code':p.returncode}
 if keep:
  row['stdout']=stream_record(f'{n:05d}_stdout',p.stdout);row['stderr']=stream_record(f'{n:05d}_stderr',p.stderr)
 else:
  row['stdout']={'bytes':len(p.stdout),'sha256':sha(p.stdout),'retained':False,'reason':'Full recursive Git maps are compared in memory; complete canonical hashes and independently retained API chunks avoid duplicate huge raw listings.'};row['stderr']=stream_record(f'{n:05d}_stderr',p.stderr)
 with lock:captures.append(row)
 if p.returncode:raise RuntimeError({'command':row['command'],'exit_code':p.returncode,'stderr':p.stderr.decode(errors='replace')})
 return p.stdout
def git(*v,keep=True):return capture(['git',*v],keep=keep)
def get(rev,path):return git('show',rev+':'+path)
def api(endpoint):return full_json(capture(['gh','api','--method','GET','-H','Cache-Control: no-cache','repos/AlecKriebel/Math/'+endpoint]),'API '+endpoint)
def safe(path):
 p=PurePosixPath(path);ck('safe relative path '+path,not p.is_absolute() and '..' not in p.parts and p.as_posix()==path);return p
cache={}
def tree(rev):
 if rev in cache:return cache[rev]
 out={}
 for row in git('ls-tree','-r','-z','--full-tree',rev,keep=False).split(b'\0'):
  if row:
   meta,path=row.split(b'\t',1);mode,typ,oid=meta.decode().split();out[path.decode()]={'mode':mode,'type':typ,'sha':oid}
 cache[rev]=out;return out
def canon(j):return json.dumps(j,sort_keys=True,separators=(',',':')).encode()
def metadata(phase):
 ghpath=git('rev-parse','--git-path','MERGE_HEAD').decode().strip();ck(phase+' no active MERGE_HEAD',not (R/ghpath).exists())
 ck(phase+' local main checkout',git('branch','--show-current').decode().strip()=='main')
 refs={r:git('rev-parse',r).decode().strip() for r in ['HEAD','refs/heads/main','refs/remotes/origin/main']};ck(phase+' local main and origin pins',all(v==BASE for v in refs.values()),refs)
 remote=git('ls-remote','origin','refs/heads/main','refs/heads/math/30004320-laurent-descent-reviewed').decode().splitlines();rd={line.split()[1]:line.split()[0] for line in remote};ck(phase+' actual remote main and head pins',rd=={'refs/heads/main':BASE,'refs/heads/math/30004320-laurent-descent-reviewed':HEAD},rd)
 pull=api('pulls/368');ck(phase+' exact open ready PR metadata',pull['number']==368 and pull['state']=='open' and not pull['draft'] and not pull['merged'] and pull['merged_at'] is None and pull['head']['sha']==HEAD and pull['base']['sha']==BASE and pull['base']['ref']=='main' and pull['head']['ref']=='math/30004320-laurent-descent-reviewed' and pull['changed_files']==54)
 ck(phase+' whole accepted body hash',sha(pull['body'].encode())==BODY_SHA and pull['body'].encode()==(A/'accepted_pr_body.txt').read_bytes())
 main=api('git/ref/heads/main');href=api('git/ref/heads/math/30004320-laurent-descent-reviewed');ck(phase+' actual API main and head refs',main['object']['sha']==BASE and href['object']['sha']==HEAD)
 c=api('git/commits/'+HEAD);ck(phase+' live API commit tree and ordered parents',c['sha']==HEAD and c['tree']['sha']==TREE and [p['sha'] for p in c['parents']]==[ORIGINAL,BASE])
 ck(phase+' live actual Git tree and ordered parents',git('show','-s','--format=%T',HEAD).decode().strip()==TREE and git('show','-s','--format=%P',HEAD).decode().strip().split()==[ORIGINAL,BASE])
 ck(phase+' mergeable clean actual PR',pull['mergeable'] is True and pull['mergeable_state']=='clean')
 test=api('git/commits/'+pull['merge_commit_sha']);ck(phase+' actual GitHub test-merge tree and ordered parents',test['tree']['sha']==TREE and [p['sha'] for p in test['parents']]==[BASE,HEAD])
 return {'phase':phase,'utc':now(),'local_refs':refs,'remote_refs':rd,'pull':pull,'actual_commit':c,'test_merge_commit':test}
chunks=[];api_maps={}
def api_map(oid,prefix=''):
 if oid in api_maps:return {prefix+p:r for p,r in api_maps[oid].items()}
 j=api('git/trees/'+oid+'?recursive=1')
 ck('API requested exact tree identity '+oid,j['sha']==oid)
 if not j['truncated']:
  out={r['path']:{k:r[k] for k in ('mode','type','sha')} for r in j['tree'] if r['type']!='tree'}
  chunks.append({'tree':oid,'recursive':True,'entries':len(j['tree']),'truncated':False})
 else:
  # Reject the truncated response as a complete map and recursively obtain all chunks.
  j=api('git/trees/'+oid);ck('API nonrecursive untruncated '+oid,j['sha']==oid and j['truncated'] is False)
  chunks.append({'tree':oid,'recursive':False,'entries':len(j['tree']),'truncated':False,'truncated_recursive_response_not_credited':True});out={}
  for r in j['tree']:
   if r['type']=='tree':out.update(api_map(r['sha'],r['path']+'/'))
   else:out[r['path']]={k:r[k] for k in ('mode','type','sha')}
 api_maps[oid]=out;return {prefix+p:r for p,r in out.items()}
def api_blob(oid):
 j=api('git/blobs/'+oid);raw=base64.b64decode(j['content']);ck('actual API raw blob '+oid,j['encoding']=='base64' and j['sha']==oid and j['size']==len(raw) and blob(raw)==oid);return raw
api_blobs={}
def batch_blobs(oids):
 missing=sorted(set(oids)-api_blobs.keys())
 with concurrent.futures.ThreadPoolExecutor(6) as pool:
  for oid,b in zip(missing,pool.map(api_blob,missing)):api_blobs[oid]=b
configs=[('descent_cohomology_review',35,'ADVERSARIAL_CONTROLS.py','ADVERSARIAL_CONTROLS.stdout',1923,'INTEGRITY_REPLAY_RECEIPT.json',866),('residue_valuation_review',37,'residue_valuation_controls.py','RESIDUE_VALUATION_CONTROLS.json',3029,'ARTIFACT_REPRODUCTION.json',434),('clean_final_adversary',47,'adversarial_controls.py','ADVERSARIAL_CONTROLS.json',8387,'FROZEN_PROVENANCE_AND_REPLAY.json',618)]
def seal_bindings(root,name):
 j=full_json((root/name).read_bytes(),str(root.relative_to(A))+'/'+name)
 rows=j.get('files',[{'path':j['file'],'bytes':j['bytes'],'sha256':j['sha256']}] if 'file' in j else [])
 for r in rows:
  safe(r['path']);b=(root/r['path']).read_bytes();ck('immutable source/math binding '+str(root.name)+'/'+r['path'],len(b)==r['bytes'] and sha(b)==r['sha256'])
 return datetime.datetime.fromisoformat(j.get('sealed_utc',j.get('sealed_at')))
def run(label,argv,expected=None):
 b=capture([str(PY),'-B',*map(str,argv)],cwd=PRIVATE)
 ck('new complete program stdout '+label,expected is None or b==expected)
 rec=next(r for r in captures if r['command']==[str(PY),'-B',*map(str,argv)] and r['stdout']['sha256']==sha(b))
 ck('new empty program stderr '+label,rec['stderr']['bytes']==0)
 replays.append({'label':label,'capture_id':rec['id'],'command':rec['command'],'stdout':rec['stdout'],'stderr':rec['stderr'],'exit_code':rec['exit_code']});return b
try:
 before=metadata('before')
 own_mf=(OWN/'PUBLIC_MANIFEST.json').read_bytes();ck('literal unchanged original47 manifest SHA',sha(own_mf)==ORIGINAL_MF_SHA)
 ht=tree(HEAD);bt=tree(BASE);ot=tree(ORIGINAL);expected={r['path']:r for r in full_json((A/'snapshot_manifest.json').read_bytes(),'snapshot_manifest.json')['files']}
 ck('entire live base-to-head map delta exactly54',len(expected)==54 and {p for p in ht.keys()|bt.keys() if ht.get(p)!=bt.get(p)}==set(expected))
 ck('complete actual53 target scope',sum(p.startswith(PREFIX+'/') for p in expected)==53 and {p for p in ht if p.startswith(PREFIX+'/')}==set(expected)-{Q})
 ck('all53 frozen target entries unchanged modes/blobs',all(ht[p]==ot[p]=={'mode':'100644','type':'blob','sha':r['git_blob_sha']} for p,r in expected.items() if p!=Q))
 # Verify entire API root maps; repeated tree identities use only exact subtree cache.
 amap=api_map(TREE);ck('entire actual head Git/API leaf map',amap==ht,{'entries':len(ht),'canonical_sha256':sha(canon(ht))})
 btree=git('show','-s','--format=%T',BASE).decode().strip();bmap=api_map(btree);ck('entire actual base Git/API leaf map',bmap==bt,{'entries':len(bt),'canonical_sha256':sha(canon(bt))})
 files=api('pulls/368/files?per_page=100&page=1');ck('complete actual54 API file scope',len(files)==54 and {r['filename'] for r in files}==set(expected))
 ck('actual API pagination exhausted',api('pulls/368/files?per_page=100&page=2')==[])
 batch_blobs(ht[p]['sha'] for p in expected)
 livefiles=[]
 for p in sorted(expected):
  raw=get(HEAD,p);ar=api_blobs[ht[p]['sha']];ck('actual live Git/API mode bytes '+p,ar==raw and ht[p]['mode']=='100644' and ht[p]['type']=='blob' and blob(raw)==ht[p]['sha'])
  fr=next(r for r in files if r['filename']==p);ck('full live API file status/blob '+p,fr['sha']==ht[p]['sha'] and fr['status']==('modified' if p==Q else 'added'))
  if p!=Q:
   r=expected[p];ck('whole frozen target disk equality '+p,raw==(A/'snapshot'/p).read_bytes() and len(raw)==r['bytes'] and sha(raw)==r['sha256']);f=CAND/p.removeprefix(PREFIX+'/');f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(raw)
  livefiles.append({'path':p,**ht[p],'bytes':len(raw),'sha256':sha(raw)})
 qbase=get(BASE,Q);qhead=get(HEAD,Q);ck('literal complete live base queue SHA',sha(qbase)==QUEUE_BASE_SHA)
 ql=qbase.splitlines(keepends=True);indices=[i for i,l in enumerate(ql) if len(l.split(b'|'))>9 and l.split(b'|')[2].strip().split()[:1]==[b'30004320']]
 ck('physical unique line399',indices==[398]);qc=ql[398].split(b'|');ck('before queued0 own cells',qc[8].strip()==b'queued' and qc[9].strip()==b'0/5');qc[8:10]=[b' unsolved ',b' 5/5 '];ql[398]=b'|'.join(qc);ck('entire queue only own status/turn cells',b''.join(ql)==qhead)
 queue={'physical_line':399,'changed_cells':[8,9],'base_sha256':sha(qbase),'head_sha256':sha(qhead),'base_bytes':len(qbase),'head_bytes':len(qhead),'all_other_bytes_preserved':True}
 # Every nested manifest, chain and actual historical identity is inspected again.
 nested=[];manifest_rows=[]
 for name in [f'TURN_{i}_MANIFEST.json' for i in range(1,6)]+['FINAL_AUTHOR_MANIFEST.json','review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']:
  raw=(CAND/name).read_bytes();j=full_json(raw,'candidate/'+name);seen=set()
  for r in j['files']:
   safe(r['path']);ck('unique nested binding '+name+'/'+r['path'],r['path'] not in seen);seen.add(r['path']);b=(CAND/name).parent.joinpath(r['path']).read_bytes();ck('full nested binding '+name+'/'+r['path'],len(b)==r['bytes'] and sha(b)==r['sha256']);nested.append({'manifest':name,**r})
  if name.startswith('TURN_'):
   i=int(name.split('_')[1]);ck('turn ordinal '+name,j['author_turns_used']==i)
   if i>1:ck('original manifest chain '+name,j['previous_manifest_sha256']==sha((CAND/f'TURN_{i-1}_MANIFEST.json').read_bytes()))
  manifest_rows.append({'path':name,'bytes':len(raw),'sha256':sha(raw),'bindings':len(seen)})
 ck('all eight130 nested instances',len(nested)==130 and len(manifest_rows)==8)
 pub=full_json((CAND/'PUBLICATION_MANIFEST.json').read_bytes(),'candidate/publication');ck('closed52 publication target scope',set(r['path'] for r in pub['files'])=={p.removeprefix(PREFIX+'/') for p in expected if p!=Q}-{ 'PUBLICATION_MANIFEST.json'})
 ck('qualified unsolved5 outcome',pub['status']=='unsolved' and pub['turns']=='5/5')
 prior=OLD_BASE;history=[]
 for i,c in enumerate(CHECKPOINTS,1):
  cj=api('git/commits/'+c);parents=git('show','-s','--format=%P',c).decode().strip().split();coid=git('show','-s','--format=%T',c).decode().strip();ck('actual Git/API author checkpoint '+str(i),parents==[prior] and [p['sha'] for p in cj['parents']]==parents and cj['sha']==c and cj['tree']['sha']==coid)
  for n in range(1,i+1):
   mj=full_json((CAND/f'TURN_{n}_MANIFEST.json').read_bytes(),'historical/'+str(i)+'/'+str(n))
   for p in [f'TURN_{n}_MANIFEST.json']+[r['path'] for r in mj['files']]:ck('full actual retained checkpoint bytes '+str(i)+'/'+p,get(c,PREFIX+'/'+p)==(CAND/p).read_bytes())
  history.append(cj);prior=c
 author=full_json((CAND/'FINAL_AUTHOR_MANIFEST.json').read_bytes(),'candidate/author');authorpaths={r['path'] for r in author['files']}|{'FINAL_AUTHOR_MANIFEST.json'};at=tree(AUTHOR);ck('full actual42 historical author subtree',{p.removeprefix(PREFIX+'/') for p in at if p.startswith(PREFIX+'/')}==authorpaths and len(authorpaths)==42)
 rb=full_json((CAND/'review/REMOTE_BINDING.json').read_bytes(),'candidate/oldremote');ck('historical remote42 exact scope',rb['head']==AUTHOR and rb['folder']==PREFIX and {r['path'] for r in rb['files']}==authorpaths)
 for r in rb['files']:
  raw=get(AUTHOR,PREFIX+'/'+r['path']);ck('actual42 historical raw remote binding '+r['path'],raw==(CAND/r['path']).read_bytes() and len(raw)==r['size'] and blob(raw)==r['git_blob_sha']==at[PREFIX+'/'+r['path']]['sha'])
 for p in [p for p in ht if p.startswith(PREFIX+'/review/')]:ck('historical seven review additions absent author '+p,p not in at)
 # Published whole audit scope, not only selected family path projections.
 published={p:entry for p,entry in bt.items() if p.startswith(AP+'/')};ck('complete236 published root audit paths',len(published)==236 and all(ht[p]==entry for p,entry in published.items()))
 batch_blobs(entry['sha'] for entry in published.values());published_rows=[];published_bytes={}
 for p,entry in sorted(published.items()):
  b=get(BASE,p);ck('actual published Git/API/root file '+p,entry['mode']=='100644' and entry['type']=='blob' and b==api_blobs[entry['sha']] and blob(b)==entry['sha']);published_bytes[p]=b
  if p.endswith('.json'):full_json(b,'published/'+p)
  published_rows.append({'path':p,**entry,'bytes':len(b),'sha256':sha(b)})
 # Full root receipts and immutable seals; mutable top-level working logs are not snapshot evidence.
 rootrec=full_json(published_bytes[AP+'/root_original_reproduction_receipt.json'],'published root original receipt');rootfamilies=full_json(published_bytes[AP+'/root_family_control_reproduction.json'],'published root family receipt')
 for name,j,count in [('root frozen',rootrec,501),('root families',rootfamilies,3310)]:
  ck(name+' full successful records',j['status']=='PASS' and j['check_count']==len(j['checks'])==count)
  for n,r in enumerate(j['checks']):ck(name+' every check '+str(n),r['pass'] is True)
 for name in ['ROOT_SOURCE_FIRST_SEAL.json','ROOT_MATHEMATICAL_SEAL.json']:
  sj=full_json(published_bytes[AP+'/'+name],name);rb0=published_bytes[AP+'/'+sj['file']];ck('root immutable published '+name,len(rb0)==sj['bytes'] and sha(rb0)==sj['sha256'] and rb0==(A/sj['file']).read_bytes() and published_bytes[AP+'/'+name]==(A/name).read_bytes())
 root_math_time=seal_bindings(A,'ROOT_MATHEMATICAL_SEAL.json');root_source_time=seal_bindings(A,'ROOT_SOURCE_FIRST_SEAL.json');ck('root source before mathematical seal',root_source_time<root_math_time)
 root_primary=full_json(published_bytes[AP+'/root_primary_fetch_receipt.json'],'root primary acquisition');root_extra=full_json(published_bytes[AP+'/root_supplemental_fetch_receipt.json'],'root supplementary acquisition')
 for r in root_primary+root_extra:
  b=(A/'raw_sources'/r['name']).read_bytes();ck('actual root retained fresh primary '+r['name'],len(b)==r['bytes'] and sha(b)==r['sha256'] and r['historical_pdf_bytes_equal'] and r['historical_pdf_sha256_equal']);t0=datetime.datetime.fromisoformat(r['started_utc']);t1=datetime.datetime.fromisoformat(r['completed_utc']);ck('root actual primary access chronology '+r['name'],t0<=t1<(root_source_time if r in root_primary else root_math_time) and (r in root_primary or t0>root_source_time))
 families=[];familyfiles=[]
 for family,count,program,output,ncontrols,receipt,nchecks in configs:
  D=A/family;mf_raw=published_bytes[AP+'/'+family+'/PUBLIC_MANIFEST.json'];mf=full_json(mf_raw,'family/'+family+'/PUBLIC_MANIFEST.json');ck('family published manifest unchanged '+family,mf_raw==(D/'PUBLIC_MANIFEST.json').read_bytes())
  scope={r['path'] for r in mf['files']};ck('unique closed family count '+family,len(scope)==len(mf['files'])==count and {p.removeprefix(AP+'/'+family+'/') for p in published if p.startswith(AP+'/'+family+'/')}==scope|{'PUBLIC_MANIFEST.json'})
  for r in mf['files']:
   safe(r['path']);disk=D/r['path'];raw=published_bytes[AP+'/'+family+'/'+r['path']];ck('entire original family bound disk/Git/API '+family+'/'+r['path'],not disk.is_symlink() and disk.resolve().is_relative_to(D.resolve()) and raw==disk.read_bytes() and len(raw)==r['bytes'] and sha(raw)==r['sha256']);familyfiles.append({'family':family,**r})
  tsource=seal_bindings(D,'SOURCE_FIRST_SEAL.json');tmath=seal_bindings(D,'MATHEMATICAL_SEAL.json');ck('independent pre-root source/math chronology '+family,tsource<tmath<root_math_time)
  if family=='clean_final_adversary':
   fs=full_json((D/'FINAL_SEAL.json').read_bytes(),'own final seal')
   for r in fs['bindings']:
    raw=(D/r['path']).read_bytes();ck('immutable original final binding '+r['path'],len(raw)==r['bytes'] and sha(raw)==r['sha256'])
  j=full_json((D/receipt).read_bytes(),'family/'+family+'/'+receipt);ck('full family check count '+family,len(j['checks'])==j.get('check_count',j.get('checks_count'))==nchecks)
  for n,r in enumerate(j['checks']):
   ck('every prior full typed family record '+family+'/'+str(n),isinstance(r,(dict,str)))
   if isinstance(r,dict) and 'pass' in r:ck('every prior family PASS '+family+'/'+str(n),r['pass'] is True)
  if family=='descent_cohomology_review':
   srcrows=full_json((D/'SOURCE_ACQUISITION.json').read_bytes(),'family first sources')['sources'];filesrc=lambda r:D/'private/sources'/(r['id']+'.pdf')
  elif family=='residue_valuation_review':
   pr=full_json((D/'PRIMARY_SOURCE_RECEIPT.json').read_bytes(),'family second primary')['sources'];er=full_json((D/'SUPPLEMENTARY_SOURCE_RECEIPT.json').read_bytes(),'family second extra')['sources'];srcrows=pr+er;filesrc=lambda r:D/'private'/r['name']
  else:srcrows=full_json((D/'SOURCE_DOWNLOAD_RECEIPT.json').read_bytes(),'family third sources');filesrc=lambda r:D/'private_sources'/r['name']
  ck('all11 unique family source identities '+family,len(srcrows)==11 and {(r['url'],r['bytes'],r['sha256']) for r in srcrows}=={(r['url'],r['bytes'],r['sha256']) for r in rootrec['primary_sources']})
  for r in srcrows:
   raw=filesrc(r).read_bytes();ck('actual independent retained source '+family+'/'+r['url'],len(raw)==r['bytes'] and sha(raw)==r['sha256'])
   if family=='clean_final_adversary':ck('own original download precedes source seal '+r['name'],datetime.datetime.fromisoformat(r['download_start_utc'])<=datetime.datetime.fromisoformat(r['download_end_utc'])<tsource)
   if family=='residue_valuation_review':
    t0=datetime.datetime.fromisoformat(r['access_started_utc']);t1=datetime.datetime.fromisoformat(r['access_finished_utc']);ck('residue actual download phase '+r['name'],t0<=t1<(tsource if r in pr else tmath) and (r in pr or t0>tsource))
  families.append({'family':family,'bound_files':count,'manifest_sha256':sha(mf_raw),'source_sealed_utc':tsource.isoformat(),'math_sealed_utc':tmath.isoformat(),'receipt':receipt,'all_prior_check_records':nchecks,'control_program':program,'control_output':output,'exact_controls':ncontrols,'prior_replays':j.get('replays',j.get('streams'))})
 ck('all119 original family bindings plus three manifests',len(familyfiles)==119 and len(families)==3)
 # Fresh live downloads occur now, never attributed to the earlier source/math seals.
 routes=[]
 for name in ['SOURCE_MANIFEST.json','SOURCE_ADDITION_T1.json','SOURCE_ADDITION_T4.json','SOURCE_ADDITION_T5.json']:routes+=full_json((CAND/name).read_bytes(),'fresh routes/'+name)['files']
 def fresh(r):
  t0=now();req=urllib.request.Request(r['url'],headers={'User-Agent':'Independent exact live mathematical provenance audit'})
  with urllib.request.urlopen(req,timeout=60) as resp:b=resp.read();final=resp.geturl()
  (SOURCE/r['name']).write_bytes(b);return {**r,'live_download_start_utc':t0,'live_download_end_utc':now(),'final_url':final,'actual_bytes':len(b),'actual_sha256':sha(b)}
 with concurrent.futures.ThreadPoolExecutor(5) as pool:sources=list(pool.map(fresh,routes))
 for r in sources:ck('new live fresh exact primary '+r['name'],r['actual_bytes']==r['bytes'] and r['actual_sha256']==r['sha256'])
 ck('all11 unique newly downloaded live source identities',len(sources)==len({r['name'] for r in sources})==11)
 # Complete output contracts are assembled independently, including portable no-source JSON.
 std={f'author{i}':(CAND/f'TURN_{i}_CHECKS.json').read_bytes() for i in range(1,6)};std['historical_review']=(CAND/'review/INDEPENDENT_CHECKS.json').read_bytes();sout=(CAND/'review/AUTHOR_REPLAY.json').read_bytes();ns=json.loads(sout);ns.update(source_check='not requested; raw sources are not distributed',source_pdfs_checked=0);nout=(json.dumps(ns,indent=2,sort_keys=True)+'\n').encode();vout=b'PASS: review hashes, frozen author/remote binding, and independent replay\n';end=b'PASS: all publication bytes, frozen author proofs and independent review; original unsolved 5/5\n'
 std.update(packet_with_sources=sout,packet_without_sources=nout,review_wrapper=vout,publication_with_sources=sout+vout+end,publication_without_sources=nout+vout+end)
 aliases={'historical_review_controls':'historical_review','historical_independent':'historical_review','prior_independent':'historical_review','author_wrapper':'packet_with_sources','historical_review_wrapper':'review_wrapper','review':'review_wrapper','publication_no_sources':'publication_without_sources'}
 def key(label):
  if label.startswith('author_turn_'):return 'author'+label.rsplit('_',1)[1]
  if label.startswith('author_') and label[7:].isdigit():return 'author'+label[7:]
  return aliases.get(label,label)
 for fam in families:
  D=A/fam['family'];streamroot=D if fam['family']=='descent_cohomology_review' else D/'replay_streams';ck('all10 complete family stream pairs '+fam['family'],len(fam['prior_replays'])==10)
  for row in fam['prior_replays']:
   label=row['label'];b=(streamroot/(label+'.stdout')).read_bytes();err=(streamroot/(label+'.stderr')).read_bytes();ck('entire stored family output '+fam['family']+'/'+label,b==std[key(label)] and len(b)==row['stdout_bytes'] and sha(b)==row['stdout_sha256'] and err==b'' and sha(err)==row['stderr_sha256'] and row.get('returncode',row.get('exit_code'))==0)
 for row in rootrec['replays']:
  label=row['label'];b=published_bytes[AP+'/root_original_streams/'+label+'.stdout'];err=published_bytes[AP+'/root_original_streams/'+label+'.stderr'];ck('entire root stored output '+label,b==std[label] and b.decode()==row['complete_output'] and len(b)==row['stdout_bytes'] and sha(b)==row['stdout_sha256'] and err==b'' and row['exit']==0)
 commands=[(f'author{i}',[CAND/f'check_turn_{i}.py']) for i in range(1,6)]+[('historical_review',[CAND/'review/independent_checks.py']),('packet_with_sources',[CAND/'verify_packet.py','--source-dir',SOURCE]),('packet_without_sources',[CAND/'verify_packet.py']),('review_wrapper',[CAND/'review/verify_review.py','--author-dir',CAND]),('publication_with_sources',[CAND/'verify_publication.py','--source-dir',SOURCE]),('publication_without_sources',[CAND/'verify_publication.py'])]
 for label,argv in commands:run(label,argv,std[label])
 for fam in families:
  D=A/fam['family'];b=run('controls_'+fam['family'],[D/fam['control_program']],(D/fam['control_output']).read_bytes());j=full_json(b,'new controls/'+fam['family']);ck('actual distinct finite control count '+fam['family'],j['status']=='PASS' and j['exact_assertions']==fam['exact_controls'])
  priorcontrol=published_bytes[AP+'/root_family_control_streams/'+fam['family']+'.stdout'];ck('root stored complete control output '+fam['family'],priorcontrol==b and published_bytes[AP+'/root_family_control_streams/'+fam['family']+'.stderr']==b'')
  verify='verify_family_manifest.py' if fam['family']=='descent_cohomology_review' else 'verify_manifest.py';vb=run('manifest_'+fam['family'],[D/verify]);ck('actual immutable manifest validator '+fam['family'],json.loads(vb)['status']=='PASS')
 # Read all 14 old negative records and root adaptation with complete tracebacks.
 originalneg=full_json((OWN/'DRIFT_NEGATIVES.json').read_bytes(),'original14 negatives');rootneg=rootfamilies['full_negative_output'];ck('full negative record counts',originalneg['negative_controls']==rootneg['negative_controls']==14 and len(originalneg['results'])==len(rootneg['results'])==14)
 for x,y in zip(originalneg['results'],rootneg['results']):
  ck('entire same negative shape '+x['control'],x.keys()==y.keys() and x['control']==y['control'] and x['rejected'] is y['rejected'] is True)
  for k in x:
   if k not in ['stderr_bytes','stderr_sha256']:ck('entire negative metadata '+x['control']+'/'+k,x[k]==y[k])
  if 'exit_code' in x:
   b=(OWN/(x['control']+'.stderr')).read_bytes();ck('actual original full negative traceback '+x['control'],len(b)==x['stderr_bytes'] and sha(b)==x['stderr_sha256'] and (OWN/(x['control']+'.stdout')).read_bytes()==b'')
 # Rerun the old negatives only after exact path adaptation in this new private run.
 old=OWN/'drift_negatives.py';code=old.read_text();needle="HERE=Path(__file__).resolve().parent;REPO=HERE.parents[3];CAND=HERE.parent/'snapshot/problems/30004320_laurent_descent';PYTHON=REPO/";ck('unique exact drift path adaptation',code.count(needle)==1)
 new=f"HERE=Path({str(PRIVATE)!r});REPO=Path({str(R)!r});CAND=Path({str(CAND)!r});PYTHON=REPO/";code=code.replace(needle,new);needle2="(HERE.parent/'snapshot'/Q)";ck('unique original queue fixture adaptation',code.count(needle2)==1);code=code.replace(needle2,f"(Path({str(A/'snapshot')!r})/Q)");shadow=PRIVATE/'drift_negatives.py';shadow.write_text(code)
 b=run('drift14_private',[shadow]);j=full_json(b,'new14 negatives');ck('new14 full negative shape',j.keys()==originalneg.keys() and j['negative_controls']==14 and len(j['results'])==14)
 for x,y in zip(originalneg['results'],j['results']):
  ck('new full negative record '+x['control'],x.keys()==y.keys() and x['control']==y['control'] and x['rejected'] is y['rejected'] is True)
  for k in x:
   if k not in ['stderr_bytes','stderr_sha256']:ck('new entire negative metadata '+x['control']+'/'+k,x[k]==y[k])
  if 'exit_code' in x:
   ob=(OWN/(x['control']+'.stderr')).read_bytes();nb=(PRIVATE/(x['control']+'.stderr')).read_bytes();ck('full exact negative traceback after private root '+x['control'],ob.replace(str(OWN/'private_controls').encode(),b'OWNED_PRIVATE')==nb.replace(str(PRIVATE/'private_controls').encode(),b'OWNED_PRIVATE') and len(nb)==y['stderr_bytes'] and sha(nb)==y['stderr_sha256']);stream_record('negative_'+x['control']+'_stderr',nb);stream_record('negative_'+x['control']+'_stdout',(PRIVATE/(x['control']+'.stdout')).read_bytes())
 # Additional literal live predicates, rather than the older placeholder body predicate.
 def exact_pins(p,h,b,t,body):return p['state']=='open' and p['draft'] is False and p['head']['sha']==h==HEAD and p['base']['sha']==b==BASE and t==TREE and sha(body.encode())==BODY_SHA
 p=before['pull'];ck('actual literal live pin predicate',exact_pins(p,HEAD,BASE,TREE,p['body']))
 negative_live=[]
 for label,field in [('head','head'),('base','base'),('body','body'),('tree','tree'),('draft','draft'),('state','state')]:
  q=json.loads(json.dumps(p));h=HEAD;b=BASE;t=TREE;body=p['body']
  if field=='head':h='0'*40;q['head']['sha']=h
  elif field=='base':b='0'*40;q['base']['sha']=b
  elif field=='body':body+=' ';q['body']=body
  elif field=='tree':t='0'*40
  elif field=='draft':q['draft']=True
  else:q['state']='closed'
  ck('literal live metadata negative '+label,not exact_pins(q,h,b,t,body));negative_live.append({'mutation':label,'rejected':True})
 after=metadata('after')
 ck('original47 MF unchanged at end',(OWN/'PUBLIC_MANIFEST.json').read_bytes()==own_mf)
 # No mutable-root logs are substituted for the published checkpoint's exact versions.
 disk_drift=[p for p,b in published_bytes.items() if (R/p).exists() and (R/p).read_bytes()!=b];ck('published immutable root/family material unchanged on disk',set(disk_drift)<= {AP+'/README.md',AP+'/RESEARCH_LOG.md'},disk_drift)
 result={'status':'PASS exact live acceptance as unsolved5/5; actual merge pending','start_utc':started,'end_utc':now(),'pins':{'head':HEAD,'base':BASE,'tree':TREE,'ordered_parents':[ORIGINAL,BASE],'accepted_body_sha256':BODY_SHA,'base_complete_queue_sha256':QUEUE_BASE_SHA},'before':before,'after':after,'check_count':len(checks),'checks':checks,'complete_recursive_maps':{'head_entries':len(ht),'head_canonical_sha256':sha(canon(ht)),'base_entries':len(bt),'base_canonical_sha256':sha(canon(bt)),'complete_api_chunks':chunks},'all54_actual_API_PR_files':files,'all54_actual_files':livefiles,'queue':queue,'all130_nested_binding_instances':nested,'all8_manifests':manifest_rows,'all5_actual_author_checkpoint_API_records':history,'all42_historical_remote_bindings':rb,'all236_published_files':published_rows,'all119_original_family_bindings':familyfiles,'families':families,'all11_new_live_source_retrievals':sources,'full_json_all_leaf_reads':json_reads,'complete_captures':sorted(captures,key=lambda x:x['id']),'complete_program_replays':replays,'live_metadata_negative_controls':negative_live,'old_drift_negative_controls':j,'published_root_working_log_drift':disk_drift,'source_chronology':'Original source/math/final seals unchanged. Full relevant sources and supplementary post-seal read chronology retained. These eleven new retrievals occur during exact-live audit only.','mathematical_acceptance_scope':'Smooth affine acting group; smooth schematic/fppf homogeneous variety; exact stabilizer classes only. Original arbitrary-field problem unsolved, no admissible counterexample, novelty/current-global-openness/human peer review not certified.','finite_controls':{'author':128694,'historical':8664,'new_distinct_families':13339,'own_new':8387,'old_negatives_replayed':14,'additional_literal_live_negatives':6},'foundational_source_theorems_independently_reproved':False,'historical_exhaustive_ref_search_reenacted':False,'read_only_git_and_services':True,'actual_merge_and_postmerge_pending':True,'program_sha256':sha(Path(__file__).read_bytes())}
 (RUN/'RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'check_count':len(checks),'all_published_files':236,'family_files':119,'fresh_sources':11,'program_replays':len(replays),'run':str(RUN),'receipt_sha256':sha((RUN/'RECEIPT.json').read_bytes())},indent=2))
except BaseException:
 failure={'status':'FAIL; no acceptance credited','start_utc':started,'failure_utc':now(),'program_sha256':sha(Path(__file__).read_bytes()),'traceback':traceback.format_exc(),'checks':checks,'complete_captures':sorted(captures,key=lambda x:x['id']),'full_json_all_leaf_reads':json_reads,'read_only_git_and_services':True}
 (RUN/'FAILURE.json').write_text(json.dumps(failure,indent=2)+'\n');raise
