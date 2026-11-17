#!/usr/bin/env python3
"""Fresh fixed11 production preparation. ALL MODES UNEXECUTED at authoring.

The literal default precedes data/environment access. Import defines functions
and constants only. Active modes require separate exact root authorities.
Failure retains evidence, locks and partial state; no retry or rollback exists.
"""
import sys

if __name__ == '__main__' and len(sys.argv) == 1:
    print('{"status":"NO_ACTION_EXPLICIT_ROOT_MODE_REQUIRED","filesystem_data_reads":0,"repository_reads":0,"writes":0,"Git_commands":0,"remote_calls":0,"authority_inferred":false}')
    raise SystemExit(0)

def _run_explicit_mode():
    from pathlib import Path
    import base64
    import ctypes
    import datetime
    import hashlib
    import json
    import os
    import re
    import stat
    import struct
    import subprocess
    import xml.etree.ElementTree as ET

    P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
    M = P.parent
    N = P / 'verification/radial-tree-production-preparation-sol-20261117'
    RUN = P / 'verification/radial-tree-runtime-sol-20261117'
    W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
    S = P / 'verification/radial-tree-stage-sol-20261117'
    A = P / 'verification/radial-tree-stage-implementation-audit-sol-20261117'
    PLAN_SHA = 'd3ee52565eb3658d51f15aad5e2f930abc38c772ff8c0f1c0e8cc88edf342516'
    TARGETS = frozenset({
        'public/research/designed-tree-congestion-fragmentation/assets/congestion-fragmentation-verification.zip',
        'public/research/designed-tree-congestion-fragmentation/assets/congestion-fragmentation.pdf',
        'public/research/designed-tree-congestion-fragmentation/citation.bib',
        'public/research/designed-tree-congestion-fragmentation/index.html',
        'public/research/index.html',
        'public/research/radial-orthogonality-dual-conformal-flatness/assets/SHA256SUMS.txt',
        'public/research/radial-orthogonality-dual-conformal-flatness/assets/paper.pdf',
        'public/research/radial-orthogonality-dual-conformal-flatness/assets/source-and-verification.zip',
        'public/research/radial-orthogonality-dual-conformal-flatness/citation.bib',
        'public/research/radial-orthogonality-dual-conformal-flatness/index.html',
        'public/research/sitemap.xml',
    })
    REPLACEMENTS = ['public/research/index.html', 'public/research/sitemap.xml']
    LOG = None
    TRACE = []


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


    def strict_json(raw):
        return json.loads(raw, object_pairs_hook=unique_pairs)


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


    def event(phase, **values):
        record = {'UTC': utc().isoformat(), 'phase': phase, **values}
        if LOG is None:
            TRACE.append(record)
        else:
            LOG.write(packed(record))
            LOG.flush()
            os.fsync(LOG.fileno())


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
        dictionary_form = set(snapshot) == {'root', 'root_mode', 'files', 'directories'}
        need(dictionary_form or set(snapshot) == {'root', 'root_mode', 'files', 'directories', 'regular_files', 'child_directories'}, 'complete actual dictionary or canonical row snapshot')
        need(isinstance(snapshot['root'], str) and Path(snapshot['root']).is_absolute(), 'explicit snapshot root identity')
        files, directories = [], []
        if dictionary_form:
            need(isinstance(snapshot['files'], dict) and isinstance(snapshot['directories'], dict), 'actual source snapshots use dictionaries')
            for name, row in snapshot['files'].items():
                relative(name)
                files.append({'path': name, **canonical_pin(row)})
            for name, value in snapshot['directories'].items():
                relative(name)
                directories.append({'path': name, 'mode': mode_value(value)})
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
            need(type(snapshot['regular_files']) is int and type(snapshot['child_directories']) is int and snapshot['regular_files'] == len(files) and snapshot['child_directories'] == len(directories), 'exact canonical snapshot counts')
        names, dirs = {r['path'] for r in files}, {r['path'] for r in directories}
        need(len(names) == len(files) and len(dirs) == len(directories) and not names & dirs, 'unique disjoint complete snapshot paths')
        for name in names | dirs:
            parent = Path(name).parent.as_posix()
            need(parent == '.' or parent in dirs, 'complete parent topology including hidden and empty directories')
        return {'root': snapshot['root'], 'root_mode': mode_value(snapshot['root_mode']), 'files': sorted(files, key=lambda r: r['path']), 'directories': sorted(directories, key=lambda r: r['path']), 'regular_files': len(files), 'child_directories': len(directories)}


    def tables(snapshot):
        normalized = normalize_snapshot(snapshot)
        return ({row['path']: {key: row[key] for key in ('bytes', 'SHA256', 'mode')} for row in normalized['files']}, {row['path']: row['mode'] for row in normalized['directories']})


    def whole_snapshot(expected):
        normalized = normalize_snapshot(expected)
        need(census(Path(normalized['root'])) == normalized, 'whole namespace root/bytes/modes/topology: ' + normalized['root'])


    def authenticate_manifest(root, manifest, final_pin, manifest_pin, family):
        terminals = {'FINAL.json': final_pin, 'OWNED_MANIFEST.json': manifest_pin}
        names, files = set(), []
        if family == 'stage':
            need(manifest['schema'] == 'finite-private-stage-owned-manifest-v1' and manifest['root'] == str(root) and mode_value(manifest['root_mode']) == '0755', 'actual stage manifest identity')
            need(sorted(manifest['exact_terminal_exclusions']) == sorted(terminals) and manifest['all_hidden_ignored_empty_files_and_modes_included'] is True and manifest['no_future_or_subtree_exclusions'] is True, 'stage omits exact two terminal rows only')
            for row in manifest['files']:
                need(set(row) == {'path', 'bytes', 'SHA256', 'mode'} and row['path'] not in terminals and row['path'] not in names, 'unique fully pinned stage member')
                names.add(row['path'])
                files.append({'path': row['path'], **canonical_pin({k: row[k] for k in ('bytes', 'SHA256', 'mode')})})
            files.extend({'path': name, **{k: value[k] for k in ('bytes', 'SHA256', 'mode')}} for name, value in terminals.items())
            count, dirs = 804, 380
        else:
            need(family == 'audit' and manifest['schema'] == 'finite-radial-tree-stage-implementation-audit-manifest-v1' and manifest['owned_root'] == str(root), 'actual implementation-audit manifest identity')
            need((manifest['regular_files'], manifest['child_directories'], manifest['root_mode']) == (11, 0, '0755') and manifest['symlinks'] == manifest['special_objects'] == 0, 'actual audit finite counts/modes')
            need(sorted(manifest['exact_terminal_recursive_hash_exclusions']) == sorted(str(root / name) for name in terminals) and manifest['other_exclusions'] == [] and manifest['no_future_subtree_or_basename_exclusions'] is True, 'audit exact two included terminal control rows only')
            for row in manifest['files']:
                name = row['path']
                need(name not in names, 'unique audit member')
                names.add(name)
                if name in terminals:
                    need(row == {'path': name, 'mode': '0644', 'terminal_control': True}, 'actual included audit terminal-control row')
                    files.append({'path': name, **{k: terminals[name][k] for k in ('bytes', 'SHA256', 'mode')}})
                else:
                    need(set(row) == {'path', 'bytes', 'SHA256', 'mode'}, 'whole audit member schema')
                    files.append({'path': name, **canonical_pin({k: row[k] for k in ('bytes', 'SHA256', 'mode')})})
            need(set(terminals) <= names, 'both audit terminal-control rows present')
            count, dirs = 11, 0
        expected = normalize_snapshot({'root': str(root), 'root_mode': '0755', 'files': files, 'directories': manifest['directories'], 'regular_files': count, 'child_directories': dirs})
        whole_snapshot(expected)
        return expected


    def normalized_native(native, p):
        need(set(native) == {'M', 'W'}, 'exact accepted Math/website native roots')
        result = []
        for key, root, branch in [('M', M, 'refs/heads/main'), ('W', W, 'refs/heads/master')]:
            item = native[key]
            need(set(item) == {'files', 'HEAD', 'resolved_local_HEAD', 'local_heads', 'packed_local_head_lines', 'packed_refs_mode'} and set(item['files']) == {'HEAD', 'index', 'config'}, 'actual native-control dictionary schema')
            need(item['HEAD'] == 'ref: ' + branch and item['resolved_local_HEAD'] == (p['Math_native_main'] if root == M else p['website_HEAD']), 'accepted current native branch and resolution')
            heads = {}
            for line in item['packed_local_head_lines']:
                match = re.fullmatch('([0-9a-f]{40}) (refs/heads/[^ ]+)', line)
                need(match is not None and match[2] not in heads, 'unique raw packed local-head lines')
                heads[match[2]] = {'OID': match[1], 'raw_line': line}
            row = {'root': str(root), **{leaf: canonical_pin(item['files'][leaf]) for leaf in ('HEAD', 'index', 'config')}, 'local_branch': branch, 'local_branch_OID': item['resolved_local_HEAD'], 'loose_local_heads': normalize_snapshot(item['local_heads']), 'packed_local_heads': heads, 'packed_refs_mode': mode_value(item['packed_refs_mode']), 'remote_tracking_FETCH_HEAD_and_nonlocal_packed_lines_deliberately_not_bound': True}
            row['HEAD']['raw'] = item['HEAD'] + '\n'
            need(row['HEAD']['bytes'] == len(row['HEAD']['raw'].encode()) and row['HEAD']['SHA256'] == sha(row['HEAD']['raw'].encode()), 'actual raw native symbolic HEAD binding')
            if root == W:
                need(row['index'] == {k: p['website_index'][k] for k in ('bytes', 'SHA256', 'mode')}, 'accepted current website index full pin')
            result.append(row)
        return result

    def load_plan():
        need(Path(__file__).absolute() == N / 'release_two.py', 'fixed fresh helper location')
        raw = read(N / 'PLAN.json')
        need(sha(raw) == PLAN_SHA and permissions(N / 'PLAN.json') == '0644', 'exact fresh PLAN bytes/mode')
        p = strict_json(raw)
        need(p['schema'] == 'fixed-radial-tree-two-page11-production-preparation-v1', 'actual fresh PLAN schema')
        fixed = {'project': str(P), 'Math': str(M), 'website': str(W), 'preparation_root': str(N), 'runtime_root': str(RUN), 'stage_root': str(S), 'audit_root': str(A), 'helper_name': 'release_two.py', 'branch': 'refs/heads/master', 'website_HEAD': '96f04aa5544df69daba07a9ed4d6212172e9984a', 'origin': 'https://github.com/AlecKriebel/aleckriebel.com.git', 'git_binary': '/usr/bin/git', 'author_name': 'Alec Kriebel', 'author_email': 'me@aleckriebel.com'}
        need(all(p[key] == value for key, value in fixed.items()), 'current fixed roots/parent/transport/author')
        need(p['scope_paths'] == sorted(TARGETS) and p['replacement_paths'] == REPLACEMENTS, 'literal exact11 scope')
        need((p['paths'], p['new_leaves'], p['replacements']) == (11, 9, 2) and p['rows'] == [184, 185] and p['record_ids'] == [22983519, 23527793], 'exact11/9A2M rows and records')
        need(permissions(N / 'release_two.py') == '0644', 'fresh ordinary0644 helper')
        return p

    def bindings(p):
        return {'helper': {'path': str(N / 'release_two.py'), **row_for(N / 'release_two.py')}, 'PLAN': {'path': str(N / 'PLAN.json'), **row_for(N / 'PLAN.json')}, 'controls': p['controls'], 'record_ids': p['record_ids'], 'scope_paths': p['scope_paths'], 'runtime_root': str(RUN), 'website_HEAD': p['website_HEAD'], 'website_index': p['website_index'], 'Math_native_main': p['Math_native_main'], 'stage_adoption_semantics': p['root_stage_adoption_semantics']}


    def timestamp(value):
        need(isinstance(value, str), 'literal time string')
        result = datetime.datetime.fromisoformat(value)
        need(result.utcoffset() is not None, 'timezone-qualified time')
        return result


    def helper_review(review, current_bindings):
        keys = {'audit_FINAL', 'actual_schema_present', 'actual_schema', 'actual_status_present', 'actual_status', 'root_personally_read_complete_helper_PLAN_and_audit', 'root_adopts_all_findings_for_exact_current_helper_PLAN', 'root_resolution'}
        need(set(review) == keys, 'explicit actual independent helper audit and root semantic disposition')
        row = review['audit_FINAL']
        path = Path(row['path'])
        need(path.name == 'FINAL.json' and path.is_relative_to(P / 'verification') and not any(path.is_relative_to(root) for root in (N, RUN, S, A)), 'actual distinct independent helper audit FINAL location')
        audit = strict_json(bound(row))
        need(isinstance(audit, dict), 'actual helper audit object')
        for key in ('schema', 'status'):
            present = review['actual_' + key + '_present']
            need(type(present) is bool and (key in audit) == present, 'actual helper audit field presence: ' + key)
            need(review['actual_' + key] == (audit[key] if present else None), 'actual helper audit literal field: ' + key)
        need(review['root_personally_read_complete_helper_PLAN_and_audit'] is True and review['root_adopts_all_findings_for_exact_current_helper_PLAN'] is True, 'root personally adopts actual helper-audit findings')
        resolution = review['root_resolution']
        need(set(resolution) == {'classification', 'rationale', 'helper', 'PLAN'} and resolution['classification'] == 'ALL_STATIC_FINDINGS_RESOLVED_FOR_EXACT_ACTION', 'explicit root helper-audit disposition')
        need(isinstance(resolution['rationale'], str) and resolution['rationale'].strip(), 'root supplies actual resolution rationale')
        need(resolution['helper'] == current_bindings['helper'] and resolution['PLAN'] == current_bindings['PLAN'], 'root semantic adoption binds current complete code and PLAN')


    def authorization(kind, p, phase):
        path = Path(p['authority_paths'][kind])
        expected_path = P / ('verification/root-radial-tree-' + ('readonly' if kind == 'readonly' else kind) + '-authorization-20261117.json')
        need(path == expected_path, 'fixed root authority path')
        raw = read(path)
        need(permissions(path) == '0644', 'root authority0644')
        a = strict_json(raw)
        b = bindings(p)
        action = {'readonly': 'READONLY_EXACT11_PREFLIGHT', 'install': 'INSTALL_EXACT11_FILESYSTEM', 'publish': 'PUBLISH_EXACT11_GIT'}[kind]
        fixed = {'schema': p['authority_schema'], 'action': action, 'phase': phase, 'bindings': b, 'concurrency': 'ROOT_SERIALIZED_NO_OTHER_W_WRITER', 'root_asserts_nonce_fresh': True, 'root_asserts_no_other_W_writer': True, 'deployment_authorized': False, 'Sheet_authorized': False, 'AA': None, 'follow_up': None}
        extras = {'issued_UTC', 'expires_UTC', 'nonce'}
        extras |= {'request_fingerprint_SHA256'} if kind == 'readonly' else {'preflight_SHA256', 'helper_review'}
        if kind == 'publish':
            extras |= {'installation_SUCCESS', 'author_name', 'author_email', 'commit_date'}
        need(set(a) == set(fixed) | extras and all(a[key] == value for key, value in fixed.items()), 'exact separate current root action authority')
        issued, expiry = timestamp(a['issued_UTC']), timestamp(a['expires_UTC'])
        need(issued <= utc() < expiry and 0 < (expiry - issued).total_seconds() <= p['authority_max_lifetime_seconds'] == 3600, 'currently issued short expiring root authority')
        need(isinstance(a['nonce'], str) and re.fullmatch('[0-9a-f]{64}', a['nonce']), 'fresh root64hex nonce')
        if kind == 'readonly':
            request = {'bindings': b, 'phase': phase, 'nonce': a['nonce']}
            need(a['request_fingerprint_SHA256'] == sha(packed(request)), 'exact current root readonly request fingerprint')
        else:
            need(isinstance(a['preflight_SHA256'], str) and re.fullmatch('[0-9a-f]{64}', a['preflight_SHA256']), 'explicit current preflight fingerprint')
            helper_review(a['helper_review'], b)
        if kind == 'publish':
            for key in ('author_name', 'author_email', 'commit_date'):
                need(isinstance(a[key], str) and a[key] and a[key] == a[key].strip() and not any(ord(char) < 32 or ord(char) == 127 for char in a[key]), 'literal root commit identity/date')
            need(a['author_name'] == p['author_name'] and a['author_email'] == p['author_email'], 'fixed actual Alec Kriebel author and committer identity')
            need('<' not in a['author_name'] and '>' not in a['author_name'] and '<' not in a['author_email'] and '>' not in a['author_email'], 'unambiguous root author identity')
            commit_time = timestamp(a['commit_date'])
            need(commit_time.microsecond == 0 and int(commit_time.utcoffset().total_seconds()) % 60 == 0, 'whole-second commit date with minute timezone offset')
            install_success(a['installation_SUCCESS'], p, b, a['nonce'])
        return {'path': path, 'raw': raw, 'data': a, 'issued': issued, 'expiry': expiry, 'bindings': b}


    def current_authority(authority):
        need(read(authority['path']) == authority['raw'] and permissions(authority['path']) == '0644', 'same literal current authority')
        need(authority['issued'] <= utc() < authority['expiry'], 'unexpired current root authority')
        need(bindings(load_plan()) == authority['bindings'], 'exact current helper/PLAN/control bindings')


    def install_success(row, p, current_bindings, publish_nonce):
        path = Path(row['path'])
        need(path.name == 'SUCCESS.json' and path.parent.parent == RUN / 'install' and re.fullmatch('[0-9a-f]{64}', path.parent.name), 'this fresh effort installation SUCCESS only')
        result = strict_json(bound(row))
        need(result['schema'] == 'radial-tree-install-success-v1' and result['status'] == 'FILESYSTEM_INSTALL_VERIFIED_SNAPSHOT', 'completed exact11 installation snapshot')
        need(result['bindings'] == current_bindings and result['counts'] == [781, 377, 128, 129] and result['targets'] == sorted(TARGETS), 'installed exact current payloads and counts')
        need(result['authorization_SHA256'] == path.parent.name and result['nonce'] != publish_nonce and result['runtime_root'] == str(RUN), 'separate publish nonce and current install transaction')
        install_raw = read(path.parent / 'authorization.json')
        need(sha(install_raw) == result['authorization_SHA256'], 'retained exact original install authority')
        installed_authority = strict_json(install_raw)
        need(installed_authority['action'] == 'INSTALL_EXACT11_FILESYSTEM' and installed_authority['nonce'] == result['nonce'] and installed_authority['bindings'] == current_bindings, 'original distinct installation action binding')
        lock = strict_json(read(RUN / 'ACTIVE_INSTALL.lock'))
        need(lock['authorization_SHA256'] == result['authorization_SHA256'] and lock['nonce'] == result['nonce'] and lock['action'] == installed_authority['action'], 'retained current runtime install lock')
        need(permissions(RUN) == '0700' and permissions(RUN / 'install') == '0700' and permissions(path.parent) == '0700', 'private fresh runtime modes')
        return result


    def git(p, *args, data=None, index=None, identity=None, opaque=False, absent_vcs=False):
        env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
        env.update(GIT_OPTIONAL_LOCKS='0', GIT_INDEX_VERSION='2', GIT_TERMINAL_PROMPT='0', GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1')
        if index is not None:
            need(index.is_relative_to(RUN), 'only this fresh runtime private Git index')
            env['GIT_INDEX_FILE'] = str(index)
        if identity is not None:
            env.update(identity)
        options = ['-c', 'core.hooksPath=/dev/null', '-c', 'core.fsmonitor=false', '-c', 'core.untrackedCache=false', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false', '-c', 'commit.gpgsign=false', '-c', 'core.splitIndex=false', '-c', 'index.version=2', '-c', 'core.sparseCheckout=false', '-c', 'index.sparse=false', '-c', 'remote.origin.mirror=false', '-c', 'protocol.allow=never', '-c', 'protocol.https.allow=always']
        command = [p['git_binary'], '--no-optional-locks', *options, *args]
        result = subprocess.run(command, cwd=W, env=env, input=data, capture_output=True)
        event('Git', argv=command, input_SHA256=None if data is None else sha(data), exit=result.returncode, stdout_SHA256=sha(result.stdout), stderr_SHA256=sha(result.stderr), stdout_base64=None if opaque else base64.b64encode(result.stdout).decode(), stderr_base64=base64.b64encode(result.stderr).decode())
        absent = absent_vcs and args == ('config', '--null', '--get-all', 'remote.origin.vcs') and result.returncode == 1 and result.stdout == b'' and result.stderr == b''
        need(result.returncode == 0 or absent, 'Git failed: ' + args[0])
        return result.stdout


    def routing(p, expected=None):
        query = ('config', '--null', '--show-origin', '--show-scope', '--get-regexp', p['routing_config_key_regex'])
        before = git(p, *query, opaque=True)
        selector = git(p, 'config', '--null', '--get-all', 'remote.origin.vcs', opaque=True, absent_vcs=True)
        fetch = git(p, 'remote', 'get-url', '--all', 'origin', opaque=True)
        push = git(p, 'remote', 'get-url', '--push', '--all', 'origin', opaque=True)
        after = git(p, *query, opaque=True)
        intended = (p['origin'] + '\n').encode()
        need(before == after and selector == b'' and fetch == push == intended, 'stable exact singleton intended HTTPS origin and no VCS selector')
        state = {'configuration': pin(before), 'effective_fetch_URL_SHA256': sha(fetch), 'effective_push_URL_SHA256': sha(push), 'singletons_match_intended_origin': True, 'origin_vcs_selector_absent': True}
        need(expected is None or state == expected, 'same authority-bound effective routing')
        return state


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
            need(row['remote_tracking_FETCH_HEAD_and_nonlocal_packed_lines_deliberately_not_bound'] is True, 'actual local-only native guard semantics')
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
        decoder = json.JSONDecoder(object_pairs_hook=unique_pairs)
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


    def adopted_aggregates(buffers, evidence, stage_files):
        need(set(evidence) == {'index', 'sitemap'}, 'actual accepted aggregate evidence')
        index, sitemap = evidence['index'], evidence['sitemap']
        need(index['whole_buffer_reversible'] is True and sitemap['whole_buffer_reversible'] is True, 'root-adopted whole aggregate reversibility')
        need(len(index['old_visible']) == len(index['old_typed']) == len(index['old_raw_JSON_units']) == len(index['old_raw_HTML_units']) == 126 and len(index['new_items']) == 2 and len(sitemap['old_raw_nodes']) == len(sitemap['old_parsed_nodes']) == 127, 'actual accepted126/127 ordered prefixes and two appends')
        for path, original in [('public/research/index.html', 'originals/research-index.html'), ('public/research/sitemap.xml', 'originals/research-sitemap.xml')]:
            need(row_for(S / original) == stage_files[original], 'whole original accepted aggregate pin')
        old_index = read(S / 'originals/research-index.html').decode('utf-8')
        new_index = buffers['public/research/index.html'].decode('utf-8')
        old_script, old_body, old_units, old_close, old_typed = script_units(old_index)
        new_script, new_body, new_units, new_close, new_typed = script_units(new_index)
        need(len(old_units) == old_typed['mainEntity']['numberOfItems'] == 126 and len(new_units) == new_typed['mainEntity']['numberOfItems'] == 128, 'actual structured126-to128 aggregate counts')
        need([old_body[a:b] for a, b, value in old_units] == index['old_raw_JSON_units'] == [new_body[a:b] for a, b, value in new_units[:126]], 'all126 exact raw JSON prefixes')
        need([value for a, b, value in old_units] == index['old_typed'] == [value for a, b, value in new_units[:126]] and [value for a, b, value in new_units[126:]] == index['new_items'], 'all126 typed prefixes and exact two adopted appends')
        html_units = index['old_raw_HTML_units']
        positions = [new_index.index(unit) for unit in html_units]
        need(positions == sorted(positions) and all(old_index.count(unit) == new_index.count(unit) == 1 for unit in html_units) and new_index.count(index['appended_HTML']) == 1, 'all126 raw visible units in order and whole adopted append')
        old_xml = read(S / 'originals/research-sitemap.xml')
        new_xml = buffers['public/research/sitemap.xml']
        old_nodes = list(re.finditer(rb'<url>.*?</url>', old_xml, re.S))
        new_nodes = list(re.finditer(rb'<url>.*?</url>', new_xml, re.S))
        need(len(old_nodes) == 127 and len(new_nodes) == 129 and [r.group().decode() for r in old_nodes] == sitemap['old_raw_nodes'] == [r.group().decode() for r in new_nodes[:127]], 'all127 actual raw XML prefixes')
        def xml_value(node):
            return {'tag': node.tag, 'attributes': dict(node.attrib), 'text': node.text, 'tail': node.tail, 'children': [xml_value(child) for child in node]}
        need([xml_value(node) for node in ET.fromstring(old_xml)] == sitemap['old_parsed_nodes'] == [xml_value(node) for node in list(ET.fromstring(new_xml))[:127]], 'all127 namespace-aware parsed XML prefixes including attributes/text/tails')
        need(new_xml.count(sitemap['appended_XML'].encode()) == 1, 'whole exact adopted XML append')
        return {'whole_reversibility': 'INHERITED_EXACT_PINNED_STAGE_AUDIT_AND_ROOT_ADOPTION', 'raw_typed_visible_prefixes_rechecked': True}

    def contract(p):
        controls = p['controls']
        adopted = strict_json(bound(controls['root_stage_adoption']))
        need(adopted == p['root_stage_adoption_semantics'] and adopted['schema'] == 'root-radial-tree-private-stage-adoption-v1' and adopted['status'] == 'ADOPTED_PRIVATE_STAGE_FIDELITY', 'exact actual root stage semantic adoption')
        need(adopted['production_preparation_may_proceed'] is True and adopted['action_authority_from_this_receipt'] is False and adopted['root_read_actual_activated_HEADs_and_whole_BODY_correspondence'] is True, 'preparation-only root adoption, full accepted body/head fidelity')
        need(adopted['independent_data_checks'] == 17 and adopted['independent_criteria'] == 26 and adopted['literal_build_history'] == [1, 0] and adopted['original_failure_stderr_bytes'] == 1028, 'accepted actual audit and retained literal history')
        for label, root in [('stage', S), ('independent_audit', A)]:
            item = next(row for row in adopted['own_fresh_authentication'] if row['root'] == str(root))
            need(item['FINAL_SHA256'] == controls[label + '_FINAL']['SHA256'] and item['manifest_SHA256'] == controls[label + '_manifest']['SHA256'] and item['all_manifest_bytes_modes_topology_exact'] is True, 'root adopted exact finite packet pins')
        need(adopted['root_complete_producer_code_read'] == {'lines': 482, 'SHA256': controls['stage_builder']['SHA256']}, 'actual root-read frozen producer pin')
        bound(controls['stage_builder'])
        stage_final = strict_json(bound(controls['stage_FINAL']))
        stage = authenticate_manifest(S, strict_json(bound(controls['stage_manifest'])), controls['stage_FINAL'], controls['stage_manifest'], 'stage')
        stage_files, stage_dirs = tables(stage)
        need(stage_final['schema'] == 'private-two-page-stage-final-v1' and stage_final['status'] == 'FROZEN_PRIVATE_STAGE_READY_FOR_INDEPENDENT_IMPLEMENTATION_AUDIT' and stage_final['publication_authority'] is False, 'actual stage FINAL and no action grant')
        need(stage_final['ordinary_private_stage_builds'] == 2 and stage_final['retained_first_attempt_exit'] == 1 and stage_final['successful_private_stage_builds'] == 1, 'retained build failure and one successful stage')
        audit_final = strict_json(bound(controls['independent_audit_FINAL']))
        audit = authenticate_manifest(A, strict_json(bound(controls['independent_audit_manifest'])), controls['independent_audit_FINAL'], controls['independent_audit_manifest'], 'audit')
        result = strict_json(bound(controls['independent_audit_result']))
        for label in ('independent_audit_report', 'independent_audit_criteria', 'build_receipt'):
            bound(controls[label])
        need(audit_final['schema'] == 'independent-radial-tree-stage-implementation-FINAL-v1' and audit_final['status'] == 'PASS' and result['schema'] == 'independent-radial-tree-stage-data-result-v1' and result['status'] == 'PASS', 'literal accepted independent implementation/data PASS schemas')
        need(audit_final['criterion_count'] == 26 and audit_final['failed_criteria'] == [] and audit_final['grouped_data_checks'] == 17 and audit_final['data_failed_checks'] == 0, 'actual26criterion17group independent audit')
        need(len(result['checks']) == 17 and all(set(row) == {'check', 'PASS', 'details'} and row['PASS'] is True for row in result['checks']) and result['failed_checks'] == 0, 'all17 actual data checks passed')
        need(audit_final['production_authority'] is False and result['production_authority'] is False and audit_final['generic_producer_duplicate_parser_certificate'] is False, 'no generic parser/action certificate inferred')
        guard_raw = bound(controls['build_guards_before'])
        need(guard_raw == bound(controls['build_guards_after']), 'complete frozen before/after guards exact')
        raw_guards = strict_json(guard_raw)
        need(set(raw_guards) == {'inputs', 'native_controls', 'public', 'retained_first_attempt'} and set(raw_guards['inputs']) == {'root_pins', 'private_packets', 'native_sources'}, 'actual stage guard dictionary schema')
        inputs = raw_guards['inputs']
        for path, row in inputs['root_pins'].items():
            bound({'path': path, **canonical_pin(row)})
        private = [normalize_snapshot(item) for item in inputs['private_packets'].values()]
        sources = [normalize_snapshot(item) for item in inputs['native_sources'].values()]
        need(len(private) == 6 and sum(x['regular_files'] for x in private) == 186 and len(sources) == 2 and sum(x['regular_files'] for x in sources) == 233, 'all accepted private186/source233 finite extents')
        for namespace in private + sources:
            whole_snapshot(namespace)
        guards = {'native': normalized_native(raw_guards['native_controls'], p), 'public': normalize_snapshot(raw_guards['public']), 'adopted_inputs': private, 'original_sources': sources}
        need(guards['public']['root'] == str(W / 'public'), 'actual baseline public root identity')
        target_plan = strict_json(bound(controls['target_plan']))
        need(set(target_plan) == {'row_order', 'A', 'M', 'D', 'new_directories', 'production_target_count'} and target_plan['row_order'] == [184, 185] and target_plan['D'] == [] and (len(target_plan['A']), len(target_plan['M']), target_plan['production_target_count']) == (9, 2, 11), 'actual exact11/9A2M target schema')
        names = target_plan['A'] + target_plan['M']
        need(len(set(names)) == 11 and all(not name.startswith('public/') for name in names), 'actual public-root-relative targets, no double prefix')
        for name in names:
            relative(name)
        need({'public/' + name for name in names} == TARGETS and ['public/' + name for name in target_plan['M']] == REPLACEMENTS and sorted(target_plan['new_directories']) == p['new_directories'], 'prepend public exactly once; exact Git scope and four dirs')
        need(stage_final['target_plan'] == target_plan and audit_final['exact_public_root_relative_targets'] == target_plan, 'actual root/producer/independent target projection agreement')
        old_files, old_dirs = tables(guards['public'])
        need((len(old_files), len(old_dirs), guards['public']['root_mode']) == (772, 373, '0750') and sum(Path(name).name == '.DS_Store' for name in old_files) == 17, 'actual772/373 baseline and17DSStore')
        candidate = normalize_snapshot(strict_json(bound(controls['candidate_manifest'])))
        need(candidate['root'] == str(S / 'candidate/public'), 'explicit actual stage candidate root')
        whole_snapshot(candidate)
        candidate_files, candidate_dirs = tables(candidate)
        buffers = {}
        for name in sorted(TARGETS):
            need((name[7:] in old_files) == (name in REPLACEMENTS), 'exact nine additions and only two existing target leaves')
            raw = read(S / 'candidate' / relative(name))
            row = {**pin(raw), 'mode': permissions(S / 'candidate' / relative(name))}
            need(row == candidate_files[name[7:]] == stage_files['candidate/' + name] and row['mode'] == '0644', 'whole frozen0644 target bytes')
            buffers[name] = raw
        necessary = set()
        for name in buffers:
            necessary.update(parent.as_posix() for parent in Path(name[7:]).parents if parent.as_posix() != '.' and parent.as_posix() not in old_dirs)
        need(necessary == set(p['new_directories']) and len(necessary) == 4, 'exact four necessary new directories')
        expected_files = dict(old_files)
        expected_files.update({name[7:]: {**pin(raw), 'mode': '0644'} for name, raw in buffers.items()})
        expected_dirs = {**old_dirs, **{name: '0755' for name in necessary}}
        need(candidate_files == expected_files and candidate_dirs == expected_dirs and candidate['root_mode'] == '0750' and (len(candidate_files), len(candidate_dirs)) == (781, 377), 'all770 untargeted old files and373 directory modes preserved')
        need(normalize_snapshot(result['evidence']['current_public772']) == guards['public'] and normalize_snapshot(result['evidence']['candidate781']) == candidate, 'independent full baseline/candidate evidence exact')
        aggregate = strict_json(bound(controls['aggregate_preservation']))
        aggregate_proof = adopted_aggregates(buffers, aggregate, stage_files)
        for original, name in [('originals/research-index.html', REPLACEMENTS[0]), ('originals/research-sitemap.xml', REPLACEMENTS[1])]:
            need(stage_files[original] == old_files[name[7:]], 'exact original aggregate equals baseline public row')
        for row in p['immutable_input_files'] + p['configuration_guards']:
            bound(row)
        return {'plan': p, 'buffers': buffers, 'guards': guards, 'old_files': old_files, 'old_dirs': old_dirs, 'new_dirs': necessary, 'stage_snapshot': stage, 'audit_snapshot': audit, 'candidate_snapshot': candidate, 'aggregate_proof': aggregate_proof}

    def public_fence(context, installed):
        p, buffers = context['plan'], context['buffers']
        expected = dict(context['old_files'])
        dirs = dict(context['old_dirs'])
        if installed:
            expected.update({name[7:]: {**pin(raw), 'mode': '0644'} for name, raw in buffers.items()})
            dirs.update({name: '0755' for name in context['new_dirs']})
        actual = census(W / 'public')
        files, actual_dirs = tables(actual)
        need(files == expected and actual_dirs == dirs and actual['root_mode'] == '0750', 'whole phase public bytes/modes/topology including hidden/empty/ignored objects')
        index = read(W / 'public/research/index.html').decode('utf-8')
        entity = script_units(index)[4]['mainEntity']
        counts = [len(files), len(dirs), entity['numberOfItems'], len(ET.fromstring(read(W / 'public/research/sitemap.xml')))]
        need(type(entity['numberOfItems']) is int and len(entity['itemListElement']) == counts[2] and counts == p['after_counts_files_childdirs_articles_sitemap' if installed else 'before_counts_files_childdirs_articles_sitemap'], 'exact phase772/373/126/127 or781/377/128/129 structured counts')
        return actual, counts


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


    def tree_entries(p, tree):
        pieces = git(p, 'ls-tree', '-r', '-z', '--full-tree', tree, opaque=True).split(b'\0')
        need(pieces.pop() == b'', 'whole NUL tree listing')
        result = {}
        for record in pieces:
            header, name = record.split(b'\t', 1)
            need(name and name not in result, 'unique complete tree leaf')
            result[name] = header
        return result


    def record_tree(records):
        result = {}
        for name, record in records.items():
            mode = struct.unpack('>I', record[1])[0]
            need(mode in (0o100644, 0o100755, 0o120000, 0o160000), 'ordinary raw index tree mode')
            result[name] = (format(mode, '06o') + ' ' + ('commit' if mode == 0o160000 else 'blob') + ' ' + record[2].hex()).encode()
        return result


    def blob_oid(raw):
        return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


    def cache_semantics(p, records, extension):
        need(pin(extension) == p['baseline_TREE_extension'] and len(extension) >= 8 and extension[:4] == b'TREE', 'exact whole TREE extension includes eight-byte header')
        size = struct.unpack('>I', extension[4:8])[0]
        payload = extension[8:]
        need(size == len(payload) and pin(payload) == p['baseline_TREE_payload'], 'distinct exact TREE payload pin, no unknown extension')
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
            need(entries >= -1 and children <= len(trees), 'TREE cached count bounds')
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
        need(pos == len(payload) and len(seen) == p['baseline_TREE_cache']['nodes'] and len(valid) == p['baseline_TREE_cache']['valid_nodes'] and sorted(invalid) == sorted(p['baseline_TREE_cache']['invalidated_paths']), 'whole cached TREE recursion,977 valid and six pre-existing invalidated/no-OID nodes')
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
        return {'whole_extension': pin(extension), 'payload': pin(payload), 'nodes': len(seen), 'valid_nodes': len(valid), 'invalidated_paths_no_OID': invalid, 'native_root_tree': trees[b''][1], 'valid_cached_nodes': [{'path_hex': path.hex(), 'OID': oid, 'entries': entries, 'subtrees': children} for path, oid, entries, children in valid]}


    def preflight(p, installed, owned_index_lock=None):
        context = contract(p)
        native_fence(context['guards']['native'])
        need(git(p, 'rev-parse', '--show-toplevel').strip().decode() == str(W), 'exact website repository root')
        need(git(p, 'rev-parse', '--absolute-git-dir').strip().decode() == str(W / '.git'), 'exact ordinary website Git directory')
        need(git(p, 'symbolic-ref', 'HEAD').strip().decode() == p['branch'] and git(p, 'rev-parse', 'HEAD').strip().decode() == p['website_HEAD'], 'existing master and exact immutable current parent')
        need(git(p, 'rev-parse', '--show-object-format').strip() == b'sha1', 'SHA1 website repository')
        tree = git(p, 'rev-parse', p['website_HEAD'] + '^{tree}').strip().decode()
        route = routing(p)
        old = read(W / '.git/index')
        need(row_for(W / '.git/index') == {key: p['website_index'][key] for key in ('bytes', 'SHA256', 'mode')}, 'exact9057886B current native index baseline')
        records, extension = index_entries(old)
        target_bytes = {name.encode() for name in TARGETS}
        need(len(records) == 58712 and set(records) & target_bytes == {name.encode() for name in REPLACEMENTS} and len(set(records) - target_bytes) == 58710 and pin(extension) == p['baseline_TREE_extension'], 'exact58712 records/58710 protected and whole known TREE baseline')
        cache = cache_semantics(p, records, extension)
        lock = W / '.git/index.lock'
        need(not os.path.lexists(lock) if owned_index_lock is None else os.path.lexists(lock) and inode(lock.lstat()) == owned_index_lock, 'exclusive native index lock state')
        head_scope = git(p, 'ls-tree', '-r', '-z', '--full-tree', p['website_HEAD'], '--', *sorted(TARGETS)).split(b'\0')
        need(head_scope.pop() == b'' and {row.split(b'\t', 1)[1] for row in head_scope} == {name.encode() for name in REPLACEMENTS}, 'HEAD has only two existing aggregate leaves in scope')
        for record in head_scope:
            header, name = record.split(b'\t', 1)
            original = 'originals/research-index.html' if name.decode() == REPLACEMENTS[0] else 'originals/research-sitemap.xml'
            raw = read(S / original)
            need(header == ('100644 blob ' + blob_oid(raw)).encode() and record_tree({name: records[name]})[name] == header, 'both existing aggregate blobs equal native index and HEAD')
        actual, counts = public_fence(context, installed)
        identities = {}
        for name in REPLACEMENTS:
            info = (W / name).lstat()
            identities[name] = [*inode(info), info.st_mtime_ns, info.st_ctime_ns]
        protected = b''.join(records[name][0] for name in sorted(set(records) - target_bytes))
        state = {'installed': installed, 'bindings': bindings(p), 'W_HEAD': p['website_HEAD'], 'W_tree': tree, 'W_index': pin(old), 'routing': route, 'public_snapshot_SHA256': sha(packed(actual)), 'counts': counts, 'aggregate_identities': identities, 'protected_raw_records': pin(protected), 'protected_count': 58710, 'baseline_TREE_extension': pin(extension), 'baseline_TREE_payload': p['baseline_TREE_payload'], 'TREE_cache_proof_SHA256': sha(packed(cache)), 'stage_snapshot_SHA256': sha(packed(context['stage_snapshot'])), 'audit_snapshot_SHA256': sha(packed(context['audit_snapshot'])), 'source_guard_SHA256': sha(packed(context['guards']['adopted_inputs'] + context['guards']['original_sources']))}
        context.update(old_index=old, old_records=records, old_extension=extension, cache_proof=cache, tree=tree, state=state, fingerprint=sha(packed(state)))
        return context


    def transaction(kind, authority):
        nonlocal LOG
        current_authority(authority)
        safe(RUN)
        if kind == 'install':
            need(not os.path.lexists(RUN), 'fresh runtime must never already exist')
            mkdir_exclusive(RUN, 0o700)
        else:
            need(stat.S_ISDIR(RUN.lstat().st_mode) and permissions(RUN) == '0700', 'this existing successful-install runtime only')
        need(RUN.stat().st_dev == W.stat().st_dev, 'actual runtime and website share filesystem before website mutation')
        lock = RUN / ('ACTIVE_INSTALL.lock' if kind == 'install' else 'ACTIVE_PUBLISH.lock')
        body = packed({'schema': 'radial-tree-runtime-lock-v1', 'action': authority['data']['action'], 'authorization_SHA256': sha(authority['raw']), 'nonce': authority['data']['nonce'], 'PID': os.getpid()})
        new_file(lock, body)
        lock_fd = os.open(lock, os.O_RDONLY | os.O_NOFOLLOW)
        owner = inode(os.fstat(lock_fd))
        phase_root = RUN / kind
        mkdir_exclusive(phase_root, 0o700)
        transaction_root = phase_root / sha(authority['raw'])
        mkdir_exclusive(transaction_root, 0o700)
        new_file(transaction_root / 'authorization.json', authority['raw'])
        fd = os.open(transaction_root / 'journal.jsonl', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        os.fchmod(fd, 0o600)
        os.fsync(fd)
        LOG = os.fdopen(fd, 'wb')
        sync_dir(transaction_root)

        def check():
            current_authority(authority)
            need(inode(lock.lstat()) == owner and held(lock_fd) == body and permissions(lock) == '0600', 'same held exclusive current runtime lock')

        check()
        event('PRETRANSACTION_READ_EVENTS', events=list(TRACE))
        event('AUTHORIZED_TRANSACTION', action=authority['data']['action'], authorization_SHA256=sha(authority['raw']), preflight_SHA256=authority['data']['preflight_SHA256'])
        return transaction_root, check, lock_fd


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
        new_file(root / 'index.before', context['old_index'], 0o644)
        for name, leaf in [('HEAD.before', 'HEAD'), ('config.before', 'config'), ('loose-master.before', 'refs/heads/master')]:
            new_file(root / name, read(W / '.git' / leaf), 0o644)
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
            need(len(absent) == 9 and all(not os.path.lexists(W / name) for name in absent), 'exact9 original leaf absences')
            need(all(not os.path.lexists(W / 'public' / name) for name in context['new_dirs']), 'exact4 original directory absences')
            recovery = {'schema': 'radial-tree-durable-install-recovery-v1', 'replacement_backups': {name: context['old_files'][name[7:]] for name in REPLACEMENTS}, 'new_leaves_before': {name: 'ABSENT' for name in absent}, 'new_directories_before': {name: 'ABSENT' for name in sorted(context['new_dirs'])}, 'native_index_before': pin(context['old_index']), 'native_guards_before': context['guards']['native'], 'public_before': context['guards']['public'], 'recovery': 'STOP_AND_ROOT_REVIEW_NO_AUTOMATIC_ROLLBACK_OR_RETRY'}
            new_file(t / 'rollback.before.json', packed(recovery))
            new_file(t / 'preflight.before.json', packed(context['state']))
            sync_dir(staged)
            sync_dir(backups)
            sync_dir(t)
            event('ALL11_BUFFERS_2_RELATIVE_BACKUPS_9_LEAF_4_DIRECTORY_ABSENCES_AND_NATIVE_ROLLBACK_MATERIAL_DURABLE')
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
            need(verified['old_index'] == context['old_index'] and not list(staged.iterdir()) and set(made) == {'public/' + name for name in context['new_dirs']}, 'native index unchanged; exact11 buffers/four dirs completed')
            check()
            result = {'schema': 'radial-tree-install-success-v1', 'status': 'FILESYSTEM_INSTALL_VERIFIED_SNAPSHOT', 'UTC': utc().isoformat(), 'bindings': authority['bindings'], 'counts': verified['state']['counts'], 'targets': sorted(TARGETS), 'authorization_SHA256': sha(authority['raw']), 'nonce': authority['data']['nonce'], 'runtime_root': str(RUN), 'transaction': str(t), 'installed_preflight_SHA256': verified['fingerprint'], 'W_native_HEAD_index_config_unchanged': True, 'Math_all_native_guards_unchanged': True, 'source_stage_audit_all_guards_unchanged': True, 'Git_object_ref_index_network_deploy_Sheet_changes': False, 'runtime_install_lock_retained': True, 'automatic_rollback_or_retry': False}
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


    def semantic_rows(mapping):
        return [{'path_hex': name.hex(), 'header_ascii': value.decode('ascii')} for name, value in sorted(mapping.items())]


    def foreign_rows(native, head, targets):
        return {name: (native.get(name), head.get(name)) for name in (set(native) | set(head)) - targets if native.get(name) != head.get(name)}


    def foreign_serialized(mapping):
        return [{'path_hex': name.hex(), 'native': None if pair[0] is None else pair[0].decode('ascii'), 'HEAD': None if pair[1] is None else pair[1].decode('ascii')} for name, pair in sorted(mapping.items())]


    def remote_parent(p, expected):
        actual = git(p, 'ls-remote', '--exit-code', 'origin', p['branch'])
        need(actual == (expected + '\t' + p['branch'] + '\n').encode(), 'exact singleton remote branch snapshot')


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
            native_backups(t / 'native-backups', context)
            new_file(t / 'preflight.before.json', packed(context['state']))
            native, commit_index = t / 'native-successor.index', t / 'commit.index'
            new_file(native, context['old_index'], 0o644)
            oids = {name: blob_oid(raw) for name, raw in buffers.items()}
            for name, raw in sorted(buffers.items()):
                check()
                need(git(p, 'hash-object', '--no-filters', '-w', '--stdin', data=raw).strip().decode() == oids[name], 'exact unfiltered frozen payload object')
            info = b''.join(('100644 ' + oids[name] + '\t' + name).encode() + b'\0' for name in sorted(buffers))
            check()
            git(p, 'update-index', '--add', '-z', '--index-info', data=info, index=native)
            check()
            git(p, 'read-tree', context['tree'], index=commit_index)
            check()
            git(p, 'update-index', '--add', '-z', '--index-info', data=info, index=commit_index)
            check()
            tree = git(p, 'write-tree', index=commit_index).strip().decode()
            staged = read(native)
            before, before_extension = index_entries(context['old_index'])
            after, after_extension = index_entries(staged)
            need(after_extension == before_extension, 'successor preserves exact whole TREE extension,977 valid and six pre-existing invalidated nodes')
            after_cache = cache_semantics(p, after, after_extension)
            targets = {name.encode() for name in TARGETS}
            need(len(after) == 58721 and set(after) == set(before) | targets and len(set(before) - targets) == 58710, 'exact58721 successor and58710 untargeted records')
            need(all(after[name] == record for name, record in before.items() if name not in targets), 'all58710 WHOLE raw stat/path/OID/mode/flag/padding records byte-exact')
            need(all(after[name.encode()][1:] == (struct.pack('>I', 0o100644), bytes.fromhex(oids[name])) for name in TARGETS), 'all11 successor target blob/mode semantics exact')
            before_check, after_check = t / 'before-semantic.index', t / 'after-semantic.index'
            new_file(before_check, context['old_index'], 0o644)
            new_file(after_check, staged, 0o644)
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
            need(set(commit_tree) == set(parent_tree) | targets and all(commit_tree[name] == record for name, record in parent_tree.items() if name not in targets), 'all untargeted HEAD tree leaves exact; only9 additions')
            delta = git(p, 'diff-tree', '--raw', '-r', '--no-commit-id', '--no-abbrev', '--no-renames', '--no-ext-diff', '-z', context['tree'], tree).split(b'\0')
            need(delta.pop() == b'' and len(delta) == 22 and {delta[index + 1] for index in range(0, 22, 2)} == targets, 'exact11-path commit delta')
            for index in range(0, 22, 2):
                header, name = delta[index].split(), delta[index + 1].decode()
                need(header[1] == b'100644' and header[3].decode() == oids[name] and header[4] == (b'M' if name in REPLACEMENTS else b'A'), 'exact9A2M frozen blob delta; no other path/action')
            for name, mapping in [('before-native-semantics.json', native_before), ('after-native-semantics.json', native_after), ('parent-HEAD-tree.json', parent_tree), ('successor-commit-tree.json', commit_tree)]:
                new_file(t / name, packed(semantic_rows(mapping)))
            for name, mapping in [('foreign-staging.before.json', foreign_before), ('foreign-staging.after.json', foreign_after)]:
                new_file(t / name, packed(foreign_serialized(mapping)))
            proof = {'schema': 'radial-tree-native-index-proof-v1', 'before_index': pin(context['old_index']), 'after_index': pin(staged), 'before_records': 58712, 'after_records': 58721, 'protected_whole_raw_records': 58710, 'before_TREE': pin(before_extension), 'after_TREE': pin(after_extension), 'before_TREE_payload': p['baseline_TREE_payload'], 'after_TREE_payload': pin(after_extension[8:]), 'before_TREE_semantics': context['cache_proof'], 'after_TREE_semantics': after_cache, 'TREE_changed': before_extension != after_extension, 'private_before_semantic_tree': before_tree, 'private_after_semantic_tree': native_tree, 'parent_commit_tree': context['tree'], 'successor_commit_tree': tree, 'delta': '9A2M', 'foreign_staging_exact': True, 'all_untargeted_HEAD_tree_leaves_exact': True, 'no_broad_refresh_or_unknown_extension_waiver': True}
            new_file(t / 'native-index-proof.json', packed(proof))
            new_file(t / 'commit-delta.raw', b'\0'.join(delta) + b'\0')
            event('PRIVATE_INDEX_AND_EXACT11_COMMIT_TREE_PROVED', **proof)
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
                need(git(p, 'symbolic-ref', 'HEAD').strip().decode() == p['branch'] and git(p, 'rev-parse', p['branch']).strip().decode() == commit, 'master retained at exact successor commit')
                need(read(W / '.git/index') == staged and index_entries(read(W / '.git/index')) == (after, after_extension), 'complete successor index/raw record/extension equality after native publication')
                need(tree_entries(p, commit) == commit_tree and all(native_after[name] == commit_tree[name] for name in targets), 'published commit exact11 targets and protected tree')
                need(foreign_rows(record_tree(after), commit_tree, targets) == foreign_before and all(after[name] == before[name] for name in before if name not in targets), 'postpublication foreign staging and58710 whole records exact')
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
            final_local()
            check()
            result = {'schema': 'radial-tree-publication-success-v1', 'status': 'SCOPED11_COMMIT_AND_PUSH_VERIFIED_SNAPSHOT', 'UTC': utc().isoformat(), 'bindings': authority['bindings'], 'authorization_SHA256': sha(authority['raw']), 'nonce': authority['data']['nonce'], 'installation_SUCCESS': authority['data']['installation_SUCCESS'], 'commit': commit, 'tree': tree, 'parent': p['website_HEAD'], 'branch': p['branch'], 'paths': 11, 'delta': '9A2M', 'protected_whole_raw_records': 58710, 'successor_index_records': 58721, 'index': {**pin(staged), 'mode': '0644'}, 'native_successor_semantic_tree': native_tree, 'TREE_before': pin(before_extension), 'TREE_after': pin(after_extension), 'foreign_staging_semantics_preserved': True, 'Math_all_native_guards_unchanged': True, 'stage_audit_sources_all_guards_unchanged': True, 'all_old772_public_buffers_retained_except2_planned_replacements': True, 'all_old373_directory_modes_and17DSStore_retained': True, 'postpush_exact_remote_and_whole_local_verification': True, 'deployment_or_Sheet_or_AA_actions': False, 'runtime_publish_lock_retained': True, 'automatic_rollback_or_retry': False}
            new_file(t / 'SUCCESS.json', packed(result), 0o644)
            event('SCOPED11_PUBLICATION_SUCCESS', **result)
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


    def main():
        args = sys.argv[1:]
        need(args in [['--preflight'], ['--verify-installed'], ['--install'], ['--publish']], 'only explicit root-controlled four active modes')
        p = load_plan()
        mode = args[0]
        kind = 'readonly' if mode in ('--preflight', '--verify-installed') else mode[2:]
        installed = mode in ('--verify-installed', '--publish')
        phase = 'installed' if installed else 'before_install'
        authority = authorization(kind, p, phase)
        current_authority(authority)
        if mode in ('--preflight', '--install'):
            need(not os.path.lexists(RUN), 'exclusive fresh runtime absent in preinstall phase')
        context = preflight(p, installed)
        current_authority(authority)
        if kind == 'install':
            result = install(context, authority)
        elif kind == 'publish':
            result = publish(context, authority)
        else:
            result = {'schema': 'radial-tree-readonly-preflight-v1', 'status': 'READONLY_INSTALLED_PREFLIGHT' if installed else 'READONLY_PREINSTALL_PREFLIGHT', 'UTC': utc().isoformat(), 'preflight_SHA256': context['fingerprint'], 'state': context['state'], 'readonly_authorization_SHA256': sha(authority['raw']), 'nonce': authority['data']['nonce'], 'filesystem_writes': 0, 'remote_calls': 0, 'authority_inferred': False, 'read_events': list(TRACE)}
        print(json.dumps(result, sort_keys=True))


    if __name__ == '__main__':
        try:
            main()
        except BaseException as error:
            event('FAILED_HISTORY_RETAINED', error=repr(error))
            print(json.dumps({'status': 'STOPPED_STATE_RETAINED', 'error': repr(error), 'pretransaction_read_events': TRACE, 'automatic_rollback': False, 'automatic_retry': False}), file=sys.stderr)
            raise


if __name__ == '__main__':
    _run_explicit_mode()
