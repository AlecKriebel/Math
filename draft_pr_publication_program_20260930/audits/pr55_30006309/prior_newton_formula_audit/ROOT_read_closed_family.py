#!/usr/bin/python3
"""UNEXECUTED separate ROOT readback; never runs the science/source controls."""
import hashlib, json, os, sys
sys.dont_write_bytecode = True
import packet_common as c
assert sys.argv[1:] == ['--root-only-read-after-close']
manifest = c.check_closed(); path = c.ROOT/'SELF_MANIFEST.json'
print(json.dumps({'status':'PASS_ACTUAL_ROOT_ESTEROV_PRIORITY_CLOSED_READBACK',
                  'actual_reader_pid':os.getpid(), 'original_actual_closer_pid':manifest['actual_closer_pid'],
                  'manifest_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                  'file_count_including_manifest':len(manifest['files'])+1,
                  'acceptance_authority':False},sort_keys=True))
