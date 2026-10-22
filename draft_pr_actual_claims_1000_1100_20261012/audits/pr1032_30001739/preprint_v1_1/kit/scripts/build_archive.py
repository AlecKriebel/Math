#!/usr/bin/env python3
"""Build a canonical ZIP at a NEW output physically outside the exact kit tree.

Example from kit cwd: python3 scripts/build_archive.py /existing/real/output/new.zip
The output parent must already exist. Neither '..' nor symlink ancestors are
accepted. This is a static-filesystem boundary check, not a race-proof sandbox.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import os
import stat
import zipfile

def require(value, message):
    if not value:
        raise RuntimeError(message)

def lexical_absolute(value):
    raw = os.fspath(value)
    require(bool(raw) and '\x00' not in raw, 'empty or invalid path')
    path = Path(raw)
    require('..' not in path.parts, 'parent traversal is not accepted')
    return path if path.is_absolute() else Path.cwd() / path

def real_directory_chain(path):
    """lstat every existing ancestor; never resolve a symlink implicitly."""
    require(path.is_absolute(), 'internal absolute path required')
    current = Path(path.anchor)
    chain = []
    for part in (None, *path.parts[1:]):
        if part is not None:
            current = current / part
        try:
            info = current.lstat()
        except OSError as exc:
            raise RuntimeError('existing real directory parent required: ' + str(current)) from exc
        require(stat.S_ISDIR(info.st_mode), 'non-directory or symlink ancestor: ' + str(current))
        chain.append((info.st_dev, info.st_ino))
    return chain

def output_preflight(root, target):
    root = lexical_absolute(root)
    root_ids = real_directory_chain(root)
    target = lexical_absolute(target)
    # lstat catches existing files, directories, symlinks, dangling symlinks,
    # and hardlink aliases without following any of them.
    try:
        target.lstat()
    except FileNotFoundError:
        pass
    except OSError as exc:
        raise RuntimeError('invalid output path') from exc
    else:
        raise RuntimeError('output must be new; refusing any existing object')
    parent_ids = real_directory_chain(target.parent)
    # Inodes detect physical containment when either path has a case alias.
    require(root_ids[-1] not in parent_ids, 'output must be physically outside kit')
    return root, target

def valid_member(name):
    if not isinstance(name, str) or not name or '\\' in name:
        return False
    path = PurePosixPath(name)
    return not path.is_absolute() and '..' not in path.parts and path.as_posix() == name

def frozen_contents(root):
    """Validate the complete allowlisted regular tree before any output write."""
    actual = {}
    for parent, directories, files in os.walk(root, followlinks=False):
        for name in directories:
            path = Path(parent) / name
            require(stat.S_ISDIR(path.lstat().st_mode), 'symlink or non-directory member ancestry')
        for name in files:
            path = Path(parent) / name
            require(stat.S_ISREG(path.lstat().st_mode), 'non-regular member')
            actual[path.relative_to(root).as_posix()] = path
    require('ALLOWLIST.json' in actual and 'MANIFEST.json' in actual, 'missing inventories')
    allow = json.loads(actual['ALLOWLIST.json'].read_text())['files']
    require(isinstance(allow, list) and all(valid_member(n) for n in allow), 'invalid allowlist member')
    require(allow == sorted(set(allow)), 'allowlist duplicate/order')
    require(set(actual) == set(allow), 'actual members differ from exact allowlist')
    manifest = json.loads(actual['MANIFEST.json'].read_text())['files']
    require(isinstance(manifest, list), 'invalid content manifest')
    require(len(manifest) == len(allow)-1, 'manifest row count')
    require(all(isinstance(r,dict) and valid_member(r.get('path')) for r in manifest), 'invalid manifest path')
    require(len({r['path'] for r in manifest}) == len(manifest), 'duplicate manifest row')
    require({r['path'] for r in manifest} == set(allow)-{'MANIFEST.json'}, 'manifest member mismatch')
    contents = {name: actual[name].read_bytes() for name in allow}
    for entry in manifest:
        data = contents[entry['path']]
        require(type(entry.get('bytes')) is int and entry['bytes'] == len(data), 'member byte length mismatch')
        require(entry.get('sha256') == hashlib.sha256(data).hexdigest(), 'member content mismatch: ' + entry['path'])
    return contents

def build(root, target):
    root, target = output_preflight(root, target)
    contents = frozen_contents(root)
    # Exclusive output creation is the first write. Supplied bytes were
    # completely checked and captured in memory under the static-tree assumption.
    with zipfile.ZipFile(target, 'x') as archive:
        for name, data in contents.items():
            entry = zipfile.ZipInfo(name, (2026,10,16,0,0,0))
            entry.create_system = 3
            entry.external_attr = (stat.S_IFREG|0o644) << 16
            entry.compress_type = zipfile.ZIP_STORED
            archive.writestr(entry, data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', help='new file outside kit, with existing real parent; no .. or symlink ancestors')
    args = parser.parse_args()
    build(Path(__file__).absolute().parents[1], args.target)
