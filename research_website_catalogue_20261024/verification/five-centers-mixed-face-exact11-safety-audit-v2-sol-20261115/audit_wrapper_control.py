"""Fresh exact changed audit-wrapper fixture; no reviewed module import or live reads."""
from pathlib import Path,PurePosixPath
import ast,hashlib,json,os,stat,tempfile
D=Path(__file__).resolve().parent;O=D.parent/'five-centers-mixed-face-production-integration-preparation-v2-sol-20261115'

def require(ok,label):
 if not ok:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 names={'need','sha','read','obj','pin','safe_rel','extent','live_path','closed_namespace','sealed_namespace'}
 tree=ast.parse((O/'exact11_lib.py').read_bytes());nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];records=[]
 with tempfile.TemporaryDirectory(prefix='changed-audit-wrapper-',dir=D) as t:
  root=Path(t);packet=root/'audit';packet.mkdir();(packet/'inputs').mkdir();rows=[]
  for i in range(721):
   p=packet/('leaf%04d'%i);p.write_bytes(b'j');rows.append({'path':str(p),'bytes':1,'SHA256':sha(b'j')})
  mb=json.dumps({'files':rows}).encode();(packet/'FINAL_MANIFEST.json').write_bytes(mb);cb=b'own closure';(packet/'FINAL_CLOSURE.json').write_bytes(cb)
  desc=lambda b:{'bytes':len(b),'SHA256':sha(b)}
  sb=json.dumps({'own_final_owned_payloads':721,'bindings':{'FINAL_MANIFEST.json':desc(mb),'FINAL_CLOSURE.json':desc(cb)}}).encode();(packet/'FINAL_SEAL.json').write_bytes(sb)
  (root/'SEALED_NAMESPACE_CONTRACT.json').write_text(json.dumps({'audit_directories':['inputs']}))
  e=dict(Path=Path,PurePosixPath=PurePosixPath,json=json,hashlib=hashlib,os=os,stat=stat,O=root,A=packet,AUDIT_SEAL=sha(sb),W=root/'never-live',LIVE_AUTHORIZED=False)
  exec(compile(ast.Module(body=nodes,type_ignores=[]),'<exact changed audit wrapper>','exec'),e)
  check=lambda:e['sealed_namespace']('audit')
  observed,payload=check();require(len(payload)==721,'whole721 selected changed wrapper')
  def reject(label):
   try:check()
   except RuntimeError as err:records.append({'case':label,'rejected':True,'diagnostic':str(err)})
   else:raise RuntimeError('missed '+label)
  (packet/'revisions').mkdir();reject('undeclared future-named empty directory');(packet/'revisions').rmdir()
  os.mkfifo(packet/'fifo');reject('FIFO');(packet/'fifo').unlink()
  (packet/'inputs-link').symlink_to(packet/'inputs');reject('symlink to declared empty inputs');(packet/'inputs-link').unlink()
  (packet/'inputs/FINAL_SEAL.json').write_bytes(b'not a root exclusion');reject('nested terminal basename');(packet/'inputs/FINAL_SEAL.json').unlink()
  (packet/'inputs').rmdir();reject('missing declared legitimate empty directory');(packet/'inputs').mkdir();check()
  original=e['read'];calls=[0]
  def interleaved(path):
   b=original(path)
   if path==packet/'FINAL_SEAL.json':calls[0]+=1;(packet/'FINAL_SEAL.json').write_bytes(b'changed after seal read')
   return b
  e['read']=interleaved
  got,_=check();require(got==json.loads(sb) and calls[0]==1,'same authenticated seal buffer retained in changed wrapper')
 print(json.dumps({'status':'PASS_FRESH_EXACT_CHANGED_AUDIT_WRAPPER','actual_selected_current_function':'sealed_namespace','toy_payloads':721,'declared_empty_inputs_accepted':True,'negative_cases':records,'seal_interleaving_reads':calls[0],'authenticated_original_seal_parsed':True,'actual_source_packet_or_runtime_or_Git_touched':False,'all_toy_writes_inside_own_removed_temporary_child':True},indent=2))
if __name__=='__main__':main()
