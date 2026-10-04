#!/usr/bin/env python3
"""Create review inventories/seal in this subtree; not a read-only replay."""
import argparse, datetime, gzip, hashlib, json, pathlib

ap = argparse.ArgumentParser()
ap.add_argument('--seal', action='store_true')
args = ap.parse_args()
root = pathlib.Path(__file__).resolve().parent
sha = lambda data: hashlib.sha256(data).hexdigest()
excluded = {'PUBLIC_MANIFEST.json', 'FINAL_SEAL.json'}
private_prefixes = {'private_sources','private_inputs','private_mutations','__pycache__'}
private_exact = {'hayman_page61.txt','carleson_all_pages.txt'}
public, private = [], []
for p in sorted(root.rglob('*')):
    if not p.is_file():
        continue
    rel = str(p.relative_to(root))
    if rel in excluded:
        continue
    data = p.read_bytes()
    rec = {'path':rel,'bytes':len(data),'sha256':sha(data)}
    (private if p.relative_to(root).parts[0] in private_prefixes or rel in private_exact else public).append(rec)
captures = []
not_readonly = {'replay_driver','hayman_lingham_2018_fetch','carleson_1976_fetch',
                'hayman_lingham_2018_extract','carleson_1976_extract','hayman_lingham_2018_page61_extract',
                'hayman_lingham_2018_page61_render','carleson_1976_render'}
for p in sorted((root/'captures').glob('*.receipt.json')):
    rec = json.loads(p.read_text())
    captures.append({'label':rec['label'],'receipt':str(p.relative_to(root)),
                     'read_only_command':rec['label'] not in not_readonly,
                     'exit_code':rec['exit_code'],'start_utc':rec['start_utc'],'end_utc':rec['end_utc']})
integrity = json.loads(gzip.decompress((root/'captures/integrity_corrected.stdout.gz').read_bytes()))
snapshot_data = (root.parent/'snapshot_manifest.json').read_bytes()
snapshot = json.loads(snapshot_data)
manifest = {'schema':1,'family':'independent topology/path geometry',
            'head':snapshot['head'],'base':snapshot['base'],'snapshot_manifest_sha256':sha(snapshot_data),
            'scope19':integrity['scope19'],'public_scope':'all review files except this manifest and FINAL_SEAL; private paths precisely listed separately',
            'files':public,'private_inventory':private,'captures':captures,
            'private_absence_policy':'Every private path is permitted absent in public verification; --include-private requires all. Any present private object is hash-verified. Two full source text extracts retain exact baseline paths but are ignored and excluded from public files.',
            'source_extract_public_stdout':'All pdftotext/render stdout and stderr logical streams are empty; original extracted texts and source renders are private.',
            'program_execution_policy':'Candidate programs were fully read before the sealed mathematical assessment and execution. Replays are read-only; acquisition commands and replay_driver write only this review subtree and must not be blindly replayed.',
            'source_and_math_baseline_order':['BASELINE_SEAL.json','MATH_ASSESSMENT_SEAL.json','captures/author_replay.receipt.json'],
            'novel_theorems':0,'credited_harmonic_resolution_percent':100,'family_audit_workflow_percent':100}
(root/'PUBLIC_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
if not args.seal:
    (root/'PRESEAL_MANIFEST.json').write_bytes((root/'PUBLIC_MANIFEST.json').read_bytes())
else:
    pre = json.loads((root/'captures/closure_preseal.receipt.json').read_text())
    assert pre['exit_code'] == 0 and pre['stdout']['bytes'] == pre['stderr']['bytes'] == 0
    final = {'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'public_manifest_sha256':sha((root/'PUBLIC_MANIFEST.json').read_bytes()),
             'snapshot_manifest_sha256':sha(snapshot_data),
             'baseline_seal_sha256':sha((root/'BASELINE_SEAL.json').read_bytes()),
             'math_assessment_seal_sha256':sha((root/'MATH_ASSESSMENT_SEAL.json').read_bytes()),
             'preseal_receipt_sha256':sha((root/'captures/closure_preseal.receipt.json').read_bytes()),
             'frozen_head':snapshot['head'],'frozen_base':snapshot['base'],
             'public_files':len(public),'private_objects':len(private),'scope_objects':19,
             'verdict':'PASS credited already_solved 0/5; continuous/harmonic proof scope',
             'novel_theorems':0,'credited_resolution_percent':100,'family_audit_percent':100,
             'root_reexecution_and_integration_pending':True,
             'private_sources_excluded':True,'sealed_paths_unchanged':True,
             'final_validation_command':'python verify_review.py --include-private --replay (silent on success, read-only)',
             'known_corrections':'CORRECTIONS.md preserves initial full-read-group count typo and failed own queue-format assumptions; original seals/program/failure streams unchanged'}
    (root/'FINAL_SEAL.json').write_text(json.dumps(final,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'sealed_utc':final['sealed_utc'],'public_manifest_sha256':final['public_manifest_sha256'],
                      'final_seal_sha256':sha((root/'FINAL_SEAL.json').read_bytes()),'public_files':len(public),'private_objects':len(private)}))
