#!/usr/bin/env python3
"""Close the acquisition packet; execution uses only this task's own code."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat

ROOT = Path(__file__).resolve().parent
RESERVED = {'FREEZE_MANIFEST.json', 'TERMINAL.json'}

def digests(p):
    b = p.read_bytes()
    return dict(bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), md5=hashlib.md5(b).hexdigest())

def inventory():
    entries = []
    inode_paths = {}
    def visit(p):
        relative = '.' if p == ROOT else p.relative_to(ROOT).as_posix()
        if relative in RESERVED:
            return
        s = p.lstat()
        e = dict(path=relative, mode=oct(stat.S_IMODE(s.st_mode)))
        if stat.S_ISDIR(s.st_mode):
            children = sorted(p.iterdir(), key=lambda c:c.name)
            e.update(type='directory', children=[c.name for c in children if not (p == ROOT and c.name in RESERVED)])
            e['empty'] = len(children) == 0
            entries.append(e)
            for c in children:
                visit(c)
        elif stat.S_ISREG(s.st_mode):
            e.update(type='regular_file', link_count=s.st_nlink, **digests(p))
            inode_paths.setdefault((s.st_dev, s.st_ino), []).append(relative)
            entries.append(e)
        elif stat.S_ISLNK(s.st_mode):
            e.update(type='symlink', target=os.readlink(p))
            entries.append(e)
        else:
            raise RuntimeError('Unexpected special entry: '+relative)
    visit(ROOT)
    return entries, sorted([sorted(v) for v in inode_paths.values() if len(v)>1])

if __name__ == '__main__':
    if any((ROOT/n).exists() for n in RESERVED):
        raise SystemExit('Already frozen; do not overwrite closure artifacts.')
    entries, groups = inventory()
    manifest = dict(format='finite-source-acquisition-v1', frozen_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), root=str(ROOT), source_only_completion_percent=100,
                    scope='source acquisition and edition/integrity qualification only; no mathematical conclusions',
                    enumeration='Recursive lstat; includes hidden and empty entries; never follows symlinks. Root children exclude exactly the two reserved closure files, added explicitly by terminal.',
                    reserved_closure_files=sorted(RESERVED), entries=entries, hardlink_groups=groups)
    manifest_path = ROOT/'FREEZE_MANIFEST.json'
    manifest_path.write_text(json.dumps(manifest, indent=2)+'\n')
    total_files = sum(e['type']=='regular_file' for e in entries)+2
    total_dirs = sum(e['type']=='directory' for e in entries)
    terminal = dict(format='finite-source-acquisition-terminal-v1', status='source-only complete and frozen', source_only_completion_percent=100,
                    manifest=dict(path='FREEZE_MANIFEST.json', mode=oct(stat.S_IMODE(manifest_path.stat().st_mode)), **digests(manifest_path)),
                    terminal_self=dict(path='TERMINAL.json', expected_mode='0o644', sha256='External pin reported to task owner; self-reference deliberately excluded.'),
                    exact_entry_paths=sorted([e['path'] for e in entries]+sorted(RESERVED)),
                    regular_files_including_closure=total_files, directories_including_root=total_dirs,
                    symlinks=sum(e['type']=='symlink' for e in entries), empty_directories=[e['path'] for e in entries if e['type']=='directory' and e['empty']],
                    hidden_entries=[e['path'] for e in entries if any(x.startswith('.') and x!='.' for x in Path(e['path']).parts)], hardlink_groups=groups,
                    closure_policy='All entries are explicitly enumerated. Exactly the two reserved root closure files are outside the payload inventory; manifest is pinned here, terminal is pinned externally. Any extra, missing, modified, retyped or remoded entry invalidates this closure.')
    terminal_path = ROOT/'TERMINAL.json'
    terminal_path.write_text(json.dumps(terminal, indent=2)+'\n')
    after, after_groups = inventory()
    assert after == entries and after_groups == groups
    actual_paths = sorted(['.']+[x.relative_to(ROOT).as_posix() for x in ROOT.rglob('*')])
    assert actual_paths == terminal['exact_entry_paths']
    assert oct(stat.S_IMODE(terminal_path.stat().st_mode)) == terminal['terminal_self']['expected_mode']
    print(json.dumps(dict(terminal=digests(terminal_path), manifest=digests(manifest_path), files=total_files, directories_including_root=total_dirs, payload_file_count=total_files-2, verified=True), indent=2))
