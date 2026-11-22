#!/usr/bin/env python3
"""Offline, fail-closed integrity check; not a mathematical proof checker."""
import ast, contextlib, hashlib, io, json, os, stat, sys
from pathlib import Path
MANIFEST_HASH = '301eb5e24361b00470a825ad3dbe11a243eb6664d22d0f6bce54ae1b0353f47c'
EXPECTED = {'EXACT_CHECKS.txt': {'bytes': 250, 'sha256': '124636c3bd6824df123cd28722451d21a940877957ab1ffd420fd230c321f0ab'}, 'EXACT_CHECKS_OPTIMIZED.txt': {'bytes': 250, 'sha256': '124636c3bd6824df123cd28722451d21a940877957ab1ffd420fd230c321f0ab'}, 'INDEPENDENT_REVIEW.md': {'bytes': 5641, 'sha256': 'f6d4615e9bc860ea4438cab3b9f57a5b85925574207113f5c46b22f2a90abc74'}, 'ORIGINAL_AUDIT_RECEIPT.json': {'bytes': 2054, 'sha256': '9fdd5074836d4b578e987aceb9527ead27dc674c43c7c0c313408c05ee66d468'}, 'README.md': {'bytes': 1902, 'sha256': '0a2116a0f2e6608cce4b95c5cd64bbac75f208793ec8fb13053d23a118ba5c6c'}, 'REPORT.md': {'bytes': 10237, 'sha256': '0205fc9137b0ce9e65d9fbdcd952bb759f58912292825ce9e9961082e796fce5'}, 'SOURCE_GATE.md': {'bytes': 1940, 'sha256': '70c4808a398148e4d6dc35946f588a13bb11be03a41468d8a4be9c40903b1764'}, 'exact_zero_fiber.json': {'bytes': 1059, 'sha256': '72ddab66ef648d9346cfe84606c700e89a8c5a786892f9b811ebe0e1c499a90c'}, 'padding_family.json': {'bytes': 6621, 'sha256': '46f25ade0b7559a64b99bbd30f2223e10331ea07ce5bc64262fa21073ad49a8f'}, 'probe_results.json': {'bytes': 348200, 'sha256': '0207e886524a0c1c2e14cc74c1af5d8c16706d7f40afe626a486abcdbb3c47dd'}, 'public_source_manifest.json': {'bytes': 1007, 'sha256': '75d2387acb98975125aed03b1900a147ed7ffe5373f15138a41c397df6316e06'}, 'verifier_original.txt': {'bytes': 3183, 'sha256': '320d58732b41804cc4bea19bc1e846dd48e414cf2f851532c9960e21d1213cdb'}, 'verify_exact.py': {'bytes': 5412, 'sha256': '7c7de4bb1fe8b9b1bfcfbdef6d2c93c0b41cfb652325593ad5b61fc457bcf5b0'}}
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

def transform_original(source):
    tree = ast.parse(source)
    class Harden(ast.NodeTransformer):
        def visit_Assert(self, node):
            return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(), operand=node.test), body=[ast.Raise(exc=ast.Call(func=ast.Name(id='RuntimeError', ctx=ast.Load()), args=[ast.Constant(value='exact mathematical check failed at original line '+str(node.lineno))], keywords=[]), cause=None)], orelse=[]), node)
        def visit_Assign(self, node):
            if any(isinstance(t, ast.Name) and t.id == 'src' for t in node.targets):
                return ast.copy_location(ast.parse("src=Path(__file__).parent").body[0], node)
            return self.generic_visit(node)
    return ast.fix_missing_locations(Harden().visit(tree))

def main():
    root = inventory(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent)
    raw = read(root, 'MANIFEST.json')
    require(hashlib.sha256(raw).hexdigest() == MANIFEST_HASH, 'manifest hash mismatch')
    manifest = json.loads(raw)
    require(manifest['schema']==1 and manifest['row']==1899 and manifest['problem_id']=='20001232', 'identity mismatch')
    require(manifest['files']==EXPECTED, 'manifest inventory mismatch')
    for name, expected in EXPECTED.items():
        data = read(root,name)
        require(len(data)==expected['bytes'] and hashlib.sha256(data).hexdigest()==expected['sha256'], 'payload mismatch: '+name)
    original = read(root,'verifier_original.txt').decode()
    source = read(root,'verify_exact.py').decode()
    tree = ast.parse(source)
    require(ast.dump(transform_original(original),include_attributes=False)==ast.dump(tree,include_attributes=False), 'whole-module transformation provenance mismatch')
    require(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)), 'unhardened assertion')
    expected=read(root,'EXACT_CHECKS.txt')
    require(expected==read(root,'EXACT_CHECKS_OPTIMIZED.txt'), 'saved modes differ')
    for optimization in (0,1,2):
        output=io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(compile(tree,str(root/'verify_exact.py'),'exec',optimize=optimization), {'__name__':'__main__','__file__':str(root/'verify_exact.py')})
        require(output.getvalue().encode()==expected, 'complete exact output mismatch')
    print('PASS: row 1899 exact inventory, source hashes, whole-module ASTs and normal/optimized outputs; partial mathematics only.')

if __name__ == '__main__':
    try: main()
    except Exception as exc:
        print('FAIL: '+str(exc), file=sys.stderr)
        sys.exit(1)
