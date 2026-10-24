#!/usr/bin/env python3
"""Offline, fail-closed integrity check; not a mathematical proof checker."""
import hashlib, json, os, stat, sys
from pathlib import Path
MANIFEST_HASH = 'b6c6c032334467d5439f3a446ecd87a8ff469bcb6547ea2e05dad62369f6ab8e'
EXPECTED = {'AUDIT.md': {'bytes': 16247, 'sha256': 'fb7c9e575ab599630c234e1ecbb6ee11154101b50937624728bba9167cbbaf9d'}, 'README.md': {'bytes': 1349, 'sha256': '9610ab6d3b11ea6d9c1f18ebb99363522fbd6e546aa560f34080b3a5f0241668'}, 'RECOVERY_PUBLIC.md': {'bytes': 3700, 'sha256': 'e1cfa6bd1cb4020c3d803753519644ff9abfec3229ff6173ebf694649786dff9'}, 'REVIEW.md': {'bytes': 4784, 'sha256': '050e15e58f5ee59b4bf7307039dbb050757478a1aa84e6e18bd3426b340ddba4'}, 'verification_manifest.json': {'bytes': 1100, 'sha256': '1e4ff95f2856739c87bda9d85f18497e8011af563929e8a180ccd7d61ac53df4'}}
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
    require(manifest['schema']==1 and manifest['row']==1897 and manifest['problem_id']=='20000726', 'identity mismatch')
    require(manifest['files']==EXPECTED, 'manifest inventory mismatch')
    for name, expected in EXPECTED.items():
        data = read(root,name)
        require(len(data)==expected['bytes'] and hashlib.sha256(data).hexdigest()==expected['sha256'], 'payload mismatch: '+name)
    original=json.loads(read(root,'verification_manifest.json'))
    require(original['authored_audit']==dict(file='AUDIT.md', **EXPECTED['AUDIT.md']), 'original provenance mismatch')
    print('PASS: exact frozen inventory and inherited provenance; analytic proofs are not machine-certified.')

if __name__ == '__main__':
    try: main()
    except Exception as exc:
        print('FAIL: '+str(exc), file=sys.stderr)
        sys.exit(1)
