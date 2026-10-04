#!/usr/bin/env python3
"""Validate the audit manifest and optionally bind the external author archive."""
from pathlib import Path
import argparse,hashlib,json,zipfile

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--author-packet',type=Path)
    args=ap.parse_args()
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'AUDIT_MANIFEST.json').read_text())
    expected={e['path'] for e in manifest['files']}
    actual={p.name for p in root.iterdir() if p.is_file() and p.name!='AUDIT_MANIFEST.json'}
    assert actual==expected,('audit file set differs',actual ^ expected)
    for e in manifest['files']:
        p=root/e['path']; assert p.parent==root and not p.is_symlink()
        b=p.read_bytes(); assert len(b)==e['bytes'] and sha(b)==e['sha256'],e['path']
    bound=False
    if args.author_packet:
        binding=json.loads((root/'BINDING.json').read_text())['author_packet']
        b=args.author_packet.read_bytes()
        assert len(b)==binding['bytes'] and sha(b)==binding['sha256'],'author archive differs'
        with zipfile.ZipFile(args.author_packet) as z:
            assert sorted(z.namelist())==sorted(e['path'] for e in binding['members'])
            for e in binding['members']:
                b=z.read(e['path']); assert len(b)==e['bytes'] and sha(b)==e['sha256'],e['path']
        bound=True
    print(json.dumps({'status':'PASS','audit_files_verified':len(expected),'external_author_archive_verified':bound},sort_keys=True))
if __name__=='__main__':main()
