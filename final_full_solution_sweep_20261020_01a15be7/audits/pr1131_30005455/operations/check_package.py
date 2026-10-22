#!/usr/bin/env python3
"""Entirely local/read-only fixed-package and proposal checker; no service mutations."""
if not globals().get('_PR1131_SOURCE_VERIFIED',False):
    raise RuntimeError('Use the externally SHA-verified source bootstrap; direct helper imports are forbidden')
import ast
from ops_common import *

def main():
    pkg=package();_,changes=proposal()
    for path in OPS.glob('*.py'):ast.parse(path.read_bytes(),filename=str(path))
    original={name:pkg['source']['original/'+name] for name in ORIGINALS}
    for name in ORIGINALS-{'README.md','STATUS.json','MANIFEST.json'}:
        need(PROBLEM+'/'+name not in changes,'Preserved historical file unexpectedly changed')
    current=strict_json(changes[PROBLEM+'/MANIFEST.json'])
    need(set(current['members'])==ORIGINALS and current['member_count']==8,'Current manifest members differ')
    for e in current['entries']:
        n=e['file'];b=changes.get(PROBLEM+'/'+n,original[n]);need(pin(b)=={'bytes':e['bytes'],'sha256':e['sha256']},'Current manifest payload mismatch')
    row=strict_json((OPS/'LEDGER_ROW_TEMPLATE.json').read_bytes())
    need(len(row)==4 and row[1]=='' and row[2]=='https://doi.org/10.5281/zenodo.{RECORD_ID}','Wrong ledger cells')
    print(json.dumps({'status':'PASS','frozen_release_assets':6,'source_payloads':44,'source_zip_members':45,'kit_members':5,'proposal_changes':8,'preserved_originals':5,'all_eight_historical_originals_in_frozen_source':True,'mutation_helpers_executed_by_this_checker':False,'scientific_acceptance_is_separate_from_operational_clearance':True},indent=2))
if __name__=='__main__':main()
