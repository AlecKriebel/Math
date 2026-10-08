#!/usr/bin/env python3
"""Authenticate exact Lefschetz-pencil partials before source-free arithmetic replay."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import hashlib,json,math,os,re,stat,subprocess,tempfile,io,tarfile,gzip
from pathlib import Path
ACCEPTED = {'author/FREEZE_MANIFEST.json': {'bytes': 1283, 'sha256': 'b744942d6086721c08ab2508a87b71e6c0d553486964b898e6cb9e1a81d10662'}, 'author/packet/APPROACHES.json': {'bytes': 1497, 'sha256': 'aafb8dee2550a5ba505c56285bd190d2f7112f80e448c77463154e326c1e5a44'}, 'author/packet/CHECK_RESULTS.json': {'bytes': 3090, 'sha256': 'a2e9069a2b8a8a60cec9517bcec9b22be3ac69bc1eb5aca2d67d105938f6b7f7'}, 'author/packet/README.md': {'bytes': 2141, 'sha256': '2fb06b62ef369a1bec1fe86d8e8df00a3774502af1bdd9ed4d50d14835f01032'}, 'author/packet/REPORT.md': {'bytes': 22522, 'sha256': 'dbf25962027b51dc3f843f0bfaa5ce1f04eef7b3cfaa9f0d24a57758d7d0c372'}, 'author/packet/SOURCES.json': {'bytes': 5229, 'sha256': 'f7961ac5e45575c1abb63f5f9962a560bd080c5545cf953b956cc29b05e5520e'}, 'author/packet/STATUS.json': {'bytes': 1828, 'sha256': 'e0efefcc4cd4cd8d1ddadf04d003fdacdfa6c67043fcc76e16ac68c1666503e7'}, 'author/packet/verify.py': {'bytes': 9256, 'sha256': '98f1dfef7940e1038259c51bd103e44bcc3c171e583db74e5c66650b32ce8e84'}, 'audit/AUDIT_MANIFEST.json': {'bytes': 1945, 'sha256': '7cd7261617dad43b672644e3386b7d2172b13a305d9ff1bd83a5629da0ae4864'}, 'audit/packet/AUDIT_REPORT.md': {'bytes': 15779, 'sha256': 'faccd4535e3d47d8a6807a8d49b912a5e624939ea9cac2b3d4ade0836657dbc2'}, 'audit/packet/AUTHOR_FREEZE_MANIFEST.json': {'bytes': 1283, 'sha256': 'b744942d6086721c08ab2508a87b71e6c0d553486964b898e6cb9e1a81d10662'}, 'audit/packet/INDEPENDENT_RESULTS.json': {'bytes': 2000, 'sha256': 'ab8d262772b6711125e14afc0268ec2c9ca7660f51bea6b8852aa00f5f46f64f'}, 'audit/packet/JOHNSON_QUOTIENT_ADDENDUM.md': {'bytes': 4659, 'sha256': '0cef7f3d32990436f5351e642bc00c6d611c8f022168ff6ca898ae686aeda4e0'}, 'audit/packet/README.md': {'bytes': 1651, 'sha256': 'aa39cfd174082cd27dfff1cc6bc5afbc1a5cde5e9b2ea84c08eeb63db7d5744f'}, 'audit/packet/REPLAY_RESULTS.json': {'bytes': 18712, 'sha256': '61fbd30054c5aa4122b96cd89f31a88350fb229629f4fbf1a57f77b9a1f43edf'}, 'audit/packet/SOURCE_INSPECTION.json': {'bytes': 5461, 'sha256': 'b2feb5c575b4a3b394a0da7044f7445740e468f0d465b89b71aae29ff0ff81a6'}, 'audit/packet/VERDICT.json': {'bytes': 1396, 'sha256': 'cebbcb950e3dd92bc295abc5cd5a59ed22e07aca42830d5c267f2c865f9c8cb4'}, 'audit/packet/independent_checks.py': {'bytes': 8777, 'sha256': '80715bd914cf6703254a4493bb88ca939040cccadd4bd388a104ad5ef8cedf59'}, 'audit/packet/replay_and_mutations.py': {'bytes': 9709, 'sha256': 'b382911eca0691c9a2b480b0098a1e894fc4ef89d958437d73855c05d11c9fa2'}}
SCOPE = {'schema': 1, 'problem_id': 2974, 'problem_code': 'KP-4.98', 'rank': 1051, 'status': 'unsolved', 'turns': 5, 'accepted': 'scoped_partials_with_proved_johnson_addendum', 'full_solution_claimed': False, 'novelty_claimed': False, 'peer_review_claimed': False, 'formal_certification_claimed': False, 'original_freeze_preserved': True, 'audit_freeze_preserved': True, 'correction_patch_required': False, 'HH18_main_theorem_refuted': False, 'HH18_classification_consequences': 'CONDITIONAL', 'HH18_valid_restricted_exclusion': 'degree-one elliptic factor', 'johnson_quotient_limit': 'nonzero initial image exhausts the full irreducible closed target', 'intrinsic_index_hypotheses': 'initial image saturated and positive rank increase', 'odd_prime_factor_two_control': 'FALSE_PASS_DISCLOSED', 'independent_even_modulus_and_integer_controls': 'DETECT_FACTOR_TWO_LOSS', 'fresh_source_checks': 'NOT_RUN', 'fresh_corpus_checks': 'NOT_RUN', 'source_bodies_included': False, 'datasets_included': False, 'private_material_included': False}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'ACCEPTANCE.json', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'author', 'author/packet', 'audit', 'audit/packet'}
AUTHOR_PIN='b744942d6086721c08ab2508a87b71e6c0d553486964b898e6cb9e1a81d10662'
AUDIT_PIN='7cd7261617dad43b672644e3386b7d2172b13a305d9ff1bd83a5629da0ae4864'
AUTHOR_ARCHIVE_PIN='beabecc7f40e4a064740fc457c5a2f1c735695c63a255021d8f35decae74d342'

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
    exact_int(value['problem_id'], 2974)
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
    need(same(value,SCOPE), 'exact acceptance scope and types')


def integrity(root, manifest_pin, bootstrap_pin):
    digest(manifest_pin); digest(bootstrap_pin)
    inventory(root)
    snapshot={name:ordinary(root/name) for name in FILES}
    need(sha(snapshot['PUBLICATION_MANIFEST.json'])==manifest_pin,'external manifest pin')
    need(sha(snapshot['BOOTSTRAP.py'])==bootstrap_pin,'external bootstrap pin')
    parsed={name:parse(raw) for name,raw in snapshot.items() if name.endswith('.json')}
    manifest(parsed['PUBLICATION_MANIFEST.json'],snapshot,PAYLOAD)
    for name,row in ACCEPTED.items():
        need(same(row,dict(bytes=len(snapshot[name]),sha256=sha(snapshot[name]))),'accepted freeze changed')
    for prefix,mname,pin,schema in [('author/','FREEZE_MANIFEST.json',AUTHOR_PIN,'lefschetz-pencils-2974-freeze-v1'),('audit/','AUDIT_MANIFEST.json',AUDIT_PIN,'lefschetz-2974-independent-audit-freeze-v1')]:
        value=parsed[prefix+mname]
        need(sha(snapshot[prefix+mname])==pin,'original manifest pin')
        need(value['schema']==schema and value['status']=='unsolved_here' and value['source_free'] is True,'original manifest scope')
        exact_int(value['problem_id'],2974);exact_int(value['approaches_completed'],5)
        files=value['packet_files'];need(type(files) is dict,'original files type')
        names={name[len(prefix+'packet/'):] for name in ACCEPTED if name.startswith(prefix+'packet/')}
        need(set(files)==names,'original inventory')
        for name,row in files.items():
            keys(row,['bytes','sha256']);exact_int(row['bytes']);digest(row['sha256'])
            need(same(row,ACCEPTED[prefix+'packet/'+name]),'original file binding')
    need(snapshot['author/FREEZE_MANIFEST.json']==snapshot['audit/packet/AUTHOR_FREEZE_MANIFEST.json'],'audit author manifest copy')
    acceptance(parsed['ACCEPTANCE.json'])
    status=parsed['author/packet/STATUS.json'];verdict=parsed['audit/packet/VERDICT.json']
    need(status['full_solution_claimed'] is False and verdict['HH18_main_theorem_refuted'] is False,'unsolved/classification scope')
    need(verdict['mandatory_author_packet_corrections']==[] and verdict['author_freeze_preserved'] is True,'no patch disposition')
    inventory(root)
    return snapshot,parsed


def author_archive(snapshot):
    raw=io.BytesIO()
    with tarfile.open(fileobj=raw,mode='w',format=tarfile.PAX_FORMAT) as archive:
        for name in sorted(n for n in ACCEPTED if n.startswith('author/packet/')):
            data=snapshot[name];info=tarfile.TarInfo(name[len('author/'):])
            info.size=len(data);info.mode=0o444;info.uid=info.gid=0;info.uname=info.gname='';info.mtime=0
            archive.addfile(info,io.BytesIO(data))
    result=gzip.compress(raw.getvalue(),mtime=0)
    need(len(result)==16496 and sha(result)==AUTHOR_ARCHIVE_PIN,'exact deterministic author archive reconstruction')
    return result


def replay(snapshot,parsed):
    need(os.getuid()==os.geteuid()==1000,'real UID/EUID 1000 required')
    with tempfile.TemporaryDirectory(prefix='lefschetz-publication-') as temporary:
        work=Path(temporary)
        for name in sorted(DIRS|{'cwd'},key=lambda n:n.count('/')):(work/name).mkdir()
        for name in ACCEPTED:(work/name).write_bytes(snapshot[name])
        (work/'author/source_free_packet.tar.gz').write_bytes(author_archive(snapshot))
        for path in sorted(work.rglob('*'),key=lambda p:len(p.parts),reverse=True):path.chmod(0o555 if path.is_dir() else 0o444)
        denied=[]
        try:
            for name in ['author/NEW_FILE','author/packet/REPORT.md','audit/packet/NEW_FILE','audit/packet/AUDIT_REPORT.md','cwd/NEW_FILE']:
                try:
                    with (work/name).open('ab') as stream:stream.write(b'forbidden')
                except PermissionError:denied.append(name)
                else:raise ValueError('read-only write succeeded')
            env=dict(PATH=os.defpath,HOME=str(work),TMPDIR=str(work),LC_ALL='C',PYTHONNOUSERSITE='1',PYTHONDONTWRITEBYTECODE='1',PYTHONSAFEPATH='1')
            flags=[] if sys.flags.optimize==0 else ['-'+('O'*sys.flags.optimize)]
            def run(script,args):
                result=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(work/script),*args],cwd=work/'cwd',env=env,capture_output=True,timeout=600)
                need(result.returncode==0 and result.stderr==b'','accepted checker replay rejected')
                return dict(stdout=result.stdout.decode(),stderr=result.stderr.decode(),exit_code=result.returncode),parse(result.stdout)
            author_out,author=run('author/packet/verify.py',['--manifest',str(work/'author/FREEZE_MANIFEST.json'),'--manifest-sha256',AUTHOR_PIN])
            check=dict(author);integrity_receipt=check.pop('integrity')
            need(same(check,parsed['author/packet/CHECK_RESULTS.json']),'exact author results')
            need(same(integrity_receipt,dict(manifest_sha256=AUTHOR_PIN,files=7,verified=True)),'author integrity result')
            independent_out,independent=run('audit/packet/independent_checks.py',[])
            need(same(independent,parsed['audit/packet/INDEPENDENT_RESULTS.json']),'exact independent results')
            # The unchanged native mutation driver preserves source mode bits on
            # its disposable copies and then edits them. Give it a separate,
            # byte-identical writable mutation seed; keep all authenticated input
            # and positive replay copies sealed. The native driver independently
            # extracts and seals its positive author replay and its working dir.
            seed=work/'native-mutation-seed';(seed/'packet').mkdir(parents=True)
            for name in ACCEPTED:
                if name.startswith('author/'):
                    (seed/name[len('author/'):]).write_bytes(snapshot[name])
            (seed/'source_free_packet.tar.gz').write_bytes(author_archive(snapshot))
            native_out,native=run('audit/packet/replay_and_mutations.py',['--author-root',str(seed)])
            for name in ACCEPTED:
                if name.startswith('author/'):
                    need((seed/name[len('author/'):]).read_bytes()==snapshot[name],'native mutation seed changed')
            need(same(native,parsed['audit/packet/REPLAY_RESULTS.json']),'exact native controls receipt')
            need(not list((work/'cwd').iterdir()),'child wrote into readonly cwd')
            for name in ACCEPTED:need((work/name).read_bytes()==snapshot[name],'replay mutated evidence')
            return dict(author_full_output=author_out,independent_full_output=independent_out,native_controls_full_output=native_out,
                        independent_semidirect_cases=992,independent_index_cases=180,independent_base_change_cases=900,
                        native_integrity_cli_rejections=39,native_arithmetic_rejections=21,native_odd_prime_factor_two_false_passes=3,
                        native_receipt_exact_type_match=True,native_mutation_seed='DISPOSABLE_WRITABLE_BYTE_IDENTICAL',author_archive_reconstructed_sha256=AUTHOR_ARCHIVE_PIN,
                        readonly_write_probes_denied=denied,fresh_source_bindings='NOT_RUN',fresh_corpus_bindings='NOT_RUN',
                        imported_theorems='NOT_MACHINE_CERTIFIED',geometric_realization='UNRESOLVED',general_problem='UNSOLVED')
        finally:
            for path in sorted(work.rglob('*'),key=lambda p:len(p.parts)):
                if path.is_dir():path.chmod(0o755)


def main():
    need(len(sys.argv)==4,'expected manifest pin, bootstrap pin, packet directory')
    manifest_pin,bootstrap_pin,path=sys.argv[1:];root=Path(os.path.abspath(path))
    snapshot,parsed=integrity(root,manifest_pin,bootstrap_pin)
    result=replay(snapshot,parsed)
    after,after_parsed=integrity(root,manifest_pin,bootstrap_pin)
    need(after==snapshot and same(after_parsed,parsed),'publication changed during replay')
    result.update(schema=1,problem_id=2974,status='PASS',publication_files=len(FILES),optimization=sys.flags.optimize,
                  uid=os.getuid(),euid=os.geteuid(),queue_status='unsolved',substantive_turns='5/5',manifest_sha256=manifest_pin,bootstrap_sha256=bootstrap_pin)
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):
        print('REJECT: publication integrity/replay validation failed',file=sys.stderr);sys.exit(1)
