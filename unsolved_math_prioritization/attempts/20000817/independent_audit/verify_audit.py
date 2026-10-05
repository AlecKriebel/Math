#!/usr/bin/env python3
"""Portable audit replay, with optional checks of the preserved author packet."""
import argparse,hashlib,json,subprocess,sys,zipfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--author-dir',type=Path);p.add_argument('--author-zip',type=Path);args=p.parse_args()
b=Path(__file__).resolve().parent
manifest=json.loads((b/'MANIFEST.json').read_text())
actual_files={q.relative_to(b).as_posix() for q in b.rglob('*') if q.is_file() and '__pycache__' not in q.parts}
expected_files={row['path'] for row in manifest['files']}|{'MANIFEST.json','AUDIT_REPLAY.json'}
assert actual_files==expected_files,(actual_files-expected_files,expected_files-actual_files)
for row in manifest['files']:
 data=(b/row['path']).read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],row['path']
observed=json.loads(subprocess.check_output([sys.executable,str(b/'code/independent_controls.py')],text=True))
expected=json.loads((b/'results/independent_controls.json').read_text());assert observed==expected
receipt={'status':'PASS','manifest_files_verified':len(manifest['files']),'independent_control_replay':'exact match','general_problem_solved':False,'author_checks_requested':bool(args.author_dir or args.author_zip)}
integrity=json.loads((b/'results/input_integrity.json').read_text())
if args.author_zip:
 data=args.author_zip.read_bytes();exp=integrity['author_archive'];assert len(data)==exp['bytes'] and hashlib.sha256(data).hexdigest()==exp['sha256'];receipt['author_archive']='exact frozen bytes'
 with zipfile.ZipFile(args.author_zip) as z:
  assert len([n for n in z.namelist() if not n.endswith('/')])==len(integrity['author_files'])
  for row in integrity['author_files']:
   matches=[n for n in z.namelist() if n==row['path'] or n.endswith('/'+row['path'])];assert len(matches)==1
   data=z.read(matches[0]);assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
if args.author_dir:
 for row in integrity['author_files']:
  data=(args.author_dir/row['path']).read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
 author=json.loads((args.author_dir/'results/verification.json').read_text())
 for ours,theirs in zip(observed['enumeration'],author['enumeration']):
  assert ours['counts_d0_to_d8']==theirs['lower_set_counts_lengths_0_to_8'];assert ours['signature_total']==theirs['nonsmoothable_component_signature']
 assert observed['flat_models_total']==author['flat_models_checked']
 assert observed['h143_tangent_histogram_Q']==author['all_120_h143_tangent_dimensions']
 assert observed['collision_border_tangent']['tangent_dimension_Q']==author['collision_tangent']['dimension']
 assert observed['anchor_border_tangent']['tangent_dimension_Q']==author['anchor_tangent']['dimension']
 for d,h in author['projective_separating_ideal_hilbert_values'].items():assert observed['projective_hilbert_series']['hilbert_values_degrees_0_to_32'][d]==h
 receipt['author_files_and_control_comparison']='exact match'
print(json.dumps(receipt,sort_keys=True))
