#!/usr/bin/env python3
"""Trusted installed-dependency adapter; does not alter checked source or output."""
import os,sys,sysconfig
from pathlib import Path
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise RuntimeError('require -I -S -B')
if os.getuid()!=1000 or os.geteuid()!=1000:raise RuntimeError('UID=EUID=1000 required')
if len(sys.argv)<2 or sys.argv[1] not in ('check_exact.py','audit_exact.py'):raise RuntimeError('known safe checker required')
# Installed packages are an explicitly trusted dependency boundary. No site
# initialization or .pth files are executed. CWD and packet paths are not added.
purelib=sysconfig.get_path('purelib')
if not isinstance(purelib,str) or not os.path.isabs(purelib):raise RuntimeError('installed dependency path')
sys.path.append(purelib)
import sympy,mpmath
if sympy.__version__!='1.14.0' or mpmath.__version__!='1.3.0':raise RuntimeError('trusted dependency version mismatch')
name=sys.argv[1];root=Path(__file__).resolve().parent;source=(root/name).read_bytes();sys.argv=[name,*sys.argv[2:]]
exec(compile(source,'<two-loop-'+name+'>','exec'),{'__name__':'__main__','__file__':str(root/name)})
