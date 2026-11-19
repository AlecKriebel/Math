"""Strict offline artifact and diagnostic replay. Requires CPython and mpmath 1.3.0."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

FILES = {'ACCEPTANCE_REPORT.md', 'ADAPTIVE_IDENTITY_CHECK.json', 'ADVERSARIAL_REVIEW.md',
         'CHECK_ADAPTIVE_IDENTITY.py', 'MATHEMATICAL_AUDIT.md', 'VERIFICATION.json',
         'SOURCE_METADATA.json', 'PROVENANCE.json', 'README.md', 'replay.py', 'mutation_tests.py',
         'MANIFEST.json'}

def require(test, message):
    if not test:
        raise RuntimeError(message)

def inventory(root):
    # No content is opened until every directory entry, including manifest, is lstat checked.
    st = root.lstat()
    require(stat.S_ISDIR(st.st_mode) and not stat.S_ISLNK(st.st_mode), 'root must be a real directory')
    found = {}
    for entry in os.scandir(root):
        s = entry.stat(follow_symlinks=False)
        require(stat.S_ISREG(s.st_mode), 'non-regular entry: ' + entry.name)
        require(s.st_nlink == 1, 'hard link rejected: ' + entry.name)
        found[entry.name] = s
    require(set(found) == FILES, 'inventory mismatch')
    return found

def read(root, name, snapshot):
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    fd = os.open(root/name, flags)
    try:
        now = os.fstat(fd)
        old = snapshot[name]
        require(stat.S_ISREG(now.st_mode) and now.st_nlink == 1, 'unsafe opened file')
        require((now.st_dev, now.st_ino, now.st_size, now.st_mtime_ns) ==
                (old.st_dev, old.st_ino, old.st_size, old.st_mtime_ns), 'file changed after inventory')
        with os.fdopen(fd, 'rb', closefd=False) as handle:
            return handle.read()
    finally:
        os.close(fd)

def unique(pairs):
    result = {}
    for k, v in pairs:
        require(k not in result, 'duplicate JSON key')
        result[k] = v
    return result

def parse(data):
    return json.loads(data, object_pairs_hook=unique)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    root = Path(__file__).absolute().parent
    snap = inventory(root)
    manifest = parse(read(root, 'MANIFEST.json', snap))
    require(set(manifest) == {'schema', 'row', 'id', 'files'}, 'manifest keys')
    for key, value in [('schema', 1), ('row', 1909), ('id', 30001941)]:
        require(type(manifest[key]) is int and manifest[key] == value, 'exact integer required: '+key)
    require(type(manifest['files']) is dict and set(manifest['files']) == FILES-{'MANIFEST.json'}, 'manifest file set')
    payload = {}
    for name in sorted(FILES-{'MANIFEST.json'}):
        record = manifest['files'][name]
        require(type(record) is dict and set(record) == {'bytes', 'sha256'}, 'file record keys')
        require(type(record['bytes']) is int and record['bytes'] >= 0, 'exact byte integer required')
        require(type(record['sha256']) is str and re.fullmatch('[0-9a-f]{64}', record['sha256']) is not None, 'digest schema')
        data = read(root, name, snap)
        require(len(data) == record['bytes'] and sha(data) == record['sha256'], 'content mismatch: '+name)
        payload[name] = data
    provenance = parse(payload['PROVENANCE.json'])
    code = payload['CHECK_ADAPTIVE_IDENTITY.py']
    tree = ast.parse(code)
    require(not any(isinstance(n, ast.Assert) for n in ast.walk(tree)), 'assert found')
    require(provenance['source_sha256'] == sha(code) == provenance['frozen_sha256'], 'byte provenance mismatch')
    require(provenance['whole_module_ast_sha256'] == sha(ast.dump(tree, include_attributes=False).encode()), 'whole-module AST mismatch')
    import mpmath
    require(mpmath.__version__ == '1.3.0', 'requires mpmath 1.3.0 for exact diagnostic output')
    outputs = []
    for flags in [[], ['-O']]:
        proc = subprocess.run([sys.executable, *flags, '-B', '-c', compile_source(code)], capture_output=True, timeout=30)
        require(proc.returncode == 0, 'diagnostic execution failed')
        require(proc.stdout == payload['ADAPTIVE_IDENTITY_CHECK.json'], 'exact diagnostic output mismatch')
        outputs.append(sha(proc.stdout))
    print(json.dumps({'status':'PASS', 'row':1909, 'id':30001941, 'normal_output_sha256':outputs[0],
                      'optimized_output_sha256':outputs[1], 'manifest_sha256':sha(read(root,'MANIFEST.json',snap)),
                      'scope':'Artifact integrity and one smooth-profile diagnostic, not a PDE proof or novelty certificate'}, indent=2))

def compile_source(code):
    return code.decode('utf-8')

if __name__ == '__main__':
    main()
