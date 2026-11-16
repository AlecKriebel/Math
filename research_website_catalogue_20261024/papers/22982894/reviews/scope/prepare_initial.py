#!/usr/bin/env python3
"""Explicit source/core metadata and fresh manuscript document derivatives.
Default inert; no project/native/scientific imports or programme execution.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import stat
import subprocess
import sys

A=Path(__file__).resolve().parent
P=A.parents[3]
S=A.parents[1]/'sources'

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def need(ok,message):
    if not ok:
        raise ValueError(message)

def pin(path):
    body=path.read_bytes()
    return {'path':str(path),'bytes':len(body),'SHA256':hashlib.sha256(body).hexdigest()}

def put(name,value):
    need(not (A/name).exists(),'refuse overwrite '+name)
    (A/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def main():
    if sys.argv[1:] != ['--prepare']:
        print('Inert default; explicit --prepare required.')
        return
    need(pin(S/'SOURCE_READY_SEAL.json')['SHA256']=='24e7b08bda1c3561d9db2040745b2b1b8eb5b2e1f8c37be60426e831511cfb11','source seal anchor')
    seal=json.loads((S/'SOURCE_READY_SEAL.json').read_bytes())
    ready=json.loads((S/'SOURCE_READY.json').read_bytes())
    for name,key in [('SOURCE_READY.json','SOURCE_READY_SHA256'),('SOURCE_READY_MANIFEST.json','MANIFEST_SHA256'),('SOURCE_READY_CLOSURE.json','CLOSURE_SHA256')]:
        need(pin(S/name)['SHA256']==seal[key],'source terminal binding')
    files,dirs=[],[]
    for base,names,leaves in os.walk(S,followlinks=False):
        for name in names+leaves:
            path=Path(base)/name
            need(not path.is_symlink(),'source symlink')
            if path.is_dir():dirs.append(path.relative_to(S).as_posix())
            else:
                need(stat.S_ISREG(path.stat().st_mode),'source special file')
                files.append(pin(path))
    files.sort(key=lambda r:r['path']);dirs.sort()
    need(len(files)==108 and len(dirs)==14,'full source108files14dirs')
    manifest=json.loads((S/'SOURCE_READY_MANIFEST.json').read_bytes())
    need(len(manifest['files'])==105,'105payload+3exactterminals')
    for row in manifest['files']:
        actual=pin(S/row['path'])
        need(actual['bytes']==row['bytes'] and actual['SHA256']==row['SHA256'],'source payload')
    put('SOURCE_INPUT_MANIFEST.json',{'UTC':utc(),'source_root':str(S),'complete_source_files':files,'exact_complete_source_directories':dirs,
        'source_payload_count':105,'source_complete_files_including_three_exact_terminals':108,'source_exact_terminals':seal['exact_root_terminal_files'],
        'root143_gate':'CLOSED','prior_record143_scientific_body_or_opinion_read':False})
    contract=P/'verification/supported-cycle-focal-independent-code-audit-sol-20261115/ACTUAL623_QUALIFIED_CORE.json'
    need(pin(contract)['SHA256']=='0f285e35daa206f53aa931946c4bcc6c5b01ae6b4b59a231a861b0a6fe11d104','neutral qualified core anchor')
    core=json.loads(contract.read_bytes());actuals=[]
    for row in core['files']:
        actual=pin(Path(row['path']))
        need(actual['bytes']==row['bytes'] and actual['SHA256']==row['SHA256'],'qualified core byreference pin')
        actuals.append(actual)
    need(len(actuals)==18,'17original plus sole405b')
    put('CORE_BINDINGS.json',{'UTC':utc(),'whole_root_contract_binding':pin(contract),'whole_original_root_contract':core,
        'actual_byreference_core_files':actuals,'qualification':'17 original source files plus sole authorized405b checkpoint, not18 original unchanged',
        'generated_caches_opaque_no_immutability_claim':True,'actual_core_programmes_read_or_executed':[]})
    pdf=Path(ready['selected_actual_PDF']['path']);tex=Path(ready['controlling_TeX']['extracted_path'])
    need(pin(pdf)['SHA256']=='a84cfe9347d3d0ce05ef0fb22e8648ee64fd77992825729d24991cf0fc1d627d','actual PDF')
    need(pin(tex)['SHA256']=='317ab083bdfc4e986921e517b368de8e1501c7f9a24b4faef5b047fe1d504f43' and len(tex.read_bytes().splitlines())==192,'actual192line sole TeX')
    need(ready['additional_controlling_TeX_sources']==[],'additional manuscript coverage')
    (A/'rasters').mkdir(exist_ok=False)
    commands=[['pdfinfo',str(pdf)],['pdftotext','-layout',str(pdf),str(A/'published-pdf-text.txt')]]
    commands += [['pdftoppm','-f',str(i),'-l',str(i),'-r','120','-png','-singlefile',str(pdf),str(A/'rasters'/('page-'+str(i)))] for i in range(1,4)]
    receipts=[]
    for argv in commands:
        start=utc();r=subprocess.run(argv,capture_output=True)
        receipts.append({'started_UTC':start,'completed_UTC':utc(),'argv':argv,'exit':r.returncode,'stdout':r.stdout.decode('utf-8'),'stderr':r.stderr.decode('utf-8')})
        need(r.returncode==0,'document derivative failure; stop')
    put('MANUSCRIPT_DERIVATION_RECEIPTS.json',{'UTC':utc(),'actual_PDF':pin(pdf),'actual_TeX':pin(tex),'commands':receipts,
        'fresh_own_rasters':[pin(A/'rasters'/('page-'+str(i)+'.png')) for i in range(1,4)],'native_or_scientific_programmes_executed':[]})
    print(json.dumps({'source_files':108,'source_directories':14,'PDF_pages':3,'TeX_lines':192,'fresh_own_rasters':3,'qualified_original_core_files':17,'sole_authorized405b':True,'scientific_execution':False,'root143_gate':'CLOSED'}))

if __name__=='__main__':
    main()
