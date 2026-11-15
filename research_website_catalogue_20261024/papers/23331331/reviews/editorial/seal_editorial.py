#!/usr/bin/env python3
"""Create only two new root terminals after bounded editorial work is complete."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat

E=Path(__file__).absolute().parent

def pin(b):
    return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}

def read(p):
    if not stat.S_ISREG(p.lstat().st_mode):
        raise ValueError('not ordinary file '+str(p))
    return p.read_bytes()

def extent():
    files,dirs=[],[]
    def walk(d):
        for ent in sorted(os.scandir(d),key=lambda x:x.name):
            p=Path(ent.path);r=p.relative_to(E).as_posix();m=p.lstat().st_mode
            if stat.S_ISDIR(m):dirs.append(r);walk(p)
            elif stat.S_ISREG(m):files.append({'path':r,**pin(read(p))})
            else:raise ValueError('nonordinary entry '+r)
    walk(E)
    return {'root':str(E),'files':sorted(files,key=lambda x:x['path']),'directories':sorted(dirs)}

def new(name,b):
    with (E/name).open('xb') as f:
        if f.write(b)!=len(b):raise ValueError('incomplete write')

def main():
    if (E/'FINAL_SEAL.json').exists() or (E/'OWNED_MANIFEST.json').exists():
        raise ValueError('root terminal already exists')
    required=['REPORT.md','VERDICT.json','FINAL_READ_LEDGER.json','CURRENT_CODE_MANIFEST.json','EXECUTION_RECEIPTS.json']
    for n in required:read(E/n)
    verdict=json.loads(read(E/'VERDICT.json'))
    if verdict['publication_authority'] is not False or verdict['canonical_url'] is not None or verdict['AA'] is not None:
        raise ValueError('authority separation')
    for mode in ('normal','optimized'):
        result=json.loads(read(E/f'PRESEAL-{mode}.stdout'))
        if result['status']!='SOURCE_COPY_CUSTODY_PASSED' or read(E/f'PRESEAL-{mode}.stderr'):
            raise ValueError('actual preseal closure')
    manifest=extent()
    mb=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()
    seal={'schema':'row133-editorial-final-v1','UTC':datetime.now(timezone.utc).isoformat(),
      'status':'FINAL_PRIVATE_EDITORIAL_PREPARATION_PENDING_ROOT_ADOPTION','record_id':'23331331','sheet_row':133,
      'OWNED_MANIFEST':pin(mb),'payload_files':len(manifest['files']),'directories':manifest['directories'],
      'total_files_including_exact_two_root_terminals':len(manifest['files'])+2,
      'root_terminal_exclusions_exact':['OWNED_MANIFEST.json','FINAL_SEAL.json'],
      'future_or_runtime_prefix_exclusions':[],
      'key_files':{n:pin(read(E/n)) for n in required+['INITIAL_SEAL.json','INPUTS_SEAL.json','EDITORIAL_CONFIG.json','PUBLIC_MAIN.html','candidate/PUBLIC_HEAD.html','candidate/index.html']},
      'preseal_results':{m:json.loads(read(E/f'PRESEAL-{m}.stdout')) for m in ('normal','optimized')},
      'original_files_unchanged':421,'strict_original_namespaces':4,'qualified_original_core':17,'sole_additive_core_helper':1,
      'unchanged_native_PDF_ZIP':True,'whole_original_claim_preserved':True,'new_scientific_execution':False,
      'publication_authority':False,'root_copy_adoption':False,'install_authority':False,'deployment_authority':False,
      'native_tracker_mutation_authority':False,'live_verified':False,'browser_verified':False,
      'canonical_url':None,'AA':None,'follow_up':None,'completion_percent_bounded_editorial':100}
    new('OWNED_MANIFEST.json',mb)
    new('FINAL_SEAL.json',(json.dumps(seal,ensure_ascii=False,indent=2)+'\n').encode())
    actual=extent();actual['files']=[x for x in actual['files'] if x['path'] not in {'OWNED_MANIFEST.json','FINAL_SEAL.json'}]
    if actual!=manifest:raise ValueError('post-write exact namespace mismatch')
    print(json.dumps({'status':'SEALED_PRIVATE_EDITORIAL','FINAL_SEAL':pin(read(E/'FINAL_SEAL.json')),
      'OWNED_MANIFEST':pin(mb),'payload_files':len(manifest['files']),'directories':len(manifest['directories']),
      'post_write_exact_namespace_verified':True,'publication_authority':False,'canonical_url':None,'AA':None},sort_keys=True))

if __name__=='__main__':
    main()
