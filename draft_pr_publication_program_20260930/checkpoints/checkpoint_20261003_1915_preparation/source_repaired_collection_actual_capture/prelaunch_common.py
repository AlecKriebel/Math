"""Proposed ROOT checkpoint primitives. SOURCE only until ROOT reviews and runs."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import shutil
import re

N = Path(__file__).absolute().parent
R = N.parents[2]
need_source_location = N == Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/checkpoints/checkpoint_20261003_1915_preparation')
assert need_source_location


def need(value, message):
    if not value:
        raise RuntimeError(message)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + '\n').encode()


def digest(body):
    return hashlib.sha256(body).hexdigest()


def path(relative):
    p = Path(relative)
    need(not p.is_absolute() and p.parts and all(v not in ('..', '.') for v in p.parts), 'Literal repository-relative path required')
    q = R / p
    for ancestor in [q] + list(q.parents):
        if ancestor == R.parent:
            break
        need(not ancestor.is_symlink(), 'No symlink path ancestor: ' + str(ancestor))
    return q


def regular_ref(q):
    before = q.lstat()
    need(stat.S_ISREG(before.st_mode) and not q.is_symlink(), 'Regular owned file required: ' + str(q))
    h = hashlib.sha256()
    git_hash = hashlib.sha1(('blob ' + str(before.st_size) + '\0').encode())
    with q.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
            git_hash.update(block)
    after = q.lstat()
    need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns, before.st_mode) ==
         (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns, after.st_mode), 'File changed while hashing')
    return dict(path=str(q.relative_to(R)), bytes=before.st_size, sha256=h.hexdigest(),
                full_mode=stat.S_IMODE(before.st_mode), git_blob_sha1=git_hash.hexdigest())


def plain_ref(q):
    v = regular_ref(q)
    del v['git_blob_sha1']
    return v


def exclusive(q, body, mode=0o644):
    fd = os.open(q, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(body)
            f.flush()
            os.fsync(f.fileno())
    except BaseException:
        raise


def load(q):
    return json.loads(q.read_bytes())


class Commands:
    """Truthful stream custody; large readonly enumerations are hashed in memory."""
    def __init__(self, root, operator_role='ROOT'):
        root.mkdir(exist_ok=False)
        self.root = root
        self.records = []
        need(operator_role in ['ROOT', 'SOURCE_PREPARER_READONLY'], 'Explicit command-record role')
        self.operator_role = operator_role

    def git(self, args, index=None, stdin=None, allowed_exit_codes=(0,)):
        if self.operator_role == 'SOURCE_PREPARER_READONLY':
            need(index is None and args and args[0] in ['branch', 'rev-parse', 'symbolic-ref', 'ls-files', 'diff', 'cat-file', 'config', 'check-attr'], 'Read-only SOURCE Git command only')
        d = self.root / ('command_%04d' % len(self.records))
        d.mkdir()
        argv = ['git'] + args
        env = os.environ.copy()
        for k in ['GIT_DIR', 'GIT_WORK_TREE', 'GIT_COMMON_DIR', 'GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY',
                  'GIT_ALTERNATE_OBJECT_DIRECTORIES', 'GIT_NAMESPACE', 'GIT_REPLACE_REF_BASE']:
            env.pop(k, None)
        env.update(GIT_OPTIONAL_LOCKS='0', GIT_LITERAL_PATHSPECS='1', GIT_NO_REPLACE_OBJECTS='1')
        if index is not None:
            env['GIT_INDEX_FILE'] = str(index)
        started = now()
        child = subprocess.Popen(argv, cwd=R, env=env, stdin=subprocess.PIPE if stdin is not None else subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        error = None
        try:
            out, err = child.communicate(stdin, timeout=180)
        except subprocess.TimeoutExpired:
            child.kill()
            out, err = child.communicate()
            error = 'timeout: actual child killed; complete returned streams retained'
        large_readonly_enumeration = bool(args and args[0] in ['ls-files', 'check-attr', 'config'])
        if large_readonly_enumeration:
            stdout = dict(bytes=len(out), sha256=digest(out), retained=False,
                          type='complete_readonly_enumeration_returned_in_memory_not_retained')
        else:
            exclusive(d / 'stdout.bin', out)
            stdout = dict(plain_ref(d / 'stdout.bin'), retained=True, type='complete_retained_stream')
        exclusive(d / 'stderr.bin', err)
        cap = dict(schema='ROOT-scoped-checkpoint-command/v1' if self.operator_role == 'ROOT' else 'SOURCE-preparer-readonly-checkpoint-command/v1', operator_role=self.operator_role, allowed_exit_codes=list(allowed_exit_codes), ROOT_approval=False, argv=argv, cwd=str(R), pid=child.pid,
                   started_utc=started, finished_utc=now(), exit_code=child.returncode, completed=True,
                   stdin_sha256=None if stdin is None else digest(stdin), error=error,
                   stdout=stdout, stderr=plain_ref(d / 'stderr.bin'),
                   private_index=None if index is None else str(index))
        exclusive(d / 'CAPTURE.json', encoded(cap))
        self.records.append(cap)
        need(error is None and child.returncode in allowed_exit_codes, 'Git child failed; full capture retained: ' + str(d))
        return out


def repository_gate(c, expected_head=None):
    need(c.git(['branch', '--show-current']).strip() == b'main', 'Stay on main')
    need(c.git(['rev-parse', '--show-toplevel']).strip() == os.fsencode(R), 'Exact repository')
    need(c.git(['rev-parse', '--show-object-format']).strip() == b'sha1', 'Explicitly supported SHA1 Git objects')
    head = c.git(['rev-parse', 'HEAD']).decode().strip()
    if expected_head is not None:
        need(head == expected_head, 'Stale main; refuse without adopting new HEAD')
    need(c.git(['symbolic-ref', 'HEAD']).strip() == b'refs/heads/main', 'Exact main reference')
    gitdir = Path(os.fsdecode(c.git(['rev-parse', '--absolute-git-dir']).strip()))
    need(gitdir.is_dir() and not gitdir.is_symlink(), 'Regular local Git directory')
    for name in ['MERGE_HEAD', 'CHERRY_PICK_HEAD', 'REVERT_HEAD', 'rebase-merge', 'rebase-apply', 'index.lock']:
        need(not (gitdir / name).exists() and not (gitdir / name).is_symlink(), 'Git operation/lock present: ' + name)
    # Index extensions requiring other mutable files are intentionally unsupported.
    index = gitdir / 'index'
    need(index.is_file() and not index.is_symlink(), 'Existing regular real index required')
    need(not list(gitdir.glob('sharedindex.*')), 'Split-index repositories need separate reviewed support')
    return head, gitdir, index


def entries(raw):
    result = {}
    for item in raw.split(b'\0'):
        if not item:
            continue
        lead, p = item.split(b'\t', 1)
        mode, oid, stage = lead.split(b' ')
        need(stage == b'0' and p not in result, 'No unmerged/duplicate index entries')
        result[p] = dict(mode=mode.decode(), oid=oid.decode(), stage=0)
    return result


def tags(raw):
    result = {}
    for item in raw.split(b'\0'):
        if item:
            need(item[1:2] == b' ' and item[2:] not in result, 'Index flag parse')
            result[item[2:]] = chr(item[0])
    return result


def debug_flag_bits(raw):
    # --debug -z has literal NUL path records, followed by this fixed stat block.
    # Stat fields themselves are not compared: the complete integer flag bits are.
    chunks = raw.split(b'\0')
    if len(chunks) == 1:
        need(not raw, 'No unterminated debug path')
        return {}
    result = {}
    current = chunks[0]
    pattern = re.compile(br'  ctime: [0-9]+:[0-9]+\n  mtime: [0-9]+:[0-9]+\n  dev: [0-9]+\tino: [0-9]+\n  uid: [0-9]+\tgid: [0-9]+\n  size: [0-9]+\tflags: ([0-9a-fA-F]+)\n')
    for block in chunks[1:]:
        need(current and current not in result, 'Whole literal debug flags domain')
        match = pattern.match(block)
        need(match is not None, 'Unsupported debug-stat format; refuse before writes')
        result[current] = int(match.group(1), 16)
        current = block[match.end():]
    need(not current, 'Trailing unterminated debug path')
    return result


def table_hash(rows):
    return digest(encoded([[os.fsdecode(p), rows[p]] for p in sorted(rows)]))


def foreign_worktree(p):
    q = R / os.fsdecode(p)
    for a in q.parents:
        if a == R:
            break
        need(not a.is_symlink(), 'Foreign tracked ancestor is a symlink')
    if not q.exists() and not q.is_symlink():
        return dict(path=os.fsdecode(p), absent=True)
    s = q.lstat()
    if stat.S_ISLNK(s.st_mode):
        b = os.fsencode(os.readlink(q))
        return dict(path=os.fsdecode(p), kind='symlink', bytes=len(b), sha256=digest(b), full_mode=stat.S_IMODE(s.st_mode))
    need(stat.S_ISREG(s.st_mode), 'Foreign tracked nonregular body needs separate support')
    v = plain_ref(q)
    v['kind'] = 'regular'
    return v


def index_observation(c, owned, index=None):
    owned_bytes = {os.fsencode(p) for p in owned}
    all_rows = entries(c.git(['ls-files', '--stage', '-z'], index=index))
    all_tags = tags(c.git(['ls-files', '-v', '-z'], index=index))
    all_flag_bits = debug_flag_bits(c.git(['ls-files', '--debug', '-z'], index=index))
    need(set(all_flag_bits) == set(all_rows), 'Complete integer index flags domain')
    foreign = {p:v for p,v in all_rows.items() if p not in owned_bytes}
    flags = {p:v for p,v in all_tags.items() if p not in owned_bytes}
    flag_bits = {p:v for p,v in all_flag_bits.items() if p not in owned_bytes}
    need(set(flags) == set(foreign), 'Complete foreign index flags/domain')
    return dict(foreign_entries_count=len(foreign), foreign_entries_sha256=table_hash(foreign),
                foreign_flags_sha256=table_hash(flags), foreign_complete_flag_bits_sha256=table_hash(flag_bits)), all_rows


def conversion_configuration(c):
    raw = c.git(['config', '--null', '--get-regexp', r'^(core\.(autocrlf|safecrlf|filemode|attributesfile|ignorecase)|filter\..*)$'], allowed_exit_codes=(0, 1))
    return dict(bytes=len(raw), sha256=digest(raw), role='Complete relevant conversion configuration hash; exact-owned add overrides autocrlf and verifies raw blob identity')


def protection(c, owned, real_index):
    summary, rows = index_observation(c, owned)
    own = {os.fsencode(v) for v in owned}
    staged = {v for v in c.git(['diff', '--cached', '--name-only', '-z', '--no-renames']).split(b'\0') if v} - own
    dirty = {v for v in c.git(['diff', '--name-only', '-z', '--no-renames']).split(b'\0') if v} - own
    # These index blobs are bound by their complete object identities, not copied.
    staged_rows = []
    for p in sorted(staged):
        z = rows.get(p)
        if z is not None:
            c.git(['cat-file', '-e', z['oid'] + '^{blob}'])
        staged_rows.append(dict(path=os.fsdecode(p), index_entry=z))
    return dict(index_summary=summary, real_index=plain_ref(real_index), conversion_configuration=conversion_configuration(c), foreign_staged=staged_rows,
                foreign_dirty_worktree=[foreign_worktree(v) for v in sorted(staged | dirty)])


def same_protection(before, after, index_body_may_change=False):
    a = dict(before)
    b = dict(after)
    if index_body_may_change:
        need(a['real_index']['full_mode'] == b['real_index']['full_mode'], 'Real index full permission bits changed')
        a.pop('real_index')
        b.pop('real_index')
    need(a == b, 'Foreign index/flags/staged objects/full worktree bodies or modes changed')


def verify_owned(observed):
    for v in observed:
        need(regular_ref(path(v['path'])) == v, 'Owned body/full mode changed: ' + v['path'])


def verify_fixed_scope(scope):
    need(scope['schema'] == 'ROOT-exact-owned-research-checkpoint-scope/v1', 'Exact scope schema')
    fixed = {v['path']:v for v in scope['fixed_files']}
    need(len(fixed) == len(scope['fixed_files']), 'No duplicate scope path')
    for p, v in fixed.items():
        need(plain_ref(path(p)) == v, 'Frozen selected body/full mode changed: ' + p)
    drows = scope['fixed_directories']
    expected_dirs = {z['path']:z['full_mode'] for z in drows}
    need(len(expected_dirs) == len(drows), 'No duplicate directory')
    for p, mode in expected_dirs.items():
        q = path(p)
        need(q.is_dir() and stat.S_IMODE(q.lstat().st_mode) == mode, 'Selected directory full mode')
        for v in q.iterdir():
            rel = str(v.relative_to(R))
            need(rel in fixed or rel in expected_dirs, 'Unlisted/ongoing selected member: ' + rel)
    return set(fixed)


def verify_selected_index(c, owned, index):
    rows = entries(c.git(['ls-files', '--stage', '-z'], index=index))
    for v in owned:
        p = os.fsencode(v['path'])
        expected_mode = '100755' if v['full_mode'] & stat.S_IXUSR else '100644'
        need(rows.get(p) == dict(mode=expected_mode, oid=v['git_blob_sha1'], stage=0), 'Exact selected Git blob/mode: ' + v['path'])
    return rows


def verify_plain_refs(rows):
    for row in rows:
        need(plain_ref(path(row['path'])) == row, 'Actual retained SOURCE body/type/bytes/full mode changed: ' + row['path'])


def source_prelaunch(run, phase):
    rows = []
    for name in ['common.py', phase + '_checkpoint.py', 'SCOPE.json', 'SOURCE_READY.json']:
        q = run / ('PRELAUNCH_' + phase + '_' + name)
        exclusive(q, (N / name).read_bytes())
        rows.append(plain_ref(q))
    return rows


def disk_preflight(index, selected_bytes=0):
    # At most three extra complete index bodies coexist in this procedure.
    # New Git objects are conservatively bounded by all selected uncompressed
    # bytes; selected scientific/archival bodies themselves are never copied.
    free = shutil.disk_usage(R).free
    required = selected_bytes + 3 * index.stat().st_size + 24 * 1024 * 1024
    need(free >= required, 'Insufficient free space before owned staging/locks; no speculative continuation')
    return dict(observed_utc=now(), available_bytes=free, required_bytes=required,
                index_bytes=index.stat().st_size, selected_uncompressed_object_upper_bound=selected_bytes,
                readonly_index_stdout_retained=False, observation_not_host_wide_reservation=True)


def directory_fsync(q):
    fd = os.open(q, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
