# Projective line quotient counterexample

Problem 30001478 / OWR-4335-003 has a complete counterexample to both assertions as stated. The quotient by (x3-x1,x4-x2) is a twisted homogeneous coordinate ring of P1. Read proof.md for the self-contained proof and precise scope.

Run with Python 3.9 or newer, standard library only:

    python3 verify.py
    python3 -O verify.py
    python3 test_suite.py

The verifier first enforces the exact regular-file inventory and SHA-256 manifest, then recomputes the symbolic identities from certificate.json. Unexpected directories, bytecode caches, symlinks, and other nonregular files are rejected. The test suite uses temporary copies and rehashes semantic mutations so that its negative controls reach the mathematical checks, rather than failing only at checksums. It also tests relocation and optimized Python.

The archive contains authored proof, verification code, an authored algebraic certificate, replay results, and public verification metadata. No source PDF, source-text extract, dataset contents, or private coordination material is included. The source URLs and hashes permit a reviewer to obtain primary documents separately.

Status: complete counterexample to the literal question, unrefereed, publication priority unclaimed. The finite computations are supporting checks, not a replacement for the universal proof.
