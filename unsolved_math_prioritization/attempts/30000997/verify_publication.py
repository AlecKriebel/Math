#!/usr/bin/env python3
"""Read-only byte and status validation. This is not a mathematical proof."""
import hashlib,json,pathlib,subprocess,sys
P=pathlib.Path(__file__).resolve().parent
m=json.loads((P/'PUBLICATION_MANIFEST.json').read_text())
for name,v in m['files'].items():
 b=(P/name).read_bytes()
 assert len(b)==v['bytes'], ('bytes',name)
 assert hashlib.sha256(b).hexdigest()==v['sha256'], ('sha256',name)
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['git_blob'], ('git_blob',name)
subprocess.run([sys.executable,str(P/'verify_corrected_packet.py')],check=True)
r=json.loads((P/'audit/narrow/NARROW_REREVIEW_RECEIPT.json').read_text())
assert r['status']=='PASS' and r['reviewed_commit']==m['reviewed_corrected_commit']
for name,v in r['files'].items():
 b=(P/'audit/narrow'/name).read_bytes();assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256']
s=json.loads((P/'PUBLICATION_STATE.json').read_text())
assert s['status']=='unsolved' and s['author_turns']==s['maximum_author_turns']==5
assert s['global_target_resolved'] is False and s['narrow_rereview']=='PASS'
assert s['current_entrypoint']=='PUBLICATION.md'
print(json.dumps({'status':'PASS','public_manifest_entries':len(m['files']),'narrow_review':'PASS','reviewed_corrected_commit':m['reviewed_corrected_commit'],'queue_disposition':'unsolved 5/5','global_target_resolved':False,'scope':'Integrity and administrative status only'},indent=2))
