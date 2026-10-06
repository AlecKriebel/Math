#!/usr/bin/python3
"""Unexecuted separate ROOT readback; does not execute a mathematical checker."""
import hashlib,json,os,sys
sys.dont_write_bytecode=True
import packet_common as c
assert sys.argv[1:]==['--root-only-read-after-close']
m=c.check_closed();p=c.ROOT/'SELF_MANIFEST.json'
print(json.dumps({'status':'PASS_ACTUAL_ROOT_GKZ_FAN_CLOSED_READBACK','actual_reader_pid':os.getpid(),'original_actual_closer_pid':m['actual_closer_pid'],'manifest_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'file_count_including_manifest':len(m['files'])+1,'acceptance_authority':False},sort_keys=True))
