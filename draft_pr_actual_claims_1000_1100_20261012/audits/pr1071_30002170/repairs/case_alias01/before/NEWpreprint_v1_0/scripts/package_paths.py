"""Static filesystem policy for frozen members and fresh external outputs.

Outputs must not exist (including dangling symlinks). Their parent must be an
existing real directory outside the package, with no symlink ancestors. A new
output directory is empty before any copy, log or trusted subprocess write.
This is a static local preflight, not a concurrent filesystem race guarantee.
"""
import os, stat
from pathlib import Path, PurePosixPath
ROOT = Path(__file__).resolve().parents[1]
def require(ok, message):
    if not ok:
        raise RuntimeError(message)
def safe_path(root, name):
    require(isinstance(name, str) and bool(name), 'Invalid member name.')
    parts = name.split('/')
    require(not PurePosixPath(name).is_absolute() and all(x not in ('', '.', '..') for x in parts) and '\\' not in name, 'Unsafe member name: ' + name)
    base = Path(root).resolve()
    current = base
    for i, part in enumerate(parts):
        current = current / part
        require(not current.is_symlink(), 'Symlink member/ancestor: ' + name)
        require(current.exists(), 'Missing member/ancestor: ' + name)
        mode = current.stat().st_mode
        require(stat.S_ISREG(mode) if i == len(parts)-1 else stat.S_ISDIR(mode), 'Nonregular member or nondirectory ancestor: ' + name)
    require(current.resolve().is_relative_to(base), 'Escaping member: ' + name)
    return current

def fresh_output(path, root=ROOT):
    """Return a preflighted absent file/directory; no mkdir or write occurs."""
    target = Path(os.path.abspath(os.fspath(path)))
    require(not target.exists() and not target.is_symlink(), 'Output must be new; existing files/directories, symlinks and hardlinks are rejected: ' + str(target))
    parent = target.parent
    require(parent.exists() and parent.is_dir(), 'Output parent must already exist: ' + str(parent))
    for ancestor in (parent, *parent.parents):
        require(not ancestor.is_symlink(), 'Symlink output ancestor: ' + str(ancestor))
        require(ancestor.is_dir(), 'Output ancestor is not a directory: ' + str(ancestor))
    require(not target.is_relative_to(Path(root).resolve()) and not target.resolve().is_relative_to(Path(root).resolve()), 'Output must be outside all frozen package descendants.')
    return target
