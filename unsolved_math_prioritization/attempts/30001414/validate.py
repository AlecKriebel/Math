#!/usr/bin/env python3
"""Offline, fail-closed integrity check; not a mathematical proof checker."""
import hashlib, json, os, stat, sys
from pathlib import Path
MANIFEST_HASH = 'cb6bf90f28284f6a8b861a15552e99a4cc4f62abf1072ea3a9d2829bc8fe7ead'
EXPECTED = {'BOUNDARY_CONSTANTS_ANALYSIS.md': {'bytes': 19599, 'sha256': '9c1dd546f3d91c937aa349eec3433e86eb5f34f1bae1c972153bd706325385ec'}, 'INDEPENDENT_AUDIT.md': {'bytes': 14356, 'sha256': 'b5796c5f952332bded9ef97efda676e65d84f57828d4a36b42e2325a720f15a7'}, 'LOCAL_THIRD_ORDER_HARDY.md': {'bytes': 6255, 'sha256': 'd349a175b5cbbf65aa489b4ba8643ec72132101599394f7eb0d8a07ea7ad7b53'}, 'PUBLIC_SOURCE_METADATA.json': {'bytes': 805, 'sha256': '2bf4d95a8897b5259f27cb22ee34f41e655b25a8fbcfff3acb436525eb544050'}, 'README.md': {'bytes': 2757, 'sha256': '5fe499af5f5fc40ffedff4b22797374431dc37252ffcb67f7f9cdd27f7236450'}, 'SOURCE_GATE.md': {'bytes': 5444, 'sha256': '492f2ad4bd4120952c1142a023c716f98a25f55427443fc7464ffc95d0d6e09d'}}
ALLOWED = set(EXPECTED) | {'MANIFEST.json', 'validate.py'}

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
    require(manifest['schema']==1 and manifest['row']==1878 and manifest['problem_id']=='30001414', 'identity mismatch')
    require(manifest['files']==EXPECTED, 'manifest inventory mismatch')
    for name, expected in EXPECTED.items():
        data = read(root,name)
        require(len(data)==expected['bytes'] and hashlib.sha256(data).hexdigest()==expected['sha256'], 'payload mismatch: '+name)
    sources = json.loads(read(root,'PUBLIC_SOURCE_METADATA.json'))
    require(len(sources)==2, 'source metadata mismatch')
    for source in sources:
        require(source['url'].startswith('https://') and len(source['sha256'])==64 and source['bytes']>0, 'invalid public metadata')
    print('PASS: exact frozen inventory and inherited provenance; analytic proofs are not machine-certified.')

if __name__ == '__main__':
    try: main()
    except Exception as exc:
        print('FAIL: '+str(exc), file=sys.stderr)
        sys.exit(1)
