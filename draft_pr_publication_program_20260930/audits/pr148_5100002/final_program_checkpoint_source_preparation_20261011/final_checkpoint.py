"""Fixed PR148 final checkpoint, PREPARED SOURCE ONLY; no import-time operations.

Future ROOT sequence: render -> plan -> independent source/input/data/plan review
-> publish -> fresh ROOT selected-writer lease -> install -> separate ROOT receipt.
No phase, test or modeled acceptance has been executed by source preparation.
"""
import sys
sys.dont_write_bytecode = True
import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import re
import signal
import stat
import subprocess
import time
import types
from pathlib import Path

# Compile the complete source buffer, never import a possibly stale pyc file.
_metadata_body = Path(__file__).with_name('conditional_metadata.py').read_bytes()
m = types.ModuleType('pr148_conditional_metadata')
exec(compile(_metadata_body, str(Path(__file__).with_name('conditional_metadata.py')), 'exec'), m.__dict__)
require, digest, encoded = m.require, m.digest, m.encoded
TOTAL = 16 * 1024 * 1024
BODY = 512 * 1024
READ_PIN_CAP = 8 * 1024 * 1024
PRIVATE_INPUT_CAP = READ_PIN_CAP  # private proof-array input, not selected/review bodies
NATIVE_PIN_CAP = 32 * 1024 * 1024  # streamed in place, never copied/provider re-GET
CHILD_RESERVATION = 4 * 1024 * 1024
SOURCES = ('conditional_metadata.py', 'final_checkpoint.py', 'SOURCE_CONTRACT.json')
UPDATE_REFS = ('mutation($input:UpdateRefsInput!){updateRefs(input:$input){clientMutationId}}')

def regular(path):
    path = Path(path)
    require(path.is_absolute(), 'absolute path required')
    for part in (path, *path.parents):
        require(not part.is_symlink(), 'symlink path rejected: ' + str(part))
    st = path.stat()
    require(stat.S_ISREG(st.st_mode), 'regular file required: ' + str(path))
    return st

def body(path, cap=READ_PIN_CAP):
    st = regular(path)
    require(st.st_size <= cap, 'input body cap exceeded')
    data = Path(path).read_bytes()
    require(len(data) == st.st_size and stable_stat(regular(path)) == stable_stat(st), 'input changed during full read')
    return data

def file_pin(path):
    st = regular(path)
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    require(stable_stat(regular(path)) == stable_stat(st), 'file changed while hashing')
    return {'path': str(path), 'bytes': st.st_size, 'mode': stat.S_IMODE(st.st_mode), 'sha256': h.hexdigest()}

def stable_stat(st):
    return (st.st_dev, st.st_ino, st.st_mode, st.st_size, st.st_mtime_ns, st.st_ctime_ns)

def full_pins(value):
    """All native acceptance custody descriptors, including nested raw proofs."""
    if isinstance(value, dict):
        if set(('path', 'bytes', 'mode', 'sha256')) <= set(value):
            yield {k: value[k] for k in ('path', 'bytes', 'mode', 'sha256')}
        for child in value.values():
            yield from full_pins(child)
    elif isinstance(value, list):
        for child in value:
            yield from full_pins(child)

def read_pin(pin, cap=READ_PIN_CAP):
    require(isinstance(pin, dict) and set(('path', 'bytes', 'mode', 'sha256')) <= set(pin), 'full input pin required')
    require(file_pin(pin['path']) == {k: pin[k] for k in ('path', 'bytes', 'mode', 'sha256')}, 'full input pin mismatch')
    data = body(pin['path'], cap)
    require(len(data) == pin['bytes'] and digest(data) == pin['sha256'] and
            stat.S_IMODE(regular(pin['path']).st_mode) == pin['mode'], 'returned complete buffer differs from supplied pin')
    return data

def within(path, root):
    path, root = Path(path), Path(root)
    require(path.is_absolute() and path != root and root in path.parents, 'path outside owned scope')
    for part in (path, *path.parents):
        require(not part.is_symlink(), 'symlink ancestor rejected')
    return path

def member_map(rows, count):
    require(isinstance(rows, list) and len(rows) == count, 'exact native member count required')
    result = {}
    for row in rows:
        path = m.relative(row['relative_path'])
        require(path not in result and path not in m.SELECTED, 'duplicate/selected native path')
        pin = row['post_pin']
        require(pin['mode'] == 0o644 and re.fullmatch('[0-9a-f]{64}', pin['sha256']) and
                isinstance(pin['bytes'], int) and 0 <= pin['bytes'] <= NATIVE_PIN_CAP, 'native streamed post pin invalid')
        require(re.fullmatch('[0-9a-f]{40}', row['post_blob']) is not None, 'native blob absent')
        require(row['local_pin']['path'] == str(m.C / path), 'native local path differs')
        require({k: row['local_pin'][k] for k in ('bytes', 'mode', 'sha256')} == pin, 'native local/post pin differs')
        result[path] = row
    return result

def readonly_custody(rows, proof_pins):
    """Relative Git roles join actual absolute native copies, never C installs."""
    paths = ('unsolved_math_prioritization/SHORTLIST.md', 'unsolved_math_prioritization/manifest.json',
             'unsolved_math_prioritization/policy.json', 'unsolved_math_prioritization/queue.py')
    require(isinstance(rows, list) and len(rows) == 4 and {r['path'] for r in rows} == set(paths),
            'exact four relative read-only Git roles required')
    joined = []
    for row in rows:
        require(set(row) == {'path', 'bytes', 'mode', 'sha256', 'Git_blob'} and
                row['mode'] == 0o644 and re.fullmatch('[0-9a-f]{40}', row['Git_blob']) and
                re.fullmatch('[0-9a-f]{64}', row['sha256']), 'read-only Git descriptor invalid')
        matches = [p for p in proof_pins if all(p[k] == row[k] for k in ('bytes', 'mode', 'sha256'))]
        require(matches, 'read-only complete native proof copy absent')
        pin = sorted(matches, key=lambda p: p['path'])[0]
        within(pin['path'], m.A)
        require(file_pin(pin['path']) == pin, 'read-only native proof copy changed')
        before = regular(pin['path'])
        h = hashlib.sha1(b'blob ' + str(pin['bytes']).encode() + b'\0')
        with Path(pin['path']).open('rb') as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b''):
                h.update(chunk)
        require(stable_stat(before) == stable_stat(regular(pin['path'])) and h.hexdigest() == row['Git_blob'],
                'read-only complete proof copy/Git blob differs')
        joined.append({'relative_Git_role': row, 'absolute_native_proof_pin': pin})
    return joined

class Budget:
    """Explicit own-namespace ledger; only census while all children are closed."""
    def __init__(self):
        self.active = False
        self.total = self.census()

    def census(self):
        require(not self.active, 'no census while a child writer is active')
        total = 0
        for root, dirs, files in os.walk(m.S, followlinks=False):
            require(stat.S_IMODE(Path(root).stat().st_mode) == 0o755, 'owned directory mode differs')
            for name in dirs:
                require(not (Path(root) / name).is_symlink(), 'owned symlink directory')
            for name in files:
                st = regular(Path(root) / name)
                require(stat.S_IMODE(st.st_mode) == 0o644, 'owned file mode differs')
                total += st.st_size
        require(total <= TOTAL, 'own namespace16MiB cap exceeded')
        return total

    def reserve(self, count):
        require(not self.active and self.total + count <= TOTAL, 'complete dispatch envelope not admitted')

    def mkdir(self, path):
        path = within(path, m.S)
        require(not path.exists(), 'owned directory already exists')
        path.mkdir(mode=0o755)
        os.chmod(path, 0o755)

    def write(self, path, data):
        path = within(path, m.S)
        require(isinstance(data, bytes) and not self.active and self.total + len(data) <= TOTAL, 'complete buffer not admitted')
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        os.fchmod(fd, 0o644)
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        self.total += len(data)

    def normalize_private_git_modes(self, root):
        require(not self.active, 'mode normalization while child active')
        for folder, dirs, files in os.walk(root, followlinks=False):
            os.chmod(folder, 0o755)
            for name in dirs:
                require(not (Path(folder) / name).is_symlink(), 'private Git symlink')
            for name in files:
                require(not (Path(folder) / name).is_symlink(), 'private Git symlink')
                os.chmod(Path(folder) / name, 0o644)

    def identity_journal(self, path, data):
        # Small identity observations are inside the pre-admitted child envelope;
        # no census and no stdout/stderr admission while a writer is active.
        path = within(path, m.S)
        require(self.active and isinstance(data, bytes) and len(data) <= 8192 and
                self.total + len(data) <= TOTAL, 'complete child identity journal not admitted')
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        os.fchmod(fd, 0o644)
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        self.total += len(data)

class Uncertain(RuntimeError):
    pass

class Transaction:
    def __init__(self, inputs_path, inputs_sha, review_path, review_sha, phase):
        require(inputs_path.parent == m.S and review_path.parent == m.S, 'ROOT input/review roles must be in own namespace')
        ib, rb = body(inputs_path, PRIVATE_INPUT_CAP), body(review_path, BODY)
        require(digest(ib) == inputs_sha and digest(rb) == review_sha, 'explicit input/review hashes differ')
        self.i, self.review, self.input_sha = json.loads(ib), json.loads(rb), inputs_sha
        require(self.i['schema'] == 'pr148-final-checkpoint-inputs/v1', 'input schema differs')
        require(self.review.get('owner') == 'ROOT' and self.review.get('independent_adversarial_review_complete') is True,
                'genuine ROOT independent review required')
        require(self.review.get('inputs_sha256') == inputs_sha, 'review does not bind input bytes')
        expected = ('ACCEPTED_SOURCE_AND_INPUTS_FOR_RENDER_PLAN' if phase in ('render', 'plan')
                    else 'ACCEPTED_SOURCE_INPUT_DATA_AND_PLAN_FOR_PUBLICATION_AND_LOCAL3')
        require(self.review.get('status') == expected, 'review does not authorize this phase')
        self.sources = {}
        for name in SOURCES:
            pin = self.i['source_pins'][name]
            require(pin['path'] == str(m.S / name), 'source outside own namespace')
            read_pin(pin, BODY)
            require(self.review['source_sha256'][name] == pin['sha256'], 'review does not bind source')
            self.sources[name] = pin
        require(digest(_metadata_body) == self.sources['conditional_metadata.py']['sha256'], 'executed metadata source differs')
        require(file_pin(Path(__file__)) == self.sources['final_checkpoint.py'], 'executed runner source differs')
        self.native_pin, self.goal_pin = self.i['native_acceptance'], self.i['goal_observation']
        require(self.native_pin['path'] == str(m.C / m.NATIVE_ROLE), 'native gate role differs')
        self.native = json.loads(read_pin(self.native_pin, BODY))
        self.goal = json.loads(read_pin(self.goal_pin, BODY))
        m.actual_gate(self.native, self.goal, dt.datetime.now(dt.timezone.utc))
        self.members = member_map(self.native['native_members'], 33)
        self.changed_native = member_map(self.native['remote_changed_members'], 19)
        require(set(self.changed_native) <= set(self.members), 'public native paths not local native paths')
        for path, row in self.changed_native.items():
            require(row == self.members[path], 'public/local native row differs')
        self.unchanged_native = member_map(self.i['remote_unchanged_members'], 14)
        require(set(self.unchanged_native).isdisjoint(self.changed_native), 'native unchanged/changed overlap')
        require(set(self.unchanged_native) | set(self.changed_native) == set(self.members), 'native33 partition differs')
        for path, row in self.unchanged_native.items():
            require(row == self.members[path], 'unchanged native member data differs from actual native acceptance')
        self.proof_pins = self.i['native_full_proof_pins']
        require(len(self.proof_pins) >= 4, 'native full proof custody absent')
        require(self.review.get('native_transitive_raw_custody_complete') is True and
                self.review.get('native_full_proof_pins_sha256') == digest(encoded(self.proof_pins)),
                'ROOT review must verify complete transitive native raw custody, not merely a pin count')
        for key in ('published_operation_receipt', 'installed_operation_receipt'):
            require(self.native[key] in self.proof_pins, 'native operation receipt not in full proof pins')
        for pin in self.proof_pins:
            within(pin['path'], m.A)
        self.readonly = readonly_custody(self.native['readonly_dependencies'], self.proof_pins)
        # These four relative Git rows are explicitly joined above to authenticated
        # absolute proof copies; all other nested descriptors remain absolute files.
        absolute_native = {k: v for k, v in self.native.items() if k != 'readonly_dependencies'}
        custody = {}
        for pin in self.proof_pins + list(full_pins(absolute_native)):
            compact = {k: pin[k] for k in ('path', 'bytes', 'mode', 'sha256')}
            require(compact['path'] not in custody or custody[compact['path']] == compact, 'conflicting native full custody pins')
            custody[compact['path']] = compact
        self.native_custody_pins = list(custody.values())
        self.check_native_custody()
        require(len(self.native['readonly_dependencies']) == 4, 'native read-only dependency scope differs')
        require(set(self.i['remote_program_preimages']) == set(self.i['local_program_preimages']) ==
                set(self.i['remote_program_blobs']) == set(m.PROGRAM3), 'exact separately pinned remote3/local3 required')
        for path, expected_sha in m.FIXED_GATES.items():
            require(digest(body(m.C / path, BODY)) == expected_sha, 'fixed scientific/publication gate drift')
        self.archive = self.native['original_archive_pins']
        self.package = self.i['immutable_package_pins']
        require(len(self.archive) == 20 and len(self.package) == 78, 'frozen archive/package inventory count differs')
        require(len({p['path'] for p in self.archive}) == 20 and len({p['path'] for p in self.package}) == 78, 'duplicate frozen pins')
        for pin in self.archive:
            within(pin['path'], m.A)
        for pin in self.package:
            within(pin['path'], m.A / 'publication_package_v1')
        self.protected_files = [row['local_pin'] for row in self.members.values()] + self.archive + self.package
        self.check_local_protected()
        self.controls = self.control_digest()
        self.op = within(self.i['operation_namespace'], m.S)
        require(self.op.parent == m.S and re.fullmatch('ROOT_ACTUAL_FINAL_[A-Z0-9_]+', self.op.name), 'operation role invalid')
        self.workspace = self.op / 'object_workspace'
        self.budget = Budget()
        if phase == 'render':
            self.budget.mkdir(self.op)
        else:
            require(self.op.is_dir(), 'render operation missing')
        self.lock = self.op / 'OPERATION_LOCK'
        self.budget.mkdir(self.lock)
        self.budget.write(self.lock / 'OWNER.json', encoded({'actual_PID': os.getpid(), 'actual_UTC': self.now(), 'phase': phase,
                                                          'source_sha256': self.sources['final_checkpoint.py']['sha256']}))
        self.raw = self.op / ('raw_' + phase)
        self.budget.mkdir(self.raw)
        self.child_count = 0
        self.mutations_started = False
        self.closed_children = []
        self.phase = phase

    def now(self):
        return dt.datetime.now(dt.timezone.utc).isoformat()

    def check_local_protected(self):
        for pin in self.protected_files:
            require(file_pin(pin['path']) == pin, 'protected native/archive/package changed')

    def check_native_custody(self):
        for pin in self.native_custody_pins:
            require(file_pin(pin['path']) == pin, 'complete streamed native proof custody changed')

    def control_digest(self):
        # Stream every body/object and record all directory modes in both clones.
        rg, cgit = m.R / '.git', m.C / '.git'
        require(rg.is_dir() and not rg.is_symlink(), 'root Git directory absent')
        require(not cgit.is_symlink(), 'checkout Git symlink rejected')
        roots, records = [rg], []
        if cgit.is_dir():
            roots.append(cgit)  # Independent isolated clone, not a worktree file.
        else:
            pointer = body(cgit, 4096)
            require(pointer.startswith(b'gitdir: ') and len(pointer.splitlines()) == 1,
                    'checkout Git pointer invalid')
            target = Path(pointer.decode().strip()[8:])
            if not target.is_absolute():
                target = cgit.parent / target
            require(not any(p.is_symlink() for p in (target, *target.parents)), 'linked Git symlink rejected')
            target = target.resolve(strict=True)
            require(target.is_dir() and rg.resolve() in target.parents,
                    'linked checkout control directory not rooted in R/.git')
            records.append(file_pin(cgit))  # Complete target already in full R walk.
        def scan_error(error):
            raise error  # Never omit an unreadable/disappeared Git subtree.
        for gitroot in roots:
            for root, dirs, files in os.walk(gitroot, followlinks=False, onerror=scan_error):
                folder = Path(root)
                require(folder.is_dir() and not folder.is_symlink(), 'real Git directory invalid')
                records.append({'directory': str(folder), 'mode': stat.S_IMODE(folder.stat().st_mode)})
                for name in dirs:
                    require(not (folder / name).is_symlink(), 'real Git symlink directory')
                for name in files:
                    records.append(file_pin(folder / name))
        return digest(encoded(sorted(records, key=lambda x: x.get('path', x.get('directory')))))

    def final_checks(self):
        require(not self.budget.active, 'final census while active writer')
        for name, pin in self.sources.items():
            require(file_pin(m.S / name) == pin, 'source changed')
        read_pin(self.native_pin, BODY)
        read_pin(self.goal_pin, BODY)
        self.check_native_custody()
        self.check_local_protected()
        require(self.control_digest() == self.controls, 'real R/C Git controls/objects changed')
        self.budget.total = self.budget.census()

    def child(self, argv, stdin=b'', mutation=False, git_writer=False):
        require(isinstance(stdin, bytes) and len(stdin) <= 2 * BODY, 'stdin cap exceeded')
        self.budget.reserve(CHILD_RESERVATION + len(stdin))
        self.child_count += 1
        folder = self.raw / ('child_%04d' % self.child_count)
        self.budget.mkdir(folder)
        start = {'UTC': self.now(), 'argv': argv, 'stdin_sha256': digest(stdin), 'stdin_bytes': len(stdin),
                 'source_sha256': self.sources['final_checkpoint.py']['sha256'], 'inputs_sha256': self.input_sha,
                 'mutation': mutation, 'ordinary_pipes': True, 'timeout_seconds': 45}
        self.budget.write(folder / 'START.json', encoded(start))
        self.budget.write(folder / 'stdin.bin', stdin)
        env = {'PATH': '/usr/bin:/bin:/opt/homebrew/bin', 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8',
               'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_SYSTEM': '/dev/null',
               'GIT_DIR': str(self.workspace), 'GIT_OBJECT_DIRECTORY': str(self.workspace / 'objects'),
               'GIT_INDEX_FILE': str(self.workspace / 'unused-private-index'), 'GIT_TERMINAL_PROMPT': '0',
               'GH_HOST': 'github.com', 'GH_PROMPT_DISABLED': '1', 'GH_NO_UPDATE_NOTIFIER': '1',
               'GH_CONFIG_DIR': str(self.op / 'provider_config'), 'XDG_CACHE_HOME': str(self.op / 'cache')}
        token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
        if argv[0] == self.i['executables']['gh']['path']:
            require(token, 'ROOT must provide provider token in environment, never input or raw logs')
            env['GH_TOKEN'] = token
        self.budget.active = True
        if mutation:
            self.mutations_started = True
        try:
            try:
                proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        cwd=self.op, env=env, start_new_session=True)
            except BaseException as error:
                raise Uncertain('constructor failed; child acquisition/dispatch unknown; retain lock') from error
            self.budget.identity_journal(folder / 'ACQUIRED.json', encoded({'UTC': self.now(),
                    'actual_returned_PID': proc.pid, 'constructor_returned': True, 'actual_PGID': None,
                    'PGID_observation': 'NOT_YET_OBSERVED', 'reaped': False, 'group_closure': 'UNKNOWN'}))
            try:
                pgid = os.getpgid(proc.pid)
                self.budget.identity_journal(folder / 'IDENTITY.json', encoded({'UTC': self.now(),
                        'actual_returned_PID': proc.pid, 'actual_observed_PGID': pgid,
                        'PGID_observation': 'OBSERVED', 'reaped': False, 'group_closure': 'UNKNOWN'}))
                require(pgid == proc.pid, 'new child group differs')
            except BaseException as error:
                raise Uncertain('actual child PGID unavailable; retain lock') from error
            timeout = False
            try:
                stdout, stderr = proc.communicate(stdin, timeout=45)
            except subprocess.TimeoutExpired:
                timeout = True
                os.killpg(pgid, signal.SIGKILL)
                try:
                    stdout, stderr = proc.communicate(timeout=10)
                except BaseException as error:
                    raise Uncertain('pipes not closed after group kill; retain lock') from error
            proc.wait()
            self.budget.identity_journal(folder / 'REAPED.json', encoded({'UTC': self.now(),
                    'actual_returned_PID': proc.pid, 'actual_observed_PGID': pgid, 'reaped': True,
                    'ordinary_pipes_closed': True, 'group_closure': 'NOT_YET_CONFIRMED',
                    'buffered_full_stdout_bytes': len(stdout), 'buffered_full_stdout_sha256': digest(stdout),
                    'buffered_full_stderr_bytes': len(stderr), 'buffered_full_stderr_sha256': digest(stderr)}))
            deadline = time.monotonic() + 2
            while True:
                try:
                    os.killpg(pgid, 0)
                except ProcessLookupError:
                    break
                if time.monotonic() >= deadline:
                    raise Uncertain('obtained child reaped but group not absent; retain lock')
                os.killpg(pgid, signal.SIGKILL)
                time.sleep(0.01)
            self.budget.active = False
            if git_writer:
                self.budget.normalize_private_git_modes(self.workspace)
            # Full buffers are admitted after closure; no active child directory scan.
            self.budget.total = self.budget.census()
            require(self.budget.total + len(stdout) + len(stderr) + 8192 <= TOTAL, 'full closed output cannot fit; retain lock')
            self.budget.write(folder / 'stdout.bin', stdout)
            self.budget.write(folder / 'stderr.bin', stderr)
            receipt = {**start, 'closed_UTC': self.now(), 'actual_PID': proc.pid, 'actual_PGID': pgid,
                       'returncode': proc.returncode, 'timed_out': timeout, 'reaped': True, 'group_absent': True,
                       'full_stdout_sha256': digest(stdout), 'full_stdout_bytes': len(stdout),
                       'full_stderr_sha256': digest(stderr), 'full_stderr_bytes': len(stderr)}
            self.budget.write(folder / 'EXECUTION.json', encoded(receipt))
            self.closed_children.append(receipt)
            require(len(stdout) <= 2 * BODY and len(stderr) <= BODY, 'closed child output exceeds semantic body cap')
            require(not timeout and proc.returncode == 0, 'child failed; no automatic retry')
            return stdout
        except BaseException:
            # No operation is retried. Even an uncertain constructor leaves the
            # owned lock and START/complete stdin intact for independent ROOT audit.
            raise

    def git(self, args, stdin=b'', writer=False):
        pin = self.i['executables']['git']
        read_pin(pin, 64 * 1024 * 1024)
        return self.child([pin['path'], '-c', 'gc.auto=0', '-c', 'core.hooksPath=/dev/null', *args], stdin, git_writer=writer)

    def api(self, endpoint, payload=None):
        pin = self.i['executables']['gh']
        read_pin(pin, 64 * 1024 * 1024)
        argv = [pin['path'], 'api', '--hostname', 'github.com', '--method', 'POST' if payload is not None else 'GET', endpoint]
        data = b''
        if payload is not None:
            argv += ['--input', '-']
            data = encoded(payload)
        out = self.child(argv, data, mutation=payload is not None)
        result = json.loads(out)
        require(isinstance(result, dict) and not result.get('errors'), 'provider returned errors; no automatic retry')
        return result

    def repo_endpoint(self, tail):
        repo = self.i['repository']
        require(re.fullmatch('[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo), 'repository format differs')
        return 'repos/' + repo + '/git/' + tail

    def verify_repository(self):
        # Bind REST object endpoints and the GraphQL CAS node to one actual repo.
        self.repo_endpoint('')
        data = self.api('repos/' + self.i['repository'])
        require(data['full_name'].casefold() == self.i['repository'].casefold() and
                data['node_id'] == self.i['repository_node_id'], 'REST repository and GraphQL CAS repository differ')

    def ref(self):
        data = self.api(self.repo_endpoint('ref/heads/main'))
        require(data.get('ref') == 'refs/heads/main' and data['object']['type'] == 'commit', 'main reference response differs')
        return data['object']['sha']

    def remote_tree(self, oid, cache):
        if oid not in cache:
            data = self.api(self.repo_endpoint('trees/' + oid))
            require(data['sha'] == oid and data.get('truncated') is False, 'full direct provider tree required')
            entries = {}
            for row in data['tree']:
                name = row['path']
                require('/' not in name and name not in entries and name not in ('.', '..', '.git'), 'provider tree entry invalid')
                entries[name] = (row['mode'], row['type'], row['sha'])
            require(self.tree_oid(entries) == oid, 'provider tree complete bytes/OID differ')
            cache[oid] = entries
        return cache[oid]

    def remote_lookup(self, tree, path, cache):
        parts = m.relative(path).split('/')
        for pos, name in enumerate(parts):
            entries = self.remote_tree(tree, cache)
            require(name in entries, 'provider path absent: ' + path)
            mode, kind, oid = entries[name]
            if pos == len(parts) - 1:
                return mode, kind, oid
            require(kind == 'tree', 'provider ancestor not tree')
            tree = oid

    def remote_blob(self, oid):
        data = self.api(self.repo_endpoint('blobs/' + oid))
        require(data['sha'] == oid and data.get('encoding') == 'base64', 'full base64 provider blob required')
        result = base64.b64decode(data['content'].replace('\n', ''), validate=True)
        require(len(result) == data['size'] and self.object_oid('blob', result) == oid, 'provider full blob bytes/OID differ')
        return result

    def remote_commit(self, oid):
        data = self.api(self.repo_endpoint('commits/' + oid))
        require(data['sha'] == oid and data['tree']['sha'], 'provider commit response differs')
        return data

    @staticmethod
    def object_oid(kind, data):
        return hashlib.sha1((kind + ' ' + str(len(data)) + '\0').encode() + data).hexdigest()

    @staticmethod
    def tree_oid(entries):
        # Git sorts subtrees as if their names end in slash.
        parts = []
        for name in sorted(entries, key=lambda n: (n + ('/' if entries[n][1] == 'tree' else '')).encode()):
            mode, kind, oid = entries[name]
            parts.append((mode.lstrip('0') + ' ' + name).encode() + b'\0' + bytes.fromhex(oid))
        return Transaction.object_oid('tree', b''.join(parts))

    def local_tree(self, oid, cache):
        if oid not in cache:
            out = self.git(['ls-tree', '-z', oid])
            entries = {}
            for row in out.split(b'\0'):
                if row:
                    head, name = row.split(b'\t', 1)
                    mode, kind, child = head.decode().split(' ')
                    name = name.decode('utf-8')
                    require(name not in entries, 'duplicate local tree entry')
                    entries[name] = (mode, kind, child)
            require(self.tree_oid(entries) == oid, 'local complete tree/OID differ')
            cache[oid] = entries
        return cache[oid]

    def local_lookup(self, tree, path, cache):
        parts = m.relative(path).split('/')
        for pos, name in enumerate(parts):
            entries = self.local_tree(tree, cache)
            if name not in entries:
                return None
            item = entries[name]
            if pos == len(parts) - 1:
                return item
            require(item[1] == 'tree', 'overlay ancestor not directory')
            tree = item[2]

    def render(self):
        self.budget.mkdir(self.op / 'rendered')
        remote, local = {}, {}
        for path in m.PROGRAM3:
            rp, lp = self.i['remote_program_preimages'][path], self.i['local_program_preimages'][path]
            require(lp['path'] == str(m.C / path), 'local program role differs')
            within(rp['path'], m.A)
            remote[path], local[path] = read_pin(rp, BODY), read_pin(lp, BODY)
        proposals = m.render(remote, local, self.native, self.goal,
                             {'native': self.native_pin, 'goal': self.goal_pin}, dt.datetime.now(dt.timezone.utc))
        selected = {}
        for path in m.SELECTED:
            if path in proposals:
                data = proposals[path]
                target = self.op / 'rendered' / Path(path).name
                require(len(data) <= BODY, 'conditional postimage cap exceeded')
                self.budget.write(target, data)
            else:
                target = m.C / path
                data = body(target, BODY)
            require(len(data) <= BODY, 'selected body cap exceeded')
            selected[path] = file_pin(target)
        require(sum(p['bytes'] for p in selected.values()) <= 2 * 1024 * 1024, 'selected total exceeds2MiB')
        self.final_checks()
        self.budget.write(self.op / 'RENDER.json', encoded({'schema': 'pr148-conditional-render/v1', 'actual_preparation_UTC': self.now(),
                              'inputs_sha256': self.input_sha, 'selected': selected, 'source_pins': self.sources,
                              'real_controls_sha256': self.controls, 'actual_final_acceptance_claimed': False}))

    def plan(self):
        render = json.loads(body(self.op / 'RENDER.json', BODY))
        require(render['inputs_sha256'] == self.input_sha and render['source_pins'] == self.sources, 'render input/source drift')
        require(render['real_controls_sha256'] == self.controls, 'controls drift since render')
        selected = render['selected']
        require(set(selected) == set(m.SELECTED) and len(selected) <= 15, 'fixed selected scope differs')
        data = {p: read_pin(pin, BODY) for p, pin in selected.items()}
        self.budget.mkdir(self.workspace)
        # Hand-written minimal private bare repository; all writes are owned.
        for name in ('objects', 'refs'):
            self.budget.mkdir(self.workspace / name)
        self.budget.mkdir(self.workspace / 'objects/info')
        self.budget.mkdir(self.workspace / 'objects/pack')
        self.budget.write(self.workspace / 'HEAD', b'ref: refs/heads/main\n')
        self.budget.write(self.workspace / 'config', b'[core]\n\trepositoryformatversion = 0\n\tbare = true\n')
        native_workspace = Path(self.native['native_object_workspace'])
        within(native_workspace, m.A)
        require(native_workspace.is_dir() and not native_workspace.is_symlink(), 'accepted native objects unavailable')
        alternate = native_workspace / 'objects'
        require(alternate.is_dir() and not alternate.is_symlink(), 'accepted native object dir unavailable')
        roots = [alternate, m.R / '.git/objects']
        self.budget.write(self.workspace / 'objects/info/alternates', ('\n'.join(str(p) for p in roots) + '\n').encode())
        for name in ('provider_config', 'cache'):
            self.budget.mkdir(self.op / name)
        parent, base_tree = self.native['native_commit'], self.native['native_tree']
        self.verify_repository()
        parent_body = self.git(['cat-file', 'commit', parent])
        require(parent_body.split(b'\n', 1)[0] == ('tree ' + base_tree).encode(), 'accepted native commit/tree unavailable')
        require(self.ref() == parent, 'main drift from actual native commit')
        remote_parent = self.remote_commit(parent)
        require(remote_parent['tree']['sha'] == base_tree, 'provider accepted native tree differs')
        remote_cache = {}
        for path, pin in self.i['remote_program_preimages'].items():
            require(path in m.PROGRAM3, 'extra remote program preimage')
            mode, kind, oid = self.remote_lookup(base_tree, path, remote_cache)
            require(mode == '100644' and kind == 'blob' and oid == self.i['remote_program_blobs'][path], 'actual remote program path/mode/blob drift')
            require(self.remote_blob(oid) == read_pin(pin, BODY), 'remote program full preimage differs from separately supplied input')
        cache, blobs, changed = {}, {}, []
        for path, value in data.items():
            oid = self.git(['hash-object', '-w', '--stdin'], value, writer=True).decode().strip()
            require(oid == self.object_oid('blob', value), 'local new blob identity differs')
            blobs[path] = oid
            if self.local_lookup(base_tree, path, cache) != ('100644', 'blob', oid):
                changed.append(path)
        branches = {}
        for path, oid in blobs.items():
            node = branches
            parts = path.split('/')
            for name in parts[:-1]:
                node = node.setdefault(name, {})
            node[parts[-1]] = ('100644', 'blob', oid)
        trees = []
        def overlay(old_oid, node):
            entries = dict(self.local_tree(old_oid, cache)) if old_oid else {}
            for name, value in node.items():
                if isinstance(value, dict):
                    previous = entries.get(name)
                    require(previous is None or previous[1] == 'tree', 'new overlay ancestor conflict')
                    entries[name] = ('040000', 'tree', overlay(previous[2] if previous else None, value))
                else:
                    entries[name] = value
            rows = b''.join((' '.join(value) + '\t' + name).encode() + b'\0' for name, value in sorted(entries.items()))
            oid = self.git(['mktree', '-z'], rows, writer=True).decode().strip()
            require(oid == self.tree_oid(entries), 'new tree identity differs')
            if oid != old_oid:
                trees.append({'oid': oid, 'entries': entries})
            return oid
        tree = overlay(base_tree, branches)
        ident = self.i['commit_identity']
        require(re.fullmatch('[^<>\r\n]+', ident['name']) and re.fullmatch(r'[^<>\s]+@[^<>\s]+', ident['email']), 'explicit reviewed commit identity required')
        epoch = int(dt.datetime.now(dt.timezone.utc).timestamp())
        author = ident['name'] + ' <' + ident['email'] + '> ' + str(epoch) + ' +0000'
        commit_body = ('tree ' + tree + '\nparent ' + parent + '\nauthor ' + author + '\ncommitter ' + author +
                       '\n\nPR148 conditional final program checkpoint;27/99,15 published\n').encode()
        commit = self.git(['hash-object', '-t', 'commit', '-w', '--stdin'], commit_body, writer=True).decode().strip()
        require(commit == self.object_oid('commit', commit_body), 'new commit identity differs')
        diff = self.git(['diff-tree', '--no-commit-id', '--name-only', '-r', '-z', parent, commit])
        require(set(x.decode() for x in diff.split(b'\0') if x) == set(changed), 'exact selected diff differs')
        require([x for x in commit_body.splitlines() if x.startswith(b'parent ')] == [('parent ' + parent).encode()], 'sole parent differs')
        for path, row in self.members.items():
            require(self.local_lookup(tree, path, cache) == self.local_lookup(base_tree, path, cache) ==
                    ('100644', 'blob', row['post_blob']), 'native33 overlay changed')
        for joined in self.readonly:
            row = joined['relative_Git_role']
            require(self.local_lookup(tree, row['path'], cache) == self.local_lookup(base_tree, row['path'], cache) ==
                    ('100644', 'blob', row['Git_blob']), 'read-only four overlay identities changed')
        require(self.ref() == parent, 'main drift during plan')
        self.final_checks()
        plan = {'schema': 'pr148-final-scoped-plan/v1', 'actual_preparation_UTC': self.now(), 'inputs_sha256': self.input_sha,
                'source_pins': self.sources, 'selected': selected, 'selected_blobs': blobs, 'changed_paths': sorted(changed),
                'sole_parent': parent, 'parent_tree': base_tree, 'tree': tree, 'commit': commit,
                'commit_body_base64': base64.b64encode(commit_body).decode(), 'new_trees_children_first': trees,
                'source_data_sha256': digest(encoded(selected)), 'real_controls_sha256': self.controls,
                'native33_preserved': True, 'whole_parent_outside_exact_overlay_preserved': True,
                'actual_publication_claimed': False, 'actual_local_installation_claimed': False,
                'raw_child_count': self.child_count, 'all_obtained_children_closed': True}
        self.budget.write(self.op / 'PLAN.json', encoded(plan))

    def load_reviewed_plan(self):
        pb = body(self.op / 'PLAN.json', BODY)
        plan = json.loads(pb)
        require(self.review.get('plan_sha256') == digest(pb) and self.review.get('source_data_sha256') == plan['source_data_sha256'], 'ROOT plan/data review differs')
        require(plan['inputs_sha256'] == self.input_sha and plan['source_pins'] == self.sources, 'reviewed plan source/input differs')
        require(set(plan['selected']) == set(m.SELECTED) and plan['sole_parent'] == self.native['native_commit'] and
                plan['parent_tree'] == self.native['native_tree'], 'reviewed plan scope/native base differs')
        require(plan['real_controls_sha256'] == self.controls, 'real Git controls changed since planning')
        selected = {path: read_pin(pin, BODY) for path, pin in plan['selected'].items()}
        require(digest(encoded(plan['selected'])) == plan['source_data_sha256'], 'source/data manifest differs')
        for path, value in selected.items():
            require(self.object_oid('blob', value) == plan['selected_blobs'][path], 'selected body/blob differs')
        return plan, selected

    def full_provider_readback(self, plan, selected, include_native=True):
        commit = self.remote_commit(plan['commit'])
        require(commit['tree']['sha'] == plan['tree'] and [p['sha'] for p in commit['parents']] == [plan['sole_parent']], 'actual final commit/tree/sole-parent differs')
        cache = {}
        checks = {}
        combined = {path: ('100644', plan['selected_blobs'][path], value) for path, value in selected.items()}
        for path, (mode, oid, value) in combined.items():
            require(self.remote_lookup(plan['tree'], path, cache) == (mode, 'blob', oid), 'direct full provider path/mode differs')
            require(self.remote_blob(oid) == value, 'direct full provider body differs')
            checks[path] = {'mode': mode, 'blob': oid, 'bytes': len(value), 'sha256': digest(value)}
        if include_native:
            # The actual native gate already verifies these immutable full bodies.
            # Native19 raw payloads total51,207,361B; one full provider blob is
            #29,953,718B. Never duplicate those into this16MiB operation. Instead,
            # check final path/mode/OID against their fully authenticated custody.
            # The sole-parent exact selected-only overlay also proves every native
            # and foreign parent leaf retains its accepted object identity.
            for path, row in self.members.items():
                require(self.remote_lookup(plan['tree'], path, cache) == ('100644', 'blob', row['post_blob']),
                        'preserved native path/mode/immutable blob identity differs')
                require(file_pin(row['local_pin']['path']) == row['local_pin'], 'native complete local body custody differs')
                checks[path] = {'mode': '100644', 'blob': row['post_blob'], 'post_pin': row['post_pin'],
                                'full_body_custody_reused_from_genuine_native_acceptance': self.native_pin,
                                'fresh_duplicate_native_blob_GET_performed': False}
            for joined in self.readonly:
                row = joined['relative_Git_role']
                require(self.remote_lookup(plan['tree'], row['path'], cache) == ('100644', 'blob', row['Git_blob']),
                        'preserved read-only dependency Git identity differs')
                checks[row['path']] = {'mode': '100644', 'blob': row['Git_blob'],
                                      'full_body_custody': joined['absolute_native_proof_pin'],
                                      'read_only_Git_role_no_local_install': True}
        require(self.ref() == plan['commit'], 'main drift during full readback')
        return checks

    def publish(self):
        plan, selected = self.load_reviewed_plan()
        self.verify_repository()
        require(not (self.op / 'CAS_DISPATCH_ONCE.json').exists(), 'CAS was already marked; never replay')
        require(self.ref() == plan['sole_parent'], 'main drift before immutable publication')
        for path, data in selected.items():
            oid = plan['selected_blobs'][path]
            result = self.api(self.repo_endpoint('blobs'), {'content': base64.b64encode(data).decode(), 'encoding': 'base64'})
            require(result['sha'] == oid, 'provider new blob identity differs')
        for row in plan['new_trees_children_first']:
            entries = row['entries']
            require(self.tree_oid(entries) == row['oid'], 'planned tree identity differs')
            result = self.api(self.repo_endpoint('trees'), {'tree': [{'path': name, 'mode': value[0], 'type': value[1], 'sha': value[2]}
                                      for name, value in sorted(entries.items())]})
            require(result['sha'] == row['oid'], 'provider new tree identity differs')
        cb = base64.b64decode(plan['commit_body_base64'], validate=True)
        require(self.object_oid('commit', cb) == plan['commit'], 'planned commit bytes differ')
        header, message = cb.decode().split('\n\n', 1)
        match = re.search(r'^author (.+) <([^<>]+)> (\d+) \+0000$', header, re.M)
        require(match is not None, 'planned commit author absent')
        who = {'name': match.group(1), 'email': match.group(2), 'date': dt.datetime.fromtimestamp(int(match.group(3)), dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
        result = self.api(self.repo_endpoint('commits'), {'message': message, 'tree': plan['tree'], 'parents': [plan['sole_parent']],
                                                       'author': who, 'committer': who})
        require(result['sha'] == plan['commit'], 'provider immutable commit identity differs')
        self.verify_repository()
        require(self.ref() == plan['sole_parent'], 'main drift before single CAS')
        self.final_checks()
        # Durable once marker precedes dispatch. Unknown outcomes forbid replay.
        request = {'query': UPDATE_REFS, 'variables': {'input': {'repositoryId': self.i['repository_node_id'],
                    'refUpdates': [{'name': 'refs/heads/main', 'beforeOid': plan['sole_parent'], 'afterOid': plan['commit'], 'force': False}],
                    'clientMutationId': 'pr148-final-' + plan['commit']}}}
        self.budget.write(self.op / 'CAS_DISPATCH_ONCE.json', encoded({'UTC': self.now(), 'request_sha256': digest(encoded(request)),
                                'beforeOid': plan['sole_parent'], 'afterOid': plan['commit'], 'force': False, 'max_dispatches': 1}))
        result = self.api('graphql', request)
        require(result.get('data', {}).get('updateRefs', {}).get('clientMutationId') == 'pr148-final-' + plan['commit'], 'CAS response unknown or rejected; no retry')
        require(self.ref() == plan['commit'], 'CAS main readback differs')
        checks = self.full_provider_readback(plan, selected)
        self.final_checks()
        self.budget.write(self.op / 'PUBLISH.json', encoded({'schema': 'pr148-actual-final-checkpoint-publication/v1', 'UTC': self.now(),
                              'actual_PID': os.getpid(), 'commit': plan['commit'], 'sole_parent': plan['sole_parent'], 'tree': plan['tree'],
                              'single_nonforce_main_CAS_observed': True, 'selected_full_body_and_native_identity_readbacks': checks,
                              'native33_full_bodies_reused_from_authenticated_immutable_native_custody': True,
                              'all_obtained_children_reaped_groups_absent': True, 'raw_children': self.closed_children,
                              'plan_sha256': digest(body(self.op / 'PLAN.json', BODY)), 'source_data_sha256': plan['source_data_sha256'],
                              'local_installation_complete': False, 'final_ROOT_acceptance_claimed': False}))

    def install(self, lease_path, lease_sha):
        plan, selected = self.load_reviewed_plan()
        pub = json.loads(body(self.op / 'PUBLISH.json', BODY))
        require(pub['commit'] == plan['commit'] and pub['single_nonforce_main_CAS_observed'] is True, 'publication incomplete')
        lease_body = body(lease_path, BODY)
        require(digest(lease_body) == lease_sha, 'explicit writer lease hash differs')
        lease = json.loads(lease_body)
        require(lease.get('schema') == 'pr148-root-cooperative-selected-program3-writer/v1' and lease.get('owner') == 'ROOT' and
                lease.get('status') == 'EXCLUDED_OTHER_KNOWN_SELECTED_WRITERS', 'fresh ROOT cooperative selected writer required')
        require(sorted(lease['selected_paths']) == sorted(m.PROGRAM3) and lease['plan_sha256'] == digest(body(self.op / 'PLAN.json', BODY)), 'lease scope/plan differs')
        require(lease.get('known_selected_writer_roles') and lease.get('arbitrary_writer_exclusion_claimed') is False and
                lease.get('whole_install_atomic_claimed') is False and isinstance(lease.get('actual_ROOT_PID'), int), 'cooperative lease scope absent')
        lease_time = dt.datetime.fromisoformat(lease['UTC'].replace('Z', '+00:00'))
        require(lease_time.tzinfo is not None and 0 <= (dt.datetime.now(dt.timezone.utc) - lease_time).total_seconds() <= 1800, 'lease stale')
        # Fresh provider path/mode/full body checks precede local replacement.
        self.full_provider_readback(plan, {p: selected[p] for p in m.PROGRAM3}, include_native=False)
        require(0 <= (dt.datetime.now(dt.timezone.utc) - lease_time).total_seconds() <= 1800, 'lease expired during provider readback')
        for path in m.PROGRAM3:
            read_pin(self.i['local_program_preimages'][path], BODY)
        installed = {}
        for path in m.PROGRAM3:
            value = selected[path]
            dest = m.C / path
            require(file_pin(dest) == self.i['local_program_preimages'][path], 'local preimage changed immediately before replacement')
            self.check_local_protected()
            require(0 <= (dt.datetime.now(dt.timezone.utc) - lease_time).total_seconds() <= 1800, 'lease expired before replacement')
            temp = dest.with_name('.' + dest.name + '.PR148_OWNED_' + str(os.getpid()) + '_' + digest(value)[:12])
            require(not temp.exists() and not temp.is_symlink(), 'owned local temporary already exists')
            # Temporary is an individual program3 installer artifact. Its full
            # complete buffer is admitted explicitly, never an opaque disk quota.
            self.budget.reserve(len(value))
            fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
            os.fchmod(fd, 0o644)
            owned = os.fstat(fd)
            with os.fdopen(fd, 'wb') as f:
                f.write(value)
                f.flush()
                os.fsync(f.fileno())
            require(temp.stat().st_dev == owned.st_dev and temp.stat().st_ino == owned.st_ino and body(temp, BODY) == value, 'individual owned temporary differs')
            require(file_pin(dest) == self.i['local_program_preimages'][path], 'local preimage changed before atomic replace')
            os.replace(temp, dest)
            require(body(dest, BODY) == value and stat.S_IMODE(dest.stat().st_mode) == 0o644, 'local full postimage differs')
            installed[path] = file_pin(dest)
            self.budget.write(self.op / ('INSTALLED_' + Path(path).name + '.json'), encoded({'UTC': self.now(), 'path': path, 'post_pin': installed[path]}))
        # Separate sequential full readbacks; no global atomicity or file CAS.
        for path in m.PROGRAM3:
            require(body(m.C / path, BODY) == selected[path] and file_pin(m.C / path) == installed[path], 'final local3 full readback differs')
        self.final_checks()
        self.budget.write(self.op / 'INSTALL.json', encoded({'schema': 'pr148-actual-final-program3-install/v1', 'UTC': self.now(),
                              'actual_PID': os.getpid(), 'commit': plan['commit'], 'installed': installed,
                              'full_local_body_mode_readback': True, 'native33_package78_archive20_preserved': True,
                              'real_R_C_Git_controls_objects_preserved': True, 'cooperative_lease_sha256': lease_sha,
                              'whole_install_atomic': False, 'arbitrary_writer_exclusion': False, 'file_compare_and_swap_claimed': False,
                              'all_obtained_children_reaped_groups_absent': True, 'final_ROOT_acceptance_claimed': False,
                              'separate_final_ROOT_receipt_role': m.FINAL_ROLE}))

    def release(self):
        self.final_checks()
        # Release only this individually owned phase lock; failure/unknown keeps it.
        owner = json.loads(body(self.lock / 'OWNER.json', BODY))
        require(owner['actual_PID'] == os.getpid() and owner['phase'] == self.phase, 'lock ownership differs')
        (self.lock / 'OWNER.json').unlink()
        self.lock.rmdir()
        self.budget.total = self.budget.census()

def main():
    parser = argparse.ArgumentParser(description='PR148 prepared fixed final checkpoint; future ROOT authority required')
    parser.add_argument('phase', choices=('render', 'plan', 'publish', 'install'))
    for name in ('inputs', 'inputs-sha256', 'review', 'review-sha256'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--lease')
    parser.add_argument('--lease-sha256')
    args = parser.parse_args()
    tx = Transaction(Path(args.inputs), args.inputs_sha256, Path(args.review), args.review_sha256, args.phase)
    try:
        if args.phase == 'install':
            require(args.lease and args.lease_sha256, 'fresh separate ROOT writer lease required')
            tx.install(Path(args.lease), args.lease_sha256)
        else:
            getattr(tx, args.phase)()
        tx.release()
    except BaseException as error:
        # A failed phase retains its lock. ROOT audits complete custody before any
        # individually authorized recovery; the runner has no recovery/retry path.
        print('STOP; operation lock retained; ' + type(error).__name__ + ': ' + str(error), file=sys.stderr)
        raise

if __name__ == '__main__':
    main()
