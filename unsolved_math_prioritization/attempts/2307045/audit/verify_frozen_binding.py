#!/usr/bin/env python3
"""Verify an audited packet against an external immutable digest binding."""
from pathlib import Path
import argparse,hashlib,json

HERE=Path(__file__).resolve().parent

def verify(root,binding):
    root=Path(root)
    expected={item['path']:item for item in binding['audited_packet_files']}
    assert len(expected)==len(binding['audited_packet_files']),'duplicate binding paths'
    assert all(Path(name).name==name and name not in ('.','..') for name in expected),'unsafe path'
    actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() or p.is_symlink()}
    assert actual==set(expected),'packet file set differs'
    for name,item in expected.items():
        p=root/name
        assert not p.is_symlink(),'symlink not allowed'
        b=p.read_bytes()
        assert len(b)==item['bytes'],name+' byte count'
        assert hashlib.sha256(b).hexdigest()==item['sha256'],name+' sha256'
    raw=(root/'MANIFEST.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==binding['audited_manifest_sha256'],'manifest binding'
    manifest=json.loads(raw)
    assert {item['path'] for item in manifest['files']}==set(expected)-{'MANIFEST.json'},'manifest file set'
    assert len(manifest['files'])==len(expected)-1,'duplicate manifest paths'
    for item in manifest['files']:
        assert item==expected[item['path']],'manifest metadata mismatch'
    return len(expected)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--packet',type=Path,required=True);args=parser.parse_args()
    binding=json.loads((HERE/'FROZEN_BINDING.json').read_text())
    print('PASS:',verify(args.packet,binding),'frozen packet files match independent binding')
