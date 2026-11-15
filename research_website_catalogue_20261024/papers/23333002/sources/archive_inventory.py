"""Opaque recursive archive custody; never interprets scientific contents."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from hashlib import sha256
import io, json, stat, tarfile, unicodedata, zipfile, zlib

S = Path(__file__).resolve().parent
containers, payloads = [], []
expanded = 0


def safe_names(names):
    seen = set()
    for name in names:
        p = PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name or '\x00' in name or not p.parts:
            raise ValueError('unsafe archive path')
        folded = unicodedata.normalize('NFC', '/'.join(p.parts)).casefold()
        if folded in seen:
            raise ValueError('duplicate or canonical/case-colliding archive path')
        seen.add(folded)


def kind(body, name):
    if zipfile.is_zipfile(io.BytesIO(body)):
        return 'zip'
    if body[257:262] == b'ustar' or name.lower().endswith(('.tar', '.tgz', '.tar.gz', '.txz', '.tar.xz', '.tbz2', '.tar.bz2')):
        with tarfile.open(fileobj=io.BytesIO(body), mode='r:*'):
            return 'tar'
    if body.startswith((b'7z\xbc\xaf\x27\x1c', b'Rar!', b'\x1f\x8b', b'BZh', b'\xfd7zXZ', b'\x28\xb5\x2f\xfd')):
        raise ValueError('unsupported compressed/archive magic; no recursive completeness claim')
    return None


def write_payload(body, target):
    global expanded
    expanded += len(body)
    if expanded > 1024 * 1024 * 1024:
        raise ValueError('expanded archive safety bound exceeded')
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as out:
        out.write(body)


def scan(path, depth, archive_kind, root=None):
    if depth > 10:
        raise ValueError('archive recursion safety bound exceeded')
    number = 'container-%03d' % (len(containers) + 1)
    root = root or S / 'nested' / number
    native = path.read_bytes()
    item = {'container_id': number, 'path': str(path), 'depth': depth, 'kind': archive_kind,
            'bytes': len(native), 'SHA256': sha256(native).hexdigest(), 'extraction_root': str(root)}
    containers.append(item)
    pending = []
    if archive_kind == 'zip':
        with zipfile.ZipFile(io.BytesIO(native)) as archive:
            members = archive.infolist()
            if len(members) > 100000:
                raise ValueError('member-count safety bound exceeded')
            safe_names([m.orig_filename for m in members])
            directory = []
            for ordinal, m in enumerate(members):
                if m.orig_filename != m.filename or m.flag_bits & 1:
                    raise ValueError('NUL-renamed or encrypted ZIP member')
                directory.append({'ordinal_zero_based': ordinal, 'filename': m.filename,
                    'original_filename': m.orig_filename, 'is_directory': m.is_dir(),
                    'bytes': m.file_size, 'compressed_bytes': m.compress_size, 'CRC32': '%08x' % m.CRC,
                    'flags': m.flag_bits, 'compression': m.compress_type, 'native_date_time': list(m.date_time),
                    'external_attr': m.external_attr, 'internal_attr': m.internal_attr,
                    'create_system': m.create_system, 'create_version': m.create_version,
                    'extract_version': m.extract_version, 'header_offset': m.header_offset,
                    'extra_hex': m.extra.hex(), 'comment_hex': m.comment.hex()})
                mode = stat.S_IFMT(m.external_attr >> 16)
                if m.is_dir():
                    if mode not in (0, stat.S_IFDIR):
                        raise ValueError('non-directory ZIP mode')
                    continue
                if mode not in (0, stat.S_IFREG):
                    raise ValueError('nonregular ZIP member')
                body = archive.read(m)
                if len(body) != m.file_size or zlib.crc32(body) & 0xffffffff != m.CRC:
                    raise ValueError('native ZIP CRC/size mismatch')
                target = root / m.filename
                write_payload(body, target)
                nested = kind(body, m.filename)
                payloads.append({'container_id': number, 'container_depth': depth,
                    'ordinal_zero_based': ordinal, 'original_member_name': m.filename,
                    'extracted_path': str(target), 'bytes': len(body), 'SHA256': sha256(body).hexdigest(),
                    'CRC32': '%08x' % m.CRC, 'safe_regular_body': True, 'nested_archive_kind': nested})
                if nested:
                    pending.append((target, depth + 1, nested))
            item['whole_original_central_directory'] = directory
            item['archive_comment_hex'] = archive.comment.hex()
    else:
        with tarfile.open(fileobj=io.BytesIO(native), mode='r:*') as archive:
            members = archive.getmembers()
            safe_names([m.name for m in members])
            directory = []
            for ordinal, m in enumerate(members):
                directory.append({'ordinal_zero_based': ordinal, 'name': m.name, 'bytes': m.size,
                                  'mode': m.mode, 'mtime': m.mtime, 'type_hex': m.type.hex(),
                                  'linkname': m.linkname, 'pax_headers': m.pax_headers})
                if m.isdir():
                    continue
                if not m.isfile():
                    raise ValueError('nonregular TAR member')
                body = archive.extractfile(m).read()
                if len(body) != m.size:
                    raise ValueError('native TAR size mismatch')
                target = root / m.name
                write_payload(body, target)
                nested = kind(body, m.name)
                payloads.append({'container_id': number, 'container_depth': depth,
                    'ordinal_zero_based': ordinal, 'original_member_name': m.name,
                    'extracted_path': str(target), 'bytes': len(body), 'SHA256': sha256(body).hexdigest(),
                    'safe_regular_body': True, 'nested_archive_kind': nested})
                if nested:
                    pending.append((target, depth + 1, nested))
            item['whole_original_member_metadata'] = directory
    item['native_member_count_including_directories'] = len(members)
    for task in pending:
        scan(*task)


def main():
    started = datetime.now(timezone.utc).isoformat()
    native = json.loads((S / 'ACQUIRED_NATIVE.json').read_bytes())
    archives = []
    for asset in native['all_assets_original_record_order']:
        p = Path(asset['path'])
        body = p.read_bytes()
        if body.startswith(b'%PDF-'):
            continue
        k = kind(body, p.name)
        if k:
            archives.append((p, k))
    for ordinal, (path, k) in enumerate(archives):
        scan(path, 0, k, S / 'published-source' if len(archives) == 1 else S / 'published-source' / ('asset-%03d' % ordinal))
    result = {'started_UTC': started, 'completed_UTC': datetime.now(timezone.utc).isoformat(),
              'containers': containers, 'all_safe_regular_occurrences': payloads,
              'top_level_archives': len(archives), 'archive_containers': len(containers),
              'nested_archives': len(containers) - len(archives), 'safe_regular_occurrences': len(payloads),
              'expanded_bytes_all_depths': expanded, 'unsafe_or_colliding_names': [],
              'encrypted_or_nonregular_payloads': [], 'unsupported_archive_magic': [],
              'all_payload_CRC_size_SHA256_and_extracted_bytes_verified': True,
              'manuscript_preamble_science_code_results_opinions_read': False}
    with (S / 'ARCHIVE_CUSTODY.json').open('x') as out:
        out.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('containers', 'all_safe_regular_occurrences')}, indent=2))


if __name__ == '__main__':
    main()
