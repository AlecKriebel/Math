# Vendored Python distributions

This directory contains the two unmodified, pure-Python wheels used by the
exact certificate replay.  `requirements.txt` disables package indexes,
selects only binary distributions from this directory, and requires the
following SHA-256 digests:

| Distribution | SHA-256 |
|---|---|
| `mpmath-1.3.0-py3-none-any.whl` | `a0b2b9fe80bbcd81a6647ff13108738cfb482d481d826cc0e02f5b35e5c88d2c` |
| `sympy-1.14.0-py3-none-any.whl` | `e091cc3e99d2141a0ba2847328f5479b05d94a6635cb96148ccb3f34671bd8f5` |

The corresponding upstream distribution releases are
<https://pypi.org/project/mpmath/1.3.0/> and
<https://pypi.org/project/sympy/1.14.0/>.  Their upstream source repositories
as recorded in the wheel metadata are
<https://github.com/fredrik-johansson/mpmath> and
<https://github.com/sympy/sympy>, respectively.

The wheels retain their upstream license files and metadata.  mpmath and
SymPy are third-party BSD-licensed projects and are not relicensed under this
project's MIT license.

These wheels make the Python certificate bootstrap offline after a compatible
Python 3.14.6 interpreter is installed.  They do not supply Python itself,
Tectonic, Poppler, or Tectonic's TeX resource bundle; document rebuilding has
the separate external-tool boundary described in `submission/ENVIRONMENT.md`.
