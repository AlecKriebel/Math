#!/usr/bin/python3
"""UNEXECUTED ROOT-only closer, requiring the parent's prior personal reading."""
from datetime import datetime, timezone
import hashlib, json, os, sys
sys.dont_write_bytecode = True
import packet_common as c
assert sys.argv[1:] == ['--root-only-close-after-reading']
assert not (c.ROOT/'SELF_MANIFEST.json').exists()
index, ready = c.check_prepared()
paths = c.all_files()
for path in paths: c.contained(path)
for path in paths: os.chmod(path,0o444)
manifest = {'schema':'pr55-Esterov-priority-actual-root-closure/v1',
            'utc':datetime.now(timezone.utc).isoformat(), 'actual_closer_pid':os.getpid(),
            'prepared_payload_file_count':len(index['files']), 'files':[c.row(p) for p in paths],
            'directories':[{'path':str(p),'mode':format(p.stat().st_mode&0o7777,'04o')} for p in c.all_dirs()],
            'external_references':index['external_references'], 'acceptance_authority':False,
            'ROOT_personal_read_not_inferred_from_integrity':True,
            'ROOT_closure_assertion':'Caller must personally read the derivation, limits, code and full actual captures before this ROOT-only action.',
            'historical_prepared_modes':'Owned files alone are frozen0444; historical capture source modes0644 remain dated facts.',
            'source_integrity_checks_before_closure':c.checks}
path = c.ROOT/'SELF_MANIFEST.json'; path.write_text(json.dumps(manifest,indent=2)+'\n'); os.chmod(path,0o444)
c.check_closed()
print(json.dumps({'status':'PASS_ACTUAL_ROOT_ESTEROV_PRIORITY_CLOSURE', 'actual_closer_pid':os.getpid(),
                  'manifest_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                  'file_count_including_manifest':len(paths)+1,
                  'ROOT_personal_read_not_inferred':True, 'acceptance_authority':False},sort_keys=True))
