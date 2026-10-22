# 2609 / KOU-21.100: credited negative resolution

Concrete title: **Counting invariant characters nonvanishing on a coprime fixed subgroup**.

Eric Hou's existing [arXiv preprint](https://arxiv.org/abs/2609.16227v1) supplies a counterexample. A cyclic operator group of order 21 acts coprimely on a group of order 2^135. The fixed subgroup is elementary abelian of order 4096, but only 1728 invariant irreducible characters are nonzero everywhere on it.

`CERTIFICATE.md` reconstructs the finite group, the fixed subgroup, one explicit irreducible character with a zero, and the complete invariant-character parameterization. The strict inequality alone gives a complete negative answer, independently of the supplemental 1728 calculation. `SOURCES.md` records exact provenance and preprint/editorial-status limits. `INDEPENDENT_CHECKS.md` explains the two independently written programs and their scope.

Original substantive proof-attempt count: **0/5**. Discovery credit: **Eric Hou**. Proposed queue disposition: **already_solved**. This is a credited source-verification record, not a new solution or paper. A separate fresh independent AI audit passed the complete certificate and independently reproduced the exact count. This draft research record is unrefereed.

Verify the manifest and replay both programs from any directory:

    python3 verify_publication.py

Python 3 and a GNU or Clang C++17 compiler are required for full replay (the independent audit checker uses the 128-bit integer extension). The minimal witness program uses only Python's standard library. No source PDFs, screenshots, copied verification archive, or raw catalogue are redistributed.
