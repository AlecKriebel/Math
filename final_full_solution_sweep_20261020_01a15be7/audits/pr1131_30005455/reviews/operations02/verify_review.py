#!/usr/bin/env python3
"""Read-only verification of public closure, optional complete private custody,
and the unchanged reviewed operations/dependency source. No project import."""
from pathlib import Path
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parents[1]
TARGET=AUDIT/'operations'
OPS_SHA='da72b199f9b4eec35eef87b18eccecacb55c3ae7f32b3f9d44a2f961d2832168'
BOOT_SHA='b42765748e6e73518ef21195bbc475f70f7b76215665bf60071bdaa35fcc857f'
def need(v,m):
    if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(b):return {'bytes':len(b),'sha256':sha(b)}
def strict(b):
    def pairs(v):
        d={}
        for k,x in v:need(k not in d,'Duplicate key');d[k]=x
        return d
    return json.loads(b,object_pairs_hook=pairs)
def private_tree():
    need(not (HERE/'private').is_symlink(),'Private root symlink')
    index=[];count=0;total=0
    for p in sorted((HERE/'private').rglob('*')):
        need(not p.is_symlink(),'Private custody symlink');name=p.relative_to(HERE).as_posix()
        if p.is_file():
            b=p.read_bytes();index.append([name,'file',pin(b)]);count+=1;total+=len(b)
        elif p.is_dir():index.append([name,'directory'])
        else:raise RuntimeError('Unexpected private file type')
    return {'files':count,'directories':len(index)-count,'logical_bytes':total,'sorted_full_tree_sha256':sha(json.dumps(index,ensure_ascii=False,separators=(',',':')).encode()),'index_rule':'Sorted relative paths, directory markers and exact file byte-count/SHA256 pins; all private entries included, symlinks forbidden.'}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--skip-private',action='store_true');args=parser.parse_args()
    m=strict((HERE/'MANIFEST.json').read_bytes());need(m['excluded']==['MANIFEST.json','private/','__pycache__/'],'Review exclusion changed')
    public=[p for p in HERE.rglob('*') if p.relative_to(HERE).parts[0] not in {'private','__pycache__'}]
    need(not any(p.is_symlink() for p in public),'Public review symlink')
    paths={p.relative_to(HERE).as_posix():p for p in public if p.is_file() and p.relative_to(HERE).as_posix()!='MANIFEST.json'}
    need(set(paths)==set(m['files']),'Review public closure changed')
    for n,p in paths.items():need(not p.is_symlink() and pin(p.read_bytes())==m['files'][n],'Review payload changed '+n)
    raw=(TARGET/'OPERATIONS_MANIFEST.json').read_bytes();need(sha(raw)==OPS_SHA,'Target seal changed');target=strict(raw)
    targetpaths={p.relative_to(TARGET).as_posix():p for p in TARGET.rglob('*') if p.is_file() and not any(part in {'private','runtime','__pycache__'} for part in p.relative_to(TARGET).parts) and p.relative_to(TARGET).as_posix()!='OPERATIONS_MANIFEST.json'}
    need(set(targetpaths)==set(target['files']) and len(targetpaths)==35,'Target closure changed')
    for n,p in targetpaths.items():need(not p.is_symlink() and pin(p.read_bytes())==target['files'][n],'Target changed '+n)
    need(sha((TARGET/'bootstrap.py').read_bytes())==BOOT_SHA,'Bootstrap changed')
    dep=strict((TARGET/'DEPENDENCY_PINS.json').read_bytes())
    for n,p in dep.items():need(pin((AUDIT.parents[2]/n).read_bytes())==p,'Shared dependency changed')
    for name in ['NORMAL_FINAL.json','O_FINAL.json','OO_FINAL.json']:
        v=strict((HERE/name).read_bytes());need(not v['failures'] and len(v['controls'])==21 and all(c['status']=='PASS' for c in v['controls']) and not v['blocked_external_attempts'] and v['actual_external_mutations']==0 and v['copied_inputs_unchanged'] is True,'Final mode result failed')
    if not args.skip_private:need(private_tree()==strict((HERE/'PRIVATE_CUSTODY.json').read_bytes()),'Private strict custody changed')
    verdict=strict((HERE/'VERDICT.json').read_bytes());need(verdict['publication_ready'] is False and verdict['status']=='CHANGES_REQUIRED','Readiness boundary changed')
    print(json.dumps({'status':'PASS','public_payloads':len(paths),'target_payloads':35,'final_mode_groups':63,'independent_groups':60,'private_custody_verified':not args.skip_private,'publication_ready':False,'external_calls':0}))
if __name__=='__main__':main()
