#!/usr/bin/env python3
"""Ensure the package pin rejects detached A1 and byte-level tampering."""
import hashlib,json,pathlib,shutil,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parent

def need(c,m):
 if not c:raise ValueError(m)
def main():
 pin=hashlib.sha256((ROOT/'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest();out={'schema':1,'clean_integrity_replays':0,'mutations_rejected':[],'restored_clean_replays':0}
 with tempfile.TemporaryDirectory(prefix='edge publication tests ') as td:
  dest=pathlib.Path(td)/'relocated package';shutil.copytree(ROOT,dest,ignore=shutil.ignore_patterns('__pycache__'))
  def run(opt):return subprocess.run([sys.executable]+(['-O'] if opt else [])+[str(dest/'verify_package.py'),'--manifest-sha256',pin,'--integrity-only'],cwd=td,capture_output=True,text=True,timeout=30)
  for opt in (False,True):need(run(opt).returncode==0,'relocated clean integrity failed');out['clean_integrity_replays']+=1
  for label,name in [('missing A1 correction','audit/CORRECTION.md'),('altered A1 patch','audit/verify_quotient_guard.patch'),('changed author mathematics','author/MATHEMATICAL_NOTE.md'),('corrupt frozen audit archive','archives/EDGE_DEGREE_30000433_INDEPENDENT_AUDIT_SAFE.zip'),('rewritten publication manifest','PUBLICATION_MANIFEST.json')]:
   p=dest/name;raw=p.read_bytes()
   if label=='missing A1 correction':p.unlink()
   else:p.write_bytes(raw+b'\n ')
   for opt in (False,True):
    r=run(opt);need(r.returncode!=0 and 'FAIL:' in r.stderr,'mutation accepted: '+label);out['mutations_rejected'].append({'mutation':label,'optimized':opt})
   p.write_bytes(raw)
  for opt in (False,True):need(run(opt).returncode==0,'restored integrity failed');out['restored_clean_replays']+=1
 print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
