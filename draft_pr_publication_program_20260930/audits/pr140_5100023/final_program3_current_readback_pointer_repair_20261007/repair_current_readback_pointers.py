from pathlib import Path
import json,os,stat,hashlib,datetime
A=Path(__file__).resolve().parent.parent;D=Path(__file__).resolve().parent;V=A/'final_program3_renderer_source_preparation_20261007';P=V/'MANIFEST.json'
def need(v,m):
 if not v:raise RuntimeError(m)
def pin(p):
 p=Path(p);s=p.lstat();need(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'regularfile');b=p.read_bytes();return {'path':str(p),'bytes':len(b),'mode':stat.S_IMODE(s.st_mode),'sha256':hashlib.sha256(b).hexdigest()}
def check(v):
 x=pin(v['path']);need(all(x[k]==v[k] for k in ['bytes','mode','sha256']),'fullinput');return x
need(pin(P)['sha256']=='03ac8c78cb231177cd77e1081f3ad0938152f61ddfd93a5917978663eb5114fe','predecessormanifest');m=json.loads(P.read_bytes());oldfiles=m['files'];changed=[];posts=D/'postimages3';posts.mkdir();rb=pin(A/'ROOT_PACKAGE_R2_CANDIDATE_READBACK.json');need(rb['sha256']=='1b8867adc1200a3da2e8d5313c953e8bd41340c20548cf2e1f0700d05cb11d88','genuinefinalreadback')
for f in oldfiles:
 check(f['preimage']);check(f['postimage']);p=Path(f['postimage']['path']);b=p.read_bytes()
 if p.name=='CURRENT_PROGRESS.json':
  old=json.loads(b);new=dict(old);new['current_publication_package_candidate_readback']='audits/pr140_5100023/ROOT_PACKAGE_R2_CANDIDATE_READBACK.json';new['current_publication_package_candidate_readback_sha256']=rb['sha256'];changed=[k for k in old.keys()|new.keys() if old.get(k)!=new.get(k)];need(set(changed)=={'current_publication_package_candidate_readback','current_publication_package_candidate_readback_sha256'},'onlytwofielddiff');b=(json.dumps(new,indent=2,sort_keys=True)+'\n').encode()
 q=posts/p.name;q.write_bytes(b);os.chmod(q,0o644);f['postimage']=pin(q)
m['schema']='pr140-ROOT-two-current-readback-fields-successor/v1';m['UTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();m['actual_preparer_PID']=os.getpid();m['predecessor_renderer_manifest']=pin(P);m['predecessor_renderer_source']=m['source_pin'];m['source_pin']=pin(Path(__file__));m['two_field_only_ROOT_repair']=changed;m['genuine_final_R2_readback']=rb;m['MD_and_global_LOG_byte_identical_to_predecessor']=True;m['historical_candidate_stays_archived']=True;m['full_inputs']+= [pin(P),rb];m['final_transaction_not_performed']=True
out=D/'MANIFEST.json';out.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n');os.chmod(out,0o644);print(json.dumps({'successormanifest':pin(out),'files':m['files'],'changed_fields':changed}))
