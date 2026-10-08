#!/usr/bin/env python3
"""Authenticate public medianity partial results; replay source-free finite checks."""
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

ACCEPTED = {'evidence/PUBLIC_DERIVATIONS.json': {'bytes': 1173, 'sha256': '5a22676f1b12840f5146dec7da907df47a703a25f43ca76716a0b799b90a3607'}, 'evidence/audit/AUDIT.md': {'bytes': 17059, 'sha256': '754b0b0d9aa393d047235bb49d284fa3cdaaa17330cced3d8553212423f2a561'}, 'evidence/audit/AUDIT_MANIFEST.json': {'bytes': 1084, 'sha256': '36cdefd6e4feab893860695d4d84cee0408e82047c7b4d5a989e94aa080a07e3'}, 'evidence/audit/DESCENT_REPLAY.json': {'bytes': 3399, 'sha256': '7f722d0dc03db6d809a86e7a6a501a8f7a548e9d7deef505d468efb0149cf871'}, 'evidence/audit/HISTORICAL_REPLAY.json': {'bytes': 15790, 'sha256': '22148df411e9f1233cc87ad52b36a18708375f66fc13646c4ba377471e096b7b'}, 'evidence/audit/SOURCE_NORMALIZATION_ADDENDUM.md': {'bytes': 1369, 'sha256': '2a0a423ce70e6e072254c08dbddc2e35f80de103dae15ffb44d5f11c9e66fea2'}, 'evidence/audit/SOURCE_PINS.json': {'bytes': 3049, 'sha256': '9ba85e5cde1922cb1dfb375eb13af8687724422f3c10e97c6020accb8cab6055'}, 'evidence/audit/verify_descent.py': {'bytes': 5392, 'sha256': '31bbae4c01c939e91a7a56e9c8d2a74d09bcd23d5140f8b38090b45e625821a2'}, 'evidence/candidate/BUDGET.json': {'bytes': 1904, 'sha256': '601fe6439a0b37231b594ef217ae312b9eab1b3a27d573112f9eec7af133602f'}, 'evidence/candidate/MANIFEST.json': {'bytes': 1293, 'sha256': 'f4091f4ddbb9841ed7bbb0e42a2ea0fd1ffbf58a3856c8c316b1d2ef937aa79c'}, 'evidence/candidate/PARTIAL_REPORT.md': {'bytes': 14086, 'sha256': 'e05d1eb4a72c853bcaeb19f7163ac49c977298aab740338a1e894301f6b38fd8'}, 'evidence/candidate/README.md': {'bytes': 1651, 'sha256': 'efd5445b56a02a9b91594b9ea0c5164f794b012b656b63445dcb4f3677ed3905'}, 'evidence/candidate/SCOPED_REVIEW.md': {'bytes': 5387, 'sha256': 'f252a49b3ce5d880a9eaa40c2c9330346db357a4e8ab0afe75163f0da2f5d3b3'}, 'evidence/candidate/SOURCE_AUDIT.json': {'bytes': 3949, 'sha256': 'ce54fa8a4d959cf8ff3f9f81927e18542e958ed2d3119bd8628e1cb2b8bc6962'}, 'evidence/candidate/VARIATIONAL_AND_BICOMBING.md': {'bytes': 7617, 'sha256': '14adce1622ef7f1c2a68a9544b25d48dfac47d06016072ba19ca4f95fd660f36'}, 'evidence/candidate/verify_bundle.py': {'bytes': 2051, 'sha256': '48dad115a8f3fd798884e1e7dff02bc8d20a14bdd4be5e9a7563538e071d7a01'}, 'evidence/candidate/verify_inputs.py': {'bytes': 1947, 'sha256': '01ffb0d86fd46bd6fb21816c2fe7fe006bf650b60cfbbba00329f534e989954f'}, 'evidence/candidate/verify_math.py': {'bytes': 6738, 'sha256': 'ff50f9b336fe7cf8220d89cabb5dea75bce1994c0f157f7466af04218da8f74d'}}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'evidence', 'evidence/candidate', 'evidence/audit'}

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
    exact_int(value['problem_id'], 30006624)
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


def bound_mapping(value, prefix, manifest_name):
    rows=value['files'];expected={n[len(prefix):] for n in ACCEPTED if n.startswith(prefix)}-{manifest_name}
    need(type(rows) is dict and set(rows)==expected,'inner manifest exact inventory')
    for name,row in rows.items():
        keys(row,['bytes','sha256']);exact_int(row['bytes']);digest(row['sha256'])
        need(same(row,ACCEPTED[prefix+name]),'inner manifest exact byte binding')


def integrity(root,manifest_pin,bootstrap_pin):
    import ast
    digest(manifest_pin);digest(bootstrap_pin);inventory(root)
    snapshot={n:ordinary(root/n) for n in FILES}
    need(sha(snapshot['PUBLICATION_MANIFEST.json'])==manifest_pin,'external manifest pin')
    need(sha(snapshot['BOOTSTRAP.py'])==bootstrap_pin,'external bootstrap pin')
    parsed={n:parse(raw) for n,raw in snapshot.items() if n.endswith('.json')}
    manifest(parsed['PUBLICATION_MANIFEST.json'],snapshot,PAYLOAD)
    for n,row in ACCEPTED.items():need(same(row,dict(bytes=len(snapshot[n]),sha256=sha(snapshot[n]))),'accepted public bytes changed')
    candidate=parsed['evidence/candidate/MANIFEST.json'];keys(candidate,['schema','status','files']);exact_int(candidate['schema'],1)
    need(candidate['status']=='UNSOLVED','public candidate scope');bound_mapping(candidate,'evidence/candidate/','MANIFEST.json')
    audit=parsed['evidence/audit/AUDIT_MANIFEST.json'];keys(audit,['schema','target_id','scope','full_target_status','substantive_families','source_free','mathematical_correction_required','files'])
    exact_int(audit['schema'],1);exact_int(audit['target_id'],30006624);exact_int(audit['substantive_families'],5)
    need(audit['scope']=='PUBLIC_DERIVATIVE_UNSOLVED_PARTIAL' and audit['full_target_status']=='UNSOLVED','public audit scope')
    need(audit['source_free'] is True and audit['mathematical_correction_required'] is False,'public audit flags')
    bound_mapping(audit,'evidence/audit/','AUDIT_MANIFEST.json')
    derivation=parsed['evidence/PUBLIC_DERIVATIONS.json'];exact_int(derivation['schema'],1);exact_int(derivation['problem_id'],30006624)
    need(derivation['full_target_status']=='UNSOLVED' and derivation['original_complete_bundle_replay']=='NOT_RUN' and derivation['fresh_sources']=='NOT_RUN' and derivation['mathematical_patch_required'] is False,'derivative scope')
    budget=parsed['evidence/candidate/BUDGET.json'];exact_int(budget['target_id'],30006624);exact_int(budget['same_target_component_id'],30006622)
    exact_int(budget['substantive_families'],5);exact_int(budget['original_prior_substantive_attempts_found'],0)
    need(budget['outcome']=='UNSOLVED' and budget['full_candidate'] is False and budget['no_novelty_claim'] is True,'shared five-family scope')
    need(type(budget['families']) is list and len(budget['families'])==5,'family inventory')
    for i,row in enumerate(budget['families'],1):exact_int(row['number'],i)
    history=parsed['evidence/audit/HISTORICAL_REPLAY.json'];exact_int(history['schema'],1);exact_int(history['target_id'],30006624)
    for key,count in [('mathematical_positive_runs',3),('mathematical_negative_runs',18),('external_input_positive_runs',3),('external_input_negative_runs',3)]:exact_int(history[key],count)
    need(history['status']=='HISTORICAL_METADATA_PUBLIC_DERIVATIVE' and len(history['records'])==27,'public historical receipt scope')
    supplemental=parsed['evidence/audit/DESCENT_REPLAY.json'];exact_int(supplemental['positive_runs'],3);exact_int(supplemental['negative_runs'],9)
    need(supplemental['status']=='PASS' and len(supplemental['records'])==12,'supplemental receipt scope')
    for n,raw in snapshot.items():
        if n.endswith('.py'):need(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(raw))),'zero disabled asserts')
    inventory(root);return snapshot,parsed


def stable_receipt(value):
    """Only fresh absolute traceback strings, sizes and hashes vary on relocation."""
    if type(value) is dict:return {k:stable_receipt(v) for k,v in value.items() if k not in {'stderr','stderr_sha256','stderr_bytes'}}
    if type(value) is list:return [stable_receipt(v) for v in value]
    return value


def replay(snapshot,parsed):
    import shutil
    need(os.getuid()==os.geteuid()==1000,'actual UID/EUID1000 required')
    mode=sys.flags.optimize;flags=[] if mode==0 else ['-'+('O'*mode)]
    history=[r for r in parsed['evidence/audit/HISTORICAL_REPLAY.json']['records'] if r['optimization']==mode]
    supplemental=[r for r in parsed['evidence/audit/DESCENT_REPLAY.json']['records'] if r['optimization']==mode]
    need(len(history)==9 and len(supplemental)==4,'mode receipt inventory')
    with tempfile.TemporaryDirectory(prefix='medianity-publication-') as directory:
        work=Path(directory);evidence=work/'evidence';cwd=work/'cwd';cwd.mkdir()
        (evidence/'candidate').mkdir(parents=True);(evidence/'audit').mkdir()
        for name,raw in snapshot.items():
            if name.startswith('evidence/'):(work/name).write_bytes(raw)
        candidate=evidence/'candidate';audit=evidence/'audit';badbytes=work/'bad_bytes';badscope=work/'bad_scope'
        shutil.copytree(candidate,badbytes);shutil.copytree(candidate,badscope)
        (badbytes/'PARTIAL_REPORT.md').write_bytes((badbytes/'PARTIAL_REPORT.md').read_bytes()+b'\n')
        wrong=parse((badscope/'BUDGET.json').read_bytes());wrong['outcome']='SOLVED';wrong['full_candidate']=True
        (badscope/'BUDGET.json').write_text(json.dumps(wrong,indent=2)+'\n')
        wrongmanifest=parse((badscope/'MANIFEST.json').read_bytes());raw=(badscope/'BUDGET.json').read_bytes()
        wrongmanifest['files']['BUDGET.json']=dict(bytes=len(raw),sha256=sha(raw));(badscope/'MANIFEST.json').write_text(json.dumps(wrongmanifest,indent=2)+'\n')
        for directory in [evidence,badbytes,badscope,cwd]:
            for path in directory.rglob('*'):path.chmod(0o555 if path.is_dir() else 0o444)
            directory.chmod(0o555)
        env=dict(PATH=os.defpath,HOME=str(work),TMPDIR=str(work),LC_ALL='C',PYTHONNOUSERSITE='1',PYTHONDONTWRITEBYTECODE='1',PYTHONSAFEPATH='1')
        records=[];probes=[]
        try:
            for path in [candidate/'README.md',candidate/'NEW_FILE',audit/'verify_descent.py',audit/'NEW_FILE',badbytes/'PARTIAL_REPORT.md',badscope/'NEW_FILE',cwd/'NEW_FILE']:
                try:
                    with path.open('ab') as stream:stream.write(b'forbidden')
                except PermissionError:probes.append(path.relative_to(work).as_posix())
                else:raise ValueError('readonly write succeeded')
            def execute(script,args,expected,comparison):
                proc=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(script),*args],cwd=cwd,env=env,capture_output=True,timeout=180)
                stdout=proc.stdout.decode();stderr=proc.stderr.decode()
                need(type(expected['exit_code']) is int and proc.returncode==expected['exit_code'],'exact native exit code')
                record=dict(script=script.name,optimization=mode,arguments=args,exit_code=proc.returncode,stdout=stdout,stderr=stderr,stdout_bytes=len(proc.stdout),stderr_bytes=len(proc.stderr),stdout_sha256=sha(proc.stdout),stderr_sha256=sha(proc.stderr),comparison=comparison)
                if proc.returncode==0:
                    need(stderr=='' and same(parse(proc.stdout),expected['output']),'complete native typed positive output')
                    if 'stdout_sha256' in expected:need(sha(proc.stdout)==expected['stdout_sha256'],'complete historical positive stdout byte identity')
                    record['output']=parse(proc.stdout)
                else:
                    need(proc.returncode==1 and stdout=='' and stderr.startswith('Traceback (most recent call last):\n') and stderr.splitlines()[-1]==expected['rejection'],'intended exact native RuntimeError; arbitrary crashes reject')
                    if 'stdout_sha256' in expected:need(sha(proc.stdout)==expected['stdout_sha256'],'negative historical stdout identity')
                    record['rejection']=expected['rejection']
                records.append(record)
            public_output=dict(status='PASS',uid=1000,optimization=mode,members=10,source_free_extension_check=True,manifest_sha256=ACCEPTED['evidence/candidate/MANIFEST.json']['sha256'])
            execute(candidate/'verify_bundle.py',[],dict(exit_code=0,output=public_output),'DIRECT_EXPECTATION_FOR_ACTUAL_PUBLIC_MANIFEST; NOT_HISTORICAL_FULL_BUNDLE')
            not_run=[]
            for hist in history:
                if hist['script']=='verify_inputs.py':
                    not_run.append(dict(script=hist['script'],historical_expected_pass=hist['expected_pass'],fresh_status='NOT_RUN'));continue
                need(hist['script']=='verify_math.py' and type(hist['arguments']) is list,'historical mathematical record')
                execute(candidate/'verify_math.py',hist['arguments'],hist,'UNCHANGED_MATHEMATICS_COMPLETE_HISTORICAL_OUTPUT_OR_EXACT_REJECTION')
            for target,message in [(badbytes,'RuntimeError: Frozen byte mismatch: PARTIAL_REPORT.md'),(badscope,'RuntimeError: Full target overclaim')]:
                execute(target/'verify_bundle.py',[],dict(exit_code=1,rejection=message),'FRESH_PUBLIC_CANDIDATE_INTEGRITY_CONTROL')
            for hist in supplemental:
                args=[] if hist['mutation'] is None else ['--mutation',hist['mutation']]
                expected=dict(exit_code=hist['exit_code'],output=hist['stdout'],rejection=hist['rejection'])
                execute(audit/'verify_descent.py',args,expected,'COMPLETE_SUPPLEMENTAL_HISTORICAL_OUTPUT_OR_EXACT_REJECTION')
            need(len(records)==14 and sum(r['exit_code']==0 for r in records)==3 and sum(r['exit_code']==1 for r in records)==11,'native source-free coverage')
            for name,raw in snapshot.items():
                if name.startswith('evidence/'):need((work/name).read_bytes()==raw,'public evidence changed')
            need(not list(cwd.iterdir()),'readonly cwd changed')
            return dict(native_records=records,native_positive_runs=3,native_expected_rejections=11,
                        historical_mathematical_positive_runs=3,historical_mathematical_negative_runs=18,
                        historical_external_input_positive_runs=3,historical_external_input_negative_runs=3,
                        historical_unreplayed_source_rows_this_mode=not_run,
                        historical_comparison='Unchanged mathematical stdout bytes and full typed JSON match retained historical metadata; supplemental complete outputs match. Negative exact exit, empty stdout and final intended RuntimeError match; historical traceback bytes were not retained, so no traceback byte identity is claimed. Full fresh stdout/stderr retained.',
                        original_complete_bundle_replay='NOT_RUN',public_bundle_replay='DIRECTLY_AUTHENTICATED_PUBLIC_FILES; NOT_EQUIVALENT_TO_HISTORICAL_FULL_BUNDLE',
                        readonly_write_probes_denied=probes,readonly_file_mode='0444',readonly_directory_mode='0555',
                        fresh_source_bindings='NOT_RUN',fresh_corpus_bindings='NOT_RUN',fresh_source_corruption_controls='NOT_RUN',
                        imported_theorems='EXTERNAL_INPUTS_NOT_MACHINE_CERTIFIED',full_target_status='UNSOLVED',
                        accepted_partial='COMPLETE_ALMOST_MODULAR_IMPLIES_MODULAR',unresolved_gap='GLOBAL_APPROXIMATE_MEDIAN_EXISTENCE',
                        source_normalization_addendum='MANDATORY_THREE_DISTINCT_PAIRS',novelty='NOT_ESTABLISHED',mathematical_correction_required=False)
        finally:
            for path in work.rglob('*'):
                if not path.is_symlink():path.chmod(0o755 if path.is_dir() else 0o644)


def main():
    need(len(sys.argv)==4,'expected manifest pin, bootstrap pin, packet directory')
    manifest_pin,bootstrap_pin,path=sys.argv[1:];root=Path(os.path.abspath(path))
    snapshot,parsed=integrity(root,manifest_pin,bootstrap_pin);result=replay(snapshot,parsed)
    after,after_parsed=integrity(root,manifest_pin,bootstrap_pin)
    need(after==snapshot and same(after_parsed,parsed),'public packet changed during replay')
    result.update(schema=1,problem_id=30006624,status='PASS',publication_files=len(FILES),optimization=sys.flags.optimize,uid=os.getuid(),euid=os.geteuid(),queue_status='unsolved',substantive_turns='5/5',manifest_sha256=manifest_pin,bootstrap_sha256=bootstrap_pin)
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):
        print('REJECT: publication integrity/replay validation failed',file=sys.stderr);sys.exit(1)
