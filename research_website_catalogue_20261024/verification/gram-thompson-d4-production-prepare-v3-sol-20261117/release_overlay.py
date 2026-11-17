#!/usr/bin/env python3
"""Fresh inert three-paper OVERLAY helper source. ALL MODES UNEXECUTED at authoring.
No producer/import/AST/compile/help/test certificate is supplied. Future modes
require exact root source/audit/adoption and phase authorities. Default zero action.
"""
import sys

if __name__ == '__main__' and len(sys.argv) == 1:
    print('{"status":"NO_ACTION_EXPLICIT_ROOT_MODE_REQUIRED","filesystem_data_reads":0,"repository_reads":0,"writes":0,"Git_commands":0,"remote_calls":0,"authority_inferred":false}')
    raise SystemExit(0)

def _run_explicit_mode():
    if sys.flags.optimize or sys.version_info[:2] != (3,14) or sys.implementation.name != 'cpython':
        raise RuntimeError('ACTIVE_MODES_REQUIRE_UNOPTIMIZED_CPYTHON_3_14')
    if sys.argv[1:] not in [['--preflight'],['--stage'],['--commit'],['--deploy']]:
        raise RuntimeError('ONLY_FOUR_EXPLICIT_ROOT_PHASES_NO_DEFAULT_AUTHORITY')
    from pathlib import Path
    import copy
    import ctypes
    import datetime
    import hashlib
    import json
    import os
    import re
    import signal
    import stat
    import struct
    import subprocess
    import time
    import traceback
    import urllib.request
    import urllib.error
    import urllib.parse
    from html.parser import HTMLParser
    import xml.etree.ElementTree as ET

    P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
    M=P.parent
    N=P/'verification/gram-thompson-d4-production-prepare-v3-sol-20261117'
    RUN=P/'verification/gram-thompson-d4-runtime-sol-20261117'
    W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
    S=P/'verification/gram-thompson-d4-overlay-sol-20261117'
    PLAN_SHA='f01b666bfd446e7ea10c1a8694bacd2d2046af1800c77ead0ecb25b620492137'
    TARGETS=frozenset(["public/research/binary-gram-locus-polynomial-obstruction/citation.bib","public/research/binary-gram-locus-polynomial-obstruction/gram_locus_note.pdf","public/research/binary-gram-locus-polynomial-obstruction/gram_locus_support.zip","public/research/binary-gram-locus-polynomial-obstruction/index.html","public/research/d4-canonical-potential-exponent-converse/Canonical_W_D4_Note_v1.0.pdf","public/research/d4-canonical-potential-exponent-converse/Canonical_W_D4_Verification_v1.0.zip","public/research/d4-canonical-potential-exponent-converse/citation.bib","public/research/d4-canonical-potential-exponent-converse/index.html","public/research/index.html","public/research/sitemap.xml","public/research/thompson-reduced-cstar-consequences/citation.bib","public/research/thompson-reduced-cstar-consequences/index.html","public/research/thompson-reduced-cstar-consequences/paper.pdf","public/research/thompson-reduced-cstar-consequences/thompson-cstar-source.zip","public/research/thompson-reduced-cstar-consequences/thompson-cstar-verification.zip"])
    REPLACEMENTS=["public/research/index.html","public/research/sitemap.xml"]
    NEW_DIRS=["research/binary-gram-locus-polynomial-obstruction","research/thompson-reduced-cstar-consequences","research/d4-canonical-potential-exponent-converse"]
    LOG=None
    CURRENT=None

    def need(condition, reason):
        if not condition:
            raise ValueError(reason)



    def utc():
        return datetime.datetime.now(datetime.timezone.utc)



    def sha(raw):
        return hashlib.sha256(raw).hexdigest()



    def pin(raw):
        return {'bytes': len(raw), 'SHA256': sha(raw)}



    def packed(value):
        return (json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False) + '\n').encode('utf-8')



    def unique_pairs(rows):
        result = {}
        for key, value in rows:
            need(key not in result, 'duplicate JSON object key rejected')
            result[key] = value
        return result



    def invalid_json_constant(value):
        raise ValueError('non-finite JSON constant rejected: ' + value)



    def strict_json(raw):
        return json.loads(raw, object_pairs_hook=unique_pairs, parse_constant=invalid_json_constant)



    def inode(info):
        return (info.st_dev, info.st_ino)



    def permissions(path):
        return format(stat.S_IMODE(path.lstat().st_mode), '04o')



    def safe(path):
        need(path.is_absolute() and '..' not in path.parts, 'absolute canonical path')
        need(all(not item.is_symlink() for item in [path, *path.parents]), 'no symlink path: ' + str(path))



    def relative(name):
        q = Path(name)
        need(isinstance(name, str) and name and not q.is_absolute() and q.as_posix() == name and '..' not in q.parts and '.' not in q.parts, 'exact relative path')
        return q



    def held(fd):
        first = os.fstat(fd)
        need(stat.S_ISREG(first.st_mode), 'held ordinary regular file')
        os.lseek(fd, 0, os.SEEK_SET)
        blocks = []
        while True:
            block = os.read(fd, 1048576)
            if not block:
                break
            blocks.append(block)
        last = os.fstat(fd)
        need((first.st_dev, first.st_ino, first.st_size, first.st_mtime_ns, first.st_ctime_ns, first.st_mode) == (last.st_dev, last.st_ino, last.st_size, last.st_mtime_ns, last.st_ctime_ns, last.st_mode), 'stable complete held read')
        raw = b''.join(blocks)
        need(len(raw) == first.st_size, 'whole held buffer')
        return raw



    def read(path):
        safe(path)
        first = path.lstat()
        need(stat.S_ISREG(first.st_mode), 'ordinary file: ' + str(path))
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
        try:
            need(inode(first) == inode(os.fstat(fd)), 'opened file identity')
            raw = held(fd)
            need(inode(path.lstat()) == inode(os.fstat(fd)), 'live held file identity')
            return raw
        finally:
            os.close(fd)



    def row_for(path):
        return {**pin(read(path)), 'mode': permissions(path)}



    def bound(row):
        need(set(row) == {'path', 'bytes', 'SHA256', 'mode'}, 'exact external pin schema')
        path = Path(row['path'])
        need(path.is_absolute(), 'external pin absolute path')
        raw = read(path)
        need({**pin(raw), 'mode': permissions(path)} == {key: row[key] for key in ('bytes', 'SHA256', 'mode')}, 'bound whole bytes/mode: ' + str(path))
        return raw



    def sync_dir(path):
        safe(path)
        fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)



    def write_all(fd, raw):
        offset = 0
        while offset < len(raw):
            count = os.write(fd, raw[offset:])
            need(count > 0, 'complete write')
            offset += count



    def new_file(path, raw, mode=0o600):
        safe(path)
        fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
        try:
            write_all(fd, raw)
            os.fchmod(fd, mode)
            os.fsync(fd)
            need(held(fd) == raw, 'durable complete new buffer')
        finally:
            os.close(fd)
        sync_dir(path.parent)



    def mkdir_exclusive(path, mode):
        safe(path)
        os.mkdir(path, mode)
        os.chmod(path, mode)
        need(stat.S_ISDIR(path.lstat().st_mode) and permissions(path) == format(mode, '04o'), 'exclusive directory mode')
        sync_dir(path)
        sync_dir(path.parent)



    def census(root):
        files = []
        directories = []

        def visit(directory):
            safe(directory)
            first = directory.lstat()
            need(stat.S_ISDIR(first.st_mode), 'ordinary census directory')
            if directory != root:
                directories.append({'path': directory.relative_to(root).as_posix(), 'mode': permissions(directory)})
            for path in sorted(directory.iterdir()):
                info = path.lstat()
                if stat.S_ISDIR(info.st_mode):
                    visit(path)
                elif stat.S_ISREG(info.st_mode):
                    files.append({'path': path.relative_to(root).as_posix(), **row_for(path)})
                else:
                    raise ValueError('special or symbolic namespace object: ' + str(path))
            last = directory.lstat()
            need((first.st_dev, first.st_ino, first.st_mode, first.st_mtime_ns, first.st_ctime_ns) == (last.st_dev, last.st_ino, last.st_mode, last.st_mtime_ns, last.st_ctime_ns), 'stable finite namespace enumeration')

        visit(root)
        files.sort(key=lambda item: item['path'])
        directories.sort(key=lambda item: item['path'])
        return {'root': str(root), 'root_mode': permissions(root), 'files': files, 'directories': directories, 'regular_files': len(files), 'child_directories': len(directories)}



    def mode_value(value):
        need(isinstance(value, str) and re.fullmatch(r'(?:0o[0-7]{3}|0[0-7]{3})', value), 'actual explicit octal mode spelling')
        return format(int(value, 8), '04o')



    def canonical_pin(row):
        need(set(row) == {'bytes', 'SHA256', 'mode'}, 'whole file pin schema')
        need(type(row['bytes']) is int and row['bytes'] >= 0 and isinstance(row['SHA256'], str) and re.fullmatch('[0-9a-f]{64}', row['SHA256']), 'whole file byte/hash types')
        return {**row, 'mode': mode_value(row['mode'])}



    def normalize_snapshot(snapshot):
        dictionary_form = set(snapshot) == {'root', 'files', 'directories', 'regular_files', 'child_directories'}
        need(dictionary_form or set(snapshot) == {'root', 'root_mode', 'files', 'directories', 'regular_files', 'child_directories'}, 'complete actual dot-root dictionary or canonical row snapshot')
        need(isinstance(snapshot['root'], str) and Path(snapshot['root']).is_absolute(), 'explicit snapshot root identity')
        files, directories = [], []
        if dictionary_form:
            need(isinstance(snapshot['files'], dict) and isinstance(snapshot['directories'], dict) and '.' in snapshot['directories'], 'actual complete snapshots use dot-root dictionaries')
            need(not set(snapshot['files']) & set(snapshot['directories']), 'dictionary file/directory disjointness')
            for name, row in snapshot['files'].items():
                relative(name)
                files.append({'path': name, **canonical_pin(row)})
            names = set(snapshot['files']) | (set(snapshot['directories']) - {'.'})
            for name, row in snapshot['directories'].items():
                need(name == '.' or relative(name), 'canonical dictionary directory path')
                need(set(row) == {'mode', 'empty'} and type(row['empty']) is bool, 'actual mode/empty directory row')
                need(row['empty'] == (not any(Path(child).parent.as_posix() == name for child in names)), 'exact dictionary empty topology')
                if name != '.':
                    directories.append({'path': name, 'mode': mode_value(row['mode'])})
            root_mode = mode_value(snapshot['directories']['.']['mode'])
        else:
            need(isinstance(snapshot['files'], list) and isinstance(snapshot['directories'], list), 'canonical snapshot lists')
            for row in snapshot['files']:
                need(set(row) == {'path', 'bytes', 'SHA256', 'mode'}, 'complete file row')
                relative(row['path'])
                files.append({'path': row['path'], **canonical_pin({k: row[k] for k in ('bytes', 'SHA256', 'mode')})})
            for row in snapshot['directories']:
                need(set(row) == {'path', 'mode'}, 'complete directory row')
                relative(row['path'])
                directories.append({'path': row['path'], 'mode': mode_value(row['mode'])})
            root_mode = mode_value(snapshot['root_mode'])
        need(type(snapshot['regular_files']) is int and type(snapshot['child_directories']) is int and snapshot['regular_files'] == len(files) and snapshot['child_directories'] == len(directories), 'exact complete snapshot counts')
        names, dirs = {r['path'] for r in files}, {r['path'] for r in directories}
        need(len(names) == len(files) and len(dirs) == len(directories) and not names & dirs, 'unique disjoint complete snapshot paths')
        for name in names | dirs:
            parent = Path(name).parent.as_posix()
            need(parent == '.' or parent in dirs, 'complete parent topology including hidden and empty directories')
        return {'root': snapshot['root'], 'root_mode': root_mode, 'files': sorted(files, key=lambda r: r['path']), 'directories': sorted(directories, key=lambda r: r['path']), 'regular_files': len(files), 'child_directories': len(directories)}



    def tables(snapshot):
        normalized = normalize_snapshot(snapshot)
        return ({row['path']: {key: row[key] for key in ('bytes', 'SHA256', 'mode')} for row in normalized['files']}, {row['path']: row['mode'] for row in normalized['directories']})



    def whole_snapshot(expected):
        normalized = normalize_snapshot(expected)
        need(census(Path(normalized['root'])) == normalized, 'whole namespace root/bytes/modes/topology: ' + normalized['root'])



    def timestamp(value):
        need(isinstance(value, str), 'literal time string')
        result = datetime.datetime.fromisoformat(value)
        need(result.utcoffset() is not None, 'timezone-qualified time')
        return result



    def packed_heads(root):
        path = root / '.git/packed-refs'
        if not os.path.lexists(path):
            return {}
        rows = {}
        for line in read(path).decode('ascii').splitlines():
            if not line or line.startswith(('#', '^')):
                continue
            match = re.fullmatch('([0-9a-f]{40}) ([^ ]+)', line)
            need(match is not None, 'well-formed packed-ref line')
            oid, name = match.groups()
            if name.startswith('refs/heads/'):
                need(name not in rows, 'unique packed local head')
                rows[name] = {'OID': oid, 'raw_line': line}
        return rows



    def native_fence(guards, successor=None, commit=None):
        need(len(guards) == 2 and {row['root'] for row in guards} == {str(M), str(W)}, 'exact native Math/W guard roots')
        for row in guards:
            root = Path(row['root'])
            need(row['all_nonlocal_refs_and_FETCH_HEAD_bound_by_separate_fences'] is True, 'separate complete native/remote ref guards mandatory')
            optional = root / '.git/config.worktree'
            need((not os.path.lexists(optional)) if row['optional_worktree_config'] is None else row_for(optional) == row['optional_worktree_config'], 'phase-appropriate optional native worktree config/absence')
            for name in ('HEAD', 'config'):
                need(row_for(root / '.git' / name) == {key: row[name][key] for key in ('bytes', 'SHA256', 'mode')}, 'native raw ' + name + ' unchanged')
            need(read(root / '.git/HEAD').decode('ascii') == row['HEAD']['raw'] == 'ref: ' + row['local_branch'] + '\n', 'exact symbolic native HEAD')
            expected_index = row['index'] if root == M or successor is None else {**pin(successor), 'mode': '0644'}
            need(row_for(root / '.git/index') == expected_index, 'phase-appropriate complete native index')
            loose = dict(row['loose_local_heads'])
            if root == W and commit is not None:
                loose['files'] = [dict(item) for item in loose['files']]
                selected = [item for item in loose['files'] if item['path'] == 'master']
                need(len(selected) == 1 and row['local_branch'] == 'refs/heads/master', 'only admitted loose master successor')
                selected[0].update(pin((commit + '\n').encode()))
            whole_snapshot(loose)
            packed = packed_heads(root)
            need(packed == row['packed_local_heads'] and permissions(root / '.git/packed-refs') == row['packed_refs_mode'], 'all selected raw packed local-head lines and mode unchanged')
            leaf = root / '.git' / row['local_branch']
            resolved = read(leaf).decode('ascii').strip() if os.path.lexists(leaf) else packed[row['local_branch']]['OID']
            expected_oid = commit if root == W and commit is not None else row['local_branch_OID']
            need(resolved == expected_oid, 'actual phase local branch resolution')



    def script_units(raw):
        matches = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S))
        need(len(matches) == 1, 'single exact aggregate JSON script')
        script = matches[0]
        body = script.group(1)
        typed = strict_json(body)
        start = body.index('[', body.index('"itemListElement"'))
        decoder = json.JSONDecoder(object_pairs_hook=unique_pairs, parse_constant=invalid_json_constant)
        items, close = decoder.raw_decode(body, start)
        pos = start + 1
        spans = []
        for item in items:
            while body[pos].isspace() or body[pos] == ',':
                pos += 1
            value, end = decoder.raw_decode(body, pos)
            need(value == item, 'actual aggregate item decoding')
            spans.append((pos, end, value))
            pos = end
        need(typed['mainEntity']['itemListElement'] == items, 'actual mainEntity ListItem list')
        return script, body, spans, close - 1, typed



    def tree_entries(p, tree):
        pieces = git(p, 'ls-tree', '-r', '-z', '--full-tree', tree, opaque=True).split(b'\0')
        need(pieces.pop() == b'', 'whole NUL tree listing')
        result = {}
        for record in pieces:
            header, name = record.split(b'\t', 1)
            need(name and name not in result, 'unique complete tree leaf')
            result[name] = header
        return result



    def zero_stat_record(name, oid):
        need(isinstance(name, bytes) and name in {target.encode() for target in TARGETS} and b'\0' not in name and isinstance(oid, str) and re.fullmatch('[0-9a-f]{40}', oid), 'literal selected path and blob OID')
        header = struct.pack('>10I', 0, 0, 0, 0, 0, 0, 0o100644, 0, 0, 0)
        raw = header + bytes.fromhex(oid) + struct.pack('>H', min(len(name), 0xFFF)) + name + b'\0'
        raw += b'\0' * ((-len(raw)) % 8)
        need(len(raw) % 8 == 0 and raw[:24] == b'\0' * 24 and raw[24:28] == struct.pack('>I', 0o100644) and raw[28:40] == b'\0' * 12, 'intentional zero-stat record with exact100644 mode')
        return raw



    def record_tree(records):
        result = {}
        for name, record in records.items():
            mode = struct.unpack('>I', record[1])[0]
            need(mode in (0o100644, 0o100755, 0o120000, 0o160000), 'ordinary raw index tree mode')
            result[name] = (format(mode, '06o') + ' ' + ('commit' if mode == 0o160000 else 'blob') + ' ' + record[2].hex()).encode()
        return result



    def blob_oid(raw):
        return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()



    def semantic_rows(mapping):
        return [{'path_hex': name.hex(), 'header_ascii': value.decode('ascii')} for name, value in sorted(mapping.items())]



    def foreign_rows(native, head, targets):
        return {name: (native.get(name), head.get(name)) for name in (set(native) | set(head)) - targets if native.get(name) != head.get(name)}



    def foreign_serialized(mapping):
        return [{'path_hex': name.hex(), 'native': None if pair[0] is None else pair[0].decode('ascii'), 'HEAD': None if pair[1] is None else pair[1].decode('ascii')} for name, pair in sorted(mapping.items())]



    def remote_parent(p, expected):
        actual = git(p, 'ls-remote', '--exit-code', 'origin', p['branch'])
        need(actual == (expected + '\t' + p['branch'] + '\n').encode(), 'exact singleton remote branch snapshot')



    def event(phase, **values):
        record = {'UTC': utc().isoformat(), 'phase': phase, **values}
        need(LOG is not None, 'private ignored journal before every event/opaque command')
        LOG.write(packed(record))
        LOG.flush()
        os.fsync(LOG.fileno())

    def load_plan():
        need(Path(__file__).absolute() == N / 'release_overlay.py', 'exact new inert-source location')
        raw = read(N / 'PLAN.json')
        need(sha(raw) == PLAN_SHA and permissions(N / 'PLAN.json') == '0644', 'exact sealed new PLAN')
        p = strict_json(raw)
        need(p['schema'] == 'fixed-gram-thompson-d4-overlay-production-source-v1', 'fresh overlay PLAN schema')
        fixed = {'project': str(P), 'Math': str(M), 'website': str(W), 'preparation_root': str(N), 'runtime_root': str(RUN), 'stage_root': str(S), 'helper_name': 'release_overlay.py', 'website_HEAD': '4cc09d6bbbad61aa11077c5002cf84a1e93b1344', 'branch': 'refs/heads/master', 'origin': 'https://github.com/AlecKriebel/aleckriebel.com.git', 'Math_origin': 'https://github.com/AlecKriebel/Math.git', 'Math_branch': 'refs/heads/main', 'git_binary': '/usr/bin/git', 'source_preparation_only': True, 'all_production_modes_UNEXECUTED': True}
        need(all(p[k] == v for k, v in fixed.items()), 'exact task/parent/transport/source-preparation facts')
        need(p['scope_paths'] == sorted(TARGETS) and p['replacement_paths'] == REPLACEMENTS, 'exact15 Git paths and2 replacements')
        need(p['new_directories'] == NEW_DIRS and p['record_ids'] == [23318851, 23204212, 23439776], 'exact three fresh root directories/records')
        need(p['before_counts_files_childdirs_articles_sitemap'] == [803,387,133,134] and p['after_counts_files_childdirs_articles_sitemap'] == [816,390,136,137], 'exact overlay projection counts')
        need(p['website_index'] == {'bytes':9062142,'SHA256':'6b76dc0a4e7a631587aec1c081057479883573f7ff284dfc88b5adad02317179','mode':'0644','version':2,'records':58743,'protected_untargeted_whole_raw_records':58741,'successor_records':58756}, 'actual current index arithmetic, not historical58728')
        need(permissions(N / 'release_overlay.py') == '0644', 'ordinary inert helper source mode')
        return p

    def bindings(p):
        return {'helper': {'path':str(N / 'release_overlay.py'),**row_for(N / 'release_overlay.py')},
                'PLAN': {'path':str(N / 'PLAN.json'),**row_for(N / 'PLAN.json')},
                'controls':p['controls'],'scope_paths':p['scope_paths'],'record_ids':p['record_ids'],
                'runtime_root':str(RUN),'website_parent':p['website_HEAD'],'website_index':p['website_index'],
                'overlay_is_not_a_full_public_mirror':True}

    def explicit_review(review, role, current_bindings, p):
        keys = {'audit_FINAL','audit_manifest','audit_snapshot','actual_schema_present','actual_schema',
                'actual_status_present','actual_status','root_adoption','root_adoption_semantics','root_resolution'}
        need(set(review) == keys, 'exact actual '+role+' audit/root adoption envelope')
        audit_path = Path(review['audit_FINAL']['path'])
        adoption_path = Path(review['root_adoption']['path'])
        need(audit_path.name == 'FINAL.json' and audit_path.is_relative_to(P / 'verification') and adoption_path.is_relative_to(P / 'verification'), 'actual private audit/adoption paths')
        need(not any(audit_path.is_relative_to(q) or adoption_path.is_relative_to(q) for q in (N,S,RUN)), 'independent distinct review/adoption')
        if role == 'overlay':
            need(review['root_adoption'] == p['controls']['overlay_root_adoption'] and review['audit_FINAL'] == p['controls']['overlay_audit_FINAL'] and review['audit_manifest'] == p['controls']['overlay_audit_manifest'], 'actual accepted overlay adoption and corrected independent audit fixed controls')
        audit = strict_json(bound(review['audit_FINAL']))
        bound(review['audit_manifest'])
        adopted = strict_json(bound(review['root_adoption']))
        need(packed(adopted) == packed(review['root_adoption_semantics']), 'entire actual root adoption and JSON types')
        snapshot = normalize_snapshot(review['audit_snapshot'])
        need(snapshot['root'] == str(audit_path.parent), 'whole actual audit root')
        whole_snapshot(snapshot)
        files, unused = tables(snapshot)
        for row in (review['audit_FINAL'],review['audit_manifest']):
            path = Path(row['path'])
            need(path.parent == audit_path.parent and files[path.name] == {k:row[k] for k in ('bytes','SHA256','mode')}, 'external controls included in whole audit')
        for key in ('schema','status'):
            present = review['actual_'+key+'_present']
            need(type(present) is bool and (key in audit) == present and review['actual_'+key] == (audit[key] if present else None), 'actual literal audit field/presence, no guessed PASS')
        resolution = review['root_resolution']
        need(resolution['classification'] == 'ALL_ACTUAL_FINDINGS_RESOLVED_FOR_EXACT_ARTIFACT' and resolution['all_actual_criteria_accepted'] is True and resolution['root_personally_read_complete_artifact_and_audit'] is True, 'root semantic disposition of actual complete criteria/history')
        need(isinstance(resolution['rationale'],str) and resolution['rationale'].strip() and isinstance(resolution['actual_criteria_summary'],str) and resolution['actual_criteria_summary'].strip(), 'literal meaningful root resolution')
        need(resolution['audit_FINAL'] == review['audit_FINAL'] and resolution['audit_manifest'] == review['audit_manifest'], 'root resolution exact actual audit controls')
        if role == 'helper':
            need(resolution['helper'] == current_bindings['helper'] and resolution['PLAN'] == current_bindings['PLAN'], 'root fully read exact new source and PLAN')
        else:
            need(resolution['overlay_FINAL'] == p['controls']['stage_FINAL'] and resolution['overlay_manifest'] == p['controls']['stage_manifest'] and resolution['overlay_seal'] == p['controls']['stage_seal'] and resolution['overlay_builder'] == p['controls']['stage_builder'], 'root adoption exact frozen41/6 overlay/source')
        return snapshot

    def authorization(mode,p):
        path = Path(p['authority_paths'][mode])
        need(path == P / ('verification/root-gram-thompson-d4-'+mode+'-authorization-20261117.json'), 'fresh fixed mode authority path')
        raw = read(path)
        need(permissions(path) == '0644', 'root authority ordinary0644')
        a = strict_json(raw)
        expected = {'schema':p['authority_schema'],'mode':mode,'bindings':bindings(p),
                    'concurrency':'ROOT_SERIALIZED_NO_OTHER_M_OR_W_WRITER',
                    'root_asserts_no_other_M_or_W_writer':True,'root_asserts_nonce_fresh':True,
                    'network_read_authorized':True,'Sheet_authorized':False,'AA':None,'follow_up':None}
        need(packed({k:a[k] for k in expected}) == packed(expected), 'exact current action bindings/JSON types')
        need(a['filesystem_stage_authorized'] is (mode == 'stage') and a['commit_and_push_authorized'] is (mode == 'commit') and a['hosting_deploy_authorized'] is (mode == 'deploy'), 'separate actual mode privileges')
        issued, expiry = timestamp(a['issued_UTC']), timestamp(a['expires_UTC'])
        need(issued <= utc() < expiry and 0 < (expiry-issued).total_seconds() <= 3600, 'fresh short root authority lifetime')
        need(isinstance(a['nonce'],str) and re.fullmatch('[0-9a-f]{64}',a['nonce']), 'fresh root nonce')
        need(re.fullmatch('[0-9a-f]{40}',a['website_tree']) and re.fullmatch('[0-9a-f]{40}',a['Math_native_main']), 'fresh exact current W tree and M parent')
        explicit_review(a['helper_review'],'helper',bindings(p),p)
        explicit_review(a['stage_review'],'overlay',bindings(p),p)
        p['_stage_review'] = a['stage_review']
        p['_native_guards'] = a['native_guards']
        p['_root_authority'] = a
        p['website_tree'], p['Math_native_main'] = a['website_tree'], a['Math_native_main']
        need(re.fullmatch('[0-9a-f]{40}',a['Math_remote_proof']['commit']), 'independently bound actual remote M checkpoint; native main may be stale')
        if mode in ('stage','commit'):
            need(re.fullmatch('[0-9a-f]{64}',a['preflight_SHA256']), 'root pins exact observed phase fingerprint')
        if mode == 'commit':
            for field in ('author_name','author_email','commit_date'):
                value = a[field]
                need(isinstance(value,str) and value == value.strip() and value and not any(ord(c)<32 or ord(c)==127 for c in value), 'literal commit identity/date')
            need(a['author_name'] == p['author_name'] and a['author_email'] == p['author_email'] and '<' not in a['author_name'] and '>' not in a['author_name'] and '<' not in a['author_email'] and '>' not in a['author_email'], 'fixed author and committer')
            when = timestamp(a['commit_date'])
            need(when.microsecond == 0 and int(when.utcoffset().total_seconds())%60 == 0, 'whole-second commit time/minute zone')
            install_success(a['installation_SUCCESS'],p,bindings(p),a['nonce'])
        return {'path':path,'raw':raw,'data':a,'issued':issued,'expiry':expiry,'bindings':bindings(p),'plan':p}

    def current_authority(authority):
        need(read(authority['path']) == authority['raw'] and permissions(authority['path']) == '0644', 'same complete literal authority')
        need(authority['issued'] <= utc() < authority['expiry'], 'still unexpired')
        p = load_plan()
        need(bindings(p) == authority['bindings'], 'exact current helper/PLAN/overlay controls')
        explicit_review(authority['data']['helper_review'],'helper',authority['bindings'],p)
        explicit_review(authority['data']['stage_review'],'overlay',authority['bindings'],p)

    def ignore_prerequisite(authority):
        a,p = authority['data'],authority['plan']
        prerequisite = a['runtime_ignore_prerequisite']
        actual = strict_json(bound(prerequisite['root_record']))
        need(packed(actual) == packed(prerequisite['actual_semantics']) and prerequisite['root_applied_exact_line'] is True and prerequisite['root_verified_effective_ignore'] is True, 'actual separately authorized/applied/effectively checked ignore prerequisite')
        path = P / '.gitignore'
        raw = bound(prerequisite['P_ignore'])
        need(Path(prerequisite['P_ignore']['path']) == path, 'exact programme ignore file')
        lines = raw.decode().splitlines()
        meaningful = [line for line in lines if line.strip() and not line.lstrip().startswith('#')]
        line = '/verification/gram-thompson-d4-runtime-sol-20261117/'
        need(meaningful and meaningful[-1] == line == p['runtime_ignore_line'], 'exact last anchored private-runtime ignore, never edited by helper')
        return {'line':line,'ignore_pin':prerequisite['P_ignore'],'root_prerequisite':prerequisite['root_record']}

    def open_runtime(mode,authority):
        nonlocal LOG,CURRENT
        current_authority(authority)
        prerequisite = ignore_prerequisite(authority)
        safe(RUN)
        if mode == 'preflight':
            need(not os.path.lexists(RUN), 'fresh preflight runtime absent')
            mkdir_exclusive(RUN,0o700)
        else:
            need(stat.S_ISDIR(RUN.lstat().st_mode) and permissions(RUN) == '0700', 'this existing private runtime only')
            for observed_lock in RUN.glob('ACTIVE_*.lock'):
                need(strict_json(read(observed_lock))['nonce'] != authority['data']['nonce'], 'nonce never reused across observed actual phases')
        need(RUN.stat().st_dev == W.stat().st_dev, 'runtime/W shared filesystem before any stage action')
        lock = RUN / ('ACTIVE_'+mode.upper()+'.lock')
        lock_body = packed({'schema':'gram-thompson-d4-mode-lock-v1','mode':mode,'nonce':authority['data']['nonce'],'authorization_SHA256':sha(authority['raw']),'PID':os.getpid()})
        new_file(lock,lock_body)
        lock_fd = os.open(lock,os.O_RDONLY|os.O_NOFOLLOW)
        phase = RUN / mode
        mkdir_exclusive(phase,0o700)
        root = phase / sha(authority['raw'])
        mkdir_exclusive(root,0o700)
        mkdir_exclusive(root/'commands',0o700)
        new_file(root/'authorization.json',authority['raw'])
        fd = os.open(root/'journal.jsonl',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        os.fchmod(fd,0o600)
        os.fsync(fd)
        sync_dir(root)
        LOG = os.fdopen(fd,'wb')
        CURRENT = {'root':root,'mode':mode,'authority':authority,'lock':lock,'lock_fd':lock_fd,'lock_body':lock_body,'owner':inode(os.fstat(lock_fd)),'command_number':0}
        event('PRIVATE_IGNORED_CAPTURE_OPEN',mode=mode,prerequisite=prerequisite)
        ignored = git(authority['plan'],'-C',str(M),'check-ignore','--no-index','-v','--',str(RUN)+'/')
        source_line, ignored_path = ignored.decode().rstrip('\n').split('\t')
        source,line_number,pattern = source_line.rsplit(':',2)
        need(source == str((P/'.gitignore').relative_to(M)) and line_number.isdecimal() and pattern == prerequisite['line'] and ignored_path == str(RUN)+'/', 'actual effective exact private ignore before any W action')
        return root

    def transaction(kind,authority):
        mode = {'install':'stage','publish':'commit'}[kind]
        need(CURRENT is not None and CURRENT['mode'] == mode and CURRENT['authority'] is authority, 'same already-open private mode transaction')
        def check():
            current_authority(authority)
            need(inode(CURRENT['lock'].lstat()) == CURRENT['owner'] and held(CURRENT['lock_fd']) == CURRENT['lock_body'] and permissions(CURRENT['lock']) == '0600', 'same retained exclusive mode lock')
            ignore_prerequisite(authority)
        check()
        event('AUTHORIZED_TRANSACTION',mode=mode,authorization_SHA256=sha(authority['raw']))
        return CURRENT['root'],check,os.dup(CURRENT['lock_fd'])

    def command(argv,*,cwd,env,data=None,before_launch=None):
        need(CURRENT is not None and LOG is not None, 'all literal command streams require private ignored capture')
        CURRENT['command_number'] += 1
        prefix = CURRENT['root']/'commands'/format(CURRENT['command_number'],'04d')
        outpath,errpath = Path(str(prefix)+'.stdout.bin'),Path(str(prefix)+'.stderr.bin')
        outfd = os.open(outpath,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        errfd = os.open(errpath,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        os.fchmod(outfd,0o600)
        os.fchmod(errfd,0o600)
        sync_dir(outpath.parent)
        started = utc().isoformat()
        event('COMMAND_INTENT',argv=argv,cwd=str(cwd),stdin=None if data is None else pin(data),stdout=str(outpath),stderr=str(errpath))
        result = None
        exception = None
        subprocess_started = False
        try:
            if before_launch is not None:
                before_launch()
            subprocess_started = True
            result = subprocess.run(argv,cwd=cwd,env=env,input=data,stdout=outfd,stderr=errfd)
        except BaseException as error:
            exception = {'type':type(error).__name__,'repr':repr(error),'traceback':traceback.format_exc()}
            raise
        finally:
            capture_errors = []
            captured = {}
            try:
                # Integer fds have no Python userspace stream buffer to flush.
                # Both raw files are fsynced even after a handled interruption.
                for label,fd,path in (('stdout',outfd,outpath),('stderr',errfd,errpath)):
                    try:
                        os.fsync(fd)
                        captured[label] = held(fd)
                    except BaseException as error:
                        capture_errors.append({'stream':label,'path':str(path),'type':type(error).__name__,'repr':repr(error),'traceback':traceback.format_exc()})
                event('COMMAND_RETURN' if exception is None else 'COMMAND_EXCEPTION',argv=argv,started_UTC=started,finished_UTC=utc().isoformat(),subprocess_started=subprocess_started,exit=None if result is None else result.returncode,exception=exception,stdout={'path':str(outpath),**(pin(captured['stdout']) if 'stdout' in captured else {})},stderr={'path':str(errpath),**(pin(captured['stderr']) if 'stderr' in captured else {})},capture_errors=capture_errors)
                need(not capture_errors,'private command capture failed; literal files and exception metadata retained')
            finally:
                os.close(outfd)
                os.close(errfd)
        return result.returncode,captured['stdout'],captured['stderr']

    def git(p,*args,data=None,index=None,identity=None,opaque=False,absent_vcs=False):
        env = {key:value for key,value in os.environ.items() if not key.startswith('GIT_')}
        env.update(GIT_OPTIONAL_LOCKS='0',GIT_INDEX_VERSION='2',GIT_TERMINAL_PROMPT='0',GIT_NO_LAZY_FETCH='1',GIT_NO_REPLACE_OBJECTS='1')
        if index is not None:
            need(index.is_relative_to(RUN),'only own ignored private checking/commit index')
            env['GIT_INDEX_FILE'] = str(index)
        if identity is not None:
            env.update(identity)
        options = ['-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','core.untrackedCache=false','-c','gc.auto=0','-c','maintenance.auto=false','-c','commit.gpgsign=false','-c','core.splitIndex=false','-c','index.version=2','-c','core.sparseCheckout=false','-c','index.sparse=false','-c','remote.origin.mirror=false','-c','protocol.allow=never','-c','protocol.https.allow=always']
        argv = [p['git_binary'],'--no-optional-locks',*options,*args]
        code,stdout,stderr = command(argv,cwd=W,env=env,data=data)
        if index is not None and os.path.lexists(index):
            os.chmod(index,0o600)
            need(permissions(index)=='0600','opaque private Git checking index remains0600')
        absent = absent_vcs and tuple(args[-4:]) == ('config','--null','--get-all','remote.origin.vcs') and code == 1 and stdout == stderr == b''
        need(code == 0 or absent,'Git stopped: '+str(args[0]))
        return stdout

    def routing(p,expected=None,root=None):
        root = W if root is None else root
        prefix = () if root == W else ('-C',str(root))
        query = (*prefix,'config','--null','--show-origin','--show-scope','--get-regexp',p['routing_config_key_regex'])
        before = git(p,*query,opaque=True)
        selector = git(p,*prefix,'config','--null','--get-all','remote.origin.vcs',opaque=True,absent_vcs=True)
        fetch = git(p,*prefix,'remote','get-url','--all','origin',opaque=True)
        push = git(p,*prefix,'remote','get-url','--push','--all','origin',opaque=True)
        after = git(p,*query,opaque=True)
        intended = ((p['origin'] if root == W else p['Math_origin'])+'\n').encode()
        need(before == after and selector == b'' and fetch == push == intended,'stable singleton exact intended HTTPS routing')
        state = {'configuration':pin(before),'fetch':pin(fetch),'push':pin(push),'singletons_match_intended_origin':True}
        need(expected is None or state == expected,'same authority-bound effective routing')
        return state


    def archived_entries(snapshot):
        entries=snapshot['entries']
        need(len({row['path'] for row in entries})==len(entries),'unique whole archived paths')
        files,dirs,root_mode=[],[],None
        for row in entries:
            if row['kind']=='file':
                files.append({'path':row['path'],**canonical_pin({k:row[k] for k in ('bytes','SHA256','mode')})})
            else:
                need(row['kind']=='directory','archived ordinary directory')
                if row['path']=='.':
                    root_mode=mode_value(row['mode'])
                else:
                    dirs.append({'path':row['path'],'mode':mode_value(row['mode'])})
        need(root_mode is not None,'archived dot-root mode')
        return normalize_snapshot({'root':snapshot['root'],'root_mode':root_mode,'files':files,'directories':dirs,'regular_files':len(files),'child_directories':len(dirs)})

    def from_entries(snapshot):
        normalized=archived_entries(snapshot)
        root=Path(snapshot['root'])
        for row in snapshot['entries']:
            name=row['path']
            path=root if name=='.' else root/relative(name)
            info=path.lstat()
            need(permissions(path)==mode_value(row['mode']) and info.st_mtime_ns==row['mtime_ns'] and info.st_ctime_ns==row['ctime_ns'],'fixed whole input timestamp/individual mode custody')
            need(row['hidden']==any(part.startswith('.') for part in Path(name).parts if part!='.'),'actual fixed hidden component')
            if row['kind']=='file':
                need(stat.S_ISREG(info.st_mode) and row['empty']==(row['bytes']==0),'fixed regular/empty file')
            else:
                need(stat.S_ISDIR(info.st_mode) and row['empty']==(not any(path.iterdir())),'fixed complete directory/empty topology')
        return normalized

    def overlay_snapshot(p):
        manifest = strict_json(bound(p['controls']['stage_manifest']))
        need(manifest['schema'] == 'finite-owned-private-overlay-namespace-v1' and manifest['scope'] == str(S),'actual frozen overlay manifest identity')
        need((manifest['file_count'],manifest['child_directory_count'],manifest['root_including_directory_count']) == (41,6,7),'whole actual41/6 overlay scope')
        need(manifest['terminal_content_hash_exclusions_exact'] == ['MANIFEST.json','SEAL.json'],'only actual terminal content-hash exclusions')
        entries = manifest['entries']
        need(len({row['path'] for row in entries}) == len(entries),'unique whole manifest objects')
        actual = census(S)
        actual_files,actual_dirs = tables(actual)
        need({row['path'] for row in entries} == set(actual_files)|set(actual_dirs)|{'.'},'complete finite paths including hidden/empty')
        for row in entries:
            name = row['path']
            path = S if name == '.' else S / relative(name)
            info = path.lstat()
            need(permissions(path) == mode_value(row['mode']) and info.st_mtime_ns == row['mtime_ns'],'exact individual actual mode/mtime')
            need(row['hidden'] == any(part.startswith('.') for part in Path(name).parts if part != '.'),'manifest hidden flag')
            if row['kind'] == 'directory':
                need(stat.S_ISDIR(info.st_mode) and row['empty'] == (not any(path.iterdir())),'whole directory/empty topology')
            else:
                need(row['kind'] == 'file' and stat.S_ISREG(info.st_mode) and row['empty'] == (row['bytes']==0) and info.st_size == row['bytes'],'whole regular/empty bytes')
                if name in ('MANIFEST.json','SEAL.json'):
                    need('SHA256' not in row and isinstance(row['content_hash_exclusion'],str),'terminal marker is not an actual hash')
                    key = 'stage_manifest' if name == 'MANIFEST.json' else 'stage_seal'
                    need(actual_files[name] == {k:p['controls'][key][k] for k in ('bytes','SHA256','mode')},'external complete terminal pin')
                else:
                    need(actual_files[name] == canonical_pin({k:row[k] for k in ('bytes','SHA256','mode')}),'all payload complete hashes/modes')
        return actual

    def replay_spans(old,new,changes):
        forward = old
        for row in changes:
            start,before,after = row['start_byte'],row['old'].encode(),row['new'].encode()
            need(type(start) is int and start>=0 and forward[start:start+len(before)] == before and sha(forward) == row['before_SHA256'],'actual sequential literal predecessor')
            forward = forward[:start]+after+forward[start+len(before):]
            need(sha(forward) == row['after_SHA256'],'actual complete forward intermediate')
        need(forward == new,'whole actual forward equality')
        reverse = new
        for row in reversed(changes):
            start,before,after = row['start_byte'],row['old'].encode(),row['new'].encode()
            need(reverse[start:start+len(after)] == after and sha(reverse) == row['after_SHA256'],'actual reverse span, including zero-length Gram deletion')
            reverse = reverse[:start]+before+reverse[start+len(after):]
            need(sha(reverse) == row['before_SHA256'],'actual complete reverse intermediate')
        need(reverse == old,'whole original buffer recovered')

    def aggregate_contract(p,buffers,old_files):
        index = strict_json(bound(p['controls']['index_preservation']))
        XML = strict_json(bound(p['controls']['XML_preservation']))
        old_index,old_XML = read(S/'before/index.html'),read(S/'before/sitemap.xml')
        need({**pin(old_index),'mode':permissions(S/'before/index.html')} == old_files['research/index.html'] and {**pin(old_XML),'mode':permissions(S/'before/sitemap.xml')} == old_files['research/sitemap.xml'],'two actual saved before-buffers equal whole baseline')
        new_index,new_XML = buffers[REPLACEMENTS[0]],buffers[REPLACEMENTS[1]]
        replay_spans(old_index,new_index,index['literal_changes'])
        replay_spans(old_XML,new_XML,XML['literal_changes'])
        old_script,old_body,old_json,unused,old_typed = script_units(old_index.decode())
        new_script,new_body,new_json,unused,new_typed = script_units(new_index.decode())
        need(len(old_json) == old_typed['mainEntity']['numberOfItems'] == 133 and len(new_json) == new_typed['mainEntity']['numberOfItems'] == 136,'133-to136 complete JSON counts')
        need([old_body[a:b] for a,b,v in old_json] == [new_body[a:b] for a,b,v in new_json[:133]] and [v for a,b,v in old_json] == [v for a,b,v in new_json[:133]],'all old raw/typed JSON lexemes retained')
        need([v['position'] for a,b,v in new_json] == list(range(1,137)),'all old/new ListItem positions')
        old_HTML = re.findall(rb'<li\b[^>]*>.*?</li>',old_index,re.S)
        new_HTML = re.findall(rb'<li\b[^>]*>.*?</li>',new_index,re.S)
        need(len(old_HTML) == 133 and len(new_HTML) == 136 and old_HTML == new_HTML[:133],'all133 complete HTML unit prefix')
        need([row['raw'].encode() for row in index['old_units']] == old_HTML and [row['raw'].encode() for row in index['new_units']] == new_HTML[133:],'actual complete raw unit inventories')
        def xml_value(node):
            return {'tag':node.tag,'attributes_in_order':list(node.attrib.items()),'text':node.text,'tail':node.tail,'children':[xml_value(child) for child in node]}
        old_root,new_root = ET.fromstring(old_XML),ET.fromstring(new_XML)
        need(old_root.tag == new_root.tag and old_root.attrib == new_root.attrib and old_root.text == new_root.text,'whole XML root context')
        need(len(old_root) == 134 and len(new_root) == 137 and [xml_value(node) for node in old_root] == [xml_value(node) for node in list(new_root)[:134]],'all134 full namespace/attribute/text/tail/children/order prefix')
        old_raw = re.findall(rb'<url(?:\s[^>]*)?>.*?</url>',old_XML,re.S)
        new_raw = re.findall(rb'<url(?:\s[^>]*)?>.*?</url>',new_XML,re.S)
        need(len(old_raw) == 134 and old_raw == new_raw[:134] and [row['raw'].encode() for row in XML['old_units']] == old_raw,'all134 raw XML units')
        return {'index_old_new':[133,136],'XML_old_new':[134,137],'whole_forward_reverse_exact':True,'complete_raw_typed_prefixes':True}

    def contract(p):
        for row in p['controls'].values():
            bound(row)
        stage = overlay_snapshot(p)
        stage_files,stage_dirs = tables(stage)
        final = strict_json(bound(p['controls']['stage_FINAL']))
        need(final['status'] == 'PRIVATE_OVERLAY_PREPARED_PENDING_INDEPENDENT_AUDIT' and final['physical_full_public_copy'] is False and final['publication_or_future_active_mode_authority'] is False,'frozen private overlay is not production authority or full mirror')
        need('_stage_review' in p,'actual independent audit/root adoption required')
        audit = explicit_review(p['_stage_review'],'overlay',bindings(p),p)
        fixed = strict_json(bound(p['controls']['fixed_inputs']))
        sources = [from_entries(row) for row in fixed['sources'].values()]
        private = [from_entries(row) for row in fixed['accepted_packets'].values()]
        need(len(sources)==3 and sum(r['regular_files'] for r in sources)==222 and sum(r['child_directories'] for r in sources)==37,'actual95/16+55/14+72/7 source scopes')
        need(len(private)==9 and sum(r['regular_files'] for r in private)==366,'all nine actual accepted writer/fact/legacy packets')
        for snapshot in sources+private:
            whole_snapshot(snapshot)
        adoption=strict_json(bound(p['controls']['overlay_root_adoption']))
        need(adoption['status']=='ACCEPTED_PRIVATE_OVERLAY_ONLY' and adoption['future_action_authority'] is False and adoption['publication_certificate'] is False and adoption['projected_files_childdirs_articles_XML']==[816,390,136,137],'actual accepted private overlay receipt, never action authority')
        snapshots=p['_root_authority']['adopted_overlay_packets']
        expected_roots={str(P/packet['path']) for packet in adoption['packets']}
        need(set(snapshots)==expected_roots and adoption['authenticated_files']==70 and adoption['child_directories']==6,'exact accepted stage41+failed12+corrected17 finite70/6')
        for packet in adoption['packets']:
            root=P/packet['path']
            normalized=normalize_snapshot(snapshots[str(root)])
            need(normalized['root']==str(root) and normalized['regular_files']==packet['files'] and normalized['child_directories']==packet['child_directories'],'whole accepted actual packet identity/counts')
            whole_snapshot(normalized)
            files,unused=tables(normalized)
            for name,expected in packet['external_controls'].items():
                need(files[name]['SHA256']==expected,'all actual adopted control pins, terminal fields not interpreted as hashes')

        for path,row in fixed['root_inputs'].items():
            bound({'path':path,**canonical_pin({k:row[k] for k in ('bytes','SHA256','mode')})})
            info = Path(path).lstat()
            need(info.st_mtime_ns == row['mtime_ns'] and info.st_ctime_ns == row['ctime_ns'],'fixed root adoption/review/clearance timestamps')
        website = strict_json(bound(p['controls']['website_before']))
        baseline = archived_entries(website['public'])
        old_files,old_dirs = tables(baseline)
        need((len(old_files),len(old_dirs),baseline['root_mode']) == (803,387,'0750'),'actual full public baseline including individual inherited modes')
        targets = strict_json(bound(p['controls']['target_plan']))
        changes = targets['changes']
        need(len(changes)==15 and targets['A']==13 and targets['M']==2 and {'public/'+r['path'] for r in changes} == TARGETS,'exact actual public-relative overlay target schema')
        need(targets['new_public_directories'] == NEW_DIRS,'three actual new root page directories')
        buffers = {}
        for row in changes:
            name = row['path']
            relative(name)
            git_name = 'public/'+name
            need((name in old_files) == (row['action']=='M') == (git_name in REPLACEMENTS),'only two old globals and13new leaves')
            path = S/'overlay'/name
            raw = read(path)
            need({**pin(raw),'mode':permissions(path)} == canonical_pin({k:row[k] for k in ('bytes','SHA256','mode')}) == stage_files['overlay/'+name] and permissions(path)=='0644','actual selected overlay complete payload/mode')
            buffers[git_name] = raw
        projection = strict_json(bound(p['controls']['projection']))
        files = {name:canonical_pin(row) for name,row in projection['files'].items()}
        dirs = {name:mode_value(mode) for name,mode in projection['directories_including_root'].items()}
        expected_files = dict(old_files)
        expected_files.update({name[7:]:{**pin(raw),'mode':'0644'} for name,raw in buffers.items()})
        expected_dirs = {'.':'0750',**old_dirs,**{name:'0755' for name in NEW_DIRS}}
        need(projection['physical_full_public_copy'] is False and files == expected_files and dirs == expected_dirs and (len(files),len(dirs)-1)==(816,390),'computed whole map equals baseline plus15overlay; all untargeted modes/dirs')
        need({name[8:] for name in stage_files if name.startswith('overlay/')} == {name[7:] for name in TARGETS},'only15physical overlay files, no CSS copies or mirror')
        activation = strict_json(bound(p['controls']['page_activation']))
        need([row['record'] for row in activation] == ['23318851','23204212','23439776'],'actual ordered accepted predecessors')
        marker = b'<p class="entry-meta">Private editorial draft</p>\n'
        for row in activation:
            old = read(Path(row['source_path']))
            new = buffers['public/'+row['candidate_path']]
            need(pin(old)['SHA256'] == row['source_SHA256'],'actual accepted predecessor whole bytes')
            replay_spans(old,new,row['literal_changes'])
            old_body,new_body = old[old.index(b'<body>'):],new[new.index(b'<body>'):]
            need(new_body == (old_body.replace(marker,b'',1) if row['record']=='23318851' else old_body),'only authorized exact Gram BODY deletion plus LF')
        pages = strict_json(bound(p['controls']['page_metadata']))
        need([row['PDF_pages'] for row in pages] == [5,4,5] and [row['native_version'] for row in pages] == ['1.0.0',None,'1.0'],'native page counts/version absence retained')
        aggregate = aggregate_contract(p,buffers,old_files)
        for row in p['configuration_guards']:
            bound(row)
        return {'plan':p,'buffers':buffers,'guards':{'native':p['_native_guards'],'public':baseline,'adopted_inputs':private,'original_sources':sources},'old_files':old_files,'old_dirs':old_dirs,'new_dirs':set(NEW_DIRS),'stage_snapshot':stage,'audit_snapshot':audit,'projection':projection,'aggregate_proof':aggregate}

    def public_fence(context,installed):
        expected,dirs = dict(context['old_files']),dict(context['old_dirs'])
        if installed:
            expected.update({name[7:]:{**pin(raw),'mode':'0644'} for name,raw in context['buffers'].items()})
            dirs.update({name:'0755' for name in context['new_dirs']})
        actual = census(W/'public')
        actual_files,actual_dirs = tables(actual)
        need(actual_files == expected and actual_dirs == dirs and actual['root_mode']=='0750','whole actual public including inherited modes/hidden/empty/topology')
        entity = script_units(read(W/'public/research/index.html').decode())[4]['mainEntity']
        counts = [len(actual_files),len(actual_dirs),entity['numberOfItems'],len(ET.fromstring(read(W/'public/research/sitemap.xml')))]
        need(type(entity['numberOfItems']) is int and len(entity['itemListElement']) == counts[2] and counts == context['plan']['after_counts_files_childdirs_articles_sitemap' if installed else 'before_counts_files_childdirs_articles_sitemap'],'exact phase803/387/133/134 or816/390/136/137')
        return actual,counts

    def Math_remote_fence(p):
        proof = p['_root_authority']['Math_remote_proof']
        need(proof['origin'] == p['Math_origin'] and proof['branch'] == 'refs/heads/main' and re.fullmatch('[0-9a-f]{40}',proof['commit']),'fresh exact Math native/remote binding')
        whole_snapshot(proof['all_loose_refs'])
        need(normalize_snapshot(proof['all_loose_refs'])['root'] == str(M/'.git/refs'),'whole Math local/remote/tag loose refs')
        for name in ('packed_refs','FETCH_HEAD','ORIG_HEAD'):
            row = proof[name]
            path = M/'.git'/('packed-refs' if name=='packed_refs' else name)
            need(not os.path.lexists(path) if row is None else Path(row['path'])==path and bound(row) is not None,'all exact Math optional remote/ref controls')
        routing(p,root=M)
        actual = git(p,'-C',str(M),'ls-remote','--exit-code','origin','refs/heads/main')
        need(actual == (proof['commit']+'\trefs/heads/main\n').encode(),'exact remote Math main snapshot, no fetch/mutation')
        need(git(p,'-C',str(M),'rev-parse','HEAD').strip().decode() == p['Math_native_main'],'unchanged independently bound stale native Math HEAD')
        raw = git(p,'-C',str(M),'ls-tree','-z','--full-tree',proof['commit'],opaque=True)
        pieces = raw.split(b'\0')
        need(pieces.pop()==b'','whole Math root NUL listing')
        mapping = {}
        for item in pieces:
            header,name = item.split(b'\t',1)
            need(name not in mapping,'unique complete Math root entry')
            mapping[name.decode()] = header.decode()
        need(mapping == proof['root_entries'],'all remote root entries, including every sibling/file')
        siblings = {name:header for name,header in mapping.items() if header.startswith('040000 tree ') and name != P.name}
        need(len(siblings)==159 and siblings == proof['protected_159_directory_siblings'],'all159 exact remote sibling tree OIDs')
        base=p['Math_remote_checkpoint_base']
        need(base=='436ec422f9ae291a365b9ff2814cb88bc15db8f3','current verified checkpoint base, not stale parent')
        git(p,'-C',str(M),'merge-base','--is-ancestor',base,proof['commit'])
        base_raw=git(p,'-C',str(M),'ls-tree','-z','--full-tree',base,opaque=True).split(b'\0')
        need(base_raw.pop()==b'','whole immutable base root map')
        base_map={name.decode():header.decode() for header,name in (row.split(b'\t',1) for row in base_raw)}
        base_siblings={name:header for name,header in base_map.items() if header.startswith('040000 tree ') and name!=P.name}
        need(base_siblings==siblings and base_map['docs']==mapping['docs'],'all159 siblings and docs unchanged from436ec base while P checkpoints may advance')
        need({name:header for name,header in base_map.items() if name!=P.name}=={name:header for name,header in mapping.items() if name!=P.name},'all untargeted Math root files/directories unchanged from436ec')
        need(mapping['docs'] == '040000 tree '+proof['docs_tree'],'exact whole remote docs tree')
        docs = git(p,'-C',str(M),'ls-tree','-r','-z','--full-tree',proof['commit'],'--','docs',opaque=True)
        need(sha(docs) == proof['docs_recursive_SHA256'],'complete remote docs leaf/mode/OID map')
        return {'commit':proof['commit'],'root_listing':pin(raw),'siblings':159,'docs':pin(docs)}

    def W_aux_fence(p,commit=None,pushed=False):
        a = p['_root_authority']
        expected = copy.deepcopy(normalize_snapshot(a['W_all_loose_refs']))
        need(expected['root'] == str(W/'.git/refs'),'whole W loose-ref namespace')
        rows = {row['path']:row for row in expected['files']}
        if commit is not None:
            need('heads/master' in rows,'existing exact loose master')
            rows['heads/master'].update(pin((commit+'\n').encode()))
            if pushed:
                row = rows.get('remotes/origin/master')
                need(row is not None,'existing exact origin/master tracking leaf required by current baseline')
                row.update(pin((commit+'\n').encode()))
        expected['files'] = sorted(rows.values(),key=lambda r:r['path'])
        whole_snapshot(expected)
        need(set(a['W_aux_controls'])=={'packed-refs','FETCH_HEAD','ORIG_HEAD'},'whole named W auxiliary ref controls/absences')
        for name,row in a['W_aux_controls'].items():
            path=W/'.git'/name
            need(not os.path.lexists(path) if row is None else Path(row['path'])==path and bound(row) is not None,'all exact auxiliary W refs/absences')
        return True

    def index_entries(raw):
        need(len(raw) >= 32 and raw[:4] == b'DIRC' and struct.unpack('>I', raw[4:8])[0] == 2 and hashlib.sha1(raw[:-20]).digest() == raw[-20:], 'complete checksum-valid native v2 index')
        total = struct.unpack('>I', raw[8:12])[0]
        records = {}
        pos = 12
        previous = None
        for unused in range(total):
            start = pos
            need(pos + 62 <= len(raw) - 20, 'complete raw index record header')
            flags = struct.unpack('>H', raw[pos + 60:pos + 62])[0]
            need(not flags & 0x7000, 'stage-zero v2 record without extended flags')
            end = raw.index(b'\0', pos + 62, len(raw) - 20)
            name = raw[pos + 62:end]
            pos = start + ((end + 1 - start + 7) // 8) * 8
            need(pos <= len(raw) - 20 and name and (previous is None or previous < name) and not any(raw[end + 1:pos]) and flags & 0xFFF == min(len(name), 0xFFF), 'whole sorted unique raw record including stat/flags/padding')
            records[name] = (raw[start:pos], raw[start + 24:start + 28], raw[start + 40:start + 60])
            previous = name
        extension_start = pos
        kinds = []
        while pos < len(raw) - 20:
            need(pos + 8 <= len(raw) - 20, 'complete extension header')
            kind = raw[pos:pos + 4]
            size = struct.unpack('>I', raw[pos + 4:pos + 8])[0]
            need(kind == b'TREE' and kind not in kinds and pos + 8 + size <= len(raw) - 20, 'only known single TREE derived cache; unknown extensions rejected')
            kinds.append(kind)
            pos += 8 + size
        need(pos == len(raw) - 20 and len(records) == total, 'complete finite index extent')
        return records, raw[extension_start:-20]



    def cache_semantics(p, records, extension):
        need(len(extension) >= 8 and extension[:4] == b'TREE', 'actual sole whole TREE extension includes eight-byte header; full index pin authenticates baseline bytes')
        size = struct.unpack('>I', extension[4:8])[0]
        payload = extension[8:]
        need(size == len(payload), 'actual exact TREE payload extent, no unknown extension')
        root = {}
        for name, record in records.items():
            node = root
            parts = name.split(b'/')
            for part in parts[:-1]:
                need(part and (part not in node or isinstance(node[part], dict)), 'native TREE directory/file topology')
                node = node.setdefault(part, {})
            need(parts[-1] and parts[-1] not in node, 'native TREE unique leaf')
            mode = struct.unpack('>I', record[1])[0]
            need(mode in (0o100644, 0o100755, 0o120000, 0o160000), 'native TREE leaf mode')
            node[parts[-1]] = (format(mode, 'o').encode(), record[2])
        trees = {}

        def build(node, path):
            entries, count = [], 0
            for name, item in node.items():
                if isinstance(item, tuple):
                    mode, oid = item
                    entries.append((name, mode, oid, False))
                    count += 1
                else:
                    oid, descendants = build(item, path + (b'/' if path else b'') + name)
                    entries.append((name, b'40000', bytes.fromhex(oid), True))
                    count += descendants
            entries.sort(key=lambda row: row[0] + (b'/' if row[3] else b''))
            body = b''.join(mode + b' ' + name + b'\0' + oid for name, mode, oid, directory in entries)
            oid = hashlib.sha1(b'tree ' + str(len(body)).encode() + b'\0' + body).hexdigest()
            trees[path] = (count, oid, body)
            return oid, count

        build(root, b'')
        pos, seen, valid, invalid = 0, set(), [], []

        def parse(parent, is_root=False):
            nonlocal pos
            end = payload.index(b'\0', pos)
            name = payload[pos:end]
            need((is_root and name == b'') or (not is_root and name and b'/' not in name and name not in (b'.', b'..')), 'actual cached TREE local name')
            lineend = payload.index(b'\n', end + 1)
            numbers = payload[end + 1:lineend]
            need(re.fullmatch(rb'-?[0-9]+ [0-9]+', numbers), 'TREE numeric record syntax')
            entries, children = map(int, numbers.split())
            need(entries >= -1 and 0 <= children <= len(trees), 'TREE cached count bounds')
            pos = lineend + 1
            path = parent + (b'/' if parent else b'') + name if not is_root else b''
            need(path not in seen and path in trees, 'unique cached actual native subtree path')
            seen.add(path)
            if entries >= 0:
                need(pos + 20 <= len(payload), 'whole cached OID bytes')
                oid = payload[pos:pos + 20].hex()
                pos += 20
                need((entries, oid) == trees[path][:2], 'every valid cached TREE native count/path/OID exact')
                valid.append((path, oid, entries, children))
            else:
                invalid.append(path.decode('ascii'))
            for unused in range(children):
                parse(path)

        parse(b'', True)
        need(pos == len(payload) and len(valid) + len(invalid) == len(seen), 'whole actual TREE recursion and every valid or explicitly invalid node')
        response = git(p, 'cat-file', '--batch', data=b''.join(oid.encode() + b'\n' for path, oid, entries, children in valid), opaque=True)
        pos = 0
        for path, oid, entries, children in valid:
            lineend = response.index(b'\n', pos)
            header = response[pos:lineend].split()
            need(len(header) == 3 and header[:2] == [oid.encode(), b'tree'], 'valid cached actual local Git tree object')
            length = int(header[2])
            pos = lineend + 1
            need(response[pos:pos + length] == trees[path][2] and response[pos + length:pos + length + 1] == b'\n', 'actual Git tree object bytes equal independently reconstructed native semantics')
            pos += length + 1
        need(pos == len(response), 'complete finite cached-object batch consumed')
        need(len(extension) == len(payload) + 8 and len(valid) + len(invalid) == len(seen), 'whole extension/payload semantics; complete native index is independently externally pinned')
        return {'whole_extension': pin(extension), 'payload': pin(payload), 'nodes': len(seen), 'valid_nodes': len(valid), 'invalidated_paths_no_OID': invalid, 'native_root_tree': trees[b''][1], 'valid_cached_nodes': [{'path_hex': path.hex(), 'OID': oid, 'entries': entries, 'subtrees': children} for path, oid, entries, children in valid]}



    def tree_ancestor_evidence(extension,targets):
        need(extension[:4]==b'TREE' and struct.unpack('>I',extension[4:8])[0]==len(extension)-8,'whole exact single TREE')
        payload,pos=extension[8:],0
        required={b''}
        for target in targets:
            parts=target.split(b'/')
            required.update(b'/'.join(parts[:i]) for i in range(1,len(parts)))
        expected={b'',b'public',b'public/research'}|{('public/'+name).encode() for name in NEW_DIRS}
        need(required==expected and len(required)==6,'exact six target ancestors: root/public/research/three fresh page roots')
        records={}
        def node(parent,is_root=False):
            nonlocal pos
            start=pos
            end=payload.index(b'\0',pos)
            name=payload[pos:end]
            need((is_root and name==b'') or (not is_root and name and b'/' not in name and name not in (b'.',b'..')),'actual cached local TREE name')
            lineend=payload.index(b'\n',end+1)
            numbers=payload[end+1:lineend]
            need(re.fullmatch(rb'-?[0-9]+ [0-9]+',numbers),'actual TREE count syntax')
            count,children=map(int,numbers.split())
            need(count>=-1 and children>=0,'actual cached count bounds')
            pos=lineend+1
            if count>=0:
                need(pos+20<=len(payload),'whole actual cached tree OID')
                pos+=20
            path=b'' if is_root else parent+(b'/' if parent else b'')+name
            need(path not in records,'unique cached TREE node')
            records[path]={'count':count,'children':children,'raw_header':payload[start:pos]}
            for unused in range(children):
                node(path)
        node(b'',True)
        need(pos==len(payload),'complete actual TREE topology')
        present=required&set(records)
        need(present=={b'',b'public',b'public/research'},'three new page roots absent from current actual cache')
        need(all(records[path]['count']==-1 for path in present),'all required existing ancestors already invalid; no general TREE rewrite authorized or needed')
        proof={'required_target_ancestors':[path.decode() for path in sorted(required)],
               'existing_required_nodes':[{'path':path.decode(),'count':records[path]['count'],'children':records[path]['children'],'raw_header':pin(records[path]['raw_header'])} for path in sorted(present)],
               'absent_new_page_roots':[path.decode() for path in sorted(required-set(records))],
               'all_required_existing_nodes_already_invalid':True,'complete_cached_nodes':len(records),
               'all_other_raw_extension_bytes_preserved':True,'whole_extension_unchanged':pin(extension)}
        return extension,proof

    def unchanged_tree_for_targets(extension,targets):
        return tree_ancestor_evidence(extension,targets)[0]

    def native_successor(raw,oids):
        records,extension = index_entries(raw)
        need(set(oids)==TARGETS and len(records)==58743,'exact current58743 index and15targets')
        targets = {name.encode() for name in TARGETS}
        need(len(set(records)-targets)==58741 and set(records)&targets == {name.encode() for name in REPLACEMENTS},'all58741 untargeted and only2existing target records')
        selected = {name.encode():zero_stat_record(name.encode(),oid) for name,oid in oids.items()}
        bodies = {name:row[0] for name,row in records.items()}
        bodies.update(selected)
        need(len(bodies)==58756,'exact13new entries and58756successor')
        after_extension = unchanged_tree_for_targets(extension,targets)
        body = b'DIRC'+struct.pack('>II',2,len(bodies))+b''.join(bodies[name] for name in sorted(bodies))+after_extension
        successor = body+hashlib.sha1(body).digest()
        after,actual_extension = index_entries(successor)
        need(actual_extension == after_extension and all(after[name][0] == row for name,row in selected.items()),'exact TREE invalidation and15whole selected zero-stat records')
        need(all(after[name]==row for name,row in records.items() if name not in targets),'all58741 whole raw stat/flags/padding/path/mode/OID buffers byte-exact')
        return successor

    def preflight(p,installed,owned_index_lock=None):
        context = contract(p)
        native_fence(context['guards']['native'])
        W_aux_fence(p)
        Math_proof = Math_remote_fence(p)
        need(git(p,'rev-parse','--show-toplevel').strip().decode() == str(W) and git(p,'rev-parse','--absolute-git-dir').strip().decode() == str(W/'.git'),'exact ordinary W repository')
        need(git(p,'symbolic-ref','HEAD').strip().decode() == p['branch'] and git(p,'rev-parse','HEAD').strip().decode() == p['website_HEAD'],'same exact W master parent')
        need(git(p,'rev-parse','--show-object-format').strip()==b'sha1','SHA1 repository')
        tree = git(p,'rev-parse',p['website_HEAD']+'^{tree}').strip().decode()
        need(tree == p['website_tree'],'root-bound exact current whole parent tree')
        route = routing(p)
        remote_parent(p,p['website_HEAD'])
        old = read(W/'.git/index')
        need(row_for(W/'.git/index') == {k:p['website_index'][k] for k in ('bytes','SHA256','mode')},'whole9062142-byte current native index')
        records,extension = index_entries(old)
        target_bytes = {name.encode() for name in TARGETS}
        need(len(records)==58743 and set(records)&target_bytes == {name.encode() for name in REPLACEMENTS} and len(set(records)-target_bytes)==58741,'exact current raw-record partition')
        cache = cache_semantics(p,records,extension)
        unused,TREE_ancestor_proof = tree_ancestor_evidence(extension,target_bytes)
        lock = W/'.git/index.lock'
        need(not os.path.lexists(lock) if owned_index_lock is None else os.path.lexists(lock) and inode(lock.lstat())==owned_index_lock,'exclusive native index lock state')
        head_scope = git(p,'ls-tree','-r','-z','--full-tree',p['website_HEAD'],'--',*sorted(TARGETS),opaque=True).split(b'\0')
        need(head_scope.pop()==b'' and {row.split(b'\t',1)[1] for row in head_scope} == {name.encode() for name in REPLACEMENTS},'only2existing target leaves in complete current HEAD')
        for record in head_scope:
            header,name = record.split(b'\t',1)
            original = 'before/index.html' if name.decode()==REPLACEMENTS[0] else 'before/sitemap.xml'
            need(header == ('100644 blob '+blob_oid(read(S/original))).encode() and record_tree({name:records[name]})[name]==header,'old aggregate blobs identical in HEAD/native index/source')
        actual,counts = public_fence(context,installed)
        identities = {}
        for name in REPLACEMENTS:
            info = (W/name).lstat()
            identities[name] = [*inode(info),info.st_mtime_ns,info.st_ctime_ns]
        protected = b''.join(records[name][0] for name in sorted(set(records)-target_bytes))
        prerequisite = ignore_prerequisite(CURRENT['authority'])
        state = {'installed':installed,'bindings':bindings(p),'W_HEAD':p['website_HEAD'],'W_tree':tree,
                 'W_index':pin(old),'routing':route,'Math_remote':Math_proof,
                 'native_guards_SHA256':sha(packed(p['_native_guards'])),
                 'public_snapshot_SHA256':sha(packed(actual)),'counts':counts,
                 'aggregate_identities':identities,'protected_raw_records':pin(protected),'protected_count':58741,
                 'baseline_TREE_extension':pin(extension),'TREE_cache_proof_SHA256':sha(packed(cache)),
                 'required_target_ancestor_proof':TREE_ancestor_proof,
                 'stage_snapshot_SHA256':sha(packed(context['stage_snapshot'])),
                 'audit_snapshot_SHA256':sha(packed(context['audit_snapshot'])),
                 'source_guard_SHA256':sha(packed(context['guards']['adopted_inputs']+context['guards']['original_sources'])),
                 'runtime_ignore_file':prerequisite['ignore_pin'],'root_ignore_prerequisite':prerequisite['root_prerequisite']}
        context.update(old_index=old,old_records=records,old_extension=extension,cache_proof=cache,TREE_ancestor_proof=TREE_ancestor_proof,tree=tree,state=state,fingerprint=sha(packed(state)))
        return context

    def install_success(row,p,current_bindings,commit_nonce):
        path = Path(row['path'])
        need(path.name=='SUCCESS.json' and path.parent.parent == RUN/'stage' and re.fullmatch('[0-9a-f]{64}',path.parent.name),'this effort single stage SUCCESS only')
        result = strict_json(bound(row))
        need(result['schema']=='gram-thompson-d4-install-success-v1' and result['status']=='FILESYSTEM_INSTALL_VERIFIED_SNAPSHOT','actual completed15leaf stage')
        need(result['bindings']==current_bindings and result['counts']==[816,390,136,137] and result['targets']==sorted(TARGETS),'exact current installed overlay and whole counts')
        need(result['authorization_SHA256']==path.parent.name and result['nonce']!=commit_nonce and result['runtime_root']==str(RUN),'distinct later commit nonce and this runtime')
        original = read(path.parent/'authorization.json')
        need(sha(original)==result['authorization_SHA256'],'actual original stage authority retained')
        stage_authority = strict_json(original)
        need(stage_authority['mode']=='stage' and stage_authority['bindings']==current_bindings and stage_authority['nonce']==result['nonce'],'exact original stage action')
        lock = strict_json(read(RUN/'ACTIVE_STAGE.lock'))
        need(lock['authorization_SHA256']==result['authorization_SHA256'] and lock['nonce']==result['nonce'] and lock['mode']=='stage','retained exact stage lock')
        need(permissions(RUN)=='0700' and permissions(RUN/'stage')=='0700' and permissions(path.parent)=='0700','private stage evidence modes')
        return result

    def private_relative_backup(root, name, raw, mode=0o644):
        parent = root
        parts = relative(name).parts
        for part in parts[:-1]:
            parent = parent / part
            if not os.path.lexists(parent):
                mkdir_exclusive(parent, 0o700)
            need(stat.S_ISDIR(parent.lstat().st_mode) and permissions(parent) == '0700', 'private relative backup ancestor')
        new_file(root / name, raw, mode)



    def native_backups(root, context):
        mkdir_exclusive(root, 0o700)
        new_file(root / 'index.before', context['old_index'], 0o600)
        for name, leaf in [('HEAD.before', 'HEAD'), ('config.before', 'config'), ('loose-master.before', 'refs/heads/master')]:
            new_file(root / name, read(W / '.git' / leaf), 0o600)
        new_file(root / 'native-guards.before.json', packed(context['guards']['native']))
        sync_dir(root)



    def install(context, authority):
        p, buffers = context['plan'], context['buffers']
        need(not context['state']['installed'] and context['fingerprint'] == authority['data']['preflight_SHA256'], 'exact current preinstall action fingerprint')
        need(sys.platform == 'darwin', 'exclusive Darwin leaf publication only')
        t, check, lock_fd = transaction('install', authority)
        opened = []
        made = {}
        completed = []
        libc = ctypes.CDLL('/usr/lib/libSystem.B.dylib', use_errno=True)
        exclusive_rename = libc.renameatx_np
        exclusive_rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        exclusive_rename.restype = ctypes.c_int
        try:
            staged, backups = t / 'staged', t / 'aggregate-backups'
            mkdir_exclusive(staged, 0o700)
            mkdir_exclusive(backups, 0o700)
            native_backups(t / 'native-backups', context)
            order = sorted(TARGETS - set(REPLACEMENTS)) + REPLACEMENTS
            prepared, originals = {}, {}
            for index, name in enumerate(order):
                new_file(staged / str(index), buffers[name], 0o644)
                fd = os.open(staged / str(index), os.O_RDONLY | os.O_NOFOLLOW)
                opened.append(fd)
                prepared[name] = fd
            for name in REPLACEMENTS:
                fd = os.open(W / name, os.O_RDONLY | os.O_NOFOLLOW)
                opened.append(fd)
                originals[name] = fd
                need(inode(os.fstat(fd)) == inode((W / name).lstat()), 'held original aggregate identity')
                raw = held(fd)
                need({**pin(raw), 'mode': permissions(W / name)} == context['old_files'][name[7:]], 'complete exact original aggregate')
                private_relative_backup(backups, name, raw)
            absent = sorted(TARGETS - set(REPLACEMENTS))
            need(len(absent) == 13 and all(not os.path.lexists(W / name) for name in absent), 'exact13 original leaf absences')
            need(all(not os.path.lexists(W / 'public' / name) for name in context['new_dirs']), 'exact3 original directory absences')
            recovery = {'schema': 'gram-thompson-d4-durable-install-recovery-v1', 'replacement_backups': {name: context['old_files'][name[7:]] for name in REPLACEMENTS}, 'new_leaves_before': {name: 'ABSENT' for name in absent}, 'new_directories_before': {name: 'ABSENT' for name in sorted(context['new_dirs'])}, 'native_index_before': pin(context['old_index']), 'native_guards_before': context['guards']['native'], 'public_before': context['guards']['public'], 'recovery': 'STOP_AND_ROOT_REVIEW_NO_AUTOMATIC_ROLLBACK_OR_RETRY'}
            new_file(t / 'rollback.before.json', packed(recovery))
            new_file(t / 'preflight.before.json', packed(context['state']))
            sync_dir(staged)
            sync_dir(backups)
            sync_dir(t)
            event('ALL15_BUFFERS_2_RELATIVE_BACKUPS_13_LEAF_3_DIRECTORY_ABSENCES_AND_NATIVE_ROLLBACK_MATERIAL_DURABLE')
            check()
            need(preflight(p, False)['fingerprint'] == context['fingerprint'], 'whole repeat fence after durable staging before first website write')
            root_fd = os.open(W, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            stage_fd = os.open(staged, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            opened.extend([root_fd, stage_fd])

            def chain(name):
                fds = [os.dup(root_fd)]
                parents = []
                try:
                    for part in relative(name).parts[:-1]:
                        parents.append(part)
                        rel = '/'.join(parents)
                        created = False
                        check()
                        need(inode(W.lstat()) == inode(os.fstat(root_fd)), 'held website root identity')
                        if rel.startswith('public/') and rel[7:] in context['new_dirs'] and rel not in made:
                            need(not os.path.lexists(W / rel), 'exclusive necessary new directory')
                            event('MKDIR_INTENT', path=rel)
                            os.mkdir(part, 0o755, dir_fd=fds[-1])
                            os.fsync(fds[-1])
                            made[rel] = inode(os.stat(part, dir_fd=fds[-1], follow_symlinks=False))
                            created = True
                        child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fds[-1])
                        need(inode(os.fstat(child)) == inode(os.stat(part, dir_fd=fds[-1], follow_symlinks=False)), 'held live directory ancestor')
                        if rel in made:
                            need(inode(os.fstat(child)) == made[rel], 'same exclusively created directory')
                        if created:
                            os.fchmod(child, 0o755)
                            os.fsync(child)
                            event('MKDIR_COMPLETE', path=rel)
                        fds.append(child)
                    return fds
                except BaseException:
                    for fd in reversed(fds):
                        os.close(fd)
                    raise

            for index, name in enumerate(order):
                fds = chain(name)
                try:
                    check()
                    need(inode(W.lstat()) == inode(os.fstat(root_fd)), 'live website root immediately before mutation')
                    for level, part in enumerate(relative(name).parts[:-1]):
                        need(inode(os.stat(part, dir_fd=fds[level], follow_symlinks=False)) == inode(os.fstat(fds[level + 1])), 'live whole parent chain immediately before mutation')
                    need(inode(os.stat(str(index), dir_fd=stage_fd, follow_symlinks=False)) == inode(os.fstat(prepared[name])) and held(prepared[name]) == buffers[name], 'same whole held durable candidate')
                    event('LEAF_PUBLISH_INTENT', path=name, atomic_replacement=name in originals)
                    if name in originals:
                        need(inode(os.stat(Path(name).name, dir_fd=fds[-1], follow_symlinks=False)) == inode(os.fstat(originals[name])) and held(originals[name]) == read(backups / name), 'same held complete original and durable relative backup')
                        os.replace(str(index), Path(name).name, src_dir_fd=stage_fd, dst_dir_fd=fds[-1])
                    else:
                        if exclusive_rename(stage_fd, os.fsencode(str(index)), fds[-1], os.fsencode(Path(name).name), 4):
                            error = ctypes.get_errno()
                            raise OSError(error, os.strerror(error))
                    os.fsync(stage_fd)
                    os.fsync(fds[-1])
                    need(inode((W / name).lstat()) == inode(os.fstat(prepared[name])) and read(W / name) == buffers[name] and permissions(W / name) == '0644', 'published held identity/whole bytes0644')
                    completed.append(name)
                    event('LEAF_PUBLISH_COMPLETE', path=name)
                finally:
                    for fd in reversed(fds):
                        os.close(fd)
            check()
            verified = preflight(p, True)
            need(verified['old_index'] == context['old_index'] and not list(staged.iterdir()) and set(made) == {'public/' + name for name in context['new_dirs']}, 'native index unchanged; exact15 buffers/three dirs completed')
            check()
            result = {'schema': 'gram-thompson-d4-install-success-v1', 'status': 'FILESYSTEM_INSTALL_VERIFIED_SNAPSHOT', 'UTC': utc().isoformat(), 'bindings': authority['bindings'], 'counts': verified['state']['counts'], 'targets': sorted(TARGETS), 'authorization_SHA256': sha(authority['raw']), 'nonce': authority['data']['nonce'], 'runtime_root': str(RUN), 'transaction': str(t), 'installed_preflight_SHA256': verified['fingerprint'], 'W_native_HEAD_index_config_unchanged': True, 'Math_all_native_guards_unchanged': True, 'source_stage_audit_all_guards_unchanged': True, 'Git_object_ref_index_deploy_Sheet_changes': False, 'remote_read_snapshots_only': True, 'runtime_install_lock_retained': True, 'automatic_rollback_or_retry': False}
            new_file(t / 'SUCCESS.json', packed(result), 0o644)
            event('FILESYSTEM_INSTALL_SUCCESS', **result)
            return result
        except BaseException as error:
            event('STOPPED_PARTIAL_INSTALL_STATE_RETAINED', error=repr(error), completed_targets=completed, created_directories=made, automatic_rollback=False, automatic_retry=False)
            raise
        finally:
            for fd in reversed(opened):
                os.close(fd)
            os.close(lock_fd)



    def publish(context, authority):
        p, buffers = context['plan'], context['buffers']
        need(context['state']['installed'] and context['fingerprint'] == authority['data']['preflight_SHA256'], 'exact installed publication fingerprint')
        install_success(authority['data']['installation_SUCCESS'], p, authority['bindings'], authority['data']['nonce'])
        t, check, lock_fd = transaction('publish', authority)
        native_owner = None
        native_fd = None
        gitdir_fd = None
        ref_attempted = False
        pushed = False
        try:
            check()
            routing(p, context['state']['routing'])
            check()
            remote_parent(p, p['website_HEAD'])
            Math_remote_fence(p)
            native_backups(t / 'native-backups', context)
            new_file(t / 'preflight.before.json', packed(context['state']))
            native, commit_index = t / 'native-successor.index', t / 'commit.index'
            oids = {name: blob_oid(raw) for name, raw in buffers.items()}
            for name, raw in sorted(buffers.items()):
                check()
                need(git(p, 'hash-object', '--no-filters', '-w', '--stdin', data=raw).strip().decode() == oids[name], 'exact unfiltered frozen payload object')
            info = b''.join(('100644 ' + oids[name] + '\t' + name).encode() + b'\0' for name in sorted(buffers))
            check()
            new_file(native, native_successor(context['old_index'], oids), 0o600)
            check()
            git(p, 'read-tree', context['tree'], index=commit_index)
            check()
            git(p, 'update-index', '--add', '-z', '--index-info', data=info, index=commit_index)
            check()
            tree = git(p, 'write-tree', index=commit_index).strip().decode()
            staged = read(native)
            before, before_extension = index_entries(context['old_index'])
            after, after_extension = index_entries(staged)
            need(after_extension == unchanged_tree_for_targets(before_extension, {name.encode() for name in TARGETS}), 'exact target-ancestor TREE invalidations; every other cached node preserved')
            after_cache = cache_semantics(p, after, after_extension)
            targets = {name.encode() for name in TARGETS}
            need(len(after) == 58756 and set(after) == set(before) | targets and len(set(before) - targets) == 58741, 'exact58756 successor and58741 untargeted records')
            need(all(after[name] == record for name, record in before.items() if name not in targets), 'all58741 WHOLE raw stat/path/OID/mode/flag/padding records byte-exact')
            need(all(after[name.encode()][1:] == (struct.pack('>I', 0o100644), bytes.fromhex(oids[name])) for name in TARGETS), 'all15 successor target blob/mode semantics exact')
            need(all(after[name.encode()][0] == zero_stat_record(name.encode(), oids[name]) for name in TARGETS), 'all15 whole selected zero-stat/flags/name/OID/mode/NUL/padding buffers exact; no lstat-cache equality assumption')
            before_check, after_check = t / 'before-semantic.index', t / 'after-semantic.index'
            new_file(before_check, context['old_index'], 0o600)
            new_file(after_check, staged, 0o600)
            check()
            before_tree = git(p, 'write-tree', index=before_check).strip().decode()
            native_before = tree_entries(p, before_tree)
            check()
            native_tree = git(p, 'write-tree', index=after_check).strip().decode()
            native_after = tree_entries(p, native_tree)
            need(native_before == record_tree(before) and native_after == record_tree(after), 'complete raw path/OID/mode semantics equal separate private Git trees')
            need(read(native) == staged and read(W / '.git/index') == context['old_index'], 'TREE semantic rebuilds confined to checking copies; successor/live index untouched')
            parent_tree, commit_tree = tree_entries(p, context['tree']), tree_entries(p, tree)
            foreign_before = foreign_rows(native_before, parent_tree, targets)
            foreign_after = foreign_rows(native_after, commit_tree, targets)
            need(foreign_before == foreign_after, 'every foreign staging difference preserved relative to old and successor HEAD')
            need(set(commit_tree) == set(parent_tree) | targets and all(commit_tree[name] == record for name, record in parent_tree.items() if name not in targets), 'all untargeted HEAD tree leaves exact; only13 additions')
            delta = git(p, 'diff-tree', '--raw', '-r', '--no-commit-id', '--no-abbrev', '--no-renames', '--no-ext-diff', '-z', context['tree'], tree).split(b'\0')
            need(delta.pop() == b'' and len(delta) == 30 and {delta[index + 1] for index in range(0, 30, 2)} == targets, 'exact15-path commit delta')
            for index in range(0, 30, 2):
                header, name = delta[index].split(), delta[index + 1].decode()
                need(header[1] == b'100644' and header[3].decode() == oids[name] and header[4] == (b'M' if name in REPLACEMENTS else b'A'), 'exact13A2M frozen blob delta; no other path/action')
            maps = {'native_before': native_before, 'native_after': native_after, 'HEAD_before': parent_tree, 'HEAD_after': commit_tree}
            new_file(t / 'semantic-map-fingerprints.json', packed({key: {'records': len(value), 'SHA256': sha(packed(semantic_rows(value)))} for key, value in maps.items()}))
            for name, mapping in [('foreign-staging.before.json', foreign_before), ('foreign-staging.after.json', foreign_after)]:
                new_file(t / name, packed(foreign_serialized(mapping)))
            proof = {'schema': 'gram-thompson-d4-native-index-proof-v1', 'before_index': pin(context['old_index']), 'after_index': pin(staged), 'before_records': 58743, 'after_records': 58756, 'protected_whole_raw_records': 58741, 'selected_zero_stat_records': 15, 'before_TREE': pin(before_extension), 'after_TREE': pin(after_extension), 'before_TREE_payload': pin(before_extension[8:]), 'after_TREE_payload': pin(after_extension[8:]), 'before_TREE_semantics': context['cache_proof'], 'required_target_ancestor_proof': context['TREE_ancestor_proof'], 'after_TREE_semantics': after_cache, 'TREE_changed': before_extension != after_extension, 'private_before_semantic_tree': before_tree, 'private_after_semantic_tree': native_tree, 'parent_commit_tree': context['tree'], 'successor_commit_tree': tree, 'delta': '13A2M', 'foreign_staging_exact': True, 'all_untargeted_HEAD_tree_leaves_exact': True, 'no_broad_refresh_or_unknown_extension_waiver': True}
            new_file(t / 'native-index-proof.json', packed(proof))
            new_file(t / 'commit-delta.raw', b'\0'.join(delta) + b'\0')
            event('PRIVATE_INDEX_AND_EXACT15_COMMIT_TREE_PROVED', **proof)
            check()
            gitdir_fd = os.open(W / '.git', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            lock = W / '.git/index.lock'
            native_fd = os.open('index.lock', os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=gitdir_fd)
            native_owner = inode(os.fstat(native_fd))
            os.fchmod(native_fd, 0o644)
            write_all(native_fd, staged)
            os.fsync(native_fd)
            need(held(native_fd) == staged, 'whole durable native successor under exclusive held lock')
            os.fsync(gitdir_fd)
            event('NATIVE_INDEX_LOCKED_AND_SUCCESSOR_DURABLE', owner=native_owner)
            check()
            need(preflight(p, True, native_owner)['fingerprint'] == context['fingerprint'], 'full final source/stage/audit/public/native/Math fence under exclusive native-index lock')
            check()
            identity = {f'GIT_{role}_{key}': authority['data'][field] for role in ('AUTHOR', 'COMMITTER') for key, field in [('NAME', 'author_name'), ('EMAIL', 'author_email'), ('DATE', 'commit_date')]}
            commit = git(p, 'commit-tree', tree, '-p', p['website_HEAD'], data=(p['commit_message'] + '\n').encode(), identity=identity).strip().decode()
            need(re.fullmatch('[0-9a-f]{40}', commit), 'literal produced commit OID')
            body = git(p, 'cat-file', '-p', commit)
            header = body.split(b'\n\n', 1)[0].splitlines()
            need(header[0] == ('tree ' + tree).encode() and [line for line in header if line.startswith(b'parent ')] == [('parent ' + p['website_HEAD']).encode()], 'successor commit has exactly verified tree and single original parent')
            commit_time = timestamp(authority['data']['commit_date'])
            minutes = int(commit_time.utcoffset().total_seconds()) // 60
            zone = ('+' if minutes >= 0 else '-') + format(abs(minutes) // 60, '02d') + format(abs(minutes) % 60, '02d')
            identity_tail = (authority['data']['author_name'] + ' <' + authority['data']['author_email'] + '> ' + str(int(commit_time.timestamp())) + ' ' + zone).encode()
            need([line for line in header if line.startswith(b'author ')] == [b'author ' + identity_tail] and [line for line in header if line.startswith(b'committer ')] == [b'committer ' + identity_tail], 'actual commit author/committer/date exactly root supplied')
            need(body.split(b'\n\n', 1)[1] == (p['commit_message'] + '\n').encode(), 'actual commit message exact PLAN')
            new_file(t / 'commit-object.txt', body)
            new_file(t / 'commit-OID.txt', (commit + '\n').encode())
            event('COMMIT_OBJECT_CREATED', commit=commit, tree=tree)
            check()
            need(inode((W / '.git').lstat()) == inode(os.fstat(gitdir_fd)) and inode(lock.lstat()) == native_owner and held(native_fd) == staged and read(W / '.git/index') == context['old_index'], 'held Git directory/native lock and original index immediately before CAS')
            need(git(p, 'rev-parse', 'HEAD').strip().decode() == p['website_HEAD'], 'original parent immediately before CAS')
            native_fence(context['guards']['native'])
            check()
            event('CAS_MASTER_INTENT', old=p['website_HEAD'], new=commit)
            ref_attempted = True
            git(p, 'update-ref', p['branch'], commit, p['website_HEAD'])
            event('CAS_MASTER_COMPLETE', commit=commit)
            check()
            need(inode((W / '.git').lstat()) == inode(os.fstat(gitdir_fd)) and inode(lock.lstat()) == native_owner and held(native_fd) == staged and permissions(lock) == '0644', 'same held durable native-index lock immediately before replacement')
            os.replace('index.lock', 'index', src_dir_fd=gitdir_fd, dst_dir_fd=gitdir_fd)
            os.fsync(gitdir_fd)
            need(inode((W / '.git/index').lstat()) == native_owner, 'atomic target-only native-index successor identity')
            event('NATIVE_INDEX_ATOMIC_REPLACEMENT_COMPLETE', SHA256=sha(staged))

            def final_local():
                check()
                fresh = contract(p)
                native_fence(fresh['guards']['native'], successor=staged, commit=commit)
                public_fence(fresh, True)
                Math_remote_fence(p)
                W_aux_fence(p, commit, pushed)
                need(git(p, 'symbolic-ref', 'HEAD').strip().decode() == p['branch'] and git(p, 'rev-parse', p['branch']).strip().decode() == commit, 'master retained at exact successor commit')
                need(read(W / '.git/index') == staged and index_entries(read(W / '.git/index')) == (after, after_extension), 'complete successor index/raw record/extension equality after native publication')
                need(tree_entries(p, commit) == commit_tree and all(native_after[name] == commit_tree[name] for name in targets), 'published commit exact15 targets and protected tree')
                need(foreign_rows(record_tree(after), commit_tree, targets) == foreign_before and all(after[name] == before[name] for name in before if name not in targets), 'postpublication foreign staging and58741 whole records exact')
                need(not os.path.lexists(W / '.git/index.lock'), 'native index lock consumed only by own atomic replacement')

            final_local()
            check()
            routing(p, context['state']['routing'])
            check()
            remote_parent(p, p['website_HEAD'])
            check()
            need(git(p, 'rev-parse', p['branch']).strip().decode() == commit, 'exact local successor immediately before ordinary push')
            git(p, 'merge-base', '--is-ancestor', p['website_HEAD'], commit)
            check()
            event('ORDINARY_NONFORCE_EXPLICIT_SINGLE_REF_PUSH_INTENT', parent=p['website_HEAD'], commit=commit, branch=p['branch'])
            git(p, 'push', '--porcelain', '--no-follow-tags', '--recurse-submodules=no', 'origin', commit + ':' + p['branch'])
            pushed = True
            check()
            routing(p, context['state']['routing'])
            check()
            remote_parent(p, commit)
            Math_remote_fence(p)
            final_local()
            check()
            result = {'schema': 'gram-thompson-d4-publication-success-v1', 'status': 'SCOPED15_COMMIT_AND_PUSH_VERIFIED_SNAPSHOT', 'UTC': utc().isoformat(), 'bindings': authority['bindings'], 'authorization_SHA256': sha(authority['raw']), 'nonce': authority['data']['nonce'], 'installation_SUCCESS': authority['data']['installation_SUCCESS'], 'commit': commit, 'tree': tree, 'parent': p['website_HEAD'], 'branch': p['branch'], 'paths': 15, 'delta': '13A2M', 'protected_whole_raw_records': 58741, 'successor_index_records': 58756, 'index': {**pin(staged), 'mode': '0644'}, 'native_successor_semantic_tree': native_tree, 'TREE_before': pin(before_extension), 'TREE_after': pin(after_extension), 'foreign_staging_semantics_preserved': True, 'Math_all_native_guards_unchanged': True, 'stage_audit_sources_all_guards_unchanged': True, 'all_old803_public_buffers_retained_except2_planned_replacements': True, 'all_old387_directory_modes_hidden_empty_topology_retained': True, 'postpush_exact_remote_and_whole_local_verification': True, 'deployment_or_Sheet_or_AA_actions': False, 'runtime_publish_lock_retained': True, 'runtime_root': str(RUN), 'automatic_rollback_or_retry': False}
            new_file(t / 'SUCCESS.json', packed(result), 0o644)
            event('SCOPED15_PUBLICATION_SUCCESS', **result)
            return result
        except BaseException as error:
            event('STOPPED_PUBLICATION_STATE_RETAINED', error=repr(error), CAS_attempted=ref_attempted, push_returned_success=pushed, native_index_lock_owner=native_owner, automatic_rollback=False, automatic_retry=False)
            raise
        finally:
            if native_fd is not None:
                os.close(native_fd)
            if gitdir_fd is not None:
                os.close(gitdir_fd)
            os.close(lock_fd)



    class LocalLinks(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.links=[]
            self.canonicals=[]
            self.pdf=[]
        def handle_starttag(self,tag,attrs):
            values=dict(attrs)
            if tag in ('a','link','iframe'):
                value=values.get('href') if tag!='iframe' else values.get('src')
                if value:
                    self.links.append(value)
            if tag=='link' and values.get('rel')=='canonical':
                self.canonicals.append(values.get('href'))
            if tag=='meta' and values.get('name')=='citation_pdf_url':
                self.pdf.append(values.get('content'))

    def local_target_links(context):
        for name,raw in context['buffers'].items():
            if not name.endswith('/index.html') or name in REPLACEMENTS:
                continue
            relative_path=Path(name[7:])
            canonical='https://aleckriebel.com/'+relative_path.parent.as_posix()+'/'
            parser=LocalLinks()
            parser.feed(raw.decode())
            need(parser.canonicals==[canonical] and len(parser.pdf)==1 and parser.pdf[0].startswith(canonical),'actual unique local canonical/Scholar PDF')
            for target in parser.links+parser.pdf:
                if target.startswith('#') or target.startswith(('mailto:','https://doi.org/','https://zenodo.org/','https://orcid.org/','https://github.com/','https://arxiv.org/','https://easychair.org/')):
                    continue
                if target.startswith('https://aleckriebel.com/'):
                    path=W/'public'/target.removeprefix('https://aleckriebel.com/').split('#',1)[0]
                elif target.startswith('https://'):
                    continue
                elif target.startswith('/'):
                    path=W/'public'/target.lstrip('/').split('#',1)[0]
                else:
                    path=W/'public'/relative_path.parent/target.split('#',1)[0]
                safe(path)
                need(path.is_file() or path.is_dir() and (path/'index.html').is_file(),'actual projected/installed local link target')
        return True

    def committed_success(row,p,a):
        path=Path(row['path'])
        need(path.name=='SUCCESS.json' and path.parent.parent==RUN/'commit' and re.fullmatch('[0-9a-f]{64}',path.parent.name),'this effort exact commit/push SUCCESS')
        result=strict_json(bound(row))
        need(result['schema']=='gram-thompson-d4-publication-success-v1' and result['status']=='SCOPED15_COMMIT_AND_PUSH_VERIFIED_SNAPSHOT','actual completed scoped commit/push')
        need(result['bindings']==bindings(p) and result['parent']==p['website_HEAD'] and result['paths']==15 and result['delta']=='13A2M','same exact new helper/PLAN/overlay/parent')
        need(result['protected_whole_raw_records']==58741 and result['successor_index_records']==58756 and result['nonce']!=a['nonce'],'whole current raw-record proof and distinct deploy nonce')
        need(result['authorization_SHA256']==path.parent.name and result['runtime_root']==str(RUN),'exact current commit evidence transaction/runtime')
        original=read(path.parent/'authorization.json')
        need(sha(original)==result['authorization_SHA256'] and strict_json(original)['mode']=='commit','retained actual commit authority')
        index=read(path.parent/'native-successor.index')
        need(pin(index)=={k:result['index'][k] for k in ('bytes','SHA256')} and permissions(path.parent/'native-successor.index')=='0600' and result['index']['mode']=='0644','whole private0600 successor buffer equals actual native0644 index bytes')
        return result,index

    def bounded_live_get(opener,request,expected,stem):
        # This ordinary main-thread Unix timer requires SIGALRM unblocked.
        # No uninterruptible-OS, SIGKILL/power-loss or hard-real-time guarantee.
        need(signal.getitimer(signal.ITIMER_REAL)==(0.0,0.0),'no inherited real timer to replace')
        need(callable(getattr(signal,'pthread_sigmask',None)) and hasattr(signal,'SIG_BLOCK'),'POSIX signal-mask inspection required before live GET')
        # SIG_BLOCK with an empty set inspects without changing inherited masks.
        need(signal.SIGALRM not in signal.pthread_sigmask(signal.SIG_BLOCK,set()),'live GET requires inherited SIGALRM unblocked; no mask changes')
        previous_handler=signal.getsignal(signal.SIGALRM)
        body_path=Path(str(stem)+'.body')
        body_fd=os.open(body_path,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        os.fchmod(body_fd,0o600)
        sync_dir(body_path.parent)
        limit=len(expected)+1
        response=None
        response_fields={}
        exception=None
        received=0
        def expired(signum,frame):
            raise TimeoutError('single live GET total60second deadline expired')
        started=time.monotonic()
        try:
            signal.signal(signal.SIGALRM,expired)
            signal.setitimer(signal.ITIMER_REAL,60.0)
            try:
                response=opener.open(request,timeout=60)
            except urllib.error.HTTPError as error:
                response=error
            response_fields={'URL':response.geturl(),'status':response.status,'headers':list(response.headers.raw_items())}
            while received<limit:
                requested=min(65536,limit-received)
                block=response.read1(requested)
                need(len(block)<=requested,'bounded one-read response size')
                if not block:
                    break
                write_all(body_fd,block)
                received+=len(block)
                need(time.monotonic()-started<60.0,'single live GET total elapsed bound')
            need(time.monotonic()-started<60.0,'single live GET completed within total deadline')
        except BaseException as error:
            exception={'type':type(error).__name__,'repr':repr(error),'traceback':traceback.format_exc()}
            raise
        finally:
            signal.setitimer(signal.ITIMER_REAL,0.0)
            signal.signal(signal.SIGALRM,previous_handler)
            try:
                if response is not None:
                    response.close()
            finally:
                try:
                    os.fsync(body_fd)
                    body=held(body_fd)
                finally:
                    os.close(body_fd)
                metadata={'requested_URL':request.full_url,**response_fields,'maximum_body_bytes':limit,'total_deadline_seconds':60,'elapsed_seconds':time.monotonic()-started,'body':pin(body),'exception':exception,'automatic_retry':False}
                new_file(Path(str(stem)+'.headers.json'),packed(metadata))
                event('SINGLE_LIVE_TARGET_GET_RETURN' if exception is None else 'SINGLE_LIVE_TARGET_GET_EXCEPTION',**metadata)
        return response_fields['status'],response_fields['URL'],body

    def deploy(context,authority):
        p,a=context['plan'],authority['data']
        result,index=committed_success(a['commit_SUCCESS'],p,a)
        commit=result['commit']
        need(re.fullmatch('[0-9a-f]{40}',commit),'actual successor commit OID')
        def fence():
            current_authority(authority)
            fresh=contract(p)
            native_fence(fresh['guards']['native'],successor=index,commit=commit)
            W_aux_fence(p,commit,True)
            Math_remote_fence(p)
            public_fence(fresh,True)
            need(git(p,'symbolic-ref','HEAD').strip().decode()==p['branch'] and git(p,'rev-parse','HEAD').strip().decode()==commit,'actual postcommit HEAD, not baseline preflight')
            need(read(W/'.git/index')==index and not os.path.lexists(W/'.git/index.lock'),'exact full postcommit index and no stale native lock')
            need(git(p,'rev-parse',commit+'^{tree}').strip().decode()==result['tree'],'actual exact published commit tree')
            remote_parent(p,commit)
            routing(p)
            local_target_links(fresh)
            return fresh
        fence()
        hosting=strict_json(bound(a['hosting_before']))
        need(packed(hosting)==packed(a['hosting_before_semantics']),'whole actual fresh root hosting-before record')
        need(hosting['root_verified_fresh_hosting_and_rollback_baseline'] is True and hosting['project_id']=='aleckriebel-bd92e' and isinstance(hosting['hosting_version'],str) and hosting['hosting_version'],'root actual prior hosting version, retained for separate rollback disposition')
        observed=timestamp(hosting['observed_UTC'])
        need(0 <= (utc()-observed).total_seconds() <= 900,'fresh hosting baseline, no stale version reuse')
        need(a['rollback_automatic_authority'] is False,'no automatic hosting rollback')
        invocation=a['firebase_invocation']
        argv=invocation['argv']
        pins=invocation['executable_pins']
        need(isinstance(pins,list) and len(pins) in (1,2),'only exact existing CLI or Node+CLI prefix')
        for executable in pins:
            bound(executable)
        need(invocation['entrypoint_fully_read_and_existing_environment_only'] is True and invocation['single_ordinary_hosting_command'] is True,'actual root existing entrypoint/environment read')
        suffix=['deploy','--only','hosting','--project','aleckriebel-bd92e','--non-interactive']
        need(argv==[row['path'] for row in pins]+suffix,'closed ordinary hosting argv, no arbitrary executable flags/subcommands')
        need(Path(pins[-1]['path']).name in ('firebase','firebase.js') and (len(pins)==1 or Path(pins[0]['path']).name in ('node','nodejs')),'actual existing Firebase CLI entrypoint, optional ordinary Node binary')
        new_file(CURRENT['root']/'hosting-before.json',packed(hosting))
        event('ONE_ORDINARY_HOSTING_DEPLOY_INTENT',argv=argv,commit=commit,prior_hosting_version=hosting['hosting_version'],automatic_rollback=False)
        env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
        def launch_gate():
            current_authority(authority)
            need(authority['issued']<=utc()<authority['expiry'],'still unexpired after all launch-authority reads and immediately before subprocess')
        code,stdout,stderr=command(argv,cwd=W,env=env,before_launch=launch_gate)
        need(code==0,'hosting deploy command failed; literal streams and partial remote state retained')
        fence()
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self,req,fp,code,msg,headers,newurl):
                return None
        opener=urllib.request.build_opener(NoRedirect())
        live=[]
        mkdir_exclusive(CURRENT['root']/'live',0o700)
        for number,(name,expected) in enumerate(sorted(context['buffers'].items()),1):
            current_authority(authority)
            path=name[7:]
            public_path=path[:-len('index.html')] if path.endswith('/index.html') else path
            url='https://aleckriebel.com/'+urllib.parse.quote(public_path,safe='/')
            request=urllib.request.Request(url,headers={'Cache-Control':'no-cache','User-Agent':'AlecKriebel-private-release-verification'})
            event('SINGLE_LIVE_TARGET_GET_INTENT',url=url)
            stem=CURRENT['root']/'live'/format(number,'02d')
            status,actual_url,body=bounded_live_get(opener,request,expected,stem)
            need(status==200 and actual_url==url and body==expected,'first live target response mismatch; no retry or cache loop')
            live.append({'path':name,'URL':url,**pin(body)})
        fence()
        success={'schema':'gram-thompson-d4-hosting-success-v1','status':'ONE_HOSTING_DEPLOY_AND15_LIVE_BUFFERS_VERIFIED_SNAPSHOT','UTC':utc().isoformat(),'bindings':bindings(p),'authorization_SHA256':sha(authority['raw']),'nonce':a['nonce'],'commit_SUCCESS':a['commit_SUCCESS'],'commit':commit,'prior_hosting_version':hosting['hosting_version'],'live':live,'W_native_public_and_M_all_siblings_docs_preserved':True,'automatic_rollback_or_retry':False,'Sheet_AA_redirect_actions':False,'UI_mobile_PDF_rendering_or_future_persistence_certificate':False}
        new_file(CURRENT['root']/'SUCCESS.json',packed(success),0o600)
        event('HOSTING_SNAPSHOT_SUCCESS',**success)
        return success

    def require_preflight(a,p):
        row=a['preflight_SUCCESS']
        path=Path(row['path'])
        need(path.name=='SUCCESS.json' and path.parent.parent==RUN/'preflight','this effort actual single preflight receipt')
        actual=strict_json(bound(row))
        need(actual['schema']=='gram-thompson-d4-preflight-success-v1' and actual['bindings']==bindings(p) and actual['preflight_SHA256']==a['preflight_SHA256'] and actual['nonce']!=a['nonce'],'exact actual previous preflight and separate stage nonce')
        return actual

    def main():
        mode=sys.argv[1][2:]
        p=load_plan()
        authority=authorization(mode,p)
        open_runtime(mode,authority)
        if mode=='deploy':
            context=contract(p)
            result=deploy(context,authority)
        else:
            installed=mode=='commit'
            context=preflight(p,installed)
            current_authority(authority)
            if mode=='stage':
                require_preflight(authority['data'],p)
                result=install(context,authority)
            elif mode=='commit':
                result=publish(context,authority)
            else:
                result={'schema':'gram-thompson-d4-preflight-success-v1','status':'READONLY_W_M_PREFLIGHT_VERIFIED_SNAPSHOT','UTC':utc().isoformat(),'bindings':bindings(p),'preflight_SHA256':context['fingerprint'],'state':context['state'],'authorization_SHA256':sha(authority['raw']),'nonce':authority['data']['nonce'],'W_Git_index_ref_public_mutations':False,'private_ignored_capture_only':True}
                new_file(CURRENT['root']/'SUCCESS.json',packed(result),0o600)
                event('READONLY_PREFLIGHT_SUCCESS',**result)
        print(json.dumps({'status':result['status'],'mode':mode,'private_evidence':str(CURRENT['root']),'automatic_retry':False,'Sheet_AA_redirect_actions':False},sort_keys=True))

    try:
        main()
    except BaseException as error:
        failure=traceback.format_exc().encode()
        if CURRENT is not None:
            try:
                new_file(CURRENT['root']/'FAILURE.txt',failure)
                event('STOPPED_STATE_RETAINED',error=repr(error),automatic_rollback=False,automatic_retry=False)
            except BaseException:
                pass
            print(json.dumps({'status':'STOPPED_STATE_RETAINED','private_evidence':str(CURRENT['root']),'automatic_rollback':False,'automatic_retry':False}),file=sys.stderr)
        else:
            print(json.dumps({'status':'STOPPED_BEFORE_PRIVATE_CAPTURE','error':repr(error),'opaque_commands_executed':0,'automatic_retry':False}),file=sys.stderr)
        raise SystemExit(1)
    finally:
        if LOG is not None:
            LOG.close()
        if CURRENT is not None:
            os.close(CURRENT['lock_fd'])

if __name__ == '__main__':
    _run_explicit_mode()
