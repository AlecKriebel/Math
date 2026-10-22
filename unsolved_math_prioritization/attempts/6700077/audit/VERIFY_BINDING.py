#!/usr/bin/env python3
"""Read-only external-anchor binding audit; adversarial writes occur only in temporary copies."""
from pathlib import Path
import argparse, hashlib, json, shutil, tempfile
ANCHOR='b25e29914341432f65924b883eb5361158e3fee1249bcdab57b2281cfbb662b2'

def verify(root, anchor=ANCHOR):
    root=Path(root)
    manifest=root/'AUTHOR_MANIFEST.json'
    if manifest.is_symlink() or not manifest.is_file():
        raise ValueError('manifest file kind')
    raw=manifest.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=anchor:
        raise ValueError('external anchor mismatch')
    data=json.loads(raw)
    if data.get('schema')!='authored-packet-sha256-v1' or data.get('problem_id')!='6700077':
        raise ValueError('wrong schema or target')
    expected={'AUTHOR_MANIFEST.json'}
    for rec in data['files']:
        name=rec['path']
        if not isinstance(name,str) or Path(name).name!=name or name in ('.','..') or name in expected:
            raise ValueError('path violation')
        expected.add(name)
        f=root/name
        if f.is_symlink() or not f.is_file():
            raise ValueError('payload file kind')
        b=f.read_bytes()
        if len(b)!=rec['bytes'] or hashlib.sha256(b).hexdigest()!=rec['sha256']:
            raise ValueError('payload hash or length')
    if {f.name for f in root.iterdir()}!=expected:
        raise ValueError('payload set')
    return len(expected)-1

def adversarial(root):
    rejected=[]
    for mode in ('payload_changed','payload_missing','extra_file','extra_directory','payload_symlink','manifest_symlink','unbound_rehashed_payload','manifest_target_change','manifest_path_traversal','manifest_duplicate_record'):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'packet'
            shutil.copytree(root,dest)
            f=dest/'README.md'; m=dest/'AUTHOR_MANIFEST.json'
            if mode=='payload_changed': f.write_bytes(f.read_bytes()+b'\nchanged')
            elif mode=='payload_missing': f.unlink()
            elif mode=='extra_file': (dest/'extra.txt').write_text('extra')
            elif mode=='extra_directory': (dest/'extra').mkdir()
            elif mode=='payload_symlink': f.unlink(); f.symlink_to(dest/'SOURCE_SCOPE.md')
            elif mode=='manifest_symlink':
                raw=m.read_bytes(); m.unlink(); q=Path(tmp)/'manifest';q.write_bytes(raw);m.symlink_to(q)
            else:
                data=json.loads(m.read_bytes())
                if mode=='unbound_rehashed_payload':
                    f.write_bytes(f.read_bytes()+b'\nchanged')
                    for row in data['files']:
                        if row['path']=='README.md':
                            row['bytes']=len(f.read_bytes());row['sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
                elif mode=='manifest_target_change': data['problem_id']='different'
                elif mode=='manifest_path_traversal': data['files'][0]['path']='../escape'
                elif mode=='manifest_duplicate_record': data['files'].append(data['files'][0])
                m.write_text(json.dumps(data))
            try: verify(dest)
            except (ValueError,OSError,KeyError,TypeError): rejected.append(mode)
            else: raise RuntimeError('Accepted mutation: '+mode)
    return rejected

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('packet');p.add_argument('--self-test',action='store_true');args=p.parse_args()
    result={'outcome':'PASS','external_author_manifest_sha256':ANCHOR,'verified_payload_files':verify(args.packet)}
    if args.self_test: result['independent_binding_negatives_rejected']=adversarial(args.packet)
    print(json.dumps(result,indent=2,sort_keys=True))
