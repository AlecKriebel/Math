#!/usr/bin/env python3
"""Source-free anchored integrity and bounded replay. No Python assertions."""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, json, os, pathlib, re, shutil, subprocess, tarfile, tempfile

ORIGINAL = 'e6f747996c9dcf7fd9d525cc34f347577538f169e620b4dd3a98269f27b31e29'
AUDIT = 'fbda65b68e6dcd94c967be5312b3e2421f708185b713c1d89ea6ee4fd178376b'
ACCEPTED = '3fd0911eb41ac797bc393d822e65eeda04bf3afc3f10df1b21620acb4a427e8c'

def need(ok, why):
    if not ok:
        raise RuntimeError(why)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def unique(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, 'duplicate JSON key')
        out[key] = value
    return out

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)

def integrity(root, anchor):
    need(not root.is_symlink(), 'root is a symlink')
    raw = (root/'PUBLIC_MANIFEST.json').read_bytes()
    need(sha(raw) == anchor, 'external manifest mismatch')
    m = read_json(root/'PUBLIC_MANIFEST.json')
    need(set(m) == {'schema','problem_id','status','turns','files'}, 'manifest schema')
    need(m['schema'] == 'ramification-publication-v1' and m['problem_id'] == 30001278
         and m['status'] == 'unsolved' and m['turns'] == '5/5', 'manifest binding')
    need(isinstance(m['files'], list), 'file list')
    paths = set()
    for x in m['files']:
        need(set(x) == {'path','bytes','sha256'}, 'entry schema')
        n = x['path']; p = pathlib.PurePosixPath(n)
        need(isinstance(n,str) and not p.is_absolute() and '..' not in p.parts
             and p.as_posix() == n and n not in paths and n != 'PUBLIC_MANIFEST.json', 'path')
        need(type(x['bytes']) is int and x['bytes'] >= 0, 'byte count')
        need(isinstance(x['sha256'],str) and re.fullmatch('[0-9a-f]{64}',x['sha256']), 'hash')
        paths.add(n)
    dirs = {str(p) for n in paths for p in pathlib.PurePosixPath(n).parents if str(p) != '.'}
    actual = set()
    for p in root.rglob('*'):
        n = p.relative_to(root).as_posix()
        need(not p.is_symlink(), 'symlink forbidden')
        if p.is_dir():
            need(n in dirs, 'unlisted directory')
        else:
            need(p.is_file(), 'not regular file'); actual.add(n)
    need(actual == paths | {'PUBLIC_MANIFEST.json'}, 'file inventory')
    for x in m['files']:
        raw = (root/x['path']).read_bytes()
        need(len(raw) == x['bytes'] and sha(raw) == x['sha256'], 'payload mismatch: '+x['path'])
    for folder, name, expected in [('original','MANIFEST.json',ORIGINAL),('accepted','MANIFEST.json',ACCEPTED),('audit','AUDIT_MANIFEST.json',AUDIT)]:
        d = root/folder
        need(sha((d/name).read_bytes()) == expected, 'frozen manifest')
        frozen = read_json(d/name)
        need({p.name for p in d.iterdir()} == {x['path'] for x in frozen['files']} | {name}, 'frozen inventory')
        for x in frozen['files']:
            b = (d/x['path']).read_bytes()
            need(len(b) == x['bytes'] and sha(b) == x['sha256'], 'frozen payload')
    need((root/'audit/AUTHOR_MANIFEST.json').read_bytes() == (root/'original/MANIFEST.json').read_bytes(), 'audit input binding')
    for archive, folder, expected in [
        ('ramification_30001278_author.tar.gz','original','d6bf160fd3973409c26ed8b514bc231956b7d3d113cf888e5e15b5f6060779d1'),
        ('ramification_30001278_independent_audit.tar.gz','audit','63da1fa858004253b9657c5fbb6536a26024851d6ef5f7bb453d013dbbd1bf92')]:
        p = root/'archives'/archive
        need(sha(p.read_bytes()) == expected, 'archive anchor')
        with tarfile.open(p,'r:gz') as t:
            members = t.getmembers(); names = [x.name for x in members]
            need(len(names) == len(set(names)) and set(names) == {x.name for x in (root/folder).iterdir()}, 'archive inventory')
            for x in members:
                need(x.isfile() and '/' not in x.name and t.extractfile(x).read() == (root/folder/x.name).read_bytes(), 'archive member')
    return len(paths)+1

def patch_replay(root):
    lines = (root/'audit/OPTIONAL_CLI_HARDENING.patch').read_text().splitlines(keepends=True)
    i = 0; patched = {}
    while i < len(lines):
        need(lines[i].startswith('--- a/'), 'patch old header')
        name = lines[i][6:].strip(); i += 1
        need(name in {'verify.py','MANIFEST.json'} and name not in patched, 'patch scope')
        need(lines[i] == '+++ b/'+name+'\n', 'patch new header'); i += 1
        original = (root/'original'/name).read_text().splitlines(keepends=True)
        output = []; pos = 0
        while i < len(lines) and lines[i].startswith('@@ '):
            m = re.fullmatch(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n',lines[i]); need(m is not None,'hunk header')
            start, oldcount, newstart, newcount = map(int,m.groups()); i += 1
            need(start-1 >= pos,'hunk overlap'); output.extend(original[pos:start-1]); pos = start-1
            oldused = newused = 0
            while i < len(lines) and not lines[i].startswith(('@@ ','--- a/')):
                line = lines[i]; i += 1; need(line[0] in ' +-','patch operation')
                if line[0] in ' -':
                    need(pos < len(original) and original[pos] == line[1:], 'patch context'); pos += 1; oldused += 1
                if line[0] in ' +':
                    output.append(line[1:]); newused += 1
            need((oldused,newused) == (oldcount,newcount),'hunk counts')
        output.extend(original[pos:]); patched[name] = ''.join(output).encode()
    need(set(patched) == {'verify.py','MANIFEST.json'}, 'two-file patch')
    with tempfile.TemporaryDirectory(prefix='ramification-patch-') as d:
        copy = pathlib.Path(d)/'accepted'; shutil.copytree(root/'original',copy)
        for name, raw in patched.items(): (copy/name).write_bytes(raw)
        for p in copy.iterdir(): need(p.read_bytes() == (root/'accepted'/p.name).read_bytes(), 'accepted copy differs')
    need((root/'original/verify.py').read_bytes().replace(b'root = Path(__file__).resolve().parent', b'root = Path(__file__).absolute().parent',1) == patched['verify.py'],'single CLI line scope')

def run(script, extra=(), optimized=False, expected=None, reject=None):
    env = dict(os.environ); env.pop('PYTHONOPTIMIZE',None); env['PYTHONDONTWRITEBYTECODE']='1'
    cmd = [sys.executable,'-B'] + (['-O'] if optimized else []) + [str(script),*extra]
    p = subprocess.run(cmd,cwd=tempfile.gettempdir(),env=env,capture_output=True,timeout=120)
    if reject is not None:
        need(p.returncode != 0 and reject.encode() in p.stderr, 'expected rejection: '+str(script))
    else:
        need(p.returncode == 0, 'replay failed: '+str(script)+' '+p.stderr.decode())
        obj = json.loads(p.stdout)
        if expected is not None: need(obj == expected, 'result mismatch: '+str(script))
    return {'script':script.name,'optimized':optimized,'returncode':p.returncode,'stdout_sha256':sha(p.stdout)}

def replay(root):
    patch_replay(root); runs = []
    for optimized in (False, True):
        for folder, anchor in [('original',ORIGINAL),('accepted',ACCEPTED)]:
            p = root/folder
            expected = {'integrity':{'result':'PASS','files':14},'mathematics':read_json(p/'CHECK_RESULTS.json')}
            runs.append(run(p/'verify.py',['--expected-manifest-sha256',anchor],optimized,expected))
            runs.append(run(p/'negative_controls.py',optimized=optimized,expected=read_json(p/'NEGATIVE_RESULTS.json')))
        p = root/'audit'
        runs.append(run(p/'independent_controls.py',optimized=optimized,expected=read_json(p/'INDEPENDENT_RESULTS.json')))
        runs.append(run(p/'packet_controls.py',['--packet',str(root/'original'),'--archive',str(root/'archives/ramification_30001278_author.tar.gz')],optimized,read_json(p/'ADVERSARIAL_RESULTS.json')))
        with tempfile.TemporaryDirectory(prefix='ramification-link-') as d:
            link = pathlib.Path(d)/'direct-root'; link.symlink_to(root/'accepted',target_is_directory=True)
            runs.append(run(link/'verify.py',['--expected-manifest-sha256',ACCEPTED],optimized,reject='packet root must not be a symlink'))
    return runs

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest-sha256',required=True)
    p.add_argument('--integrity-only',action='store_true')
    args = p.parse_args(); root = pathlib.Path(__file__).absolute().parent
    count = integrity(root,args.manifest_sha256)
    runs = [] if args.integrity_only else replay(root)
    print(json.dumps({'status':'PASS','files':count,'frozen_manifests':3,'patch_replay':not args.integrity_only,
                      'runs':runs,'scope':'Bounded checks; no full solution, formal proof, novelty or global-openness claim.'},indent=2,sort_keys=True))

if __name__ == '__main__': main()
