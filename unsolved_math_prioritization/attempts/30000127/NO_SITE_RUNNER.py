#!/usr/bin/env python3
"""Explicit trusted-installed-dependency adapter; never execute site initialization."""
import os,sys,sysconfig
from pathlib import Path
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise RuntimeError("require -I -S -B")
if os.getuid()!=1000 or os.geteuid()!=1000:raise RuntimeError("require UID=EUID=1000")
if len(sys.argv)!=4 or sys.argv[1] not in ("current/verify_algebra.py","current/audit_checks.py") or sys.argv[2]!="--mutation":raise RuntimeError("exact checker arguments")
purelib=Path(sysconfig.get_path("purelib")).resolve()
if not purelib.is_dir():raise RuntimeError("trusted installed dependency directory unavailable")
sys.path.append(str(purelib))
import sympy,mpmath
if sympy.__version__!="1.14.0" or mpmath.__version__!="1.3.0":raise RuntimeError("trusted installed dependency versions")
if not all(Path(x.__file__).resolve().is_relative_to(purelib) for x in (sympy,mpmath)):raise RuntimeError("trusted installed dependency origin")
script=sys.argv[1];sys.argv=sys.argv[1:]
try:exec(compile(Path(script).read_bytes(),script,"exec"),{"__name__":"__main__","__file__":script})
except ValueError as exc:
 print("ValueError: "+str(exc),file=sys.stderr)
 raise SystemExit(1)
