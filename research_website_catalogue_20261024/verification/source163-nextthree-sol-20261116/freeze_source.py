"""Finite opaque ZIP custody/PDF metadata/source sealing for one of the fixed3 records."""
from pathlib import Path, PurePosixPath
import datetime
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import unicodedata
import zipfile
import zlib

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
ROWS = {23357329: 163, 23203143: 164, 23153134: 166}


def pin(p, root):
    data = p.read_bytes()
    return {'path': p.relative_to(root).as_posix(), 'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(), 'mode': oct(stat.S_IMODE(p.stat().st_mode))}


def write_json(p, value):
    assert not p.exists()
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def member_path(name):
    original = name
    while name.startswith('./'):
        name = name[2:]
    name = name.removesuffix('/')
    parts = name.split('/')
    assert name and not name.startswith('/') and '\\' not in name and '\0' not in name
    assert all(x not in ('', '.', '..') and ':' not in x for x in parts), original
    return PurePosixPath(*parts)


def main():
    assert len(sys.argv) == 2 and int(sys.argv[1]) in ROWS
    record = int(sys.argv[1])
    S = P / 'papers' / str(record) / 'sources'
    assert not (S / 'SOURCE_FINAL.json').exists() and not (S / 'published-source').exists()
    acquired = json.loads((S / 'ACQUIRED.json').read_bytes())
    native = json.loads((S / 'record.response.body').read_bytes())
    assert acquired['record'] == record and len(acquired['assets']) == len(native['files'])
    for item in acquired['assets']:
        data = (S / item['asset']['path']).read_bytes()
        assert len(data) == item['asset']['bytes'] and hashlib.sha256(data).hexdigest() == item['asset']['SHA256']
        assert hashlib.md5(data).hexdigest() == item['native_MD5'][4:]
    queue = [(S / x['asset']['path'], 0, None) for x in acquired['assets'] if zipfile.is_zipfile(S / x['asset']['path'])]
    containers, total_members, total_bytes = [], 0, 0
    if queue:
        (S / 'published-source').mkdir()
    while queue:
        archive, depth, parent_container = queue.pop(0)
        assert depth <= 3 and len(containers) < 32
        number = len(containers) + 1
        container = S / 'published-source' / ('container-' + str(number).zfill(3))
        tree = container / 'tree'
        rows, seen = [], set()
        with zipfile.ZipFile(archive) as z:
            infos = z.infolist()
            total_members += len(infos)
            assert total_members <= 4096
            for item in infos:
                relative = member_path(item.filename)
                key = unicodedata.normalize('NFC', str(relative)).casefold()
                assert key not in seen and not item.flag_bits & 1, 'duplicate/colliding/encrypted member'
                seen.add(key)
                unix_mode = item.external_attr >> 16
                kind = stat.S_IFMT(unix_mode)
                assert kind in (0, stat.S_IFREG, stat.S_IFDIR) and not unix_mode & 0o7000, 'special/set-id archive mode'
                assert (kind != stat.S_IFDIR or item.is_dir()) and (kind != stat.S_IFREG or not item.is_dir())
                assert 0 <= item.file_size <= 33554432
                assert item.file_size == 0 or item.compress_size > 0 and item.file_size <= item.compress_size * 1000
                total_bytes += item.file_size
                assert total_bytes <= 268435456
                rows.append({'archive_position': len(rows)+1, 'native_name': item.filename, 'relative_path': relative.as_posix(), 'directory': item.is_dir(), 'native_unix_mode': oct(unix_mode), 'native_CRC32': format(item.CRC, '08x'), 'uncompressed_bytes': item.file_size, 'compressed_bytes': item.compress_size, 'compression_method': item.compress_type, 'flag_bits': item.flag_bits})
            tree.mkdir(parents=True)
            for item, row in zip(infos, rows):
                target = tree / row['relative_path']
                assert target.is_relative_to(tree) and not any(p.is_symlink() for p in [target, *target.parents])
                if row['directory']:
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                assert not target.exists()
                body = z.read(item)
                assert len(body) == item.file_size and zlib.crc32(body) == item.CRC
                fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
                try:
                    with os.fdopen(fd, 'wb') as out:
                        out.write(body)
                except BaseException:
                    raise
                permissions = (item.external_attr >> 16) & 0o777
                target.chmod(permissions if permissions else 0o644)
                row['materialized'] = pin(target, S)
                assert row['materialized']['bytes'] == len(body) and row['materialized']['SHA256'] == hashlib.sha256(body).hexdigest()
                if zipfile.is_zipfile(target):
                    queue.append((target, depth + 1, number))
            # Explicit native directory modes are applied only after children are materialized.
            for item, row in reversed(list(zip(infos, rows))):
                if row['directory']:
                    permissions = (item.external_attr >> 16) & 0o777
                    target = tree / row['relative_path']
                    target.chmod(permissions if permissions else 0o755)
                    row['materialized_mode'] = oct(stat.S_IMODE(target.stat().st_mode))
        containers.append({'container_number': number, 'archive': pin(archive, S), 'depth': depth, 'parent_container': parent_container, 'members_in_original_order': rows, 'member_count': len(rows), 'tree': tree.relative_to(S).as_posix()})
    write_json(S / 'CONTAINERS.json', {'status': 'COMPLETE_GUARDED_OPAQUE_ZIP_MATERIALIZATION', 'containers': containers, 'total_members': total_members, 'total_uncompressed_bytes': total_bytes, 'limits': {'members':4096,'uncompressed_bytes':268435456,'member_bytes':33554432,'depth':3,'containers':32,'compression_ratio':1000}, 'path_mode_checks': 'No absolute/traversal/backslash/drive/NUL/case-Unicode-collision/encryption/symlink/device/set-id entries; regular bytes/CRC/SHA preserved. Native permission bits preserved when present; implicit directories755/default regular644.', 'native_program_or_archived_opinion_body_execution_or_reading': False})
    all_paths = sorted((S / 'assets').rglob('*')) + (sorted((S / 'published-source').rglob('*')) if (S / 'published-source').exists() else [])
    tex = [{**pin(p, S), 'lines': len(p.read_bytes().splitlines()), 'LF_count': p.read_bytes().count(b'\n')} for p in all_paths if p.is_file() and p.suffix.lower() == '.tex']
    native_tex = [x for x in tex if x['path'].startswith('assets/')]
    primary_tex = native_tex if len(native_tex) == 1 else [x for x in tex if '/publication/preprint.tex' in x['path']]
    assert len(primary_tex) == 1, 'controlling TeX packaging label ambiguous; no unsupported selection'
    native_pdfs, all_pdf_refs = [], []
    for index, item in enumerate([x for x in acquired['assets'] if x['name'].lower().endswith('.pdf')], 1):
        p = S / item['asset']['path']
        r = subprocess.run(['/opt/homebrew/bin/pdfinfo', str(p)], capture_output=True)
        label = 'pdfinfo-' + str(index).zfill(3)
        (S / (label + '.stdout.txt')).write_bytes(r.stdout)
        (S / (label + '.stderr.txt')).write_bytes(r.stderr)
        pages = re.search(rb'^Pages:\s+(\d+)\s*$', r.stdout, re.M)
        assert r.returncode == 0 and pages
        native_pdfs.append({**pin(p, S), 'pages': int(pages.group(1)), 'pdfinfo_exit': r.returncode, 'literal_stdout': label+'.stdout.txt', 'literal_stderr': label+'.stderr.txt'})
    for p in all_paths:
        if p.is_file() and p.suffix.lower() == '.pdf':
            x = pin(p, S)
            x['identical_native_PDF_paths'] = [q['path'] for q in native_pdfs if q['SHA256'] == x['SHA256']]
            all_pdf_refs.append(x)
    ready = {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status': 'SOURCE_READY_OPAQUE_ACQUISITION_ONLY', 'record':record,'sheet_row':ROWS[record],'title':native['metadata']['title'],'DOI':native['doi'],'concept_DOI':native['conceptdoi'],'native_version':native['metadata'].get('version'),'publication_date':native['metadata']['publication_date'],'created':native['created'],'modified':native.get('modified'),'license':native['metadata']['license'],'creators':native['metadata']['creators'],'native_order':acquired['record_files_order'],'files_entries_order':acquired['files_entries_order'],'files_custom_order':acquired['files_custom_order'],'default_preview':acquired['default_preview'],'latest_record_id':acquired['latest_record_id'],'fixed_record_is_latest':acquired['fixed_record_is_latest'],'version_record_ids':acquired['version_record_ids'],'native_assets':acquired['assets'],'containers':{'count':len(containers),'members':total_members,'uncompressed_bytes':total_bytes,'manifest':pin(S/'CONTAINERS.json',S)},'controlling_TeX':primary_tex,'controlling_selection_basis':'Exactly one directly published native TeX asset, else unique publication/preprint.tex packaging path; no scientific/archived acceptance reading.','all_TeX_candidates':tex,'native_PDFs':native_pdfs,'all_materialized_PDFs':all_pdf_refs,'printed_version_limit':'PDF/TeX mathematical text and printed numeric version were not inspected in this opaque acquisition. Native metadata version is not asserted to be printed. PDF page counts only are independently parsed.','programs_or_archived_opinions_results_bodies_read_or_executed':False,'mathematical_verdict':None,'scientific_intake_authority':False,'production_authority':False,'ordinary_access_failures':[],'automatic_retries':0}
    write_json(S / 'SOURCE_READY.json', ready)
    (S / 'SOURCE_LOG.jsonl').write_text(json.dumps({'UTC':ready['UTC'],'phase':'OPAQUE_SOURCE_ACQUISITION_COMPLETE','native_assets':len(acquired['assets']),'ZIP_containers':len(containers),'members':total_members,'scientific_programs_executed':0,'archived_opinions_results_program_bodies_human_read':0,'printed_version_not_inspected':True,'completion_percent_acquisition':100})+'\n')
    paths = sorted(S.rglob('*'))
    assert not any(p.is_symlink() for p in paths)
    directories = [{'path':p.relative_to(S).as_posix(),'mode':oct(stat.S_IMODE(p.stat().st_mode))} for p in paths if p.is_dir()]
    files = [pin(p,S) for p in paths if p.is_file()]
    write_json(S / 'SOURCE_MANIFEST.json', {'schema':'opaque-native-source-manifest-v1','UTC':ready['UTC'],'root':str(S),'ordinary_files_including_controls':len(files)+2,'child_directory_count':len(directories),'directories':directories,'files':files,'root_controls_excluded_from_own_list':['SOURCE_MANIFEST.json','SOURCE_FINAL.json'],'all_regular_no_symlinks':True})
    final = {'schema':'opaque-native-source-final-v1','UTC':ready['UTC'],'status':'SOURCE_READY_FROZEN_OPAQUE_ACQUISITION_NO_SCIENTIFIC_VERDICT','record':record,'sheet_row':ROWS[record],'SOURCE_READY':pin(S/'SOURCE_READY.json',S),'SOURCE_MANIFEST':pin(S/'SOURCE_MANIFEST.json',S),'extent':{'ordinary_files':len(files)+2,'child_directories':len(directories)},'native_assets':len(acquired['assets']),'native_asset_MD5_size_SHA256_verified':True,'record_files_latest_versions_ordinary_receipts_preserved':True,'controlling_TeX':primary_tex,'native_PDFs':native_pdfs,'printed_numeric_version_not_inspected':True,'container_count':len(containers),'container_member_count':total_members,'source_body_or_program_alteration':False,'scientific_or_native_program_execution':False,'archived_opinions_results_program_bodies_human_read':False,'mathematical_verdict':None,'production_or_publication_authority':False,'completion_percent_acquisition':100,'immutable_after_this_seal':True}
    write_json(S / 'SOURCE_FINAL.json', final)
    print(json.dumps({'record':record,'row':ROWS[record],'SOURCE_FINAL':pin(S/'SOURCE_FINAL.json',S),'SOURCE_READY':pin(S/'SOURCE_READY.json',S),'SOURCE_MANIFEST':pin(S/'SOURCE_MANIFEST.json',S),'extent':final['extent'],'controlling_TeX':primary_tex,'PDF_pages':[x['pages'] for x in native_pdfs],'native_version':ready['native_version'],'publication_date':ready['publication_date'],'created':ready['created']},indent=2))


if __name__ == '__main__':
    main()
