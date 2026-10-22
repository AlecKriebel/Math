#!/usr/bin/env python3
"""Verified snapshot dispatcher; only used by the publication's temporary shim."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: dispatcher requires -I -S -B')
import stat
from pathlib import Path
shim,entry,*args=sys.argv[1:]
p=Path(entry)
if not p.is_absolute() or '..' in p.parts:raise ValueError('absolute entrypoint required')
for q in p.parents:
    if not stat.S_ISDIR(q.lstat().st_mode):raise ValueError('nonordinary entrypoint ancestry')
if not stat.S_ISREG(p.lstat().st_mode):raise ValueError('nonregular entrypoint')
# All original source bytes were authenticated by the outer bootstrap. The
# archived control suite also creates its known diagnostic mutations itself.
sys.executable=shim
sys.argv=[entry,*args]
exec(compile(p.read_bytes(),entry,'exec'),{'__name__':'__main__','__file__':entry})
