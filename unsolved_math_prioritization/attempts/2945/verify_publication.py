#!/usr/bin/env python3
"""Authenticate frozen pseudo-isotopy partial results; replay source-free finite checks."""
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

ACCEPTED = {'original/CANDIDATE_FREEZE.json': {'bytes': 1632, 'sha256': '5ca5ea8c8f68876e60dbc5d576ff1cd4415adf22761ea2fcf1969cbdc428c901'}, 'original/public/APPROACH_LEDGER.json': {'bytes': 2667, 'sha256': '0df03b4147a6a8dddb72f803101fbe8af14aed1283abfaa48eaaf51904e6e7af'}, 'original/public/CORPUS_BINDINGS.json': {'bytes': 882, 'sha256': '4b94ca8c41d024f8b060c23828da511eef6f6aa4d9fe6374ff2b87d8160ab73b'}, 'original/public/EXACT_CHECKS.json': {'bytes': 1788, 'sha256': 'fa2f8ae686297574d5a0a4ea0037f5a63c059ef82e47adf43747f1eab5952dc3'}, 'original/public/MATHEMATICAL_REPORT.md': {'bytes': 26220, 'sha256': 'e89c61fd84e05bdb36cb4056ddf2254cbb1023b0d21efb16b4be4e696acaa5d5'}, 'original/public/README.md': {'bytes': 1979, 'sha256': '7691850de74ee321de6d0b4861b6ab30ad47fb456ca4f04871343e60d44f1dbe'}, 'original/public/REVIEW_CHECKLIST.md': {'bytes': 2881, 'sha256': '8979abcc06f4469050a45bb341b6d11db079ca10afff9deb794e6c5ecf10a34b'}, 'original/public/SOURCE_MANIFEST.json': {'bytes': 6870, 'sha256': 'e59f66e848a387518b7b2142f88b895a962ed54dc1d8af0f1a7b3b13a73fbecb'}, 'original/public/verify_exact_checks.py': {'bytes': 6282, 'sha256': 'f5657978e48493e459196dab61f6bebccc03889d1881105c83661d9451322820'}, 'audit/AUDIT.md': {'bytes': 25624, 'sha256': 'eb8c9dd785fb9e59f450e9678ecbf7065f262e95709e34924794d3827172615e'}, 'audit/AUDIT_PINS.json': {'bytes': 1735, 'sha256': 'b07bc7e3914bf3f361f310c2a884199f32838bf3217346fc1346e1aa00985884'}, 'audit/AUDIT_RESULT.json': {'bytes': 2109, 'sha256': '680d82c8bea6b2f5c625154b85ee4bd357728aff438d5b44e7cd04f116652d00'}, 'audit/CORPUS_AUDIT.json': {'bytes': 967, 'sha256': '42fd8a157c6a1492c9ee555ae6c7c4090329a75f4412ac8850784375f13cee3b'}, 'audit/EXECUTION_AUDIT.json': {'bytes': 40276, 'sha256': '204b2b8cd83ef64f069c378d232e18d066203a63c214ec23258c27b7dc2f1c2c'}, 'audit/INDEPENDENT_CHECKS.json': {'bytes': 1512, 'sha256': '73cbcb4e6d2fae4cee9b2a7e1d7f9bf1391bab65e5831f489674259e436daeb9'}, 'audit/ORIGINAL_FREEZE.json': {'bytes': 1632, 'sha256': '5ca5ea8c8f68876e60dbc5d576ff1cd4415adf22761ea2fcf1969cbdc428c901'}, 'audit/README.md': {'bytes': 1889, 'sha256': '8cac640bc8b3f8dbb2c7d0f06ab0498aa17afbe5f2be63cbe61a2788cb0c471d'}, 'audit/SOURCE_AUDIT.json': {'bytes': 5411, 'sha256': 'fdbfde895ad49b7379a1a99270c29c2fbc7fabb85f9d3a91c444a7b370987e83'}, 'audit/independent_checks.py': {'bytes': 6214, 'sha256': '678588b03953678b233ee444c2c49bf0350c6d5061b04002ffa0302e4795ce6d'}, 'audit/reproduce_audit.py': {'bytes': 9363, 'sha256': '754bb5ef763ffc47366bedcd82da7597594685f2f84f5d8b8b13d7c0c9721ad5'}, 'audit/verify_audit.py': {'bytes': 2768, 'sha256': '1ea1c5b12e33c716c4292d495e0fc31e2055942ff364d28c53a64f8cca887ab4'}}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'original', 'original/public', 'audit'}
ORIGINAL_PIN = '5ca5ea8c8f68876e60dbc5d576ff1cd4415adf22761ea2fcf1969cbdc428c901'
TREE_PIN = '9373856af6e529c088f6df98cc42e147f3b8730e00494a90af7781e62d90cf83'
AUDIT_PIN = 'b07bc7e3914bf3f361f310c2a884199f32838bf3217346fc1346e1aa00985884'


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
    exact_int(value['problem_id'], 2945)
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
    candidate = parsed['original/CANDIDATE_FREEZE.json']
    need(sha(snapshot['original/CANDIDATE_FREEZE.json']) == ORIGINAL_PIN, 'original external pin')
    need(sha(snapshot['audit/AUDIT_PINS.json']) == AUDIT_PIN, 'audit external pin')
    keys(candidate, ['problem_id','problem_number','frozen_at_utc','status','five_math_approaches_completed','publication_performed','queue_changed','files','candidate_tree_sha256'])
    exact_int(candidate['problem_id'],2945)
    need(candidate['problem_number']=='KP-4.69' and candidate['status']=='partial_unresolved', 'candidate scope')
    need(candidate['five_math_approaches_completed'] is True and candidate['publication_performed'] is False and candidate['queue_changed'] is False, 'historical candidate status')
    audit = parsed['audit/AUDIT_PINS.json']
    keys(audit,['format','files'])
    need(audit['format']=='kp-4.69-independent-audit-v1','audit format')
    for prefix, value, excluded in [('original/',candidate,'CANDIDATE_FREEZE.json'),('audit/',audit,'AUDIT_PINS.json')]:
        names={n[len(prefix):] for n in ACCEPTED if n.startswith(prefix)}-{excluded}
        rows=value['files']; need(type(rows) is list and len(rows)==len(names),'frozen row count')
        seen=set()
        for row in rows:
            keys(row,['path','bytes','sha256']);name=row['path']
            need(type(name) is str and name in names and name not in seen,'frozen exact path')
            seen.add(name);exact_int(row['bytes']);digest(row['sha256'])
            need(same(row,dict(path=name,bytes=len(snapshot[prefix+name]),sha256=sha(snapshot[prefix+name]))),'frozen row binding')
        need(seen==names,'frozen inventory')
    need(sha(json.dumps(candidate['files'],sort_keys=True,separators=(',',':')).encode())==TREE_PIN==candidate['candidate_tree_sha256'],'original tree pin')
    need(snapshot['audit/ORIGINAL_FREEZE.json']==snapshot['original/CANDIDATE_FREEZE.json'],'audit original freeze')
    disposition=parsed['audit/AUDIT_RESULT.json']
    need(disposition['status']=='ACCEPT_PARTIAL_UNRESOLVED' and disposition['full_solution'] is False and disposition['novelty_established'] is False,'audit scope')
    need(disposition['candidate_unchanged'] is True and disposition['correction_required'] is False and disposition['corrected_candidate_created'] is False,'no patch required')
    exact_int(disposition['counted_mathematical_approaches'],5)
    need(disposition['section_6']['unstabilized_smooth_pseudoisotopy']=='unresolved','unstabilized boundary')
    inventory(root)
    return snapshot, parsed


def stable_audit(value):
    """Only version text and failed-child traceback hashes are path-dependent.

    Exact failure messages, exit codes, mathematical results, runtime identities,
    optimization levels, counts, and every other field remain strictly compared.
    The historical receipt does not retain full tracebacks. Fresh tracebacks have
    temporary paths, so their whole hashes cannot equal historical hashes.
    """
    import copy
    value=copy.deepcopy(value)
    need(type(value['python_version']) is str and value['python_version'].startswith('3.'),'runtime version')
    value['python_version']='<runtime version>'
    for row in value['rows']:
        if row['returncode'] != 0:
            exact_int(row['returncode'],1)
            need(type(row['error_last_line']) is str and row['error_last_line'].startswith('RuntimeError: '),'intended semantic failure')
            digest(row['stderr_sha256'])
            need(row['stderr_sha256']!=sha(b''),'nonempty failure traceback')
            row['stderr_sha256']='<temporary-path-dependent traceback hash>'
    return value


def replay(snapshot, parsed):
    need(hasattr(os,'geteuid') and os.getuid()==os.geteuid()==1000,'real UID/EUID 1000 required')
    with tempfile.TemporaryDirectory(prefix='pseudoisotopy-publication-') as temporary:
        work=Path(temporary)
        for name in ['original','original/public','audit','cwd']:(work/name).mkdir()
        for name in ACCEPTED:(work/name).write_bytes(snapshot[name])
        for name in ACCEPTED:(work/name).chmod(0o444)
        readonly=[work/name for name in ['original/public','original','audit','cwd']]
        for directory in readonly:directory.chmod(0o555)
        denied=[]
        try:
            for name in ['original/NEW_FILE','original/CANDIDATE_FREEZE.json','original/public/NEW_FILE','original/public/verify_exact_checks.py','audit/NEW_FILE','audit/reproduce_audit.py','cwd/NEW_FILE']:
                try:
                    with (work/name).open('ab') as f:f.write(b'forbidden')
                except PermissionError:denied.append(name)
                else:raise ValueError('read-only write succeeded')
            env=dict(PATH=os.defpath,HOME=str(work),TMPDIR=str(work),LC_ALL='C',PYTHONNOUSERSITE='1',PYTHONDONTWRITEBYTECODE='1',PYTHONSAFEPATH='1')
            flags=[] if sys.flags.optimize==0 else ['-'+('O'*sys.flags.optimize)]
            def run(script,args):
                result=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(work/script),*args],cwd=work/'cwd',env=env,capture_output=True,timeout=300)
                need(result.returncode==0 and result.stderr==b'','accepted replay rejected')
                return result.stdout,parse(result.stdout)
            candidate_raw,candidate=run('original/public/verify_exact_checks.py',[])
            need(candidate_raw==snapshot['original/public/EXACT_CHECKS.json'],'candidate frozen output')
            independent_raw,independent=run('audit/independent_checks.py',[])
            need(independent_raw==snapshot['audit/INDEPENDENT_CHECKS.json'],'independent frozen output')
            verified_raw,verified=run('audit/verify_audit.py',[str(work/'audit'),AUDIT_PIN])
            need(same(verified,dict(status='PASS',files_checked=11,manifest_sha256=AUDIT_PIN)),'audit verifier receipt')
            # The unchanged harness copytree preserves modes before preparing mutations.
            # Supply a separate disposable staging tree, not the read-only packet.
            # The harness itself freezes every actual executed specimen to 0555/0444
            # and proves real UID-1000 write denial. Its source bytes are rechecked.
            staging=work/'native_staging';(staging/'public').mkdir(parents=True)
            for name in ACCEPTED:
                if name.startswith('original/'):
                    (staging/name[len('original/'):]).write_bytes(snapshot[name])
            staged_expected={name[len('original/'):]:dict(bytes=len(snapshot[name]),sha256=sha(snapshot[name])) for name in ACCEPTED if name.startswith('original/')}
            def staged_snapshot():
                result={}
                for path in staging.rglob('*'):
                    need(not path.is_symlink(),'staging symlink')
                    if path.is_file():
                        raw=ordinary(path);result[path.relative_to(staging).as_posix()]=dict(bytes=len(raw),sha256=sha(raw))
                    else:need(path.is_dir() and path==staging/'public','staging extra directory')
                return result
            need(same(staged_snapshot(),staged_expected),'native staged-source pre-run pins')
            native_summary_raw,native_summary=run('audit/reproduce_audit.py',[str(staging),str(work/'fresh_execution.json')])
            need(same(staged_snapshot(),staged_expected),'native staged-source post-run pins')
            native=parse(ordinary(work/'fresh_execution.json'))
            need(native['python_version']==sys.version,'actual native Python version')
            need(same(stable_audit(native),stable_audit(parsed['audit/EXECUTION_AUDIT.json'])),'native audit exact stable receipt')
            need(same(native_summary,{k:native[k] for k in ['status','runs','invalid_control_rejections','candidate_unchanged','pins']}),'native summary receipt')
            need(not list((work/'cwd').iterdir()),'readonly cwd changed')
            for name in ACCEPTED:need((work/name).read_bytes()==snapshot[name],'evidence changed during replay')
            return dict(candidate_output_sha256=sha(candidate_raw),independent_output_sha256=sha(independent_raw),
                native_harness_preparation='SEPARATE_AUTHENTICATED_WRITABLE_DISPOSABLE_STAGING',native_executed_specimens='UID1000_READONLY_0555_0444_WITH_DENIED_WRITE_PROBES',
                native_process_runs=36,native_invalid_control_rejections=30,native_controls_own_modes=['normal','-O','-OO'],
                candidate_assert_statements=0,independent_assert_statements=0,
                readonly_write_probes_denied=denied,python_version=sys.version.split()[0],
                historical_source_bindings='NINE_PDF_HASHES_MATCHED_IN_FROZEN_AUDIT',
                historical_corpus_bindings='TWO_DATASET_HASHES_AND_UNIQUE_RECORD_MATCHED_IN_FROZEN_AUDIT',
                fresh_source_bindings='NOT_RUN',fresh_corpus_bindings='NOT_RUN',
                imported_theorem_proofs='NOT_MACHINE_CERTIFIED',KS96_full_text='NOT_OBTAINED',
                relative_realization='SUPPORTED_BY_RELATIVE_PROOF_MARKINGS_AS_AUDITED',
                finite_interior_stabilized_extension='ACCEPTED_WITH_IMPORTED_DEPENDENCIES',
                unstabilized_pseudoisotopy='UNRESOLVED',novelty='NOT_ESTABLISHED',general_problem='UNSOLVED')
        finally:
            for directory in readonly:directory.chmod(0o755)
            for name in ACCEPTED:(work/name).chmod(0o644)


def main():
    need(len(sys.argv) == 4, 'expected manifest pin, bootstrap pin, packet directory')
    manifest_pin, bootstrap_pin, path = sys.argv[1:]
    root = Path(os.path.abspath(path))
    snapshot, parsed = integrity(root, manifest_pin, bootstrap_pin)
    result = replay(snapshot, parsed)
    after, after_parsed = integrity(root, manifest_pin, bootstrap_pin)
    need(after == snapshot and same(after_parsed, parsed), 'publication changed during replay')
    result.update(schema=1, problem_id=2945, status='PASS', publication_files=len(FILES),
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
