#!/usr/bin/env python3
"""Adversarial integrity controls in disposable copies; never modify the payload."""
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CASES=['changed_bytes','same_size_changed_bytes','missing_file','extra_file','extra_directory','symlink_file','unsafe_manifest_path','duplicate_manifest_path','manifest_self_entry','wrong_byte_count','wrong_hash','noncanonical_manifest','duplicate_json_key','wrong_external_pin','nonregular_object']
def require(ok,message):
    if not ok:raise RuntimeError(message)
def canonical(obj):return (json.dumps(obj,indent=2,sort_keys=True)+'\n').encode()
def run(root,*flags,expected=None):
    args=[sys.executable,'-I','-B',*flags,str(root/'verify_package.py')]
    if expected:args+=['--manifest-sha256',expected]
    return subprocess.run(args,cwd=root,capture_output=True,timeout=30)
def main():
    require(run(ROOT).returncode==0,'Original package failed verification')
    results=[]
    with tempfile.TemporaryDirectory(prefix='percolation-tamper-controls-') as temp:
        for name in CASES:
            work=Path(temp)/name;shutil.copytree(ROOT,work)
            for p in work.rglob('*'):
                if p.is_file():p.chmod(0o644)
            readme=work/'README.md';manifest=work/'MANIFEST.json';m=json.loads(manifest.read_bytes())
            if name=='changed_bytes':readme.write_bytes(readme.read_bytes()+b'changed\n')
            elif name=='same_size_changed_bytes':
                data=readme.read_bytes();readme.write_bytes(b'!'+data[1:])
            elif name=='missing_file':readme.unlink()
            elif name=='extra_file':(work/'unexpected.json').write_text('{}')
            elif name=='extra_directory':(work/'unexpected').mkdir()
            elif name=='symlink_file':(work/'unexpected').symlink_to('README.md')
            elif name=='nonregular_object':os.mkfifo(work/'unexpected_fifo')
            elif name=='unsafe_manifest_path':m['files'][0]['path']='../outside';manifest.write_bytes(canonical(m))
            elif name=='duplicate_manifest_path':m['files'].append(copy.deepcopy(m['files'][0]));manifest.write_bytes(canonical(m))
            elif name=='manifest_self_entry':m['files'][0]['path']='MANIFEST.json';manifest.write_bytes(canonical(m))
            elif name=='wrong_byte_count':m['files'][0]['bytes']+=1;manifest.write_bytes(canonical(m))
            elif name=='wrong_hash':m['files'][0]['sha256']='0'*64;manifest.write_bytes(canonical(m))
            elif name=='noncanonical_manifest':manifest.write_text(json.dumps(m))
            elif name=='duplicate_json_key':manifest.write_bytes(b'{"schema":"discarded",'+manifest.read_bytes()[1:])
            expected='0'*64 if name=='wrong_external_pin' else None
            for label,flags in [('normal',[]),('optimized',['-O']),('double_optimized',['-OO'])]:
                cp=run(work,*flags,expected=expected)
                require(cp.returncode!=0,'Tamper accepted: '+name+' '+label)
            results.append({'case':name,'rejected_in_all_three_modes':True})
    print(json.dumps({'status':'PASS','case_count':len(results),'verification_invocations':3*len(results),'modes':['normal','optimized','double_optimized'],'original_package_intact':run(ROOT).returncode==0,'controls':results},indent=2,sort_keys=True))
if __name__=='__main__':main()
