#!/usr/bin/env python3
"""Relocated outer-integrity positive and negative controls in temporary copies."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def need(ok,message):
    if not ok: raise RuntimeError(message)


def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True);args=p.parse_args()
    root=Path(__file__).absolute().parent;status=json.loads((root/'PUBLICATION_STATUS.json').read_bytes())
    result={'relocated_positive_modes':[],'rejected_controls':[],'original_inputs_preserved':True}
    cases=['positive','proof-byte','missing-file','extra-file','extra-directory','manifest-byte','wrong-pin','invalid-pin','proof-symlink','manifest-symlink','directory-symlink','root-symlink','author-zip-byte','audit-zip-byte','unmanifested-bytecode','verifier-symlink']
    with tempfile.TemporaryDirectory(prefix='ricci publication controls ') as tmp:
        parent=Path(tmp)
        for mode in [[],['-O']]:
            label='optimized' if mode else 'normal'
            for name in cases:
                dest=parent/(label+' '+name);shutil.copytree(root,dest);target=dest/'author/ATTEMPT_1.md';pin=args.expected_manifest
                if name=='proof-byte':
                    b=target.read_bytes();target.write_bytes(b'!'+b[1:])
                elif name=='missing-file': target.unlink()
                elif name=='extra-file': (dest/'unexpected.txt').write_text('unexpected')
                elif name=='extra-directory': (dest/'unexpected').mkdir()
                elif name=='manifest-byte':
                    q=dest/'PUBLICATION_MANIFEST.json';q.write_bytes(q.read_bytes()+b' ')
                elif name=='wrong-pin':pin='0'*64
                elif name=='invalid-pin':pin='G'*64
                elif name in ['proof-symlink','manifest-symlink','verifier-symlink']:
                    q={'proof-symlink':target,'manifest-symlink':dest/'PUBLICATION_MANIFEST.json','verifier-symlink':dest/'verify_publication.py'}[name];external=parent/(label+' '+name+' external');external.write_bytes(q.read_bytes());q.unlink();q.symlink_to(external)
                elif name=='directory-symlink': (dest/'unexpected').symlink_to(dest/'archives',target_is_directory=True)
                elif name=='root-symlink':
                    link=parent/(label+' linked root');link.symlink_to(dest,target_is_directory=True);dest=link
                elif name in ['author-zip-byte','audit-zip-byte']:
                    key='author_archive' if name=='author-zip-byte' else 'audit_archive';q=dest/'archives'/status[key];q.write_bytes(q.read_bytes()+b'!')
                elif name=='unmanifested-bytecode':(dest/'author'/'math_check.pyc').write_bytes(b'not bytecode')
                run=subprocess.run([sys.executable,'-I',*mode,'-B',str(dest/'verify_publication.py'),'--expected-manifest',pin],cwd=parent,capture_output=True,text=True,timeout=300)
                if name=='positive':
                    need(run.returncode==0,'relocated positive failed: '+run.stderr);result['relocated_positive_modes'].append(label)
                else:
                    need(run.returncode!=0 and 'REJECT:' in run.stderr,'bad negative: '+label+':'+name);result['rejected_controls'].append(label+':'+name)
    result['negative_control_count']=len(result['rejected_controls']);print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':main()
