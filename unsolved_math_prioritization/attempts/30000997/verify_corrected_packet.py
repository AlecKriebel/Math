#!/usr/bin/env python3
"""Read-only integrity check for the appended MTW correction packet.
Uses only the Python standard library. No proof search or file modification.
"""
import hashlib,json,pathlib
P=pathlib.Path(__file__).resolve().parent
m=json.loads((P/'CORRECTED_PACKET_MANIFEST.json').read_text())
def check(path,want):
 b=(P/path).read_bytes()
 assert len(b)==want['bytes'],('bytes',path)
 assert hashlib.sha256(b).hexdigest()==want['sha256'],('sha256',path)
 return True
old=json.loads((P/'FINAL_AUTHOR_MANIFEST.json').read_text())
for n,v in old['files'].items():check(n,v)
for n,v in m['append_only_files'].items():check(n,v)
check('FINAL_AUTHOR_MANIFEST.json',m['frozen_author_manifest'])
audit=P/'audit/initial';am=json.loads((audit/'REVIEW_MANIFEST.json').read_text())
assert hashlib.sha256((audit/'REVIEW_MANIFEST.json').read_bytes()).hexdigest()==m['full_audit_manifest_sha256']
for n,v in am['files'].items():check('audit/initial/'+n,v)
state=json.loads((P/'CURRENT_STATE.json').read_text())
assert state['author_turns']==state['maximum_author_turns']==5
assert state['status']=='exhausted' and state['global_target_resolved'] is False
assert state['current_entrypoint']=='CURRENT.md'
sp=json.loads((P/'STATE_PROVENANCE.json').read_text())
for key in ['local_historical','remote_historical']:
 v=sp[key];check(v['path'],v)
assert sp['local_historical']['sha256']!=sp['remote_historical']['sha256']
actual=hashlib.sha256((P/'TURN_STATE.json').read_bytes()).hexdigest()
assert actual in {sp['local_historical']['sha256'],sp['remote_historical']['sha256']}
print(json.dumps({'status':'PASS','frozen_author_files_unchanged':len(old['files']),'append_only_files_verified':len(m['append_only_files']),'full_audit_manifest_verified':True,'historical_states_preserved_and_distinct':True,'operational_state_is_recognized_historical_variant':True,'author_turns':5,'global_target_resolved':False,'scope':'Integrity and status checks only; not a new mathematical proof or the narrow re-review.'},indent=2))
