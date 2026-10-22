#!/usr/bin/env python3
"""Entirely local/read-only fixed-package and proposal checker; no service mutations."""
if not globals().get('_PR1131_SOURCE_VERIFIED',False):
    raise RuntimeError('Use the externally SHA-verified source bootstrap; direct helper imports are forbidden')
import argparse
import ast
from ops_common import *

def private_tree(root):
    need(root.is_dir() and not root.is_symlink(),'Private custody root absent/symlink')
    entries=[[root.relative_to(OPS).as_posix(),'directory']];files=0;size=0
    for path in sorted(root.rglob('*')):
        need(not path.is_symlink(),'Private custody symlink')
        name=path.relative_to(OPS).as_posix()
        if path.is_file():
            body=path.read_bytes();entries.append([name,'file',pin(body)]);files+=1;size+=len(body)
        elif path.is_dir():entries.append([name,'directory'])
        else:raise RuntimeError('Unexpected private custody file type')
    return {'files':files,'directories':len(entries)-files,'logical_bytes':size,'sorted_full_tree_sha256':sha(json.dumps(entries,ensure_ascii=False,separators=(',',':')).encode())}

def verify_preparation():
    validation=strict_json((OPS/'PREPARATION_VALIDATION.json').read_bytes())
    need(validation['schema_version']==3 and validation['publication_ready'] is False and validation['root_operational_gate_pending'] is True and validation['requires_new_independent_adversary'] is True,'Preparation readiness boundary changed')
    actual={p.name:pin(p.read_bytes()) for p in OPS.glob('*.py')}
    actual.update(strict_json((OPS/'DEPENDENCY_PINS.json').read_bytes()))
    need(actual==validation['tested_executable_pins'],'Final executable/dependency bytes differ from all-mode tested source')
    need(len(validation['runs'])==3 and {r['mode'] for r in validation['runs']}=={0,1,2},'All three modes required')
    for run in validation['runs']:
        output=strict_json(read_pinned(safe(OPS,run['public_output']),run['public_output_pin']))
        need(output['mode']==run['mode'] and not output['failures'] and output['full_groups']==26 and output['focused_groups']==21 and output['attempted_external_calls']==0 and output['external_mutations']==0 and output['publication_ready'] is False,'Public complete mode controls failed')
        raw=strict_json(read_pinned(safe(OPS,run['private_output']),run['private_output_pin']))
        need(not raw['failures'] and len(raw['controls'])==26 and all(x['status']=='PASS' for x in raw['controls']) and not raw['blocked_external_attempts'] and raw['actual_external_mutations']==0 and raw['copied_inputs_unchanged'] is True,'Private full mode evidence failed')
        receipt=strict_json(read_pinned(safe(OPS,run['copy_receipt']),run['copy_receipt_pin']))
        need(raw['target_operations_sha256']==receipt['target_manifest']['sha256'] and raw['bootstrap_sha256']==receipt['bootstrap_sha256']==actual['bootstrap.py']['sha256'],'Raw result/copy/bootstrap source anchors disagree')
        for name,expected_pin in validation['tested_executable_pins'].items():
            relative=name if '/' in name else (OPS.relative_to(REPO)/name).as_posix()
            need(receipt['files'].get(relative)==expected_pin,'Final executable differs from exact replay input pin: '+name)
        mirror=Path(receipt['mirror']);need(PRIVATE in mirror.parents and not mirror.is_symlink(),'Copy receipt outside assigned private area')
        for name,expected in receipt['files'].items():read_pinned(safe(mirror,name),expected)
    custody=strict_json((OPS/'PRIVATE_REPLAY_CUSTODY.json').read_bytes())
    expected=custody['roots'];actual_roots={q.relative_to(OPS).as_posix() for q in PRIVATE.iterdir() if q.name.startswith('repair03_')}
    need(actual_roots==set(expected),'New repair03 private custody roots changed')
    for name,tree in expected.items():need(private_tree(safe(OPS,name))==tree,'Complete private custody changed: '+name)
    old=strict_json((OPS/'history/v2/OPERATIONS_MANIFEST.json').read_bytes())
    for name in ['INTEGRATION_PROPOSAL.json',*[n for n in old['files'] if n.startswith('proposed/')]]:read_pinned(safe(OPS,name),old['files'][name])
    return {'all_mode_full_groups':78,'focused_groups':63,'private_custody_roots':len(expected),'final_tested_executable_bytes_equal':True,'publication_ready':False,'root_operational_gate_pending':True}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify-preparation',action='store_true');args=parser.parse_args()
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
    if args.verify_preparation:print(json.dumps(verify_preparation(),indent=2))
    print(json.dumps({'status':'PASS','frozen_release_assets':6,'source_payloads':44,'source_zip_members':45,'kit_members':5,'proposal_changes':8,'preserved_originals':5,'all_eight_historical_originals_in_frozen_source':True,'mutation_helpers_executed_by_this_checker':False,'scientific_acceptance_is_separate_from_operational_clearance':True},indent=2))
if __name__=='__main__':main()
