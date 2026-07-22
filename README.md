# Alec's Math Explorations

Provisional, AI-assisted mathematical experiments by **Alec Kriebel, with
heavy assistance from ChatGPT 5.6 Sol**.

This repository is the source for the public research notebook at
<https://aleckriebel.github.io/Math/>. It is separate from Alec's personal
website, <https://aleckriebel.com/>.

## Important verification disclaimer

I am a complete amateur and cannot independently verify the mathematical
claims in this repository. I am exploring the limits of AI-assisted
mathematics. Nothing here should be treated as an established result until
qualified experts have independently checked the proofs, computations,
citations, scope, and novelty claims.

The source, exact verification scripts, and machine-readable certificates are
published so that others can audit the work. Passing the included checks is
evidence about the encoded algebra; it is not peer review and does not prove
that the interpretation or literature claims are correct.

## Current papers

**An explicit counterexample to the Special Image Conjecture in dimension
21** is Discovery 05, currently an unreviewed research draft. It gives a
72-term rational pair `(A,b)` in 42 indeterminates, proves that every positive
power of `A` lies in `ker(E_21)`, and proves that `b*A^m` lies outside it for
infinitely many `m`. Its novelty claim is intentionally limited: Exploration
03's cubic model already implies SIC(22), while this construction removes one
homogenizing variable and handles the resulting linear block with a
scalar-parameter inversion lemma.

**Full wreath-product monodromy for the square of an explicit Keller map** is
Discovery 04. It provisionally determines the geometric monodromy of the
canonical self-composition as `S_3 wr S_3` in degree nine and proves a full
`3^m`-cycle in geometric inertia for every iterate. The strengthened site
edition includes an exact linear-subresultant/function-field certificate and a
local-field Puiseux induction.

**An explicit 44-variable vanishing witness from a 22-variable cubic Keller
map** remains the consolidated paper for Explorations 01-03. It contains the
factor-reusing 13-variable
stable reduction, the rank-eight/22-variable cubic construction, the explicit
44-variable quartic certificate, the corrected priority audit, and an appendix
with the surviving uniform rational collision from Exploration 01.

## Active computational search

[`hadamard_668_search/`](hadamard_668_search/) is a reproducible attempt to
construct a Hadamard matrix of order 668. No exact matrix has been found. The
current mechanically checked progress includes the fixed-`q` obstruction,
exhaustive variable-`q` margin decomposition, independent Legendre-pair and
cyclic-SDS lanes, and a bounded exclusion of every exact `BS(84,83)` within
raw Hamming distance 17 of Eliahou's published seed. A result counts only if
an explicit `668 x 668` matrix passes exact full verification.

## Archival derivations

- **Exploration 01** is retained as the full derivation of one weighted-lift
  specialization. Its monodromy theorem was already available in stronger form
  before release; only its uniform rational collision remains in the canonical
  appendix.
- **Exploration 02** is retained as the timestamped first 13-variable/54-variable
  construction. It is superseded and absorbed into the canonical paper.

The archive remains public to preserve provenance rather than rewrite history.
It should not be read as three independent discoveries.
