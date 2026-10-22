"""Strict closed-inventory verifier. Only the root MANIFEST.json is exempt."""
from pathlib import Path
import hashlib
import json
import stat


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def verify(root):
    root = Path(root)
    require(not root.is_symlink(), 'Root symlink')
    manifest = root / 'MANIFEST.json'
    require(not manifest.is_symlink() and manifest.is_file(), 'Invalid root manifest')
    data = json.loads(manifest.read_text(), object_pairs_hook=unique_object)
    require(set(data) == {'schema', 'files'} and data['schema'] == 1, 'Invalid schema')
    require(isinstance(data['files'], list), 'Invalid inventory')
    expected = {}
    for item in data['files']:
        require(set(item) == {'path', 'bytes', 'sha256'}, 'Invalid record')
        name = item['path']
        require(isinstance(name, str) and name and '\\' not in name, 'Invalid path')
        parts = name.split('/')
        require(all(x not in ('', '.', '..') for x in parts), 'Unsafe path')
        require(name != 'MANIFEST.json' and name not in expected, 'Duplicate/exempt record')
        require(type(item['bytes']) is int and item['bytes'] >= 0, 'Invalid size')
        digest = item['sha256']
        require(isinstance(digest,str) and len(digest)==64 and all(c in '0123456789abcdef' for c in digest), 'Invalid hash')
        expected[name] = item
    actual = {}
    directories = set()
    def walk(directory):
        for entry in directory.iterdir():
            mode = entry.lstat().st_mode
            require(not stat.S_ISLNK(mode), 'Symlink forbidden: '+str(entry))
            relative = entry.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                directories.add(relative)
                walk(entry)
            else:
                require(stat.S_ISREG(mode), 'Nonregular file: '+relative)
                if relative != 'MANIFEST.json':
                    actual[relative] = entry
    walk(root)
    require(set(actual) == set(expected), 'Inventory mismatch')
    expected_dirs = {str(parent) for name in expected for parent in Path(name).parents if str(parent) != '.'}
    require(directories == expected_dirs, 'Directory inventory mismatch')
    for name, entry in actual.items():
        content = entry.read_bytes()
        require(len(content) == expected[name]['bytes'], 'Size mismatch: '+name)
        require(hashlib.sha256(content).hexdigest() == expected[name]['sha256'], 'Hash mismatch: '+name)
    return len(actual)


if __name__ == '__main__':
    print(json.dumps({'verified_files': verify(Path(__file__).resolve().parent), 'status':'PASS'}, sort_keys=True))
