"""Complete original scope/history/bindings and whole-output source replays."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import base64,gzip,hashlib,json,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];P='unsolved_math_prioritization/attempts/2303002/';Q='unsolved_math_prioritization/QUEUE.md'
D=A/'snapshot'/P;S=A/'root_original_streams';S.mkdir(exist_ok=True);V=A/'root_replay_private';V.mkdir(exist_ok=True)
checks=[];commands=[];sha=lambda b:hashlib.sha256(b).hexdigest();blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def ck(v,name):checks.append({'name':name,'passed':bool(v)});assert v,name
def run(label,argv,private=False,expected_exit=0):
 z=subprocess.run(argv,cwd=R,capture_output=True);directory=V if private else S;e={'label':label,'argv':argv,'exit':z.returncode,'utc':datetime.now(timezone.utc).isoformat(),'private':private}
 for stream,b in [('stdout',z.stdout),('stderr',z.stderr)]:
  p=directory/(label+'.'+stream+'.gz');p.write_bytes(gzip.compress(b,mtime=0));ck(gzip.decompress(p.read_bytes())==b,'complete lossless '+label+'/'+stream);e[stream]={'path':p.relative_to(A).as_posix(),'bytes':len(b),'sha256':sha(b),'stored_bytes':p.stat().st_size,'stored_sha256':sha(p.read_bytes())}
 commands.append(e);(A/'root_original_command_progress.json').write_text(json.dumps(commands,indent=2)+'\n');ck(z.returncode==expected_exit,'complete exit '+label)
 if expected_exit==0:ck(not z.stderr,'complete empty stderr '+label)
 return z.stdout
def git(label,*args):return run(label,['git',*args])
def tree(label,rev):
 return {row.split(b'\t',1)[1].decode():row.split(b'\t',1)[0].decode() for row in git(label,'ls-tree','-rz','--full-tree',rev).split(b'\0') if row}
def get(label,rev,p):return git(label,'show',rev+':'+p)
m=json.loads((A/'snapshot_manifest.json').read_bytes());H=m['head'];B=m['base'];C='a3ac55761d2301fbfe30e07a266da4a039cbfaba'
ck(H=='4245f1af53840a07f43c05c928c4783bc6c3a467' and B=='efd29c05204703acca9a0860812f54b94fae54b1','literal original pair')
bt,ht=tree('base_tree',B),tree('original_tree',H);expected={e['path'] for e in m['files']}
ck(len(expected)==19 and expected=={p for p in bt.keys()|ht.keys() if bt.get(p)!=ht.get(p)},'all19 whole-repository mode/type/blob changes')
ck({p for p in ht if p.startswith(P)}==expected-{Q},'closed all18 original target namespace')
ck({P+f.relative_to(D).as_posix() for f in D.rglob('*') if f.is_file()}==expected-{Q},'all18 snapshot target paths')
remote=[]
for i,e in enumerate(m['files']):
 p=e['path'];b=get('blob_'+str(i),H,p);ck(b==(A/'snapshot'/p).read_bytes() and len(b)==e['bytes'] and sha(b)==e['sha256'] and blob(b)==e['git_blob_sha'],'whole original Git/disk '+p)
 ck(ht[p].split()==['100644','blob',blob(b)],'whole original mode/type/blob '+p)
 o=json.loads(run('remote_'+str(i),['gh','api','repos/AlecKriebel/Math/contents/'+p+'?ref='+H],private=True));ck(o['path']==p and o['type']=='file' and o['size']==len(b) and o['sha']==blob(b) and o['encoding']=='base64' and base64.b64decode(o['content'])==b,'whole full remote content '+p)
 remote.append({'path':p,'bytes':len(b),'sha256':sha(b),'git_blob':blob(b),'mode':'100644','all_Git_API_disk_equal':True})
bindings=[]
for name in ['FINAL_FROZEN_MANIFEST.json','final_review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']:
 mf=D/name;o=json.loads(mf.read_bytes());entries=o['files'] if 'files' in o else [{'path':p,'sha256':h} for p,h in o.items()];seen=set()
 for e in entries:
  q=PurePosixPath(e['path']);ck(not q.is_absolute() and '..' not in q.parts and q.as_posix()==e['path'] and e['path'] not in seen,'safe nested '+name+'/'+e['path']);seen.add(e['path']);b=(mf.parent/q).read_bytes();ck(sha(b)==e['sha256'] and ('bytes' not in e or len(b)==e['bytes']),'whole nested '+name+'/'+e['path']);bindings.append({'manifest':name,'resolved_path':str((mf.parent/q).relative_to(D)),'bytes':len(b),**e})
ck(len(bindings)==29,'all29 nested instances9+3+17')
pub=json.loads((D/'PUBLICATION_MANIFEST.json').read_bytes());ck({e['path'] for e in pub['files']}=={p.removeprefix(P) for p in expected-{Q,P+'PUBLICATION_MANIFEST.json'}},'closed publication17 self-excluded paths')
ck(pub['author_manifest_sha256']==sha((D/'FINAL_FROZEN_MANIFEST.json').read_bytes()) and pub['review_manifest_sha256']==sha((D/'final_review/REVIEW_MANIFEST.json').read_bytes()),'literal cross-manifest anchors')
ck(git('checkpoint_parent','show','-s','--format=%P',C).decode().strip()==B,'source-gate checkpoint parent')
ck(git('head_parents','show','-s','--format=%P',H).decode().split()==[B,C],'original head actual parents')
author={e['path'] for e in json.loads((D/'FINAL_FROZEN_MANIFEST.json').read_bytes())['files']}|{'FINAL_FROZEN_MANIFEST.json'};ck(len(author)==10,'actual10 source-gate author files')
ck(set(git('checkpoint_paths','diff','--name-only',B,C).decode().splitlines())=={P+p for p in author},'whole source checkpoint exactly10 files')
for i,p in enumerate(sorted(author)):ck(get('author_'+str(i),C,P+p)==(D/p).read_bytes(),'whole historical author '+p)
st=json.loads((D/'SOURCE_AUDIT_STATE.json').read_bytes());ck(st['turns_used']==0 and st['proposed_disposition']=='already_solved' and json.loads((D/'FINAL_FROZEN_MANIFEST.json').read_bytes())['turns_used']==0,'genuine0 source/proof-verification research turns')
ck(not any('TURN_' in p for p in expected),'no fabricated discovery-turn packet')
catalog=json.loads(get('base_catalog',B,'unsolved_math_prioritization/catalog.json'));row=next(x for x in catalog if x['id']=='2303002');source=json.loads((D/'SOURCE_MANIFEST.json').read_bytes())
ck(row['review_hash']==source['review_hash'] and row['problem_number']=='AMR-022-3002','literal base catalog problem/review anchors')
baseq=get('base_queue',B,Q);old=baseq.splitlines(keepends=True);indices=[i for i,l in enumerate(old) if len(l.split(b'|'))>9 and l.split(b'|')[2].strip().split(b' / ')[0]==b'2303002'];ck(len(indices)==1,'unique exact original queue row')
i=indices[0];new=list(old);cells=new[i].split(b'|');ck([cells[j].strip() for j in [8,9]]==[b'queued',b'0/5'],'original queued0 cells');cells[8]=b' already_solved ';new[i]=b'|'.join(cells);ck(b''.join(new)==(A/'snapshot'/Q).read_bytes(),'entire original queue only own status, turns0 preserved')
for e in source['primary_pdfs']:
 b=(A/'root_primary_private'/e['file']).read_bytes();ck(len(b)==e['bytes'] and sha(b)==e['sha256'],'whole fresh primary '+e['file'])
baseline=json.loads((A/'ROOT_BASELINE_SEAL.json').read_bytes());assessment=json.loads((A/'ROOT_MATH_ASSESSMENT_SEAL.json').read_bytes());ck(sha((A/'ROOT_SOURCE_FIRST_BASELINE.md').read_bytes())==baseline['baseline_sha256'],'pre-candidate baseline unchanged');ck(sha((A/'ROOT_MATH_ASSESSMENT.md').read_bytes())==assessment['assessment_sha256'] and sha((A/'ROOT_BASELINE_SEAL.json').read_bytes())==assessment['baseline_seal_sha256'],'pre-code whole math seal unchanged')
run('dataset_object',['git','cat-file','-t',source['dataset_revision']],expected_exit=128)
replays=[]
for label,argv,expected_path,count in [('author',['python3',str(D/'verify_source_alignment.py')],D/'SOURCE_CHECKS.json',3675),('historical_with_sources',['python3',str(D/'final_review/run_portable.py'),'--sources',str(A/'root_primary_private')],D/'final_review/INDEPENDENT_CHECKS.json',1667),('historical_math_only',['python3',str(D/'final_review/run_portable.py'),'--math-only'],None,1665)]:
 b=run(label,argv);o=json.loads(b)
 if expected_path is not None:ck(b==expected_path.read_bytes(),'entire byte-exact replay '+label)
 ck(o.get('assertions',o.get('independent_assertions'))==count,'literal complete count '+label)
 if expected_path is None:
  expected_output=json.loads((D/'final_review/INDEPENDENT_CHECKS.json').read_bytes());expected_output['independent_assertions']=1665;ck(b==(json.dumps(expected_output,indent=2)+'\n').encode(),'whole source-free output only two source hashes omitted')
 replays.append({'label':label,'argv':argv,'complete_output':b.decode(),'stdout_sha256':sha(b),'count':count})
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','frozen_head':H,'original_base':B,'actual_source_checkpoint':C,'source_gate_author_files':10,'genuine_discovery_turns':0,'remote_files':remote,'nested_bindings':bindings,'binding_count':29,'whole_original_queue_lines':len(old),'queue_physical_line':i+1,'queue_changed_pipe_cells':[8],'queue_turns_preserved':'0/5','base_catalog_statement_hash':row['statement_hash'],'base_catalog_review_hash':row['review_hash'],'checks':checks,'check_count':len(checks),'commands':commands,'replays':replays,'historical_dataset_revision_available_locally':False,'historical_all_refs_negative_search_reproduced':False,'novelty_certificate':False,'continuum_proof_established_by_finite_controls':False,'program_sha256':sha(Path(__file__).read_bytes())}
(A/'root_original_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','check_count','binding_count','actual_source_checkpoint','source_gate_author_files','queue_physical_line']},indent=2))
