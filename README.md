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

**The Quantum Chromatic Number of the \(G_{19}\) Join Family** proves the
finite-dimensional equality
\[
\chi_q(G_{19}\vee K_{n-3})=n+1\qquad(n\ge3).
\]
This confirms Lalonde's proposed finite witnesses:
\(\xi(G_{19}\vee K_{n-3})=n<\chi_q(G_{19}\vee K_{n-3})=n+1\), and the same
value holds at every fixed finite dimension and projector rank. It also gives
an alternative finite-witness proof that
\(\chi_q(S_{\mathbb C}^{n-1})\ge n+1\). The \(n=3\) equality was known; the
first new unrestricted case is the 20-vertex apex graph
\(G_{19}\vee K_1\), whose quantum chromatic number is five.
The proof symmetrizes arbitrary ranks, rigidifies the 13-vertex core by an
exact rational SOS, classifies every higher-rank tail by a \(J\)-invariant
plane, and finishes with a two-sector dimension-packing contradiction. Two
independent standard-library verifiers and machine-readable certificates
accompany the unreviewed note. See the
[research-note page](https://aleckriebel.github.io/Math/papers/lalonde-quantum-coloring/)
and [canonical proof package](https://github.com/AlecKriebel/Math/tree/91290c5764d89d6d6da7b6935c232d3d83733c75/lalonde20_quantum_coloring).

**Minimum Input Complexity for Separating Qubit POVMs from Projective
Measurements** proves that, with two Bell inputs per party and arbitrary
finite declared outputs, every fixed-qubit POVM behavior belongs to the
shared-randomness convex hull of fixed-qubit PVM behaviors. It pairs that
universal equality with an explicit rational \(3\times2\) Bell functional
whose exact algebraic POVM value exceeds a global analytic PVM upper bound.
Thus \(3\times2\), up to exchanging the parties, is the minimum input
architecture. The qualitative \(3\times2\) phenomenon is prior art; the
paper's contribution is the arbitrary-output \(2\times2\) closure and
resulting minimum-setting classification, together with a self-contained
proof, exact certificates, proof/priority audits, and a one-command verifier.
The release remains unreviewed and is labeled **READY, NEEDS EXPERT
SCRUTINY**. See the
[paper PDF](qubit_povm_pvm_minimum_settings/paper/main.pdf) and
[complete source and verification package](qubit_povm_pvm_minimum_settings/).

**Low-Schmidt rigidity and tensor-local constraints in the exceptional
unitary Hecke Yang--Baxter class** establishes exact structural constraints
for the remaining dimension-spectrum problem after the four-dimensional
construction.  Every exceptional solution is automatically standard and
faithfully represents the Jones--Wenzl trace quotient, while the complete
simple-multiplicity, central-rank, Markov-weight, and branching arithmetic of
that quotient permits every even local dimension.
The note proves that exceptional reflections of operator-Schmidt rank at most
three exist exactly when \(4\mid d\), and gives a new unrestricted rank-four
obstruction: in dimensions \(d\equiv2\pmod4\), both intrinsic joint-sandwich
maps must be singular.  It further proves that any hypothetical
six-dimensional solution is nonrestrictable, has scalar intersection of its
left and right leg commutants, and lies outside the primitive-Weyl
Bell-diagonal and four-product Clifford-frame mechanisms.  The complete
dimension spectrum remains open.
See the
[paper page](https://aleckriebel.github.io/Math/papers/exceptional-ybe-constraints/)
and [version 1.0.1 reproducibility release](https://github.com/AlecKriebel/Math/releases/tag/exceptional-ybe-constraints-v1.0.1).

**Exact Quantum Values and Permutation-Blind Maximizers in Cyclic Bell
Inequalities** consolidates the three historical cyclic-Bell notes. It proves
the all-dimensional commuting-operator value
\[
\beta_q(\mathcal I_d)=\beta_{qa}(\mathcal I_d)=\beta_{qc}(\mathcal I_d)
=2\csc\!\left(\frac{\pi}{2d}\right),
\]
then identifies a paired phase-permutation freedom invisible to the complete
first-harmonic Bell data. For both augmented families introduced by Perito,
D'Avino, Jung, Mironowicz, Acín, and Augusiak, an explicit permutation gives
nonuniform exact maximizers for every \(d\ge4\):
\[
G(AB\mid E)
\ge\frac1{d^2}
+\frac{2\sin(\pi/d)\sin(3\pi/d)}{d^2(d-1)}
>\frac1{d^2}.
\]
Both marginals remain uniform. The conclusion concerns the scalar Bell value,
not a randomness optimization conditioned on the complete canonical
behavior. Two independent \(d=4\) verifiers work exactly in
\(\mathbb Q(\zeta_{16})\); the package also retains the one-input baseline and
narrow low-setting observations. See the
[canonical paper page](https://aleckriebel.github.io/Math/papers/cyclic-bell-exact-values-and-randomness/),
[merged source package](cyclic_bell_exact_values_and_randomness/), and
[preserved historical versions](PUBLICATION.md).

**An exceptional four-dimensional unitary Hecke Yang--Baxter operator**
gives an exact representative of the previously unresolved class
\[
\left[e^{i\pi/3},\frac12,4\right].
\]
Its five-word Pauli formula is a Hermitian involution selected from a
one-parameter reflection circle by the braid relation. The \((-1)\)-spectral
projection has rank eight and both partial traces \(2I_4\), yielding faithful
embeddings of every \(H_n(3,6)\) and an ordinary unitary localization of the
\(\mathcal C(\mathfrak{sl}_3,6)\) Jones--Wenzl tower. The note proves local
dimension four is minimal and records a \((3,2)\)-generalized active form.
The public priority audit found no earlier ordinary four-dimensional
localization, but absolute novelty is not claimed. See the
[paper page](https://aleckriebel.github.io/Math/papers/exceptional-ybe-d4/)
and [version 1.1.0 source package](https://github.com/AlecKriebel/Math/releases/tag/exceptional-ybe-d4-v1.1.0).

**Excluding Parameter Three at Order Thirteen in the \(\gamma\)--\(\theta\)
Conjecture** proves that no graph on 13 vertices satisfies
\(\gamma(G)=\gamma^\infty(G)=3<\theta(G)\).  The argument splits at a
maximum independent triple into full-response and no-full-response branches,
then combines structural reductions with two independently reconstructed,
deletion-free RUP certificates.  Exact orbit coverage, sharp satisfiable
controls, hashes, and a compact replay wrapper accompany the paper.  This is
a finite, unreviewed result: common parameters four and five remain open at
order 13, and the universal conjecture is unresolved.  See the
[paper page](https://aleckriebel.github.io/Math/papers/gamma-theta-order-13-k3/),
the [active research page](https://aleckriebel.github.io/Math/research/gamma-theta-conjecture/),
and the [source package](gamma_theta_eternal_domination/).

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
order-12 frontier and now excluded the complete order-13 parameter-three
slice; any order-13 counterexample must have common parameter four or five.
The campaign is prioritizing a universal minimum-counterexample proof before
proceeding to order 14.  The current
proof lane has closed the exact-two-list branch at parameter three and
reduced the residual singleton/full-list cases to explicit multi-step
gates.  In the full-list lane, trapped rank-zero escapes force positive-rank
completion fans; a rank-one fan exit is now exactly an attacked-anchor
restoration, while higher-rank exits and cross-color coupling remain open.
In the independent exchange lane, every supported one-sided edge forces a
polarized bow tie of retained and omitted repair fans; the remaining QQ1
obstruction is global coupling among those objects.  These are
size-independent structural advances, not a complete parameter-three
theorem or a resolution of the universal conjecture.
The
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
