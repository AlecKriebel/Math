"""Strict read paths, fresh output paths and deterministic closed ZIP bytes."""
import sys
sys.dont_write_bytecode = True
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import zipfile

ROOT = Path(__file__).resolve().parent.parent
ORIGINAL = Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1098_3000018')

def require(value, message):
    if not value:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def raw_absolute(value):
    p = Path(value)
    require(p.is_absolute(), 'absolute path required')
    require('..' not in p.parts, 'parent traversal rejected before resolution')
    return p

def no_links(path):
    for p in (path, *path.parents):
        require(not p.is_symlink(), 'symlink leaf/ancestor rejected: '+str(p))

def regular(path):
    p = raw_absolute(path)
    no_links(p)
    info = p.lstat()
    require(stat.S_ISREG(info.st_mode), 'regular file required: '+str(p))
    require(info.st_nlink == 1, 'hardlinked input rejected: '+str(p))
    return p

def load(path):
    p = regular(path)  # Bootstrap validation occurs BEFORE any JSON parsing.
    def unique(pairs):
        result = {}
        for k, v in pairs:
            require(k not in result, 'duplicate JSON key: '+k)
            result[k] = v
        return result
    return json.loads(p.read_text(encoding='utf-8'), object_pairs_hook=unique)

def member(value):
    p = Path(value)
    require(not p.is_absolute() and p.parts and '..' not in p.parts,
            'relative safe member required')
    return regular(ROOT/p)

def fresh(value):
    p = raw_absolute(value)
    no_links(p)
    require(not p.exists(), 'output leaf must be absent')
    require(p.parent.is_dir(), 'existing real output parent required')
    for ancestor in (p.parent, *p.parent.parents):
        no_links(ancestor)
        for protected in (ROOT, ORIGINAL):
            # Compare directory identities, not case-sensitive spellings.
            if protected.exists():
                require(not os.path.samefile(ancestor, protected),
                        'output is inside physical protected root')
    # Keep lexical containment too, including a temporarily absent origin.
    for protected in (ROOT, ORIGINAL):
        require(p != protected and protected not in p.parents,
                'output is inside lexical protected root')
    return p

def write_new(path, data):
    p = fresh(path)
    with p.open('xb') as stream:
        stream.write(data)

def archive_bytes():
    manifest = load(ROOT/'MANIFEST.json')
    records = manifest['entries']
    names = [r['path'] for r in records]
    require(names == sorted(set(names)), 'manifest must be sorted and unique')
    payload = {}
    for r in records:
        raw = member(r['path']).read_bytes()
        require(len(raw) == r['bytes'] and digest(raw) == r['sha256'],
                'payload binding mismatch: '+r['path'])
        payload[r['path']] = raw
    payload['MANIFEST.json'] = regular(ROOT/'MANIFEST.json').read_bytes()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_STORED) as z:
        for name in sorted(payload):
            info = zipfile.ZipInfo(name, (2026, 10, 16, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, payload[name])
    return buffer.getvalue()  # AFTER ZipFile.close writes the central directory.
