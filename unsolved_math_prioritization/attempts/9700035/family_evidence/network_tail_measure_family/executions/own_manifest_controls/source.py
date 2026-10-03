#!/usr/bin/env python3
"""Real isolated guard executions; all fixture text is synthetic authored data."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

HERE=Path(__file__).resolve().parent
fixtures=HERE/'controls'/'strict_views';fixtures.mkdir(exist_ok=False)
guard=HERE/'check_manifest.py';records=[]
cases=['baseline','missing','extra','same_size_hash','nested_self_basename','nested_foreign_basename','foreign_hash','symlink','duplicate_path','false_size','unsafe_path']
for case in cases:
    root=fixtures/case;root.mkdir()
    (root/'foreign_primary').mkdir();(root/'payload.json').write_text('{"value":2}\n')
    (root/'foreign_primary/synthetic.txt').write_text('Synthetic authored foreign-inventory control fixture.\n')
    def pin(path):
        data=(root/path).read_bytes();return {'path':path,'size':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    manifest={'self_excluded':['FIRST_PARTY_MANIFEST.json'],'foreign_root':'foreign_primary','files':[pin('payload.json')],'foreign_files':[pin('foreign_primary/synthetic.txt')]}
    if case=='missing':(root/'payload.json').unlink()
    elif case=='extra':(root/'extra.txt').write_text('Unexpected authored file.\n')
    elif case=='same_size_hash':(root/'payload.json').write_text('{"value":3}\n')
    elif case=='nested_self_basename':
        (root/'nested').mkdir();(root/'nested/FIRST_PARTY_MANIFEST.json').write_text('{}\n')
    elif case=='nested_foreign_basename':
        (root/'nested/foreign_primary').mkdir(parents=True);(root/'nested/foreign_primary/extra.txt').write_text('Extra under deceptive basename.\n')
    elif case=='foreign_hash':(root/'foreign_primary/synthetic.txt').write_text('Corrupted foreign binding.\n')
    elif case=='symlink':(root/'alias').symlink_to('payload.json')
    elif case=='duplicate_path':manifest['files'].append(dict(manifest['files'][0]))
    elif case=='false_size':manifest['files'][0]['size']=False
    elif case=='unsafe_path':manifest['files'][0]['path']='../payload.json'
    (root/'FIRST_PARTY_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result=subprocess.run(['/usr/bin/python3',str(guard),str(root)],capture_output=True,timeout=30)
    # Retain complete executed source and actual streams for every isolated run.
    (root/'EXECUTED_GUARD_SOURCE.py').write_bytes(guard.read_bytes())
    (root/'ACTUAL.stdout').write_bytes(result.stdout);(root/'ACTUAL.stderr').write_bytes(result.stderr)
    row={'case':case,'argv':['/usr/bin/python3',str(guard),str(root)],'started_utc':started,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'actual_execution':True,'exit_code':result.returncode,'expected_exit':0 if case=='baseline' else 1,'source_sha256':hashlib.sha256(guard.read_bytes()).hexdigest(),
         'full_stdout':result.stdout.decode(),'full_stderr':result.stderr.decode(),'synthetic_authored_fixture_only':True}
    assert row['exit_code']==row['expected_exit']
    records.append(row)
    # Preserve the symlink's target as first-party evidence but remove that
    # intentional live test symlink before the final family's symlink-free seal.
    if case=='symlink':
        (root/'SYMLINK_TEST_RECORD.json').write_text(json.dumps({'path':'alias','target':'payload.json','existed_during_actual_guard':True},indent=2)+'\n')
        (root/'alias').unlink()
receipt={'status':'PASS_OWN_REAL_STRICT_GUARD_CONTROLS','cases':records,'baseline':1,'rejections':10,'fixtures_are_administrative_not_SIRSNs':True,'new_substantive_attempts':0,'audit_turns':0}
(HERE/'MANIFEST_CONTROL_RESULTS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
