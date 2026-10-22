#!/usr/bin/env python3
"""Runs trusted verifier against copies; never modifies the original packet."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def require(condition,message):
    if not condition:
        raise RuntimeError(message)

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--manifest-sha256',required=True);args=parser.parse_args()
    original=args.root.resolve();trusted=original/'verify_packet.py';pin=args.manifest_sha256
    require(digest(original/'MANIFEST.json')==pin,'original pin mismatch')
    before={p.name:digest(p) for p in original.iterdir()}
    reports=[]
    integrity_names=['changed_payload','missing_payload','unexpected_file','unexpected_directory',
                     'nested_manifest','symlink_member','changed_manifest','wrong_pin',
                     'duplicate_entry','unsafe_path','wrong_bytes','duplicate_json_key']
    math_mutations=[
        ('false_surjection','({2:1,3:1}.get(d,0))','({2:0,3:0}.get(d,0))'),
        ('wrong_monomial_count','count == n*d+1','count == n*d+2'),
        ('missing_point_defect','== [0,0,0,1]','== [0,0,0,0]'),
        ('wrong_residual','u-v+t == -4','u-v+t == 0'),
    ]
    for mode in (0,1,2):
        flags=[] if mode==0 else ['-O' if mode==1 else '-OO']
        with tempfile.TemporaryDirectory(prefix='unexpected-controls-') as td:
            base=Path(td)
            def invoke(root,pin_value):
                return subprocess.run([sys.executable,*flags,'-I','-B',str(trusted),'--root',str(root),'--manifest-sha256',pin_value],cwd=base,capture_output=True,timeout=60)
            fresh=base/'relocated';shutil.copytree(original,fresh)
            good=invoke(fresh,pin)
            require(good.returncode==0,'relocated clean verification failed')
            require(json.loads(good.stdout)['optimization']==mode,'wrong verified optimization')
            for name in integrity_names:
                root=base/name;shutil.copytree(original,root);use_pin=pin
                if name=='changed_payload':
                    p=root/'APPROACH_2.md';p.write_bytes(p.read_bytes()+b'\nchanged\n')
                elif name=='missing_payload': (root/'APPROACH_2.md').unlink()
                elif name=='unexpected_file': (root/'EXTRA.txt').write_text('extra')
                elif name=='unexpected_directory': (root/'extra').mkdir()
                elif name=='nested_manifest':
                    (root/'extra').mkdir();(root/'extra'/'MANIFEST.json').write_text('{}')
                elif name=='symlink_member':
                    (root/'APPROACH_2.md').unlink();(root/'APPROACH_2.md').symlink_to(original/'APPROACH_2.md')
                elif name=='changed_manifest':
                    p=root/'MANIFEST.json';p.write_bytes(p.read_bytes()+b' ')
                elif name=='wrong_pin': use_pin='0'*64
                elif name=='duplicate_json_key':
                    p=root/'MANIFEST.json';s=p.read_text();p.write_text(s.replace('"schema":','"schema":"source-free-flat-v1","schema":',1));use_pin=digest(p)
                else:
                    p=root/'MANIFEST.json';m=json.loads(p.read_text())
                    if name=='duplicate_entry':m['files'].append(m['files'][0])
                    elif name=='unsafe_path':m['files'][0]['path']='../escaped'
                    elif name=='wrong_bytes':m['files'][0]['bytes']+=1
                    p.write_text(json.dumps(m));use_pin=digest(p)
                bad=invoke(root,use_pin)
                require(bad.returncode!=0,'accepted corruption: '+name)
            # Mutating code is a negative diagnostic; this is not a new trusted packet.
            for name,old,new in math_mutations:
                p=base/(name+'.py');s=(original/'check_math.py').read_text()
                require(s.count(old)==1,'ambiguous mathematical mutation')
                p.write_text(s.replace(old,new,1))
                bad=subprocess.run([sys.executable,*flags,'-I','-B',str(p)],cwd=base,capture_output=True,timeout=60)
                require(bad.returncode!=0,'accepted false mathematical control: '+name)
                require(b'CheckFailure' in bad.stderr,'mathematical control failed for wrong reason')
            reports.append({'optimization':mode,'clean_relocations_passed':1,'integrity_rejections':len(integrity_names),'mathematical_rejections':len(math_mutations)})
    after={p.name:digest(p) for p in original.iterdir()}
    require(before==after,'original packet changed')
    print(json.dumps({'status':'PASS','runs':reports,'original_unchanged':True},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
