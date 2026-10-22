#!/usr/bin/env python3
"""Isolated adapter for the two byte-preserved exact checkers.

Trust assumption: the CPython installation, its stdlib, and installed SymPy
1.14.0 plus mpmath 1.3.0 are trusted. No package install, site startup, .pth
processing, or cwd/PYTHONPATH import is performed. Unsupported versions fail.
The fixed publication bootstrap authenticates this adapter and checker bytes.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: adapter requires -I -S -B')
import importlib.util
import os
from pathlib import Path
import sysconfig


def need(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    need(os.getuid() == os.geteuid() == 1000, 'UID=EUID=1000 required')
    need(len(sys.argv) in (2, 3), 'checker and optional mutation required')
    program = sys.argv[1]
    need(program in ('original', 'independent'), 'known checker')
    mutation = sys.argv[2] if len(sys.argv) == 3 else None
    mutations = ('remove_factorials', 'wrong_heat_scale', 'wrong_cross_multiplicity',
                 'wrong_elimination_sign', 'wrong_residual_coefficient', 'wrong_fourier_lead')
    need(mutation is None or (program == 'independent' and mutation in mutations), 'known independent mathematical mutation')
    root = Path(__file__).resolve().parent
    prefix = Path(sys.base_prefix).resolve()
    installed = Path(sysconfig.get_path('purelib')).resolve()
    need(installed.is_relative_to(prefix) and installed.is_dir(), 'trusted installation location')
    need(all(p and Path(p).resolve().is_relative_to(prefix) for p in sys.path), 'initial isolated stdlib search path')
    # An explicit installed-package directory is appended without executing site
    # or any .pth file. Never append the packet, its current directory, or cwd.
    sys.path.append(str(installed))
    for name in ('sympy', 'mpmath'):
        spec = importlib.util.find_spec(name)
        need(spec is not None and spec.origin is not None and
             Path(spec.origin).resolve() == installed / name / '__init__.py',
             'trusted installed ' + name + ' origin')
    import sympy
    import mpmath
    need(sympy.__version__ == '1.14.0' and mpmath.__version__ == '1.3.0',
         'supported installed SymPy 1.14.0 and mpmath 1.3.0 required')
    filename = 'check_formal_jets.py' if program == 'original' else 'independent_checks.py'
    source = (root / 'current' / filename).read_bytes()
    sys.argv = [filename] + ([] if mutation is None else ['--mutation', mutation])
    try:
        exec(compile(source, '<authenticated-' + filename + '>', 'exec'),
             {'__name__': '__main__', '__file__': str(root / 'current' / filename)})
    except RuntimeError as error:
        if mutation is None:
            raise
        print('REJECT: intended mathematical mutation: ' + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, ImportError, RuntimeError) as error:
        print('REJECT: isolated checker adapter: ' + str(error), file=sys.stderr)
        sys.exit(2)
