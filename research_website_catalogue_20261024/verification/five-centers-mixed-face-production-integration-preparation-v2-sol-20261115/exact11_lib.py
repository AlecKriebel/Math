"""Source-only held fences; live reads and installation require a later real root receipt."""
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
S = P / 'verification/five-centers-mixed-face-private-stage-sol-20261115'
A = P / 'verification/five-centers-mixed-face-independent-code-audit-sol-20261115'
BASE = '46773fd3d0e7289f5ab79bfc9f8ddf382fa508fc'
STAGE_SEAL = '1fb0b5d399d013a729e3d709e18581e011d1643f88e1622f63dd62d2169cd24f'
AUDIT = A / 'FINAL_SEAL.json'
AUDIT_SEAL = 'c80ea0ca5c4aca8137ecf1bffca4c8effad7ddd81489c1c0153e6b150580f4ec'
ADOPTION = P / 'verification/root-five-centers-mixed-face-stage-adoption-20261115.json'
COMMIT_APPROVAL = P / 'verification/root-five-centers-mixed-face-commit-approval-20261115.json'
ROOT_READING = P / 'verification/root-five-centers-mixed-face-stage-reading-20261115.json'
ROOT_READING_SHA256 = '339e9a0e1d109dd54dfd52ca5143ac852a643332c896596a521bc9828195cbde'
LIVE_AUTHORIZED = False
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
    need(LIVE_AUTHORIZED or not live_path(path), 'source-only: no website or .git access')
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
    return extent(root)[0]


def extent(root):
    root = Path(root)
    need(LIVE_AUTHORIZED or not live_path(root), 'source-only: no live namespace inspection')
    need(stat.S_ISDIR(root.lstat().st_mode) and root.resolve() == root, 'ordinary real directory root')
    files, directories = [], []
    def walk(directory):
        with os.scandir(directory) as entries:
            for entry in entries:
                path = Path(entry.path)
                mode = entry.stat(follow_symlinks=False).st_mode
                relative = path.relative_to(root).as_posix()
                if stat.S_ISDIR(mode):
                    directories.append(relative)
                    walk(path)
                else:
                    need(stat.S_ISREG(mode), 'reject symlink or special namespace entry: ' + relative)
                    files.append(relative)
    walk(root)
    return sorted(files), sorted(directories)


def live_path(path):
    return path == W or W in path.parents or '.git' in path.parts


def closed_namespace(root, files, directories, terminals=()):
    actual_files, actual_directories = extent(root)
    need(len(files) == len(set(files)) and actual_files == sorted(set(files) | set(terminals)),
         'exact ordinary file extent and exact root terminals only')
    need(directories == sorted(set(directories)) and actual_directories == directories,
         'exact declared directory extent, including legitimate empty directories')
    return actual_files, actual_directories


def root_reading():
    body = read(ROOT_READING)
    need(sha(body) == ROOT_READING_SHA256, 'separate actual root stage/copy/audit adoption')
    value = json.loads(body)
    need(value['root_stage_code_adopted'] is True
         and value['root_complete_current_copy_adopted'] is True
         and value['root_independent_integration_audit_adopted'] is True
         and value['source_only_production_helper_preparation_authorized'] is True
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
    need(LIVE_AUTHORIZED, 'source-only preparation cannot invoke Git')
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


def counts(root):
    text = read(root / 'research/index.html').decode()
    graphs = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', text, re.S)
    need(len(graphs) == 1, 'one research index graph')
    listing = json.loads(graphs[0])['mainEntity']
    need(listing['numberOfItems'] == len(listing['itemListElement']), 'actual research index count')
    return len(namespace(root)), listing['numberOfItems'], len(ET.fromstring(read(root / 'research/sitemap.xml')))


def sealed_namespace(kind):
    root = S if kind == 'writer' else A
    seal_bytes = read(root / 'FINAL_SEAL.json')
    need(sha(seal_bytes) == (STAGE_SEAL if kind == 'writer' else AUDIT_SEAL), 'exact current packet seal')
    seal = json.loads(seal_bytes)
    if kind == 'writer':
        name = 'OWNED_MANIFEST.json'
        descriptor = seal['manifest']
        excluded = {'OWNED_MANIFEST.json', 'FINAL_SEAL.json'}
    else:
        need(kind == 'audit', 'bounded current packet interface')
        name = 'FINAL_MANIFEST.json'
        descriptor = seal['bindings'][name]
        excluded = {'FINAL_CLOSURE.json', 'FINAL_MANIFEST.json', 'FINAL_SEAL.json'}
        pin(root / 'FINAL_CLOSURE.json', seal['bindings']['FINAL_CLOSURE.json'])
    manifest = json.loads(pin(root / name, descriptor))
    if kind == 'writer':
        rows = [dict(row, path=path) for path, row in manifest['payloads'].items()]
        need(len(rows) == 961 and seal['owned_payload_files'] == 961, 'actual writer961 interface')
        declared_directories = manifest['directories']
    else:
        # The independent manifest has absolute paths, unlike the writer manifest.
        rows = [dict(row, path=Path(row['path']).relative_to(root).as_posix())
                for row in manifest['files']]
        need(len(rows) == 721 and seal['own_final_owned_payloads'] == 721, 'actual audit721 interface')
        declared_directories = obj(O / 'SEALED_NAMESPACE_CONTRACT.json')['audit_directories']
    paths = [row['path'] for row in rows]
    contract = obj(O / 'SEALED_NAMESPACE_CONTRACT.json')
    need(declared_directories == contract[kind + '_directories'],
         'whole exact declared packet directories, including empty inputs')
    closed_namespace(root, paths, declared_directories, excluded)
    for row in rows:
        pin(root / safe_rel(row['path']), row)
    return seal, rows


def overlay_rows(overlay, plan):
    expected = [
        'research/five-outgoing-centers-alpha16/citation.bib',
        'research/five-outgoing-centers-alpha16/five_centers.pdf',
        'research/five-outgoing-centers-alpha16/five_centers.tex',
        'research/five-outgoing-centers-alpha16/index.html',
        'research/five-outgoing-centers-alpha16/verification-package.zip',
        'research/index.html', 'research/sitemap.xml',
        'research/totally-mixed-face-posets/citation.bib',
        'research/totally-mixed-face-posets/index.html',
        'research/totally-mixed-face-posets/totally-mixed-face-posets-source-and-verification.zip',
        'research/totally-mixed-face-posets/totally-mixed-face-posets.pdf']
    need([r['path'] for r in overlay] == plan['exact_future_public_relative_paths'] == expected,
         'exact new11 article-root paths including separate130TeX')
    need(set(plan['existing_aggregate_replacements']) == AGGREGATES
         and plan['baseline_counts'] == [614, 92, 93] and plan['proposed_counts'] == [623, 94, 95]
         and plan['actual_frozen_installed_baseline_commit'] == BASE, 'actual current plan interface')
    rows = []
    for row in overlay:
        need(row['whole_actual_normal_optimized_bytes_equal'] is True
             and row['role'] == ('aggregate' if row['path'] in AGGREGATES else 'new_leaf'),
             'actual current role and paired-byte fields')
        rows.append(dict(row, action='replace_aggregate_only' if row['path'] in AGGREGATES else 'add_new_leaf'))
    return rows


def core_fences(live=False):
    core = obj(A / 'CORE17_AND_AUTHORIZED_CHECKPOINT.json')
    prior = core['prior_whole_qualification']
    need(core['original17_files_unchanged'] == 17 and core['claim_all18_match_original_baseline'] is False
         and core['authorized_checkpoint_current_SHA256'] ==
         '405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0',
         'qualified17original plus authorized405b, never18original')
    need(len(core['current_actual_file_snapshots']) == 18, 'whole18 qualified current bindings')
    expected = {r['path']: r for r in prior['files']}
    for row in core['current_actual_file_snapshots']:
        source = row['source']
        need(source['bytes'] == expected[source['path']]['bytes']
             and source['SHA256'] == expected[source['path']]['SHA256'], 'whole retained qualified core interface')
        need(pin(Path(row['snapshot']['path']), row['snapshot']) == pin(Path(row['snapshot']['path']), source),
             'held actual core buffer, no source execution')
        if live:
            need(LIVE_AUTHORIZED, 'core live comparison requires later real authority')
            pin(Path(source['path']), source)
    if live:
        need(sorted(str(p) for p in (P / 'scripts').glob('*.py')) == prior['scripts_namespace'],
             'complete future current script namespace')
    return core


def stage_fences(mode):
    need(mode in ['held', 'baseline', 'installed'], 'bounded held/live state')
    live = mode != 'held'
    need(not live or LIVE_AUTHORIZED, 'no website access during source-only preparation')
    reading = root_reading()
    writer, writer_rows = sealed_namespace('writer')
    audit, audit_rows = sealed_namespace('audit')
    need(audit['writer_FINAL_SEAL_SHA256'] == STAGE_SEAL, 'independent audit binds this exact writer')
    need(writer['root_stage_code_adopted'] is False and writer['production_installation_authorized'] is False,
         'historical writer false flags retained, separate current root adoption used')
    rows = overlay_rows(obj(S / 'OVERLAY_MANIFEST.json')['files'], obj(S / 'INSTALLATION_PLAN.json'))
    paths = [r['path'] for r in rows]
    for row in rows:
        need(pin(S / 'candidate-a/public' / row['path'], row)
             == pin(S / 'candidate-b/public' / row['path'], row), 'whole paired current payloads')
    for candidate in ['candidate-a', 'candidate-b']:
        need(namespace(S / candidate / 'public') == paths, 'whole current11 counterpart namespace')
    source = obj(S / 'SOURCE_INPUTS.json')
    need(len(source['files']) == 341
         and [len(n['files']) for n in source['complete_original_namespaces']] == [121, 69, 81, 59],
         'current source341 and four complete namespaces')
    for row in source['files']:
        frozen = pin(S / safe_rel(row['blob']), row)
        if live:
            need(read(row['path']) == frozen, 'future unchanged source and original wrapper bytes')
    if live:
        for entry in source['complete_original_namespaces']:
            root = Path(entry['path'])
            need(namespace(root) == entry['files'], 'future whole source/editorial file namespace')
            need(sorted(p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir())
                 == entry['directories'], 'future whole original directory namespace')
    base = obj(S / 'WEBSITE_BASELINE.json')
    need(base['baseline_counts'] == [614, 92, 93] and base['proposed_counts'] == [623, 94, 95]
         and base['local_HEAD_and_origin_master_tracking'] == BASE
         and base['remote_server_ref_queried'] is False, 'actual held614 baseline, no invented server query')
    oldpaths = set(base['public_namespace'])
    need(len(oldpaths) == 614 and oldpaths & set(paths) == AGGREGATES
         and len(oldpaths - set(paths)) == 612 and len(oldpaths | set(paths)) == 623,
         'exact9new leaves/2aggregates and612 unrelated public paths')
    independent = obj(A / 'FRESH_WEBSITE_BASELINE.json')
    independent_rows = {r['public_relative_path']: r for r in independent['public_files']}
    need(set(independent_rows) == oldpaths and independent['HEAD'] == BASE, 'whole independent held614 interface')
    public = {}
    for row in base['files']:
        frozen = pin(S / safe_rel(row['blob']), row)
        path = Path(row['path'])
        if path.is_relative_to(W / 'public'):
            rel = path.relative_to(W / 'public').as_posix()
            other = independent_rows[rel]
            need(frozen == pin(Path(other['snapshot']['path']), other), 'whole independent/writer old public buffer')
            public[rel] = frozen
        if live and not (mode == 'installed' and path.is_relative_to(W / 'public')
                         and path.relative_to(W / 'public').as_posix() in paths):
            need(read(path) == frozen, 'future expected-before public/config/receipt byte fence')
    need(set(public) == oldpaths and len(base['files']) == 620, '614public plus6 nonpublic held rows')
    for row in independent['configs']:
        pin(Path(row['snapshot']['path']), row)
    core_fences(live)
    if live:
        expected = oldpaths if mode == 'baseline' else oldpaths | set(paths)
        need(set(namespace(W / 'public')) == expected, 'entire authorized future public namespace')
        expected_dirs = set(base['public_directories'])
        if mode == 'installed':
            expected_dirs |= {str(parent) for p in paths for parent in PurePosixPath(p).parents if str(parent) != '.'}
        need(sorted(p.relative_to(W / 'public').as_posix() for p in (W / 'public').rglob('*') if p.is_dir())
             == sorted(expected_dirs), 'future whole public directory namespace')
        for row in rows:
            destination = W / 'public' / row['path']
            if mode == 'installed':
                pin(destination, row)
            elif row['action'] == 'add_new_leaf':
                need(not destination.exists() and not destination.is_symlink(), 'future no-clobber new leaf absence')
        need(list(counts(W / 'public')) == ([614, 92, 93] if mode == 'baseline' else [623, 94, 95]),
             'future actual public/index/sitemap counts')
    for name, wanted in [('research/index.html', 94), ('research/sitemap.xml', 95)]:
        body = read(S / 'candidate-a/public' / name)
        if name.endswith('.xml'):
            need(len(ET.fromstring(body)) == wanted, 'held candidate sitemap95')
        else:
            match = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', body.decode(), re.S)
            need(len(match) == 1, 'one held candidate index graph')
            listing = json.loads(match[0])['mainEntity']
            need(listing['numberOfItems'] == len(listing['itemListElement']) == wanted, 'held candidate index94')
    return rows, {'mode': mode, 'writer_payloads': len(writer_rows), 'audit_payloads': len(audit_rows),
                  'source_originals': 341, 'held_baseline_counts': [614, 92, 93],
                  'candidate_counts': [623, 94, 95], 'unrelated_public_paths': 612,
                  'current_stage_and_independent_root_adoption_complete': True,
                  'website_or_dot_git_access': live, 'production_authority_from_this_preparation': False}




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
    files, directories = closed_namespace(O, [r['path'] for r in manifest['files']], manifest['directories'], excluded)
    actual = set(files) - excluded
    need(len(actual) == seal['owned_payload_count'], 'complete final preparation extent')
    for row in manifest['files']:
        pin(O / safe_rel(row['path']), row)
    return seal


def runtime_custody(root, preparation_sha, contract_body, held):
    """Pure finite durable-state custody; no authority or live-state observation."""
    contract = json.loads(contract_body)
    need(str(root) == contract['runtime_root'], 'one explicitly named separate runtime')
    try:
        root.lstat()
    except FileNotFoundError:
        return {'phase': 'ABSENT', 'live_state_reverified': False}
    files, directories = extent(root)
    state = obj(root / 'STATE.json')
    need(set(state) == {'schema', 'phase', 'preparation_final_seal_SHA256', 'runtime_contract_SHA256',
                       'root_adoption_SHA256', 'root_commit_approval_SHA256', 'files', 'directories'},
         'exact runtime state fields')
    need(state['schema'] == 'exact11-durable-runtime-state-v1'
         and state['preparation_final_seal_SHA256'] == preparation_sha
         and state['runtime_contract_SHA256'] == sha(contract_body), 'runtime bound to this whole preparation')
    phase = state['phase']
    need(phase in contract['phases'], 'finite durable runtime phase')
    permitted = contract['phases'][phase]
    need(set(state['files']) == set(permitted['files'])
         and files == sorted(permitted['files'] + ['STATE.json'])
         and directories == state['directories'] == permitted['directories'], 'exact finite runtime extent')
    bodies = {}
    for name, row in state['files'].items():
        need(set(row) == {'bytes', 'SHA256'}, 'exact runtime content descriptor')
        bodies[name] = pin(root / safe_rel(name), row)
    adoption = json.loads(bodies['ROOT_ADOPTION.json'])
    need(adoption.get('schema') == 'root_five_centers_mixed_face_exact11_production_adoption_v1'
         and adoption.get('authority') == 'root' and adoption.get('template_not_root_receipt') is False
         and all(adoption.get(k) is True for k in ['root_stage_adopted', 'independent_code_audit_adopted',
                 'complete_current_helper_and_rendered_output_adopted', 'production_install_authorized'])
         and adoption['preparation_final_seal_SHA256'] == preparation_sha
         and adoption['root_stage_reading_SHA256'] == contract['root_stage_reading_SHA256']
         and adoption['runtime_root'] == str(root) and adoption['runtime_contract_SHA256'] == sha(contract_body)
         and sha(bodies['ROOT_ADOPTION.json']) == state['root_adoption_SHA256'], 'bound actual root receipt copy')
    pre = json.loads(bodies['PRE_INSTALL.json'])
    need(pre['root_adoption_SHA256'] == state['root_adoption_SHA256']
         and pre['actual_parent'] == contract['parent']
         and ['public/' + row['path'] for row in pre['exact11']] == contract['gitpaths'], 'bound pre-install receipt')
    if phase != 'PUBLISHED':
        need(state['root_commit_approval_SHA256'] is None, 'no premature publication authority')
    if phase in ['INSTALLED', 'PUBLISHED']:
        pending = json.loads(bodies['PENDING_COMMIT.json'])
        need(pending['root_adoption_SHA256'] == state['root_adoption_SHA256']
             and pending['parent'] == contract['parent'] and pending['gitpaths'] == contract['gitpaths']
             and pending['public_counts'] == [623, 94, 95]
             and pending['shared_index_SHA256_unchanged'] == held['Git']['index_SHA256']
             and pending['protected_raw_records_SHA256'] == held['Git']['protected_raw_records_SHA256']
             and pending['temporary_index_SHA256'] == sha(bodies['commit.index']), 'bound pending commit and temporary index')
        need(all(re.fullmatch('[0-9a-f]{40}', pending[k]) for k in ['commit', 'tree']), 'bounded commit identifiers')
    if phase == 'PUBLISHED':
        approval = json.loads(bodies['ROOT_COMMIT_APPROVAL.json'])
        need(approval['schema'] == 'root_five_centers_mixed_face_exact11_commit_approval_v1'
             and sha(bodies['ROOT_COMMIT_APPROVAL.json']) == state['root_commit_approval_SHA256']
             and approval['authority'] == 'root' and approval['publication_authorized'] is True
             and approval['root_adoption_SHA256'] == state['root_adoption_SHA256']
             and approval['pending_commit_receipt_SHA256'] == sha(bodies['PENDING_COMMIT.json']), 'bound separate commit approval copy')
        for key in ['parent', 'commit', 'tree', 'gitpaths', 'protected_raw_records_SHA256']:
            need(approval[key] == pending[key], 'durable checked commit field: ' + key)
        prepub = json.loads(bodies['PRE_PUBLICATION.json'])
        need(prepub['root_adoption_SHA256'] == state['root_adoption_SHA256']
             and prepub['root_commit_approval_SHA256'] == state['root_commit_approval_SHA256']
             and prepub['old_index_SHA256'] == held['Git']['index_SHA256']
             and prepub['approved_index_SHA256'] == sha(bodies['shared-index.approved'])
             and prepub['commit'] == pending['commit'], 'bound validated publication buffer')
        publication = json.loads(bodies['PUBLICATION.json'])
        need(all(publication[k] == pending[k] for k in ['parent', 'commit', 'tree', 'gitpaths'])
             and publication['counts'] == [623, 94, 95]
             and publication['protected_raw_records_SHA256'] == pending['protected_raw_records_SHA256'],
             'bound durable publication receipt, not fresh live verification')
    return {'phase': phase, 'files': len(files), 'directories': len(directories), 'live_state_reverified': False}


def adoption_fields(adoption):
    need(adoption.get('schema') == 'root_five_centers_mixed_face_exact11_production_adoption_v1'
         and adoption.get('authority') == 'root' and adoption.get('template_not_root_receipt') is False,
         'actual root-authored receipt, never preparation template')
    for key in ['root_stage_adopted', 'independent_code_audit_adopted',
                'complete_current_helper_and_rendered_output_adopted', 'production_install_authorized']:
        need(adoption.get(key) is True, 'future explicit root authority: ' + key)
    message = adoption.get('commit_message')
    need(isinstance(message, str) and 0 < len(message) <= 300 and '\0' not in message,
         'bounded explicit commit message before any mutation')


def root_adoption(expected_sha):
    global LIVE_AUTHORIZED
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
         and adoption['website_branch'] == 'master' and adoption['baseline_counts'] == [614, 92, 93]
         and adoption['candidate_counts'] == [623, 94, 95], 'root exact11 baseline and candidate authority')
    need(adoption['preparation_final_seal_SHA256'] == sha(read(O / 'PREPARATION_SEAL.json')), 'exact preparation adopted')
    verify_preparation()
    runtime = read(O / 'RUNTIME_CONTRACT.json')
    need(adoption['runtime_root'] == json.loads(runtime)['runtime_root']
         and adoption['runtime_contract_SHA256'] == sha(runtime), 'future root explicitly adopts finite separate runtime')
    for name in CODE_FILES:
        need(adoption['code_files_SHA256'][name] == sha(read(O / name)), 'root personally adopted complete current body: ' + name)
    need(sha(read(AUDIT)) == AUDIT_SEAL and sha(read(S / 'FINAL_SEAL.json')) == STAGE_SEAL, 'actual adopted seals unchanged')
    need(adoption['hook_mode_octal'] == '0555'
         and (O / 'hooks/pre-push').stat().st_mode & 0o7777 == 0o555, 'required executable guard')
    need(adoption['public_relative_paths'] == [r['path'] for r in obj(S / 'OVERLAY_MANIFEST.json')['files']], 'root exact11 path order')
    capture = obj(O / 'HELD_BASELINE_CONTRACT.json')
    need(adoption['held_baseline_contract_SHA256'] == sha(read(O / 'HELD_BASELINE_CONTRACT.json'))
         and adoption['index_SHA256'] == capture['Git']['index_SHA256']
         and adoption['protected_raw_records_SHA256'] == capture['Git']['protected_raw_records_SHA256'],
         'root adopted exact held index protection; fresh live equality remains mandatory')
    LIVE_AUTHORIZED = True
    return adoption
