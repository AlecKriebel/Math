#!/usr/bin/env python3
"""Authenticate an exact publication snapshot before running frozen checkers."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: invoke with -I -S -B')
import hashlib, json, os, pathlib, shlex, stat, subprocess, tempfile, zipfile

PINS = {
    'AUDIT_SAFE.zip': (57974, 'c2b6716a48e5f4d5046ef4a85f54182506684d676f32d49e58bdf14c9ea9fd6a'),
    'AUDIT_EXTERNAL_MANIFEST.json': (3225, 'd7079b353c419f2558444b9eb0efa9efcf49fffc3bc252f55895f9603b544c0c'),
    'audit/AUTHOR_SAFE_FREEZE.zip': (15877, 'd1b572fc384124819c9f0618965bb77e86dd9474dc92dce57466ee3bf386602d'),
    'audit/AUTHOR_EXTERNAL_MANIFEST.json': (1975, '7853a1c2eb0c0ae13509de1f8ea2a05b5714170ad5d3a98f802fc54b6a797034'),
    'audit/CLARIFIED_SAFE.zip': (16579, 'af5efef8873f2a4b6fdc1f454a16d2c3cbac07fd8e103922df736793544d5f8c'),
    'audit/CLARIFIED_EXTERNAL_MANIFEST.json': (2302, 'f2a7bd92aaeca89f664ba718666ddb7187a1a8a06d7b8a32fede32a5264f52bf'),
    'audit/CLARIFICATION.patch': (6752, 'cb959b183c4da486043a8be3bb789906167194eb6852e8c84a0fe18ffc613604'),
    'audit/ACCEPTANCE.json': (2021, '31588c1d03942bb7bb3a8519f4ebfab1b219e62b845cf4f6cf40caec6d436a0f'),
}
def need(ok, message):
    if not ok: raise ValueError(message)
def sha(b): return hashlib.sha256(b).hexdigest()
def pairs(items):
    result = {}
    for k, v in items:
        need(k not in result, 'duplicate JSON key')
        result[k] = v
    return result
def decode(b): return json.loads(b, object_pairs_hook=pairs)
def regular(p):
    need(stat.S_ISREG(p.lstat().st_mode), 'not a regular file: ' + p.name)
    return p.read_bytes()
def zip_members(b):
    import io
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        infos=z.infolist(); names=[i.filename for i in infos]
        need(len(names)==len(set(names)), 'duplicate ZIP member')
        for i in infos:
            need(i.filename == pathlib.PurePosixPath(i.filename).name and i.filename not in ('', '.', '..'), 'unsafe ZIP path')
            need(not i.is_dir() and not (i.flag_bits & 1), 'ZIP directory or encryption')
            need(stat.S_IFMT(i.external_attr >> 16) in (0, stat.S_IFREG), 'ZIP special member')
        return {i.filename:z.read(i.filename) for i in infos}
def main():
    need(len(sys.argv)==3 and sys.argv[1]=='--expected-manifest', 'trusted external manifest digest required')
    anchor=sys.argv[2]
    need(len(anchor)==64 and all(c in '0123456789abcdef' for c in anchor), 'invalid digest')
    root=pathlib.Path(__file__).absolute().parent
    need(all(not p.is_symlink() for p in [root,*root.parents]), 'symlink path ancestry')
    manifest_bytes=regular(root/'PUBLICATION_MANIFEST.json')
    need(sha(manifest_bytes)==anchor, 'publication manifest anchor mismatch')
    manifest=decode(manifest_bytes)
    need(manifest['schema']=='torus-surgery-publication-v1' and manifest['problem_id']==2910, 'manifest identity')
    entries=manifest['files']; names=[e['path'] for e in entries]
    need(len(names)==len(set(names)) and 'PUBLICATION_MANIFEST.json' not in names, 'manifest inventory')
    for n in names:
        path=pathlib.PurePosixPath(n)
        need(not path.is_absolute() and all(c not in ('', '.', '..') for c in path.parts) and path.as_posix()==n, 'unsafe manifest path')
    dirs={pathlib.PurePosixPath(n).parent.as_posix() for n in names if '/' in n}
    actual=set()
    for p in root.rglob('*'):
        rel=p.relative_to(root).as_posix(); mode=p.lstat().st_mode
        if stat.S_ISDIR(mode): need(rel in dirs, 'unexpected directory')
        else:
            need(stat.S_ISREG(mode), 'symlink or special file')
            actual.add(rel)
    need(actual==set(names)|{'PUBLICATION_MANIFEST.json'}, 'publication file inventory')
    data={}
    for e in entries:
        b=regular(root/e['path'])
        need(type(e['bytes']) is int and len(b)==e['bytes'] and sha(b)==e['sha256'], 'publication member binding: '+e['path'])
        data[e['path']]=b
    for n,pin in PINS.items(): need((len(data[n]),sha(data[n]))==pin, 'immutable pin: '+n)
    meta=decode(data['PUBLICATION_METADATA.json'])
    need(meta['problem_id']==2910 and meta['rank']==918 and meta['status']=='unsolved' and meta['turns']=='3/5', 'publication status')
    need(meta['full_problem_solved'] is False and meta['full_problem_refuted'] is False and meta['novelty_claimed'] is False, 'publication claim scope')
    for folder, archive in [('audit','AUDIT_SAFE.zip'),('original','audit/AUTHOR_SAFE_FREEZE.zip'),('clarified','audit/CLARIFIED_SAFE.zip')]:
        members=zip_members(data[archive])
        actual_members={n[len(folder)+1:]:b for n,b in data.items() if n.startswith(folder+'/')}
        need(members==actual_members, 'exact ZIP/extracted member mismatch: '+folder)
    with tempfile.TemporaryDirectory(prefix='torus publication authenticated snapshot ') as td:
        td=pathlib.Path(td); snapshot=td/'packet'; snapshot.mkdir(); cwd=td/'unrelated cwd'; cwd.mkdir()
        for n,b in data.items():
            p=snapshot/n; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b)
        shim=td/'isolated-python'
        shim.write_text('#!/bin/sh\nexec '+shlex.quote(os.path.realpath(sys.executable))+' -I -S -B "$@"\n')
        shim.chmod(0o700)
        launcher="import sys;from pathlib import Path;shim,entry,*args=sys.argv[1:];sys.executable=shim;sys.argv=[entry,*args];exec(compile(Path(entry).read_bytes(),entry,'exec'),{'__name__':'__main__','__file__':entry})"
        env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
        cmd=[str(shim)]+(['-O'] if sys.flags.optimize else [])+['-c',launcher,str(shim),str(snapshot/'audit/replay.py'),str(snapshot/'audit'),str(snapshot/'AUDIT_EXTERNAL_MANIFEST.json'),str(snapshot/'AUDIT_SAFE.zip')]
        r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=600)
        need(r.returncode==0 and not r.stderr, 'frozen replay failed: '+r.stderr.decode(errors='replace'))
        result=decode(r.stdout)
        need(result['result']=='pass' and result['package_cli_rejections']==48 and result['patch_reproduced'] is True, 'replay result')
    print(json.dumps({'result':'pass','problem_id':2910,'status':'unsolved','turns':'3/5','optimized':bool(sys.flags.optimize),'files_verified':len(data)+1,'authenticated_snapshot':True,'descendants_isolated_no_site_no_bytecode':True,'source_bytes_rehashed_this_run':False,'frozen_replay':result},sort_keys=True))
if __name__=='__main__':
    try: main()
    except Exception as e:
        print(json.dumps({'result':'fail','error':str(e)},sort_keys=True),file=sys.stderr)
        sys.exit(1)
