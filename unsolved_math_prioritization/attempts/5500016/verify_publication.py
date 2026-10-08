#!/usr/bin/env python3
"""Exact, source-free publication verification. Invoke through a trusted external bootstrap.
No online requests. Requires actual UID=EUID=1000 and Python 3.10+.
Security scope: static byte anchoring, POSIX permissions and isolated Python imports;
not a kernel sandbox and not safe execution of arbitrarily replaced Python runtimes.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile

ACCEPTED = {'PUBLIC_SCOPE.json': {'bytes': 1279, 'sha256': '0494074ff1c6ee318d07c21ca775345cc0fffd23959b564408563e2aad51cef0'}, 'audit/AUDIT.md': {'bytes': 19315, 'sha256': 'eca9ea5dc193ec7edd9ff634155fa5dc4a5c72c20710083daa9fa180c3927394'}, 'audit/EXPECTED_AUDIT_RESULTS.json': {'bytes': 25560, 'sha256': '6b713901ea104722665722d349c2748c83d4289b94077a84b9aeeb161944363d'}, 'audit/FROZEN_INPUT_MANIFEST.json': {'bytes': 1347, 'sha256': '530c97c88d71b6a570da586ae579c8e919ae3c9063d2b83b11027aa795a33a4c'}, 'audit/MANIFEST.json': {'bytes': 3751, 'sha256': 'e77ef2e0aaca67621af1a85b9c864a0accf8d1968fc36670f58a1e97cb4605c4'}, 'audit/README.md': {'bytes': 1633, 'sha256': '80074483532cdca3b166a545c179bc66460985414a0f0875fa38ec8dcf7ed059'}, 'audit/SOURCE_AUDIT.json': {'bytes': 8767, 'sha256': '917f373375b0c624342659d6c01fd04640d6735255d15e8be54fd36483c183a7'}, 'audit/audit_counting.py': {'bytes': 18154, 'sha256': '3d923b6b4dae1ebffcf7896322913337ef971b391229ce48ce70658026dc5fea'}, 'audit/receipts/EXECUTION_RECEIPT.json': {'bytes': 8905, 'sha256': '12a3e6576e0af21f43df9a03d92adbbd206a5798a8b230ec70d4de5ff263d11f'}, 'audit/receipts/audit.O.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'audit/receipts/audit.O.stdout.json': {'bytes': 25560, 'sha256': '6b713901ea104722665722d349c2748c83d4289b94077a84b9aeeb161944363d'}, 'audit/receipts/audit.OO.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'audit/receipts/audit.OO.stdout.json': {'bytes': 25560, 'sha256': '6b713901ea104722665722d349c2748c83d4289b94077a84b9aeeb161944363d'}, 'audit/receipts/audit.normal.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'audit/receipts/audit.normal.stdout.json': {'bytes': 25560, 'sha256': '6b713901ea104722665722d349c2748c83d4289b94077a84b9aeeb161944363d'}, 'audit/receipts/author.O.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'audit/receipts/author.O.stdout.json': {'bytes': 7683, 'sha256': 'bceedd5fd3210423942f9001d7e75ab0c8c1c15225917e2f2f2845ec82711959'}, 'audit/receipts/author.OO.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'audit/receipts/author.OO.stdout.json': {'bytes': 7683, 'sha256': 'bceedd5fd3210423942f9001d7e75ab0c8c1c15225917e2f2f2845ec82711959'}, 'audit/receipts/author.normal.stderr.txt': {'bytes': 0, 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}, 'audit/receipts/author.normal.stdout.json': {'bytes': 7683, 'sha256': 'bceedd5fd3210423942f9001d7e75ab0c8c1c15225917e2f2f2845ec82711959'}, 'audit/run_validation.py': {'bytes': 4650, 'sha256': '72231b2a1f23e94ee4e39711023e70f53aee1521165baa182e4bf3e854893702'}, 'author/EXECUTION_RESULTS.json': {'bytes': 1055, 'sha256': '2dc90625beaa4aa292c5e5f063cdaab07af5ed01129993801a17bda7df85a027'}, 'author/EXPECTED_RESULTS.json': {'bytes': 7683, 'sha256': 'bceedd5fd3210423942f9001d7e75ab0c8c1c15225917e2f2f2845ec82711959'}, 'author/MANIFEST.json': {'bytes': 1323, 'sha256': '633ea7bc019fe35490faacdc2b42b31ce1e48048c60689f2f054bec813de08b5'}, 'author/README.md': {'bytes': 1081, 'sha256': '0b69fa4cbaf40a4cbfd41fc7fdb05618714509014fe29b3311900b2e237ef5c3'}, 'author/REPORT.md': {'bytes': 24229, 'sha256': '51ce97fa26e2f27f4f649b89a85711c118467ac8210835f518206990ef19e621'}, 'author/SOURCE_METADATA.json': {'bytes': 6591, 'sha256': 'fb50713c0628a610f92d3843f3ad75a25e3f5963fa4658ab3d41878afa89c65d'}, 'author/VALIDATION.md': {'bytes': 2857, 'sha256': 'ba6e5bc6ef564e35d16abd169683551041167af66face34334993f05e44d4420'}, 'author/check_counting.py': {'bytes': 14014, 'sha256': 'c3598583dacd2695b4a245fafb23c9b253c31262c95e6f7a8fe8236b514eae33'}}
QUEUE = {'bytes': 397815, 'sha256': '9eef625462e2dff44c306c9eb515a5c2446179539bb6887eb2183a1549838393'}
OUTER = {'README.md','ACCEPTANCE.md','PUBLIC_SCOPE.json','verify_publication.py',
         'controls.py','REPLAY_RESULTS.json','CONTROL_RESULTS.json','VERIFICATION_RESULTS.json',
         'PUBLICATION_MANIFEST.json','BOOTSTRAP.py'}
FILES = set(ACCEPTED) | OUTER
DIRS = {'author','audit','audit/receipts'}
MODES = [('normal',[]),('O',['-O']),('OO',['-OO'])]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def same(a,b):
    """Full recursive equality, including exact scalar/container types."""
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return set(a)==set(b) and all(type(k) is str and same(a[k],b[k]) for k in a)
    if type(a) is list:
        return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b


def strict_json(data):
    def pairs(rows):
        result={}
        for k,v in rows:
            need(k not in result,'duplicate JSON key')
            result[k]=v
        return result
    def invalid(value):
        raise ValueError('nonfinite JSON number')
    value=json.loads(data.decode('utf-8'),object_pairs_hook=pairs,parse_constant=invalid)
    def visit(x):
        need(type(x) in (dict,list,str,int,float,bool,type(None)),'JSON type')
        if type(x) is float:
            need(__import__('math').isfinite(x),'nonfinite JSON number')
        elif type(x) is dict:
            for k,v in x.items():
                need(type(k) is str,'JSON key type');visit(v)
        elif type(x) is list:
            for v in x:visit(v)
    visit(value)
    return value


def keys(obj,wanted):
    need(type(obj) is dict and set(obj)==set(wanted),'exact object keys')


def integer(x):
    need(type(x) is int and x>=0,'nonnegative exact integer')


def descriptor(data):
    return {'bytes':len(data),'sha256':sha(data)}


def file_table(root):
    """Reject symlinks, hardlinks, devices, FIFOs and unexpected directories."""
    need(stat.S_ISDIR(root.lstat().st_mode),'root must be an ordinary directory')
    files={};dirs=set()
    def walk(d):
        for f in sorted(d.iterdir()):
            rel=f.relative_to(root).as_posix();s=f.lstat()
            if stat.S_ISDIR(s.st_mode):
                dirs.add(rel);walk(f)
            else:
                need(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'nonordinary input: '+rel)
                files[rel]=f.read_bytes()
    walk(root)
    need(dirs==DIRS,'exact directory inventory')
    need(set(files)==FILES,'exact file inventory')
    return files


def manifest_schema(obj):
    keys(obj,['schema','problem_id','files','queue'])
    need(same(obj['schema'],1) and same(obj['problem_id'],5500016),'manifest identity')
    need(type(obj['files']) is list,'manifest files list')
    expected=FILES-{'PUBLICATION_MANIFEST.json','BOOTSTRAP.py'}
    seen=set()
    for row in obj['files']:
        keys(row,['path','bytes','sha256'])
        n=row['path'];need(type(n) is str and n in expected and n not in seen,'manifest path')
        seen.add(n);integer(row['bytes'])
        need(type(row['sha256']) is str and len(row['sha256'])==64 and all(c in '0123456789abcdef' for c in row['sha256']),'manifest SHA')
    need(seen==expected,'manifest exact inventory')
    need(same(obj['queue'],QUEUE),'exact queue descriptor')


def integrity(root,queue):
    snapshot=file_table(root)
    need(not queue.is_symlink() and stat.S_ISREG(queue.lstat().st_mode),'ordinary queue file')
    need(same(descriptor(queue.read_bytes()),QUEUE),'exact queue bytes')
    for n,d in ACCEPTED.items():
        need(same(descriptor(snapshot[n]),d),'frozen public input: '+n)
    parsed={n:strict_json(b) for n,b in snapshot.items() if n.endswith('.json')}
    manifest=parsed['PUBLICATION_MANIFEST.json'];manifest_schema(manifest)
    for row in manifest['files']:
        need(same({'path':row['path'],**descriptor(snapshot[row['path']])},row),'manifest byte mismatch')
    # Validate original public author, original audit and frozen-author manifests independently.
    for prefix in ('author','audit'):
        original=parsed[prefix+'/MANIFEST.json'];rows=original['files']
        expected={n[len(prefix)+1:] for n in ACCEPTED if n.startswith(prefix+'/') and n!=prefix+'/MANIFEST.json'}
        need(type(rows) is list and len(rows)==len(expected),'inner manifest length')
        seen=set()
        for row in rows:
            keys(row,['path','bytes','sha256']);n=row['path']
            need(type(n) is str and n in expected and n not in seen,'inner manifest inventory')
            seen.add(n);integer(row['bytes'])
            need(same(row,{'path':n,**descriptor(snapshot[prefix+'/'+n])}),'inner manifest bytes')
        need(seen==expected,'inner manifest missing file')
    frozen=parsed['audit/FROZEN_INPUT_MANIFEST.json']
    need(same(frozen['file_count'],8),'frozen author count')
    need(same(frozen['files'],[{'path':n[7:],**descriptor(snapshot[n])} for n in sorted(ACCEPTED) if n.startswith('author/')]),'frozen author full inventory')
    for n in FILES:
        if n.endswith('.py'):
            need(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(snapshot[n]))),'optimized-away assertion')
    for kind,expected in [('author','author/EXPECTED_RESULTS.json'),('audit','audit/EXPECTED_AUDIT_RESULTS.json')]:
        for mode,_ in MODES:
            need(snapshot[f'audit/receipts/{kind}.{mode}.stdout.json']==snapshot[expected],'historical complete stdout')
            need(snapshot[f'audit/receipts/{kind}.{mode}.stderr.txt']==b'','historical complete stderr')
    return snapshot,parsed


def physical_probes(root,queue):
    need(os.getuid()==1000 and os.geteuid()==1000,'actual UID=EUID=1000 required')
    observations=[]
    entries=[('.',root)]+[(f.relative_to(root).as_posix(),f) for f in sorted(root.rglob('*'))]+[('QUEUE.md',queue)]
    for n,f in entries:
        directory=f.is_dir();wanted=0o555 if directory else 0o444
        need(stat.S_IMODE(f.lstat().st_mode)==wanted and not os.access(f,os.W_OK),'read-only mode: '+n)
        target=f/'DENIED_CREATE_PROBE' if directory else f
        flags=os.O_WRONLY | (os.O_CREAT|os.O_EXCL if directory else 0)
        try:
            fd=os.open(target,flags,0o600)
        except PermissionError as e:
            need(e.errno==13,'write probe errno')
            observations.append({'path':n,'operation':'create' if directory else 'write_open','denied':True,'errno':e.errno})
        else:
            os.close(fd);raise ValueError('write unexpectedly succeeded')
    return observations


def replay(snapshot):
    """Fresh raw stdout/stderr, no timestamp/path stripping or numeric coercion."""
    need(os.getuid()==1000 and os.geteuid()==1000,'actual UID=EUID=1000 required')
    with tempfile.TemporaryDirectory(prefix='polygonalization-public-replay-') as tmp:
        temp=Path(tmp);root=temp/'relocated public inputs';hostile=temp/'hostile working directory'
        root.mkdir();hostile.mkdir()
        for n,b in snapshot.items():
            if n.startswith(('author/','audit/')):
                f=root/n;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
        for name in ['json','fractions','random','hashlib','pathlib','sitecustomize','usercustomize','check_counting','audit_counting']:
            (hostile/(name+'.py')).write_text("raise RuntimeError('HOSTILE_IMPORT_EXECUTED')\n")
        for f in root.rglob('*'):f.chmod(0o555 if f.is_dir() else 0o444)
        root.chmod(0o555)
        before={f.relative_to(root).as_posix():descriptor(f.read_bytes()) for f in root.rglob('*') if f.is_file()}
        runs=[]
        probe_code="""import os,sys,json,stat
from pathlib import Path
r=Path(sys.argv[1]);rows=[]
if os.getuid()!=1000 or os.geteuid()!=1000:raise ValueError('UID')
for f in [r,*sorted(r.rglob('*'))]:
 d=f.is_dir();n='.' if f==r else f.relative_to(r).as_posix()
 if stat.S_IMODE(f.lstat().st_mode)!=(0o555 if d else 0o444) or os.access(f,os.W_OK):raise ValueError('mode')
 try:fd=os.open(f/'DENIED_CREATE_PROBE' if d else f,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if d else 0),0o600)
 except PermissionError as e:
  if e.errno!=13:raise
  rows.append({'path':n,'operation':'create' if d else 'write_open','denied':True,'errno':e.errno})
 else:os.close(fd);raise ValueError('write succeeded')
print(json.dumps({'uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,'probes':rows},sort_keys=True,indent=2))
"""
        env=dict(os.environ,PYTHONPATH=str(hostile),PYTHONSTARTUP=str(hostile/'sitecustomize.py'),PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='1')
        try:
            for mode,flags in MODES:
                probe=subprocess.run([sys.executable,'-I','-S','-B',*flags,'-c',probe_code,str(root)],cwd=hostile,env=env,capture_output=True,timeout=30)
                need(probe.returncode==0 and probe.stderr==b'','physical probe failed')
                probes=strict_json(probe.stdout)
                need(same(probes['uid'],1000) and same(probes['euid'],1000),'probe UID')
                for kind,script,args,expected in [('author','author/check_counting.py',[],'author/EXPECTED_RESULTS.json'),('audit','audit/audit_counting.py',[str(root/'author')],'audit/EXPECTED_AUDIT_RESULTS.json')]:
                    run=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/script),*args],cwd=hostile,env=env,capture_output=True,timeout=180)
                    need(run.returncode==0,'mathematical execution exit')
                    need(run.stdout==snapshot[expected] and run.stderr==b'','full raw stream mismatch')
                    actual=strict_json(run.stdout);reference=strict_json(snapshot[expected])
                    need(same(actual,reference),'full recursively typed stdout object mismatch')
                    runs.append({'kind':kind,'mode':mode,'exit_code':run.returncode,'stdout_utf8':run.stdout.decode('utf-8'),'stderr_utf8':run.stderr.decode('utf-8'),'stdout':descriptor(run.stdout),'stderr':descriptor(run.stderr),'typed_result':actual,'probe_stdout_utf8':probe.stdout.decode('utf-8'),'probe_stderr_utf8':probe.stderr.decode('utf-8'),'probe_result':probes})
            after={f.relative_to(root).as_posix():descriptor(f.read_bytes()) for f in root.rglob('*') if f.is_file()}
            need(same(before,after),'read-only relocated inputs changed')
            return {'schema':1,'problem_id':5500016,'uid':os.getuid(),'euid':os.geteuid(),'inputs_unchanged':True,'hostile_import_sentinels_executed':False,'python_import_isolation':['-I','-S','-B'],'runs':runs,'source_original_byte_replay':'NOT_RUN','source_text_replay':'NOT_RUN','source_inspection':'NOT_RUN','corpus_or_dataset_replay':'NOT_RUN'}
        finally:
            root.chmod(0o755)
            for f in root.rglob('*'):f.chmod(0o755 if f.is_dir() else 0o644)


def execute(root,queue,inventory_only=False):
    snapshot,parsed=integrity(root,queue)
    before={n:descriptor(b) for n,b in snapshot.items()}
    probes=physical_probes(root,queue)
    if inventory_only:
        return {'schema':1,'problem_id':5500016,'inventory_verified':True,'uid':os.getuid(),'euid':os.geteuid(),'physical_probes':probes}
    result=replay(snapshot)
    need(same(result,parsed['REPLAY_RESULTS.json']),'entire fresh replay differs from pinned full reference')
    need(same(before,{n:descriptor(b) for n,b in file_table(root).items()}),'entire delivery changed')
    need(same(descriptor(queue.read_bytes()),QUEUE),'queue changed during replay')
    return {'schema':1,'problem_id':5500016,'accepted_scope':'bounded partial results only','full_target_resolved':False,'status':'exhausted','turns':'5/5','physical_probes':probes,'fresh_replay':result}


def verify(root,queue,inventory_only=False):
    result=execute(root,queue,inventory_only)
    if not inventory_only:
        reference=(root/'VERIFICATION_RESULTS.json').read_bytes()
        need(same(result,strict_json(reference)),'full typed verification result mismatch')
        rendered=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode('utf-8')
        need(rendered==reference,'complete verification stdout bytes mismatch')
    return result
