#!/usr/bin/env python3
"""ROOT-only absent-first closure of this bounded source/review family.
No production code is imported; external inputs are read-only. Unexecuted by author.
"""
from pathlib import Path
import datetime, hashlib, json, stat
base=Path(__file__).absolute().parent
destination=base/'MANIFEST.json'
if destination.exists(): raise SystemExit('Refusing to replace existing closure')
sha=lambda b:hashlib.sha256(b).hexdigest()
ready=json.loads((base/'READY.json').read_bytes())
assert ready['status']=='SOURCE_AND_REVIEW_READY_FOR_ROOT_CLOSURE'
verdict=json.loads((base/'VERDICT.json').read_bytes())
assert verdict['mandatory_corrections']==[] and verdict['remaining_gap_within_stated_theorem'] is None
readback=json.loads((base/'COMPLETE_READBACK.json').read_bytes())
for row in readback['external_inputs']:
    p=Path(row['path']);st=p.lstat();assert stat.S_ISREG(st.st_mode) and not p.is_symlink()
    b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256']
# Recorded external modes are dated observations, not a claim that external chmod is impossible.
for folder in sorted(base.glob('*_actual')):
    if not folder.is_dir(): continue
    cap=json.loads((folder/'CAPTURE.json').read_bytes())
    assert cap['exit_code']==0 and type(cap['child_pid']) is int and cap['child_pid']>0
    for stream in ('stdout','stderr'):
        b=(folder/(stream+'.bin')).read_bytes()
        assert {'bytes':len(b),'sha256':sha(b)}==cap[stream]
    assert not (folder/'stderr.bin').read_bytes()
    for row in cap['source_pins']:
        b=Path(row['path']).read_bytes()
        assert b==(folder/row['copy']).read_bytes() and len(b)==row['bytes'] and sha(b)==row['sha256']
files=[];directories=[]
for p in sorted(base.rglob('*')):
    assert not p.is_symlink()
    st=p.lstat()
    if stat.S_ISDIR(st.st_mode): directories.append(p.relative_to(base).as_posix())
    else:
        assert stat.S_ISREG(st.st_mode)
        b=p.read_bytes();files.append({'path':p.relative_to(base).as_posix(),'bytes':len(b),'sha256':sha(b),'mode':0o444})
assert len(files)==ready['payload_count_before_manifest']
record={'schema':'pr50-final-submission-adversary-manifest/v1',
        'role':'bounded completed review/source closure; not production or publication approval',
        'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'payload_count':len(files),'payload':files,'directories':directories,
        'external_inputs_reference':'COMPLETE_READBACK.json','external_modes_are_dated_observations':True,
        'reviewer_did_not_execute_this_closer':True,'root_mathematical_or_publication_approval_conferred':False}
body=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode()
with destination.open('xb') as out: out.write(body)
for row in files: (base/row['path']).chmod(0o444)
destination.chmod(0o444)
for relative in sorted(directories,key=lambda x:len(Path(x).parts),reverse=True): (base/relative).chmod(0o555)
base.chmod(0o555)
for row in files:
    p=base/row['path'];b=p.read_bytes()
    assert len(b)==row['bytes'] and sha(b)==row['sha256'] and stat.S_IMODE(p.lstat().st_mode)==0o444
assert destination.read_bytes()==body
print(json.dumps({'status':'PASS_ROOT_SELF_ONLY_FINAL_REVIEW_CLOSURE','payload_count':len(files),
                  'manifest_sha256':sha(body),'new_native_or_publication_actions':False},indent=2))
