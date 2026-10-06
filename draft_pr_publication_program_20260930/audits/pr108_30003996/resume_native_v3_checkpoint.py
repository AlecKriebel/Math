"""Preserve Git-reserved fixture paths and finish the interrupted own checkpoint."""
from pathlib import Path
import datetime, hashlib, io, json, os, subprocess, zipfile

A = Path(__file__).resolve().parent
C = A.parents[2]
D = A / 'actual_checkpoints/native_V3_review_resume_v2_20261006'
D.mkdir(parents=True, exist_ok=False)
records = []
first = '802ad19155b8a44506f512440dc18e70407f4c86'
remote = 'fb1eadba14d56b9f49409e31533242ac1b400e6b'

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def pin(path):
    body = path.read_bytes()
    return {'path': str(path.relative_to(C)), 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}

def run(*args):
    argv = ['git', *args]
    start = now()
    process = subprocess.Popen(argv, cwd=C, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    index = len(records)
    for stream, body in [('stdout', out), ('stderr', err)]:
        (D / (str(index) + '.' + stream + '.prefix.bin')).write_bytes(body[:4096])
    records.append({'argv': argv, 'PID': process.pid, 'UTC_start': start, 'UTC_end': now(),
                    'exit_code': process.returncode, 'stdout_bytes': len(out), 'stderr_bytes': len(err),
                    'stdout_sha256': hashlib.sha256(out).hexdigest(), 'stderr_sha256': hashlib.sha256(err).hexdigest(),
                    'retained_prefix_cap_bytes': 4096})
    (D / 'PROCESS_JOURNAL.json').write_text(json.dumps({'actual_operator_PID': os.getpid(), 'records': records}, indent=2) + '\n')
    require(process.returncode == 0, err.decode()[:1200])
    return out

require(run('symbolic-ref', '--short', 'HEAD').strip() == b'main', 'main required')
require(run('rev-parse', 'HEAD').strip().decode() == first, 'own interrupted commit changed')
require(run('rev-parse', first + '^').strip().decode() == remote, 'parent changed')
require(run('ls-remote', 'https://github.com/AlecKriebel/Math.git', 'refs/heads/main').decode().split()[0] == remote, 'remote changed')
require(not run('diff', '--cached', '--name-only', '-z'), 'foreign staged files')
selection = json.loads((A / 'NATIVE_V3_REVIEW_CHECKPOINT_SELECTION_20261006.json').read_bytes())
paths = sorted(set(selection['paths']))
stored = set(x.decode() for x in run('ls-tree', '-r', '--name-only', '-z', first).split(b'\0') if x)
reserved = []
verified = []
reserved_allowed = set()
for folder in [A / 'native_helper_v3_fresh_code_adversary_20261006',
               A / 'native_publication_integration_plan_20261006/corrected_v3']:
    manifest = json.loads((folder / 'OUTPUT_MANIFEST.json').read_bytes())
    for entry in manifest['files']:
        if entry['relative_path'].endswith('/private_config/repository/.git/config'):
            path = folder / entry['relative_path']
            actual = pin(path)
            require(actual['bytes'] == entry['bytes'] and actual['sha256'] == entry['sha256'], 'fixture manifest body')
            reserved_allowed.add(actual['path'])
for relative in paths:
    path = C / relative
    require(path.resolve().is_relative_to(C) and path.is_file() and not path.is_symlink(), 'unsafe selected path')
    body = path.read_bytes()
    expected = pin(path)
    if relative in stored:
        require(run('show', first + ':' + relative) == body, 'selected committed body differs: ' + relative)
        verified.append(expected)
    else:
        require('/.git/' in relative and len(body) <= 4096, 'unexpected uncommitted selection')
        require(relative in reserved_allowed, 'not an authenticated sealed fixture')
        reserved.append((relative, body, expected))
require(reserved, 'expected reserved fixture paths')
require({x[0] for x in reserved} == reserved_allowed, 'exact six sealed reserved fixture paths')
archive = A / 'NATIVE_V3_GIT_RESERVED_FIXTURE_BYTES_20261006.zip'
mapping = A / 'NATIVE_V3_GIT_RESERVED_FIXTURE_MAPPING_20261006.json'
require(not archive.exists() and not mapping.exists(), 'refuse to replace supplement')
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
    for relative, body, expected in reserved:
        info = zipfile.ZipInfo(relative, (2026, 10, 6, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        output.writestr(info, body)
with zipfile.ZipFile(archive) as source:
    require(source.namelist() == [x[0] for x in reserved], 'archive inventory')
    for relative, body, expected in reserved:
        require(source.read(relative) == body, 'archive body')
mapping.write_text(json.dumps({
    'schema': 'pr108-git-reserved-fixture-recovery-map/v1', 'UTC': now(), 'actual_operator_PID': os.getpid(),
    'interrupted_checkpoint': first, 'original_remote_parent': remote,
    'reason': 'Git ignores reserved .git/config fixture paths even with git add -f. Original sealed audit bytes and paths remain unchanged locally; archive supplies their exact public recovery bytes.',
    'archive': pin(archive), 'members': [x[2] for x in reserved],
    'recovery': 'Verify archive and member pins. Each archive member names the exact checkout-relative original path; restore only these regular fixture files in an audit checkout after checking no path is a live Git directory. Never extract into any unrelated checkout.',
    'native_source_or_mathematics_changed': False,
}, indent=2) + '\n')
extra = [archive, mapping, Path(__file__), A / 'actual_operations/native_V3_review_checkpoint_release/started.json',
         A / 'actual_operations/native_V3_review_checkpoint_release/execution.json',
         A / 'actual_operations/native_V3_review_checkpoint_release/stdout.bin',
         A / 'actual_operations/native_V3_review_checkpoint_release/stderr.bin']
extra.append(A / 'resume_native_v3_checkpoint_failed_scope_v1.py')
extra.extend(A / 'actual_operations/native_V3_review_checkpoint_resume' / name
             for name in ['started.json', 'execution.json', 'stdout.bin', 'stderr.bin'])
require(all(p.is_file() for p in extra), 'supplement missing')
extra_pins = [pin(p) for p in extra]
run('add', '-f', '--', *[x['path'] for x in extra_pins])
staged = sorted(x.decode() for x in run('diff', '--cached', '--name-only', '-z').split(b'\0') if x)
require(staged == sorted(x['path'] for x in extra_pins), 'supplement scope')
run('commit', '-m', 'Preserve exact PR108 Git-reserved audit fixture bytes')
second = run('rev-parse', 'HEAD').strip().decode()
require(run('rev-parse', second + '^').strip().decode() == first, 'supplement parent')
for expected in extra_pins:
    body = run('show', second + ':' + expected['path'])
    require(len(body) == expected['bytes'] and hashlib.sha256(body).hexdigest() == expected['sha256'], 'supplement committed body')
run('push', '--force-with-lease=refs/heads/main:' + remote, 'https://github.com/AlecKriebel/Math.git', 'HEAD:refs/heads/main')
require(run('ls-remote', 'https://github.com/AlecKriebel/Math.git', 'refs/heads/main').decode().split()[0] == second, 'remote readback')
require(not run('diff', '--cached', '--name-only', '-z'), 'index remainder')
receipt = {'schema': 'pr108-own-checkpoint-resume-actual-receipt/v1', 'UTC': now(), 'actual_operator_PID': os.getpid(),
           'first_commit': first, 'supplement_commit': second, 'remote_parent': remote, 'remote_verified': True,
           'complete_selected_files': len(paths), 'direct_Git_body_verified_count': len(verified),
           'archive_member_verified_count': len(reserved), 'direct_pins': verified, 'archive': pin(archive),
           'mapping': pin(mapping), 'supplement_pins': extra_pins, 'primary_checkout_mutated': False,
           'native_or_service_execution': False, 'original_failure_retained': True}
(D / 'RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k: v for k, v in receipt.items() if k not in ('direct_pins', 'supplement_pins')}))
