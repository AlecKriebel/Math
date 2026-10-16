#!/usr/bin/env python3
"""Authenticate the accepted distinct-area partial results; replay source-free finite checks."""
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

ACCEPTED = {'ACCEPTANCE.md': {'bytes': 3245, 'sha256': '5f901a872208284059c4b4864f57ee5dfdf646ee53205a8cee7f6f0a10969b64'}, 'PUBLIC_SCOPE.json': {'bytes': 1608, 'sha256': 'bf99aae4935f69a3694b1642c3195020ba2c28ca235df98135aae8cb2449fa6d'}, 'README.md': {'bytes': 5453, 'sha256': '9b05ce20f3d86799c7d8578152bffd744a2429858078bf04b7dcf8544e513e7c'}, 'REPLAY_RESULTS.json': {'bytes': 76561, 'sha256': '099841fd865536250477ed28bcd617dd123589f11e41a9d50c57f9b5e9976c7b'}, 'audit/ACCEPTANCE.json': {'bytes': 1904, 'sha256': '74d37693cf8e1c7fb171c2060547d0fa5eaefe60b6eea5e6eb7b2657f9d5004b'}, 'audit/AUDIT_MANIFEST.json': {'bytes': 4043, 'sha256': '95d3a9ef897f17b9cb752aedbcdbc01742f40e52e00ed1321f9e6edc4977ab4e'}, 'audit/authored/AUDIT.md': {'bytes': 15941, 'sha256': '3d809a9d24c2e59641b8b9d4ea1e1432e98bac9648e9a534716359a29ec374ca'}, 'audit/authored/independent_check.py': {'bytes': 11154, 'sha256': '4879901553c99e73388f18ec7ed445964c61234aca2bf543e6b8cdf38dc744e9'}, 'audit/authored/rerun_audit.py': {'bytes': 5031, 'sha256': 'c0f1611af67d2dec123b63461e079dc513664789c1517637f4013cf3d37a9ebf'}, 'audit/authored/semantic_controls.py': {'bytes': 2848, 'sha256': '22f52e0132cf96b076b81a8489d96fb9e837b188588e0fb42043dd66280ca58d'}, 'audit/verification/EXECUTION_RECEIPT.json': {'bytes': 6998, 'sha256': 'ba3a9be5f171d1a4e36a2e41f7ca7e47afa764325b788131693935c8cb504cf2'}, 'audit/verification/SOURCE_METADATA_CHECK.json': {'bytes': 1333, 'sha256': 'fd773b9093141616f97b3c61ba00a9a187474e37bbdcdc07e58c089449bc0b45'}, 'audit/verification/SUBJECT_MANIFEST.json': {'bytes': 1115, 'sha256': '2be9f1d7b582291f223c96981f74963baf61ea16897ab3ae031b0ee44fdad3e3'}, 'audit/verification/independent_O.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'audit/verification/independent_O.stdout.json': {'bytes': 11064, 'sha256': '187a54babe78a540dc32bfade7b708be4c521f4d4613550f7772b481340604bb'}, 'audit/verification/independent_OO.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'audit/verification/independent_OO.stdout.json': {'bytes': 11064, 'sha256': '69bc888592708263534ab264b1f924fd49ebf682f54caf5fe716b5ca908c5bf4'}, 'audit/verification/independent_normal.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'audit/verification/independent_normal.stdout.json': {'bytes': 11064, 'sha256': 'bd1327f8ba8e529728e5c413982d8ce856d33b56b9b3da4d33aee36d617290f1'}, 'audit/verification/native_O.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'audit/verification/native_O.stdout.json': {'bytes': 1819, 'sha256': 'a5b55e6b84b84c41f9e1912cc730e576b51073a4f41e923110058b06c21f040c'}, 'audit/verification/native_OO.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'audit/verification/native_OO.stdout.json': {'bytes': 1819, 'sha256': 'a4d1c1367aed7cb9b82a33800f32ae0b7e47e0e06061b0dee2418852c918efec'}, 'audit/verification/native_normal.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'audit/verification/native_normal.stdout.json': {'bytes': 1819, 'sha256': '423f4d2c63ad9c1f1221ad718f3542c0741ea958db25f10abd743ab9fa03e81b'}, 'audit/verification/semantic_O.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'audit/verification/semantic_O.stdout.json': {'bytes': 1204, 'sha256': '57a5c70c4c33ed98804cca3caa30e7a6cdabf50837f32200d0a3d2509c272b30'}, 'audit/verification/semantic_OO.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'audit/verification/semantic_OO.stdout.json': {'bytes': 1204, 'sha256': '017884ad08fd1947d905139db09d94af63879d3a1eafb64ad15b6a2fcc7d113c'}, 'audit/verification/semantic_normal.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'audit/verification/semantic_normal.stdout.json': {'bytes': 1204, 'sha256': '6a38494a498955d9cb3b1969a82dd0b22e870583d9034b799409e2f5427e9f95'}, 'author/PAYLOAD_PINS.json': {'bytes': 1075, 'sha256': 'f8a0ca3f560e2cf4908d4655655a55503d2965c4502c8cee80a2e16a429a3839'}, 'author/README.md': {'bytes': 1336, 'sha256': '0b2b8397229b5026c65755f2a58b3806984e8a672555cdca30a398e1e5352cf6'}, 'author/REPORT.md': {'bytes': 15426, 'sha256': '65c34cdf480507a3ac514364df7091eccc2e47c579f9cb9ddcbc537d3eb1f3ed'}, 'author/SOURCE_AUDIT.md': {'bytes': 3757, 'sha256': 'b7b4c1ef2be3e89cf5a1fa84a302e124a8985e98ee012625f5f573d3c3f3084c'}, 'author/SOURCE_MANIFEST.json': {'bytes': 3449, 'sha256': '690d492299e8d81301d605fe1807446e34b83c2c299cd27cb2348c428c52c698'}, 'author/STATUS.json': {'bytes': 767, 'sha256': 'b032df10a68a024bcf85651dc321f34ee077d2243b8087ee46ca2fa1e87ff210'}, 'author/VERIFICATION.md': {'bytes': 3076, 'sha256': '68f0e994a6d6d08cda16722c54a0bcd0d4566c897e39f19c7d706b2296213654'}, 'author/check_claims.py': {'bytes': 13842, 'sha256': '3ae252893b21521ac9dae7d8974e6048e018c968aae73ed5636953c7b591d22e'}, 'mutation_tests.py': {'bytes': 13145, 'sha256': '060332f27503e3208680dd5c5c1b88466efdf6675d4a5c746f9176288e63614a'}}
PAYLOAD = set(ACCEPTED) | {'README.md','ACCEPTANCE.md','verify_publication.py','mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json','BOOTSTRAP.py'}
DIRS = {'author','audit','audit/authored','audit/verification'}

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
    exact_int(value['problem_id'], 3900016)
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
    pins=parsed['author/PAYLOAD_PINS.json']
    keys(pins,['schema','files']);exact_int(pins['schema'],1)
    rows=pins['files']; expected={n[7:] for n in ACCEPTED if n.startswith('author/') and n!='author/PAYLOAD_PINS.json'}
    need(type(rows) is list and len(rows)==len(expected),'author inventory list')
    seen=set()
    for row in rows:
        keys(row,['path','bytes','sha256']);n=row['path']
        need(type(n) is str and n in expected and n not in seen,'author manifest path')
        seen.add(n);exact_int(row['bytes']);digest(row['sha256'])
        need(same(row,dict(path=n,bytes=len(snapshot['author/'+n]),sha256=sha(snapshot['author/'+n]))),'author bytes')
    need(seen==expected,'author exact inventory')
    audit=parsed['audit/AUDIT_MANIFEST.json'];keys(audit,['schema','files']);exact_int(audit['schema'],1)
    rows=audit['files'];expected={n[6:] for n in ACCEPTED if n.startswith('audit/') and n!='audit/AUDIT_MANIFEST.json'}
    need(type(rows) is dict and set(rows)==expected,'audit exact inventory')
    for n,row in rows.items():
        keys(row,['bytes','sha256']);exact_int(row['bytes']);digest(row['sha256'])
        need(same(row,dict(bytes=len(snapshot['audit/'+n]),sha256=sha(snapshot['audit/'+n]))),'audit bytes')
    import ast
    for name in [n for n in FILES if n.endswith('.py')]:
        need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(snapshot[name]))),'no optimized-away assertions')
    status=parsed['author/STATUS.json'];decision=parsed['audit/ACCEPTANCE.json']
    need(same(status['problem_id'],3900016) and same(status['substantive_proof_search_approaches'],5),'5/5 author status')
    need(status['outcome']=='exhausted' and status['full_target_resolved'] is False and status['novelty_claimed'] is False,'author scope')
    need(decision['verdict']=='accepted_partial_results' and decision['independent_audit_status']=='accepted' and decision['correction_patch_required'] is False,'accepted partial scope')
    need(same(decision['problem_id'],3900016) and same(decision['substantive_research_approaches'],5),'accepted identity')
    need(decision['terminal_research_status']=='exhausted' and decision['full_target_resolved'] is False and decision['novelty_or_best_known_claim_accepted'] is False,'accepted limitations')
    sl=parsed['PUBLIC_SCOPE.json']
    for name in ['fresh_source_retrieval','fresh_source_inspection','fresh_pdf_byte_bindings','fresh_dataset_byte_bindings','full_baseline_patch_replay','archive_reconstruction']:
        need(sl[name]=='NOT_RUN','honest source-free scope')
    return snapshot

def replay(snapshot):
    """Replay complete finite outputs. No source retrieval or corpus reads occur."""
    import shutil
    need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000 required')
    modes=[('normal',[]),('O',['-O']),('OO',['-OO'])]
    with tempfile.TemporaryDirectory(prefix='distinct-areas-public-replay-') as td:
        root=Path(td);ro=root/'author';audit=root/'audit';cwd=root/'cwd'
        ro.mkdir();audit.mkdir();cwd.mkdir()
        for prefix,dest in [('author/',ro),('audit/',audit)]:
            for name,body in snapshot.items():
                if name.startswith(prefix):
                    path=dest/name[len(prefix):];path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(body)
        def freeze(d):
            for f in d.rglob('*'):f.chmod(0o555 if f.is_dir() else 0o444)
            d.chmod(0o555)
        def thaw(d):
            d.chmod(0o755)
            for f in d.rglob('*'):f.chmod(0o755 if f.is_dir() else 0o644)
        freeze(ro);freeze(audit);freeze(cwd)
        initial={str(f.relative_to(root)):sha(f.read_bytes()) for d in [ro,audit] for f in d.rglob('*') if f.is_file()}
        env=dict(PATH=os.defpath,HOME=str(root),TMPDIR=str(root),LC_ALL='C',PYTHONDONTWRITEBYTECODE='1')
        def execute(args,flags,where=cwd):
            q=subprocess.run([sys.executable,'-I','-S','-B',*flags,*map(str,args)],cwd=where,env=env,capture_output=True,timeout=120)
            return dict(exit_code=q.returncode,stdout=q.stdout.decode(),stderr=q.stderr.decode(),stdout_bytes=len(q.stdout),stdout_sha256=sha(q.stdout),stderr_bytes=len(q.stderr),stderr_sha256=sha(q.stderr))
        try:
            runs=[]
            for i,(mode,flags) in enumerate(modes):
                tasks=[('native',ro/'check_claims.py',['--require-readonly']),('independent',audit/'authored/independent_check.py',[]),('semantic',audit/'authored/semantic_controls.py',[ro/'check_claims.py'])]
                for kind,script,args in tasks:
                    r=execute([script,*args],flags)
                    prefix='audit/verification/'+kind+'_'+mode
                    expected=snapshot[prefix+'.stdout.json'];err=snapshot[prefix+'.stderr.txt']
                    need(r['exit_code']==0 and r['stdout'].encode()==expected and r['stderr'].encode()==err,'full '+kind+' output bytes '+mode)
                    value=parse(r['stdout']);need(same(value,parse(expected)),'full typed output '+kind+' '+mode)
                    need(same(value['uid'],1000),'exact UID')
                    if kind=='native':need(same(value['python_optimization'],i),'native optimization')
                    else:need(same(value['euid'],1000) and same(value['optimization'],i),'audit runtime')
                    r.update(kind=kind,mode=mode);runs.append(r)
            # Probe every replicated evidence file and every directory, not only
            # the native checker's eight files. Every attempt is nontruncating.
            probe_code="""import errno,json,os,pathlib,sys
root=pathlib.Path(sys.argv[1]); entries=[]
if os.getuid()!=1000 or os.geteuid()!=1000:raise RuntimeError('UID 1000 required')
paths=[]
for name in ['author','audit','cwd']:
 d=root/name;paths.append(d);paths.extend(sorted(d.rglob('*')))
for p in paths:
 name=p.relative_to(root).as_posix();isdir=p.is_dir()
 expected=0o555 if isdir else 0o444
 if (p.stat().st_mode&0o777)!=expected or os.access(p,os.W_OK):raise RuntimeError('mode/write access')
 try:
  fd=os.open(p/'UNEXPECTED_CREATE' if isdir else p,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if isdir else 0),0o600)
 except PermissionError as e:
  if e.errno not in (errno.EACCES,errno.EPERM,errno.EROFS):raise
  entries.append({'path':name,'operation':'create' if isdir else 'write_open','errno':e.errno,'denied':True})
 else:
  os.close(fd);raise RuntimeError('write succeeded')
print(json.dumps({'uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,'entries':entries},sort_keys=True))
"""
            probes=[];branches=[];expected_entries=[]
            for name in ['author','audit','cwd']:
                d=root/name
                for f in [d,*sorted(d.rglob('*'))]:expected_entries.append(dict(path=f.relative_to(root).as_posix(),operation='create' if f.is_dir() else 'write_open',errno=13,denied=True))
            writable=root/'writable';shutil.copytree(ro,writable);thaw(writable)
            for i,(mode,flags) in enumerate(modes):
                r=execute(['-c',probe_code,root],flags)
                need(r['exit_code']==0 and r['stderr']=='','physical probes executed')
                need(same(parse(r['stdout']),dict(uid=1000,euid=1000,optimization=i,entries=expected_entries)),'full physical probes')
                r.update(mode=mode);probes.append(r)
                ext=root/('external_'+mode+'.json')
                r=execute([ro/'check_claims.py','--require-readonly','--output',ext],flags)
                expected=snapshot['audit/verification/native_'+mode+'.stdout.json']
                need(r['exit_code']==0 and r['stdout']==r['stderr']=='' and ext.read_bytes()==expected,'full external output bytes')
                r.update(mode=mode,branch='external_output',file_content=ext.read_text());branches.append(r)
                r=execute([ro/'check_claims.py','--require-readonly','--output',ro/'FORBIDDEN.json'],flags)
                need(r['exit_code']==1 and r['stdout']=='' and r['stderr']=='RuntimeError: output must be external to the packet\n' and not (ro/'FORBIDDEN.json').exists(),'inside output rejected')
                r.update(mode=mode,branch='inside_output');branches.append(r)
                r=execute([writable/'check_claims.py','--require-readonly'],flags)
                need(r['exit_code']==1 and r['stdout']=='' and r['stderr']=='RuntimeError: packet directory is writable\n','writable tree rejected')
                r.update(mode=mode,branch='writable_tree');branches.append(r)
            final={str(f.relative_to(root)):sha(f.read_bytes()) for d in [ro,audit] for f in d.rglob('*') if f.is_file()}
            need(initial==final and not list(cwd.iterdir()),'all source-free inputs unchanged')
            return dict(status='PASS',problem_id=3900016,disposition='exhausted',turns='5/5',full_target_resolved=False,novelty_claimed=False,best_known_claimed=False,native_runs=runs,physical_write_probes=probes,cli_branches=branches,semantic_mutations_rejected_per_mode=7,independent_negative_controls_per_mode=8,native_guard_negative_controls_per_mode=7,top_level_subprocess_executions=21,readonly_inputs_unchanged=True,fresh_source_retrieval='NOT_RUN',fresh_source_inspection='NOT_RUN',fresh_pdf_byte_bindings='NOT_RUN',fresh_dataset_byte_bindings='NOT_RUN',full_baseline_patch_replay='NOT_RUN',archive_reconstruction='NOT_RUN',normalization='NONE; every fresh native stdout/stderr byte is compared to the pinned complete mode-specific output; outer JSON is compared with exact recursive types.',scope='Source-free executable replay only. Historical source and corpus checks remain retained metadata, not fresh reruns. Finite checks support proofs and do not settle unresolved extremal functions or certify novelty.')
        finally:
            for d in [ro,audit,cwd]:thaw(d)


def main():
    need(len(sys.argv)==4,'supply external manifest pin, external bootstrap pin, and root')
    mp,bp,location=sys.argv[1:];root=Path(os.path.abspath(location));before=integrity(root,mp,bp)
    result=replay(before)
    need(same(result,parse(before['REPLAY_RESULTS.json'])),'fresh complete replay equals pinned record')
    need(integrity(root,mp,bp)==before,'entire release unchanged after replay')
    print(json.dumps(dict(status='PASS',optimization=sys.flags.optimize,problem_id=3900016,disposition='exhausted',turns='5/5',manifest_sha256=mp,bootstrap_sha256=bp,exact_files=len(FILES),fresh_pdf_byte_bindings='NOT_RUN',replay=result),indent=2,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,UnicodeError,subprocess.TimeoutExpired):
        print('REJECT: publication integrity or replay failed',file=sys.stderr);sys.exit(1)
