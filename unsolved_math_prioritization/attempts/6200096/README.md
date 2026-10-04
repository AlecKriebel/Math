# 6200096: published negative homotopy Nielsen realization

**Disposition: already_solved, negative; one of five author turns used.**

This is a verification of prior work, with no novelty claim. Smrekar's 2023
published Example 1 gives an explicit cyclic-group obstruction. The C₂ case
has a compact two-dimensional polyhedron and a simple self-equivalence
whose unbased homotopy class has order two, but it has no compatible
homeomorphism action on any homotopy-equivalent replacement space.
The fundamental-group extension would force the impossible equation 2n=-1
for n∈Z.

The intended scope is prescribed unbased simple homotopy classes and
homotopy-compatible realization. No fixed-point or free-action condition
is imposed. Strict groups of actual maps, unrelated abstract-group actions,
and torsion-free acting-group variants are different questions.

## Preserved records

* `packet/` preserves all 13 original authored files, including its manifest.
* `audit/` preserves all 9 independent AI audit files, including its manifest.
* Both original authored-only archives and the original audit receipt are
  preserved byte-for-byte. The audit is an independent AI mathematical
  review, not journal peer review.
* The frozen author's pending-audit field and the frozen audit's pending
  normalization clarification record their original times. The accepted
  mathematical audit is in `audit/INDEPENDENT_AUDIT.md`. The subsequently
  recovered normalization specification is recorded separately below.

## Reproduction from this final directory

    python3 packet/verify.py --output /tmp/6200096-author.json
    python3 packet/verify_manifest.py
    python3 audit/verify_audit_manifest.py
    python3 audit/independent_verify.py --packet packet --archive rank648-6200096-authored-packet.tar.gz --output /tmp/6200096-independent.json
    python3 verify_publication.py

The author controls have 632,826 passing assertions. The full independent
replay, including original-archive bindings and author replay, has 74,902.
Their JSON outputs match the frozen results byte-for-byte.

The last command checks final file inventory, byte counts, and digests. The
top-level publication manifest excludes only itself. The mathematical
programs need Python's standard library and no private inputs or source PDFs.

## Source-normalization clarification

The frozen audit correctly flagged that the author's verbal normalization
description did not fix the exact output alphabet. The original routine
has now been recovered, published as `normalize_statement.py`, and rerun
on the original primary-source extraction and selected record. Its literal
prime placeholder is `X PRIME`, while the independent audit used a prime
glyph. Both exact statement comparisons pass; their distinct normal forms
legitimately have different hashes. `NORMALIZATION_REPLAY.json` records
the author's bit-for-bit reproduction, without source text. The raw
selected-statement hash was already independently verified. Original records
remain unchanged; this clarification has no mathematical effect.

## Sources

- [Kapovich, Problem 96 and Remark 32, p. 24](https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf)
- [Smrekar, Journal of Pure and Applied Algebra 227 (2023), 107350, Example 1](https://doi.org/10.1016/j.jpaa.2023.107350)
- [University repository publication record](https://repozitorij.uni-lj.si/IzpisGradiva.php?id=148644)

Only authored mathematics, audit material, executable checks, and public
verification metadata are included. Source PDFs, full text, dataset records,
corpora, and private coordination material are not redistributed.
