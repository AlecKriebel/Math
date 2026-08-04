# Locked verification environment

The archived transcripts were produced with the following environment:

- Python 3.13.5
- SymPy 1.14.0
- mpmath 1.3.0
- GNU Make 4.4.1
- MPFR shared library `libmpfr.so.6`
- GMP shared library `libgmp.so.10`
- latexmk 4.86
- pdfTeX 3.141592653-2.6-1.40.26 (TeX Live 2025 development/Debian build)

The Python package lock is `requirements-lock.txt`. The exact verifier calls MPFR directly through `ctypes`; it does not use binary floating point for theorem-bearing interval claims. NumPy is not required by the exact verifier. The simulation audit uses only the Python standard library.
