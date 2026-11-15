#!/usr/bin/env python3
"""Read-only owned-packet and external-input replay; no command-line overrides."""
from pathlib import Path
import hashlib,json,subprocess,sys
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;P=E.parents[2]
def require(t,m):
 if not t:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 require(len(sys.argv)==1,'No overrides accepted')
 seal=json.loads((E/'SEAL.json').read_text());require(sha(E/'MANIFEST.json')==seal['manifest_sha256'],'Owned manifest changed')
 manifest=json.loads((E/'MANIFEST.json').read_text());expected={x['path']:x for x in manifest['files']}
 require(set(expected)=={p.name for p in E.iterdir() if p.is_file()}-{'MANIFEST.json','SEAL.json'},'Owned file set changed')
 for name,x in expected.items():require(not (E/name).is_symlink() and (E/name).stat().st_size==x['bytes'] and sha(E/name)==x['sha256'],'Owned file changed: '+name)
 result=json.loads((E/'RESULT.json').read_text())
 for name,x in result['input_bindings'].items():require((P/name).stat().st_size==x['bytes'] and sha(P/name)==x['sha256'],'Original input changed: '+name)
 helper=P/'verification/local-banach-mtp2-stage-sol-20261025/resume/banach_mtp2_source.py';require(sha(helper)==result['helper_sha256'],'Source helper changed')
 replay=subprocess.run([sys.executable,'-B',str(E/'verify_native.py')],capture_output=True,text=True,check=True)
 require(json.loads(replay.stdout)==result,'Native audit replay changed')
 optimized=subprocess.run([sys.executable,'-B','-O',str(E/'verify_native.py')],capture_output=True,text=True,check=True)
 require(json.loads(optimized.stdout)==result,'Optimized native audit replay changed')
 print(json.dumps({'assessment':'NATIVE_PACKET_AND_BOTH_REPLAYS_SUPPORTED','owned_files_verified':len(expected),'original_inputs_verified':len(result['input_bindings']),'native_checks':result['check_count'],'in_memory_negative_controls':len(result['in_memory_negative_controls']),'helper_sha256':result['helper_sha256'],'manifest_sha256':seal['manifest_sha256']},indent=2))
if __name__=='__main__':main()
