"""Independent literal head/base/body/full-scope gate; no PR mutation or merge."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import base64,gzip,hashlib,json,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];V=A/'root_live_private';V.mkdir(exist_ok=True);Q='unsolved_math_prioritization/QUEUE.md';P='unsolved_math_prioritization/attempts/2303016/';checks=[];captures=[];sha=lambda b:hashlib.sha256(b).hexdigest();blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def ck(v,n):checks.append({'name':n,'passed':bool(v)});assert v,n
def run(args,label,allow_stderr=False):
 start=datetime.now(timezone.utc).isoformat();r=subprocess.run(args,cwd=R,capture_output=True);streams={}
 for stream,b in [('stdout',r.stdout),('stderr',r.stderr)]:
  p=V/(label+'.'+stream+'.gz');p.write_bytes(gzip.compress(b,mtime=0));ck(gzip.decompress(p.read_bytes())==b,'whole lossless capture '+label+'/'+stream);streams[stream]={'path':p.relative_to(A).as_posix(),'bytes':len(b),'sha256':sha(b),'gzip_bytes':p.stat().st_size,'gzip_sha256':sha(p.read_bytes())}
 captures.append({'args':args,'label':label,'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),'exit':r.returncode,'stderr_policy':'full Git fetch diagnostics retained' if allow_stderr else 'empty',**streams});ck(r.returncode==0 and (allow_stderr or not r.stderr),'complete exit '+label);return r.stdout
def git(label,*args):return run(['git',*args],label)
def api(label,path):return json.loads(run(['gh','api','repos/AlecKriebel/Math/'+path],label))
def entries(raw):return {row.split(b'\t',1)[1].decode():row.split(b'\t',1)[0].decode() for row in raw.split(b'\0') if row}
pins=json.loads((A/'LIVE_ACCEPTANCE_PINS.json').read_bytes());m=json.loads((A/'repaired_snapshot_manifest.json').read_bytes());o=json.loads((A/'snapshot_manifest.json').read_bytes());H=pins['head'];B=pins['base'];OLD='f4039c9c093b10e651ee7fd2e6379073b84238c7'
ck(m['head']==H and m['base']==B and o['head']==OLD and m['original_frozen_head']==OLD,'literal pinned reviewed pair')
body=(A/'accepted_pr_body.txt').read_bytes();ck(sha(body)==pins['body_sha256'],'whole pinned body')
ck(git('current_branch','branch','--show-current').strip()==b'main','main only')
run(['git','fetch','origin','main'],'fetch_main',allow_stderr=True);ck(git('remote_main','rev-parse','origin/main').decode().strip()==B,'reviewed actual remote main');ck(git('local_main','rev-parse','HEAD').decode().strip()==B,'reviewed actual local main')
def pr(p):
 ck(p['number']==366 and p['state']=='open' and p['draft'] is False,'live open ready PR366')
 ck(p['head']['sha']==H and p['base']['sha']==B and p['body'].encode()==body,'literal head/base/full body')
 ck(p['mergeable'] is True and p['mergeable_state']=='clean','live clean mergeable')
first=api('pr_first','pulls/366');pr(first);ck(api('main_ref_first','git/ref/heads/main')['object']['sha']==B,'actual main raw ref first')
bt=entries(git('base_all_entries','ls-tree','-rz','--full-tree',B));ht=entries(git('head_all_entries','ls-tree','-rz','--full-tree',H));ot=entries(git('original_target_entries','ls-tree','-rz',OLD,'--',P,Q));expected={e['path'] for e in m['files']}
ck(len(expected)==22 and expected=={e['path'] for e in o['files']},'same complete22 reviewed paths')
ck(expected=={p for p in bt.keys()|ht.keys() if bt.get(p)!=ht.get(p)},'whole-repository mode/type/blob delta exactly22')
ck({p for p in ht if p.startswith(P)}==expected-{Q},'closed21 target scope')
files=[]
for i,e in enumerate(m['files']):
 p=e['path'];raw=git('head_blob_'+str(i),'show',H+':'+p);ck(raw==(A/'repaired_snapshot'/p).read_bytes() and len(raw)==e['bytes'] and sha(raw)==e['sha256'],'every reviewed file byte '+p)
 ck(ht[p].split()==['100644','blob',blob(raw)],'reviewed exact mode/type/blob '+p)
 remote=api('remote_blob_'+str(i),'contents/'+p+'?ref='+H);rr=base64.b64decode(remote['content']);ck(rr==raw and remote['size']==len(raw) and remote['sha']==blob(raw),'whole current remote bytes '+p)
 if p!=Q:ck(raw==(A/'snapshot'/p).read_bytes() and ht[p]==ot[p],'every original math byte/mode '+p)
 files.append({'path':p,'bytes':len(raw),'sha256':sha(raw),'entry':ht[p]})
before=git('base_queue','show',B+':'+Q);after=(A/'repaired_snapshot'/Q).read_bytes();bl=before.splitlines(keepends=True);al=after.splitlines(keepends=True);ck(len(bl)==len(al),'full queue line count');diff=[i for i,(x,y) in enumerate(zip(bl,al)) if x!=y];ck(len(diff)==1,'whole queue only own line');i=diff[0];x=bl[i].split(b'|');y=al[i].split(b'|')
ck(len(x)==len(y) and x[2].strip().split(b' / ')[0]==b'2303016','own queue identifier and full cell count');ck([j for j,(a,b) in enumerate(zip(x,y)) if a!=b]==[8,9],'only two own queue cells');ck([x[j].strip() for j in [8,9]]==[b'queued',b'0/5'] and [y[j].strip() for j in [8,9]]==[b'already_solved',b'1/5'],'exact credited one-turn transition');ck(bt[Q].split()[:2]==ht[Q].split()[:2],'queue mode/type preserved')
tree=git('head_tree','show','-s','--format=%T',H).decode().strip();ck(git('virtual_merge','merge-tree','--write-tree',B,H).decode().splitlines()[0]==tree,'exact virtual integration tree')
ck(git('refresh_parents','show','-s','--format=%P',H).decode().strip().split()==[m['previous_review_head'],B],'actual refresh parent order')
test=api('test_merge','git/commits/'+first['merge_commit_sha']);ck([p['sha'] for p in test['parents']]==[B,H] and test['tree']['sha']==tree,'actual GitHub test-merge pair/tree')
D=A/'repaired_snapshot'/P;bindings=[]
for name in ['TURN_1_MANIFEST.json','FINAL_FROZEN_MANIFEST.json','final_review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']:
 mf=D/name;obj=json.loads(mf.read_bytes());seen=set()
 for e in obj['files']:
  q=PurePosixPath(e['path']);ck(not q.is_absolute() and '..' not in q.parts and q.as_posix()==e['path'] and e['path'] not in seen,'safe nested manifest '+name+'/'+e['path']);seen.add(e['path']);raw=(mf.parent/q).read_bytes();ck(len(raw)==e['bytes'] and sha(raw)==e['sha256'],'whole nested binding '+name+'/'+e['path']);bindings.append({'manifest':name,**e})
ck(len(bindings)==48,'all48 nested binding instances')
manifests=[]
for f in pins['audit_manifests']:
 d=A/f['family'];mf=d/f['manifest'];raw=mf.read_bytes();ck(sha(raw)==f['sha256'],'literal immutable audit '+f['family']);obj=json.loads(raw);seen=set()
 for e in obj['files']:
  q=PurePosixPath(e['path']);ck(not q.is_absolute() and '..' not in q.parts and q.as_posix()==e['path'] and e['path'] not in seen,'audit path '+e['path']);seen.add(e['path']);p=d/q;ck(p.is_file() and not p.is_symlink(),'audit regular file '+e['path']);b=p.read_bytes();ck(len(b)==e['bytes'] and sha(b)==e['sha256'],'complete audit artifact '+f['family']+'/'+e['path'])
 ck(len(seen)==f['count'],'closed family count '+f['family']);manifests.append(f)
ck(len(manifests)==3,'two independent families plus new whole adversary')
for name,pin,n,status in [('root_original_reproduction_receipt.json',pins['root_original_receipt_sha256'],158,'PASS'),('root_family_verification_receipt.json',pins['root_family_receipt_sha256'],612,'PASS_ALL_FAMILY_EVIDENCE_AND_EVERY_COMPLETE_CAPTURE')]:
 raw=(A/name).read_bytes();r=json.loads(raw);ck(sha(raw)==pin and r['status']==status and r['check_count']==n and all(c['passed'] for c in r['checks']),'whole sealed root evidence '+name)
for e in json.loads((D/'SOURCE_MANIFEST.json').read_bytes())['primary_pdfs']:
 b=(A/'root_primary_private'/e['file']).read_bytes();ck(len(b)==e['bytes'] and sha(b)==e['sha256'],'entire primary '+e['file'])
last=api('pr_last','pulls/366');pr(last);ck(last['merge_commit_sha']==first['merge_commit_sha'],'test merge stable');ck(api('main_ref_last','git/ref/heads/main')['object']['sha']==B,'raw actual main stable at end');ck(git('local_main_last','rev-parse','HEAD').decode().strip()==B,'local main stable at end')
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_ROOT_EXACT_LIVE','reviewed_head':H,'base':B,'reviewed_tree':tree,'test_merge':first['merge_commit_sha'],'body_sha256':sha(body),'check_count':len(checks),'checks':checks,'files':files,'nested_bindings':bindings,'audit_manifests':manifests,'captures':captures,'queue_line':i+1,'only_queue_cells':[8,9],'all_other_queue_bytes_preserved':True,'mathematical_replay_basis':'All21 author/review math bytes unchanged; complete158 root original and612 family checks with full28 reexecutions already sealed. Independent whole proof/reproduction separately checked.','program_sha256':sha(Path(__file__).read_bytes())}
(A/'root_exact_live_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','reviewed_head','base','reviewed_tree','test_merge','check_count','queue_line']},indent=2))
