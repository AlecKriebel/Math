#!/usr/bin/env python3
"""Seal public audit bytes; all third-party extracts/renderings remain private."""
import datetime,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()

def digest(p):
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

inputs=[]
for row in json.loads((HERE/'initial_input_manifest.json').read_text())['inputs']:
    inputs.append(dict(row))
original=json.loads((HERE/'original_input_manifest.json').read_text())
for row in original['files']:
    inputs.append({'path':str(Path(original['original_attempt'])/row['relative_to_original_attempt']),'bytes':row['bytes'],'sha256':row['sha256']})
effective=json.loads((HERE/'effective_candidate_inspection.json').read_text())
for row in effective['input_files']:
    inputs.append({k:v for k,v in row.items() if k in ('path','bytes','sha256')})
inputs.append(digest(Path(effective['root_actual_receipt_path'])))
unique={r['path']:r for r in inputs}
for row in unique.values():
    if digest(Path(row['path']))!=row:raise RuntimeError('pinned input bytes changed '+row['path'])
(HERE/'INPUT_MANIFEST.json').write_text(json.dumps({'sealed_utc':now,'head':'3526d46bf143b08e5055ffa7728c6278e9f958ea','files':list(unique.values()),'third_party_source_pdf_in_public_outputs':False},indent=2)+'\n')

journals=[]
for p in sorted((HERE/'journals').glob('*.json')):
    r=json.loads(p.read_text())
    for output in r['outputs'].values():
        q=HERE/output['relative_path'] if 'relative_path' in output else Path(output['path'])
        d=digest(q)
        if d['bytes']!=output['bytes'] or d['sha256']!=output['sha256']:raise RuntimeError('journal output hash mismatch')
    label=r['label']
    expected=1 if ('known_false' in label or 'corrupt_cost' in label) and (label.startswith('independent_') or 'repaired_' in label or '_normal_' in label) else 0
    if label.startswith('badproof_'):
        expected=0 if label=='badproof_original_optimized' else 1
    if r['returncode']!=expected:raise RuntimeError('unexpected actual status in '+label)
    journals.append({'label':label,'actual_returncode':r['returncode'],'expected_returncode':expected,'journal':str(p.relative_to(HERE)),'journal_bytes':p.stat().st_size,'journal_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
if len(journals)!=43:raise RuntimeError('unexpected journal count '+str(len(journals)))
(HERE/'JOURNAL_INDEX.json').write_text(json.dumps({'sealed_utc':now,'actual_subprocess_journals':len(journals),'all_statuses_expected':True,'records':journals,'not_presented_as_historical_journals':True},indent=2)+'\n')

files=[]
for p in sorted(HERE.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(HERE)
    if 'private' in rel.parts or '__pycache__' in rel.parts or rel.as_posix() in ('OUTPUT_MANIFEST.json','SHA256SUMS'):continue
    d=digest(p);d['path']=rel.as_posix();d['public']=True
    d['classification']='intentional_adversarial_fixture' if 'badproof_controls' in rel.parts else 'historical_exact_replay' if 'exact_replays' in rel.parts else 'suggested_guard_repair' if 'suggested_guard_repairs' in rel.parts else 'audit_artifact'
    files.append(d)
(HERE/'OUTPUT_MANIFEST.json').write_text(json.dumps({'sealed_utc':now,'files':files,'public_file_count':len(files),'excludes':['private/**','__pycache__/**','OUTPUT_MANIFEST.json (self)','SHA256SUMS (authenticates this manifest; no circular hash)'],'no_third_party_pdf_extract_or_render_in_public_list':True,'adversarial_fixture_success_flags_are_not_verification_evidence':True},indent=2)+'\n')
allfiles=files+[dict(digest(HERE/'OUTPUT_MANIFEST.json'),path='OUTPUT_MANIFEST.json')]
(HERE/'SHA256SUMS').write_text(''.join(f"{r['sha256']}  {r['path']}\n" for r in sorted(allfiles,key=lambda r:r['path'])))
print(json.dumps({'sealed_utc':now,'input_files':len(unique),'actual_subprocess_journals':len(journals),'public_outputs':len(files),'report':digest(HERE/'REPORT.md'),'verdict':digest(HERE/'VERDICT.json'),'output_manifest':digest(HERE/'OUTPUT_MANIFEST.json')},indent=2))
