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

**The exact quantum value of a cyclic Bell operator** proves Conjecture 1 of
Perito, D'Avino, Jung, Mironowicz, Acín, and Augusiak:
\[
\beta_q(\mathcal I_d)
=\beta_{qa}(\mathcal I_d)
=\beta_{qc}(\mathcal I_d)
=2\csc\!\left(\frac{\pi}{2d}\right)
\quad(d\ge2).
\]
Their paper introduced the Bell family, conjectured the formula, and supplied
the attaining strategy and lower bound. The candidate contribution is the
dimension-independent analytic upper bound, which remains valid for arbitrary
unitary Alice and Bob observables satisfying cross-party commutation, without
order relations or a tensor-product representation. The proof uses an exact
polar positive-factor identity and a sharp scalar roots-of-unity extremum. It
does not prove uniqueness, self-testing, or all-dimensional randomness. See the
[paper page](https://aleckriebel.github.io/Math/papers/cyclic-bell-tsirelson-bound/)
and [source package](cyclic_bell_tsirelson_bound/).

**A Certified Order-Twelve Extension of the \(\gamma\)--\(\theta\) Frontier
in One-Guard Eternal Domination** combines a complete order-12 parameter
split—exact proof certificates for common parameters three and four, and a
structural argument for parameter five—with
MacGillivray--Mynhardt--Virgile's published exhaustive computation through
order 11. Relative to that published premise, every counterexample now has at
least 13 vertices. This is a finite, unreviewed result and does not resolve
the universal conjecture. See the
[paper page](https://aleckriebel.github.io/Math/papers/gamma-theta-order-12-frontier/),
the [active research page](https://aleckriebel.github.io/Math/research/gamma-theta-conjecture/),
the [tagged reproducibility release](https://github.com/AlecKriebel/Math/releases/tag/gamma-theta-order12-frontier-v1.0.0),
and the [source package](gamma_theta_eternal_domination/).

**Eternal domination and the Lovász theta function** gives an explicit family
with
\(\vartheta(G)/\gamma^\infty(G)=\Theta(|V(G)|^{1/3})\), by combining
published results of Alon and of Goddard, Hedetniemi, and Hedetniemi. It also
gives the sharp smallest example: the graph with graph6 record `IEhbtj{ro`
satisfies
\(\gamma^\infty(G)=3<7593/2500\leq\vartheta(G)\).
The finite theta certificate uses exact rational arithmetic, and a separate
state-space verifier independently recomputes the standard one-guard game.
The minimum-order conclusion uses the published exhaustive classification
through order nine. See the
[paper page](https://aleckriebel.github.io/Math/papers/eternal-domination-lovasz-theta/)
and [source package](eternal_domination_lovasz_theta/).

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

Three scoped **Hadamard-order-668 pause papers** publish exact mathematics
from a four-day construction program: local repair obstructions around
Eliahou's modular seed, shell descent and norm gates in one fixed-compression
Legendre-pair chart, and semiregular cyclic conference quotients. All three
are computer-assisted, unreviewed, and explicitly state that they neither
construct nor exclude `H(668)`. See the
[public research checkpoint](https://aleckriebel.github.io/Math/research/hadamard-matrix-order-668/)
and tagged
[reproducibility release](https://github.com/AlecKriebel/Math/releases/tag/h668-research-checkpoint-v1.0.0).

## Active research

[`gamma_theta_eternal_domination/`](gamma_theta_eternal_domination/) is a
27-day campaign to prove or disprove the one-guard \(\gamma\)--\(\theta\)
conjecture. The conjecture remains open. The campaign has certified the
order-12 frontier, reduced the order-13 parameter-three slice to two
overlapping odd-hole templates, and is now prioritizing a universal
minimum-counterexample proof before proceeding to order 14. The
[public workstream](https://aleckriebel.github.io/Math/research/gamma-theta-conjecture/)
is a dated snapshot; `STATE.md` and `CLAIMS.md` in the source package are the
live records.

## Paused H(668) research

[`hadamard_668_search/`](hadamard_668_search/) is a reproducible attempt to
construct a Hadamard matrix of order 668. No exact matrix, Legendre pair of
length 333, base sequence in `BS(84,83)`, or conference graph was found.
The strongest final reduction is a triple pair-resultant norm key in
`F_(167^3)^*`, but the complete remaining join still requires about
5.092 trillion invariant evaluations and 81.5 TB under the stated naive
layout. The headline search is paused under explicit restart criteria.
A solution counts only if an explicit `668 x 668` matrix passes exact full
verification.

## Paused research

[`kissing_number_5/`](kissing_number_5/) records an intensive attempt on the
five-dimensional kissing-number problem. It did **not** resolve the problem or
improve the rigorous interval
\(40\leq\tau(5)\leq44\). The repository contains an exact checker for the
40-point \(D_5\) construction, scoped local and finite-model results, exact
counterexamples to several tempting proof strategies, numerical construction
searches, and a detailed resume guide. The
[public checkpoint](https://aleckriebel.github.io/Math/research/kissing-number-5/)
is deliberately labeled paused and unresolved.

[`erdos_084_cycle_sets/`](erdos_084_cycle_sets/) records a paused attempt on
the lower-bound half of Erdős Problem 84. It did **not** prove
\(f(n)/2^{n/2}\to\infty\) or improve the published asymptotic bounds. The
dossier preserves a protected difference-support reduction, exact shadow
counts, a short all-\(m\) twin-boundary identity, finite Hall-matching tests,
and explicit falsifications of several proposed proof mechanisms. The
[public checkpoint](https://aleckriebel.github.io/Math/research/erdos-problem-84/)
separates the proved lemmas, finite evidence, conjectures, and two remaining
global gaps.

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
The Lovász-theta note is a separate current graph-theory paper. Discovery 04
and Discovery 07 are the two current canonical discovery papers; the three
H(668) papers are separately labeled provisional pause-checkpoint research.
