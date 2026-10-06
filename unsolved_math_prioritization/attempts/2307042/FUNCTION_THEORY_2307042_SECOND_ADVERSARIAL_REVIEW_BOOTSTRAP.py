#!/usr/bin/env python3
"""Independent verifier for pinned, data-only second-review archive; never executes payload."""
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import struct
import sys
import zipfile

ARCHIVE_SHA = '36a1f5b72b2bc03374f61959a338a135994a98113c8c586c1c33f5171c4691c1'
MANIFEST_SHA = '86911a7823c8b8dc595fa64d2390c4e8b509bc16e677404489028ebc3a4d9e6f'
NAMES = frozenset(('ACCEPTANCE.json', 'INDEPENDENT_LEMMAS.md', 'MANIFEST.json', 'PRIMARY_SOURCE_METADATA.json', 'README.md', 'REPLAY.json', 'REVIEW.md'))

class Reject(ValueError):
    pass

def require(ok, label):
    if not ok:
        raise Reject(label)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate-json-key')
            result[key] = value
        return result
    def constant(value):
        raise Reject('nonfinite-json-number')
    return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=constant)

def inventory(rows):
    require(type(rows) is list, 'inventory-type')
    result = {}
    for row in rows:
        require(type(row) is dict and set(row) == {'path', 'bytes', 'sha256'}, 'inventory-row-schema')
        name = row['path']
        require(type(name) is str and name in NAMES and name not in result, 'inventory-name')
        require(type(row['bytes']) is int and 0 <= row['bytes'] <= 20000, 'inventory-size')
        require(type(row['sha256']) is str and len(row['sha256']) == 64 and all(c in '0123456789abcdef' for c in row['sha256']), 'inventory-sha256')
        result[name] = row
    return result

def validate_structure(raw, manifest_raw):
    """Structural layer, also tested using resealed synthetic negative fixtures."""
    require(len(raw) <= 131072 and len(manifest_raw) <= 16384, 'bounded-input')
    ext = strict_json(manifest_raw)
    require(type(ext) is dict and set(ext) == {'archive', 'archive_bytes', 'archive_sha256', 'format', 'inventory', 'payload_executable', 'mathematical_decision'}, 'external-schema')
    require(ext['archive'] == 'FUNCTION_THEORY_2307042_SECOND_ADVERSARIAL_REVIEW_SAFE.zip', 'external-archive-name')
    require(ext['format'] == 'function-theory-2307042-second-review-external-manifest-v1', 'external-format')
    require(type(ext['archive_bytes']) is int and ext['archive_bytes'] == len(raw), 'external-archive-size')
    require(ext['archive_sha256'] == digest(raw), 'external-archive-hash')
    require(ext['payload_executable'] is False and ext['mathematical_decision'] == 'ACCEPT_UNMODIFIED_AUTHOR_THEOREM', 'review-acceptance-scope')
    rows = inventory(ext['inventory'])
    require(set(rows) == NAMES, 'external-inventory')
    require(len(raw) >= 22 and raw[:4] == b'PK\x03\x04' and raw[-22:-18] == b'PK\x05\x06', 'zip-wrapper-layout')
    end = struct.unpack('<4s4H2LH', raw[-22:])
    require(end[1] == end[2] == end[7] == 0 and end[3] == end[4] and end[5] + end[6] == len(raw)-22, 'zip-end-layout')
    blobs = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        items = z.infolist()
        require(len(items) == len(NAMES), 'member-count')
        names = [item.filename for item in items]
        require(len(names) == len(set(names)), 'duplicate-member')
        require(set(names) == NAMES, 'closed-member-inventory')
        require(not z.comment, 'archive-comment')
        require(sum(item.file_size for item in items) <= 65536, 'bounded-expanded-size')
        cursor = 0
        for item in sorted(items, key=lambda item: item.header_offset):
            require(item.header_offset == cursor, 'zip-local-gap')
            local = struct.unpack('<4s5H3L2H', raw[cursor:cursor+30])
            require(local[0] == b'PK\x03\x04' and local[2] == item.flag_bits and not local[2] & 8 and local[3] == item.compress_type and local[10] == 0, 'zip-local-header')
            local_name = raw[cursor+30:cursor+30+local[9]]
            require(local_name == item.filename.encode('utf-8') and local[7] == item.compress_size and local[8] == item.file_size, 'zip-local-crosscheck')
            cursor += 30 + local[9] + local[10] + item.compress_size
            name = item.filename
            require(name == item.orig_filename and '/' not in name and '\\' not in name and '\x00' not in name, 'unsafe-member-name')
            require(item.create_system == 3 and stat.S_IFMT(item.external_attr >> 16) == stat.S_IFREG, 'nonregular-member')
            require((item.external_attr >> 16) & 0o111 == 0, 'executable-member')
            require(not item.is_dir(), 'directory-member')
            require(not item.flag_bits & 1, 'encrypted-member')
            require(item.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED), 'compression-method')
            require(not item.extra and not item.comment, 'member-metadata')
            require(item.file_size == rows[name]['bytes'], 'member-size')
            blob = z.read(item)
            require(len(blob) == rows[name]['bytes'], 'readback-size')
            require(digest(blob) == rows[name]['sha256'], 'member-hash')
            blob.decode('utf-8')
            if name.endswith('.json'):
                strict_json(blob)
            blobs[name] = blob
        require(cursor == end[6] == z.start_dir, 'zip-central-offset')
    inside = strict_json(blobs['MANIFEST.json'])
    require(type(inside) is dict and set(inside) == {'files','format','manifest_self_reference','payload_kind','problem_id'}, 'internal-schema')
    require(inside['format'] == 'function-theory-2307042-second-independent-review-safe-v1' and inside['problem_id'] == 2307042, 'internal-identity')
    inner_rows = inventory(inside['files'])
    require(set(inner_rows) == NAMES - {'MANIFEST.json'}, 'internal-inventory')
    require(all(row == rows[name] for name,row in inner_rows.items()), 'manifest-crosscheck')
    return blobs

def read_regular(path, limit):
    p=Path(path)
    require(not p.is_symlink() and p.is_file(), 'nonregular-input')
    fd=os.open(p, os.O_RDONLY | getattr(os,'O_NOFOLLOW',0))
    try:
        st=os.fstat(fd)
        require(stat.S_ISREG(st.st_mode) and st.st_size <= limit,'input-type-or-bound')
        with os.fdopen(fd,'rb',closefd=False) as f:
            data=f.read(limit+1)
        require(len(data) <= limit,'input-read-bound')
        return data
    finally:
        os.close(fd)

def verify(archive,manifest):
    raw=read_regular(archive,131072)
    manifest_raw=read_regular(manifest,16384)
    require(len(raw)==13736 and digest(raw)==ARCHIVE_SHA,'review-archive-pin')
    require(len(manifest_raw)==1433 and digest(manifest_raw)==MANIFEST_SHA,'review-manifest-pin')
    blobs=validate_structure(raw,manifest_raw)
    return {'status':'PASS','archive_bytes':len(raw),'archive_sha256':digest(raw),'external_manifest_sha256':digest(manifest_raw),'member_count':len(blobs),'expanded_bytes':sum(map(len,blobs.values())),'payload_executed':False,'mathematics_machine_verified':False}

if __name__=='__main__':
    try:
        require(len(sys.argv)==3,'usage-two-paths-required')
        print(json.dumps(verify(sys.argv[1],sys.argv[2]),sort_keys=True))
    except Exception as exc:
        print(json.dumps({'status':'REJECT','reason':str(exc),'error_type':type(exc).__name__},sort_keys=True))
        sys.exit(1)
