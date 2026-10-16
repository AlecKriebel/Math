#!/usr/bin/env python3
"""Authenticate frozen elliptic-reeb partial results; replay source-free finite checks."""
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

ACCEPTED = {'author/AUDIT.md': {'bytes': 3829, 'sha256': '052c8f9d263a7d6caf2892e5a6def6163ca7aeffa5c587a72a16cdaf1a388e04'}, 'author/EXACT_CHECKS.json': {'bytes': 762, 'sha256': 'c15a15b794bd5a48682ae7c807b0e255f02e2f1cab55e32254be04044e71c637'}, 'author/MANIFEST.json': {'bytes': 1049, 'sha256': 'e807c15d1bcd72e46389a6f9955a9a8c6ce73e764b036ae2a08aa356d9b9c4a1'}, 'author/README.md': {'bytes': 1276, 'sha256': 'f0f9301ff28ff7b1d70eb17deb14e013c9c132f8ac870ac3eb3519272bcf51b5'}, 'author/REPORT.md': {'bytes': 20868, 'sha256': '040099b67234e29b545bed600edd59c9408b900f5fedb6d89480b857a7b381d6'}, 'author/SOURCE_PINS.json': {'bytes': 3269, 'sha256': 'ff5ce6b64c275e107ab5e5c15fd5f0836fa340981f901d3fc17b8d8e327fb86b'}, 'author/STATUS.json': {'bytes': 948, 'sha256': '319288de6fa0b64e90b2438b82fb2f83f405a1d0b7581210e5c4c68a1b7d5d53'}, 'author/verify_exact.py': {'bytes': 3536, 'sha256': '18c9abff1ad2e5e539edfb0ed88a7d6a47704f66d75e2daa646125979b63587c'}, 'corrected/AUDIT.md': {'bytes': 3846, 'sha256': '46cc8d160dff0c7550135620732218031700ee8cadbf05710534ad692eea0b6f'}, 'corrected/EXACT_CHECKS.json': {'bytes': 762, 'sha256': 'c15a15b794bd5a48682ae7c807b0e255f02e2f1cab55e32254be04044e71c637'}, 'corrected/MANIFEST.json': {'bytes': 1049, 'sha256': '7beb5ce3cb8b294c18ab9256c896a79cd8fe8920e46bd253c30a02bbe849407f'}, 'corrected/README.md': {'bytes': 1276, 'sha256': 'f0f9301ff28ff7b1d70eb17deb14e013c9c132f8ac870ac3eb3519272bcf51b5'}, 'corrected/REPORT.md': {'bytes': 20976, 'sha256': 'b3cd61f8a00e6b79741dfeea6e7c1c8a0ec42611c7f959ddea9634d0f84d2039'}, 'corrected/SOURCE_PINS.json': {'bytes': 3324, 'sha256': '95cbd794a17b316bf769bd0c7287cb239525882b5dac5dec02face85300f030a'}, 'corrected/STATUS.json': {'bytes': 948, 'sha256': '319288de6fa0b64e90b2438b82fb2f83f405a1d0b7581210e5c4c68a1b7d5d53'}, 'corrected/verify_exact.py': {'bytes': 3536, 'sha256': '18c9abff1ad2e5e539edfb0ed88a7d6a47704f66d75e2daa646125979b63587c'}, 'audit/ACCEPTANCE.json': {'bytes': 1092, 'sha256': 'bd326337a7d84cd218db2791e5ca8267f4e57a35529b7bc9ec088d7d27f421fb'}, 'audit/CORRECTED_PACKET_PINS.json': {'bytes': 1663, 'sha256': '26cbf738b1219f0fe8ed5f858c53b5e8ed099fea726a54cac3d84b8ec835d5dd'}, 'audit/FROZEN_INPUTS.json': {'bytes': 1286, 'sha256': 'bc06977d98f03d458a511df9b7a4c808718176f78dc8d2dc3b61d7a1c40fa436'}, 'audit/INDEPENDENT_AUDIT.md': {'bytes': 15182, 'sha256': '5df77c0121719c1a4d5a4de688b6110311e5b38cecc5ef42abd4dcc3ae5d4657'}, 'audit/MANIFEST.json': {'bytes': 1479, 'sha256': '2d8e417f2921ba7eae8e8500a6d0680292abc50725ba93e6f001fc335ccfe559'}, 'audit/REPRODUCIBILITY_RESULTS.json': {'bytes': 8417, 'sha256': 'c89125c798620d4d8c1550e3ebb72af21040b30d8a6a12d1be7a38ded1abd65f'}, 'audit/SOURCE_ATTRIBUTION_CORRECTION.patch': {'bytes': 5941, 'sha256': '75d4a2302f5cec463c23daad9e44fab3dddc51f3faf0c245ee60c92566c08551'}, 'audit/SOURCE_AUDIT.json': {'bytes': 8168, 'sha256': '10a402b778c784642d2612cbef34e606578f0f6869c19d53a3384443db12f14a'}, 'audit/independent_checks.py': {'bytes': 6968, 'sha256': '22475a7be0d5b585502e795f799af23ff15767efc426604a70e01fd025b28845'}, 'audit/reproduce_audit.py': {'bytes': 8356, 'sha256': '6b4a4588d4f4b8a2bbbba8acab18ed38ae9c915f80e1a41b4d2d88f6e43cd61c'}}
AUTHOR = {n.split('/', 1)[1] for n in ACCEPTED if n.startswith('author/')}
CORRECTED = {n.split('/', 1)[1] for n in ACCEPTED if n.startswith('corrected/')}
AUDIT = {n.split('/', 1)[1] for n in ACCEPTED if n.startswith('audit/')}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'author', 'corrected', 'audit'}
AUTHOR_PIN = 'e807c15d1bcd72e46389a6f9955a9a8c6ce73e764b036ae2a08aa356d9b9c4a1'
CORRECTED_PIN = '7beb5ce3cb8b294c18ab9256c896a79cd8fe8920e46bd253c30a02bbe849407f'
AUDIT_PIN = '2d8e417f2921ba7eae8e8500a6d0680292abc50725ba93e6f001fc335ccfe559'


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
    exact_int(value['problem_id'], 2845)
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
    for prefix, names, pin in [('author/', AUTHOR, AUTHOR_PIN), ('corrected/', CORRECTED, CORRECTED_PIN), ('audit/', AUDIT, AUDIT_PIN)]:
        need(sha(snapshot[prefix+'MANIFEST.json']) == pin, 'frozen manifest pin')
        value = parsed[prefix+'MANIFEST.json']
        keys(value, ['files', 'schema'] if prefix == 'audit/' else ['files'])
        if prefix == 'audit/':
            need(value['schema'] == 'independent-audit-manifest-v1', 'audit manifest schema')
        rows = value['files']
        need(type(rows) is list and len(rows) == len(names)-1, 'nested file count')
        seen = set()
        for row in rows:
            keys(row, ['file', 'bytes', 'sha256'])
            name = row['file']
            need(type(name) is str and name in names-{'MANIFEST.json'} and name not in seen, 'nested member name')
            seen.add(name)
            exact_int(row['bytes']); digest(row['sha256'])
            need(same(row, dict(file=name, bytes=len(snapshot[prefix+name]), sha256=sha(snapshot[prefix+name]))), 'nested manifest binding')
        need(seen == names-{'MANIFEST.json'}, 'nested exact inventory')
    for name,prefix in [('FROZEN_INPUTS.json','author/'), ('CORRECTED_PACKET_PINS.json','corrected/')]:
        need(same(parsed['audit/'+name]['files'], [dict(file=n, **ACCEPTED[prefix+n]) for n in sorted(AUTHOR)]), 'independent slice pins')
    status = parsed['corrected/STATUS.json']
    exact_int(status['problem_id'], 2845)
    exact_int(status['mathematical_approaches_completed'], 5)
    need(status['universal_part_a_resolved'] is False and status['universal_part_b_resolved'] is False, 'unsolved scope')
    need(status['status'] == 'partial_results_unresolved', 'status disposition')
    acceptance = parsed['audit/ACCEPTANCE.json']
    need(acceptance['verdict'] == 'accept_corrected_authored_partial_results', 'audit disposition')
    need(acceptance['both_universal_questions_resolved'] is False, 'audit scope')
    exact_int(acceptance['mathematical_approaches_completed'],5)
    exact_int(acceptance['negative_control_rejections'],18)
    reconstruct_patch(snapshot)
    inventory(root)
    return snapshot, parsed


def reconstruct_patch(snapshot):
    # Exact line/offset patch application in memory; no fuzzy patch utility.
    lines = snapshot['audit/SOURCE_ATTRIBUTION_CORRECTION.patch'].splitlines(keepends=True)
    output = {name:snapshot['author/'+name] for name in AUTHOR}
    index = 0; changed = []
    while index < len(lines):
        need(lines[index].startswith(b'--- a/'), 'patch source header')
        name = lines[index][6:].rstrip(b'\n').decode('utf-8'); index += 1
        need(name in AUTHOR and name not in changed, 'patch path')
        need(index < len(lines) and lines[index] == ('+++ b/'+name+'\n').encode(), 'patch destination header'); index += 1
        source = output[name].splitlines(keepends=True); result = []; pos = 0; hunks = 0
        while index < len(lines) and lines[index].startswith(b'@@ '):
            match = re.fullmatch(rb'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@\n',lines[index])
            need(match is not None, 'patch hunk syntax'); index += 1; hunks += 1
            old_start, old_count, new_start, new_count = [int(v) if v is not None else 1 for v in match.groups()]
            start = old_start-1 if old_count else old_start
            need(pos <= start <= len(source), 'patch old offset')
            result.extend(source[pos:start]);pos=start
            need(len(result) == (new_start-1 if new_count else new_start), 'patch new offset')
            old_used = new_used = 0
            while index < len(lines) and lines[index][:1] in [b' ',b'+',b'-'] and not lines[index].startswith(b'--- a/'):
                line=lines[index];index+=1;sign=line[:1];body=line[1:]
                if sign in [b' ',b'-']:
                    need(pos<len(source) and source[pos] == body, 'exact patch context')
                    pos+=1;old_used+=1
                if sign in [b' ',b'+']:
                    result.append(body);new_used+=1
            need(old_used==old_count and new_used==new_count, 'patch hunk counts')
        need(hunks>0, 'patch has hunk');result.extend(source[pos:]);output[name]=b''.join(result);changed.append(name)
    need(changed == ['AUDIT.md','MANIFEST.json','REPORT.md','SOURCE_PINS.json'], 'exact patch change scope')
    need(all(output[name] == snapshot['corrected/'+name] for name in AUTHOR), 'patch reconstruction byte identity')
    return changed


def replay(snapshot, parsed):
    need(hasattr(os, 'geteuid') and os.getuid() == os.geteuid() == 1000, 'real UID/EUID 1000 required')
    with tempfile.TemporaryDirectory(prefix='elliptic-reeb-publication-') as temporary:
        work = Path(temporary)
        for name in DIRS | {'cwd'}:
            (work/name).mkdir()
        for name in ACCEPTED:
            (work/name).write_bytes(snapshot[name])
        env = dict(PATH=os.defpath, HOME=str(work), TMPDIR=str(work), LC_ALL='C',
                   PYTHONNOUSERSITE='1', PYTHONDONTWRITEBYTECODE='1', PYTHONSAFEPATH='1')
        flags = [] if sys.flags.optimize == 0 else ['-'+('O'*sys.flags.optimize)]
        result = subprocess.run([sys.executable, '-I', '-S', '-B', *flags,
                                 str(work/'audit/reproduce_audit.py'),str(work/'author'),str(work/'corrected')],
                                cwd=work/'cwd',env=env,capture_output=True,timeout=240)
        need(result.returncode==0 and result.stderr==b'', 'native bubblewrap audit replay failed')
        native=parse(result.stdout)
        need(result.stdout == snapshot['audit/REPRODUCIBILITY_RESULTS.json'], 'native receipt bytes differ')
        need(same(native, parsed['audit/REPRODUCIBILITY_RESULTS.json']), 'native receipt exact types')
        need(native['status']=='pass' and native['genuine_uid']==1000, 'native pass and actual UID')
        exact_int(native['negative_control_executions'],18)
        need(native['network_isolation_claimed'] is False, 'no network isolation claim')
        need([x['mode'] for x in native['mode_results']] == ['normal','O','OO'], 'native three modes')
        for mode in native['mode_results']:
            probe=mode['read_only_probe'];exact_int(probe['uid'],1000);exact_int(probe['euid'],1000)
            need(len(probe['write_open_denials'])==3, 'three native write probes')
            for denial in probe['write_open_denials']:
                need(denial['name']=='EROFS' and type(denial['errno']) is int and denial['errno']==30, 'real read-only mount')
        for name in ACCEPTED:
            need((work/name).read_bytes()==snapshot[name], 'replay changed evidence')
        need(not list((work/'cwd').iterdir()), 'replay wrote into cwd')
        return dict(native_receipt_sha256=sha(result.stdout), native_mutation_rejections=18,
                    native_controls_own_modes=['normal','-O','-OO'], native_uid=1000,
                    native_readonly_mechanism='bubblewrap --ro-bind / /, no writable mounts',
                    native_EROFS_denials=9, network_isolation_claimed=False,
                    exact_patch_reconstruction='PASS', unchanged_mathematics_and_code=True,
                    historical_source_bindings='7_PUBLIC_PDF_HASHES_AND_SIZES_MATCHED_HISTORICALLY',
                    fresh_source_bindings='NOT_RUN', imported_theorem_proofs='NOT_MACHINE_CERTIFIED',
                    universal_part_a='UNSOLVED', universal_part_b='UNSOLVED')


def main():
    need(len(sys.argv) == 4, 'expected manifest pin, bootstrap pin, packet directory')
    manifest_pin, bootstrap_pin, path = sys.argv[1:]
    root = Path(os.path.abspath(path))
    snapshot, parsed = integrity(root, manifest_pin, bootstrap_pin)
    result = replay(snapshot, parsed)
    after, after_parsed = integrity(root, manifest_pin, bootstrap_pin)
    need(after == snapshot and same(after_parsed, parsed), 'publication changed during replay')
    result.update(schema=1, problem_id=2845, status='PASS', publication_files=len(FILES),
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
