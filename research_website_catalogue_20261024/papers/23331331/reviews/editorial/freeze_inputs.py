#!/usr/bin/env python3
"""One bounded editorial intake; writes only new files inside this packet."""
import hashlib
import json
import os
from pathlib import Path
import stat
from datetime import datetime, timezone

E = Path(__file__).absolute().parent
P = E.parents[3]
S = P / 'papers/23331331/sources'
R = P / 'papers/23331331/reviews/root'

def need(ok, why):
    if not ok:
        raise ValueError(why)

def regular(path):
    need(stat.S_ISREG(path.lstat().st_mode), 'not ordinary file: ' + str(path))
    return path.read_bytes()

def pin(b):
    return {'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest()}

def scan(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'not ordinary root')
    files, dirs = [], []
    def walk(d):
        for ent in sorted(os.scandir(d), key=lambda x: x.name):
            q = Path(ent.path)
            rel = q.relative_to(root).as_posix()
            mode = q.lstat().st_mode
            if stat.S_ISDIR(mode):
                dirs.append(rel)
                walk(q)
            else:
                need(stat.S_ISREG(mode), 'link/special: ' + str(q))
                files.append({'path': rel, **pin(regular(q))})
    walk(root)
    return {'root': str(root), 'files': sorted(files, key=lambda x:x['path']), 'directories': sorted(dirs)}

def new(path, b):
    need(path.is_relative_to(E), 'outside write')
    with path.open('xb') as f:
        f.write(b)

def main():
    need(not (E/'SOURCE_INPUTS.json').exists(), 'intake already exists')
    a = P/'verification/root-clearance-23331331-20261115.json'
    ab = regular(a)
    need(pin(ab) == {'bytes':129113,'SHA256':'27721f2437e7a9af2a8aabcf25f18599a1c667f32d0de2d7836fdc0ca8affc16'}, 'authority pin')
    authority = json.loads(ab)
    cb = regular(R/'ROOT_NATIVE_CUSTODY_CONTRACT_20261115.json')
    need(pin(cb) == {k:authority['root_custody_contract'][k] for k in ('bytes','SHA256')}, 'root custody pin')
    contract = json.loads(cb)
    namespaces=[]
    for expected in contract['namespaces']:
        current=scan(Path(expected['root']))
        need(current == expected, 'whole original namespace mismatch ' + expected['root'])
        namespaces.append(current)
    namespaces.append(scan(R))
    source_ready=json.loads(regular(S/'SOURCE_READY.json'))
    need(json.dumps(source_ready,ensure_ascii=False)==json.dumps(authority['whole_original_SOURCE_READY'],ensure_ascii=False), 'whole typed ordered READY')
    for name,filename,field in [('scope','VERDICT.json','whole_literal_scope_VERDICT'),('adversarial','CUSTOM_VERDICT.json','whole_literal_adversarial_VERDICT')]:
        v=json.loads(regular(P/f'papers/23331331/reviews/{name}/{filename}'))
        need(json.dumps(v,ensure_ascii=False)==json.dumps(authority[field],ensure_ascii=False), 'literal verdict '+name)
    core=[]
    for q in sorted((P/'scripts').glob('*.py'))+[P/'verification/final-content-check.py']:
        core.append({'path':str(q),**pin(regular(q)), 'role':'sole authorized additive helper' if q.name=='checkpoint_subtree.py' else 'original core'})
    need(len(core)==18 and sum(x['role']=='original core' for x in core)==17, 'qualified core extent')
    need(next(x['SHA256'] for x in core if x['role']=='sole authorized additive helper')=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0', 'helper pin')
    (E/'inputs').mkdir()
    (E/'inputs/blobs').mkdir()
    originals=[]
    for ns in namespaces:
        for row in ns['files']:
            originals.append({'path':str(Path(ns['root'])/row['path']),**{k:row[k] for k in ('bytes','SHA256')}})
    originals.extend([{'path':str(a),**pin(ab)}]+[{k:x[k] for k in ('path','bytes','SHA256')} for x in core])
    originals=sorted({x['path']:x for x in originals}.values(),key=lambda x:x['path'])
    for row in originals:
        b=regular(Path(row['path']))
        need(pin(b)=={k:row[k] for k in ('bytes','SHA256')}, 'copy race')
        dest=E/'inputs/blobs'/row['SHA256']
        if dest.exists():
            need(regular(dest)==b,'blob collision')
        else:
            new(dest,b)
        row['copy']='inputs/blobs/'+row['SHA256']
    result={'schema':'row133-editorial-whole-source-inputs-v1','UTC':datetime.now(timezone.utc).isoformat(),
      'namespaces':namespaces,'original_files':originals,'qualified_core':core,
      'whole_original_SOURCE_READY':source_ready,'whole_root_authority':authority,
      'no_web_Git_Sheet_or_science_execution':True,
      'current_context_outside_immutable_history':{'parent_reported_native_science_count':106,'native_status':'Reviewed/preparing','native_live_read':False,'root_historical_pending_flag_preserved':True},
      'original_raw_objects_preserved_as_whole_bytes':True}
    new(E/'SOURCE_INPUTS.json',(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
    new(E/'INPUTS_SEAL.json',(json.dumps({'SOURCE_INPUTS':pin(regular(E/'SOURCE_INPUTS.json')),'source_ready':pin(regular(S/'SOURCE_READY.json')),'root_authority':pin(ab),'original_files':len(originals),'namespaces':len(namespaces),'qualified_core_original':17,'additive_helper':1},indent=2)+'\n').encode())
    print(json.dumps({'status':'FROZEN_SOURCE_ONLY','original_files':len(originals),'namespaces':len(namespaces),'blob_files':len(list((E/'inputs/blobs').iterdir()))}))

if __name__=='__main__':
    main()
