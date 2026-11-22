#!/usr/bin/env python3
"""Offline, fail-closed integrity check; not a mathematical proof checker."""
import hashlib, json, os, stat, sys
from pathlib import Path
MANIFEST_HASH = '5091fd26e8ba2f24dc5ee8fdfbd869079c16709a623932ae7151b72c232974d3'
EXPECTED = {'INDEPENDENT_ACCEPTANCE.md': {'bytes': 6071, 'sha256': '7d52ae6068e3e319b4161fdd26466dce3addb880fa28c486c897ac47b10b64ea'}, 'ORIGINAL_MANIFEST.json': {'bytes': 593, 'sha256': 'c9c8c6f82741441f0377bb2860decd4903a27f9b921bb0b37aa04759140aba61'}, 'ETALE_AUDIT.md': {'bytes': 12061, 'sha256': '38e6b3e8f614a8c29a635b249556084bb7606ca2c0043bea37f2a97d7bbdb359'}, 'README.md': {'bytes': 1645, 'sha256': '9f91f7c731200b2bfdf9845c9298fac6525b96d8896a4ee1c2a67ba1bd143680'}}
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
    require(manifest['schema']==1 and manifest['row']==1896 and manifest['problem_id']=='20000162', 'identity mismatch')
    require(manifest['files']==EXPECTED, 'manifest inventory mismatch')
    for name, expected in EXPECTED.items():
        data = read(root,name)
        require(len(data)==expected['bytes'] and hashlib.sha256(data).hexdigest()==expected['sha256'], 'payload mismatch: '+name)
    original=json.loads(read(root,'ORIGINAL_MANIFEST.json'))
    require(original['files']==[dict(path=n, **EXPECTED[n]) for n in ['ETALE_AUDIT.md','INDEPENDENT_ACCEPTANCE.md']], 'original provenance mismatch')
    print('PASS: exact frozen inventory and inherited provenance; analytic proofs are not machine-certified.')

if __name__ == '__main__':
    try: main()
    except Exception as exc:
        print('FAIL: '+str(exc), file=sys.stderr)
        sys.exit(1)
