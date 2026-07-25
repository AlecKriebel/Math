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

**A 14-variable unipotent Keller map and every-order image and vanishing
obstructions** is Discovery 07, the repository's canonical consequence paper.
It isolates one inverse-series mechanism behind the strongest parts of
Discoveries 03, 05, and 06. Its flagship is a 24-term 14-variable map whose
nonlinear Jacobian is generically one nilpotent Jordan block and whose special
fiber consists scheme-theoretically of exactly three reduced rational points.
The same closed inverse coefficients disprove `SIC(14)` at every exponent and,
after exact transforms, give every-order Hessian-nilpotent Vanishing witnesses
in 30 variables at degree eight and 44 variables at degree four. The several
named injectivity and fixed-point consequences are explicitly treated as one
transformation family, not as independent discoveries.

**Full wreath-product monodromy through the third iterate of an explicit
Keller map** is Discovery 04. It provisionally determines the geometric
monodromy of the second and third iterates as `S_3 wr S_3` and
`S_3 wr S_3 wr S_3`, in degrees nine and 27. The strengthened paper includes
exact function-field, discriminant, denominator, Newton-polygon, and group
certificates and proves a full `3^m`-cycle in geometric inertia for every
iterate. A separately published, independently audited bounded-memory
certificate in the Discovery 04 source proves the fourth-iterate group
`S_3 wr S_3 wr S_3 wr S_3`; this is an internal audit, not peer review.

## Active computational search

[`hadamard_668_search/`](hadamard_668_search/) is a reproducible attempt to
construct a Hadamard matrix of order 668. No exact matrix has been found. The
current mechanically checked progress includes the fixed-`q` obstruction,
exhaustive variable-`q` margin decomposition, independent Legendre-pair and
cyclic-SDS lanes, a bounded exclusion of every exact `BS(84,83)` within raw
Hamming distance 18 of Eliahou's published seed, and a new semiregular
`C37` conference-core lane whose 625 integral nine-orbit quotient classes
are now classified exactly.  The latter has exact trace and moment laws and
an explicit full
characteristic-37 completion for every admissible first moment.  Its exact
all-quotient characteristic-two relaxation is bounded between `2^720` and
`2^721` modulo natural equivalences.  Explicit supports for both surviving
parity classes now satisfy every exact block margin and all adjacency
equations modulo two, while the best retained next-digit support still has
672 of 1,503 independent carry coefficients wrong.  Constant generators
through rank three and two named first-nonconstant rank-two families are
excluded across the quotient census; the smallest exact switch families
also fail.  This is not a classification of all formal solutions and no
support reaches adjacency modulo four.  The current construction gate is
therefore paused pending a genuinely new contraction or integral
construction principle.
A result counts only if an explicit `668 x 668` matrix passes exact full
verification.

## Archival derivations

- **Discovery 06** is the technical precursor containing the flagship
  14-variable construction and its scoped constant-state optimality proof.
  Discovery 07 incorporates the construction and adds the unified transfers,
  exact reduced-fiber proof, homogeneous Jordan type, and every-order
  companions.
- **Discovery 05** is retained as the earlier 21-dimensional Special Image
  Conjecture construction. It supplied an intermediate inverse lemma and is
  quantitatively superseded by the 14-dimensional witness.
- **Discovery 03** remains the timestamped 22/44-variable technical precursor.
  Its factor-reusing reduction and exact quartic certificate are incorporated
  into Discovery 07, which strengthens the quartic result to every-order
  nonvanishing.
- **Exploration 01** is retained as the full derivation of one weighted-lift
  specialization. Its monodromy theorem was already available in stronger form
  before release; its uniform rational collision remains in the archived
  Discovery 03 appendix.
- **Exploration 02** is retained as the timestamped first 13-variable/54-variable
  construction. It is superseded and absorbed through Discoveries 03 and 07.

The archive remains public to preserve provenance rather than rewrite history.
The only current papers are Discovery 04 and Discovery 07.
