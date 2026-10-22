#!/usr/bin/env python3
"""Authenticate frozen raag-type partial results; replay source-free finite checks."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile

ACCEPTED = {'original/EDITION_MANIFEST.json': {'bytes': 1198, 'sha256': '00949c87a3adfa815c55af7b95df7e72da00ca64f382f401c0ca97f3ba0c7f19'}, 'original/LITERATURE_AND_SCOPE.md': {'bytes': 6085, 'sha256': '75d2a231c4e81f58f2c58442a6326252a7749ebac007d5dec0126156102d0453'}, 'original/README.md': {'bytes': 1134, 'sha256': '15aaa6b9cf3c69d2e8386be171a0995bde2fd2a1868cdcedd53417392beb751c'}, 'original/RESEARCH_REPORT.md': {'bytes': 24256, 'sha256': '97ea5742a67e4bd617eea51d1876b72b34b285f8e46ca4edf5a7bb5ee9808f1d'}, 'original/SOURCE_MANIFEST.json': {'bytes': 4441, 'sha256': '13315a1f54ce4fce05751432f52ef411d2608825178051a984c8ad6ce2c50791'}, 'original/VERIFICATION_RESULTS.json': {'bytes': 2985, 'sha256': 'bb55320a299063cf85efc4c016e55397645a1f9a5e6a919309b9cfface9d9d5c'}, 'original/verify_exact.py': {'bytes': 8617, 'sha256': '791cec4578a02ef1f5b1697df7631d2e5ce9ce79e4db353070983d1d0eefa7ff'}, 'audit/AUDIT_MANIFEST.json': {'bytes': 3002, 'sha256': 'a87355863db038d44d826d3e7df039c97e5684a8e319da81731008e2823b6d8f'}, 'audit/AUDIT_REPORT.md': {'bytes': 21293, 'sha256': '94ebc8710e612efa6bddb0d7b12001fa77df4fcc2e7e80691522200513d49da7'}, 'audit/CORRECTION_SCOPE.json': {'bytes': 533, 'sha256': '68a9511fe474cff4ae206e0f6770feed1c32698224add50675615dea32085e2b'}, 'audit/EXECUTION_AUDIT.json': {'bytes': 22612, 'sha256': '2af7b09fe2d370bbc2c110d147163c88ccf19c23ce23acc290d34157094f85c8'}, 'audit/INDEPENDENT_EXACT_RESULTS.json': {'bytes': 999, 'sha256': 'e913bddd1c6602d46492c548100690aa83d6c4ab66d748f253b7b5ef10120c43'}, 'audit/ORIGINAL_FREEZE_RECHECK.json': {'bytes': 1364, 'sha256': '0aec11d2eab42b76d7b81330cd8f1bb6c85b6178ac92a64134803fded3aba8bc'}, 'audit/PATCH_VALIDATION.json': {'bytes': 453, 'sha256': '064309d2714891944839076e075d3dd40352ce3250c69cd035bd26758a5847c2'}, 'audit/README.md': {'bytes': 2021, 'sha256': '84f739c2ce9f533e96e96f7622ce487d783098bc5dd5b34efe10a2bae0b355ba'}, 'audit/SCOPE_CLARIFICATIONS.patch': {'bytes': 3390, 'sha256': '083d2728179a30be7801e736d7f1c0b9cd904a0727da31c19e8877637dcb0023'}, 'audit/SOURCE_EXTRACTION_RECHECK.json': {'bytes': 1161, 'sha256': '54beb13d91dd79d4cdc43165572b81d60d32b2593de064f8aa5d99e34f8089e3'}, 'audit/SOURCE_IDENTITY_RECHECK.json': {'bytes': 1819, 'sha256': '9b4d4774c10f6cc8a23a6c211f291fcd7ce86867a6136d058351df7f5fda89db'}, 'audit/VERIFIER_CORRECTION.patch': {'bytes': 6807, 'sha256': '137fd6e21242e7dae7b94a609795b9569d853791067b55be7e9cf27081ac6f45'}, 'audit/independent_exact_check.py': {'bytes': 8912, 'sha256': 'f9600106e04ff6822b435337ed271274fa9e517667d88a59e0a5f7ff0d94a23f'}, 'audit/readonly_core_runner.py': {'bytes': 1396, 'sha256': 'e85d80893fd29e64981c053f9c762dc28fe1063c88890fc784cc9ee1dcd54f62'}, 'audit/run_readonly_audit.py': {'bytes': 8488, 'sha256': 'dfd1e0a41882574170de0e8dd8c571255912030a7eb9191484fb13a3470ebe05'}, 'audit/verify_exact_corrected.py': {'bytes': 9712, 'sha256': '6b624c31b8a061054ad06720798c04bd62a8e359f2077099db40f23cc855f7ae'}, 'corrected/CORRECTED_MANIFEST.json': {'bytes': 453, 'sha256': '7041f59837c542cfe38444012431386b9d5611ae31215965cf2c46e2c1e87e42'}, 'corrected/RESEARCH_REPORT.md': {'bytes': 24589, 'sha256': 'd6d61493e485c26f738632d96e84cb0e3f992894729b40f27dbabdc4177bfc92'}, 'corrected/verify_exact.py': {'bytes': 9712, 'sha256': '6b624c31b8a061054ad06720798c04bd62a8e359f2077099db40f23cc855f7ae'}}
ORIGINAL = {n.split('/', 1)[1] for n in ACCEPTED if n.startswith('original/')}
AUDIT = {n.split('/', 1)[1] for n in ACCEPTED if n.startswith('audit/')}
CORRECTED = {n.split('/', 1)[1] for n in ACCEPTED if n.startswith('corrected/')}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'original', 'audit', 'corrected'}
ORIGINAL_PIN = '00949c87a3adfa815c55af7b95df7e72da00ca64f382f401c0ca97f3ba0c7f19'
AUDIT_PIN = 'a87355863db038d44d826d3e7df039c97e5684a8e319da81731008e2823b6d8f'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def same(a, b):
    if type(a) is not type(b):
        return False
    if type(b) is dict:
        return set(a) == set(b) and all(same(a[k], v) for k, v in b.items())
    if type(b) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def nonfinite(value):
    raise ValueError('nonfinite JSON number')


def finite(value):
    result = float(value)
    need(math.isfinite(result), 'overflowed JSON number')
    return result


def parse(raw):
    return json.loads(raw, object_pairs_hook=unique, parse_constant=nonfinite, parse_float=finite)


def keys(obj, names):
    need(type(obj) is dict and set(obj) == set(names), 'exact object schema')


def exact_int(value, expected=None):
    need(type(value) is int and value >= 0 and (expected is None or value == expected), 'exact nonnegative integer')


def digest(value):
    need(type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None, 'lowercase SHA-256')


def inventory(root):
    for path in (root, *root.parents):
        need(stat.S_ISDIR(path.lstat().st_mode), 'linked/non-directory root or ancestor')
    files, dirs = set(), set()
    def visit(directory):
        for entry in os.scandir(directory):
            path = Path(entry.path)
            name = path.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                need(name in DIRS, 'extra directory')
                dirs.add(name)
                visit(path)
            else:
                need(stat.S_ISREG(mode), 'symlink or special member')
                files.add(name)
    visit(root)
    need(files == FILES and dirs == DIRS, 'exact recursive inventory')


def ordinary(path):
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_size <= 1000000, 'regular bounded member')
    with os.fdopen(os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)), 'rb') as stream:
        opened = os.fstat(stream.fileno())
        need((before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino), 'member replaced at open')
        raw = stream.read(1000001)
    need(len(raw) == before.st_size, 'member size changed')
    return raw


def manifest(value, snapshot, payload, role=None):
    keys(value, ['schema', 'problem_id', 'files'] + (['role'] if role is not None else []))
    if role is not None:
        need(same(value['role'], role), 'manifest role')
    exact_int(value['schema'], 1)
    exact_int(value['problem_id'], 2776)
    rows = value['files']
    need(type(rows) is list and len(rows) == len(payload), 'manifest list length/type')
    seen = set()
    for row in rows:
        keys(row, ['path', 'bytes', 'sha256'])
        name = row['path']
        need(type(name) is str and name in payload and name not in seen, 'unknown/duplicate manifest path')
        seen.add(name)
        exact_int(row['bytes']); digest(row['sha256'])
        need(same(row, dict(path=name, bytes=len(snapshot[name]), sha256=sha(snapshot[name]))), 'manifest byte binding')
    need(seen == payload, 'manifest inventory')


def integrity(root, manifest_pin, bootstrap_pin):
    digest(manifest_pin); digest(bootstrap_pin)
    inventory(root)
    snapshot = {name: ordinary(root/name) for name in FILES}
    need(sha(snapshot['PUBLICATION_MANIFEST.json']) == manifest_pin, 'external manifest pin')
    need(sha(snapshot['BOOTSTRAP.py']) == bootstrap_pin, 'external bootstrap pin')
    parsed = {name: parse(raw) for name, raw in snapshot.items() if name.endswith('.json')}
    manifest(parsed['PUBLICATION_MANIFEST.json'], snapshot, PAYLOAD)
    for name, row in ACCEPTED.items():
        need(same(row, dict(bytes=len(snapshot[name]), sha256=sha(snapshot[name]))), 'accepted evidence bytes changed')
    for prefix, names, name, pin in [
        ('original/', ORIGINAL, 'EDITION_MANIFEST.json', ORIGINAL_PIN),
        ('audit/', AUDIT, 'AUDIT_MANIFEST.json', AUDIT_PIN),
        ('corrected/', CORRECTED, 'CORRECTED_MANIFEST.json', ACCEPTED['corrected/CORRECTED_MANIFEST.json']['sha256'])]:
        need(sha(snapshot[prefix+name]) == pin, 'frozen manifest pin')
        value = parsed[prefix+name]
        rows = value['files']
        need(type(rows) is list and len(rows) == len(names)-1, 'frozen list count')
        seen = set()
        for row in rows:
            keys(row, ['path', 'bytes', 'sha256'])
            leaf = row['path']
            need(type(leaf) is str and leaf in names-{name} and leaf not in seen, 'frozen member name')
            seen.add(leaf)
            exact_int(row['bytes']); digest(row['sha256'])
            need(same(row, dict(path=leaf, bytes=len(snapshot[prefix+leaf]), sha256=sha(snapshot[prefix+leaf]))), 'frozen manifest binding')
        need(seen == names-{name}, 'frozen exact inventory')
    original = parsed['original/EDITION_MANIFEST.json']
    need(original['status'] == 'partial_unresolved' and original['novelty'] == 'not established', 'unsolved and novelty boundary')
    exact_int(original['mathematical_routes'], 5)
    need(original['source_documents_included'] is False, 'source boundary')
    audit = parsed['audit/AUDIT_MANIFEST.json']
    need(audit['disposition'] == 'partial_unresolved_after_five_routes' and audit['original_edition_unchanged'] is True, 'audit disposition')
    for name, patch_name in [('verify_exact.py','VERIFIER_CORRECTION.patch'), ('RESEARCH_REPORT.md','SCOPE_CLARIFICATIONS.patch')]:
        actual = apply_patch(snapshot['original/'+name], snapshot['audit/'+patch_name], name)
        need(actual == snapshot['corrected/'+name], 'actual patch differs from corrected slice')
    need(snapshot['corrected/verify_exact.py'] == snapshot['audit/verify_exact_corrected.py'], 'corrected verifier mismatch')
    inventory(root)
    return snapshot, parsed


def apply_patch(original, patch, name):
    """Apply exact-context unified hunks in memory, with no fuzzy matching."""
    lines = original.decode('utf-8').splitlines(keepends=True)
    changes = patch.decode('utf-8').splitlines(keepends=True)
    need(changes[0] == '--- original/'+name+'\n', 'patch old header')
    expected_new = 'corrected' if name == 'verify_exact.py' else 'clarified'
    need(changes[1] == '+++ '+expected_new+'/'+name+'\n', 'patch new header')
    result=[]; cursor=0; i=2
    while i < len(changes):
        match = re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@[^\n]*\n', changes[i])
        need(match is not None, 'exact unified hunk header')
        old_start, old_count, new_start, new_count = [int(x) if x is not None else 1 for x in match.groups()]
        start=old_start-1
        need(cursor <= start <= len(lines), 'ordered patch hunks')
        result.extend(lines[cursor:start]); cursor=start
        need(len(result) == new_start-1, 'patch output position')
        used_old=used_new=0; i+=1
        while i < len(changes) and not changes[i].startswith('@@ '):
            line=changes[i]; need(line[:1] in (' ', '+', '-'), 'patch line type')
            if line[0] in ' -':
                need(cursor < len(lines) and lines[cursor] == line[1:], 'exact patch context')
                cursor+=1; used_old+=1
            if line[0] in ' +':
                result.append(line[1:]); used_new+=1
            i+=1
        need((used_old, used_new) == (old_count, new_count), 'exact hunk line counts')
    result.extend(lines[cursor:])
    return ''.join(result).encode('utf-8')


def stable_audit(value):
    """Normalize only verified runtime provenance and temporary output locations."""
    import copy
    v=copy.deepcopy(value)
    need(type(v['python_version']) is str and v['python_version'].startswith('3.'), 'Python runtime string')
    v['python_version']='<runtime version>'
    for record in v['records']:
        if record['specimen']=='original_baseline' and record['execution']=='cli':
            need(type(record['stderr_last_line']) is str and re.fullmatch(
                r"PermissionError: \[Errno 13\] Permission denied: '/[^'\n]+/raag-audit-[^/'\n]+/original_baseline/VERIFICATION_RESULTS.json'",
                record['stderr_last_line']) is not None, 'expected read-only path failure')
            record['stderr_last_line']='PermissionError: original mandatory neighbor output write'
        if record['execution']=='cli_external':
            digest(record['stdout_sha256'])
            record['stdout_sha256']='<temporary output path acknowledgment>'
    return v


def replay(snapshot, parsed):
    need(hasattr(os, 'geteuid') and os.getuid() == os.geteuid() == 1000, 'real UID/EUID 1000 required')
    with tempfile.TemporaryDirectory(prefix='raag-type-publication-') as temporary:
        work = Path(temporary)
        for name in DIRS | {'cwd'}:
            (work/name).mkdir()
        for name in ACCEPTED:
            (work/name).write_bytes(snapshot[name])
        readonly = [work/name for name in sorted(DIRS | {'cwd'})]
        for directory in readonly:
            for path in directory.iterdir(): path.chmod(0o444)
            directory.chmod(0o555)
        denied=[]
        try:
            for path in [work/'original/NEW_FILE',work/'original/RESEARCH_REPORT.md',work/'audit/NEW_FILE',work/'audit/AUDIT_REPORT.md',work/'corrected/NEW_FILE',work/'corrected/verify_exact.py',work/'cwd/NEW_FILE']:
                try:
                    with path.open('ab') as stream: stream.write(b'forbidden')
                except PermissionError: denied.append(path.relative_to(work).as_posix())
                else: raise ValueError('read-only write succeeded')
            env=dict(PATH=os.defpath, HOME=str(work), TMPDIR=str(work), LC_ALL='C', PYTHONNOUSERSITE='1', PYTHONDONTWRITEBYTECODE='1', PYTHONSAFEPATH='1')
            flags=[] if sys.flags.optimize == 0 else ['-'+('O'*sys.flags.optimize)]
            def run(script, arguments):
                r=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(work/script),*arguments],cwd=work/'cwd',env=env,capture_output=True,timeout=300)
                need(r.returncode==0 and r.stderr==b'', 'accepted replay rejected')
                return r.stdout,parse(r.stdout)
            corrected_raw,corrected=run('corrected/verify_exact.py',[])
            need(corrected_raw==snapshot['original/VERIFICATION_RESULTS.json'], 'corrected exact frozen stdout')
            need(corrected['all_checks_passed'] is True, 'corrected finite checks')
            independent_raw,independent=run('audit/independent_exact_check.py',[])
            need(independent_raw==snapshot['audit/INDEPENDENT_EXACT_RESULTS.json'], 'independent exact frozen stdout')
            native_raw,native=run('audit/run_readonly_audit.py',[str(work/'original')])
            need(native['python_version']==sys.version, 'fresh actual Python version')
            need(same(stable_audit(native),stable_audit(parsed['audit/EXECUTION_AUDIT.json'])), 'native audit exact stable receipt')
            need(native['uid']==native['euid']==1000, 'native identity')
            exact_int(native['original_assert_nodes'],15);exact_int(native['corrected_assert_nodes'],0)
            exact_int(native['original_optimized_false_passes'],10);exact_int(native['corrected_mutations_rejected'],15)
            need(not list((work/'cwd').iterdir()), 'read-only cwd changed')
            for name in ACCEPTED: need((work/name).read_bytes()==snapshot[name], 'replay mutated evidence')
            return dict(corrected_output_sha256=sha(corrected_raw),independent_output_sha256=sha(independent_raw),
                original_assert_nodes=15,original_optimized_false_passes=10,corrected_mutations_rejected=15,
                original_cli_readonly='FAILS_MANDATORY_NEIGHBOR_WRITE_ALL_THREE_MODES',
                corrected_cli_readonly='PASS_ALL_THREE_MODES',native_process_runs=45,
                native_controls_own_modes=['normal','-O','-OO'],readonly_write_probes_denied=denied,
                python_version=sys.version.split()[0],historical_source_bindings='SIX_PDF_HASHES_AND_FIVE_TEXT_EXTRACTIONS_MATCHED_HISTORICALLY',
                fresh_source_bindings='NOT_RUN',imported_theorem_proofs='NOT_MACHINE_CERTIFIED',
                finite_cover_argument='WRITTEN_PROOF_NOT_COMPUTATION',novelty='NOT_ESTABLISHED',general_problem='UNSOLVED')
        finally:
            for directory in readonly:
                directory.chmod(0o755)
                for path in directory.iterdir(): path.chmod(0o644)


def main():
    need(len(sys.argv) == 4, 'expected manifest pin, bootstrap pin, packet directory')
    manifest_pin, bootstrap_pin, path = sys.argv[1:]
    root = Path(os.path.abspath(path))
    snapshot, parsed = integrity(root, manifest_pin, bootstrap_pin)
    result = replay(snapshot, parsed)
    after, after_parsed = integrity(root, manifest_pin, bootstrap_pin)
    need(after == snapshot and same(after_parsed, parsed), 'publication changed during replay')
    result.update(schema=1, problem_id=2776, status='PASS', publication_files=len(FILES),
                  optimization=sys.flags.optimize, uid=os.getuid(), euid=os.geteuid(),
                  queue_status='unsolved', substantive_turns='5/5',
                  manifest_sha256=manifest_pin, bootstrap_sha256=bootstrap_pin)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, TypeError, KeyError, subprocess.TimeoutExpired):
        print('REJECT: publication integrity/replay validation failed', file=sys.stderr)
        sys.exit(1)
