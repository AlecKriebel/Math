#!/usr/bin/env python3
"""Offline, fail-closed integrity check; not a mathematical proof checker."""
import ast, contextlib, hashlib, io, json, os, stat, sys
from pathlib import Path
MANIFEST_HASH = 'b4f1ee6bbebc3c6b3888f811747ad8ae2d6645401dac940564f9f3514666776c'
EXPECTED = {'ANALYSIS_MANIFEST.json': {'bytes': 1509, 'sha256': '75bfd5edfa961a6ccbc8a40f90df7dceb6e39e4a36270c604fc85fbe55f231f4'}, 'EXACT_CHECKS.json': {'bytes': 679, 'sha256': '31918c030c22b6f74c7fab705cf671fda6d832087d4f54de55b5d472a22c1f5e'}, 'EXACT_CHECKS_OPTIMIZED.json': {'bytes': 679, 'sha256': '31918c030c22b6f74c7fab705cf671fda6d832087d4f54de55b5d472a22c1f5e'}, 'FINITE_PRODUCT_CHECK.json': {'bytes': 341, 'sha256': '2cec69204f85b35b5138a520f3ccdbed854413fac82aec9e43b9e75b87f4f528'}, 'FINITE_PRODUCT_CHECK_OPTIMIZED.json': {'bytes': 341, 'sha256': '2cec69204f85b35b5138a520f3ccdbed854413fac82aec9e43b9e75b87f4f528'}, 'FINITE_PRODUCT_EXAMPLE.md': {'bytes': 1276, 'sha256': 'de845f1964cb820a0193ab935a752184cf5643d189535f5adb64b80395ecf25f'}, 'INDEPENDENT_REVIEW.md': {'bytes': 21356, 'sha256': '4866beeb3d99a9a4c0fe63af65993336c34e95dbb8d8d48c9424853eddd2c44a'}, 'README.md': {'bytes': 1627, 'sha256': 'f049a5a159352adc2c8ac5bc6b5ef6707e5cae45cc29dbe62479797d4fde150a'}, 'RECOVERY_GATE.md': {'bytes': 5948, 'sha256': '2e9a91d30881e226dbab195c15ddfd1f68c83c0280dfa1288e8ede45b56096c9'}, 'RESIDUAL_REPORT.md': {'bytes': 10442, 'sha256': 'a3007895c78780bb198abe89a78def742edaa9ff41022b91bc07b2adcc68dd80'}, 'public_source_manifest.json': {'bytes': 693, 'sha256': 'f68915c11e4ccfb6ef84390953d56485429b7c7bcd36f086e93f8343a2e70f7e'}, 'verify_exact.py': {'bytes': 2453, 'sha256': '92d10513ebc3022d8104afc299e28574476d922ef56f538b1cd36468fa602e0d'}, 'verify_finite_product.py': {'bytes': 941, 'sha256': 'abe7b239b945e1cc666bfa1f008a19c4a6c0f711bd761387741337c85b75abea'}}
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
            require(s.st_size <= 100000, 'oversized file: '+name)
            found.add(name)
    walk(absolute)
    require(found == ALLOWED, 'missing or extra files')
    return absolute

def read(root, name):
    fd = os.open(root/name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        s = os.fstat(fd)
        require(stat.S_ISREG(s.st_mode) and s.st_nlink == 1, 'unsafe file at read')
        with os.fdopen(fd, 'rb', closefd=False) as f: data = f.read(100001)
        require(len(data) <= 100000, 'file too large')
        return data
    finally: os.close(fd)

def main():
    root = inventory(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent)
    raw = read(root, 'MANIFEST.json')
    require(hashlib.sha256(raw).hexdigest() == MANIFEST_HASH, 'manifest hash mismatch')
    manifest = json.loads(raw)
    require(manifest['schema']==1 and manifest['row']==1898 and manifest['problem_id']=='20000750', 'identity mismatch')
    require(manifest['files']==EXPECTED, 'manifest inventory mismatch')
    for name, expected in EXPECTED.items():
        data = read(root,name)
        require(len(data)==expected['bytes'] and hashlib.sha256(data).hexdigest()==expected['sha256'], 'payload mismatch: '+name)
    original=json.loads(read(root,'ANALYSIS_MANIFEST.json'))
    require(original['files']=={n:EXPECTED[n] for n in original['files']}, 'inherited manifest mismatch')
    scripts={'verify_exact.py': '5b3935c2b485010df60d9f5eeacfe79445b59448180ac0adbb07f268606ba172', 'verify_finite_product.py': '61f36e05a45bc34e7baac027f68f65a9e0dd3f9ece859c7cd88acffec406dccb'}
    # Pin the entire AST, including imports, top-level code and all function bodies.
    for name, pin in scripts.items():
        source=read(root,name).decode('utf-8')
        tree=ast.parse(source,filename=name)
        require(hashlib.sha256(ast.dump(tree,include_attributes=False).encode()).hexdigest()==pin, 'whole-module AST mismatch')
        expected_name='EXACT_CHECKS.json' if name=='verify_exact.py' else 'FINITE_PRODUCT_CHECK.json'
        expected=read(root,expected_name)
        require(expected==read(root,expected_name.replace('.json','_OPTIMIZED.json')), 'saved modes differ')
        for optimization in (0,2):
            output=io.StringIO()
            with contextlib.redirect_stdout(output):
                exec(compile(tree,str(root/name),'exec',optimize=optimization), {'__name__':'__main__','__file__':str(root/name)})
            require(output.getvalue().encode()==expected, 'exact output mismatch')
    print('PASS: row 1898 exact inventory, source hashes, whole-module ASTs and normal/optimized outputs; partial mathematics only.')

if __name__ == '__main__':
    try: main()
    except Exception as exc:
        print('FAIL: '+str(exc), file=sys.stderr)
        sys.exit(1)
