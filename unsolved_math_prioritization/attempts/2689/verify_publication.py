#!/usr/bin/env python3
"""Authenticate frozen khovanov partial results; replay source-free finite checks."""
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

ACCEPTED = {'author/EXACT_CHECKS.json': {'bytes': 5546, 'sha256': 'b59436f1306569a0e4c17070b98b7c1e99d173fbb1240941c742d944260a39b5'}, 'author/MANIFEST.json': {'bytes': 1157, 'sha256': '859d3ac083256be02e0c0f139b08c502304855d47831af75dd94119dd647d2cc'}, 'author/REPORT.md': {'bytes': 22726, 'sha256': '6e1354f0909e2a45212b1d0723ff85a84f00e179d4ec40ffeaff444886ae5022'}, 'author/RUN_METADATA.json': {'bytes': 1259, 'sha256': 'e8236712e9de82ae4c007cd7be7040e20382707787036e89c86f0151304fdd00'}, 'author/SOURCE_METADATA.json': {'bytes': 7024, 'sha256': '37ccdc924822d5d1e3eb3160ef6da0378e7adc3eff97f9c7fae63554c5b6b29a'}, 'author/verify_exact.py': {'bytes': 8857, 'sha256': 'c50db261666ad00895b6325a0f2d0235112a150100622a07652c414655fd8fa0'}, 'audit/AUDIT.md': {'bytes': 24614, 'sha256': '5fb01df74288846df03148357d6ef5b82f83a3c85a0e3f53d52d7464a22055d3'}, 'audit/AUDIT_MANIFEST.json': {'bytes': 2805, 'sha256': '329e588edb809fe0bfb92bd6f0f08d95853dcddd0b63f9990ce9870506872e31'}, 'audit/INDEPENDENT_ALGEBRA.json': {'bytes': 8372, 'sha256': 'a17bdbf788263f00cd2f1a93163ab8ef18cc23790075e1158be0ea4bc1483e4f'}, 'audit/INDEPENDENT_COMPARISON.json': {'bytes': 2710, 'sha256': '3559342f2eae6980c9834a3ef2ffcb2b2fbd83f77ba97e8b5604e626642b7e40'}, 'audit/INDEPENDENT_CUBE.json': {'bytes': 3319, 'sha256': '970ead1898e485e8f8912661807659e770760e0a4eaba7505ef1d54d9c94e234'}, 'audit/RUNTIME_AUDIT.json': {'bytes': 10706, 'sha256': 'ad3d456cbe8ee0397656ab2177e1dbd5fa5b3e6ca5fb9e24e97d5c61cef56e1f'}, 'audit/SOURCE_INTEGRITY.json': {'bytes': 1372, 'sha256': 'ceca952b0ae5d242362835f833fb852ea9071c190257261f41e2f4a29c1e60d6'}, 'audit/audit_runtime.py': {'bytes': 7356, 'sha256': '94824ce228ea77979044d040c2e97a9985810a7eb76652bd46b8288185c29e11'}, 'audit/independent_algebra.py': {'bytes': 6952, 'sha256': '409e9fea08a4fb5871e6dfdc81ae4249c63e523787167a1d1cde84e08ed6e730'}, 'audit/independent_cube.py': {'bytes': 8173, 'sha256': '6b64ea30d18ad9181dd4b6f4543f03b8d67c768b0139fe0c28bcf803734bef75'}}
AUTHOR = {n.split('/', 1)[1] for n in ACCEPTED if n.startswith('author/')}
AUDIT = {n.split('/', 1)[1] for n in ACCEPTED if n.startswith('audit/')}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'author', 'audit'}
AUTHOR_PIN = '859d3ac083256be02e0c0f139b08c502304855d47831af75dd94119dd647d2cc'
AUDIT_PIN = '329e588edb809fe0bfb92bd6f0f08d95853dcddd0b63f9990ce9870506872e31'


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
    exact_int(value['problem_id'], 2689)
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
    for prefix, names, pin, manifest_name in [('author/', AUTHOR, AUTHOR_PIN, 'MANIFEST.json'), ('audit/', AUDIT, AUDIT_PIN, 'AUDIT_MANIFEST.json')]:
        need(sha(snapshot[prefix+manifest_name]) == pin, 'original manifest pin')
        value = parsed[prefix+manifest_name]
        exact_int(value['problem_id'], 2689)
        need(value['problem_code'] == 'KP-1.30', 'problem code')
        if prefix == 'author/':
            need(value['status'] == 'partial-progress; universal conjecture unresolved', 'author scope')
            exact_int(value['proof_approaches'], 5)
        else:
            need(value['verdict'] == 'ACCEPT as partial progress; no mathematical correction required; universal conjecture unresolved', 'audit scope')
            exact_int(value['approaches_audited'], 5)
            exact_int(value['approaches_resolving_universal_problem'], 0)
        rows = value['files']
        need(type(rows) is list and len(rows) == len(names)-1, 'original file count')
        seen = set()
        for row in rows:
            keys(row, ['file', 'bytes', 'sha256'])
            name = row['file']
            need(type(name) is str and name in names-{manifest_name} and name not in seen, 'original member name')
            seen.add(name)
            exact_int(row['bytes']); digest(row['sha256'])
            need(same(row, dict(file=name, bytes=len(snapshot[prefix+name]), sha256=sha(snapshot[prefix+name]))), 'original manifest binding')
        need(seen == names-{manifest_name}, 'original exact inventory')
    historical = parsed['audit/AUDIT_MANIFEST.json']['original_frozen_anchors']
    need(same(historical, {'archive_bytes':17653, 'archive_sha256':'3feb6d48ac9e30cd1cf36a4a4e42430b9e8cb4f471a6439e1e393711975fe669', 'manifest_sha256':AUTHOR_PIN, 'report_sha256':ACCEPTED['author/REPORT.md']['sha256']}), 'independent original anchors')
    inventory(root)
    return snapshot, parsed


def replay(snapshot, parsed):
    need(hasattr(os, 'geteuid') and os.getuid() == os.geteuid() == 1000, 'real UID/EUID 1000 required')
    with tempfile.TemporaryDirectory(prefix='khovanov-publication-') as temporary:
        work = Path(temporary)
        for name in DIRS | {'cwd'}:
            (work/name).mkdir()
        for name in ACCEPTED:
            (work/name).write_bytes(snapshot[name])
        readonly = [work/'author', work/'audit', work/'cwd']
        for directory in readonly:
            for path in directory.iterdir():
                path.chmod(0o444)
            directory.chmod(0o555)
        denied = []
        try:
            for path in [work/'author'/'NEW_FILE', work/'author'/'REPORT.md', work/'audit'/'NEW_FILE', work/'audit'/'AUDIT.md', work/'cwd'/'NEW_FILE']:
                try:
                    with path.open('ab') as stream:
                        stream.write(b'forbidden')
                except PermissionError:
                    denied.append(path.relative_to(work).as_posix())
                else:
                    raise ValueError('read-only write succeeded')
            env = dict(PATH=os.defpath, HOME=str(work), TMPDIR=str(work), LC_ALL='C')
            flags = [] if sys.flags.optimize == 0 else ['-'+('O'*sys.flags.optimize)]
            # This is not a stdlib-only replay. Isolated, no-site children add only
            # the interpreter's configured installation directory for SymPy and
            # mpmath; no .pth, sitecustomize, user-site or environment path runs.
            setup = "import sys,sysconfig\nsys.path.append(sysconfig.get_path('purelib'))\nimport sympy,mpmath\nif sympy.__version__!='1.14.0' or mpmath.__version__!='1.3.0': raise RuntimeError('Dependency version mismatch')\n"
            independent = "import types\nm=types.ModuleType('independent_cube')\nexec(compile("+repr(snapshot['audit/independent_cube.py'].decode())+",'<authenticated-independent-cube>','exec'),m.__dict__)\nsys.modules['independent_cube']=m\n"
            def run(source, label, helper=False):
                program=setup+(independent if helper else '')+"ns={'__name__':'__main__'}\nexec(compile("+repr(source)+","+repr(label)+",'exec'),ns)\n"
                return subprocess.run([sys.executable,'-I','-S','-B',*flags,'-c',program],cwd=work/'cwd',env=env,capture_output=True,timeout=240)
            outputs={}
            for script, saved, helper in [('author/verify_exact.py','author/EXACT_CHECKS.json',False),('audit/independent_cube.py','audit/INDEPENDENT_CUBE.json',False),('audit/independent_algebra.py','audit/INDEPENDENT_ALGEBRA.json',True)]:
                result=run(snapshot[script].decode(),'<authenticated-'+script+'>',helper)
                need(result.returncode==0 and result.stderr==b'', 'accepted verifier replay rejected: '+script)
                need(result.stdout==snapshot[saved], 'full exact output mismatch: '+script)
                value=parse(result.stdout)
                need(same(value,parsed[saved]), 'exact parsed output mismatch')
                outputs[script]={'stdout_utf8':result.stdout.decode(),'stdout_bytes':len(result.stdout),'stdout_sha256':sha(result.stdout),'stderr_utf8':'','exit_code':0}
            author=parsed['author/EXACT_CHECKS.json']; cube=parsed['audit/INDEPENDENT_CUBE.json']; algebra=parsed['audit/INDEPENDENT_ALGEBRA.json']
            comparisons=[]
            for knot in ['T(2,1)','T(2,3)','T(2,5)']:
                for theory in ['unreduced','reduced']:
                    original=author['knots'][knot][theory]
                    keys(original,['Q','F2','bigraded','d_squared_zero'])
                    need(original['d_squared_zero'] is True,'author integer differential')
                    need(same({k:v for k,v in original.items() if k!='d_squared_zero'},cube['knots'][knot][theory]),'independent bigraded dimensions')
                    comparisons.append(dict(knot=knot,theory=theory,all_bigraded_dimensions_match=True,Q=cube['knots'][knot][theory]['Q'],F2=cube['knots'][knot][theory]['F2']))
                rho=cube['knots'][knot]['direct_connecting_rank']
                need(same(rho,author['knots'][knot]['connecting_rank_from_exact_sequence']),'direct connecting rank')
                comparisons.append(dict(knot=knot,direct_connecting_rank=rho,matches_candidate_rank_from_exact_sequence=True))
            need(same(comparisons,parsed['audit/INDEPENDENT_COMPARISON.json']['cube_comparisons']),'full independent comparison receipt')
            exact_int(algebra['module_lemma']['valid_composition_pairs'],3126)
            need(same([x['E1_dimension'] for x in algebra['staircases']],[6,14]),'staircase dimensions')
            source=snapshot['author/verify_exact.py'].decode()
            mutations=[
                ('trefoil_rank','(3, (4, 6, 3, 3))','(3, (4, 5, 3, 3))','main'),
                ('cube_sign','sign = (-1) ** sum(s[:k])','sign = 1','main'),
                ('comultiplication','[(0, 1), (1, 0)]','[(0, 1)]','main'),
                ('bockstein_parity','int(e == 1)','int(e == 2)','algebra_checks'),
                ('odd_cycle_smith','[2 if n % 2 else 0]','[0 if n % 2 else 2]','algebra_checks'),
                ('module_composition','sp.Matrix([[0], [1], [0]])','sp.Matrix([[0], [0], [0]])','algebra_checks'),
                ('turner_zigzag','sp.eye(2)','sp.zeros(2)','algebra_checks'),
                ('tensor_connecting_rank','require(delta_sum.rank() == 4)','require(delta_sum.rank() == 3)','algebra_checks')]
            controls=[]
            for label,old,new,entry in mutations:
                need(source.count(old)==1,'mutation unique')
                changed=source.replace(old,new)
                # Compile with a stable descriptive filename and print only the
                # verified mathematical exception, yielding portable full output.
                program=setup+"ns={'__name__':'semantic_mutant'}\nexec(compile("+repr(changed)+",'<semantic-mutant>','exec'),ns)\ntry:\n ns["+repr(entry)+"]()\nexcept RuntimeError as e:\n if str(e)!='Exact verification condition failed': raise\n print('RuntimeError: '+str(e),file=sys.stderr)\n sys.exit(1)\n"
                result=subprocess.run([sys.executable,'-I','-S','-B',*flags,'-c',program],cwd=work/'cwd',env=env,capture_output=True,timeout=240)
                need(result.returncode==1 and result.stderr==b'RuntimeError: Exact verification condition failed\n','semantic mutation not mathematically rejected: '+label)
                controls.append(dict(mutation=label,candidate_sha256=sha(changed.encode()),exit_code=result.returncode,stdout_utf8=result.stdout.decode(),stderr_utf8=result.stderr.decode()))
            need(not list((work/'cwd').iterdir()),'child wrote to read-only cwd')
            for name in ACCEPTED:
                need((work/name).read_bytes()==snapshot[name],'replay mutated accepted evidence')
            return dict(exact_full_outputs=outputs,independent_comparisons=comparisons,semantic_mutations=controls,
                        native_mutation_rejections=len(controls),readonly_write_probes_denied=denied,
                        dependency_versions={'sympy':'1.14.0','mpmath':'1.3.0'},dependency_code_trust='INSTALLED_INTERPRETER_ENVIRONMENT_NOT_PINNED_BY_PACKET',
                        dependency_loading='isolated no-site child; configured purelib only; no site startup',
                        python_version=sys.version.split()[0],historical_source_bindings='8_SOURCE_PDF_HASH_SIZE_PAGE_RECORDS_MATCHED_HISTORICALLY',
                        fresh_source_bindings='NOT_RUN',imported_theorem_proofs='NOT_MACHINE_CERTIFIED',general_problem='UNSOLVED')
        finally:
            for directory in readonly:
                directory.chmod(0o755)
                for path in directory.iterdir():path.chmod(0o644)


def main():
    need(len(sys.argv) == 4, 'expected manifest pin, bootstrap pin, packet directory')
    manifest_pin, bootstrap_pin, path = sys.argv[1:]
    root = Path(os.path.abspath(path))
    snapshot, parsed = integrity(root, manifest_pin, bootstrap_pin)
    result = replay(snapshot, parsed)
    after, after_parsed = integrity(root, manifest_pin, bootstrap_pin)
    need(after == snapshot and same(after_parsed, parsed), 'publication changed during replay')
    result.update(schema=1, problem_id=2689, status='PASS', publication_files=len(FILES),
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
