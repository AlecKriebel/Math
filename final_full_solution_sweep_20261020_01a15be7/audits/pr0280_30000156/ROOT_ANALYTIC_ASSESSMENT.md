# Root analytic assessment of PR280

2026-10-21T02:46Z. Root proof/source review checkpoint, about90% of that
assigned mathematical check; publication/priority clearance is not given.
Overall final-sweep completion estimate remains17%.

The17-file original source is bound by SOURCE_SNAPSHOT.json to head
091bdecef6f84154f5d5c205a4b07eeb6391b8f8. The fresh full173-row GWS read found
only a birational-keyword hit for a different original problem, PR329's quintic
fifth-torsion theorem. The local Zenodo-state search likewise found only that
different record. The prior PR280 audit reports no prepared paper or publication;
it is retained as earlier evidence, not presumed mathematical or priority truth.

## Exact claim checked

For L(u,v)=(u,(u²+1)v), its rational inverse is (u,v/(u²+1)). At each prime
p≡3 modulo4 this is an everywhere-defined permutation of F_p². Its point-period
distribution, normalized by p² with period threshold px, has no ordinary limit
for every fixed1/2≤x<1 along that fixed arithmetic prime class, and has no weak
limit. No polynomial inverse over C or arbitrary refinement of the prime class
is claimed.

The author's complete two-page original source was freshly read at
https://webspace.maths.qmul.ac.uk/f.vivaldi/research/Oberwolfach.pdf . Its
unrestricted birational existence assertion, rational integrability convention,
point weighting and p scaling agree with the candidate. Genus one is used in a
later heuristic, rather than imposed on the universal assertion. The independent
source family also authenticates the printed original pages2944–2945 and tests
the prime-set wording separately. The full MFO report timed out in root's web
read; that failure is not counted as an additional authenticated root read.

## Independent reconstruction of the deductions

Write N=p−1, θ=φ(N)/N and P=#{u:ord_p(u²+1)=N}. On every nonzero-v fiber all
periods equal the multiplier's order, while the p points with v=0 have period1.
Every proper divisor of N is at most N/2. For fixed1/2≤x<1, eventually N>px, so
the exact excluded point count is (p−1)P and D_p(x)=1−(p−1)P/p². Counting cycles
instead would be wrong; the submitted formula counts the actual points.

The primitive-element indicator factors over primes dividing N. Extending all
characters by zero at0, each nontrivial χ satisfies
Σ_uχ(u²+1)=η(−1)J(η,χ). The Gauss identity gives modulus sqrt(p) except at χ=η,
where the sum is−1. The principal term is exactly p because u²+1 has no zero.
Triangle inequality in the squarefree-divisor indicator therefore gives
|P/p−θ|≤θ(2^ω(N)−1)/sqrt(p). Separating the six primes below16 gives
2^ω(N)≤64N^(1/4). Consequently |D_p(x)−(1−θ)|≤1/p+64p^(−1/4), eventually for
each fixed x in the stated interval. There is no required uniformity as x→1.

The required totient mean is unconditional. Root freshly read the published
Menici–Pehlivan2016 introduction equation1 and the entire Lemma2/proof,
printed262–263: https://www.impan.pl/shop/en/publication/transaction/download/product/91625 .
The r=m=1 specialization uses Siegel–Walfisz with arbitrary fixed logarithmic
modulus/error parameters, not a fixed-base primitive-root conjecture. Directly,
Möbius inversion and K=(log X)^6 leave a tail bounded by O(X/K); the small-modulus
error is O(X log K/(log X)^4)=o(X/log X). The bound φ(d)≥sqrt(d/2) makes the
coefficient series absolutely convergent. Its Euler product is Artin's constant A.
This restates an established analytic argument and is not a new mean theorem.

The elementary product bound A≥7/24 is valid: after the factor1/2 at2, the sum
of the omitted factors' decrements is at most the sum over all integers≥3 with4
excluded, namely5/12. This intentionally weak bound still exceeds13/48.

CRT plus Dirichlet supplies increasing p_j≡3 modulo4 with every chosen finite
initial set of odd primes dividing p_j−1. Euler's vanishing prime product gives
θ_(p_j)→0, hence D_(p_j)(x)→1. Conversely, if only finitely many primes in the
3-modulo4 class had θ≥1/24, the fixed-modulus prime number theorem and θ≤1/2 at
every odd prime would force the overall prime mean to be at most13/48. This
contradicts A≥14/48. The second subsequence thus has D_p(x)≤23/24+o(1).
Both subsequences work for every fixed threshold in the claimed interval.

Failure at an interval of thresholds rules out weak convergence, since a
probability CDF has at most countably many discontinuities. The independent
source reviewer additionally supplied the continuous-test-function proof:
h(t)=0 for t≤1/2, h(t)=2t−1 for1/2<t<1, and h(t)=1 for t≥1. For p≥3 the proper
periods contribute zero and the primitive fibers contribute exactly
(1−2/p)(p−1)P/p². Thus its expectation is θ+o(1), and the same two subsequences
give incompatible limits. This is a deduction, not a numerical inference.

## Checks and remaining gate

The source and arithmetic families are independent of this root reconstruction
and of one another. The arithmetic reviewer reports a new replay of earlier
standard-library controls, including8,347,742 finite assertions and230,780
analytic controls. Their completed reports/receipts, rather than this progress
message, must be inspected before final acceptance. The submitted original
verifiers require SymPy, which the default interpreter lacks; no unreported
successful original-script replay is claimed here. Finite checks do not prove
the infinite-prime deductions.

No mathematical error has been identified in the written proof. The exact
application's priority remains a separate open gate: construction, character
machinery and totient ingredients are established, and a closely related2011
manuscript was not recovered by the earlier audit. A fresh independent family
is checking new institutional/version routes and the exact classical implication.
An unavailable body is neither proof of an earlier result nor proof of novelty.
This assessment supplies mathematical evidence only; scientific publication readiness remains pending the separate priority and final-package gates.
