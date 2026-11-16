#!/usr/bin/env python3
"""Explicit paper-first initial metadata seal; inert default, no science."""
from pathlib import Path
import datetime
import hashlib
import json
import sys

A=Path(__file__).resolve().parent

def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}

def main():
    if sys.argv[1:]!=['--freeze']:
        print('Inert default; explicit --freeze required.')
        return
    if any((A/n).exists() for n in ['INITIAL_MANIFEST.json','INITIAL_SEAL.json']):
        raise ValueError('refuse initial overwrite')
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    files=sorted([pin(p) for p in A.rglob('*') if p.is_file()],key=lambda r:r['path'])
    dirs=sorted(p.relative_to(A).as_posix() for p in A.rglob('*') if p.is_dir())
    (A/'INITIAL_MANIFEST.json').write_text(json.dumps({'schema':'row143-paper-first-initial-manifest-v1','UTC':now,'files':files,'complete_directories_at_initial':dirs,'no_initial_payload_overwrite_authorized':True},ensure_ascii=False,indent=2)+'\n')
    obj={'schema':'row143-paper-first-initial-seal-v1','UTC':now,'record_id':22982894,'sheet_row':143,
        'status':'SUBSTANTIVE_INDEPENDENT_PAPER_FIRST_INITIAL_FROZEN','manifest':pin(A/'INITIAL_MANIFEST.json'),
        'substantive_reconstruction':pin(A/'INITIAL_DERIVATIONS.md'),'read_ledger':pin(A/'INITIAL_READ_LEDGER.json'),
        'complete_PDF_pages':3,'complete_TeX_lines':192,'fresh_own_rasters_viewed':3,'materially_distinct_mechanism_falsifier_families':12,
        'supplied_scientific_README_support_code_results_archive_foreign_current_opinion_exposure':False,
        'scientific_programmes_executed':[],'primary_GETs':0,'completion_percent':20,'root143_gate':'CLOSED',
        'scientific_findings_sent_to_root':False,'not_final_disposition':True,'followup':None,'publication_authority':False}
    (A/'INITIAL_SEAL.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(pin(A/'INITIAL_SEAL.json')))

if __name__=='__main__':
    main()
