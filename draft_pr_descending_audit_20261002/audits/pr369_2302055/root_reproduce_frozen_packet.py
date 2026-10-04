"""Root literal frozen Git/API/history/source audit and complete-output replay."""
from pathlib import Path, PurePosixPath
import base64, concurrent.futures, datetime, hashlib, json, subprocess
A=Path(__file__).resolve().parent; R=A.parents[2]
PREFIX='unsolved_math_prioritization/attempts/2302055/'; Q='unsolved_math_prioritization/QUEUE.md'
PY=R/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
D=A/'snapshot'/PREFIX; PRIVATE=A/'tmp/root_original'; PRIVATE.mkdir(parents=True,exist_ok=True)
STREAMS=A/'root_original_streams'; STREAMS.mkdir(exist_ok=True); checks=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def ck(c,name):
    checks.append({'name':name,'pass':bool(c)}); assert c,name
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def get(rev,path):return git('show',rev+':'+path)
def tree(rev):
    rows={}
    for row in git('ls-tree','-rz','--full-tree',rev).split(b'\0'):
        if row:
            meta,path=row.split(b'\t',1);rows[path.decode()]=meta.decode()
    return rows
m=json.loads((A/'snapshot_manifest.json').read_bytes()); HEAD=m['head']; BASE=m['base']
ck(HEAD=='d9e4600d05b8272fe913a22ae7dcc0fbe0a26344','literal original head')
ck(BASE=='efd29c05204703acca9a0860812f54b94fae54b1','literal original base')
bt=tree(BASE);ht=tree(HEAD);expected={e['path'] for e in m['files']}
ck(len(expected)==50 and expected=={p for p in bt.keys()|ht.keys() if bt.get(p)!=ht.get(p)},'all-root literal50 path/mode/type/blob scope')
ck({p for p in ht if p.startswith(PREFIX)}==expected-{Q},'complete49 actual target paths')
ck({PREFIX+p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file()}==expected-{Q},'complete49 disk target paths')
def remote(row):
    path=row['path'];res=subprocess.run(['gh','api','repos/AlecKriebel/Math/contents/'+path+'?ref='+HEAD],cwd=R,capture_output=True)
    (PRIVATE/(path.replace('/','__')+'.api.stdout')).write_bytes(res.stdout)
    (PRIVATE/(path.replace('/','__')+'.api.stderr')).write_bytes(res.stderr)
    assert res.returncode==0 and not res.stderr,path
    obj=json.loads(res.stdout);raw=base64.b64decode(obj['content']);local=(A/'snapshot'/path).read_bytes()
    return {'path':path,'bytes':len(raw),'sha256':sha(raw),'git_blob':blob(raw),'git_entry':ht[path],
            'pass':raw==local==get(HEAD,path) and len(raw)==row['bytes']==obj['size'] and sha(raw)==row['sha256'] and blob(raw)==row['git_blob_sha']==obj['sha'] and ht[path].split()==['100644','blob',blob(raw)]}
remote_rows=list(concurrent.futures.ThreadPoolExecutor(8).map(remote,m['files']))
for row in remote_rows:ck(row['pass'],'literal frozen Git/API/disk '+row['path'])
bindings=[];manifests=[]
for name in ['SOURCE_GATE_MANIFEST.json',*[f'TURN_{i}_MANIFEST.json' for i in range(1,6)],'FINAL_AUTHOR_MANIFEST.json','review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']:
    mf=D/name;obj=json.loads(mf.read_bytes());root=mf.parent;seen=set()
    for row in obj['files']:
        rel=PurePosixPath(row['path']);ck(not rel.is_absolute() and '..' not in rel.parts and row['path'] not in seen,'safe nested path '+name+' '+row['path']);seen.add(row['path'])
        f=root/rel;raw=f.read_bytes();ck(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'full nested binding '+name+' '+row['path'])
        bindings.append({'manifest':name,'path':f.relative_to(D).as_posix(),'bytes':len(raw),'sha256':sha(raw),'pass':True})
    manifests.append({'path':name,'bytes':mf.stat().st_size,'sha256':sha(mf.read_bytes()),'bound_files':len(seen)})
ck(len(manifests)==9 and len(bindings)==211,'all nine manifests and211 binding instances')
pub=json.loads((D/'PUBLICATION_MANIFEST.json').read_bytes())
ck({e['path'] for e in pub['files']}=={p.removeprefix(PREFIX) for p in expected-{Q,PREFIX+'PUBLICATION_MANIFEST.json'}},'exact self-excluded48-file publication manifest')
commits=['6a6164860d7f46a1073babeab9665b3546e2f55d','68c823a4613c38b4af556f9dffbc3d4320aff0b8','d8dab0657462712e7719c3aca697a6c117638586','6e620ae93e637be90f6ea7fd63e4f9cc9346fc46','81b9b389012ec79645c73e8d1196aa6b955fb531']
checkpoint_rows=[]
for i,commit in enumerate(commits,1):
    ck(git('show','-s','--format=%P',commit).decode().strip()==(BASE if i==1 else commits[i-2]),'actual author checkpoint parent '+str(i))
    obj=json.loads((D/f'TURN_{i}_MANIFEST.json').read_bytes());paths={e['path'] for e in obj['files']}|{f'TURN_{i}_MANIFEST.json'}
    for path in sorted(paths):ck(get(commit,PREFIX+path)==(D/path).read_bytes(),'actual checkpoint'+str(i)+' '+path)
    checkpoint_rows.append({'turn':i,'commit':commit,'bound_files_plus_manifest':len(paths),'pass':True})
author=json.loads((D/'FINAL_AUTHOR_MANIFEST.json').read_bytes());author_paths={e['path'] for e in author['files']}|{'FINAL_AUTHOR_MANIFEST.json'}
ck(len(author_paths)==40,'forty final author files')
for path in sorted(author_paths):ck(get(commits[-1],PREFIX+path)==get(HEAD,PREFIX+path),'final author anchor '+path)
ck(git('show','-s','--format=%P',HEAD).decode().strip().split()==[BASE,commits[-1]],'frozen head actual parents')
review=json.loads((D/'review/REVIEW_MANIFEST.json').read_bytes());ck(review['author_manifest_sha256']==sha((D/'FINAL_AUTHOR_MANIFEST.json').read_bytes()),'historical review exact author-manifest anchor')
before=get(BASE,Q);lines=before.splitlines(keepends=True);found=[i for i,l in enumerate(lines) if len(l.split(b'|'))>9 and l.split(b'|')[2].strip().split(b' / ')[0]==b'2302055'];ck(len(found)==1,'unique original queue row')
i=found[0];cells=lines[i].split(b'|');ck([cells[j].strip() for j in [8,9]]==[b'queued',b'0/5'],'original queued0/5 cells')
cells[8:10]=[b' unsolved ',b' 5/5 '];lines[i]=b'|'.join(cells);ck(b''.join(lines)==get(HEAD,Q),'whole original queue changes only own status and turns')
sources=json.loads((D/'SOURCE_MANIFEST.json').read_bytes())['sources']+[json.loads((D/'SOURCE_ADDITION_T4.json').read_bytes())['source']]
source_rows=[]
for row in sources:
    raw=(A/'raw_sources'/row['file']).read_bytes();ck(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'fresh historical primary '+row['file']);source_rows.append({'file':row['file'],'url':row['url'],'bytes':len(raw),'sha256':sha(raw),'pass':True})
ck(len(source_rows)==5,'five fresh exact historical PDF identities')
seal=json.loads((A/'ROOT_MATHEMATICAL_SEAL.json').read_bytes());ck(sha((A/seal['file']).read_bytes())==seal['sha256'],'root pre-code mathematical seal unchanged')
commands=[(f'author{i}',[str(PY),str(D/f'verify_turn{i}.py')],D/f'TURN_{i}_CHECKS.json') for i in range(1,6)]
commands += [('historical_review',[str(PY),str(D/'review/independent_check.py')],D/'review/INDEPENDENT_CHECKS.json'),('author_replay_wrapper',[str(PY),str(D/'review/replay_author.py'),str(D)],D/'review/AUTHOR_REPLAY.json')]
replays=[]
for label,args,old in commands:
    result=subprocess.run(args,cwd=PRIVATE,capture_output=True);(STREAMS/(label+'.stdout')).write_bytes(result.stdout);(STREAMS/(label+'.stderr')).write_bytes(result.stderr)
    ck(result.returncode==0 and not result.stderr,'full replay exit '+label);ck(result.stdout==old.read_bytes(),'full byte-exact replay '+label)
    replays.append({'label':label,'exit':result.returncode,'stdout_bytes':len(result.stdout),'stdout_sha256':sha(result.stdout),'stderr_bytes':len(result.stderr),'stderr_sha256':sha(result.stderr),'complete_output':json.loads(result.stdout)})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','frozen_head':HEAD,'original_base':BASE,'checks':checks,'check_count':len(checks),'remote_files':remote_rows,'manifests':manifests,'nested_bindings':bindings,'nested_binding_instances':211,'actual_author_checkpoints':checkpoint_rows,'final_author_files':40,'review_files_plus_manifest':6,'historical_review_first_parent_anchor_claimed':False,'primary_sources':source_rows,'demailly_scans_text_recovered':False,'replays':replays,'author_assertions':sum(r['complete_output']['exact_assertions'] for r in replays[:5]),'historical_review_assertions':replays[5]['complete_output']['independent_assertions'],'root_math_sealed_utc':seal['sealed_utc'],'program_sha256':sha(Path(__file__).read_bytes()),'original_annals_full_proof_reproduced':False,'historical_all_refs_search_reproduced':False}
ck(out['author_assertions']==38066 and out['historical_review_assertions']==1420,'complete finite assertion totals')
out['check_count']=len(checks);(A/'root_original_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','check_count','nested_binding_instances','final_author_files','author_assertions','historical_review_assertions']},indent=2))
