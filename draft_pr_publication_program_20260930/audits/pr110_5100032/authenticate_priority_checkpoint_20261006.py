from pathlib import Path
import subprocess,json,hashlib,datetime,os
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parents[1]
D=A/'root_priority_checkpoint_authentication_20261006';D.mkdir(exist_ok=False)
r=json.loads((P/'audits/pr108_30003996/actual_checkpoints/PR110_priority_20261006/RECEIPT.json').read_text())
queries=''.join(r['commit']+':'+v['file']+'\n' for v in r['pins']).encode()
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.Popen(['git','cat-file','--batch'],cwd=C,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
o,e=p.communicate(queries)
(D/'stdout.prefix.bin').write_bytes(o[:4096]);(D/'stderr.bin').write_bytes(e)
rec={'actual_operator_PID':os.getpid(),'actual_child_PID':p.pid,'argv':['git','cat-file','--batch'],'UTC_start':start,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'stdin_bytes':len(queries),'stdin_sha256':hashlib.sha256(queries).hexdigest(),'stdout_bytes':len(o),'stdout_sha256':hashlib.sha256(o).hexdigest(),'stdout_retained':4096,'stderr_bytes':len(e),'stderr_sha256':hashlib.sha256(e).hexdigest()}
(D/'ACTUAL_PROCESS.json').write_text(json.dumps(rec,indent=2)+'\n')
if p.returncode:raise RuntimeError(e.decode())
pos=0;pins=[]
for v in r['pins']:
 end=o.index(b'\n',pos);info=o[pos:end].decode().split();pos=end+1
 if len(info)!=3 or info[1]!='blob':raise RuntimeError('Gitbatchheader')
 size=int(info[2]);b=o[pos:pos+size];pos+=size
 if o[pos:pos+1]!=b'\n':raise RuntimeError('Gitseparator')
 pos+=1
 if size!=v['bytes'] or hashlib.sha256(b).hexdigest()!=v['sha256']:raise RuntimeError('committedpin')
 if hashlib.sha1(b'blob '+str(size).encode()+b'\0'+b).hexdigest()!=info[0]:raise RuntimeError('GitblobOID')
 current=(C/v['file']).read_bytes()
 if current!=b:raise RuntimeError('currentselectedchanged')
 pins.append(dict(v,git_blob=info[0]))
if pos!=len(o):raise RuntimeError('unparsed')
out={'schema':'pr110-root-complete-priority-checkpoint-body-readback/v1','UTC':rec['UTC_end'],'actual_operator_PID':os.getpid(),'actual_git_batch_PID':p.pid,'commit':r['commit'],'parent':r['parent'],'all_committed_full_bodies_and_current_files_equal':True,'file_count':len(pins),'pins':pins,'remote_verified_by_actual_checkpoint':r['remote_verified'],'mathematical_gate_complete':True,'priority_or_publication_clearance':False,'workflow_percent':30,'new_central_proof_search_turns':0}
(A/'ROOT_PRIORITY_CHECKPOINT_AUTHENTICATION_20261006.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:x for k,x in out.items() if k!='pins'}))

