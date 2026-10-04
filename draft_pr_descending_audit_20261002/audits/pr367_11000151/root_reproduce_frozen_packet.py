"""Literal frozen scope/history verification and complete root executable replay."""
from pathlib import Path, PurePosixPath
import base64, datetime, gzip, hashlib, json, os, subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];C=A/'snapshot/problems/11000151_artin_a5_quotient'
D=A/'root_replay_private_02';D.mkdir(exist_ok=False);S=A/'root_original_streams_02';S.mkdir(exist_ok=False)
PREFIX='problems/11000151_artin_a5_quotient';Q='unsolved_math_prioritization/QUEUE.md'
PY=R/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
checks=[];captures=[];outputs=[];started=datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def ck(v,label):
    checks.append({'check':label,'pass':bool(v)})
    assert v,label
def cmd(argv,label,store=False,cwd=R):
    t=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(list(map(str,argv)),cwd=cwd,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    root=S if store else D
    rows={}
    for ch,b in [('stdout',p.stdout),('stderr',p.stderr)]:
        f=root/(label+'.'+ch+'.gz');z=gzip.compress(b,mtime=0);f.write_bytes(z);rows[ch]={'path':str(f.relative_to(A)),'bytes':len(b),'sha256':sha(b),'gzip_bytes':len(z),'gzip_sha256':sha(z)}
    captures.append({'label':label,'command':list(map(str,argv)),'started_utc':t,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,**rows})
    ck(p.returncode==0,label+' successful execution');ck(p.stderr==b'',label+' empty stderr');return p.stdout
def git(*argv):return subprocess.check_output(['git',*argv],cwd=R)
def get(rev,p):return git('show',rev+':'+p)
def tree(rev):
    out={}
    for r in git('ls-tree','-rz','--full-tree',rev).split(b'\0'):
        if r:
            m,p=r.split(b'\t',1);mode,typ,oid=m.decode().split();out[p.decode()]={'mode':mode,'type':typ,'sha':oid}
    return out
def api(endpoint,label):return json.loads(cmd(['gh','api','--method','GET','-H','Cache-Control: no-cache','repos/AlecKriebel/Math/'+endpoint],label))
freeze=json.loads((A/'snapshot_manifest.json').read_bytes());HEAD=freeze['head'];BASE=freeze['base'];expected={r['path']:r for r in freeze['files']}
ck(HEAD=='d977c9564f079cde975a7b4261776eb9061c5f5f' and BASE=='efd29c05204703acca9a0860812f54b94fae54b1','literal original pins')
ht=tree(HEAD);bt=tree(BASE);delta={p for p in ht.keys()|bt.keys() if ht.get(p)!=bt.get(p)}
ck(delta==set(expected) and len(delta)==44,'complete recursive Git delta exactly44')
ck({p for p in ht if p.startswith(PREFIX+'/')}==set(expected)-{Q} and len(expected)-1==43,'closed43 target paths')
files=api('pulls/367/files?per_page=100&page=1','API_frozen_pr_files');ck(len(files)==44 and {r['filename'] for r in files}==set(expected),'full44 API PR file scope')
ck(api('pulls/367/files?per_page=100&page=2','API_frozen_pr_files_end')==[],'PR file pagination exhausted')
for i,(p,r) in enumerate(sorted(expected.items())):
    raw=get(HEAD,p);ck(raw==(A/'snapshot'/p).read_bytes() and len(raw)==r['bytes'] and sha(raw)==r['sha256'],'full frozen Git bytes '+p)
    ck(ht[p]=={'mode':'100644','type':'blob','sha':r['git_blob_sha']} and blob(raw)==r['git_blob_sha'],'full frozen mode/blob '+p)
    fr=next(x for x in files if x['filename']==p);ck(fr['sha']==r['git_blob_sha'] and fr['status']==r['status'],'entire API file status/blob '+p)
    j=api('git/blobs/'+r['git_blob_sha'],'API_frozen_blob_'+str(i));b=base64.b64decode(j['content']);ck(j['sha']==r['git_blob_sha'] and j['encoding']=='base64' and j['size']==len(b) and b==raw,'entire actual API blob '+p)
old=get(BASE,Q);new=get(HEAD,Q);lines=old.splitlines(keepends=True);other=new.splitlines(keepends=True);ck(len(lines)==len(other),'complete queue length')
indices=[i for i,(u,v) in enumerate(zip(lines,other)) if u!=v];ck(len(indices)==1,'exactly one queue row changed');i=indices[0];cells=lines[i].split(b'|');newcells=other[i].split(b'|')
ck(cells[2].strip().split()[0]==b'11000151' and cells[8].strip()==b'queued' and cells[9].strip()==b'0/5','original queue own row queued0')
ck([n for n,(u,v) in enumerate(zip(cells,newcells)) if u!=v]==[8,9],'only status/turn pipe cells');cells[8:10]=[b' claimed_solved ',b' 4/5 '];lines[i]=b'|'.join(cells);ck(b''.join(lines)==new,'every other queue byte preserved')
bindings=[];manifests=[]
names=[f'TURN_{n}_MANIFEST.json' for n in range(1,5)]+['FINAL_AUTHOR_MANIFEST.json','review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']
for name in names:
    f=C/name;m=json.loads(f.read_bytes());seen=set()
    for row in m['files']:
        p=PurePosixPath(row['path']);ck(not p.is_absolute() and '..' not in p.parts and row['path'] not in seen,'safe unique binding '+name+'/'+row['path']);seen.add(row['path']);f2=f.parent/p
        ck(not f2.is_symlink() and f2.resolve().is_relative_to(C.resolve()),'owned binding '+name+'/'+row['path']);b=f2.read_bytes();ck(len(b)==row['bytes'] and sha(b)==row['sha256'],'full nested identity '+name+'/'+row['path']);bindings.append({'manifest':name,**row})
    manifests.append({'path':name,'bytes':f.stat().st_size,'sha256':sha(f.read_bytes()),'bindings':len(seen)})
ck(len(bindings)==106 and len(manifests)==7,'all106 bindings in7 manifests')
pub=json.loads((C/'PUBLICATION_MANIFEST.json').read_bytes());ck({r['path'] for r in pub['files']}=={p.removeprefix(PREFIX+'/') for p in expected if p!=Q}-{'PUBLICATION_MANIFEST.json'},'closed42 publication bindings')
ck(pub['status']=='claimed_solved' and type(pub['turns']) is int and pub['turns']==4,'literal integer manifest complete candidate disposition; queue fraction4/5')
headparents=git('show','-s','--format=%P',HEAD).decode().strip().split();ck(headparents==[BASE,'a440a519393bf4c68433c6a8cdd49b384d3bfca6'],'frozen publication actual parents')
commits=[json.loads((C/f'TURN_{n}_REMOTE_RECEIPT.json').read_bytes())['commit'] for n in range(1,4)]+[headparents[1]];prior=BASE;history=[]
for n,rev in enumerate(commits,1):
    parents=git('show','-s','--format=%P',rev).decode().strip().split();t=git('show','-s','--format=%T',rev).decode().strip();j=api('git/commits/'+rev,'API_author_commit_'+str(n))
    ck(parents==[prior] and [p['sha'] for p in j['parents']]==parents and j['sha']==rev and j['tree']['sha']==t,'actual checkpoint ordered parents/tree '+str(n))
    for k in range(1,n+1):
        m=json.loads((C/f'TURN_{k}_MANIFEST.json').read_bytes())
        for p in [f'TURN_{k}_MANIFEST.json']+[r['path'] for r in m['files']]:ck(get(rev,PREFIX+'/'+p)==(C/p).read_bytes(),'actual retained checkpoint bytes '+str(n)+'/'+p)
    if n<4:
        receipt=json.loads((C/f'TURN_{n}_REMOTE_RECEIPT.json').read_bytes());tr=tree(rev)
        ck(receipt['raw_bytes_exact'] and not receipt['queue_changed'],'checkpoint receipt original flags '+str(n))
        ck({r['name'] for r in receipt['files']}=={p.removeprefix(PREFIX+'/') for p in tr if p.startswith(PREFIX+'/')},'full actual old remote scope '+str(n))
        for r in receipt['files']:
            b=get(rev,PREFIX+'/'+r['name']);ck(b==(C/r['name']).read_bytes() and blob(b)==r['sha'] and len(b)==r['size'],'actual old remote full blob '+str(n)+'/'+r['name'])
    history.append(j);prior=rev
author=json.loads((C/'FINAL_AUTHOR_MANIFEST.json').read_bytes());at=tree(commits[-1]);paths={r['path'] for r in author['files']}|{'FINAL_AUTHOR_MANIFEST.json'}
ck(len(author['files'])==33 and len(paths)==34 and {p.removeprefix(PREFIX+'/') for p in at if p.startswith(PREFIX+'/')}==paths,'complete33 author bindings plus manifest34 actual anchor')
for p in paths:ck(get(commits[-1],PREFIX+'/'+p)==(C/p).read_bytes(),'actual final author anchor full bytes '+p)
sources=json.loads((A/'root_source_fetch_receipts.json').read_bytes())
for row in sources:
    b=(A/'root_primary_private'/row['name']).read_bytes();ck(row['matches'] and not row['returncode'] and len(b)==row['bytes'] and sha(b)==row['sha256'],'actual primary PDF '+row['name'])
sealed=json.loads((A/'ROOT_CODE_PRE_REPLAY_SEAL.json').read_bytes())
for row in sealed['files']:
    b=(C/row['path']).read_bytes();ck(row['full_root_read_before_execution'] and len(b)==row['bytes'] and sha(b)==row['sha256'],'entire executable access binding '+row['path'])
programs=[(f'author{n}',[C/f'check_turn_{n}.py'],(C/f'TURN_{n}_CHECKS.json').read_bytes()) for n in range(1,5)]
programs += [('cpp_wrapper',[C/'verify_turn_4_cpp.py'],(C/'TURN_4_CPP_CHECKS.json').read_bytes()),('historical_independent',[C/'review/independent_check.py'],(C/'review/INDEPENDENT_CHECKS.json').read_bytes()),('historical_replay',[C/'review/replay_author.py',C],(C/'review/AUTHOR_REPLAY.json').read_bytes()),('publication',[C/'verify_publication.py'],b'PASS: all frozen public bytes, four Python receipts, C++ full stream, and independent review controls\n')]
for label,args,expected_output in programs:
    b=cmd([PY,'-B',*args],label,store=True,cwd=D);ck(b==expected_output,'entire byte-for-byte original output '+label);outputs.append({'label':label,'bytes':len(b),'sha256':sha(b),'complete_output':b.decode(),'parsed':json.loads(b) if label!='publication' else None})
exe=D/'check_turn4';cmd(['g++','-O3','-std=c++17',C/'check_turn_4.cpp','-o',exe],'direct_CPP_compile')
b=cmd([exe,'--stream'],'direct_CPP_full_state_stream',store=True,cwd=D);lines=b.splitlines(keepends=True);records=lines[:-1];terminal=json.loads(lines[-1]);ck(len(records)==90921 and all(r.startswith(b'S|') for r in records),'all90921 literal complete state records')
codes=[];state_scalar_assertions=0
for line in records:
    fields=line.decode().rstrip('\n').split('|');assert len(fields)==9 and fields[0]=='S';state_scalar_assertions+=1;code=int(fields[1]);codes.append(code);packed=int(fields[2]);perm=[(packed>>(3*k))&7 for k in range(6)];assert sorted(perm)==list(range(6)) and 0<=code<3**15;state_scalar_assertions+=1
    for word in fields[3:]:
        w=[int(x) for x in word.split(',')] if word else [];assert all(1<=abs(x)<=6 for x in w) and all(u!=-v for u,v in zip(w,w[1:]));state_scalar_assertions+=1
ck(state_scalar_assertions==90921*8,'all727368 complete state-record scalar validations')
ck(codes==sorted(set(codes)) and codes[0]==0 and codes[-1]==3**15-1,'complete canonical stream ordered unique endpoints')
digest=sha(b''.join(records));expected4=json.loads((C/'TURN_4_CHECKS.json').read_bytes());ck(digest==expected4['canonical_action_stream_sha256']=='af2b8ec569d613e4f3d8ba3b72d18e85e8c612f4265057b7f4c485d544d159bf','entire literal state stream identity')
ck(all(expected4[k]==v for k,v in terminal.items()),'full direct C++ terminal census')
for row in freeze['files']:ck((A/'snapshot'/row['path']).read_bytes()==get(HEAD,row['path']),'frozen bytes unchanged after all execution '+row['path'])
out={'status':'PASS','started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'check_count':len(checks),'checks':checks,'literal_frozen_head':HEAD,'literal_base':BASE,'all44_actual_files':freeze['files'],'nested_bindings':bindings,'manifests':manifests,'all4_actual_author_checkpoint_API_records':history,'final_author_bindings':33,'final_author_actual_files':34,'queue_physical_line':i+1,'queue_changed_pipe_cells':[8,9],'all_other_queue_bytes_equal':True,'sources':sources,'all_complete_captures':captures,'original_program_outputs':outputs,'full_CPP_stream_bytes':len(b),'full_CPP_state_records':90921,'complete_state_record_scalar_assertions':state_scalar_assertions,'state_stream_sha256':digest,'public_sources_redistributed':False,'mathematical_priority_pending':True,'workflow_completion_percent':55,'original_problem_resolution_percent':0}
(A/'root_original_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','check_count','nested_bindings','full_CPP_stream_bytes','full_CPP_state_records','workflow_completion_percent'] if k!='nested_bindings'},indent=2))
