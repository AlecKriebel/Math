#!/usr/bin/env python3
"""Read-only final-packet custody and computational replay; accepts no overrides."""
from pathlib import Path,PurePosixPath
import hashlib,json,runpy,subprocess,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def require(t,m):
 if not t:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 require(len(sys.argv)==1,'No arguments accepted')
 seal=json.loads((HERE/'PACKET_SEAL.json').read_text())
 require(sha(HERE/'PACKET_MANIFEST.json')==seal['manifest_sha256'],'Packet manifest seal mismatch')
 m=json.loads((HERE/'PACKET_MANIFEST.json').read_text());expected={}
 for x in m['files']:
  q=PurePosixPath(x['path'])
  require(not q.is_absolute() and str(q)==x['path'] and '..' not in q.parts and '\\' not in x['path'],'Unsafe manifest path')
  require(x['path'] not in expected,'Duplicate manifest path');expected[x['path']]=x
 for p in HERE.rglob('*'):require(not p.is_symlink(),'Packet symlink')
 actual={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file()}
 require(actual==set(expected)|{'PACKET_MANIFEST.json','PACKET_SEAL.json'},'Packet file set changed')
 for name,x in expected.items():
  p=HERE/name;require(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'Packet bytes changed: '+name)
 binds=json.loads((HERE/'INPUT_BINDINGS.json').read_text())
 for name,x in binds['files'].items():
  p=ROOT/name;require(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'External input changed: '+name)
 old=ROOT/'reviews/analytic';em=json.loads((old/'EARLY_MANIFEST.json').read_text())
 for x in em['files']:
  p=old/x['path'];require(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'Predecessor file changed: '+x['path'])
 own=subprocess.run([sys.executable,'-B',str(HERE/'independent_verify.py')],capture_output=True,text=True,check=True)
 require(json.loads(own.stdout)==json.loads((HERE/'INDEPENDENT_CHECKS.json').read_text()),'Independent replay changed')
 supplied=ROOT/'sources/published-source/birational-cycle-verification/verify.py'
 suppliedrun=subprocess.run([sys.executable,'-B',str(supplied)],capture_output=True,text=True,check=True)
 require(json.loads(suppliedrun.stdout)==json.loads((HERE/'SUPPLIED_REPLAY.json').read_text()),'Supplied replay changed')
 mutations=subprocess.run([sys.executable,'-B',str(HERE/'mutation_controls.py')],capture_output=True,text=True,check=True)
 require(json.loads(mutations.stdout)==json.loads((HERE/'MUTATION_CHECKS.json').read_text()),'Mutation replay changed')
 print(json.dumps({'status':'PASS','manifest_sha256':seal['manifest_sha256'],'packet_files_verified':len(expected),'external_inputs_verified':len(binds['files']),'predecessor_files_verified':len(em['files']),'independent_controls':json.loads(own.stdout)['total_controls'],'supplied_finite_controls':json.loads(suppliedrun.stdout)['finite_checks'],'supplied_all_odd_controls':json.loads(suppliedrun.stdout)['all_odd_prime_checks'],'scope':'Custody and exact finite replay only; proof and primary interfaces remain essential'},sort_keys=True,indent=2))
if __name__=='__main__':main()
