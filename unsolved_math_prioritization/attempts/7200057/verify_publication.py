#!/usr/bin/env python3
"""Authenticate the accepted crossing/halving corrected partial results; replay source-free finite checks."""
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

ACCEPTED = {'ACCEPTANCE.md': {'bytes': 4219, 'sha256': 'dd87ce463fb5609832e0554f3c609a9016c964c7648a7f035c6436b83d7e1716'}, 'PUBLIC_SCOPE.json': {'bytes': 1515, 'sha256': '0efee2a8818fdbc779ac57c0648f82d9236108a8b601708f8deddfaa260d57f6'}, 'QUEUE_BINDING.json': {'bytes': 703, 'sha256': '0fc15eb87fd1cb35307660364c2a3ef1aa0cfe85013412c49f2e575eefaca504'}, 'README.md': {'bytes': 2748, 'sha256': 'f93281b9360ca66bc30ad6c501cd8e1accff083fd079ff5abedeadc802826f65'}, 'REPLAY_RESULTS.json': {'bytes': 225082, 'sha256': '52e799578a5120957ba58b4a3250c946405e62029cdeeb7d1c52e09ede05e1c0'}, 'audit/AUDIT.md': {'bytes': 14823, 'sha256': '7c2971a1da5dd4e00f93532abe4b6daa8b7b83085455c928f2c2bb0d0dced37f'}, 'audit/AUDIT_PINS.json': {'bytes': 1087, 'sha256': 'ec818f59fa750d004bd48dbdd395915c374ca2d84b1dae2539ee541f2e1b7fbd'}, 'audit/CORRECTION.patch': {'bytes': 6076, 'sha256': 'ab892a6aa46e76dadfd725a27cf3038cf93d767059ac81bbda8ceb871bec187a'}, 'audit/ORIGINAL_PINS.json': {'bytes': 1324, 'sha256': 'b2512434df364e4f9691bb103e9c404d4e524c70faf84e90457bda05df0cf4fe'}, 'audit/README.md': {'bytes': 1563, 'sha256': '59d8d5525aad9fe92698f433d33e1e68a2dcb133a16c41f810f744cccbb4c757'}, 'audit/SOURCE_VERIFICATION.json': {'bytes': 2506, 'sha256': '5621bd624f1039210d31d383495bf414f060be0a643ffe0cf2c4814181f91ee2'}, 'audit/STATUS.json': {'bytes': 777, 'sha256': '1fff43dbe485e26a44dba764d8bb82b8bb639df0b16e5814f6af2a1416bfdc0d'}, 'audit/check_independent.py': {'bytes': 15402, 'sha256': 'dbd61303d398d2a2b00cdd49dd407dfcf53336e7e30eb6308107c2537bbc62ed'}, 'current/PAYLOAD_PINS.json': {'bytes': 1076, 'sha256': '254eac2502cbae5152cd2799cb62b1f8e3c3aa20732cfa2668e6a4f68f5c4ec6'}, 'current/README.md': {'bytes': 1305, 'sha256': 'c87be16836e98d10977213b72385a1ca92b2faca196127753c332f0eda282ccc'}, 'current/REPORT.md': {'bytes': 19519, 'sha256': 'd7b562ed6f5019e7f4a391adc19db0136bcb94659348eb5e43722ba4d0f550e0'}, 'current/SOURCE_AUDIT.md': {'bytes': 2318, 'sha256': 'b4ae15eda0f94440ab4e0eca2ee587f416be7c2440556aaaa80127fb9d3a38de'}, 'current/SOURCE_MANIFEST.json': {'bytes': 3845, 'sha256': '9996f66c0d4ed7efe0dd7dcf5039e907c655061aa340e4d6884b23bdb21d2647'}, 'current/STATUS.json': {'bytes': 1107, 'sha256': '0a2eccd250236747bd4d45a47206cc9e10310b099197b57e5f19e79ae0e5c9f6'}, 'current/VERIFICATION.md': {'bytes': 2598, 'sha256': '44bb0590b0668f251eba3278d770c75c9dda069f7b14f89e3bbe5d8b3b527069'}, 'current/check_claims.py': {'bytes': 12779, 'sha256': 'a3a27ec26a66dfb787370ba2a5cb8a31e722eec5d049d162de9225e5418b861c'}, 'mutation_tests.py': {'bytes': 16148, 'sha256': '8a70b913c4889ed5735fb9f839bc7db3b6a39062591fb99db0c845f6a8682035'}, 'verification/audit_O.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'verification/audit_O.stdout.txt': {'bytes': 22510, 'sha256': '5f4d4c6c0f87e9096ef684d46fb4228ea9d98212fea1f344862593c61ed59688'}, 'verification/audit_OO.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'verification/audit_OO.stdout.txt': {'bytes': 22510, 'sha256': '0b096a63faea3899cbd0ebbdeedb9933ba6630a02cbd6d762c7d594c3cb47c71'}, 'verification/audit_normal.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'verification/audit_normal.stdout.txt': {'bytes': 22510, 'sha256': 'b98cd140abdaaa934aac572a0c6ef52254be5f9f2c1a448c0d1842a09a47f58c'}, 'verification/current_O.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'verification/current_O.stdout.txt': {'bytes': 6277, 'sha256': 'f8a82f3d3e3cc004b1c8f7895261d98012da98da8ceda57e703e1271e45817fb'}, 'verification/current_OO.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'verification/current_OO.stdout.txt': {'bytes': 6277, 'sha256': '250282e93c50c81d9b178ac1667220075d5b989ec5e608be0e3150c8b4a736a6'}, 'verification/current_normal.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'verification/current_normal.stdout.txt': {'bytes': 6277, 'sha256': '8b622e511bd3393fbdaa8125308f4f43af208ad0fbfc2f6424e488a5a8594bbb'}}
PAYLOAD = set(ACCEPTED) | {'verify_publication.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json','BOOTSTRAP.py'}
DIRS = {'current','audit','verification'}

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
    exact_int(value['problem_id'], 7200057)
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
    for prefix,filename in [('current','PAYLOAD_PINS.json'),('audit','AUDIT_PINS.json')]:
        pins=parsed[prefix+'/'+filename];keys(pins,['schema','files']);exact_int(pins['schema'],1)
        rows=pins['files'];expected={n[len(prefix)+1:] for n in ACCEPTED if n.startswith(prefix+'/') and n!=prefix+'/'+filename}
        need(type(rows) is list and len(rows)==len(expected),'inner inventory list')
        seen=set()
        for row in rows:
            keys(row,['path','bytes','sha256']);n=row['path']
            need(type(n) is str and n in expected and n not in seen,'inner manifest path')
            seen.add(n);exact_int(row['bytes']);digest(row['sha256'])
            raw=snapshot[prefix+'/'+n]
            need(same(row,dict(path=n,bytes=len(raw),sha256=sha(raw))),'inner byte binding')
        need(seen==expected,'inner exact inventory')
    original=parsed['audit/ORIGINAL_PINS.json'];keys(original,['schema','subject','files']);exact_int(original['schema'],1)
    need(original['subject']=='Omitted superseded authored original; metadata only; full original replay NOT_RUN','omitted original scope')
    expected={n.split('/')[1] for n in ACCEPTED if n.startswith('current/')}
    need(type(original['files']) is list and len(original['files'])==len(expected),'original metadata list')
    seen=set()
    for row in original['files']:
        keys(row,['path','bytes','sha256']);need(type(row['path']) is str and row['path'] in expected and row['path'] not in seen,'original metadata path')
        seen.add(row['path']);exact_int(row['bytes']);digest(row['sha256'])
    need(seen==expected,'original metadata inventory')
    import ast
    for name in [n for n in FILES if n.endswith('.py')]:
        need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(snapshot[name]))),'no optimized-away assertions')
    status=parsed['current/STATUS.json'];decision=parsed['audit/STATUS.json']
    need(same(status['problem_id'],7200057) and same(status['substantive_proof_search_approaches'],5),'5/5 current status')
    need(status['outcome']=='exhausted' and status['full_target_resolved'] is False and status['novelty_claimed'] is False,'current scope')
    need(decision['current_verdict']=='accepted_partial_results_after_correction' and decision['original_verdict']=='requires_explicit_rounding_correction','accepted correction')
    need(same(decision['problem_id'],7200057) and same(decision['substantive_proof_search_approaches'],5),'accepted identity')
    need(decision['outcome']=='exhausted' and decision['full_target_resolved'] is False and decision['novelty_claimed'] is False,'accepted limitations')
    need(snapshot['audit/CORRECTION.patch'].startswith(b'CONTEXTUAL CORRECTION HISTORY: NOT THE ACCEPTED CURRENT REPORT.\nRemoved hunks are rejected or superseded statements and are not endorsed.\n'),'patch own preamble')
    queue=parsed['QUEUE_BINDING.json'];keys(queue,['schema','problem_id','base_commit','path','base','current','changed_cells','unrelated_bytes_preserved','existing_links_preserved','literal_initial_sha_line_preserved'])
    exact_int(queue['schema'],1);exact_int(queue['problem_id'],7200057)
    for name in ['base','current']:
        row=queue[name];keys(row,['bytes','sha256','git_blob']);exact_int(row['bytes']);digest(row['sha256'])
        need(type(row['git_blob']) is str and re.fullmatch('[0-9a-f]{40}',row['git_blob']) is not None,'queue git blob')
    need(same(queue['changed_cells'],['Status','Turns','Findings']),'only target queue cells')
    for name in ['unrelated_bytes_preserved','existing_links_preserved','literal_initial_sha_line_preserved']:need(queue[name] is True,'queue preservation')
    sl=parsed['PUBLIC_SCOPE.json']
    for name in ['fresh_source_retrieval','fresh_source_inspection','fresh_pdf_byte_bindings','fresh_dataset_byte_bindings','full_original_replay','full_baseline_patch_replay','archive_reconstruction']:
        need(sl[name]=='NOT_RUN','honest source-free scope')
    return snapshot
def queue_integrity(path, binding):
    path=Path(os.path.abspath(path))
    for ancestor in path.parents:
        need(stat.S_ISDIR(ancestor.lstat().st_mode),'linked/non-directory queue ancestor')
    raw=ordinary(path)
    actual=dict(bytes=len(raw),sha256=sha(raw),git_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest())
    need(same(actual,binding['current']),'actual QUEUE bytes differ from fixed binding')
    return raw


def replay(snapshot, queue_bytes):
    """Fresh safe mathematical replay; omitted original/source inputs are not run."""
    import shutil
    need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000 required')
    modes=[('normal',[]),('O',['-O']),('OO',['-OO'])]
    errors={'count_locations':'pair crossings disagree with affine dependence','wrong_weight':'weighted identity','parity_blind_last':'last coefficient parity','omit_e1_parameter':'eight-point independent profile parameter','wrong_crossing_deletion':'crossing deletion coefficient','wrong_odd_deletion':'parity-specific halving deletion','omit_adjacent_even':'parity-specific halving deletion','reverse_mutation_sign':'mutation crossing sign','reverse_profile_transfer':'entire mutation profile transfer','unqualified_floor_slack':'unqualified floor-slack inequality is false'}
    with tempfile.TemporaryDirectory(prefix='crossing-halving-public-replay-') as td:
        root=Path(td);current=root/'current';audit=root/'audit';cwd=root/'cwd'
        current.mkdir();audit.mkdir();cwd.mkdir();queue=root/'queue';queue.mkdir();(queue/'QUEUE.md').write_bytes(queue_bytes)
        for prefix,dest in [('current/',current),('audit/',audit)]:
            for name,body in snapshot.items():
                if name.startswith(prefix):(dest/name[len(prefix):]).write_bytes(body)
        def freeze(d):
            for f in d.rglob('*'):f.chmod(0o555 if f.is_dir() else 0o444)
            d.chmod(0o555)
        def thaw(d):
            d.chmod(0o755)
            for f in d.rglob('*'):f.chmod(0o755 if f.is_dir() else 0o644)
        freeze(current);freeze(audit);freeze(cwd);freeze(queue)
        initial={f.relative_to(root).as_posix():sha(f.read_bytes()) for d in [current,audit,queue] for f in d.rglob('*') if f.is_file()}
        env=dict(PATH=os.defpath,HOME=str(root),TMPDIR=str(root),LC_ALL='C',PYTHONDONTWRITEBYTECODE='1')
        def execute(args,flags,where=cwd):
            q=subprocess.run([sys.executable,'-I','-S','-B',*flags,*map(str,args)],cwd=where,env=env,capture_output=True,timeout=120)
            return dict(exit_code=q.returncode,stdout=q.stdout.decode(),stderr=q.stderr.decode(),stdout_bytes=len(q.stdout),stdout_sha256=sha(q.stdout),stderr_bytes=len(q.stderr),stderr_sha256=sha(q.stderr))
        try:
            runs=[];mutants=[];probes=[];branches=[]
            for i,(mode,flags) in enumerate(modes):
                for kind,script in [('current',current/'check_claims.py'),('audit',audit/'check_independent.py')]:
                    r=execute([script,'--require-readonly'],flags)
                    expected=snapshot['verification/'+kind+'_'+mode+'.stdout.txt'];err=snapshot['verification/'+kind+'_'+mode+'.stderr.txt']
                    need(r['exit_code']==0 and r['stdout'].encode()==expected and r['stderr'].encode()==err,'full '+kind+' output bytes '+mode)
                    value=parse(r['stdout']);need(same(value,parse(expected)),'full typed output '+kind+' '+mode)
                    need(same(value['uid'],1000),'exact checker UID')
                    need(same(value['python_optimization' if kind=='current' else 'optimization'],i),'exact checker optimization')
                    r.update(kind=kind,mode=mode,command=['python','-I','-S','-B',*flags,kind+'/'+script.name,'--require-readonly']);runs.append(r)
                for mutant,message in errors.items():
                    r=execute([audit/'check_independent.py','--require-readonly','--mutant',mutant],flags)
                    need(r['exit_code']==1 and r['stdout']=='' and r['stderr']=='RuntimeError: '+message+'\n','semantic mutant must fail: '+mutant)
                    r.update(mode=mode,mutant=mutant);mutants.append(r)
            probe_code="""import errno,json,os,pathlib,sys
root=pathlib.Path(sys.argv[1]); entries=[]
if os.getuid()!=1000 or os.geteuid()!=1000:raise RuntimeError('UID 1000 required')
paths=[]
for name in ['current','audit','cwd','queue']:
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
            expected_entries=[]
            for name in ['current','audit','cwd','queue']:
                d=root/name
                for f in [d,*sorted(d.rglob('*'))]:expected_entries.append(dict(path=f.relative_to(root).as_posix(),operation='create' if f.is_dir() else 'write_open',errno=13,denied=True))
            writable=root/'writable';shutil.copytree(current,writable);thaw(writable)
            writable_audit=root/'writable_audit';shutil.copytree(audit,writable_audit);thaw(writable_audit)
            for i,(mode,flags) in enumerate(modes):
                r=execute(['-c',probe_code,root],flags)
                need(r['exit_code']==0 and r['stderr']=='','physical probes executed')
                need(same(parse(r['stdout']),dict(uid=1000,euid=1000,optimization=i,entries=expected_entries)),'full physical probes')
                r.update(mode=mode);probes.append(r)
                for kind,script in [('current',current/'check_claims.py'),('audit',audit/'check_independent.py')]:
                    ext=root/(kind+'_external_'+mode+'.json')
                    r=execute([script,'--require-readonly','--output',ext],flags)
                    expected=snapshot['verification/'+kind+'_'+mode+'.stdout.txt']
                    need(r['exit_code']==0 and r['stdout']==r['stderr']=='' and ext.read_bytes()==expected,'full external output bytes')
                    r.update(mode=mode,kind=kind,branch='external_output',file_content=ext.read_text());branches.append(r)
                    for branch,path,message in [('inside_output',script.parent/'FORBIDDEN.json','output must be external to the packet' if kind=='current' else 'output must be external'),('existing_output',ext,'output already exists')]:
                        r=execute([script,'--require-readonly','--output',path],flags)
                        need(r['exit_code']==1 and r['stdout']=='' and r['stderr']=='RuntimeError: '+message+'\n','invalid output rejected')
                        if branch=='inside_output':need(not path.exists(),'internal output absent')
                        r.update(mode=mode,kind=kind,branch=branch);branches.append(r)
                for kind,args,message in [('current',[writable/'check_claims.py','--require-readonly'],'packet directory is writable'),('audit',[writable_audit/'check_independent.py','--packet',current,'--require-readonly'],'directory writable')]:
                    r=execute(args,flags)
                    need(r['exit_code']==1 and r['stdout']=='' and r['stderr']=='RuntimeError: '+message+'\n','writable tree rejected')
                    r.update(mode=mode,kind=kind,branch='writable_tree');branches.append(r)
            final={f.relative_to(root).as_posix():sha(f.read_bytes()) for d in [current,audit,queue] for f in d.rglob('*') if f.is_file()}
            need(initial==final and not list(cwd.iterdir()),'all source-free inputs unchanged')
            return dict(status='PASS',queue_input=dict(bytes=len(queue_bytes),sha256=sha(queue_bytes),git_blob=hashlib.sha1(b'blob '+str(len(queue_bytes)).encode()+b'\0'+queue_bytes).hexdigest()),problem_id=7200057,disposition='exhausted',turns='5/5',full_target_resolved=False,novelty_claimed=False,best_known_claimed=False,native_runs=runs,semantic_mutants=mutants,physical_write_probes=probes,cli_branches=branches,semantic_mutations_rejected_per_mode=10,current_guard_negative_controls_per_mode=7,top_level_subprocess_executions=63,readonly_inputs_unchanged=True,fresh_source_retrieval='NOT_RUN',fresh_source_inspection='NOT_RUN',fresh_pdf_byte_bindings='NOT_RUN',fresh_dataset_byte_bindings='NOT_RUN',full_original_replay='NOT_RUN',full_baseline_patch_replay='NOT_RUN',archive_reconstruction='NOT_RUN',normalization='NONE; complete fresh mode-specific stdout/stderr bytes match pinned references, and the full outer record matches exact recursive JSON types.',scope='Source-free current mathematics and independent audit only. Omitted original and source/corpus/archive inputs are not freshly replayed. General target unresolved.')
        finally:
            for d in [current,audit,cwd,queue]:thaw(d)


def main():
    need(len(sys.argv)==5,'supply external manifest pin, external bootstrap pin, root, and actual QUEUE path')
    mp,bp,location,queue_path=sys.argv[1:];root=Path(os.path.abspath(location));before=integrity(root,mp,bp)
    queue_before=queue_integrity(queue_path,parse(before['QUEUE_BINDING.json']))
    result=replay(before,queue_before)
    need(same(result,parse(before['REPLAY_RESULTS.json'])),'fresh complete replay equals pinned record')
    need(integrity(root,mp,bp)==before,'entire release unchanged after replay')
    need(queue_integrity(queue_path,parse(before['QUEUE_BINDING.json']))==queue_before,'actual QUEUE unchanged after replay')
    print(json.dumps(dict(status='PASS',optimization=sys.flags.optimize,problem_id=7200057,disposition='exhausted',turns='5/5',manifest_sha256=mp,bootstrap_sha256=bp,exact_files=len(FILES),actual_queue_authenticated_before_and_after=True,fresh_pdf_byte_bindings='NOT_RUN',replay=result),indent=2,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,UnicodeError,subprocess.TimeoutExpired):
        print('REJECT: publication integrity or replay failed',file=sys.stderr);sys.exit(1)
