"""Exact11 read fences and future authority-gated installation primitives."""
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import re
import struct
import stat
import subprocess
import tempfile
import xml.etree.ElementTree as ET

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
O = Path(__file__).resolve().parent
S = P / 'verification/lefschetz-link-private-stage-sol-20261115'
A = P / 'verification/lefschetz-link-independent-code-audit-sol-20261115'
BASE = '27cd946786754d66b44cbb309dae76da238b133e'
STAGE_SEAL = 'b42073395a01c7a60c733627212df7d56f484023662119a215a8b6cb57b89575'
AUDIT = A / 'FINAL_SEAL.json'
AUDIT_SEAL = 'afe06ee13def341fe2798f25aee2ad971477a442ad6320357f2b3cf2dafa1ed0'
ADOPTION = P / 'verification/root-lefschetz-link-stage-adoption-20261115.json'
COMMIT_APPROVAL = P / 'verification/root-lefschetz-link-commit-approval-20261115.json'
ROOT_READING = P / 'verification/root-lefschetz-link-stage-reading-20261115.json'
ROOT_READING_SHA256 = '455b7f101f01bd4a677be69ffd53aefb9f146872360f5c3e94fe16a65740d865'
LOCK_BODY = b'Exact11 publication lock; inspect run-state if interrupted\n'
AGGREGATES = {'research/index.html', 'research/sitemap.xml'}
CODE_FILES = ['exact11_lib.py', 'preflight.py', 'install_exact.py', 'hooks/pre-push',
              'controls.py', 'verify_preparation.py']


def need(ok, why):
    if not ok:
        raise RuntimeError(why)


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(body):
    return hashlib.sha256(body).hexdigest()


def read(path):
    path = Path(path)
    need(path.is_file() and not path.is_symlink() and path.resolve() == path,
         'regular file through real ancestors: ' + str(path))
    return path.read_bytes()


def obj(path):
    return json.loads(read(path))


def pin(path, row):
    body = read(path)
    need(len(body) == row['bytes'] and sha(body) == row['SHA256'], 'whole-byte pin: ' + str(path))
    return body


def safe_rel(text):
    path = PurePosixPath(text)
    need(not path.is_absolute() and '..' not in path.parts and str(path) == text
         and '\\' not in text and path.parts, 'safe relative path')
    return path


def namespace(root):
    paths = list(root.rglob('*'))
    need(root.is_dir() and not root.is_symlink() and root.resolve() == root
         and all(not p.is_symlink() and (p.is_file() or p.is_dir()) for p in paths),
         'whole regular namespace: ' + str(root))
    return sorted(p.relative_to(root).as_posix() for p in paths if p.is_file())


def root_reading():
    body = read(ROOT_READING)
    need(sha(body) == ROOT_READING_SHA256, 'separate actual root stage/copy/audit adoption')
    value = json.loads(body)
    need(value['root_stage_code_and_current_copy_adopted'] is True
         and value['root_independent_integration_audit_adopted'] is True
         and value['production_installation_authorized'] is False,
         'completed stage reading remains distinct from future install authority')
    return value


def owned_entry(path, fd, missing_ok=False):
    try:
        entry = path.lstat()
    except FileNotFoundError:
        need(missing_ok, 'owned entry disappeared: ' + str(path))
        return False
    descriptor = os.fstat(fd)
    need(stat.S_ISREG(entry.st_mode) and stat.S_ISREG(descriptor.st_mode)
         and (entry.st_dev, entry.st_ino) == (descriptor.st_dev, descriptor.st_ino),
         'owned regular inode required: ' + str(path))
    return True


def write_complete(fd, body):
    view = memoryview(body)
    offset = 0
    while offset < len(view):
        try:
            written = os.write(fd, view[offset:])
        except InterruptedError:
            continue
        need(0 < written <= len(view) - offset, 'complete write must make positive progress')
        offset += written


def validate_owned_buffer(path, fd, expected):
    owned_entry(path, fd)
    os.fsync(fd)
    os.lseek(fd, 0, os.SEEK_SET)
    chunks = []
    while True:
        chunk = os.read(fd, 1024 * 1024)
        if not chunk:
            break
        chunks.append(chunk)
    need(b''.join(chunks) == expected, 'same owned FD must contain exact validated buffer')
    owned_entry(path, fd)


def unlink_owned(path, fd):
    if owned_entry(path, fd, missing_ok=True):
        path.unlink()


def publish_buffer(newraw, destination, lock, lock_fd):
    # Caller retains a distinct exclusive index.lock through the later ref/push.
    fd, temporary = tempfile.mkstemp(prefix='.exact11-index-approved-', dir=destination.parent)
    temporary = Path(temporary)
    try:
        write_complete(fd, newraw)
        validate_owned_buffer(temporary, fd, newraw)
        validate_owned_buffer(lock, lock_fd, LOCK_BODY)
        owned_entry(temporary, fd)
        os.replace(temporary, destination)
        validate_owned_buffer(destination, fd, newraw)
    finally:
        try:
            unlink_owned(temporary, fd)
        finally:
            os.close(fd)


def git(*args, index=None, data=None, mutating=False, guard_commit=None, guard_remote_sha=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['GIT_OPTIONAL_LOCKS'] = '0'
    if index is not None:
        env['GIT_INDEX_FILE'] = str(index)
    if guard_commit is not None:
        need(args[0] == 'push' and re.fullmatch('[0-9a-f]{40}', guard_commit)
             and re.fullmatch('[0-9a-f]{64}', guard_remote_sha or ''), 'explicit approved push parameters')
        hook = O / 'hooks/pre-push'
        need(namespace(O / 'hooks') == ['pre-push'] and hook.stat().st_mode & 0o7777 == 0o555
             and os.access(hook, os.X_OK), 'sole read-only executable0555 push guard')
        env['EXACT11_APPROVED_COMMIT'] = guard_commit
        env['EXACT11_APPROVED_PUSH_URL_SHA256'] = guard_remote_sha
    command = ['git', '-c', 'gc.auto=0', '-c', 'core.hooksPath=/dev/null',
               '-c', 'core.fsmonitor=false', '-c', 'commit.gpgsign=false',
               '-c', 'push.followTags=false', '-c', 'remote.origin.mirror=false']
    if guard_commit is not None:
        command += ['-c', 'core.hooksPath=' + str(O / 'hooks')]
    allowed = {'rev-parse', 'symbolic-ref', 'ls-files', 'ls-remote', 'remote', 'diff',
               'diff-tree', 'cat-file', 'ls-tree', 'config'}
    need(mutating or args[0] in allowed, 'write command requires explicit future mutation path')
    result = subprocess.run(command + list(args), cwd=W, env=env, input=data,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    need(result.returncode == 0, 'Git ' + args[0] + ' failed: '
         + result.stderr.decode('utf-8', 'replace')[-1200:])
    return result.stdout


def parse_index(raw, targets):
    need(raw[:4] == b'DIRC' and len(raw) >= 32, 'whole DIRC index')
    version, count = struct.unpack('>II', raw[4:12])
    need(version == 2 and hashlib.sha1(raw[:-20]).digest() == raw[-20:], 'audited v2 checksum')
    offset = 12
    entries, protected, paths = [], [], []
    for _ in range(count):
        start = offset
        need(offset + 62 < len(raw) - 20, 'whole v2 header')
        flags = struct.unpack('>H', raw[offset + 60:offset + 62])[0]
        need(flags & 0xF000 == 0, 'no unmerged/extended/assume-valid flags')
        end = raw.find(b'\0', offset + 62, len(raw) - 20)
        need(end >= 0, 'whole pathname terminator')
        path = raw[offset + 62:end]
        need(path and flags & 0xFFF == min(len(path), 0xFFF), 'native pathname length')
        offset = start + ((end + 1 - start + 7) // 8) * 8
        need(raw[end:offset] == b'\0' * (offset - end), 'native entry padding')
        mode = struct.unpack('>I', raw[start + 24:start + 28])[0]
        need(mode in [0o100644, 0o100755, 0o120000, 0o160000], 'audited native index mode')
        record = raw[start:offset]
        entries.append((path, record, mode, raw[start + 40:start + 60].hex()))
        paths.append(path)
        if path not in targets:
            protected.append((path, record))
    need(paths == sorted(paths) and len(paths) == len(set(paths)), 'unique byte-sorted stage0 paths')
    extensions = []
    while offset < len(raw) - 20:
        need(offset + 8 <= len(raw) - 20, 'whole extension header')
        key = raw[offset:offset + 4]
        length = struct.unpack('>I', raw[offset + 4:offset + 8])[0]
        offset += 8
        need(offset + length <= len(raw) - 20 and key == b'TREE', 'only audited TREE extension')
        body = raw[offset:offset + length]
        offset += length
        extensions.append((key.decode(), len(body), sha(body)))
    need(offset == len(raw) - 20 and len(extensions) <= 1, 'exact v2 extent')
    records = b'\0'.join(path + b'\t' + record.hex().encode() for path, record in protected) + b'\0'
    return {'version': version, 'count': count, 'entries': entries, 'protected': protected,
            'protected_record_count': len(protected), 'protected_raw_records_SHA256': sha(records),
            'whole_index_SHA256': sha(raw), 'extensions': extensions}


def sealed_namespace(root, seal_name, manifest_name, expected_seal, manifest_key, rows_key):
    seal_bytes = read(root / seal_name)
    need(sha(seal_bytes) == expected_seal, 'exact sealed packet: ' + str(root))
    seal = json.loads(seal_bytes)
    manifest_raw = read(root / manifest_name)
    expected = seal[manifest_key]
    need(sha(manifest_raw) == (expected['SHA256'] if isinstance(expected, dict) else expected), 'sealed manifest')
    manifest = json.loads(manifest_raw)
    values = manifest[rows_key]
    rows = ([dict(row, path=name) for name, row in values.items()]
            if isinstance(values, dict) else values)
    names = [r['path'] for r in rows]
    need(len(names) == len(set(names)) and set(namespace(root)) == set(names) | {seal_name, manifest_name},
         'complete exact owned packet extent')
    directory_key = 'exact_relative_directories' if rows_key == 'files' else 'directories'
    directories = sorted(p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir())
    need(directories == sorted(manifest[directory_key]), 'complete immutable packet directory extent')
    for row in rows:
        pin(root / safe_rel(row['path']), row)
    return seal, rows


def counts(root):
    text = read(root / 'research/index.html').decode()
    graphs = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', text, re.S)
    need(len(graphs) == 1, 'one research index graph')
    listing = json.loads(graphs[0])['mainEntity']
    need(listing['numberOfItems'] == len(listing['itemListElement']), 'actual research index count')
    return len(namespace(root)), listing['numberOfItems'], len(ET.fromstring(read(root / 'research/sitemap.xml')))


def stage_fences(mode):
    need(mode in ['baseline', 'installed'], 'bounded actual website state')
    seal, stage_rows = sealed_namespace(S, 'FINAL_SEAL.json', 'OWNED_MANIFEST.json',
                                        STAGE_SEAL, 'owned_manifest_SHA256', 'files')
    audit, audit_rows = sealed_namespace(A, 'FINAL_SEAL.json', 'OWNED_MANIFEST.json',
                                        AUDIT_SEAL, 'manifest', 'payloads')
    need(len(stage_rows) == 948 and len(audit_rows) == 941, 'whole current writer/audit extents')
    need(audit['writer_FINAL_SEAL_SHA256'] == STAGE_SEAL
         and audit['root_stage_code_adopted'] is False
         and seal['root_stage_code_adopted'] is False, 'historical unadopted flags remain unchanged')
    contract = obj(S / 'STAGE_CONTRACT.json')
    overlay = obj(S / 'OVERLAY_MANIFEST.json')['files']
    paths = [r['path'] for r in overlay]
    need(paths == contract['overlay_paths'] == sorted(set(paths)) and len(paths) == 11, 'exact11 ordered overlay')
    need(contract['baseline_counts'] == [605, 90, 91] and contract['virtual_counts'] == [614, 92, 93],
         'exact actual baseline/candidate counts')
    plan = obj(S / 'INSTALLATION_PLAN.json')
    need(plan['website_baseline_commit'] == BASE and plan['exact_future_public_relative_paths'] == paths
         and set(plan['existing_aggregate_overlays']) == AGGREGATES and plan['new_leaf_files'] == 9,
         'exact original installation-plan interface')
    rows = []
    for row in overlay:
        need(str(safe_rel(row['path'])).startswith('research/'), 'research-only target')
        body = pin(S / 'candidate-a/public' / row['path'], row)
        need(body == pin(S / 'candidate-b/public' / row['path'], row), 'whole paired payload equality')
        rows.append(dict(row, action='replace_aggregate_only' if row['path'] in AGGREGATES else 'add_new_leaf'))
    for candidate in ['candidate-a', 'candidate-b']:
        need(namespace(S / candidate / 'public') == paths, 'complete exact11 paired candidate extent')
    inputs = obj(S / 'INPUT_MANIFEST.json')
    allowed = {str(W / 'public' / p) for p in paths} if mode == 'installed' else set()
    for row in inputs['files']:
        original = pin(S / safe_rel(row['blob']), row)
        if row['path'] not in allowed:
            need(read(row['path']) == original, 'whole unchanged external source/site/config input')
    for ns in inputs['strict_source_editorial_namespaces']:
        need(namespace(Path(ns['root'])) == ns['exact_relative_file_names'], 'entire source/editorial namespace')
        dirs = sorted(p.relative_to(Path(ns['root'])).as_posix() for p in Path(ns['root']).rglob('*') if p.is_dir())
        need(dirs == ns['exact_relative_directory_names'], 'entire source/editorial directory extent')
    base = obj(S / 'WEBSITE_BASELINE.json')
    need(base['prior_installation_commit'] == BASE and base['baseline_counts'] == [605, 90, 91], 'fresh owner website baseline')
    public = [r for r in base['files'] if r['path'].startswith(str(W / 'public') + '/')]
    oldpaths = {str(Path(r['path']).relative_to(W / 'public')) for r in public}
    need(len(public) == len(oldpaths) == 605 and oldpaths & set(paths) == AGGREGATES, '605 old files and only two overlaps')
    expected = oldpaths if mode == 'baseline' else oldpaths | set(paths)
    need(set(namespace(W / 'public')) == expected, 'complete actual public namespace')
    for row in public:
        if mode == 'baseline' or str(Path(row['path']).relative_to(W / 'public')) not in paths:
            pin(row['path'], row)
    for row in rows:
        destination = W / 'public' / row['path']
        if mode == 'installed':
            pin(destination, row)
        elif row['action'] == 'add_new_leaf':
            need(not destination.exists() and not destination.is_symlink(), 'new leaf must remain absent')
    measured = list(counts(W / 'public'))
    need(measured == ([605, 90, 91] if mode == 'baseline' else [614, 92, 93]), 'fresh actual counts')
    # Paired overlay has only11 files; count its actual92/93 aggregates separately.
    candidate = S / 'candidate-a/public'
    _, number, sitemap = counts(candidate)
    need([len(oldpaths | set(paths)), number, sitemap] == [614, 92, 93], 'exact candidate union and aggregate counts')
    return rows, {'writer_owned': len(stage_rows), 'audit_owned': len(audit_rows),
                  'external_input_bindings': len(inputs['files']), 'actual_counts': measured,
                  'candidate_counts': [614, 92, 93], 'unrelated_public_files': 603}


def website_git_state(overlay, head=BASE, remote=True):
    need(git('rev-parse', '--show-toplevel').decode().strip() == str(W), 'exact website repository')
    need(git('rev-parse', '--show-object-format').strip() == b'sha1', 'audited SHA1 object format')
    need(git('symbolic-ref', 'HEAD').strip() == b'refs/heads/master'
         and git('rev-parse', 'HEAD').decode().strip() == head
         and git('rev-parse', 'refs/heads/master').decode().strip() == head, 'existing actual master/HEAD parent')
    gitdir = Path(git('rev-parse', '--absolute-git-dir').decode().strip())
    need(gitdir == W / '.git' and gitdir.is_dir() and not gitdir.is_symlink(), 'ordinary real gitdir')
    need(not (gitdir / 'index.lock').exists(), 'no existing index lock')
    targets = {('public/' + r['path']).encode() for r in overlay}
    raw = read(gitdir / 'index')
    index = parse_index(raw, targets)
    selected = {path for path, record, mode, oid in index['entries'] if path in targets}
    need(selected == {('public/' + p).encode() for p in AGGREGATES},
         'only two aggregate targets already indexed; all nine leaf targets absent')
    records = [r for r in git('ls-files', '--stage', '-z').split(b'\0') if r]
    parsed = [('%06o' % mode).encode() + b' ' + oid.encode() + b' 0\t' + path
              for path, record, mode, oid in index['entries']]
    need(records == parsed, 'whole raw index/ls-files stage tuple equality')
    urls = git('remote', 'get-url', '--push', '--all', 'origin').splitlines()
    need(len(urls) == 1 and urls[0] and b'\0' not in urls[0], 'one explicit actual origin push URL')
    if remote:
        advertisement = git('ls-remote', '--refs', urls[0].decode(), 'refs/heads/master')
        need(advertisement.split() == [BASE.encode(), b'refs/heads/master'], 'actual push-destination remote parent advertisement')
    else:
        advertisement = b''
    protected = [r for r in records if r.split(b'\t', 1)[1] not in targets]
    return raw, index, {'HEAD': head, 'master': head, 'branch': 'master', 'gitdir': str(gitdir),
                        'HEAD_file_SHA256': sha(read(gitdir / 'HEAD')),
                        'master_file_SHA256': sha(read(gitdir / 'refs/heads/master')),
                        'local_git_config_SHA256': sha(read(gitdir / 'config')),
                        'index_SHA256': sha(raw), 'index_record_count': index['count'],
                        'protected_record_count': index['protected_record_count'],
                        'protected_raw_records_SHA256': index['protected_raw_records_SHA256'],
                        'protected_stage_tuple_SHA256': sha(b'\0'.join(protected) + b'\0'),
                        'index_extensions': index['extensions'], 'origin_push_URL_SHA256': sha(urls[0]),
                        'remote_master_checked': remote, 'remote_master': BASE if remote else None,
                        'whole_remote_advertisement': advertisement.decode()}


def verify_preparation():
    seal = obj(O / 'PREPARATION_SEAL.json')
    need(sha(read(O / 'PREPARATION_MANIFEST.json')) == seal['MANIFEST_SHA256'], 'final preparation manifest')
    need(sha(read(O / 'PREPARATION_CLOSURE.json')) == seal['CLOSURE_SHA256'], 'actual preparation closure receipt')
    manifest = obj(O / 'PREPARATION_MANIFEST.json')
    excluded = {'PREPARATION_MANIFEST.json', 'PREPARATION_SEAL.json', 'PREPARATION_CLOSURE.json'}
    actual = {n for n in namespace(O) if not n.startswith('run-state/') and n not in excluded}
    need(actual == {r['path'] for r in manifest['files']}, 'complete sealed preparation payloads')
    need(len(actual) == seal['owned_payload_count'], 'complete final preparation extent')
    for row in manifest['files']:
        pin(O / safe_rel(row['path']), row)
    return seal


def adoption_fields(adoption):
    need(adoption.get('schema') == 'root_exact11_production_adoption_v1'
         and adoption.get('authority') == 'root' and adoption.get('template_not_root_receipt') is False,
         'actual root-authored receipt, never preparation template')
    for key in ['root_stage_adopted', 'independent_code_audit_adopted',
                'complete_current_helper_and_rendered_output_adopted', 'production_install_authorized']:
        need(adoption.get(key) is True, 'future explicit root authority: ' + key)
    message = adoption.get('commit_message')
    need(isinstance(message, str) and 0 < len(message) <= 300 and '\0' not in message,
         'bounded explicit commit message before any mutation')


def root_adoption(expected_sha):
    need(re.fullmatch('[0-9a-f]{64}', expected_sha or ''), 'explicit actual root receipt hash')
    need(ADOPTION.exists(), 'ROOT_ADOPTION_MISSING: current pair has no mutation authority')
    body = read(ADOPTION)
    need(sha(body) == expected_sha, 'whole actual root adoption receipt')
    adoption = json.loads(body)
    adoption_fields(adoption)
    root_reading()
    need(adoption['root_stage_reading_SHA256'] == ROOT_READING_SHA256,
         'future installation receipt binds the separate completed stage adoption')
    need(adoption['stage_root'] == str(S) and adoption['stage_final_seal_SHA256'] == STAGE_SEAL
         and adoption['independent_audit_final_seal_path'] == str(AUDIT)
         and adoption['independent_audit_final_seal_SHA256'] == AUDIT_SEAL, 'root adopted exact current pair and actual audit FINAL_SEAL')
    need(adoption['website_root'] == str(W) and adoption['website_HEAD'] == BASE
         and adoption['website_branch'] == 'master' and adoption['baseline_counts'] == [605, 90, 91]
         and adoption['candidate_counts'] == [614, 92, 93], 'root exact11 baseline and candidate authority')
    need(adoption['preparation_final_seal_SHA256'] == sha(read(O / 'PREPARATION_SEAL.json')), 'exact preparation adopted')
    verify_preparation()
    for name in CODE_FILES:
        need(adoption['code_files_SHA256'][name] == sha(read(O / name)), 'root personally adopted complete current body: ' + name)
    need(sha(read(AUDIT)) == AUDIT_SEAL and sha(read(S / 'FINAL_SEAL.json')) == STAGE_SEAL, 'actual adopted seals unchanged')
    need(adoption['hook_mode_octal'] == '0555'
         and (O / 'hooks/pre-push').stat().st_mode & 0o7777 == 0o555, 'required executable guard')
    need(adoption['public_relative_paths'] == [r['path'] for r in obj(S / 'OVERLAY_MANIFEST.json')['files']], 'root exact11 path order')
    capture = obj(O / 'PREFLIGHT_CAPTURE.json')
    need(adoption['preflight_capture_SHA256'] == sha(read(O / 'PREFLIGHT_CAPTURE.json'))
         and adoption['index_SHA256'] == capture['Git']['index_SHA256']
         and adoption['protected_raw_records_SHA256'] == capture['Git']['protected_raw_records_SHA256'],
         'root adopted exact fresh shared-index protection')
    return adoption
