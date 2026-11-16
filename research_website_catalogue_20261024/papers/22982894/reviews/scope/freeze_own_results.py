#!/usr/bin/env python3
"""Explicit metadata freeze of actual written/hand-worked results, default inert."""
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
    if any((A/n).exists() for n in ['OWN_PROOF_CONTROL_MANIFEST.json','OWN_PROOF_CONTROL_SEAL.json']):
        raise ValueError('refuse result overwrite')
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    names=['OWN_NORMALIZED_CURVE_PROOF_AND_CONTROLS.md','OWN_HANDWORKED_RESULTS.json','OWN_RESEARCH_LOG.md']
    manifest={'schema':'row143-own-proof-control-manifest-v1','UTC':now,'files':[pin(A/n) for n in names],
        'initial_seal':pin(A/'INITIAL_SEAL.json'),'no_foreign_or_supplied_scientific_exposure':True,'scientific_execution':[]}
    (A/'OWN_PROOF_CONTROL_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    seal={'schema':'row143-own-proof-control-seal-v1','UTC':now,'record_id':22982894,
        'status':'ACTUAL_UNIVERSAL_PROOF_AND_HANDWORKED_CONTROLS_FROZEN_BEFORE_FOREIGN_OR_SUPPLIED_SCIENCE',
        'manifest':pin(A/'OWN_PROOF_CONTROL_MANIFEST.json'),'initial_seal_SHA256':pin(A/'INITIAL_SEAL.json')['SHA256'],
        'scientific_programmes_executed':[],'scientific_README_support_code_results_archive_foreign_current_opinion_exposure':False,
        'primary_GETs':0,'completion_percent':35,'root143_gate':'CLOSED','scientific_findings_sent_to_root':False,
        'followup':None,'publication_authority':False}
    (A/'OWN_PROOF_CONTROL_SEAL.json').write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(pin(A/'OWN_PROOF_CONTROL_SEAL.json')))

if __name__=='__main__':
    main()
