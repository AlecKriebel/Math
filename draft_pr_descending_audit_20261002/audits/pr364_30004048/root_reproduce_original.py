"""Read-only Git/API reproduction of the original PR364 mathematical packet."""
from pathlib import Path
from datetime import datetime,timezone
import base64,gzip,hashlib,json,os,shutil,subprocess,sys
A=Path(__file__).resolve().parent;R=A.parents[2];D=A/'root_replay_private';D.mkdir(exist_ok=True)
S=A/'snapshot';P='unsolved_math_prioritization/attempts/30004048';Q='unsolved_math_prioritization/QUEUE.md'
H='0d07b06537aded3e76f5a71908f3546df574a691';B='efd29c05204703acca9a0860812f54b94fae54b1';AUTHOR='067266518aca8b427edd926a68a311e538ad45dd'
sha=lambda b:hashlib.sha256(b).hexdigest();blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
commands=[];checks=[]
def ck(c,n):
    checks.append({'name':n,'passed':bool(c)});assert c,n
def utc():return datetime.now(timezone.utc).isoformat()
def run(label,argv,expected=0):
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1',PYTHONDONTWRITEBYTECODE='1')
    start=utc();z=subprocess.run(argv,cwd=R,env=env,capture_output=True);end=utc();streams={}
    for name,b in [('stdout',z.stdout),('stderr',z.stderr)]:
        p=D/(label+'.'+name+'.gz');p.write_bytes(gzip.compress(b,mtime=0));stored=p.read_bytes()
        streams[name]={'path':p.relative_to(A).as_posix(),'bytes':len(b),'sha256':sha(b),'stored_bytes':len(stored),'stored_sha256':sha(stored)}
    commands.append({'label':label,'argv':argv,'cwd':str(R),'started_utc':start,'finished_utc':end,'exit':z.returncode,'expected_exit':expected,'environment_changes':{k:env[k] for k in ['GIT_OPTIONAL_LOCKS','GIT_NO_LAZY_FETCH','PYTHONDONTWRITEBYTECODE']},'streams':streams})
    (A/'root_original_reproduction_progress.json').write_text(json.dumps({'status':'IN_PROGRESS','commands':commands,'checks':checks},indent=2)+'\n')
    ck(z.returncode==expected and not z.stderr,label+' entire exit/stderr');return z.stdout
def git(label,*argv):return run(label,['git',*argv])
def api(label,path):return json.loads(run(label,['gh','api','repos/AlecKriebel/Math/'+path]))
def tree(label,ref):
    b=git(label,'ls-tree','-rz','--full-tree',ref);out={}
    for row in b.split(b'\0'):
        if row:
            h,p=row.split(b'\t',1);ck(p.decode() not in out,label+' unique path');out[p.decode()]=h.decode().split()
    return out
ck((A/'ROOT_CANDIDATE_ANALYTIC_SEAL.json').exists(),'root full analytical seal precedes execution')
start_main=git('begin_main','rev-parse','HEAD');start_branch=git('begin_branch','branch','--show-current');ck(start_branch==b'main\n','main only')
idx=Path(git('index_path','rev-parse','--git-path','index').decode().strip());idx=idx if idx.is_absolute() else R/idx;index_before=sha(idx.read_bytes())
meta=api('original_pr_begin','pulls/364');ck(meta['head']['sha']==H and meta['base']['sha']==B and meta['state']=='open' and meta['draft'] is True,'literal original draft head/base')
listed=api('original_files','pulls/364/files?per_page=100');mf=json.loads((A/'snapshot_manifest.json').read_bytes());entries=mf['files'];ck(len(entries)==len(listed)==42,'42 actual files')
listed={e['filename']:e for e in listed};bt=tree('base_tree',B);ht=tree('head_tree',H);delta={p for p in set(bt)|set(ht) if bt.get(p)!=ht.get(p)}
ck(delta==set(listed)=={e['path'] for e in entries},'whole repository42 scope');ck({p for p in ht if p.startswith(P+'/')}==delta-{Q},'exact41 target namespace')
bindings=[]
for i,e in enumerate(entries):
    p=e['path'];d=git('blob_'+str(i).zfill(2),'show',H+':'+p);disk=(S/p).read_bytes()
    ck(d==disk and len(d)==e['bytes'] and sha(d)==e['sha256'] and blob(d)==e['git_blob_sha'],'whole frozen Git/disk identity '+p)
    ck(ht[p]==['100644','blob',blob(d)] and listed[p]['sha']==blob(d) and listed[p]['status']==e['status'],'API scope/mode/blob '+p)
    o=api('content_'+str(i).zfill(2),'contents/'+p+'?ref='+H)
    ck(o['path']==p and o['type']=='file' and o['sha']==blob(d) and o['size']==len(d) and base64.b64decode(o['content'])==d,'full original contents API '+p)
    bindings.append(dict(e,mode='100644',kind='blob'))
T=S/P;nested=[]
for name in ['SOURCE_GATE_MANIFEST.json','TURN_1_MANIFEST.json','TURN_2_MANIFEST.json','TURN_3_MANIFEST.json','FINAL_AUTHOR_MANIFEST.json','PUBLICATION_MANIFEST.json','review/REVIEW_MANIFEST.json']:
    m=json.loads((T/name).read_bytes());base=T/'review' if name.startswith('review/') else T
    for e in m['files']:
        p=Path(e['path']);ck(not p.is_absolute() and '..' not in p.parts,'safe nested literal path');b=(base/p).read_bytes();ck(len(b)==e['bytes'] and sha(b)==e['sha256'],'full nested binding '+name+'/'+str(p));nested.append(dict(e,manifest=name))
ck(len(nested)==135,'all135 nested binding instances (88author+40wrapper+7review)')
source_bindings=[]
for e in json.loads((T/'SOURCE_MANIFEST.json').read_bytes())['sources']:
    d=(A/'root_primary_private'/e['file']).read_bytes();ck(len(d)==e['bytes'] and sha(d)==e['sha256'],'fresh primary source exact '+e['file']);source_bindings.append(e)
for label,ref in [('original_head',H),('author_checkpoint',AUTHOR)]:
    raw=git(label+'_raw','cat-file','-p',ref);ck(hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==ref,'complete commit object '+ref)
    git(label+'_parents','show','-s','--format=%P',ref)
git('genuine_target_history','log',H,'--format=%H%n%P%n%s%n%aI','--',P)
at=tree('author_checkpoint_tree',AUTHOR);author_files=json.loads((T/'review/REMOTE_BINDING.json').read_bytes())['files'];ck(len(author_files)==30,'30 author checkpoint files')
for i,e in enumerate(author_files):
    p=P+'/'+e['name'];d=git('author_blob_'+str(i).zfill(2),'show',AUTHOR+':'+p);ck(d==(T/e['name']).read_bytes() and len(d)==e['size'] and blob(d)==e['sha'] and at[p]==['100644','blob',e['sha']],'actual author checkpoint '+e['name'])
oldqueue=git('base_queue','show',B+':'+Q);newqueue=(S/Q).read_bytes();old=oldqueue.splitlines(keepends=True);new=newqueue.splitlines(keepends=True)
changed=[i for i,(a,b) in enumerate(zip(old,new)) if a!=b];ck(len(old)==len(new)==1966 and changed==[397],'original whole queue only physical398')
oldcells=old[397].split(b'|');newcells=new[397].split(b'|');cellchanges=[i for i,(a,b) in enumerate(zip(oldcells,newcells)) if a!=b]
ck(oldcells[2].strip()==newcells[2].strip()==b'30004048 / OWR-16763-022' and newcells[8].strip()==b'claimed_solved' and newcells[9].strip()==b'3/5','original target claimed_solved3/5')
ck(old[:2]==new[:2] and old[0].startswith(b'sha: c87c275c'),'malformed metadata header inherited unchanged from base')
copy=D/'candidate';ck(not copy.exists(),'fresh private byte-identical replay directory');shutil.copytree(T,copy)
outputs=[]
for turn in [1,2,3]:
    got=run('turn_'+str(turn),[sys.executable,str(copy/('verify_turn'+str(turn)+'.py'))]);expected=(copy/('TURN_'+str(turn)+'_CHECKS.json')).read_bytes();ck(got==expected,'entire author turn'+str(turn)+' stdout');outputs.append(json.loads(got))
got=run('historical_review',[sys.executable,str(copy/'review/check_independent.py')]);ck(got==(copy/'review/INDEPENDENT_CHECKS.json').read_bytes(),'entire historical independent stdout');review=json.loads(got)
ck(sum(e['assertions'] for e in outputs)==43755 and review['exact_assertions']==2552,'whole receipt assertions')
ck(all(p.read_bytes()==(T/p.relative_to(copy)).read_bytes() for p in copy.rglob('*') if p.is_file()),'all private replay inputs unchanged')
end=api('original_pr_end','pulls/364');ck(end['head']['sha']==H and end['base']['sha']==B and end['state']=='open' and end['draft'] is True,'draft/head/base unchanged through reproduction')
ck(git('end_main','rev-parse','HEAD')==start_main and git('end_branch','branch','--show-current')==start_branch and sha(idx.read_bytes())==index_before,'main branch/index unchanged')
out={'status':'PASS_FULL_ORIGINAL_GIT_API_SOURCE_BINDING_AND_WHOLE_REPRODUCTION','utc':utc(),'original_head':H,'base':B,'files':42,'math_files':41,'bindings':bindings,'nested_binding_instances':len(nested),'nested_bindings':nested,'source_bindings':source_bindings,'author_checkpoint':AUTHOR,'actual_author_checkpoint_files':30,'author_assertions':43755,'historical_review_assertions':2552,'whole_receipts':outputs+[review],'queue':{'lines':1966,'physical_line':398,'changed_cells':cellchanges,'status':'claimed_solved','turns':'3/5','inherited_malformed_header_unchanged':True},'commands':commands,'checks':checks,'check_count':len(checks),'mathematical_resolution_percent':95,'workflow_percent':45,'priority_pending':True,'preprint_pending':True}
(A/'root_original_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','files','nested_binding_instances','author_assertions','historical_review_assertions','check_count','queue']},indent=2))
