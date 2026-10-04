"""Verify reviewed live files, staged blobs and the actual committed tree."""
from pathlib import Path
import hashlib, stat

def live_pins(root, expected):
    for rel, e in expected.items():
        p = Path(root)/rel
        assert p.is_file() and not p.is_symlink(), rel
        b = p.read_bytes()
        actual = dict(bytes=len(b), sha256=hashlib.sha256(b).hexdigest(),
            mode=format(stat.S_IMODE(p.stat().st_mode), '04o'))
        assert actual == e, ('Reviewed live file changed', rel)

def tree_pins(git, tree, base, expected):
    changed = set(git('diff', '--name-only', '-z', base, tree).split(b'\0')) - {b''}
    assert changed <= {x.encode() for x in expected}, 'Unreviewed path in tree'
    for rel, e in expected.items():
        b = git('show', tree+':'+rel)
        assert len(b) == e['bytes'] and hashlib.sha256(b).hexdigest() == e['sha256'], ('Reviewed blob changed', rel)
        entry = git('ls-tree', '-z', tree, '--', rel).rstrip(b'\0').split(b'\t')
        assert len(entry) == 2 and entry[1] == rel.encode()
        mode, kind, oid = entry[0].split()
        expected_mode = b'100755' if int(e['mode'], 8) & 0o111 else b'100644'
        assert mode == expected_mode and kind == b'blob', ('Reviewed Git mode changed', rel)
    return changed

def staged_tree(git, base, expected):
    tree = git('write-tree').decode().strip()
    tree_pins(git, tree, base, expected)
    return tree

def committed_tree(git, commit, parent, staged, expected):
    row = git('show', '-s', '--format=%T %P', commit).decode().strip().split()
    assert row == [staged, parent], 'Commit changed the verified staged tree or parent'
    tree_pins(git, staged, parent, expected)
