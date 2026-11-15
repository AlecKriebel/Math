#!/usr/bin/env python3
"""One-shot owned-packet manifest/seal. No imports or execution of science.
Writes only these two root terminals, refuses an existing terminal, and has
no recursive basename exclusions. Source/default custody is verified separately.
"""
from pathlib import Path
import datetime
import hashlib
import json

E=Path(__file__).resolve().parent
if (E/'MANIFEST.json').exists() or (E/'FINAL_SEAL.json').exists():
    raise ValueError('refuse to replace a final terminal')
def pin(p):
    b=p.read_bytes()
    return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
files={};dirs=[]
for p in sorted(E.rglob('*')):
    if p.is_symlink():raise ValueError('no symlinks in owned closure')
    if p.is_file():files[p.relative_to(E).as_posix()]=pin(p)
    elif p.is_dir():dirs.append(p.relative_to(E).as_posix())
    else:raise ValueError('nonregular owned entry')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest={'schema':'scope23205305-whole-owned-namespace-v1','UTC':now,
 'only_exact_root_terminal_exclusions':['FINAL_SEAL.json','MANIFEST.json'],
 'recursive_basename_exclusions':False,'payloads':files,'directories':dirs}
(E/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
verdict=json.loads((E/'CUSTOM_VERDICT.json').read_bytes())
seal={'schema':'scope23205305-independent-family-FINAL-v1','UTC':now,
 'record_id':23205305,'completion_percent_own_family_packet':100,'manifest':pin(E/'MANIFEST.json'),
 'payload_files':len(files),'complete_actual_files':len(files)+2,
 'complete_directories':len(dirs),'initial_seal':pin(E/'INITIAL_SEAL.json'),
 'source_namespace_files':126,'protected_paths':144,
 'core_qualification':'17original plus sole root-authorized405b checkpoint helper',
 'whole_literal_CUSTOM_VERDICT':verdict,
 'root_scientific_gate_at_seal':'CLOSED','only_neutral_or_raw_handoffs_sent':True,
 'followup':None,'canonical_AA_assignment_authority':False,
 'publication_authority':None,'full_programme_goal_completion_claimed':False}
(E/'FINAL_SEAL.json').write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'MANIFEST.json':pin(E/'MANIFEST.json'),
 'FINAL_SEAL.json':pin(E/'FINAL_SEAL.json'),
 'payloads':len(files),'actual_files':len(files)+2,'directories':len(dirs)},indent=2))
