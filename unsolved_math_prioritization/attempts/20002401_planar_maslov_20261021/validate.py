#!/usr/bin/env python3
"""Offline, fail-closed integrity check; not a mathematical proof checker."""
import ast, contextlib, hashlib, io, json, os, stat, sys
from pathlib import Path
MANIFEST_HASH = '8dbb2deb1ade921b6726cc934f452dae5396b056230c220fbc463df9e471e1ca'
EXPECTED = {'CHECK.py': {'bytes': 2263, 'sha256': '899f4f27366dface71624f4472cfff39bfdae8709b22e83d4698db2becc76846'}, 'CHECK_RESULT.json': {'bytes': 813, 'sha256': '957059e0110d1499090eade39093c04af710a962f73ce2fd71a7d0989f71a8f1'}, 'CHECK_RESULT_OPTIMIZED.json': {'bytes': 813, 'sha256': '957059e0110d1499090eade39093c04af710a962f73ce2fd71a7d0989f71a8f1'}, 'INDEPENDENT_REVIEW.md': {'bytes': 9404, 'sha256': 'edcfd96334707db1e2a2c64304edddf7f2b7fff2876e01aadba5b0409edf7664'}, 'ORIGINAL_AUDIT_RECEIPT.json': {'bytes': 1041, 'sha256': '578a13093154ab829f23ba459a348a9e1fe4d45f128173eabf1cf816c7251128'}, 'PDF_METADATA.json': {'bytes': 549, 'sha256': 'fe96949002d728f45b84c9b4ef9b0eee3294beb7a2e90b3d4ce3f3d9b8d835a7'}, 'PUBLIC_PROJECTION.md': {'bytes': 1987, 'sha256': '4cecca3ef18f54182799d477bbbe40e4a14ca1f7367502c015ff1618ccb14cd2'}, 'README.md': {'bytes': 1765, 'sha256': 'cfa2fcef2161c18dd46a627f78330570577b402290ae52edfdaf9391099c0c43'}, 'REPORT.md': {'bytes': 13038, 'sha256': 'fc7209e944888839101fffe93a2dc743391410d32f014cb1d72ae7b0e1c2a537'}, 'SOURCE_GATE.md': {'bytes': 4956, 'sha256': 'a76467cb7ae42ad24040743e5116454783fb3b196a1d01659e3abd6c00e81b1e'}, 'checker_original.txt': {'bytes': 2263, 'sha256': '899f4f27366dface71624f4472cfff39bfdae8709b22e83d4698db2becc76846'}, 'public_source_manifest.json': {'bytes': 1394, 'sha256': '1018e251ee683dffbd245e3a7f88c5a6816955de672380e188538bd9cd5314a9'}}
ALLOWED = set(EXPECTED) | {'MANIFEST.json', 'validate.py'}

def no_sockets(event, args):
    if event.startswith('socket.'):
        raise PermissionError('socket use denied')
sys.addaudithook(no_sockets)
sys.dont_write_bytecode = True

def require(ok, message):
    if not ok: raise ValueError(message)

def inventory(root):
    # Check every ancestor without resolving symlinks.
    absolute = Path(os.path.abspath(root))
    for p in reversed([absolute, *absolute.parents]):
        s = os.lstat(p)
        require(stat.S_ISDIR(s.st_mode), 'unsafe root/ancestor')
    found = set()
    def walk(directory, prefix=''):
        for entry in os.scandir(directory):
            name = prefix + entry.name
            s = entry.stat(follow_symlinks=False)
            require(not stat.S_ISLNK(s.st_mode), 'symlink rejected: '+name)
            require(stat.S_ISREG(s.st_mode) or stat.S_ISDIR(s.st_mode), 'special file rejected: '+name)
            if stat.S_ISDIR(s.st_mode):
                # Every directory is forbidden in this flat frozen format.
                raise ValueError('unexpected directory: '+name)
            require(s.st_nlink == 1, 'hard link rejected: '+name)
            require(name in ALLOWED, 'unexpected file: '+name)
            require(s.st_size <= 1000000, 'oversized file: '+name)
            found.add(name)
    walk(absolute)
    require(found == ALLOWED, 'missing or extra files')
    return absolute

def read(root, name):
    fd = os.open(root/name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        s = os.fstat(fd)
        require(stat.S_ISREG(s.st_mode) and s.st_nlink == 1, 'unsafe file at read')
        with os.fdopen(fd, 'rb', closefd=False) as f: data = f.read(1000001)
        require(len(data) <= 1000000, 'file too large')
        return data
    finally: os.close(fd)

def main():
    root = inventory(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent)
    raw = read(root, 'MANIFEST.json')
    require(hashlib.sha256(raw).hexdigest() == MANIFEST_HASH, 'manifest hash mismatch')
    manifest = json.loads(raw)
    require(manifest['schema']==1 and manifest['row']==1900 and manifest['problem_id']=='20002401', 'identity mismatch')
    require(manifest['files']==EXPECTED, 'manifest inventory mismatch')
    for name, expected in EXPECTED.items():
        data = read(root,name)
        require(len(data)==expected['bytes'] and hashlib.sha256(data).hexdigest()==expected['sha256'], 'payload mismatch: '+name)
    original = read(root,'checker_original.txt').decode()
    source = read(root,'CHECK.py').decode()
    tree = ast.parse(source)
    require(ast.dump(ast.parse(original),include_attributes=False)==ast.dump(tree,include_attributes=False), 'whole-module transformation provenance mismatch')
    require(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)), 'unhardened assertion')
    expected=read(root,'CHECK_RESULT.json')
    require(expected==read(root,'CHECK_RESULT_OPTIMIZED.json'), 'saved modes differ')
    for optimization in (0,1,2):
        output=io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(compile(tree,str(root/'CHECK.py'),'exec',optimize=optimization), {'__name__':'__main__','__file__':str(root/'CHECK.py')})
        require(output.getvalue().encode()==expected, 'complete exact output mismatch')
    print('PASS: row 1900 exact inventory, source hashes, whole-module ASTs and normal/optimized outputs; partial mathematics only.')

if __name__ == '__main__':
    try: main()
    except Exception as exc:
        print('FAIL: '+str(exc), file=sys.stderr)
        sys.exit(1)
