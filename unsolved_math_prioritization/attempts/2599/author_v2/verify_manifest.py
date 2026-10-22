#!/usr/bin/env python3
"""Validate only the frozen safe publication allowlist, rejecting symlinks."""
import hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
m=json.loads((ROOT/'AUTHOR_MANIFEST.json').read_text())
for entry in m['files']:
 p=ROOT/entry['name']
 assert p.parent==ROOT and not p.is_symlink() and p.is_file()
 b=p.read_bytes()
 assert len(b)==entry['bytes'],entry['name']
 assert hashlib.sha256(b).hexdigest()==entry['sha256'],entry['name']
assert {x.name for x in ROOT.iterdir() if x.is_file()}=={'AUTHOR_MANIFEST.json'}|{x['name']for x in m['files']}
print(json.dumps({'verified_files':len(m['files']),'status':'PASS','publication_scope':'manifest-listed authored files and public metadata only'}))
