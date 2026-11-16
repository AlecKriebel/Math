#!/usr/bin/env python3
"""Create two new root terminals for the completed private editorial packet.

Only this owned directory is read/written. No original input, site, tracker,
network, source code, renderer, subprocess or scientific programme is invoked.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat

E=Path(__file__).absolute().parent

def pin(body):
    return {'bytes':len(body),'SHA256':hashlib.sha256(body).hexdigest()}

def read(path):
    if not path.is_relative_to(E) or not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError('not ordinary owned file')
    return path.read_bytes()

def extent():
    files,dirs=[],[]
    def visit(path):
        with os.scandir(path) as it:
            entries=sorted(it,key=lambda x:x.name)
        for ent in entries:
            p=path/ent.name; rel=p.relative_to(E).as_posix(); mode=p.lstat().st_mode
            if stat.S_ISDIR(mode):
                dirs.append(rel);visit(p)
            elif stat.S_ISREG(mode):
                files.append({'path':rel,**pin(read(p))})
            else:
                raise ValueError('symlink/FIFO/special '+rel)
    visit(E)
    return {'root':str(E),'files':sorted(files,key=lambda x:x['path']),'directories':sorted(dirs)}

def new(name,body):
    with (E/name).open('xb') as f:
        if f.write(body)!=len(body):
            raise ValueError('incomplete terminal write')
        f.flush();os.fsync(f.fileno())

def main():
    terms={'OWNED_MANIFEST.json','FINAL_SEAL.json'}
    if any((E/n).exists() for n in terms):
        raise ValueError('final terminal exists')
    required=['REPORT.md','VERDICT.json','CURRENT_CODE_MANIFEST.json','FINAL_READ_LEDGER.json','EXECUTION_RECEIPTS.json']
    for n in required:
        read(E/n)
    verdict=json.loads(read(E/'VERDICT.json'))
    if verdict['publication_authority'] is not False or verdict['root_copy_adopted'] is not False or verdict['canonical_url'] is not None or verdict['AA'] is not None:
        raise ValueError('separate authority')
    for mode in ['normal','optimized']:
        result=json.loads(read(E/('PRESEAL-'+mode+'.stdout')))
        if result['status']!='PRIVATE_EDITORIAL_COPY_CUSTODY_PASSED' or result['strict_final_namespace'] is not False or read(E/('PRESEAL-'+mode+'.stderr')):
            raise ValueError('actual preseal closure')
    manifest=extent()
    manifest['exact_root_terminal_exclusions']=sorted(terms)
    manifest['subtree_or_future_exclusions']=[]
    mb=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()
    seal={'schema':'row135-private-editorial-final-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'record_id':'23202966','sheet_row':135,'status':'PRIVATE_EDITORIAL_PREPARATION_COMPLETE_PENDING_ROOT_ADOPTION',
          'manifest':pin(mb),'payload_files':len(manifest['files']),
          'total_files_including_exact_two_root_terminals':len(manifest['files'])+2,
          'directories':manifest['directories'],'exact_root_terminal_exclusions':sorted(terms),
          'subtree_or_future_exclusions':[],
          'key_files':{n:pin(read(E/n)) for n in required+['INITIAL_SEAL.json','SOURCE_INPUTS.json','AUTHORING_INPUTS_SEAL.json','PUBLIC_MAIN.html','EDITORIAL_CONFIG.json','candidate/index.html']},
          'actual_preseal_results':{m:json.loads(read(E/('PRESEAL-'+m+'.stdout'))) for m in ['normal','optimized']},
          'original_native_assets_unchanged':4,'original_native_asset_order':['README.md','paper.pdf','main.tex','verification.zip'],
          'whole_ZIP_regular_payloads':28,'native_version_present':False,'printed_version_present':False,
          'full_original_claim_preserved':True,'source_or_scientific_repair':False,'new_scientific_execution':False,
          'root_copy_adopted':False,'publication_authority':False,'production_install_authority':False,
          'deployment_authority':False,'native_tracker_mutation_authority':False,'live_verified':False,'browser_verified':False,
          'canonical_url':None,'AA':None,'follow_up':None,'completion_percent_bounded_editorial':100}
    new('OWNED_MANIFEST.json',mb)
    new('FINAL_SEAL.json',(json.dumps(seal,ensure_ascii=False,indent=2)+'\n').encode())
    actual=extent();actual['files']=[r for r in actual['files'] if r['path'] not in terms]
    if actual['files']!=manifest['files'] or actual['directories']!=manifest['directories']:
        raise ValueError('postseal exact namespace changed')
    print(json.dumps({'status':'SEALED_PRIVATE_EDITORIAL','FINAL_SEAL':pin(read(E/'FINAL_SEAL.json')),
                     'OWNED_MANIFEST':pin(mb),'payload_files':len(manifest['files']),
                     'directories':len(manifest['directories']),'publication_authority':False,
                     'root_copy_adopted':False,'canonical_url':None,'AA':None},sort_keys=True))

if __name__=='__main__':
    main()
