"""Bounded native GET acquisition and archive data extraction; no source code runs."""
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import time
import traceback
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'verification/acquire-rows192-194-sol-20261117'
ROWS = [(192, '23204212'), (193, '23204810'), (194, '23318851')]

def need(value, label):
    if not value:
        raise ValueError(label)

def utc():
    return datetime.now(timezone.utc).isoformat()

def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Not regular: ' + str(path))
    body = path.read_bytes()
    return {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest(), 'MD5': hashlib.md5(body).hexdigest(), 'mode': oct(stat.S_IMODE(info.st_mode))}

def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as handle:
        handle.write(data)
    os.chmod(path, 0o644)

def writej(path, value):
    write(path, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())

def pairs(rows):
    value = {}
    for key, item in rows:
        need(key not in value, 'Duplicate JSON key: ' + key)
        value[key] = item
    return value

def readj(path):
    return json.loads(path.read_text(), object_pairs_hook=pairs)

def safe_name(name):
    need(type(name) is str and name and '\\' not in name and '\x00' not in name and not name.startswith('/') and all(part not in ['', '.', '..'] for part in name.split('/')) and PurePosixPath(name).as_posix() == name, 'Unsafe native/archive path: ' + str(name))
    return name

def census(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'Not ordinary root')
    files, dirs = {}, {'.': {'mode': oct(stat.S_IMODE(root.lstat().st_mode)), 'empty': not any(root.iterdir())}}
    for path in sorted(root.rglob('*'), key=lambda item: item.relative_to(root).as_posix()):
        name = safe_name(path.relative_to(root).as_posix())
        info = path.lstat()
        if stat.S_ISDIR(info.st_mode):
            dirs[name] = {'mode': oct(stat.S_IMODE(info.st_mode)), 'empty': not any(path.iterdir())}
        else:
            files[name] = pin(path)
    return {'root': str(root), 'files': files, 'directories': dirs, 'regular_files': len(files), 'child_directories': len(dirs) - 1}

def get(root, url, target, label):
    need(urlsplit(url).scheme == 'https' and urlsplit(url).hostname in ['zenodo.org', 'www.zenodo.org'], 'Native HTTPS Zenodo URL required')
    target.parent.mkdir(parents=True, exist_ok=True)
    base = root / 'transport' / label
    base.parent.mkdir(parents=True, exist_ok=True)
    headers = base.with_name(base.name + '.headers.txt')
    stdout = base.with_name(base.name + '.stdout.txt')
    stderr = base.with_name(base.name + '.stderr.txt')
    receipt = base.with_name(base.name + '.json')
    need(not target.exists() and not any(path.exists() for path in [headers, stdout, stderr, receipt]), 'Request outputs already exist')
    command = ['/usr/bin/curl', '--location', '--silent', '--show-error', '--proto', '=https', '--proto-redir', '=https', '--max-redirs', '4', '--connect-timeout', '30', '--max-time', '120', '--retry', '0', '--dump-header', str(headers), '--output', str(target), '--write-out', '%{http_code}\n%{url_effective}\n%{size_download}\n%{content_type}\n', url]
    start, tick = utc(), time.monotonic()
    with stdout.open('xb') as out, stderr.open('xb') as err:
        result = subprocess.run(command, stdout=out, stderr=err)
    for path in [headers, stdout, stderr, target]:
        if path.exists():
            os.chmod(path, 0o644)
    lines = stdout.read_text().splitlines()
    code = int(lines[0]) if lines and re.fullmatch('[0-9]{3}', lines[0]) else None
    final_url = lines[1] if len(lines) > 1 else None
    value = {'request_URL': url, 'method': 'GET', 'argv': command, 'UTC_start': start, 'UTC_end': utc(), 'elapsed_seconds': time.monotonic() - tick, 'curl_exit': result.returncode, 'HTTP_status': code, 'effective_URL': final_url, 'literal_stdout': pin(stdout), 'literal_stderr': pin(stderr), 'raw_headers': pin(headers) if headers.exists() else None, 'whole_response': pin(target) if target.exists() else None, 'retry': False}
    writej(receipt, value)
    need(result.returncode == 0 and code == 200 and final_url is not None and urlsplit(final_url).hostname in ['zenodo.org', 'www.zenodo.org'] and target.exists(), 'Native download failed; literal transport retained: ' + label)
    return value

def extract_archive(source, destination):
    need(not destination.exists(), 'Archive extraction already exists')
    destination.mkdir(mode=0o755)
    rows, seen, total = [], set(), 0
    with zipfile.ZipFile(source) as archive:
        infos = archive.infolist()
        need(len(infos) <= 20000, 'Archive entry budget')
        for item in infos:
            directory = item.is_dir()
            name = safe_name(item.filename[:-1] if directory and item.filename.endswith('/') else item.filename)
            folded = name.casefold()
            need(folded not in seen and not item.flag_bits & 1, 'Archive duplicate/case alias or encrypted member')
            seen.add(folded)
            total += item.file_size
            need(item.file_size <= 100_000_000 and total <= 400_000_000, 'Archive expanded-byte budget')
            encoded_mode = item.external_attr >> 16
            kind = stat.S_IFMT(encoded_mode)
            need(kind in [0, stat.S_IFDIR if directory else stat.S_IFREG] and not encoded_mode & 0o7000, 'Archive symbolic/special/privileged mode rejected')
            path = destination / name
            path.parent.mkdir(parents=True, exist_ok=True)
            for parent in [path.parent, *path.parent.parents]:
                if parent == destination.parent:
                    break
                need(parent.is_relative_to(destination) and not parent.is_symlink() and parent.is_dir(), 'Extraction parent escape')
            mode = stat.S_IMODE(encoded_mode) or (0o755 if directory else 0o644)
            if directory:
                path.mkdir(exist_ok=True)
                os.chmod(path, mode)
                member = {'mode': oct(mode), 'empty': not any(path.iterdir())}
            else:
                data = archive.read(item)
                need(len(data) == item.file_size, 'Archive member extent')
                write(path, data)
                os.chmod(path, mode)
                member = pin(path)
            rows.append({'native_name': item.filename, 'path': name, 'directory': directory, 'compressed_bytes': item.compress_size, 'bytes': item.file_size, 'CRC32_hex': format(item.CRC, '08x'), 'compression': item.compress_type, 'external_attr': item.external_attr, 'member': member})
    return {'outer': pin(source), 'entries': rows, 'entry_count': len(rows), 'total_uncompressed_bytes': total, 'source_program_execution_import_install': False}

def pdf_data(root, source, number):
    target = root / 'derived' / ('pdf-' + str(number).zfill(3))
    target.mkdir(parents=True)
    info_out, info_err = target / 'pdfinfo.stdout.txt', target / 'pdfinfo.stderr.txt'
    text_out, text_err = target / 'pdftotext.stdout.txt', target / 'pdftotext.stderr.txt'
    text = target / 'paper.txt'
    commands = [['/opt/homebrew/bin/pdfinfo', str(source)], ['/opt/homebrew/bin/pdftotext', '-layout', str(source), str(text)]]
    results = []
    for command, out, err in zip(commands, [info_out, text_out], [info_err, text_err], strict=True):
        with out.open('xb') as output, err.open('xb') as errors:
            start = utc()
            result = subprocess.run(command, stdout=output, stderr=errors)
        results.append({'argv': command, 'UTC_start': start, 'UTC_end': utc(), 'exit': result.returncode, 'stdout': pin(out), 'stderr': pin(err)})
    match = re.search(r'^Pages:\s+(\d+)\s*$', info_out.read_text(), re.M)
    pages = int(match[1]) if match and results[0]['exit'] == 0 else None
    first_lines = text.read_text(errors='replace').splitlines()[:35] if text.exists() else []
    value = {'native_PDF': source.relative_to(root).as_posix(), 'pages': pages, 'executions': results, 'first35_extracted_lines_for_cover_identity_only': first_lines, 'text': pin(text) if text.exists() else None, 'scientific_analysis': False}
    writej(target / 'PDF_DATA.json', value)
    return {'native_file': source.name, 'pages': pages, 'text_path': text.relative_to(root).as_posix() if text.exists() else None, 'cover_identity_excerpt': first_lines}

def seal_source(root, status, metadata, error):
    terminals = ['SOURCE_FINAL.json', 'SOURCE_MANIFEST.json']
    for name in terminals:
        write(root / name, b'')
    snap = census(root)
    files = {name: row for name, row in snap['files'].items() if name not in terminals}
    entries = [{'path': name, 'kind': 'directory', 'mode_octal': row['mode'], 'empty': row['empty']} for name, row in snap['directories'].items()]
    entries += [{'path': name, 'kind': 'file', 'bytes': row['bytes'], 'sha256': row['SHA256'], 'md5': row['MD5'], 'mode_octal': row['mode']} for name, row in files.items()]
    manifest = {'schema': 'source-custody-finite-manifest-v1', 'UTC': utc(), 'root': str(root), 'excluded_control_files': terminals, 'file_count': len(files), 'directory_count': len(snap['directories']), 'entries': sorted(entries, key=lambda row: row['path']), 'all_hidden_empty_bytes_modes_topology_included': True, 'terminal_modes': {name: '0o644' for name in terminals}, 'other_exclusions': []}
    (root / 'SOURCE_MANIFEST.json').write_bytes((json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode())
    final = {'schema': 'native-source-acquisition-final-v1', 'UTC': utc(), 'status': status, 'root': str(root), 'regular_files': len(snap['files']), 'child_directories': snap['child_directories'], 'root_mode': snap['directories']['.']['mode'], 'manifest': pin(root / 'SOURCE_MANIFEST.json'), 'metadata': metadata, 'error': error, 'source_scientific_execution_import_install': False, 'read_only_native_GET_only': True, 'exact_already_created_control_exclusions': terminals, 'frozen_after_this_write': True}
    (root / 'SOURCE_FINAL.json').write_bytes((json.dumps(final, ensure_ascii=False, indent=2) + '\n').encode())
    return {'root': str(root), 'status': status, 'files': final['regular_files'], 'child_directories': final['child_directories'], 'SOURCE_FINAL': pin(root / 'SOURCE_FINAL.json'), 'SOURCE_MANIFEST': pin(root / 'SOURCE_MANIFEST.json'), 'metadata': metadata, 'error': error}

def collect(row, record):
    root = P / 'papers' / record / 'sources'
    need(not root.exists(), 'Existing source namespace preserved; separate schema authentication needed, no overwrite/rerun')
    root.mkdir(parents=True, mode=0o755)
    metadata = {'row': row, 'record': record, 'native_order': []}
    error = None
    try:
        api = root / 'native-metadata/record-api.json'
        page = root / 'native-metadata/record-page.html'
        api_error = None
        try:
            get(root, 'https://zenodo.org/api/records/' + record, api, 'record-api')
        except BaseException as exc:
            api_error = exc
        get(root, 'https://zenodo.org/records/' + record, page, 'record-page')
        if api_error is not None:
            raise api_error
        native = readj(api)
        need(type(native) is dict and str(native['id']) == record and native['status'] == 'published', 'Native published record identity/status')
        m = native['metadata']
        need(native['doi'] == '10.5281/zenodo.' + record and type(native['files']) is list and len(native['files']) > 0, 'Native DOI/file metadata')
        names = [item['key'] for item in native['files']]
        need(len(names) == len(set(names)) and len(names) == len({name.casefold() for name in names}), 'Native duplicate/case-alias names')
        display = re.findall(r'Version\s+(v[^<\s]+)</span>', page.read_text())
        metadata.update({'title': m['title'], 'DOI': native['doi'], 'DOI_URL': native.get('doi_url'), 'record_URL': native.get('links', {}).get('self_html'), 'native_API_version': m.get('version'), 'native_API_version_present': 'version' in m, 'host_display_edition_labels': display, 'host_label_not_author_API_version': True, 'original_declared_publication_date': m.get('publication_date'), 'record_created': native.get('created'), 'record_updated': native.get('updated'), 'native_license': m.get('license'), 'native_creators': m.get('creators'), 'native_Description': m.get('description')})
        archives, pdfs = [], []
        for number, item in enumerate(native['files'], 1):
            name = safe_name(item['key'])
            need('/' not in name and type(item['size']) is int and item['size'] >= 0 and re.fullmatch(r'md5:[0-9a-f]{32}', item['checksum']), 'Native flat original name/size/MD5')
            asset = root / 'zenodo-files' / name
            url = item['links'].get('content', item['links'].get('self'))
            need(type(url) is str and '/records/' + record + '/files/' in urlsplit(url).path, 'Exact native file content link')
            get(root, url, asset, 'assets/' + str(number).zfill(3))
            actual = pin(asset)
            need(actual['bytes'] == item['size'] and 'md5:' + actual['MD5'] == item['checksum'], 'Native asset size/MD5 mismatch; literal downloaded bytes retained')
            metadata['native_order'].append({'ordinal': number, 'name': name, 'native_URL': url, 'native_checksum': item['checksum'], **actual})
            if name.lower().endswith('.zip'):
                destination = root / 'archives' / (str(number).zfill(2) + '-' + name + '.extracted')
                destination.parent.mkdir(parents=True, exist_ok=True)
                extraction = extract_archive(asset, destination)
                writej(destination.parent / (str(number).zfill(2) + '-' + name + '.manifest.json'), extraction)
                archives.append(destination.relative_to(root).as_posix())
            elif name.lower().endswith('.pdf'):
                pdfs.append(pdf_data(root, asset, number))
        metadata['archive_data_roots'] = archives
        metadata['PDFs'] = pdfs
        metadata['TeX_paths'] = sorted(path.relative_to(root).as_posix() for path in root.rglob('*.tex'))
        metadata['rights_and_README_paths'] = sorted(path.relative_to(root).as_posix() for path in root.rglob('*') if path.is_file() and re.search(r'(?i)(?:^|/)(?:license[^/]*|copying[^/]*|readme[^/]*|third_party_notices[^/]*)$', path.relative_to(root).as_posix()))
        writej(root / 'SOURCE_METADATA.json', metadata)
    except BaseException:
        error = traceback.format_exc()
        write(root / 'ACQUISITION_FAILURE.txt', error.encode())
    status = 'COMPLETE_NATIVE_PUBLISHED_SOURCES' if error is None else 'FAILED_NATIVE_ACQUISITION_LITERAL_EVIDENCE_FROZEN'
    return seal_source(root, status, metadata, error)

def main():
    results = []
    for row, record in ROWS:
        try:
            result = collect(row, record)
        except BaseException:
            literal = traceback.format_exc()
            write(OWN / ('record-' + record + '.failure.txt'), literal.encode())
            result = {'record': record, 'row': row, 'status': 'EXISTING_OR_UNSEALED_NAMESPACE_RETAINED_NO_OVERWRITE', 'error': literal}
        writej(OWN / ('record-' + record + '.json'), result)
        results.append(result)
    writej(OWN / 'RESULTS.json', {'UTC': utc(), 'records': results, 'scientific_analysis': False, 'children': 0, 'Git_W_Sheet_mutations_or_outreach': False})
    success = all(result['status'] == 'COMPLETE_NATIVE_PUBLISHED_SOURCES' for result in results)
    with (OWN / 'RESEARCH_LOG.md').open('a') as handle:
        handle.write('\n- ' + utc() + ' — ' + ('100%' if success else '60%') + ' complete toward three finite native source packets. One saved/read data acquirer attempt; independent records processed without retry or overwriting existing packets. Statuses: ' + '; '.join(result['status'] for result in results) + '. Every actual transport/extraction/data-utility failure is retained. Original API/file order, full bytes/checksums and actual version/date/license metadata are recorded; API absent versions and host display editions remain distinct. No source program execution/import/install or scientific opinions, Git/W/Sheet/deploy/AA/redirect/releases/Zenodo mutations/contact/outreach/children. All packets freeze after their terminal controls.\n')
    sys.stdout.flush()
    sys.stderr.flush()
    for name in ['FINAL.json', 'OWNED_MANIFEST.json']:
        write(OWN / name, b'')
    snap = census(OWN)
    payload = {name: data for name, data in snap['files'].items() if name not in ['FINAL.json', 'OWNED_MANIFEST.json']}
    manifest = {'schema': 'finite-native-three-record-acquisition-manifest-v1', 'UTC': utc(), 'root': str(OWN), 'root_mode': snap['directories']['.']['mode'], 'regular_files': snap['regular_files'], 'child_directories': snap['child_directories'], 'files': [{'path': name, **data} for name, data in payload.items()], 'directories': [{'path': name, **data} for name, data in snap['directories'].items()], 'exact_already_created_terminal_exclusions': ['FINAL.json', 'OWNED_MANIFEST.json'], 'other_exclusions': [], 'all_hidden_empty_bytes_modes_topology_included': True}
    (OWN / 'OWNED_MANIFEST.json').write_bytes((json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode())
    final = {'schema': 'native-three-record-source-acquisition-FINAL-v1', 'UTC': utc(), 'status': 'COMPLETE_THREE_NATIVE_SOURCE_PACKETS' if success else 'PARTIAL_ACQUISITION_WITH_LITERAL_FAILURES', 'completion_percent': 100 if success else 60, 'root': str(OWN), 'records': results, 'manifest': pin(OWN / 'OWNED_MANIFEST.json'), 'extent': {'files': snap['regular_files'], 'child_directories': snap['child_directories'], 'root_mode': snap['directories']['.']['mode']}, 'acquirer': pin(OWN / 'acquire.py'), 'literal_stdout': pin(OWN / 'ACQUIRE.stdout.txt'), 'literal_stderr': pin(OWN / 'ACQUIRE.stderr.txt'), 'ordinary_invocations': 1, 'source_scientific_execution_import_install_or_opinions': False, 'Git_W_Sheet_deploy_AA_redirect_release_Zenodo_mutation_outreach_or_children': False, 'all_actual_source_and_own_terminal_pins_external_in_handoff': True, 'frozen_after_this_write': True}
    (OWN / 'FINAL.json').write_bytes((json.dumps(final, ensure_ascii=False, indent=2) + '\n').encode())
    return 0 if success else 1

if __name__ == '__main__':
    raise SystemExit(main())
