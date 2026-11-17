"""Opaque acquisition for exactly three authorized records; no source prose or native execution."""
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse
import datetime
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import unicodedata
import zipfile
import zlib

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
ROWS = {23409879: 174, 23171212: 175, 23384924: 176}
LIMITS = {'native_assets': 32, 'native_asset_bytes': 104857600, 'version_pages': 10,
          'redirects': 3, 'containers': 32, 'nested_depth': 3, 'members': 4096,
          'member_bytes': 33554432, 'uncompressed_bytes': 268435456,
          'compression_ratio': 1000, 'path_depth': 32, 'path_bytes': 2048}

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def dump(path, value):
    with path.open('x', encoding='utf-8') as out:
        out.write(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def pin(path, root):
    raw = path.read_bytes()
    return {'path': path.relative_to(root).as_posix(), 'bytes': len(raw),
            'SHA256': hashlib.sha256(raw).hexdigest(), 'mode': oct(stat.S_IMODE(path.stat().st_mode))}

def check(condition, reason):
    if not condition:
        raise ValueError(reason)

def safe_url(url):
    u = urlparse(url)
    check(u.scheme == 'https' and u.hostname == 'zenodo.org' and u.port in (None, 443)
          and not u.username and not u.password and not u.fragment, 'URL outside ordinary public Zenodo scope')

def fetch(S, label, url):
    safe_url(url)
    check(not any(S.glob(label + '.*')), 'request label already exists; never overwrite/retry')
    cmd = ['curl', '--disable', '--silent', '--show-error', '--request', 'GET',
           '--proto', '=https', '--retry', '0', '--connect-timeout', '15', '--max-time', '45',
           '--max-filesize', str(LIMITS['native_asset_bytes']), '--dump-header', str(S / (label + '.response.headers')),
           '--output', str(S / (label + '.response.body')), '--write-out', '%{json}', url]
    start = utc()
    result = subprocess.run(cmd, cwd=S, capture_output=True)
    (S / (label + '.curl.stdout.txt')).write_bytes(result.stdout)
    (S / (label + '.curl.stderr.txt')).write_bytes(result.stderr)
    try:
        transport = json.loads(result.stdout)
    except (ValueError, UnicodeDecodeError):
        transport = None
    receipt = {'UTC_start': start, 'UTC_end': utc(), 'command': cmd, 'exit': result.returncode,
               'curl_transport': transport, 'automatic_retries': 0, 'automatic_redirects': False,
               'body': label + '.response.body', 'headers': label + '.response.headers',
               'stdout': label + '.curl.stdout.txt', 'stderr': label + '.curl.stderr.txt'}
    dump(S / (label + '.transport.json'), receipt)
    print(json.dumps({'record': int(S.parent.name), 'request': label, 'exit': result.returncode,
                      'HTTP': None if transport is None else transport.get('http_code')}), flush=True)
    check(result.returncode == 0 and transport is not None, 'ordinary transport failure retained: ' + label)
    return transport, S / (label + '.response.body')

def get(S, label, url):
    seen = set()
    for hop in range(LIMITS['redirects'] + 1):
        check(url not in seen, 'redirect loop')
        seen.add(url)
        name = label if hop == 0 else label + '.redirect-' + str(hop).zfill(2)
        transport, body = fetch(S, name, url)
        code = transport.get('http_code')
        if code in (301, 302, 303, 307, 308):
            url = transport.get('redirect_url')
            check(url and hop < LIMITS['redirects'], 'finite ordinary redirect limit or missing Location')
            safe_url(url)
            continue
        check(code == 200, 'ordinary HTTP failure retained: ' + name + '/' + str(code))
        return body, {'logical_label': label, 'response_label': name, 'redirect_hops': hop,
                      'effective_url': transport.get('url_effective'), 'body': pin(body, S)}
    raise ValueError('unreachable redirect bound')

def safe_asset_name(name):
    check(name not in ('', '.', '..') and not any(c in name for c in '/\\:\0')
          and not any(ord(c) < 32 for c in name) and len(name.encode('utf-8')) <= 255,
          'unsafe native asset name')

def acquire(S, record):
    events = []
    path, event = get(S, 'record', 'https://zenodo.org/api/records/' + str(record))
    events.append(event)
    native = json.loads(path.read_bytes())
    check(native['id'] == record and native.get('status') == 'published' and native.get('state') == 'done',
          'fixed published record identity/status mismatch')
    check(1 <= len(native['files']) <= LIMITS['native_assets'], 'finite native asset count')
    path, event = get(S, 'files-' + str(record), native['links']['files'])
    events.append(event)
    wrapper = json.loads(path.read_bytes())
    entries = wrapper['entries']
    check(len(entries) == len(native['files']), 'native files wrapper count mismatch')
    by_name = {x['key']: x for x in entries}
    check(len(by_name) == len(entries) and set(by_name) == {x['key'] for x in native['files']}, 'native files wrapper names mismatch')
    path, event = get(S, 'latest', native['links']['latest'])
    events.append(event)
    latest = json.loads(path.read_bytes())
    version_ids, seen = [], set()
    url = native['links']['versions']
    for page in range(1, LIMITS['version_pages'] + 1):
        check(url not in seen, 'version-pagination loop')
        seen.add(url)
        path, event = get(S, 'versions-' + str(page).zfill(3), url)
        events.append(event)
        version = json.loads(path.read_bytes())
        version_ids.extend(x['id'] for x in version['hits']['hits'])
        url = version.get('links', {}).get('next')
        if not url:
            break
    else:
        raise ValueError('finite version-pagination limit')
    check(record in version_ids, 'fixed record absent from native version wrapper')
    (S / 'assets').mkdir()
    assets, folded = [], set()
    for pos, item in enumerate(native['files'], 1):
        name = item['key']
        safe_asset_name(name)
        key = unicodedata.normalize('NFC', name).casefold()
        check(key not in folded, 'case/Unicode native asset collision')
        folded.add(key)
        other = by_name[name]
        check(item['size'] == other['size'] and item['checksum'] == other['checksum'], 'record/files size or MD5 mismatch')
        check(0 <= item['size'] <= LIMITS['native_asset_bytes'], 'native asset size limit')
        url = item['links']['self']
        safe_url(url)
        check(urlparse(url).path.startswith('/api/records/' + str(record) + '/files/')
              and urlparse(url).path.endswith('/content'), 'not the fixed record native content link')
        path, event = get(S, 'asset-' + str(record) + '-' + str(pos).zfill(3), url)
        events.append(event)
        raw = path.read_bytes()
        check(len(raw) == item['size'] and item['checksum'].startswith('md5:')
              and hashlib.md5(raw).hexdigest() == item['checksum'][4:], 'native size/MD5 mismatch; literal body retained')
        dest = S / 'assets' / name
        with dest.open('xb') as out:
            out.write(raw)
        dest.chmod(0o644)
        assets.append({'native_position': pos, 'name': name, 'native_MD5': item['checksum'],
                       'actual_MD5': hashlib.md5(raw).hexdigest(), 'asset': pin(dest, S),
                       'native_files_entry_created': other.get('created', 'ABSENT'),
                       'native_files_entry_updated': other.get('updated', 'ABSENT'),
                       'source_url': url, 'response_label': event['response_label']})
    meta = native['metadata']
    acquired = {'schema': 'opaque-fixed-native-acquired-v1', 'UTC': utc(), 'record': record, 'sheet_row': ROWS[record],
                'title': meta['title'], 'DOI': native['doi'], 'concept_DOI': native.get('conceptdoi', 'ABSENT'),
                'native_version': meta.get('version', 'ABSENT'), 'native_version_field_present': 'version' in meta,
                'publication_date_declared': meta['publication_date'], 'created': native['created'],
                'modified': native.get('modified', 'ABSENT'), 'updated': native.get('updated', 'ABSENT'),
                'status': native.get('status', 'ABSENT'), 'state': native.get('state', 'ABSENT'),
                'submitted': native.get('submitted', 'ABSENT'), 'is_published': native.get('is_published', 'ABSENT'),
                'resource_type': meta.get('resource_type', 'ABSENT'), 'access_right': meta.get('access_right', 'ABSENT'),
                'license': meta.get('license', 'ABSENT'), 'creators': meta.get('creators', 'ABSENT'),
                'native_order': [x['key'] for x in native['files']], 'files_entries_order': [x['key'] for x in entries],
                'files_custom_order': wrapper.get('order', 'ABSENT'), 'default_preview': wrapper.get('default_preview', 'ABSENT'),
                'latest_record_id': latest['id'], 'fixed_record_is_latest': latest['id'] == record,
                'version_record_ids': version_ids, 'native_assets': assets, 'events': events,
                'raw_metadata_and_wrappers_preserved': True, 'human_scientific_body_reading': False,
                'automatic_retries': 0, 'scientific_or_native_program_execution': False}
    dump(S / 'ACQUIRED.json', acquired)
    return acquired

def member_path(name, directory):
    original = name
    while name.startswith('./'):
        name = name[2:]
    name = name.removesuffix('/')
    if name in ('', '.') and directory:
        return None
    parts = name.split('/')
    check(name and not name.startswith('/') and '\\' not in name and '\0' not in name,
          'absolute/backslash/NUL/empty archive path: ' + repr(original))
    check(all(x not in ('', '.', '..') and ':' not in x and not any(ord(c) < 32 for c in x)
              and len(x.encode('utf-8')) <= 255 for x in parts), 'unsafe archive component')
    check(len(parts) <= LIMITS['path_depth'] and len(name.encode('utf-8')) <= LIMITS['path_bytes'], 'archive path depth/size')
    return PurePosixPath(*parts)

def materialize(S, acquired):
    queue = []
    for item in acquired['native_assets']:
        p = S / item['asset']['path']
        is_zip = zipfile.is_zipfile(p)
        check(p.suffix.lower() != '.zip' or is_zip, 'native .zip is not a readable ZIP')
        if is_zip:
            queue.append((p, 0, None))
    containers, members, expanded = [], 0, 0
    if queue:
        (S / 'published-source').mkdir()
    while queue:
        archive, depth, parent = queue.pop(0)
        check(depth <= LIMITS['nested_depth'] and len(containers) < LIMITS['containers'], 'nested archive/container bound')
        number = len(containers) + 1
        tree = S / 'published-source' / ('container-' + str(number).zfill(3)) / 'tree'
        rows, prefixes, explicit = [], {}, set()
        with zipfile.ZipFile(archive) as z:
            infos = z.infolist()
            members += len(infos)
            check(members <= LIMITS['members'], 'total archive member limit')
            for index, info in enumerate(infos, 1):
                rel = member_path(info.filename, info.is_dir())
                mode = info.external_attr >> 16
                kind = stat.S_IFMT(mode)
                check(not info.flag_bits & 1 and kind in (0, stat.S_IFREG, stat.S_IFDIR)
                      and not mode & 0o7000, 'encrypted/symlink/special/set-id ZIP member')
                check((kind != stat.S_IFDIR or info.is_dir()) and (kind != stat.S_IFREG or not info.is_dir()), 'ZIP type/name mismatch')
                check(0 <= info.file_size <= LIMITS['member_bytes'], 'ZIP member size bound')
                check(info.file_size == 0 or info.compress_size > 0 and info.file_size <= info.compress_size * LIMITS['compression_ratio'], 'ZIP expansion ratio')
                check(not info.is_dir() or info.file_size == 0, 'directory with payload bytes')
                expanded += info.file_size
                check(expanded <= LIMITS['uncompressed_bytes'], 'total ZIP expansion bound')
                logical = '.' if rel is None else rel.as_posix()
                key = unicodedata.normalize('NFC', logical).casefold()
                check(key not in explicit, 'duplicate/colliding explicit ZIP member')
                explicit.add(key)
                if rel is not None:
                    for k in range(1, len(rel.parts) + 1):
                        spelling = '/'.join(rel.parts[:k])
                        normal = unicodedata.normalize('NFC', spelling).casefold()
                        expected = 'directory' if k < len(rel.parts) or info.is_dir() else 'file'
                        check(normal not in prefixes or prefixes[normal] == (spelling, expected), 'ZIP prefix Unicode/case/file-directory collision')
                        prefixes[normal] = (spelling, expected)
                permissions = mode & 0o777 if info.create_system == 3 and mode else (0o755 if info.is_dir() else 0o644)
                check((permissions & 0o500 == 0o500) if info.is_dir() else bool(permissions & 0o400),
                      'native member mode cannot be preserved with readable finite custody')
                rows.append({'archive_position': index, 'native_name': info.filename, 'relative_path': logical,
                             'directory': info.is_dir(), 'root_marker': rel is None, 'native_create_system': info.create_system,
                             'native_external_attr': info.external_attr, 'native_unix_mode': oct(mode),
                             'materialized_permissions': oct(permissions), 'native_CRC32': format(info.CRC, '08x'),
                             'uncompressed_bytes': info.file_size, 'compressed_bytes': info.compress_size,
                             'compression_method': info.compress_type, 'flag_bits': info.flag_bits})
            tree.mkdir(parents=True)
            for info, row in zip(infos, rows):
                target = tree if row['root_marker'] else tree / row['relative_path']
                check(target.is_relative_to(tree) and not any(x.is_symlink() for x in [target, *target.parents]), 'nonlocal/symlink materialization target')
                if row['directory']:
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                raw = z.read(info)
                check(len(raw) == info.file_size and zlib.crc32(raw) == info.CRC, 'ZIP byte/CRC mismatch')
                fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
                with os.fdopen(fd, 'wb') as out:
                    out.write(raw)
                target.chmod(int(row['materialized_permissions'], 8))
                row['materialized'] = pin(target, S)
                check(row['materialized']['SHA256'] == hashlib.sha256(raw).hexdigest(), 'materialization changed bytes')
                if zipfile.is_zipfile(target):
                    queue.append((target, depth + 1, number))
            for row in reversed(rows):
                if row['directory']:
                    target = tree if row['root_marker'] else tree / row['relative_path']
                    target.chmod(int(row['materialized_permissions'], 8))
                    row['actual_directory_mode'] = oct(stat.S_IMODE(target.stat().st_mode))
        containers.append({'container_number': number, 'archive': pin(archive, S), 'depth': depth,
                           'parent_container': parent, 'tree': tree.relative_to(S).as_posix(),
                           'member_count': len(rows), 'members_in_original_order': rows})
    value = {'schema': 'finite-safe-opaque-ZIP-materialization-v1', 'UTC': utc(), 'containers': containers,
             'total_members': members, 'total_uncompressed_bytes': expanded, 'limits': LIMITS,
             'path_policy': 'Reject traversal/absolute/drive/backslash/control/encrypted/special/set-id entries and duplicate/Unicode/case/file-directory prefix collisions. Preserve original member order/names/attrs/CRC and ordinary permission bits; implicit directories755.',
             'scientific_program_execution_or_human_source_body_reading': False}
    dump(S / 'CONTAINERS.json', value)
    return value

def inspect_metadata(S, acquired):
    roots = [S / 'assets'] + ([S / 'published-source'] if (S / 'published-source').exists() else [])
    paths = [p for root in roots for p in sorted(root.rglob('*')) if p.is_file()]
    tex = [{**pin(p, S), 'lines': len(p.read_bytes().splitlines()), 'LF_count': p.read_bytes().count(b'\n')}
           for p in paths if p.suffix.lower() == '.tex']
    native_tex = [x for x in tex if x['path'].startswith('assets/')]
    if len(native_tex) == 1:
        chosen, basis = native_tex, 'unique directly published native TeX asset'
    elif len({x['SHA256'] for x in tex}) == 1 and tex:
        chosen, basis = tex, 'all TeX packaging copies are byte-identical'
    else:
        labelled = [x for x in tex if PurePosixPath(x['path']).name in ('preprint.tex', 'manuscript.tex', 'main.tex', 'paper.tex')
                    and not any(k in x['path'].lower() for k in ('audit', 'review', 'history', 'verification'))]
        chosen = labelled if len(labelled) == 1 else []
        basis = 'unique non-audit packaging-labelled manuscript path' if chosen else 'AMBIGUOUS; no controlling selection from scientific content'
    pdfs, groups = [], {}
    executable = shutil.which('pdfinfo')
    check(executable is not None, 'installed pdfinfo unavailable; no installation')
    for p in paths:
        if p.suffix.lower() != '.pdf':
            continue
        x = pin(p, S)
        if x['SHA256'] not in groups:
            label = 'pdfinfo-' + str(len(groups) + 1).zfill(3)
            cmd = [executable, str(p)]
            start = utc()
            try:
                result = subprocess.run(cmd, capture_output=True, timeout=20)
                out, err, code = result.stdout, result.stderr, result.returncode
            except subprocess.TimeoutExpired as error:
                out, err, code = error.stdout or b'', error.stderr or b'', 'TIMEOUT20'
            (S / (label + '.stdout.txt')).write_bytes(out)
            (S / (label + '.stderr.txt')).write_bytes(err)
            pages = re.search(rb'^Pages:\s+(\d+)\s*$', out, re.M)
            meta = {'command': cmd, 'UTC_start': start, 'UTC_end': utc(), 'exit': code,
                    'pages': int(pages.group(1)) if code == 0 and pages else None,
                    'stdout': label + '.stdout.txt', 'stderr': label + '.stderr.txt'}
            dump(S / (label + '.execution.json'), meta)
            groups[x['SHA256']] = meta
        x['metadata'] = groups[x['SHA256']]
        x['native_asset'] = x['path'].startswith('assets/')
        pdfs.append(x)
    for x in pdfs:
        x['identical_native_PDF_paths'] = [y['path'] for y in pdfs if y['native_asset'] and y['SHA256'] == x['SHA256']]
    return tex, chosen, basis, pdfs

def seal(S, record, ready, complete):
    dump(S / 'SOURCE_READY.json', ready)
    dump(S / 'SOURCE_LOG.json', {'UTC': utc(), 'phase': 'OPAQUE_SOURCE_FINITE_CLOSURE',
                               'acquisition_complete': complete, 'completion_percent_acquisition': 100 if complete else 0,
                               'scientific_bodies_human_read': 0, 'scientific_program_executions': 0,
                               'printed_numeric_version_uninspected': True})
    controls = ['SOURCE_MANIFEST.json', 'SOURCE_FINAL.json']
    for name in controls:
        with (S / name).open('x', encoding='utf-8') as out:
            out.write('{}\n')
    paths = sorted(S.rglob('*'))
    check(not any(p.is_symlink() for p in paths), 'source symlink')
    check(all(p.is_dir() or stat.S_ISREG(p.stat().st_mode) for p in paths), 'source special file')
    dirs = [{'path': p.relative_to(S).as_posix(), 'mode': oct(stat.S_IMODE(p.stat().st_mode))} for p in paths if p.is_dir()]
    files = [pin(p, S) for p in paths if p.is_file() and p.relative_to(S).as_posix() not in controls]
    manifest = {'schema': 'opaque-native-source-manifest-v1', 'UTC': utc(), 'root': str(S),
                'root_mode': oct(stat.S_IMODE(S.stat().st_mode)),
                'ordinary_files_including_controls': len(files) + 2, 'child_directory_count': len(dirs),
                'directories': dirs, 'files': files,
                'root_controls_excluded_from_own_list': controls,
                'exact_controls_existed_before_enumeration': True,
                'actual_file_paths_including_controls': sorted(p.relative_to(S).as_posix() for p in paths if p.is_file()),
                'no_subtree_wildcard_runtime_or_future_exclusions': True, 'all_regular_no_symlinks': True}
    (S / 'SOURCE_MANIFEST.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    final = {'schema': 'opaque-native-source-final-v1', 'UTC': utc(), 'record': record, 'sheet_row': ROWS[record],
             'status': 'SOURCE_READY_FROZEN_OPAQUE_NO_SCIENTIFIC_VERDICT' if complete else 'INCOMPLETE_FROZEN_LITERAL_FAILURE_NO_RETRY',
             'acquisition_complete': complete, 'SOURCE_READY': pin(S / 'SOURCE_READY.json', S),
             'SOURCE_MANIFEST': pin(S / 'SOURCE_MANIFEST.json', S),
             'extent': {'ordinary_files': len(files) + 2, 'child_directories': len(dirs)},
             'printed_numeric_version_uninspected': True, 'scientific_body_reading_or_execution': False,
             'mathematical_verdict': None, 'publication_authority': False,
             'completion_percent_acquisition': 100 if complete else 0, 'immutable_after_this_seal': True}
    (S / 'SOURCE_FINAL.json').write_text(json.dumps(final, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    for item in files:
        check(pin(S / item['path'], S) == item, 'postseal payload mismatch')
    check(sorted(p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file()) == manifest['actual_file_paths_including_controls'], 'postseal actual extent mismatch')
    return {'record': record, 'row': ROWS[record], 'complete': complete,
            'SOURCE_FINAL': pin(S / 'SOURCE_FINAL.json', S), 'SOURCE_READY': pin(S / 'SOURCE_READY.json', S),
            'SOURCE_MANIFEST': pin(S / 'SOURCE_MANIFEST.json', S), 'extent': final['extent'],
            'controlling_TeX': ready.get('controlling_TeX'), 'PDFs': ready.get('native_PDFs'),
            'native_version': ready.get('native_version'), 'native_asset_count': ready.get('native_asset_count'),
            'container_count': ready.get('container_count'), 'archive_member_occurrences': ready.get('archive_member_occurrences')}

def main():
    check(len(sys.argv) == 2 and int(sys.argv[1]) in ROWS, 'exact authorized record argument required')
    record = int(sys.argv[1])
    S = P / 'papers' / str(record) / 'sources'
    check(not S.parent.exists(), 'paper root already exists unexpectedly; halt this record without overwrite')
    check(not S.exists(), 'source root already exists; immutable targets never rerun')
    S.mkdir(parents=True)
    try:
        acquired = acquire(S, record)
        containers = materialize(S, acquired)
        tex, chosen, basis, pdfs = inspect_metadata(S, acquired)
        native_pdfs = [x for x in pdfs if x['native_asset']]
        complete = bool(chosen and native_pdfs and all(x['metadata']['pages'] is not None for x in native_pdfs))
        ready = {**acquired, 'schema': 'opaque-native-source-ready-v1', 'UTC': utc(),
                 'status': 'SOURCE_READY_OPAQUE_ACQUISITION_ONLY' if complete else 'INCOMPLETE_PACKAGING_OR_PDF_METADATA_INTERFACE',
                 'native_asset_count': len(acquired['native_assets']), 'all_TeX_candidates': tex,
                 'controlling_TeX': chosen, 'controlling_selection_basis': basis,
                 'native_PDFs': native_pdfs, 'all_materialized_PDFs': pdfs,
                 'container_count': len(containers['containers']), 'archive_member_occurrences': containers['total_members'],
                 'uncompressed_bytes': containers['total_uncompressed_bytes'], 'containers_manifest': pin(S / 'CONTAINERS.json', S),
                 'printed_numeric_version': 'UNINSPECTED; native metadata version is not asserted printed',
                 'pdf_prose_TeX_science_README_audit_results_program_bodies_human_read': False,
                 'scientific_or_native_program_execution': False, 'mathematical_verdict': None,
                 'publication_authority': False, 'ordinary_access_failures': [], 'automatic_retries': 0}
    except Exception as error:
        ready = {'schema': 'opaque-source-literal-failure-ready-v1', 'UTC': utc(), 'record': record,
                 'sheet_row': ROWS[record], 'status': 'INCOMPLETE_FAILURE_LITERAL_EVIDENCE_RETAINED_NO_RETRY',
                 'error': repr(error), 'printed_numeric_version': 'UNINSPECTED',
                 'scientific_body_reading_or_execution': False, 'mathematical_verdict': None,
                 'publication_authority': False, 'automatic_retries': 0}
        dump(S / 'ACQUISITION_FAILURE.json', ready)
        complete = False
    print('SEALED ' + json.dumps(seal(S, record, ready, complete), ensure_ascii=False), flush=True)

if __name__ == '__main__':
    main()
