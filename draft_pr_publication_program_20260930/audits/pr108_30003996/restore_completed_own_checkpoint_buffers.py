#!/usr/bin/env python3
"""Verify compressed own private records; optionally restore their exact original bytes."""
from pathlib import Path
import argparse, gzip, hashlib, json, shutil

A = Path(__file__).resolve().parent
C = A.parents[2]

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--restore', action='store_true'); parser.add_argument('--batch', choices=['pr107', 'pr104'], default='pr107'); args = parser.parse_args()
    name = 'ROOT_COMPLETED_PRIVATE_BUFFER_COMPRESSION_20261006.json' if args.batch == 'pr107' else 'ROOT_COMPLETED_PR104_PRIVATE_BUFFER_COMPRESSION_20261006.json'
    receipt = json.loads((A / name).read_text())
    for row in receipt['rows']:
        packed = C / row['compressed_path']; original = C / row['original_path']
        if not packed.resolve().is_relative_to(C) or not original.resolve().is_relative_to(C) or packed.is_symlink():
            raise RuntimeError('Recovery scope')
        data = packed.read_bytes()
        if len(data) != row['compressed_bytes'] or hashlib.sha256(data).hexdigest() != row['compressed_sha256']:
            raise RuntimeError('Compressed custody')
        raw = gzip.decompress(data)
        if len(raw) != row['original_bytes'] or hashlib.sha256(raw).hexdigest() != row['original_sha256']:
            raise RuntimeError('Exact roundtrip')
        if args.restore:
            if original.exists() or shutil.disk_usage(A).free < len(raw) + 32 * 1024 * 1024:
                raise RuntimeError('No overwrite; retain disk reserve')
            with original.open('xb') as stream:
                stream.write(raw)
    print(json.dumps({'all_exact_roundtrips_verified': True, 'original_files_restored': args.restore, 'file_count': len(receipt['rows'])}))

if __name__ == '__main__':
    main()
