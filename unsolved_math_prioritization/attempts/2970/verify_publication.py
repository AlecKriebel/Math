#!/usr/bin/env python3
"""Authenticate frozen Horikawa equivalence partial results; replay source-free finite checks."""
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

ACCEPTED = {'original/CHECKS.md': {'bytes': 2281, 'sha256': '5663d5bb8696ca2ee548d486e14aaadbf8980171324c4e757992f5fa17e960d7'}, 'original/MANIFEST.sha256': {'bytes': 645, 'sha256': 'a8cd4866d04bba62d53083e3e3f353e90974d955f09218f59244687f6d9152e4'}, 'original/README.md': {'bytes': 1207, 'sha256': '8f154d357d83c1a06c1a5b488c6a6f549ba68eb3fff589c3563b09223b5e2269'}, 'original/REPORT.md': {'bytes': 22709, 'sha256': 'd225a30ed01a47a2476430d70cdcdf753f0aa33dfdd098cdd8595e0d22221a8c'}, 'original/SOURCE_AUDIT.md': {'bytes': 5289, 'sha256': '03454a7b8d263fdc82692389730a520a52f534b2e4a915a580a880d709cf0ea6'}, 'original/attempts.json': {'bytes': 1692, 'sha256': '52a275d9f2cd17f16cc106e11f502e0a72807565f8907b0f0658a5ec51020fa1'}, 'original/source_manifest.json': {'bytes': 2730, 'sha256': 'dccea850218d54b439863b6728f7b7676ca84c57abd7b8acdd385d4e014e5be9'}, 'original/verification_results.json': {'bytes': 23969, 'sha256': 'b85cb80dfd9a9b7b25b3257e04ca162c75964cd35d640adf174c899ab0a60b2a'}, 'original/verify.py': {'bytes': 7321, 'sha256': 'bef6898cc003dbebf4567bcac7c6ccdf54aa240645ee19f53ee4242fbd989cac'}, 'audit/AUDIT.md': {'bytes': 17148, 'sha256': '7f3f902478c3ed01528ed133a6f9c88042415960017ae8cd85597fd0ad98f9a4'}, 'audit/MANIFEST.sha256': {'bytes': 766, 'sha256': 'a1e8bdf42fbe2fcb4042b10fce98626c70b0a8c0a12cca84fa9a3ea02adbe668'}, 'audit/OPTIONAL_ORBIT_GUARD.patch': {'bytes': 609, 'sha256': '29ca3a2569bf129c9c7632b38b8691cd3ed4c251de073bc9bf5b620e3ffe9f8e'}, 'audit/README.md': {'bytes': 1950, 'sha256': '39ab6538b3ca178f63d1e3a6e9e8d61a43bc7eebbeb2c614e7414a32d339fab5'}, 'audit/audit_results.json': {'bytes': 19024, 'sha256': '3e10bb02c1b37cc87dc259f5729095cf3fa70a22dcc36b7fd3269de934dcc387'}, 'audit/independent_results.json': {'bytes': 1343, 'sha256': 'cc399e3de012e1aec6596b43ae1464d949c163bb69a57b3e9e97a4a1b8546896'}, 'audit/independent_verify.py': {'bytes': 10995, 'sha256': 'f028093e4f70551a174789efcffdcd18ceedb73bc0114c7686957b3d494c0667'}, 'audit/optional_patch_results.json': {'bytes': 1682, 'sha256': 'd5e64c8141c19c708da24ccd791654806252249e9c92be2394322d77ea735497'}, 'audit/run_audit.py': {'bytes': 8016, 'sha256': 'd2aa6eb1f186e21dbb2c2b0f3dbe6547a717465d64dae2c33214d5aaf662339b'}, 'audit/source_checks.json': {'bytes': 3693, 'sha256': 'ade9560f1efc73dddfea2735ce1475acc2fc83fd1b160f6643ada30cb8391a55'}, 'corrected_v1/ADOPTION.json': {'bytes': 571, 'sha256': 'b7d54e8203c32f2884d538bfe54548d38308922e93f8773cd72ad6417a38e4aa'}, 'corrected_v1/MANIFEST.sha256': {'bytes': 248, 'sha256': 'b3eb3a856ec24e52b48e212a444ce4f7cee0ad6efd1feca231cf90ab2e46256f'}, 'corrected_v1/verification_results.json': {'bytes': 23969, 'sha256': 'b85cb80dfd9a9b7b25b3257e04ca162c75964cd35d640adf174c899ab0a60b2a'}, 'corrected_v1/verify.py': {'bytes': 7456, 'sha256': '3d14f6b0281baab6c4e354ef892b4642c2905d19ea3e4c1a99289864e057e9c3'}, 'REPLAY_RESULTS.json': {'bytes': 318570, 'sha256': '3fdc7ff06e114ae8bb2163874b3274d1bffd50c8cecfa0000c51c3dd24363632'}}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'original', 'audit', 'corrected_v1'}
CASES = [('original', 'collapse_first_generator', 'A = (1, 1, 0, 1)', 'A = (1, 0, 0, 1)', 'RuntimeError'), ('original', 'remove_partial_conjugator', 'P = (0, 1, 2, 0)', 'P = (1, 0, 0, 1)', 'RuntimeError'), ('original', 'wrong_saturation_pairing', 'saturated=((-r,1),(1,0))', 'saturated=((-r,2),(2,0))', 'RuntimeError'), ('original', 'wrong_canonical_coefficient', 'ky=(2,3*r-2)', 'ky=(2,3*r-1)', 'RuntimeError'), ('original', 'wrong_signature', 'sig=-24*r', 'sig=-24*r+1', 'RuntimeError'), ('original', 'wrong_pencil_nodes', 'nodes=e+d*(3*k*k+2*k)', 'nodes=e+d*(3*k*k+3*k)', 'RuntimeError'), ('original', 'wrong_hurwitz_inverse', 'qconj(qinv(b),a)', 'qconj(b,a)', 'RuntimeError'), ('original', 'wrong_formal_canonical_vector', 'kval=[3]*(4*r-1)', 'kval=[2]*(4*r-1)', 'RuntimeError'), ('original', 'truncate_orbit_to_seed', 'return seen\n\n\ndef check_finite_example', 'return {t}\n\n\ndef check_finite_example', 'saved_output_mismatch'), ('independent', 'wrong_orbit_cardinality', '== [216, 144]', '== [216, 143]', 'RuntimeError'), ('independent', 'wrong_saturation_pairing', 'saturation = ((-r, 1), (1, 0))', 'saturation = ((-r, 2), (2, 0))', 'RuntimeError'), ('independent', 'wrong_pencil_nodes', 'euler+base-4+4*genus', 'euler+base-4+5*genus', 'RuntimeError'), ('independent', 'wrong_hurwitz_inverse', 'conjugate(inverse(y), x)', 'conjugate(y, x)', 'RuntimeError'), ('independent', 'wrong_canonical_coefficient', 'ky = (2, 3*r-2)', 'ky = (2, 3*r-1)', 'RuntimeError'), ('independent', 'collapse_partial_conjugation', 'tp = (conjugate(p, a), conjugate(p, b), inverse(b), inverse(a))', 'tp = t', 'RuntimeError'), ('corrected', 'collapse_first_generator', 'A = (1, 1, 0, 1)', 'A = (1, 0, 0, 1)', 'RuntimeError'), ('corrected', 'remove_partial_conjugator', 'P = (0, 1, 2, 0)', 'P = (1, 0, 0, 1)', 'RuntimeError'), ('corrected', 'wrong_saturation_pairing', 'saturated=((-r,1),(1,0))', 'saturated=((-r,2),(2,0))', 'RuntimeError'), ('corrected', 'wrong_canonical_coefficient', 'ky=(2,3*r-2)', 'ky=(2,3*r-1)', 'RuntimeError'), ('corrected', 'wrong_signature', 'sig=-24*r', 'sig=-24*r+1', 'RuntimeError'), ('corrected', 'wrong_pencil_nodes', 'nodes=e+d*(3*k*k+2*k)', 'nodes=e+d*(3*k*k+3*k)', 'RuntimeError'), ('corrected', 'wrong_hurwitz_inverse', 'qconj(qinv(b),a)', 'qconj(b,a)', 'RuntimeError'), ('corrected', 'wrong_formal_canonical_vector', 'kval=[3]*(4*r-1)', 'kval=[2]*(4*r-1)', 'RuntimeError'), ('corrected', 'truncate_orbit_to_seed', 'return seen\n\n\ndef check_finite_example', 'return {t}\n\n\ndef check_finite_example', 'RuntimeError')]

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
    exact_int(value['problem_id'], 2970)
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
    import ast, difflib
    for prefix, count, total in [('original',9,67843),('audit',10,65226),('corrected_v1',4,None)]:
        names={n[len(prefix)+1:] for n in ACCEPTED if n.startswith(prefix+'/')}
        need(len(names)==count,'frozen slice count')
        if total is not None:need(sum(len(snapshot[prefix+'/'+n]) for n in names)==total,'frozen slice bytes')
        seen=set()
        for line in snapshot[prefix+'/MANIFEST.sha256'].decode().splitlines():
            need(re.fullmatch('[0-9a-f]{64}  [A-Za-z0-9_.-]+',line) is not None,'digest manifest syntax')
            h,n=line.split('  ');need(n in names-{'MANIFEST.sha256'} and n not in seen,'manifest unknown or duplicate');seen.add(n)
            need(sha(snapshot[prefix+'/'+n])==h,'frozen digest manifest member')
        need(seen==names-{'MANIFEST.sha256'},'digest manifest exact inventory')
    original=snapshot['original/verify.py'].decode();corrected=snapshot['corrected_v1/verify.py'].decode()
    old='    orbit_tp = hurwitz_orbit(tp,qgroup)\n'
    addition="    require((len(orbit_t), len(orbit_tp)) == (216, 144),\n            'check failed: complete orbit cardinalities must be 216 and 144')\n"
    need(original.count(old)==1 and corrected==original.replace(old,old+addition),'exact two-line adoption')
    actual=''.join(difflib.unified_diff(original.splitlines(True),corrected.splitlines(True),fromfile='a/verify.py',tofile='b/verify.py'))
    need(actual.encode()==snapshot['audit/OPTIONAL_ORBIT_GUARD.patch'],'actual supplied patch bytes')
    need(snapshot['original/verification_results.json']==snapshot['corrected_v1/verification_results.json'],'unchanged saved mathematical output')
    for name in ['original/verify.py','corrected_v1/verify.py','audit/independent_verify.py']:
        need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(snapshot[name]))),'no optimized-away mathematical assertions')
    return snapshot


def replay(snapshot):
    """Fresh exact tests with complete stdout/stderr, from genuine non-root read-only files."""
    need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000 required')
    modes=[('normal',[]),('O',['-O']),('OO',['-OO'])]
    sources={'original':snapshot['original/verify.py'],'corrected':snapshot['corrected_v1/verify.py'],'independent':snapshot['audit/independent_verify.py']}
    expected={'original':snapshot['original/verification_results.json'],'corrected':snapshot['corrected_v1/verification_results.json'],'independent':snapshot['audit/independent_results.json']}
    with tempfile.TemporaryDirectory(prefix='horikawa-sourcefree-replay-') as td:
        root=Path(td);ro=root/'readonly';ro.mkdir()
        for name,body in sources.items():(ro/(name+'.py')).write_bytes(body)
        for program,name,old,new,want in CASES:
            body=sources[program].decode();need(body.count(old)==1,'one mutation target '+name)
            (ro/(program+'_'+name+'.py')).write_text(body.replace(old,new))
        before={f.name:sha(f.read_bytes()) for f in ro.iterdir()}
        for f in ro.iterdir():f.chmod(0o444)
        ro.chmod(0o555)
        probe_code="""import json,os
r={'uid':os.getuid(),'euid':os.geteuid(),'directory_mode':oct(os.stat('.').st_mode&0o777),'directory_writable':os.access('.',os.W_OK)}
try:
 open('MUST_NOT_EXIST','x').close();r['creation_denied']=False
except PermissionError:r['creation_denied']=True
print(json.dumps(r,sort_keys=True))
"""
        def execute(name,flags):
            run=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(ro/name)],cwd=ro,capture_output=True,timeout=60)
            # Keep every output byte; normalize only the disposable directory spelling in traceback text.
            out=run.stdout.decode();err=run.stderr.decode().replace(str(ro),'<readonly>')
            return dict(exit_code=run.returncode,stdout=out,stderr=err,stdout_bytes=len(run.stdout),stdout_sha256=sha(run.stdout))
        try:
            pr=subprocess.run([sys.executable,'-I','-S','-B','-c',probe_code],cwd=ro,capture_output=True,timeout=10)
            need(pr.returncode==0 and not pr.stderr,'permission probe execution')
            probe=parse(pr.stdout)
            need(same(probe,dict(uid=1000,euid=1000,directory_mode='0o555',directory_writable=False,creation_denied=True)),'actual non-root write rejection')
            runs=[]
            for program in sources:
                for mode,flags in modes:
                    r=execute(program+'.py',flags);r.update(program=program,mode=mode)
                    need(r['exit_code']==0 and r['stderr']=='' and r['stdout'].encode()==expected[program],'byte-exact baseline '+program+' '+mode)
                    runs.append(r)
            independent=parse(expected['independent'])
            need(same(independent['finite_group']['orbit_sizes'],[216,144]),'exhaustive independent orbits')
            need(independent['finite_group']['order_three_generating_identity_tuple_universe_with_two_factors_per_class']==360,'exhaustive generating universe')
            mutations=[]
            for program,name,old,new,want in CASES:
                outcomes=[]
                for mode,flags in modes:
                    r=execute(program+'_'+name+'.py',flags);r.update(mode=mode)
                    if want=='RuntimeError':
                        need(r['exit_code']!=0 and 'RuntimeError:' in r['stderr'],'active mathematical rejection '+program+' '+name+' '+mode)
                        if name=='truncate_orbit_to_seed':need('complete orbit cardinalities must be 216 and 144' in r['stderr'],'corrected guard rejection')
                    else:
                        need(r['exit_code']==0 and r['stderr']=='' and parse(r['stdout'])['status']=='passed','original false-PASS reproduced')
                        need(r['stdout'].encode()!=expected[program],'strict saved-output comparator rejects original false-PASS')
                    outcomes.append(r)
                mutations.append(dict(program=program,mutation=name,expected_rejection=want,runs=outcomes))
            need({f.name:sha(f.read_bytes()) for f in ro.iterdir()}==before,'read-only execution input unchanged')
            return dict(status='PASS',problem_id=2970,mathematical_status='unsolved',turns='5/5',readonly_probe=probe,baseline_runs=runs,mutation_cases=mutations,mutation_count=len(CASES),mutation_executions=3*len(CASES),all_readonly_input_unchanged=True,independent_exhaustive_result=independent,fresh_source_retrieval='NOT_RUN',fresh_source_inspection='NOT_RUN',fresh_pdf_byte_bindings='NOT_RUN',limits=['Marked lattice and fiber obstructions do not classify unmarked manifolds.','The Lagrangian-span hypothesis is conditional.','The finite PSL(2,F3) example is not an actual Horikawa monodromy quotient.','The r=4 counterexample is outside the odd-r target.','The AEHK normal r=3 bridge does not settle smooth or symplectic equivalence.'])
        finally:
            ro.chmod(0o755)
            for f in ro.iterdir():f.chmod(0o644)


def main():
    need(len(sys.argv)==4,'supply external manifest pin, external bootstrap pin, and root')
    mp,bp,location=sys.argv[1:];root=Path(os.path.abspath(location));before=integrity(root,mp,bp)
    result=replay(before)
    need(same(result,parse(before['REPLAY_RESULTS.json'])),'fresh complete replay equals pinned acceptance record')
    need(integrity(root,mp,bp)==before,'entire release unchanged after replay')
    print(json.dumps(dict(status='PASS',optimization=sys.flags.optimize,problem_id=2970,mathematical_status='unsolved',turns='5/5',manifest_sha256=mp,bootstrap_sha256=bp,exact_files=len(FILES),fresh_source_retrieval='NOT_RUN',fresh_source_inspection='NOT_RUN',fresh_pdf_byte_bindings='NOT_RUN',replay=result),indent=2,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,UnicodeError,subprocess.TimeoutExpired):
        print('REJECT: publication integrity or replay failed',file=sys.stderr);sys.exit(1)
