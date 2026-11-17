"""Freeze the exact finite continuation; preserve original and INITIAL guards."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat
import subprocess

LANE=Path(__file__).resolve().parent
TERMINALS=['MANIFEST.json','FINAL.json']

def record(path):
    st=path.lstat()
    e={'path':str(path.relative_to(LANE)) if path!=LANE else '.',
       'mode_octal':oct(stat.S_IMODE(st.st_mode))}
    if stat.S_ISDIR(st.st_mode):e.update(kind='directory',empty=not any(path.iterdir()))
    elif stat.S_ISREG(st.st_mode):
        data=path.read_bytes();e.update(kind='file',bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    else:raise ValueError(str(path))
    return e

assert not any((LANE/name).exists() for name in TERMINALS)
guard=subprocess.run(['python3',str(LANE/'guard_sources.py'),'final'],capture_output=True)
assert guard.returncode==0,guard.stderr.decode()
result=json.loads((LANE/'RESULT.json').read_text())
assert result['native_reproduction']['ordinary_unmodified_native_routes_attempted']==1
assert result['follow_up'] is None
stamp=datetime.now(timezone.utc).isoformat()
with (LANE/'RESEARCH_LOG.md').open('a') as log:
    log.write(f'\nActual finite closure at {stamp}. Final source97 and INITIAL17 guards '
              'match every byte, mode, and topology entry. Bounded review 100%. '
              'All continuation payload files made read-only and child directories '
              'read-only; exact terminal exclusions are MANIFEST.json and FINAL.json. '
              'Quiescent after this closure.\n')
for path in LANE.rglob('*'):
    if path.is_file():os.chmod(path,0o444)
for path in sorted(LANE.rglob('*'),reverse=True):
    if path.is_dir():os.chmod(path,0o555)
payload=[record(p) for p in [LANE,*sorted(LANE.rglob('*'))]]
manifest={'schema':'finite-whole-continuation-manifest-v1','utc':stamp,'root':str(LANE),
          'scope':'Every actual payload object including root, hidden/ignored files, all empty directories, byte lengths, hashes and modes; no implicit exclusions',
          'exact_terminal_exclusions':[{'path':name,'kind':'file','reason':'Terminal control; FINAL pins MANIFEST and external root message pins FINAL'} for name in TERMINALS],
          'entries':payload,'payload_files':sum(e['kind']=='file' for e in payload),
          'child_directories':sum(e['kind']=='directory' and e['path']!='.' for e in payload),
          'payload_bytes':sum(e.get('bytes',0) for e in payload)}
mpath=LANE/TERMINALS[0]
mpath.write_text(json.dumps(manifest,indent=2)+'\n');os.chmod(mpath,0o444)
final={'schema':'finite-whole-continuation-final-v1','utc':stamp,'root':str(LANE),
       'record_id':23203270,'inventory_row':188,'lane':'scope-sol-continuation-20261117',
       'status':'COMPLETE_FROZEN_QUIESCENT_AWAIT_ROOT_GATE_AND_ADOPTION',
       'scientific_result':'RESULT.json','manifest':record(mpath),
       'exact_terminal_exclusions':TERMINALS,
       'own_self_pin':'External root message supplies actual bytes, mode and SHA256; no circular self-hash',
       'payload_files':manifest['payload_files'],'whole_files':manifest['payload_files']+2,
       'whole_child_directories':manifest['child_directories'],
       'original_source_namespace':{'files':97,'child_directories':12,'unchanged':True},
       'frozen_INITIAL_namespace':{'files':17,'child_directories':1,'unchanged':True,
          'manifest_sha256':'ccc2d42694ab76d834624bb9a60edeeb79a6060a330a3f141e98a109a6d8fc19',
          'seal_sha256':'658f4d17a204ab3ba16d960dbe00ac397d99cc5d555ce2ba4187f657f0bb9631'},
       'guards':{'before':record(LANE/'INPUT_GUARD_BEFORE.json'),'final':record(LANE/'INPUT_GUARD_FINAL.json')},
       'completion_percent_of_bounded_review':100,'native_routes':1,
       'follow_up':None,'further_work_authorized_now':False,
       'scientific_mechanisms_or_verdicts_sent_to_root_before_root_gate':False,
       'publication_disposition_authority':'root only'}
fpath=LANE/TERMINALS[1]
fpath.write_text(json.dumps(final,indent=2)+'\n');os.chmod(fpath,0o444)
actual=[record(p) for p in [LANE,*sorted(LANE.rglob('*'))]]
assert [e for e in actual if e['path'] not in TERMINALS]==payload
assert sum(e['kind']=='file' for e in actual)==final['whole_files']
assert len(actual)==len(payload)+2
print(json.dumps({'manifest':record(mpath),'final':record(fpath),'whole_files':final['whole_files'],
                  'child_directories':final['whole_child_directories'],'status':final['status']},indent=2))
