#!/usr/bin/env python3
"""Authenticate accepted synchronous reflected-Brownian partials; replay source-free finite checks."""
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

ACCEPTED = {'ACCEPTANCE.md': {'bytes': 3295, 'sha256': 'bd2205f344bf1fcda5d5433227acea9547d6654e4cb21cbea49edde302a1a401'}, 'PUBLIC_SCOPE.json': {'bytes': 1292, 'sha256': 'e4c544d744d67f85c6062a584c8a73adfd737a391a8c0410d76eb856e6dbeab6'}, 'QUEUE_BINDING.json': {'bytes': 652, 'sha256': '19f3f7dbaa38ec0fd5b31362fd8f55e6bff80f4c2e4e73584ab685c860a336e0'}, 'README.md': {'bytes': 2527, 'sha256': 'c1f6d933c9b61006cf2dfee18245ffd3ed012c7c85d74ba3e568d37a858a5147'}, 'REPLAY_RESULTS.json': {'bytes': 35935, 'sha256': '34b05f2183c1cd6c376d88bccb9bddd32e54212c4b798c23e5e0bbd637d21ab7'}, 'audit/AUDIT.md': {'bytes': 15200, 'sha256': '96113aa6ad578370a0499bf29fbf334df7c28c702410743f601b8184b60d51f7'}, 'audit/MANIFEST.json': {'bytes': 2267, 'sha256': 'dc0587714cdbaee9b3aee0bee0eedf51f36ff31579e7604e0c9547509306c84a'}, 'audit/README.md': {'bytes': 1193, 'sha256': '756bc770ae76e7027770002b7e6dcf94cdceb52c76d8f6eed778d655879be004'}, 'audit/REPLAY_RECEIPT.json': {'bytes': 29151, 'sha256': 'b55acd5734966e9dec7e3c0d2e592b04e38feedc4a3777b90c5302b2ed9121d0'}, 'audit/SEAL_RECEIPT.json': {'bytes': 2159, 'sha256': '26850282788c106ade0f37b1121cddb7c92dfb1949bee21ccd315ef40978d83a'}, 'audit/SOURCE_RECHECK.json': {'bytes': 4210, 'sha256': 'e551ee97e34a8d2928205639d9f4b079092e3a4fd4b26266313666fcf1254e42'}, 'audit/independent_checks.py': {'bytes': 7247, 'sha256': 'c4efc3beae3f74391f7e93188d57bbe8c8f1a4518ee9316d57b75bfabdaf2353'}, 'audit/replay_audit.py': {'bytes': 6638, 'sha256': '6e1914b79792f12aff5ceeb825e11ce3b446e38bd18c7324e248d712d9397be1'}, 'author/MANIFEST.json': {'bytes': 954, 'sha256': 'f2e19fe10945f8319e3b40823c05b24fc58f06a27ce20bf0a6458f4f4b33ea7d'}, 'author/README.md': {'bytes': 915, 'sha256': 'd5d28a303e6028bcdcbdcb014dd65fe9398dd0f1dff5020b99dc398f840e7eda'}, 'author/REPORT.md': {'bytes': 20699, 'sha256': '1f2ec9eac67a2c94232dcf62fca851162ef22013fd968804bcfcc3c97074e5b9'}, 'author/SOURCE_METADATA.json': {'bytes': 5105, 'sha256': '69057be50db380b5068ad152dd9c3f53669893066398d06a791ae0a05d05cc7d'}, 'author/VERIFICATION.json': {'bytes': 3500, 'sha256': '57685a43a1ab22286516b49db4731ae468072fa303f479e45048994a008c1d8f'}, 'author/check_identities.py': {'bytes': 6062, 'sha256': 'a8b388ab8a2170c50fd6ca1df1a93dfa10848fa3a9792006c0a98915089cebac'}, 'mutation_tests.py': {'bytes': 13445, 'sha256': '3fa9b986e0cb0060cc0db08423b4bbdb6c1fec37be29e77af2a00d6eef011a0d'}}
PAYLOAD = set(ACCEPTED) | {'verify_publication.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json','BOOTSTRAP.py'}
DIRS = {'author','audit'}

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
    exact_int(value['problem_id'], 9500005)
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
    for prefix,skip in [('author/',{'MANIFEST.json'}),('audit/',{'MANIFEST.json','SEAL_RECEIPT.json'})]:
        inner=parsed[prefix+'MANIFEST.json']; exact_int(inner['problem_id'],9500005)
        rows=inner['files']; expected={n[len(prefix):] for n in FILES if n.startswith(prefix)}-skip
        need(type(rows) is dict and set(rows)==expected,'frozen manifest inventory')
        for n,row in rows.items():
            need(type(row) is dict,'frozen manifest row')
            keys(row,['bytes','sha256']+(['mode'] if prefix=='audit/' else []))
            exact_int(row['bytes']);digest(row['sha256'])
            need(same(row['bytes'],len(snapshot[prefix+n])) and row['sha256']==sha(snapshot[prefix+n]),'frozen byte binding')
            if prefix=='audit/':need(row['mode']=='0444','historical mode')
    import ast
    for name in [n for n in FILES if n.endswith('.py')]:
        need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(snapshot[name]))),'no optimized-away assertions')
    sl=parsed['PUBLIC_SCOPE.json']
    need(sl['full_target_resolved'] is False and sl['novelty_claimed'] is False and sl['disposition']=='exhausted' and sl['turns']=='5/5','accepted scope')
    for name in ['fresh_source_retrieval','fresh_source_inspection','fresh_pdf_byte_bindings','fresh_dataset_byte_bindings']:
        need(sl[name]=='NOT_RUN','honest source-free scope')
    return snapshot

def queue_check(path, snapshot):
    expected=parse(snapshot['QUEUE_BINDING.json']);raw=ordinary(Path(path))
    need(same(len(raw),expected['new_bytes']) and sha(raw)==expected['new_sha256'],'exact external QUEUE postimage')
    need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==expected['new_git_blob'],'queue git blob')
    return dict(bytes=len(raw),sha256=sha(raw),git_blob=expected['new_git_blob'])


def replay(snapshot):
    """Complete deterministic finite replay, with no source/corpus reads."""
    need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000 required')
    historical=parse(snapshot['audit/REPLAY_RECEIPT.json'])
    verification=parse(snapshot['author/VERIFICATION.json'])
    modes=[('normal',[]),('-O',['-O']),('-OO',['-OO'])]
    with tempfile.TemporaryDirectory(prefix='synchronous-brownian-public-replay-') as td:
        root=Path(td);ro=root/'author';audit=root/'audit';cwd=root/'cwd'
        ro.mkdir();audit.mkdir();cwd.mkdir()
        for prefix,dest in [('author/',ro),('audit/',audit)]:
            for name,body in snapshot.items():
                if name.startswith(prefix):
                    path=dest/name[len(prefix):];path.write_bytes(body)
        def freeze(d):
            for f in d.rglob('*'):f.chmod(0o555 if f.is_dir() else 0o444)
            d.chmod(0o555)
        def thaw(d):
            d.chmod(0o755)
            for f in d.rglob('*'):f.chmod(0o755 if f.is_dir() else 0o644)
        freeze(ro);freeze(audit);freeze(cwd)
        initial={f.relative_to(root).as_posix():dict(bytes=f.stat().st_size,sha256=sha(f.read_bytes()),mode=f.stat().st_mode&0o777) for d in [ro,audit] for f in d.rglob('*') if f.is_file()}
        env=dict(PATH=os.defpath,HOME=str(root),TMPDIR=str(root),LC_ALL='C',PYTHONDONTWRITEBYTECODE='1')
        def execute(args,flags):
            q=subprocess.run([sys.executable,'-I','-S','-B',*flags,*map(str,args)],cwd=cwd,env=env,capture_output=True,timeout=120)
            return dict(returncode=q.returncode,stdout=q.stdout.decode(),stderr=q.stderr.decode(),stdout_bytes=len(q.stdout),stdout_sha256=sha(q.stdout),stderr_bytes=len(q.stderr),stderr_sha256=sha(q.stderr))
        def compare(r,ref):
            need(same(r['returncode'],ref['returncode']) and r['stdout']==ref['stdout'] and r['stderr']==ref['stderr'],'complete historical process bytes')
            if 'parsed_result' in ref:
                need(same(parse(r['stdout']),ref['parsed_result']),'complete typed positive output')
        try:
            positives=[];negatives=[];code=snapshot['author/check_identities.py'].decode()
            need(len(historical['positive_runs'])==6 and len(historical['semantic_negative_control_runs'])==21 and len(historical['mutations'])==7,'exact historical process inventory')
            for i,(mode,flags) in enumerate(modes):
                for j,(kind,script) in enumerate([('original_checker',ro/'check_identities.py'),('independent_checker',audit/'independent_checks.py')]):
                    ref=historical['positive_runs'][2*i+j]
                    need(ref['label']==kind and ref['mode']==mode,'positive order and mode')
                    r=execute([script],flags);compare(r,ref)
                    value=parse(r['stdout']);need(same(value['uid'],1000),'actual checker UID')
                    if j==0:
                        vr=verification['runs'][i]
                        need(vr['mode']==mode and same(value,vr['result']) and r['stderr']==vr['stderr'] and same(r['returncode'],vr['returncode']),'complete author verification reference')
                    r.update(label=kind,mode=mode,parsed_result=value);positives.append(r)
                for j,m in enumerate(historical['mutations']):
                    old=m['original_fragment'];new=m['mutated_fragment'];label=m['name']
                    need(code.count(old)==1,'unique mutation')
                    changed=code.replace(old,new,1)
                    need(sha(changed.encode())==m['mutated_sha256'],'exact semantic mutant bytes')
                    script="exec(compile("+repr(changed)+", "+repr('<semantic-'+label+'>')+", 'exec'), {'__name__':'__main__'})"
                    r=execute(['-c',script],flags);ref=historical['semantic_negative_control_runs'][7*i+j]
                    need(ref['label']==label and ref['mode']==mode and ref['expected_error']==m['expected_error'],'negative order and mode')
                    compare(r,ref)
                    need(r['returncode']==1 and r['stdout']=='' and ('RuntimeError: '+m['expected_error']+'\n') in r['stderr'],'intended semantic failure')
                    r.update(label=label,mode=mode,expected_error=m['expected_error']);negatives.append(r)
            probe_code="""import errno,json,os,pathlib,sys
root=pathlib.Path(sys.argv[1]);entries=[]
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
            probes=[];expected_entries=[]
            for name in ['author','audit','cwd']:
                d=root/name
                for f in [d,*sorted(d.rglob('*'))]:expected_entries.append(dict(path=f.relative_to(root).as_posix(),operation='create' if f.is_dir() else 'write_open',errno=13,denied=True))
            for i,(mode,flags) in enumerate(modes):
                r=execute(['-c',probe_code,root],flags)
                expected=dict(uid=1000,euid=1000,optimization=i,entries=expected_entries)
                need(r['returncode']==0 and r['stderr']=='' and r['stdout']==json.dumps(expected,sort_keys=True)+'\n','full physical probe output bytes')
                need(same(parse(r['stdout']),expected),'full typed physical probes')
                r.update(mode=mode);probes.append(r)
            final={f.relative_to(root).as_posix():dict(bytes=f.stat().st_size,sha256=sha(f.read_bytes()),mode=f.stat().st_mode&0o777) for d in [ro,audit] for f in d.rglob('*') if f.is_file()}
            need(same(initial,final) and not list(cwd.iterdir()),'all input bytes/modes unchanged')
            return dict(schema=1,status='PASS',problem_id=9500005,uid=os.getuid(),euid=os.geteuid(),disposition='exhausted',turns='5/5',full_target_resolved=False,novelty_claimed=False,positive_runs=positives,semantic_negative_runs=negatives,physical_write_probes=probes,input_before=initial,input_after=final,readonly_inputs_unchanged=True,fresh_source_retrieval='NOT_RUN',fresh_source_inspection='NOT_RUN',fresh_pdf_byte_bindings='NOT_RUN',fresh_dataset_byte_bindings='NOT_RUN',historical_replay_driver='NOT_RUN',normalization='NONE; exact complete process bytes and complete typed positive objects, then exact typed full fresh replay.',scope='Finite exact algebra only. Both Brownian questions remain unresolved.')
        finally:
            for d in [ro,audit,cwd]:thaw(d)


def main():
    need(len(sys.argv)==5,'supply external manifest pin, external bootstrap pin, root and QUEUE')
    mp,bp,location,queue=sys.argv[1:];root=Path(os.path.abspath(location));before=integrity(root,mp,bp)
    queue_receipt=queue_check(queue,before)
    result=replay(before)
    need(same(result,parse(before['REPLAY_RESULTS.json'])),'fresh complete replay equals pinned record')
    need(integrity(root,mp,bp)==before and same(queue_check(queue,before),queue_receipt),'entire release/QUEUE unchanged after replay')
    print(json.dumps(dict(status='PASS',optimization=sys.flags.optimize,problem_id=9500005,disposition='exhausted',turns='5/5',manifest_sha256=mp,bootstrap_sha256=bp,exact_files=len(FILES),fresh_pdf_byte_bindings='NOT_RUN',queue=queue_receipt,replay=result),indent=2,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,UnicodeError,subprocess.TimeoutExpired):
        print('REJECT: publication integrity or replay failed',file=sys.stderr);sys.exit(1)
