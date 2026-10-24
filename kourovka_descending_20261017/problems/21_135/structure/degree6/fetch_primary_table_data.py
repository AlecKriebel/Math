#!/usr/bin/env python3
"""Recover precisely the hashed primary ordinary table files used by the checks."""
from pathlib import Path
import hashlib,io,json,tarfile,urllib.request
root=Path(__file__).resolve().parent
manifest=json.loads((root/'sources'/'manifest.json').read_text())
archive=next(x for x in manifest['sources'] if x['file']=='ctbllib-1.3.11.tar.gz')
body=urllib.request.urlopen(archive['url'],timeout=60).read()
assert hashlib.sha256(body).hexdigest()==archive['sha256'],'primary archive hash changed'
wanted={x['file']:x for x in manifest['sources'] if x.get('archive_member') and (x['file'].endswith('.tbl') or x['file']=='construc.gi')}
with tarfile.open(fileobj=io.BytesIO(body),mode='r:gz') as tar:
    for name,row in wanted.items():
        data=tar.extractfile(row['archive_member']).read()
        assert hashlib.sha256(data).hexdigest()==row['sha256'],name
        (root/'sources'/name).write_bytes(data)
print(json.dumps({'archive_sha256_verified':True,'primary_files_recovered':len(wanted)},sort_keys=True))
