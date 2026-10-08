#!/usr/bin/env python3
"""Authenticate frozen trisection proof and bounded partial results; replay source-free finite checks."""
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

ACCEPTED = {'evidence/AUDIT_REPORT.md': {'bytes': 18583, 'sha256': '9769dd4fe7c62e3fea70a48d5a53620c353a7641d0ed60a13b4e3de99d675eaf'}, 'evidence/PUBLICATION_ENVELOPE.json': {'bytes': 4020, 'sha256': '90a91ee509f88c05bce04a3359ee01726358c1d4f7ef06c8d6477d1052c8a664'}, 'evidence/README.md': {'bytes': 2837, 'sha256': 'dd87001fe7e98888f1c0805b727fd0a7cf2d7215b2327d4e221f2d620d5b3e6e'}, 'evidence/SOURCE_REVIEW.md': {'bytes': 10691, 'sha256': 'd9fe062963b11c9afe467c41800320c4c051cc0b90ed7c1225bc415a5fe03d82'}, 'evidence/VERIFICATION_METADATA.json': {'bytes': 3917, 'sha256': '4603602d10d9d7a7be0751021fe4abeb41e5be38a85733228e374e43b62b562a'}, 'evidence/audit_exact.py': {'bytes': 15799, 'sha256': 'a54f7ffb2358b089db9a744cfdc0030783018470f34aa670864218b3f28d1d76'}, 'evidence/candidate/CORPUS_BINDINGS.json': {'bytes': 698, 'sha256': 'afb728c1b5acb8e022c63f182387355931d0834a01495e61cb59c4c26d9c8463'}, 'evidence/candidate/FROZEN_MANIFEST.json': {'bytes': 1523, 'sha256': 'ed9dc743686e9f58d67f4ec796ab217a3a94dec1635b05f9c4804e4b22bf4cf4'}, 'evidence/candidate/PART_A_INDEPENDENT_AUDIT.md': {'bytes': 15446, 'sha256': 'ab958fd7bc47b11a82155c01df10d348128c4b960f200d191aebb43145b806cc'}, 'evidence/candidate/PART_A_PROOF.md': {'bytes': 9755, 'sha256': '90be5ae3ab394227e9b22db5db3c49e1798714f70a7c554eed4fadb539ee820b'}, 'evidence/candidate/README.md': {'bytes': 1727, 'sha256': 'e4d947639a61820f29f44bd3c8efbcf9368af5a1e200754232a722e7e2747787'}, 'evidence/candidate/REPORT.md': {'bytes': 15589, 'sha256': 'db97c3883cf11867655b8709e03df25deabb026a0224e9cd551570059ee4463f'}, 'evidence/candidate/RESULT.json': {'bytes': 1403, 'sha256': '39d48551c0b3eb46bc0c90cdff6db68e7598b7e30ab2f1bb98093ab64ca7d36e'}, 'evidence/candidate/SOURCE_METADATA.json': {'bytes': 4314, 'sha256': 'ea5cc84ce0171d74e80d9c7bdd65e45037336d6e29f5e3653e51ec7ddfed7ed8'}, 'evidence/candidate/verify_exact.py': {'bytes': 7126, 'sha256': '027b55ed72d6d71df566d983427118e6f592898cdab804b0335c0deb798c85c5'}, 'evidence/prior_review/SECOND_INDEPENDENT_PART_A_AUDIT.md': {'bytes': 13605, 'sha256': '754bbad35d34ba48882fbc957498b3b9ae16b4eadf204838efac47717c1e1bf6'}, 'evidence/receipts/AUDIT_RECEIPT_O.json': {'bytes': 17910, 'sha256': '8323c0c95bd9eb0bab1e6d6dd595a47798196878507607bbc11d1f9eb893cf67'}, 'evidence/receipts/AUDIT_RECEIPT_OO.json': {'bytes': 17910, 'sha256': '4670cbc423e86aaf12ac50517b49b2cb7c656c52d308c0caf5b76e339d53ddb0'}, 'evidence/receipts/AUDIT_RECEIPT_normal.json': {'bytes': 17910, 'sha256': '8393cdbcde3baa07d17d3d1860f2e1dcdb96932385ff9fb2241b90b78b289a76'}, 'evidence/verify_envelope.py': {'bytes': 2006, 'sha256': 'e338dcd503d24938d93f93f005a547ff8e3c29eea5a6f5f9f1835165e745c0de'}, 'source_free_audit.tar.gz': {'bytes': 47510, 'sha256': 'feac3f5cda81ee3645eb8fab2f339efec643b356f641555134663f4901944fc0'}}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'evidence', 'evidence/candidate', 'evidence/prior_review', 'evidence/receipts'}


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
    exact_int(value['problem_id'], 2991)
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
    # The source-free tar is authenticated before opening and is never extracted.
    import io, tarfile, ast
    mapping={n[len('evidence/'):]:n for n in ACCEPTED if n.startswith('evidence/')}
    with tarfile.open(fileobj=io.BytesIO(snapshot['source_free_audit.tar.gz']),mode='r:gz') as archive:
        members=archive.getmembers();prefix='trisection2991_audit/'
        names=[m.name for m in members]
        dirs={'trisection2991_audit','trisection2991_audit/candidate','trisection2991_audit/prior_review','trisection2991_audit/receipts'}
        need(len(names)==len(set(names)) and set(names)==dirs|{prefix+n for n in mapping},'exact tar inventory')
        for member in members:
            if member.name in dirs:
                need(member.isdir() and member.mode==0o555,'tar directory type/mode')
            else:
                need(member.isreg() and member.mode==0o444,'tar regular member type/mode')
                name=mapping[member.name[len(prefix):]]
                need(member.size==len(snapshot[name]),'tar member size')
                need(archive.extractfile(member).read()==snapshot[name],'tar member bytes')
    envelope=parsed['evidence/PUBLICATION_ENVELOPE.json']
    need(envelope['target_id']==2991 and envelope['source_free'] is True,'audit envelope scope')
    rows=envelope['files'];seen=set();expected=set(mapping)-{'PUBLICATION_ENVELOPE.json'}
    need(type(rows) is list and len(rows)==len(expected),'audit envelope count')
    for row in rows:
        keys(row,['path','bytes','sha256','recorded_mode']);exact_int(row['bytes']);digest(row['sha256'])
        name=row['path'];need(type(name) is str and name in expected and name not in seen,'audit envelope path');seen.add(name)
        need(row['recorded_mode']=='0444','audit envelope mode')
        need(same(dict(bytes=row['bytes'],sha256=row['sha256']),ACCEPTED['evidence/'+name]),'audit envelope byte binding')
    need(seen==expected,'audit envelope complete')
    frozen=parsed['evidence/candidate/FROZEN_MANIFEST.json']
    exact_int(frozen['target_id'],2991);exact_int(frozen['format_version'],1)
    seen=set();expected={n[len('candidate/'):] for n in mapping if n.startswith('candidate/')}-{'FROZEN_MANIFEST.json'}
    for row in frozen['files']:
        keys(row,['name','bytes','sha256','mode']);exact_int(row['bytes']);digest(row['sha256'])
        name=row['name'];need(type(name) is str and name in expected and name not in seen,'freeze exact path');seen.add(name)
        need(row['mode']=='0444','freeze recorded mode')
        need(same(dict(bytes=row['bytes'],sha256=row['sha256']),ACCEPTED['evidence/candidate/'+name]),'freeze byte binding')
    need(seen==expected and len(expected)==8,'freeze inventory')
    result=parsed['evidence/candidate/RESULT.json'];exact_int(result['target_id'],2991);exact_int(result['approaches_used'],5)
    need(result['part_a']['non_isotopic_even_with_sector_permutations'] is True and result['part_a']['minimal_genus'] is True,'accepted part-a scope')
    need(result['part_b']['status']=='unresolved in this packet' and result['novelty']=='not established','unresolved part-b/no novelty')
    for name in ['evidence/candidate/verify_exact.py','evidence/audit_exact.py','evidence/verify_envelope.py']:
        need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(snapshot[name]))),'zero disabled asserts')
    inventory(root)
    return snapshot,parsed


def stable_receipt(value):
    """Only traceback byte counts depend on disposable absolute path lengths."""
    if type(value) is dict:
        return {k:stable_receipt(v) for k,v in value.items() if k!='stderr_bytes'}
    if type(value) is list:return [stable_receipt(v) for v in value]
    return value


def replay(snapshot, parsed):
    import shutil
    need(os.getuid()==os.geteuid()==1000,'actual UID/EUID1000 required')
    flags=[] if sys.flags.optimize==0 else ['-'+('O'*sys.flags.optimize)]
    mode=['normal','O','OO'][sys.flags.optimize]
    with tempfile.TemporaryDirectory(prefix='trisection-publication-') as directory:
        work=Path(directory);evidence=work/'evidence';cwd=work/'cwd';out=work/'output'
        evidence.mkdir();cwd.mkdir();out.mkdir()
        for folder in ['candidate','prior_review','receipts']:(evidence/folder).mkdir()
        for name,raw in snapshot.items():
            if name.startswith('evidence/'):
                target=work/name;target.write_bytes(raw);target.chmod(0o444)
        for folder in [evidence,*[p for p in evidence.rglob('*') if p.is_dir()],cwd]:folder.chmod(0o555)
        env=dict(PATH=os.defpath,HOME=str(work),TMPDIR=str(work),LC_ALL='C',PYTHONNOUSERSITE='1',PYTHONDONTWRITEBYTECODE='1',PYTHONSAFEPATH='1')
        def execute(script,args=()):
            return subprocess.run([sys.executable,'-I','-S','-B',*flags,str(script),*args],cwd=cwd,env=env,capture_output=True,timeout=300)
        try:
            probes=[]
            for path in [evidence/'NEW_FILE',evidence/'candidate/NEW_FILE',evidence/'candidate/PART_A_PROOF.md',evidence/'audit_exact.py',cwd/'NEW_FILE']:
                try:
                    with path.open('ab') as stream:stream.write(b'forbidden')
                except PermissionError:probes.append(path.relative_to(work).as_posix())
                else:raise ValueError('readonly write succeeded')
            proc=execute(evidence/'verify_envelope.py',[str(evidence),ACCEPTED['evidence/PUBLICATION_ENVELOPE.json']['sha256']])
            need(proc.returncode==0 and proc.stderr==b'','native envelope verification')
            value=parse(proc.stdout)
            need(same(value,dict(status='pass',files_bound=19,envelope_sha256=ACCEPTED['evidence/PUBLICATION_ENVELOPE.json']['sha256'],optimization=sys.flags.optimize,read_only=True)),'complete envelope stdout')
            proc=execute(evidence/'audit_exact.py',[str(evidence/'candidate'),str(out)])
            need(proc.returncode==0 and proc.stderr==b'','independent 72-run harness')
            summary=parse(proc.stdout)
            algebra=dict(general_odd_sector_unit_triples=121856,signed_sector_assignments=3072,symmetric_integer_matrices=15755,unimodular_matrices=1636)
            expected=dict(status='pass',uid=1000,euid=1000,audit_optimization=sys.flags.optimize,checker_runs=72,integrity_controls=16,independent_algebra=algebra,original_candidate_unchanged=True)
            need(same(summary,expected),'complete independent stdout')
            raw=(out/'AUDIT_RECEIPT.json').read_bytes();receipt=parse(raw)
            historical=parsed['evidence/receipts/AUDIT_RECEIPT_'+mode+'.json']
            need(same(stable_receipt(receipt),stable_receipt(historical)),'complete historical receipt mismatch excluding traceback byte counts')
            need(len(receipt['checker_runs'])==72 and len(receipt['integrity_controls'])==16,'exact native coverage')
            successes=failures=scope_passes=0;checker_outputs={}
            for record in receipt['checker_runs']:
                label=record['label'];stdout=(out/'runs'/label).with_suffix('.stdout').read_bytes();stderr=(out/'runs'/label).with_suffix('.stderr').read_bytes()
                exact_int(record['stdout_bytes'],len(stdout));exact_int(record['stderr_bytes'],len(stderr))
                if record['expected_success']:
                    need(record['exit_code']==0 and stderr==b'','successful checker streams')
                    successes+=1
                    if 'report_only_change_not_bound_by_original' in label:scope_passes+=1
                    if stdout:
                        got=parse(stdout)
                        need(got['uid']==1000 and got['optimization']==record['optimization'] and got['candidate_read_only'] is True,'actual native identity/mode')
                        need(got['proof_sha256']==ACCEPTED['evidence/candidate/PART_A_PROOF.md']['sha256'] and got['geometric_proof_certified_by_code'] is False,'native proof and scope')
                        checker_outputs[label]=got
                else:
                    need(record['exit_code']!=0 and stdout==b'' and len(stderr)>0,'required checker rejection')
                    failures+=1
            need((successes,failures,scope_passes)==(9,63,3),'native successes/rejections/scope probes')
            for record in receipt['integrity_controls']:need(record['rejected'] is True,'whole-candidate integrity rejection')
            for name,data in snapshot.items():
                if name.startswith('evidence/'):need((work/name).read_bytes()==data,'immutable evidence changed')
            need(not list(cwd.iterdir()),'readonly cwd changed')
            return dict(complete_native_receipt=receipt,native_summary=summary,native_checker_outputs=checker_outputs,
                        native_receipt_comparison='COMPLETE_TYPED_EQUAL_EXCEPT_PATH_DEPENDENT_TRACEBACK_BYTE_COUNTS',
                        native_harness_runs=72,native_expected_rejections=63,native_clean_passes=3,native_external_output_passes=3,
                        native_expected_unbound_report_passes=3,independent_integrity_controls_rejected=16,
                        native_report_change_pass_is_integrity_pass=False,readonly_write_probes_denied=probes,
                        readonly_file_mode='0444',readonly_directory_mode='0555',original_freeze_files=9,
                        archive_inventory='EXACT_20_FILES_AND_4_DIRECTORIES_MATCH',audit_envelope_files_bound=19,
                        fresh_source_bindings='NOT_RUN',fresh_corpus_bindings='NOT_RUN',
                        historical_source_bindings='EIGHT_LOCAL_PDF_REHASHES_AND_PUBLIC_SOURCE_REVIEW_PRESERVED',
                        imported_theorems='EXTERNAL_INPUTS_NOT_MACHINE_CERTIFIED',part_a='AFFIRMATIVELY_RESOLVED_BY_ACCEPTED_PROOF',
                        part_b='UNRESOLVED',novelty='NOT_ESTABLISHED',general_problem='UNSOLVED',mathematical_correction_required=False)
        finally:
            # Only disposable materializations are thawed for deletion.
            for path in work.rglob('*'):
                if not path.is_symlink():path.chmod(0o755 if path.is_dir() else 0o644)


def main():
    need(len(sys.argv)==4,'expected manifest pin, bootstrap pin, packet directory')
    manifest_pin,bootstrap_pin,path=sys.argv[1:];root=Path(os.path.abspath(path))
    snapshot,parsed=integrity(root,manifest_pin,bootstrap_pin);result=replay(snapshot,parsed)
    after,after_parsed=integrity(root,manifest_pin,bootstrap_pin)
    need(after==snapshot and same(after_parsed,parsed),'publication changed during replay')
    result.update(schema=1,problem_id=2991,status='PASS',publication_files=len(FILES),optimization=sys.flags.optimize,uid=os.getuid(),euid=os.geteuid(),queue_status='unsolved',substantive_turns='5/5',manifest_sha256=manifest_pin,bootstrap_sha256=bootstrap_pin)
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):
        print('REJECT: publication integrity/replay validation failed',file=sys.stderr);sys.exit(1)
