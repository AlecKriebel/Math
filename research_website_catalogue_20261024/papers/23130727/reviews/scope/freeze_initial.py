#!/usr/bin/env python3
"""Explicit immutable initial metadata freeze; no scientific execution."""
from pathlib import Path
import datetime
import hashlib
import json
import sys

A = Path(__file__).resolve().parent

def pin(path):
    body = path.read_bytes()
    return {'path':str(path),'bytes':len(body),'SHA256':hashlib.sha256(body).hexdigest()}

def main():
    if sys.argv[1:] != ['--freeze']:
        print('Inert default; --freeze required for new initial metadata controls.')
        return
    for name in ['INITIAL_MANIFEST.json','INITIAL_SEAL.json']:
        if (A/name).exists():
            raise ValueError('refuse initial overwrite')
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    rows = [pin(p) for p in sorted(A.rglob('*')) if p.is_file()]
    dirs = sorted(p.relative_to(A).as_posix() for p in A.rglob('*') if p.is_dir())
    manifest = {'schema':'row141-paper-first-initial-manifest-v1','UTC':now,'files':rows,
                'complete_directories_at_initial':dirs,'no_initial_payload_overwrite_authorized':True}
    (A/'INITIAL_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    seal = {'schema':'row141-paper-first-initial-seal-v1','UTC':now,'record_id':23130727,'sheet_row':141,
            'status':'SUBSTANTIVE_INDEPENDENT_PAPER_FIRST_INITIAL_FROZEN',
            'manifest':pin(A/'INITIAL_MANIFEST.json'),'substantive_reconstruction':pin(A/'INITIAL_DERIVATIONS.md'),
            'read_ledger':pin(A/'INITIAL_READ_LEDGER.json'),'complete_PDF_pages':3,'complete_TeX_lines':229,
            'fresh_own_rasters_viewed':3,'materially_distinct_reconstruction_families':12,
            'supplied_code_results_archive_foreign_or_current_opinion_exposure':False,
            'scientific_programmes_executed':[],'primary_GETs':0,'completion_percent':20,
            'root141_gate':'CLOSED','scientific_findings_sent_to_root':False,
            'not_final_disposition':True,'followup':None,'publication_authority':False}
    (A/'INITIAL_SEAL.json').write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(pin(A/'INITIAL_SEAL.json')))

if __name__ == '__main__':
    main()
