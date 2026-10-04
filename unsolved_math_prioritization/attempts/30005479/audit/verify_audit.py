#!/usr/bin/env python3
"""Verify portable audit files and optional frozen author inputs.
Usage: python3 verify_audit.py [--author ../author] [--archive path.tar.gz]
"""
import argparse,hashlib,json,pathlib,tarfile
p=argparse.ArgumentParser();p.add_argument('--author');p.add_argument('--archive');args=p.parse_args()
root=pathlib.Path(__file__).resolve().parent
manifest=json.loads((root/'AUDIT_MANIFEST.json').read_text())
def check(path,meta):
    raw=path.read_bytes()
    assert len(raw)==meta['bytes'],str(path)
    assert hashlib.sha256(raw).hexdigest()==meta['sha256'],str(path)
for name,meta in manifest['files'].items():check(root/name,meta)
if args.author:
    author=pathlib.Path(args.author)
    check(author/'SHA256SUMS.json',manifest['bound_author_manifest'])
    m=json.loads((author/'SHA256SUMS.json').read_text())
    for name,meta in m['files'].items():check(author/name,meta)
    assert {x.name for x in author.iterdir() if x.is_file()}==set(m['files'])|{'SHA256SUMS.json'}
if args.archive:
    archive=pathlib.Path(args.archive);check(archive,manifest['bound_author_archive'])
    if args.author:
        with tarfile.open(archive,'r:gz') as tar:
            members=[member for member in tar.getmembers() if member.isfile()]
            assert {member.name for member in members}=={'author/'+name for name in set(m['files'])|{'SHA256SUMS.json'}}
            for member in members:assert tar.extractfile(member).read()==(author/pathlib.Path(member.name).name).read_bytes()
print(json.dumps(dict(passed=True,audit_payload_files=len(manifest['files']),author_checked=bool(args.author),archive_checked=bool(args.archive)),sort_keys=True))
