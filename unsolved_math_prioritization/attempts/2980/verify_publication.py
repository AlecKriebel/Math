#!/usr/bin/env python3
"""Authenticate frozen curve isotopy partial results; replay source-free finite checks."""
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

ACCEPTED = {'original/public/CHECK_RUNS.json': {'bytes': 1242, 'sha256': 'd3dfef4b23f2204d47cf949ae2d8c45e45d29eaedb386533d3534d58bb9a36f2'}, 'original/public/EXACT_CHECKS.json': {'bytes': 4265, 'sha256': '9ed8e2898b651ea06f20a3e7c4eb2742bda3ba8d955ae7f7b23fa22e546054ca'}, 'original/public/FROZEN_MANIFEST.json': {'bytes': 1120, 'sha256': 'c1e5aabbdb411673c6ef7a002a49a615698ffcc172afad6012f5112ee0b0ba89'}, 'original/public/REPORT.md': {'bytes': 25467, 'sha256': 'b05408b043af27f7ad7ca28e737bfd3f92a47a37badceaaad7b1a3d3662fe7b5'}, 'original/public/RESULT.json': {'bytes': 894, 'sha256': '0871ce00b7796711764c50908c9e425f6ac0b8081edacf53c086c6ba04f1246c'}, 'original/public/SOURCE_METADATA.json': {'bytes': 4556, 'sha256': '8300e47340ba02ad1fffcf72755b7a23197bee82f73ed63a5a34d9fb215fec59'}, 'original/public/verify_exact.py': {'bytes': 6833, 'sha256': '208b1f8a05fbfc03c5efb5fc8aa64ab626eb1f1911bf7737e0bfe160371efc1b'}, 'original/symplectic_curve_isotopy_2980_sourcefree.zip': {'bytes': 17306, 'sha256': '5a15ce6890e0bfd750f3f67e18043a33200fabd4e3dd8b5ed963ce19691f9881'}, 'audit/AUDIT_RECEIPT.json': {'bytes': 979, 'sha256': 'dc8ce8e0ce2c5785821d6705a61a70fb0b16926067b86ec5cc90c33e77b6ef51'}, 'audit/public/ADDITIONAL_SOURCE_METADATA.json': {'bytes': 887, 'sha256': 'cc22a49bee3c7cff86fbeed689fd4fe79ef63b0f93433c189d22458aa1acc0e5'}, 'audit/public/AUDIT.md': {'bytes': 18107, 'sha256': '4ed816f022e2c17d4477e881dc8dbb41389f2addd5700e0376f5328e0b441911'}, 'audit/public/AUDIT_MANIFEST.json': {'bytes': 2228, 'sha256': '5d4aa66da6317cf9e502ac9625f0062de837996c8267ade1a15f1baada41df52'}, 'audit/public/AUDIT_RESULT.json': {'bytes': 737, 'sha256': 'f8e6b921396dc8b4ed0630709e0d58457df4372df2e3324225eee416085a49d6'}, 'audit/public/INDEPENDENT_EXACT.json': {'bytes': 1792, 'sha256': '993e80c004d478358c3acf3f46f449f4e7b701f1b9e91a7a14237106c757caf6'}, 'audit/public/PATCH_VERIFICATION.json': {'bytes': 666, 'sha256': '872990e71bd35e57243eedb462a7ecca7d72f2f9cdbbd524a743626aaac8f3b1'}, 'audit/public/READONLY_RUNS.json': {'bytes': 25796, 'sha256': 'e1467db134598f02b10f5e3fc4fdc8f925cc148ff98efbad93076938314f889c'}, 'audit/public/REPORT.corrected.md': {'bytes': 26685, 'sha256': '1372f3c3de364d04472a17c67085324041ee6f7dbfc30e1fd2c1abbcd98910a0'}, 'audit/public/SOURCE_AUDIT.json': {'bytes': 4191, 'sha256': '162e68f877f10102a1d48ee9dd98a5444e06f5e4164a4028777689c79babb424'}, 'audit/public/SOURCE_COMPLETENESS.patch': {'bytes': 5556, 'sha256': 'ba36649ad1875f9ee1305274f4899e90410bbd3f8ddadc9667e861e7dafe4c9d'}, 'audit/public/independent_exact.py': {'bytes': 4825, 'sha256': '10b8538612048a03221b2ce9f1c3a66624a29b68bdcc7ffa3b38715b4b3811af'}, 'audit/public/run_readonly_audit.py': {'bytes': 7042, 'sha256': 'a48ac286180469d09edfa0a376ec7522aa49413e08279c4a9dc6176e4ea4fd6b'}, 'audit/symplectic_curve_isotopy_2980_audit_sourcefree.zip': {'bytes': 33006, 'sha256': '91c11dc8430ff3dd9c5a3f69a735cb7338f77a0d5256fdf6ba9067083fd533cb'}}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'original', 'original/public', 'audit', 'audit/public'}


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
    exact_int(value['problem_id'], 2980)
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
    # Open pinned archives in memory; no extraction or source input.
    import io, zipfile, ast
    def archive(name, prefix):
        mapping={n[len(prefix):]:n for n in ACCEPTED if n.startswith(prefix)}
        with zipfile.ZipFile(io.BytesIO(snapshot[name])) as z:
            infos=z.infolist()
            need(len(infos)==len(mapping) and {i.filename for i in infos}==set(mapping),'archive exact inventory')
            for info in infos:
                need(not info.is_dir() and info.file_size==len(snapshot[mapping[info.filename]]),'archive member size')
                need(z.read(info)==snapshot[mapping[info.filename]],'archive member bytes')
    archive('original/symplectic_curve_isotopy_2980_sourcefree.zip','original/public/')
    archive('audit/symplectic_curve_isotopy_2980_audit_sourcefree.zip','audit/public/')
    for name,prefix in [('original/public/FROZEN_MANIFEST.json','original/public/'),('audit/public/AUDIT_MANIFEST.json','audit/public/')]:
        m=parsed[name];exact_int(m['problem_id'],2980)
        need(m['problem_code']=='KP-4.104' and m['source_free'] is True and m['source_documents_included'] is False,'slice scope')
        expected={n for n in ACCEPTED if n.startswith(prefix)}-{name};seen=set()
        need(type(m['files']) is list and len(m['files'])==len(expected),'slice length')
        for row in m['files']:
            keys(row,['path','bytes','sha256']);exact_int(row['bytes']);digest(row['sha256'])
            need(type(row['path']) is str,'slice path type');full=prefix+row['path']
            need(full in expected and full not in seen,'slice unique path');seen.add(full)
            need(same(dict(bytes=row['bytes'],sha256=row['sha256']),ACCEPTED[full]),'slice exact byte binding')
        need(seen==expected,'slice complete inventory')
    need(apply_patch(snapshot['original/public/REPORT.md'],snapshot['audit/public/SOURCE_COMPLETENESS.patch'])==snapshot['audit/public/REPORT.corrected.md'],'exact original plus patch reconstruction')
    for name in ['original/public/verify_exact.py','audit/public/independent_exact.py','audit/public/run_readonly_audit.py']:
        need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(snapshot[name]))),'zero disabled assert nodes')
    original=parsed['original/public/RESULT.json'];audit=parsed['audit/public/AUDIT_RESULT.json']
    need(original['result']=='UNRESOLVED_PARTIAL' and audit['target_status']=='UNRESOLVED_PARTIAL','unresolved target')
    exact_int(original['substantive_approaches'],5);exact_int(audit['substantive_approaches'],5)
    need(original['new_complete_solution'] is False and original['verified_prior_complete_solution'] is False,'no solution established')
    need(same(original['all_target_clauses_preserved'],['smooth versus complex isotopy','smooth versus symplectic isotopy','infinite-family question']),'all target clauses')
    need(audit['audit_verdict']=='ACCEPT_WITH_MINIMAL_SOURCE_COMPLETENESS_CORRECTION' and audit['original_freeze_preserved'] is True,'correction accepted')
    exact_int(audit['normal_O_OO_uid1000_readonly_baselines'],6);exact_int(audit['normal_O_OO_uid1000_mutations_detected'],30)
    inventory(root)
    return snapshot, parsed


def apply_patch(original, patch):
    """Apply only the exact authored report patch, with no offset or fuzz."""
    source=original.decode().splitlines(keepends=True);lines=patch.decode().splitlines(keepends=True)
    need(lines[:2]==['--- a/REPORT.md\n','+++ b/REPORT.md\n'],'patch file headers')
    result=[];cursor=0;i=2;hunks=0
    while i<len(lines):
        match=re.fullmatch(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n',lines[i]);need(match is not None,'patch hunk header')
        old_start,old_count,new_start,new_count=map(int,match.groups());i+=1
        need(old_start-1>=cursor,'patch old position');result.extend(source[cursor:old_start-1]);cursor=old_start-1
        need(len(result)==new_start-1,'patch new position');old_used=new_used=0
        while i<len(lines) and not lines[i].startswith('@@ '):
            line=lines[i];i+=1;need(line and line[0] in ' +-','patch line kind')
            if line[0] in ' -':
                need(cursor<len(source) and source[cursor]==line[1:],'patch exact context');cursor+=1;old_used+=1
            if line[0] in ' +':result.append(line[1:]);new_used+=1
        need((old_used,new_used)==(old_count,new_count),'patch hunk sizes');hunks+=1
    need(hunks==2,'expected exact two hunks');result.extend(source[cursor:]);return ''.join(result).encode()


def replay(snapshot, parsed):
    import copy
    need(hasattr(os,'geteuid') and os.getuid()==os.geteuid()==1000,'actual UID/EUID1000 required')
    flags=[] if sys.flags.optimize==0 else ['-'+('O'*sys.flags.optimize)]
    with tempfile.TemporaryDirectory(prefix='curve-isotopy-publication-') as directory:
        work=Path(directory);folders=[];probes=[]
        for folder in ['original','audit','cwd']:(work/folder).mkdir();folders.append(work/folder)
        mapping={n:work/('original' if n.startswith('original/') else 'audit')/Path(n).name for n in ACCEPTED if '/public/' in n}
        for name,path in mapping.items():path.write_bytes(snapshot[name]);path.chmod(0o444)
        for folder in folders:folder.chmod(0o555)
        env=dict(PATH=os.defpath,HOME=str(work),TMPDIR=str(work),LC_ALL='C',PYTHONNOUSERSITE='1',PYTHONDONTWRITEBYTECODE='1',PYTHONSAFEPATH='1')
        def execute(script,args=()):
            return subprocess.run([sys.executable,'-I','-S','-B',*flags,str(script),*args],cwd=work/'cwd',env=env,capture_output=True,timeout=300)
        try:
            for path in [work/'original/NEW_FILE',work/'original/verify_exact.py',work/'audit/NEW_FILE',work/'audit/run_readonly_audit.py',work/'cwd/NEW_FILE']:
                try:
                    with path.open('ab') as f:f.write(b'forbidden')
                except PermissionError:probes.append(path.relative_to(work).as_posix())
                else:raise ValueError('read-only write unexpectedly permitted')
            outputs={}
            for label,script,expected in [('original','original/verify_exact.py','original/public/EXACT_CHECKS.json'),('independent','audit/independent_exact.py','audit/public/INDEPENDENT_EXACT.json')]:
                proc=execute(work/script)
                need(proc.returncode==0 and proc.stderr==b'','fresh checker failed')
                need(proc.stdout==snapshot[expected] and same(parse(proc.stdout),parsed[expected]),'complete exact checker stdout differs')
                outputs[label]=dict(stdout=proc.stdout.decode(),stdout_bytes=len(proc.stdout),stdout_sha256=sha(proc.stdout),complete_result=parse(proc.stdout),returncode=0,stderr='')
            proc=execute(work/'audit/run_readonly_audit.py',[str(work/'original')])
            need(proc.returncode==0 and proc.stderr==b'','native read-only mutation harness failed')
            value=parse(proc.stdout);historical=copy.deepcopy(parsed['audit/public/READONLY_RUNS.json'])
            need(type(value['python_version']) is str and value['python_version']==sys.version.split()[0],'native actual Python version')
            need(type(historical['python_version']) is str and re.fullmatch(r'3\.[0-9]+\.[0-9]+',historical['python_version']) is not None,'historical Python version')
            historical['python_version']=sys.version.split()[0]
            need(same(value,historical),'complete native receipt typed match except runtime Python version')
            exact_int(value['baseline_runs'],6);exact_int(value['mutation_runs'],30);exact_int(value['mutation_families'],10)
            for name,path in mapping.items():need(path.read_bytes()==snapshot[name],'frozen source-free input changed')
            need(not list((work/'cwd').iterdir()),'read-only cwd changed')
            return dict(exact_outputs=outputs,complete_native_receipt=value,native_stdout=proc.stdout.decode(),native_stdout_sha256=sha(proc.stdout),native_stdout_bytes=len(proc.stdout),native_returncode=0,native_stderr='',native_receipt_comparison='COMPLETE_TYPED_EQUAL_WITH_RUNTIME_VERSION_ONLY_NORMALIZED',native_harness_runs=36,native_mutation_runs=30,native_modes=['normal','-O','-OO'],readonly_write_probes_denied=probes,readonly_file_mode='0444',readonly_directory_mode='0555',original_files_preserved=7,audit_files_preserved=12,patch_application='EXACT_ZERO_OFFSET_ZERO_FUZZ_TWO_HUNK_RECONSTRUCTION',fresh_source_bindings='NOT_RUN',fresh_corpus_bindings='NOT_RUN',historical_source_bindings='NINE_ORIGINAL_PDF_PINS_RECHECKED_AND_ADDITIONAL_CGHS_SOURCE_PINNED_IN_FROZEN_AUDIT',historical_literature_status='BOUNDED_NEGATIVE_SEARCH_NO_COMPLETE_SOLUTION_VERIFIED',imported_theorems='EXTERNAL_INPUTS_NOT_MACHINE_CERTIFIED',CGHS_conversion='KNOWN_MOVED_BOUNDARY_SYMPLECTIC_AND_COMPLEX_ENDPOINTS',smooth_class='UNMARKED_CLASS_RETAINED_UNDER_TRACKED_SMOOTH_ISOTOPIES',Hamiltonian_distinction_survival='UNRESOLVED',fixed_Legendrian_Stokes_obstruction='VALID',target_clauses=['smooth_versus_complex_UNRESOLVED','smooth_versus_symplectic_UNRESOLVED','infinite_family_UNRESOLVED'],mathematical_status='UNRESOLVED_PARTIAL',novelty='NOT_ESTABLISHED',general_problem='UNSOLVED')
        finally:
            for folder in folders:folder.chmod(0o755)
            for path in mapping.values():path.chmod(0o644)


def main():
    need(len(sys.argv)==4,'expected manifest pin, bootstrap pin, packet directory')
    manifest_pin,bootstrap_pin,path=sys.argv[1:];root=Path(os.path.abspath(path))
    snapshot,parsed=integrity(root,manifest_pin,bootstrap_pin);result=replay(snapshot,parsed)
    after,after_parsed=integrity(root,manifest_pin,bootstrap_pin)
    need(after==snapshot and same(after_parsed,parsed),'publication changed during replay')
    result.update(schema=1,problem_id=2980,status='PASS',publication_files=len(FILES),optimization=sys.flags.optimize,uid=os.getuid(),euid=os.geteuid(),queue_status='unsolved',substantive_turns='5/5',manifest_sha256=manifest_pin,bootstrap_sha256=bootstrap_pin)
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):
        print('REJECT: publication integrity/replay validation failed',file=sys.stderr);sys.exit(1)
