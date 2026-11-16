#!/usr/bin/env python3
"""Explicit metadata seal of actual hand-worked proof; default inert."""
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
        print('Inert default; --freeze required for new own-result controls.')
        return
    for name in ['OWN_PROOF_CONTROL_MANIFEST.json','OWN_PROOF_CONTROL_SEAL.json']:
        if (A/name).exists():
            raise ValueError('refuse result overwrite')
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    names = ['OWN_EUCLIDEAN_PROOF_AND_CONTROLS.md','OWN_HANDWORKED_RESULTS.json','OWN_RESEARCH_LOG.md']
    obj = {'schema':'row141-own-proof-control-manifest-v1','UTC':now,'files':[pin(A/n) for n in names],
           'initial_seal':pin(A/'INITIAL_SEAL.json'),'no_foreign_or_supplied_scientific_exposure':True,'scientific_execution':[]}
    (A/'OWN_PROOF_CONTROL_MANIFEST.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    seal = {'schema':'row141-own-proof-control-seal-v1','UTC':now,'record_id':23130727,
            'status':'ACTUAL_UNIVERSAL_PROOF_AND_HANDWORKED_CONTROLS_FROZEN_BEFORE_FOREIGN_OR_SUPPLIED_SCIENCE',
            'manifest':pin(A/'OWN_PROOF_CONTROL_MANIFEST.json'),'initial_seal_SHA256':pin(A/'INITIAL_SEAL.json')['SHA256'],
            'scientific_programmes_executed':[],'supplied_code_results_archive_or_foreign_exposure':False,'primary_GETs':0,
            'completion_percent':35,'root141_gate':'CLOSED','scientific_findings_sent_to_root':False,'followup':None,'publication_authority':False}
    (A/'OWN_PROOF_CONTROL_SEAL.json').write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(pin(A/'OWN_PROOF_CONTROL_SEAL.json')))

if __name__ == '__main__':
    main()
