#!/usr/bin/env python3
"""Explicit source-byte/core metadata authentication and fresh PDF derivatives.
No project/native/scientific imports or programme execution; default is inert.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import stat
import subprocess
import sys

A = Path(__file__).resolve().parent
P = A.parents[3]
S = A.parents[1] / 'sources'

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def need(condition, message):
    if not condition:
        raise ValueError(message)

def pin(path):
    body = path.read_bytes()
    return {'path': str(path), 'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest()}

def put(name, obj):
    path = A/name
    need(not path.exists(), 'refuse overwrite ' + name)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def main():
    if sys.argv[1:] != ['--prepare']:
        print('Inert default; explicit --prepare required for new local metadata derivatives.')
        return
    ready = json.loads((S/'SOURCE_READY.json').read_bytes())
    seal = json.loads((S/'SOURCE_READY_SEAL.json').read_bytes())
    need(pin(S/'SOURCE_READY_SEAL.json')['SHA256'] == '7327ed767e15386ae633b54ea6ba90152d87de7addbbf44136212af2b5ff5d36', 'source SEAL anchor')
    for name, field in [('SOURCE_READY.json','SOURCE_READY_SHA256'),('SOURCE_READY_MANIFEST.json','MANIFEST_SHA256'),('SOURCE_READY_CLOSURE.json','CLOSURE_SHA256')]:
        need(pin(S/name)['SHA256'] == seal[field], 'whole source terminal binding')
    manifest = json.loads((S/'SOURCE_READY_MANIFEST.json').read_bytes())
    files = []
    dirs = []
    for root, names, leaves in os.walk(S, followlinks=False):
        for name in names + leaves:
            path = Path(root)/name
            need(not path.is_symlink(), 'source symlink')
            if path.is_dir():
                dirs.append(path.relative_to(S).as_posix())
            else:
                need(stat.S_ISREG(path.stat().st_mode), 'source special file')
                files.append(pin(path))
    files.sort(key=lambda row:row['path'])
    dirs.sort()
    need(len(files) == 128 and len(dirs) == 18, 'actual source128files18dirs')
    listed = manifest['files']
    need(len(listed) == 125, 'source125payload+3terminals')
    for row in listed:
        actual = pin(S / row['path'])
        need(actual['bytes'] == row['bytes'] and actual['SHA256'] == row['SHA256'], 'source payload pin')
    put('SOURCE_INPUT_MANIFEST.json', {'UTC':now(),'source_root':str(S), 'complete_source_files':files,
        'exact_complete_source_directories':dirs,'source_payload_count':125,'source_complete_files_including_three_exact_terminals':128,
        'source_exact_terminals':seal['exact_root_terminal_files'],'source_old_printed_and_current_Sheet_nulls_unmodified':True,
        'root141_gate':'CLOSED','prior_record141_scientific_body_or_opinion_read':False})
    contract = P/'verification/supported-cycle-focal-independent-code-audit-sol-20261115/ACTUAL623_QUALIFIED_CORE.json'
    need(pin(contract)['SHA256'] == '0f285e35daa206f53aa931946c4bcc6c5b01ae6b4b59a231a861b0a6fe11d104', 'qualified core contract anchor')
    core = json.loads(contract.read_bytes())
    actual_core = []
    for row in core['files']:
        actual = pin(Path(row['path']))
        need(actual['bytes'] == row['bytes'] and actual['SHA256'] == row['SHA256'], 'actual qualified core source')
        actual_core.append(actual)
    need(len(actual_core) == 18, 'qualified17 plus sole405b')
    put('CORE_BINDINGS.json', {'UTC':now(),'whole_root_contract_binding':pin(contract),'whole_original_root_contract':core,
        'actual_byreference_core_files':actual_core,'qualification':'17 original files plus sole authorized405b checkpoint helper; not18 original unchanged',
        'generated_caches_opaque_no_immutability_claim':True,'actual_code_programmes_read_or_executed':[], 'no_duplicate_core_corpus_created':True})
    pdf = Path(ready['selected_actual_PDF']['path'])
    tex = Path(ready['controlling_TeX']['extracted_path'])
    need(pin(pdf)['SHA256'] == '3ee2635930d4d107ff80cde1dfb7f8c57752fa833d0d212ba15c4ef7d4cdd81d', 'actual original PDF')
    need(pin(tex)['SHA256'] == 'ccf85ea52eb1d2003b69344e23e5c4641f851b22155bc95cbe01775ca41b2cab' and len(tex.read_bytes().splitlines()) == 229, 'sole original229line TeX')
    need(ready['additional_controlling_TeX_sources'] == [], 'no unaccounted controlling source')
    raster = A/'rasters'
    raster.mkdir(exist_ok=False)
    receipts = []
    commands = [['pdfinfo',str(pdf)],['pdftotext','-layout',str(pdf),str(A/'published-pdf-text.txt')]]
    for page in range(1,4):
        commands.append(['pdftoppm','-f',str(page),'-l',str(page),'-r','120','-png','-singlefile',str(pdf),str(raster/('page-'+str(page)))])
    for argv in commands:
        start = now()
        process = subprocess.run(argv,capture_output=True)
        receipts.append({'started_UTC':start,'completed_UTC':now(),'argv':argv,'exit':process.returncode,
                         'stdout':process.stdout.decode('utf-8'),'stderr':process.stderr.decode('utf-8')})
        need(process.returncode == 0, 'document derivative failed; stop')
    put('MANUSCRIPT_DERIVATION_RECEIPTS.json', {'UTC':now(),'actual_original_PDF':pin(pdf),'actual_original_TeX':pin(tex),
        'commands':receipts,'fresh_rasters':[pin(raster/('page-'+str(i)+'.png')) for i in range(1,4)],
        'source_or_scientific_programmes_executed':[],'document_derivatives_only':True})
    print(json.dumps({'source_files':128,'source_directories':18,'PDF_pages':3,'TeX_lines':229,'fresh_own_rasters':3,
                      'qualified_original_core_files':17,'sole_authorized_checkpoint':1,'scientific_execution':False,'root141_gate':'CLOSED'}))

if __name__ == '__main__':
    main()
