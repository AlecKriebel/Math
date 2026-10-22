#!/usr/bin/env python3
"""Read-only binding check for the exact corrected release; standard library only.
Usage: python3 verify_binding.py /path/to/rank618-30003790-release-v2
"""
import difflib
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys

EXPECTED = {
 'RELEASE_MANIFEST.json':'ea2b9302812262a611e68745648dad936f796bd4fa9c03f32ae320e2767760fe',
 'public/RESULT.md':'a993c07d3765e53d89c4c6eb4bc4c0f768ddf7f7e8d2e9038d603e0308d4c02b',
 'CHANGE_LEDGER.md':'ea08db5eca5864ee3539953195a9de870a38188e58eb075ee3a5c6f4c47a6aa8',
 'AUTHOR_V1_TO_CORRECTED_V2.diff':'7a30cbe0c73dccab511e4f6d36df14ae07b210bf17a94e8b6d6c07fb1e9a398f',
 'history/public/MANIFEST.json':'a18df1c214a6ea7ed7aa14d8a038827f463a7c9ff4f069228e0eb68b247367d2',
 'history/public/RESULT.md':'0c63e1801d50434d217a8a66d16ea8bad27cac4867919f7532abc4819eb9dc16',
 'history/independent-audit/MANIFEST.json':'b7f66c7809bf22cda967274d6c8dc9d8bbd9ce8d5e0a969a23ad8b90a4df4d73',
 'history/auxiliary-independent-audit/MANIFEST.json':'5a00c1b073bd6fd57e65ba537d4125617feb43651825cb57dcd03372aa802226',
 'history/auxiliary-independent-audit/AUDIT.md':'954dedd9ec67d2819b211aa6cbb6f33cd578977175fb1478ede820aa3f4aab6f',
 'public/AUXILIARY_THEOREM.md':'072aba944c908baf44bb86d6c9a3d1c87444b5f779c53a14b4a9648d9595351c'}

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def tree(p): return {x.relative_to(p).as_posix():x for x in p.rglob('*') if x.is_file()}
def verify_manifest(base,name='MANIFEST.json'):
 m=json.loads((base/name).read_text()); listed=set()
 for row in m['files']:
  q=PurePosixPath(row['path'])
  assert not q.is_absolute() and '..' not in q.parts and '.' not in q.parts
  assert row['path'] not in listed
  listed.add(row['path']); p=base/row['path']
  assert p.is_file() and not p.is_symlink()
  assert len(p.read_bytes())==row['bytes'] and digest(p)==row['sha256']
 assert set(tree(base))==listed|{name}
 return len(listed)

def main():
 r=Path(sys.argv[1]).resolve()
 for p in r.rglob('*'):
  assert not p.is_symlink(),str(p)
  if p.is_file(): assert p.suffix in {'.md','.json','.py','.diff'}
 for path,value in EXPECTED.items(): assert digest(r/path)==value,path
 counts={}
 for path in ['history/public','history/independent-audit','history/auxiliary-independent-audit','public']:
  counts[path]=verify_manifest(r/path)
 counts['release']=verify_manifest(r,'RELEASE_MANIFEST.json')
 a,b=tree(r/'history/public'),tree(r/'public')
 lines=[]
 for p in sorted(set(a)|set(b)):
  before=a[p].read_text().splitlines(keepends=True) if p in a else []
  after=b[p].read_text().splitlines(keepends=True) if p in b else []
  lines.extend(difflib.unified_diff(before,after,fromfile='history/public/'+p,tofile='public/'+p))
 assert ''.join(lines)==(r/'AUTHOR_V1_TO_CORRECTED_V2.diff').read_text()
 original=json.loads((r/'history/public/turns.json').read_text())
 revised=json.loads((r/'public/turns.json').read_text())
 assert original['turns']==revised['turns'] and revised['turns_used']==5
 assert (r/'public/AUXILIARY_THEOREM.md').read_bytes()==(r/'history/independent-audit/AUXILIARY_CANDIDATE.md').read_bytes()
 state=json.loads((r/'CURRENT_STATUS.json').read_text())
 assert state['literal_bounded_model_consistency']=='established'
 assert state['dimension_efficiency_part_of_literal_source_question'] is False
 assert state['queue_disposition']=='unsolved' and state['original_model_coverage']=='not_established'
 # This pending field is immutable historical assembly state, superseded by this audit.
 assert state['release_binding_review']=='pending'
 assert state['publication_authorized'] is False and state['remote_writes'] is False
 completed=subprocess.run([sys.executable,str(r/'VERIFY_RELEASE.py')],check=True,capture_output=True)
 replay=json.loads(completed.stdout); assert replay['status']=='PASS'
 # All file hashes and the exact inventory must still hold after executing controls.
 verify_manifest(r,'RELEASE_MANIFEST.json')
 print(json.dumps({'status':'PASS','exact_release_manifest_sha256':EXPECTED['RELEASE_MANIFEST.json'],
  'distributed_files':len(tree(r)),'manifest_entry_counts':counts,
  'exact_diff_reconstructed':True,'accepted_theorem_byte_identical':True,
  'original_five_turn_entries_unchanged':True,'safe_relative_inventory':True,
  'all_three_control_outputs_byte_identical':replay['all_three_recorded_control_outputs_byte_identical'],
  'replayed_cases':{'author_guard':replay['author_guard_cases'],'first_audit_guard':replay['first_audit_guard_cases'],
   'auxiliary_fixed_guard':replay['auxiliary_fixed_guard_cases'],'auxiliary_adaptive_guard':replay['auxiliary_adaptive_guard_cases']},
  'release_unchanged_after_checks':True,'remote_writes':False},indent=2,sort_keys=True))

if __name__=='__main__': main()
