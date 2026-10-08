#!/usr/bin/env python3
"""Authenticate exact support-genus partials before source-free arithmetic replay."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import hashlib,json,math,os,re,stat,subprocess,tempfile
from pathlib import Path
ACCEPTED = {'original/CHECK_RESULTS.json': {'bytes': 1569, 'sha256': 'ad25d01c247fe0628ab0e24674a3e2532fd9f657fc2275ab39e4e3d46cb0b229'}, 'original/FROZEN_MANIFEST.json': {'bytes': 1349, 'sha256': '9e290bec9d6ba40ec3a61a1c41b9e70381f75c3ab80db6e2a4ef55f83d3aa751'}, 'original/README.md': {'bytes': 1784, 'sha256': 'ecb0c7c94979d4bb818e81533256f02a97d6682e71a2b0f11dc9ae2d969bc7a2'}, 'original/REPORT.md': {'bytes': 22641, 'sha256': '0b92d877093fca11901fe51a14de95f7ae647c4c3a49dbef67158308e5e88fe9'}, 'original/RESULT.json': {'bytes': 978, 'sha256': '3baf0d1ca95e5e0707e72ee55679e12831d017345d8d7b430a8a4f1d1caa572b'}, 'original/SOURCE_METADATA.json': {'bytes': 7489, 'sha256': 'e44ecf51b73a01b13884e1694995b265a59d439ade837aadfdf424316a73efe8'}, 'original/TURN_LEDGER.md': {'bytes': 2297, 'sha256': 'b4e8d5f048a519938118a8ec682ad2261aef4d109c196708b7be50cb6e55bea8'}, 'original/check_math.py': {'bytes': 4429, 'sha256': '80243d3d3e0911302b8c2bb4d22b5fff02502284543ef7f701014ac9b6cacb98'}, 'original/verify_packet.py': {'bytes': 1167, 'sha256': 'f66e87d57ec88d836b4fe5e0e70dc017ce4f986713272370ba4a5f170f826144'}, 'audit/candidate_public/CHECK_RESULTS.json': {'bytes': 1569, 'sha256': 'ad25d01c247fe0628ab0e24674a3e2532fd9f657fc2275ab39e4e3d46cb0b229'}, 'audit/candidate_public/FROZEN_MANIFEST.json': {'bytes': 1467, 'sha256': 'daaf2d88de9272733ea1d674396ec2236cfe250d4796dc922e841890ff087b69'}, 'audit/candidate_public/README.md': {'bytes': 1784, 'sha256': 'ecb0c7c94979d4bb818e81533256f02a97d6682e71a2b0f11dc9ae2d969bc7a2'}, 'audit/candidate_public/REPORT.md': {'bytes': 22641, 'sha256': '0b92d877093fca11901fe51a14de95f7ae647c4c3a49dbef67158308e5e88fe9'}, 'audit/candidate_public/RESULT.json': {'bytes': 978, 'sha256': '3baf0d1ca95e5e0707e72ee55679e12831d017345d8d7b430a8a4f1d1caa572b'}, 'audit/candidate_public/SOURCE_METADATA.json': {'bytes': 7489, 'sha256': 'e44ecf51b73a01b13884e1694995b265a59d439ade837aadfdf424316a73efe8'}, 'audit/candidate_public/TURN_LEDGER.md': {'bytes': 2297, 'sha256': 'b4e8d5f048a519938118a8ec682ad2261aef4d109c196708b7be50cb6e55bea8'}, 'audit/candidate_public/check_math.py': {'bytes': 5811, 'sha256': 'ebe79a3d497554d183a9cfce45fd5a780bdd66d42a2186a1c38cc373b73423eb'}, 'audit/candidate_public/verify_packet.py': {'bytes': 1498, 'sha256': '9aade65cc379e9ed0b40635628dea16738d35441b57c8fa42c32a8ac5ee06e88'}, 'audit/public/AUDIT.md': {'bytes': 22831, 'sha256': 'ef4853df77213fd222ac1452d34858d0b3a010407a53f073e453769adff420b2'}, 'audit/public/AUDIT_PINS.json': {'bytes': 3645, 'sha256': 'e63e6135620d9bac3fa22abcfe0af22b61c5dfd4167513472711e5aab43c116f'}, 'audit/public/AUDIT_RESULT.json': {'bytes': 1426, 'sha256': '9ba67ad5fb514ba70df66e40a9ffe979fbf149585e8572a40787233f4ee35969'}, 'audit/public/CORRECTION_NOTE.md': {'bytes': 2082, 'sha256': '2012f7dd6905e9732798bc1642fe807b4fe480c424f5ae35e71f992fcc32ccc3'}, 'audit/public/EXECUTION_AUDIT.json': {'bytes': 158801, 'sha256': '59b41fad44ed6551386335b276aeba0c1b30e7c6218e650a6b2e28d2c2731aa6'}, 'audit/public/INDEPENDENT_EXECUTION.json': {'bytes': 1244, 'sha256': '00d472b38713468215465381255b6ee0cc38d6940b0cdabf5f03b520ab8c903b'}, 'audit/public/INDEPENDENT_MATH_RESULTS.json': {'bytes': 1587, 'sha256': 'fbe3bd0ab81c6a5f4f4c29cac4bfcc5a53203ed76fbdaa59be0c9f82290549e5'}, 'audit/public/OPTIMIZATION_FIX.patch': {'bytes': 7791, 'sha256': 'cd6ab8820430914185d670e82dd69a199b455302e2b60b685b4d2d31daed488a'}, 'audit/public/PATCH_VERIFICATION.json': {'bytes': 386, 'sha256': '9d516bdcf7a05ca2ea4394c864d4317daa63eb5446c92671b9410e1771ec421a'}, 'audit/public/SOURCE_AUDIT.json': {'bytes': 4895, 'sha256': '1b2dcc87522f5dd4075330bcdf1205bb4716db5a8960b77b360bc7000da7ee03'}, 'audit/public/independent_math_checks.py': {'bytes': 5852, 'sha256': 'c05a20c7e76458737db30ae3dc3045acee9fc9d1144f70112faf65458bd8564d'}, 'audit/public/reproduce_audit.py': {'bytes': 8664, 'sha256': '22a73fc5028b178a951e46205358b6e635a570ede018a65e660c51f0d5fea37c'}}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'ACCEPTANCE.json', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'original', 'audit', 'audit/public', 'audit/candidate_public'}
ORIGINAL_PIN = '9e290bec9d6ba40ec3a61a1c41b9e70381f75c3ab80db6e2a4ef55f83d3aa751'
CANDIDATE_PIN = 'daaf2d88de9272733ea1d674396ec2236cfe250d4796dc922e841890ff087b69'
AUDIT_PIN = 'e63e6135620d9bac3fa22abcfe0af22b61c5dfd4167513472711e5aab43c116f'

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
    exact_int(value['problem_id'], 2843)
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


def acceptance(value):
    keys(value, ['schema','problem_id','problem_code','rank','status','turns','parts','full_solution_claimed','novelty_claimed','source_bodies_included','fresh_source_checks','original_optimized_false_passes','native_type_equivalence_preserved','native_strict_json_claimed','correction_scope'])
    exact_int(value['schema'],1); exact_int(value['problem_id'],2843); exact_int(value['rank'],1045); exact_int(value['turns'],5)
    need(same(value['parts'], {'a':'unresolved','b':'unresolved'}), 'problem parts')
    for name in ['full_solution_claimed','novelty_claimed','source_bodies_included','native_strict_json_claimed']:
        need(value[name] is False, 'scope boolean')
    need(value['native_type_equivalence_preserved'] is True, 'native type limitation')
    exact_int(value['original_optimized_false_passes'],44)
    need(same(value['problem_code'],'KP-3.45') and same(value['status'],'unsolved') and same(value['fresh_source_checks'],'NOT_RUN'), 'scope strings')
    need(same(value['correction_scope'],'23 arithmetic and 6 packet assertions replaced by explicit require checks; report unchanged'), 'correction scope')


def rows_bound(rows, names, snapshot, prefix=''):
    need(type(rows) is list and len(rows)==len(names),'frozen member count')
    seen=set()
    for row in rows:
        keys(row,['path','bytes','sha256']);name=row['path']
        need(type(name) is str and name in names and name not in seen,'frozen member name')
        seen.add(name);exact_int(row['bytes']);digest(row['sha256'])
        raw=snapshot[prefix+name]
        need(same(row,dict(path=name,bytes=len(raw),sha256=sha(raw))),'frozen member binding')
    need(seen==names,'frozen inventory')


def integrity(root, manifest_pin, bootstrap_pin):
    digest(manifest_pin);digest(bootstrap_pin);inventory(root)
    snapshot={name:ordinary(root/name) for name in FILES}
    need(sha(snapshot['PUBLICATION_MANIFEST.json'])==manifest_pin,'external manifest pin')
    need(sha(snapshot['BOOTSTRAP.py'])==bootstrap_pin,'external bootstrap pin')
    parsed={name:parse(raw) for name,raw in snapshot.items() if name.endswith('.json')}
    manifest(parsed['PUBLICATION_MANIFEST.json'],snapshot,PAYLOAD)
    acceptance(parsed['ACCEPTANCE.json'])
    for name,row in ACCEPTED.items():
        need(same(row,dict(bytes=len(snapshot[name]),sha256=sha(snapshot[name]))),'accepted evidence changed')
    for prefix,pin,status in [('original/',ORIGINAL_PIN,'author_frozen_partial_report'),('audit/candidate_public/',CANDIDATE_PIN,'separately_pinned_optimization_safe_correction')]:
        name=prefix+'FROZEN_MANIFEST.json';need(sha(snapshot[name])==pin,'independent original/candidate pin')
        value=parsed[name];fields=['format','problem_id','freeze_date_utc','status','source_free','files']
        if prefix.startswith('audit'):fields+=['supersedes_manifest_sha256']
        keys(value,fields);exact_int(value['format'],1);exact_int(value['problem_id'],2843)
        need(value['source_free'] is True and same(value['status'],status) and same(value['freeze_date_utc'],'2026-10-08'),'native manifest scope')
        if prefix.startswith('audit'):need(same(value['supersedes_manifest_sha256'],ORIGINAL_PIN),'superseded pin')
        names={n[len(prefix):] for n in ACCEPTED if n.startswith(prefix)}-{'FROZEN_MANIFEST.json'}
        rows_bound(value['files'],names,snapshot,prefix)
    need(sha(snapshot['audit/public/AUDIT_PINS.json'])==AUDIT_PIN,'independent audit pin')
    value=parsed['audit/public/AUDIT_PINS.json']
    keys(value,['format','problem_id','purpose','original_manifest_sha256','corrected_manifest_sha256','files'])
    exact_int(value['format'],1);exact_int(value['problem_id'],2843)
    need(same(value['original_manifest_sha256'],ORIGINAL_PIN) and same(value['corrected_manifest_sha256'],CANDIDATE_PIN),'audit original/candidate anchors')
    names={n[len('audit/'):] for n in ACCEPTED if n.startswith('audit/')}-{'public/AUDIT_PINS.json'}
    rows_bound(value['files'],names,snapshot,'audit/')
    for name in ['CHECK_RESULTS.json','README.md','REPORT.md','RESULT.json','SOURCE_METADATA.json','TURN_LEDGER.md']:
        need(snapshot['original/'+name]==snapshot['audit/candidate_public/'+name],'non-code original content altered')
    need(parsed['original/RESULT.json']['full_solution_claimed'] is False,'unresolved author scope')
    inventory(root)
    return snapshot,parsed


def replay(snapshot,parsed):
    need(os.getuid()==os.geteuid()==1000,'actual UID/EUID 1000 required')
    with tempfile.TemporaryDirectory(prefix='support-genus-publication-') as temporary:
        work=Path(temporary)
        for name in sorted(DIRS,key=lambda x:x.count('/')):(work/name).mkdir()
        (work/'cwd').mkdir()
        for name in ACCEPTED:(work/name).write_bytes(snapshot[name])
        readonly=[work/name for name in DIRS]+[work/'cwd']
        for name in ACCEPTED:(work/name).chmod(0o444)
        for path in readonly:path.chmod(0o555)
        denied=[]
        try:
            for name in ['original/NEW_FILE','original/REPORT.md','audit/candidate_public/NEW_FILE','audit/candidate_public/REPORT.md','audit/public/NEW_FILE','audit/public/AUDIT.md','cwd/NEW_FILE']:
                try:
                    with (work/name).open('ab') as stream:stream.write(b'forbidden')
                except PermissionError:denied.append(name)
                else:raise ValueError('read-only write succeeded')
            env=dict(PATH=os.defpath,HOME=str(work),TMPDIR=str(work),LC_ALL='C',PYTHONDONTWRITEBYTECODE='1')
            flags=[] if sys.flags.optimize==0 else ['-'+('O'*sys.flags.optimize)]
            def run(script,args):
                p=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(work/script),*args],cwd=work/'cwd',env=env,capture_output=True,timeout=600)
                need(p.returncode==0 and p.stderr==b'','accepted script failed: '+script)
                return p.stdout,parse(p.stdout)
            for prefix in ['original/','audit/candidate_public/']:
                raw,result=run(prefix+'check_math.py',[])
                need(same(result,parsed[prefix+'CHECK_RESULTS.json']),'saved arithmetic exact-type mismatch')
                _,result=run(prefix+'verify_packet.py',[])
                need(same(result,dict(status='PASS',verified_files=8,math_results_reproduced=True,problem_status='unresolved')),'native baseline mismatch')
            raw,independent=run('audit/public/independent_math_checks.py',[])
            need(same(independent,parsed['audit/public/INDEPENDENT_MATH_RESULTS.json']),'independent arithmetic mismatch')
            # Native audit mutates its own copytree controls before making them read-only.
            # Stage disposable writable sources because copytree preserves source modes.
            # Accepted evidence and every executed native control remain read-only.
            stage=work/'native_sources';stage.mkdir()
            for label,prefix in [('original','original/'),('candidate','audit/candidate_public/')]:
                (stage/label).mkdir()
                for name in ACCEPTED:
                    if name.startswith(prefix):(stage/label/name[len(prefix):]).write_bytes(snapshot[name])
            output=work/'fresh_native_audit.json'
            _,summary=run('audit/public/reproduce_audit.py',[str(stage/'original'),str(stage/'candidate'),str(output)])
            for label,prefix in [('original','original/'),('candidate','audit/candidate_public/')]:
                for name in ACCEPTED:
                    if name.startswith(prefix):need((stage/label/name[len(prefix):]).read_bytes()==snapshot[name],'native staged source changed')
            fresh=parse(output.read_bytes());historical=parsed['audit/public/EXECUTION_AUDIT.json']
            exact_int(fresh['total_runs'],150);need(fresh['input_packets_unchanged'] is True and fresh['strict_json_schema_claimed'] is False,'native scope')
            # Temporary path-bearing stderr hashes vary. Retain the complete frozen receipt;
            # compare actual outcomes, runtime identity, result types, modes and read-only probes.
            def normalized(receipt):
                result=[]
                for row in receipt['rows']:
                    item={k:v for k,v in row.items() if k not in ['stdout_sha256','stderr_sha256','last_error_line']}
                    error=row['last_error_line']
                    item['error_class']=error.split(':',1)[0] if error is not None else None
                    result.append(item)
                return result
            need(same(normalized(fresh),normalized(historical)),'native control outcome changed')
            rows=fresh['rows']
            false_passes=sum(row['packet']=='original' and row['test'] not in ['baseline','saved_integer_true_rehashed'] and row['returncode']==0 for row in rows)
            type_acceptances={name:sum(row['packet']==name and row['test']=='saved_integer_true_rehashed' and row['returncode']==0 for row in rows) for name in ['original','corrected']}
            corrected_rejects=sum(row['packet']=='corrected' and row['test'] not in ['baseline','saved_integer_true_rehashed'] and row['returncode']!=0 and not row['pass_claimed'] for row in rows)
            exact_int(false_passes,44);exact_int(corrected_rejects,60);need(same(type_acceptances,dict(original=5,corrected=5)),'native type-equivalence disclosure changed')
            need(not list((work/'cwd').iterdir()),'child wrote to readonly cwd')
            for name in ACCEPTED:need((work/name).read_bytes()==snapshot[name],'replay changed evidence')
            return dict(native_control_runs=150,original_optimized_false_passes=44,corrected_negative_rejections=60,native_true_to_one_acceptances=type_acceptances,native_strict_json_schema=False,independent_counts=independent['counts'],readonly_write_probes_denied=denied,python_version=sys.version.split()[0],fresh_source_bindings='NOT_RUN',imported_theorem_proofs='NOT_MACHINE_CERTIFIED',july_2026_max_theorem_status='IMPORTED_PREPRINT',general_problem='UNSOLVED')
        finally:
            for path in readonly:path.chmod(0o755)
            for name in ACCEPTED:(work/name).chmod(0o644)


def main():
    need(len(sys.argv)==4,'expected manifest pin, bootstrap pin, packet directory')
    manifest_pin,bootstrap_pin,path=sys.argv[1:];root=Path(os.path.abspath(path))
    snapshot,parsed=integrity(root,manifest_pin,bootstrap_pin)
    result=replay(snapshot,parsed)
    after,after_parsed=integrity(root,manifest_pin,bootstrap_pin)
    need(after==snapshot and same(after_parsed,parsed),'publication changed during replay')
    result.update(schema=1,problem_id=2843,status='PASS',publication_files=len(FILES),optimization=sys.flags.optimize,uid=os.getuid(),euid=os.geteuid(),queue_status='unsolved',substantive_turns='5/5',manifest_sha256=manifest_pin,bootstrap_sha256=bootstrap_pin)
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):
        print('REJECT: publication integrity/replay validation failed',file=sys.stderr)
        sys.exit(1)
