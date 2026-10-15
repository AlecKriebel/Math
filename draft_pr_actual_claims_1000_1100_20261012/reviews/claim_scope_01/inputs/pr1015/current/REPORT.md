# Algebraic dimension from positive normal bundles

**Result: partial mathematical audit, not a solution of the general implication.**

## The exact question

Let Z be a compact connected complex manifold of dimension n+p (n≥0, p≥1), and let Y⊂Z be a compact complex submanifold of dimension p−1. Assume N_{Y/Z} is Griffiths-positive. Suppose a compact normal complex space S parameterizes an analytic family (X_s) of compact n-cycles whose supports cover Z. Must a(Z)≥p?

Here a(Z) is the transcendence degree over C of its field of global meromorphic functions. Griffiths positivity means positivity of a smooth Hermitian curvature tensor for every pair of nonzero tangent and normal-bundle vectors. The ambient is not assumed Kähler, and the covering family is not asserted to consist of deformations of Y. The compact/closed convention for Y is the one used by the underlying paper, including its introduction and Theorem 4.3.

Source: Daniel Barlet's contribution, OWR 21/2004, printed p.1154, https://ems.press/content/serial-article-files/45885 . The workshop took place in 2004; the catalogue's “2005” label should not change the issue identification.

## Verified prior scope

Barlet–Magnússon (2004), Theorem 0.7, needs generically finite incidence with Y and an additional local separation condition. Sections 3.18–3.24 implement separation using intersection points, first normal directions, or suitable tangent cones; the relevant maximal-pole component matters. The fibration case in Corollary 0.8 is affirmative. The cases p=1 and n=0 are already known (Remarks 0.6(1), 0.2(3)).

Theorem 4.3 reduces an effective, generically irreducible reduced covering family to a residual case: dim S=p, no compact covering family of positive-dimensional Moishezon cycles on S, divisorial incidence Σ, and S\Σ a proper modification of a Stein space. Remark 4.4(2) gives holomorphic functions on a complement; Introduction 0.9 explicitly warns that these may have essential boundary singularities. This is not a meromorphic-extension theorem.

The relevant proofs in §§3.15–3.25 and §4 were inspected in the complete 42-page primary PDF. Foundational results cited there were not independently reproved.

Reference: D. Barlet and J. Magnússon, *Integration of meromorphic cohomology classes and applications*, Asian J. Math. 8 (2004), 173–214, https://doi.org/10.4310/AJM.2004.v8.n1.a13 .

Peternell's Corollary 3.4 proves the p=2 case when Z is compact Kähler: a positive-normal curve together with a covering codimension-two family gives a(Z)≥2. Its proof uses the surface lemma 3.5. The higher-dimensional extension is discussed as a further problem in Remark 3.6. This does not remove the Kähler hypothesis from the OWR question. See *Compact subvarieties with ample normal bundles, algebraicity and cones of cycles*, https://arxiv.org/abs/1106.4433 , §§3.3–3.6. The downloaded file is arXiv v1, with an internal typesetting date in 2022; neither date is evidence of a new general theorem.

## Authored results

- **INCIDENCE_CAVEAT.md:** a compact P²-family of planes in P⁴, with positive-normal Y=P¹, has X_s∩Y=Y for every s. Finite incidence is not automatic for the given family.
- **JET_SEPARATION.md:** the plane-conic family in P³ has generically finite non-tangential incidence with a positive-normal line, but initial normal data cannot separate its seven-dimensional incidence divisor. A separate elementary lemma proves generic local separation by finitely many Taylor coefficients when the full germ separates parameters. The missing global pole-control step is identified.
- **GRAPH_TRANSFORM.md:** a positive-normal line in P³ lifts under a natural incidence modification to a fibre with trivial normal bundle. Positivity cannot be carried through such a modification without proof.
- **FIBRE_FIELDS.md:** a standard elliptic K3 example disproves unqualified addition of algebraic dimensions of base and fibre. It has no positive-normal curve and is used only to test that intermediate inference.
- **BOUNDARY_GROWTH.md:** polynomial boundary growth would give a precise meromorphic-extension bridge. An exact exponential trace calculation proves that finite traces do not automatically remove essential singularities.

All examples are obstacles to intermediate shortcuts. None is a counterexample to the target. The local finite-jet lemma and conditional growth bridge do not establish the original global conclusion. No novelty claim is made for these elementary observations.

## Validation and limits

The accompanying standard-library Python checker verifies exact dimension formulas, selected Taylor coefficients, finite-dimensional trace identities, and explicit rejection of corrupted values. It does not certify analytic geometry or replace the written proofs. It performs no floating-point experiment and writes no files by default. The original checker is unchanged. Independent audit tests additionally compare its trace values with rational multiplication matrices and its Taylor coefficients with a formal derivative/inverse-series calculation. All three CLI modes, with and without injected failures, and 22 semantic mutations were tested under normal Python, -O and -OO, with actual UID/EUID 1000 and real denial of file-write and file-creation attempts in the read-only packet. Source-interface guards are documentary checks, not formal proofs of the cited sources.

The general target remains unresolved by this audit. Bounded primary-literature checks through 8 October 2026 did not locate a later full theorem; they are not an exhaustive proof of worldwide openness. Independent mathematical review remains appropriate before relying on the partial lemmas in another proof.
