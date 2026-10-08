#!/usr/bin/env python3
"""Authenticate frozen exotic mapping-class torsion partial results; replay source-free finite checks."""
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

ACCEPTED = {'original/FREEZE_RECEIPT.json': {'bytes': 514, 'sha256': '188e0fc0a7940b7a26f3aeb14a0144ba84a3b7b213af1f7e49408908ad89a65f'}, 'original/exotic_mapping_torsion_2956_sourcefree.zip': {'bytes': 21964, 'sha256': 'cd72bc9863fb1cf4d99a22471ff712c7a59a3b2ed15d3323583204182865a570'}, 'original/frozen_v1/EXACT_CHECKS.json': {'bytes': 11023, 'sha256': '1d349aa78a91369f62a886273cef5b03df4d8860b576e77dfbf86177d17138a4'}, 'original/frozen_v1/FROZEN_MANIFEST.json': {'bytes': 1182, 'sha256': 'bbb98a52fe3279b655a768147fab72bae6f0eb51aa01e5f97468f49ce192d4f1'}, 'original/frozen_v1/REPORT.md': {'bytes': 35690, 'sha256': 'b8ffa82c80ed0c05807155ddb3c12d4154aea080a17a25be7c79677b3a65eab9'}, 'original/frozen_v1/RUN_METADATA.json': {'bytes': 2484, 'sha256': 'b7ece8a5b4a88424e556dea86950916bcce73e58aa39c6cc71db69c46112463d'}, 'original/frozen_v1/SOURCE_METADATA.json': {'bytes': 7746, 'sha256': '15d0a8e38b63217c71664a5052fc6cd61eb71a54b71f10153461a122eec1ca78'}, 'original/frozen_v1/verify_exact.py': {'bytes': 6241, 'sha256': '79bd23c24dd6d5fdf9f6a513a9acbe90813606293384ccb02e1d6197f5c89469'}, 'audit/AUDIT_RECEIPT.json': {'bytes': 655, 'sha256': '4b424dae924dbbb637cdf2cd6784c7967db449bb2594587c7829ff5a15181577'}, 'audit/exotic_mapping_torsion_2956_independent_audit_sourcefree.zip': {'bytes': 29127, 'sha256': 'ab0d2fb046f4cce7677a5f7589633f0cd31c618e53b8ca519391a109a01a3a07'}, 'audit/public/AUDIT_MANIFEST.json': {'bytes': 2887, 'sha256': 'b907a40f950a82aa52d692873890250e9c5bb71ae18cbc2b737dc48886d79242'}, 'audit/public/AUDIT_REPORT.md': {'bytes': 14527, 'sha256': '02bcdf2f2acfe8c60b8510811701d89be6cda23570640233c65e98cd7bddcdd6'}, 'audit/public/INDEPENDENT_EXACT_RESULTS.json': {'bytes': 6302, 'sha256': '33b43423705492a55f056b297aecf2dba79231909bc6a0b3c760dda41e0e3685'}, 'audit/public/INDEPENDENT_MUTATION_RESULTS.json': {'bytes': 25247, 'sha256': '122d5fd908e2659a04226d4bf5edde030d412bee4c7b2227edd7fe1184ea451c'}, 'audit/public/INPUT_PINS.json': {'bytes': 2187, 'sha256': '4a8e8d65ca3e7b97876af781e2a19d2fcd8c17709d04959e1d6ab0d0d71c8675'}, 'audit/public/INSPECTION_HISTORY.json': {'bytes': 3235, 'sha256': '613fb60677105ca6536fed21e6f19f5c7060c87f122da1b5dd18093af1589c78'}, 'audit/public/READONLY_MUTATION_RESULTS.json': {'bytes': 32345, 'sha256': '353e4d0931f60631f1b476fb431f984ff0e8a8647649fcba02b7012a78c6e59e'}, 'audit/public/REPRODUCE.md': {'bytes': 2744, 'sha256': '92dff003bb56e78838df27b178491abbf0319b06cbf36fe71850c86554ad5139'}, 'audit/public/SOURCE_PIN_RECHECK.json': {'bytes': 4957, 'sha256': 'b7e7ecb96a7e9b06b048b8c921c8fc2268aabbb5a26bc98d4e3d225118055051'}, 'audit/public/VERIFY_EXACT_OPTIMIZATION_FIX.patch': {'bytes': 3573, 'sha256': '082c5aa24a747e09fbbcf8a2fcc32db750e0af90ab88f1e9e6fe9e74cee6d76d'}, 'audit/public/independent_exact.py': {'bytes': 7095, 'sha256': '93df51370ad54240cfc0542b7fa8162eaf449a92ffa6556f6d0212abd26c5810'}, 'audit/public/run_independent_mutations.py': {'bytes': 3415, 'sha256': 'a24ae9e599f92958da6c05fc1cb5a83b30a9941c039b87f450da7ffd99dcb07c'}, 'audit/public/run_readonly_audit.py': {'bytes': 5200, 'sha256': '87a5de8a8bd79823e5f40b5b1ae0b089a60c6bdce8266d61bcf29616ff3943c9'}, 'corrected_v1/EXACT_CHECKS.json': {'bytes': 11023, 'sha256': '1d349aa78a91369f62a886273cef5b03df4d8860b576e77dfbf86177d17138a4'}, 'corrected_v1/verify_exact.py': {'bytes': 6917, 'sha256': '8d24a326b7b2d9f3b381e030f7bb6e4b67cc0a9691719959517066ba52bfe0c5'}}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'original', 'original/frozen_v1', 'audit', 'audit/public', 'corrected_v1'}


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
    exact_int(value['problem_id'], 2956)
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
    # Pinned archives are opened in memory, never extracted or executed.
    import io, zipfile, ast
    def archive(name, mapping):
        with zipfile.ZipFile(io.BytesIO(snapshot[name])) as z:
            infos=z.infolist()
            need(len(infos)==len(mapping) and {i.filename for i in infos}==set(mapping),'archive exact inventory')
            for info in infos:
                need(not info.is_dir() and info.file_size==len(snapshot[mapping[info.filename]]),'archive entry size')
                need(z.read(info)==snapshot[mapping[info.filename]],'archive member bytes')
    names={n[len('original/frozen_v1/'):]:n for n in ACCEPTED if n.startswith('original/frozen_v1/')}
    archive('original/exotic_mapping_torsion_2956_sourcefree.zip',names)
    names={n[len('audit/'):]:n for n in ACCEPTED if n.startswith('audit/public/')}
    names.update({n:n for n in ACCEPTED if n.startswith('corrected_v1/')})
    archive('audit/exotic_mapping_torsion_2956_independent_audit_sourcefree.zip',names)
    for manifest_name,prefixes,exempt in [
        ('original/frozen_v1/FROZEN_MANIFEST.json',{'':'original/frozen_v1/'},'original/frozen_v1/FROZEN_MANIFEST.json'),
        ('audit/public/AUDIT_MANIFEST.json',{'public/':'audit/public/','corrected_v1/':'corrected_v1/'},'audit/public/AUDIT_MANIFEST.json')]:
        m=parsed[manifest_name]
        need(type(m['problem_id']) is int and m['problem_id']==2956 and m['problem_code']=='KP-4.80','manifest problem')
        expected={n for n in ACCEPTED if any(n.startswith(x) for x in prefixes.values())}-{exempt}
        seen=set()
        for row in m['files']:
            keys(row,['file','bytes','sha256']);exact_int(row['bytes']);digest(row['sha256'])
            name=row['file'];need(type(name) is str,'manifest filename')
            candidates=[target+name[len(source):] for source,target in prefixes.items() if name.startswith(source)]
            need(len(candidates)==1,'manifest prefix')
            full=candidates[0];need(full in expected and full not in seen,'manifest mapping inventory')
            seen.add(full);need(same({k:row[k] for k in ['bytes','sha256']},ACCEPTED[full]),'manifest metadata')
        need(seen==expected,'manifest complete inventory')
    need(snapshot['corrected_v1/EXACT_CHECKS.json']==snapshot['original/frozen_v1/EXACT_CHECKS.json'],'unchanged expected output')
    original=snapshot['original/frozen_v1/verify_exact.py']
    corrected=snapshot['corrected_v1/verify_exact.py']
    patch=snapshot['audit/public/VERIFY_EXACT_OPTIMIZATION_FIX.patch']
    need(apply_patch(original,patch)==corrected,'actual patch reconstruction')
    need(sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(original)))==10,'original ten assert nodes')
    need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(corrected))),'corrected zero assert nodes')
    need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(snapshot['audit/public/independent_exact.py']))),'independent zero assert nodes')
    need(parsed['original/frozen_v1/RUN_METADATA.json']['mathematical_approaches_completed']==5,'five approaches')
    inventory(root)
    return snapshot, parsed


def apply_patch(original, patch):
    """Strictly apply the preserved unified patch to the preserved original."""
    source=original.decode().splitlines(keepends=True);lines=patch.decode().splitlines(keepends=True)
    need(lines[:2]==['--- frozen_v1/verify_exact.py\n','+++ corrected_v1/verify_exact.py\n'],'patch file headers')
    result=[];cursor=0;i=2;hunks=0
    while i<len(lines):
        match=re.fullmatch(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n',lines[i]);need(match is not None,'patch hunk header')
        old_start,old_count,new_start,new_count=map(int,match.groups());i+=1
        need(old_start-1>=cursor,'patch old position');result.extend(source[cursor:old_start-1]);cursor=old_start-1
        need(len(result)==new_start-1,'patch new position');old_used=new_used=0
        while i<len(lines) and not lines[i].startswith('@@ '):
            line=lines[i];i+=1;need(line and line[0] in ' +-','patch line kind')
            if line[0] in ' -':
                need(cursor<len(source) and source[cursor]==line[1:],'patch exact context')
                cursor+=1;old_used+=1
            if line[0] in ' +':result.append(line[1:]);new_used+=1
        need((old_used,new_used)==(old_count,new_count),'patch hunk sizes');hunks+=1
    need(hunks==6,'expected exact six hunks')
    result.extend(source[cursor:]);return ''.join(result).encode()


def replay(snapshot, parsed):
    import copy
    need(hasattr(os,'geteuid') and os.getuid()==os.geteuid()==1000,'actual UID/EUID1000 required')
    flags=[] if sys.flags.optimize==0 else ['-'+('O'*sys.flags.optimize)]
    cases=[
        ('odd_rank_one_allowed','expected=sorted({0,n-1} if n%2 else {0,1,n-1})','expected=sorted({0,1,n-1})'),
        ('scalar_diagonal_condition_removed',' and v.bit_count()%2==0]',']'),
        ('wrong_triple_diagonal','delta=7','delta=3'),
        ('reflection_generator_dropped','        refl.append(s)','        if i != 0:\n            refl.append(s)'),
        ('coxeter_product_omitted','        coxeter = matmul(coxeter,s)','        coxeter = coxeter')]
    independent_cases=[]
    def case(name,change):
        d=copy.deepcopy(parsed['corrected_v1/EXACT_CHECKS.json']);change(d);independent_cases.append((name,d))
    case('odd_rank_one_claim',lambda d:d['permutation_modules'][1].update(permitted_twist_group_ranks=[0,1,2]))
    case('wrong_triple_generator',lambda d:d['triple_quotient'].update(neck_generators=[1,2,2]))
    case('wrong_A2_group_order',lambda d:d['A_type_reflection_groups'][1].update(generated_matrix_group_order=3))
    case('false_eta4_nonvanishing',lambda d:d['nonequivariant_BF_arithmetic'][1]['neck_cases'][0].update(spin_choice_left='eta^3_nonzero_order_2'))
    case('wrong_twoK3_spin_lift',lambda d:d['nonequivariant_BF_arithmetic'][0]['neck_cases'][0].update(spin_choice_right='zero'))
    case('wrong_connected_sum_Euler',lambda d:d['K3_sums'][2].update(euler_characteristic=72))
    case('truncated_module_coverage',lambda d:d['permutation_modules'].pop())
    case('truncated_root_coverage',lambda d:d['A_type_reflection_groups'].pop())
    with tempfile.TemporaryDirectory(prefix='exotic-torsion-publication-') as directory:
        work=Path(directory);records=[];probes=[];folders=[];all_bytes={}
        def specimen(label,files):
            folder=work/label;folder.mkdir();folders.append(folder)
            for name,raw in files.items():
                path=folder/name;path.write_bytes(raw);path.chmod(0o444);all_bytes[path]=raw
            folder.chmod(0o555)
            denied=[]
            for path in [folder/'NEW_FILE',folder/next(iter(files))]:
                try:
                    with path.open('ab') as f:f.write(b'forbidden')
                except PermissionError:denied.append(path.name)
                else:raise ValueError('readonly write succeeded')
            probes.append(dict(specimen=label,directory_mode='0o555',file_modes='0o444',denied=denied,uid=os.getuid(),euid=os.geteuid()))
            return folder
        env=dict(PATH=os.defpath,HOME=str(work),TMPDIR=str(work),LC_ALL='C',PYTHONNOUSERSITE='1',PYTHONDONTWRITEBYTECODE='1',PYTHONSAFEPATH='1')
        def run(folder,script,args,label,expected=None,should_reject=False,false_pass=False):
            proc=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(folder/script),*args],cwd=folder,env=env,capture_output=True,timeout=300)
            if should_reject:
                need(proc.returncode==1 and proc.stdout==b'' and b'AssertionError' in proc.stderr and b'PermissionError' not in proc.stderr,'explicit semantic rejection')
                need(proc.stderr.decode().splitlines()[-1].startswith('AssertionError'),'semantic last line')
            else:
                need(proc.returncode==0 and proc.stderr==b'','successful semantic run')
                output=parse(proc.stdout)
                if expected is not None:need(proc.stdout==expected,'complete exact output mismatch')
                if false_pass:need(output['all_assertions_passed'] is True,'original optimized false-PASS expected')
            historical_mode='normal' if sys.flags.optimize==0 else 'O'*sys.flags.optimize
            if label.startswith(('original_','corrected_')):
                implementation,_,case_name=label.partition('_')
                rows=[row for row in parsed['audit/public/READONLY_MUTATION_RESULTS.json']['runs'] if row['implementation']==implementation and row['case']==case_name and row['mode']==historical_mode]
                need(len(rows)==1,'unique historical candidate execution')
                row=rows[0]
                need(proc.returncode==row['returncode'] and len(proc.stdout)==row['stdout_bytes'] and sha(proc.stdout)==row['stdout_sha256'],'exact historical candidate output hash/size and exit')
            else:
                case_name=label[len('independent_'):]
                rows=[row for row in parsed['audit/public/INDEPENDENT_MUTATION_RESULTS.json']['runs'] if row['case']==case_name and row['mode']==historical_mode]
                need(len(rows)==1,'unique historical independent execution')
                row=rows[0]
                need(proc.returncode==row['returncode'] and sha(proc.stdout)==row['stdout_sha256'],'exact historical independent output hash and exit')
            if proc.stderr:
                need(proc.stderr.decode().splitlines()[-1]==row['stderr'].splitlines()[-1],'exact historical semantic failure message')
            # All output text retained. Only the random disposable path is tokenized.
            records.append(dict(case=label,returncode=proc.returncode,stdout=proc.stdout.decode(),stderr=proc.stderr.decode().replace(str(work),'<temporary>'),expected_outcome='ORIGINAL_OPTIMIZED_FALSE_PASS' if false_pass else 'SEMANTIC_REJECTION' if should_reject else 'EXACT_BASELINE_MATCH'))
        try:
            for version,source_name in [('original','original/frozen_v1/verify_exact.py'),('corrected','corrected_v1/verify_exact.py')]:
                source=snapshot[source_name].decode()
                variants=[('baseline',source)]
                for name,old,new in cases:
                    need(source.count(old)==1,'unique semantic replacement');variants.append((name,source.replace(old,new)))
                for name,body in variants:
                    label=version+'_'+name;folder=specimen(label,{'verify_exact.py':body.encode()})
                    false_pass=name!='baseline' and version=='original' and sys.flags.optimize>0
                    reject=name!='baseline' and not false_pass
                    run(folder,'verify_exact.py',[],label,expected=snapshot['corrected_v1/EXACT_CHECKS.json'] if name=='baseline' else None,should_reject=reject,false_pass=false_pass)
            baseline=snapshot['corrected_v1/EXACT_CHECKS.json'];cached=snapshot['audit/public/INDEPENDENT_EXACT_RESULTS.json']
            for label,data in [('baseline',None),*independent_cases]:
                raw=baseline if data is None else (json.dumps(data,sort_keys=True)+'\n').encode()
                folder=specimen('independent_'+label,{'independent_exact.py':snapshot['audit/public/independent_exact.py'],'candidate.json':raw,'cached.json':cached})
                args=['--candidate',str(folder/'candidate.json')]
                if data is not None:args+=['--cached',str(folder/'cached.json')]
                run(folder,'independent_exact.py',args,'independent_'+label,expected=cached if data is None else None,should_reject=data is not None)
            for path,raw in all_bytes.items():need(ordinary(path)==raw,'readonly specimen changed')
            need(len(records)==21 and len(probes)==21,'exact execution coverage')
            return dict(execution_records=records,stderr_random_path_tokenized=True,readonly_probes=probes,
                full_stdout_compared_byte_for_byte=True,independent_baseline='FRESH_RREF_AND_PERMUTATION_RECOMPUTATION',independent_mutants='PINNED_EXPECTED_CACHE_NOT_RECOMPUTATION',
                original_optimized_false_passes=5 if sys.flags.optimize else 0,original_normal_semantic_rejections=0 if sys.flags.optimize else 5,
                corrected_semantic_rejections=5,independent_semantic_rejections=8,baseline_runs=3,actual_patch_reconstruction=True,
                historical_source_bindings='ELEVEN_PDF_PINS_MATCHED_IN_FROZEN_AUDIT',historical_corpus_bindings='TWO_DATASET_PINS_AND_UNIQUE_RECORD_MATCHED_IN_FROZEN_AUDIT',
                fresh_source_bindings='NOT_RUN',fresh_corpus_bindings='NOT_RUN',ruberman_original_proof='NOT_INSPECTED_IMPORTED_VIA_KONNO',
                nonequivariant_eta4_detector='VANISHES_DOES_NOT_PROVE_NECK_TRIVIALITY',three_K3_neck_nontriviality='UNPROVED',
                mathematical_report_changed=False,novelty='NOT_ESTABLISHED',general_problem='UNSOLVED',python_version=sys.version)
        finally:
            for folder in folders:
                folder.chmod(0o755)
                for path in folder.iterdir():path.chmod(0o644)


def main():
    need(len(sys.argv)==4,'expected external manifest pin, bootstrap pin, packet directory')
    manifest_pin,bootstrap_pin,path=sys.argv[1:];root=Path(os.path.abspath(path))
    snapshot,parsed=integrity(root,manifest_pin,bootstrap_pin)
    result=replay(snapshot,parsed)
    after,after_parsed=integrity(root,manifest_pin,bootstrap_pin)
    need(after==snapshot and same(after_parsed,parsed),'publication changed during replay')
    result.update(schema=1,problem_id=2956,status='PASS',publication_files=len(FILES),optimization=sys.flags.optimize,
        uid=os.getuid(),euid=os.geteuid(),queue_status='unsolved',substantive_turns='5/5',manifest_sha256=manifest_pin,bootstrap_sha256=bootstrap_pin)
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):
        print('REJECT: publication integrity/replay validation failed',file=sys.stderr)
        sys.exit(1)
