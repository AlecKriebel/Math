# Independent audit: minimal separations on squarefree split circles

Problem 30003279 / OWR-15174-012; queue rank 996. Audit date: 8 October 2026.

## Verdict

**Accept the mathematical partial results and the UNSOLVED overall disposition.** The three-point construction really does give infinitely many squarefree squared radii whose prime divisors are all 1 modulo 4, with limiting arc constant 16^(1/3). The other four routes have the stated scope. None supplies the missing sharp four-point or larger squarefree construction.

**Accept the hardened validation copy.** The frozen original has narrow input-validation defects, reproduced below. They do not invalidate its fixed examples, proofs, manifest pin, or test output. A separate patch corrects the input validation; no mathematical statement needs correction. The original packet remains unchanged.

This is an independent AI-assisted mathematical and computational audit, not human peer review, a formal proof certificate, a proof of the cited sieve theorem, or an exhaustive literature review.

## 1. Audited object and source alignment

The frozen author's MANIFEST.json has SHA-256:

1e69db6319607fb6cb9a207193701dbb2fc38e5fe3cd0c799df44a49f6963799

All 12 listed members match their sizes and hashes. The exact flat inventory matches; both the author's verifier and an independently written inventory check pass. The original manifest and member bytes were checked again after all tests.

The mathematical target was checked against Granville's Problem 7 on printed page 3025 of [Oberwolfach Report 53/2016](https://publications.mfo.de/bitstream/handle/mfo/3557/OWR_2016_53.pdf?isAllowed=y&sequence=1). That question expressly assumes distinct rational prime factors congruent to 1 modulo 4. It asks whether the indicated lower-bound scales can be achieved for close clusters. Its displayed prime-factor count is not a prescribed cluster cardinality.

The report's precise convention is appropriate: for each fixed cluster size m, seek infinitely many n tending to infinity and a cluster on x²+y²=n whose containing arc is O(R^e), R=√n. No uniform assertion over all admissible n is implied. No particular number of prime factors is prescribed. A claim for unrestricted integer norms would be insufficient.

For a small cluster, arc length and diameter have the same leading asymptotics. To make the report's angle-lifting argument explicit, fix one point. If D/R tends to zero, every other angle has a lift within O(D/R) of it. The span of these lifts is less than π for large R. The two extreme points then determine the diameter, and L=2R arcsin(D/(2R))=(1+o(1))D. Thus the exponent translation is valid.

The audited source PDFs have the same byte counts and SHA-256 hashes listed in the author's SOURCES.json. The theorem image and the exact OWR problem page were visually inspected. The public audit includes no source PDF, source extract, screenshot, raw dataset, or private coordination material.

## 2. The squarefree-value dependency

The cited [Booker–Browning paper](https://discreteanalysisjournal.com/article/732-square-free-values-of-reducible-polynomials) was published in June 2016. The [arXiv version history](https://arxiv.org/abs/1511.00601) identifies the January 2017 v3 as a reformatting of the previous version. Theorem 1.1 uses the introductory assumptions that H is a nonconstant squarefree integer polynomial, adds no fixed prime divisor and irreducible-factor degree at most three, and yields a bounded-prime-factor squarefree subsequence. Its lower bound is of order x/(log x)^κ, with κ the number of irreducible factors. This is sufficient for infinitude of positive parameters here.

Do not replace that conclusion with a positive-density claim based on this theorem alone. The author's report does not do so. The hypothesis is “no fixed prime divisor,” stronger than absence of a fixed square divisor. Both hold for the triple polynomial because H(0)=1. For the balanced family the report proves the stronger fixed-prime condition directly.

The audit checks the application of this published theorem, not its analytic proof or numerical sieve constants. No prime-value conjecture, quartic squarefree-value conjecture, or squarefree Fibonacci theorem is silently substituted for it.

## 3. Route 1: geometry and the prime-radius quantifier

The area argument is correct for every circle centered at the origin containing three distinct integer points. Equal norms modulo two allow at most two coordinate-parity classes. A pair in the same class gives an even side vector; the determinant against the third vertex is a nonzero even integer. Thus the triangle area is at least one.

With side lengths a,b,c, its circumradius is R and abc=4RΔ≥4R. On a shortest containing arc, write the two successive positive subarc lengths as s,t. Each corresponding chord is strictly shorter than the subarc, so abc<st(s+t)≤(s+t)³/4. Therefore L³>16R. This remains valid even if the containing arc is not minor. The strict inequality concerns actual finite configurations; asymptotic equality in the normalized bound is possible.

For n=p prime, p≡1 mod 4, the eight points are the signed coordinate permutations of one representation p=a²+b², 0<a<b. Their successive angular gaps alternate between 2θ and π/2−2θ. Any three consecutive points span exactly π/2, while any containing arc for three points must span at least two successive gaps. Hence the least three-point containing arc is exactly πR/2. This is a valid obstruction to the stronger, incorrect “every admissible n” assertion. It does not obstruct an infinite subsequence of composite admissible n.

The independent controls enumerate 5,600 triangles on norms up to 150 and verify the exact determinant and circumradius identities. They also check all eight-point configurations for the 44 primes p≤500 with p≡1 mod 4, using exact polar ordering and orthogonality rather than floating-point angle comparisons.

## 4. Route 2: the sharp squarefree triple

The report correctly credits the construction and classical normalization to [Cilleruelo–Granville, Close Lattice Points on Circles](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/E14DBCBF07B4B98FECF3282E2BA672B5/S0008414X00004296a.pdf/close-lattice-points-on-circles.pdf), Theorem 1.2 and its opening example. The audit independently expands the supplied coordinates.

The three norms are exactly

H(t)=16t⁶+4t⁴+4t²+1=(4t²+1)(2t²+2t+1)(2t²−2t+1).

The factors have discriminants −16,−4,−4 and pairwise resultants 20,20,32. They are primitive, irreducible over Q and distinct, so their product is a squarefree polynomial. The common constant term one excludes every fixed prime divisor. They are positive for positive t. The sieve dependency therefore produces infinitely many positive t with squarefree H(t), and H(t) tends to infinity along that subsequence.

Each factor is an odd sum of two coprime squares: (2t)²+1, t²+(t+1)², and t²+(t−1)². If an odd prime 3 modulo 4 divided one, it would divide both coordinates, contradicting the displayed gcds. No factor is even. Thus every prime factor of H(t) is 1 modulo 4 even before squarefreeness is imposed. On the sieve subsequence all required arithmetic restrictions hold.

The independent polynomial computation confirms the three squared distances as 4t²−4t+2, 4t²+4t+2, and 16t²+4, and the oriented double area as −2. The extreme points and the middle point have the asserted polar order, in the right half-plane for t≥1. Consequently the endpoint chord d=√(16t²+4) determines the containing minor arc. Since R∼4t³ and d∼4t, the limit L/R^(1/3)=16^(1/3) follows. The constant can also be checked without a floating-point limit: the leading coefficient ratio in d⁶/H is exactly 256, the square of 16.

Together with Route 1 this establishes the sharp infimal limiting arc constant in the squarefree split-prime class. It is not just an unrestricted construction. The diameter along this construction has the same limiting constant; by the small-cluster arc/diameter relation, an allegedly smaller asymptotic diameter constant would contradict the arc lower bound.

The samples behave as claimed: t=1 gives 25 and is inadmissible; t=2 gives 1105=5·13·17. Independent exact factor checks find 480 squarefree parameters among 1≤t≤1000. That finite count is only a control and is not a density estimate or infinitude proof.

## 5. Route 3: Gaussian divisibility and balanced prime assignments

For a squarefree split n and a Gaussian integer z with N(z)=n, exactly one member of each conjugate prime pair above p|n divides z, and its exponent is one. A difference of two points sharing one Gaussian prime is divisible by it. Multiplying over unordered pairs and then taking the rational integer norm produces p to at least binom(a_p,2)+binom(m−a_p,2).

Every point has odd norm, so its coordinates have opposite parities; modulo 1+i every point is congruent to one. Every difference therefore contributes a factor of two to its norm. These powers of two are coprime to the odd-prime divisors already obtained.

Writing M=binom(m,2) and E=floor((m−1)²/4), the exact divisor is 2^M n^E B, where B is the report's nonnegative-excess product. Since the product of squared pairwise distances is at most D^(2M), its lower bound gives precisely

D≥√2 R^(E/M) B^(1/(2M)).

There is no missing square root or factor of two in this formula. For even m=2s, the excess is (a−s)²; for odd m=2s+1, it is (a−s)(a−s−1). These are nonnegative integers. The exponents for m=3,...,7 are exactly 1/3,1/3,2/5,2/5,3/7.

If D≤C R^(E/M), then B≤(C/√2)^(2M). Any p larger than this upper bound cannot have positive excess. Thus its assignment is balanced. The result is necessary, not sufficient: it does not construct compatible points or solve the geometry. The independent controls test 52,828 distinct subsets on four admissible circles and verify both the divisibility and diameter inequality exactly. The imbalance formulas are checked for all m from 2 through 200.

## 6. Route 4: the Fibonacci family and the squarefree gap

The three-factor squared-radius formula and four points agree with the inspected publisher version of the cited circle paper. The factor F_(2u+1) must be present. Its omission is incompatible with the norm identity and is rejected by the controls. The supplied u=4 example has common norm 98345=5·13·17·89 and squared diameter 890.

The three odd indices 2u−1,2u+1,2u+3 are pairwise coprime: their pairwise differences are two or four. The Fibonacci gcd identity then makes the three Fibonacci values pairwise coprime. Exactly one index is divisible by three. The period-six recurrence modulo four gives valuation exactly one at the corresponding even Fibonacci value. Dividing that value by two therefore leaves three pairwise coprime odd integers G_j and N_u=5G_1G_2G_3.

Squarefreeness of N_u is equivalent to squarefreeness of each G_j and avoidance of five in all three. The zero positions of Fibonacci numbers modulo five are exactly the multiples of five, giving u≡0 or 4 modulo five. This condition alone does not exclude other repeated prime factors. If N_u is squarefree, the integral norm representation and oddness imply that every prime factor is 1 modulo 4: a prime 3 modulo 4 dividing a sum of squares would divide both coordinates and force its square into the norm.

The size estimates are also consistent: N_u grows like a positive constant times φ^(6u), and the squared diameter is 10F_(2u+3), so the arc scale is O(R^(1/3)). The 299 parameter checks u=2,...,300 verify the exact norms, diameter, coprimality, two-adic property and five-avoidance equivalence.

The unresolved step is indeed an infinite simultaneous squarefree subsequence of the three recurrence-derived factors. The polynomial sieve theorem does not apply to the parameter u in this exponential recurrence family. The report correctly stops at a sufficient criterion for this family and does not assert that failure to prove it rules out all other constructions.

## 7. Route 5: larger clusters at a weaker exponent

For fixed s≥2, d=2s, and B the product of rational primes at most 2d, the factors B²(t+j)²+1 are irreducible quadratics with distinct roots. Their product has no repeated polynomial factor. For p≤2d it is one modulo p; for p>2d it has degree 2d<p and nonzero leading coefficient modulo p, so it cannot vanish at every residue. These cases exhaust all primes and establish the sieve hypothesis, not merely an absence of obvious local squares.

The squarefree subsequence makes the rational norms pairwise coprime. Within any one norm, a_j+i and a_j−i have no common Gaussian prime because a common divisor would divide 2i and the norms are odd. Changing one sign therefore changes a Gaussian prime valuation that no other factor can supply. The resulting balanced-sign products are all distinct, including any potential equality up to a unit.

The degree-d and degree-(d−1) coefficients agree across all balanced sign choices. Differences have degree at most d−2. There are only binom(2s,s) choices for fixed s, and their real parts are asymptotically B^d t^d>0, so they share a small arc. The resulting bound is L=O_s(R^(1−1/s)). For s=2 this yields six distinct points on infinitely many admissible circles at exponent 1/2. This does not close the exponent gap for four, five or six points.

Independent Gaussian polynomial multiplication verifies the norm identities and coefficient cancellation for all 96 balanced choices at s=2,3,4. It also verifies the supplied six-point sample by exact coordinates and norm factorization. These symbolic finite-degree checks complement the general proof.

## 8. Later-source and priority limits

The cited [Temur preprint](https://arxiv.org/abs/2012.10784) was checked at Theorems 5 and 6 and the surrounding scope discussion. Theorem 5 fixes the coordinate offsets before its finiteness conclusion; Theorem 6 is restricted to a near-square range and counts points. Neither is the missing moving-cluster squarefree construction. A fresh bounded public search did not locate a source overturning the report's stated gaps. This is not a proof of worldwide open status.

The author's corpus and remote prior-attempt search records are bounded provenance claims. This audit does not certify every historical branch, every corpus record, or novelty. No new remote repository write was made. The mathematical acceptance does not rely on a novelty claim or on absence of prior attempts.

## 9. Validation findings, correction, and acceptance boundaries

The original fixed packet passes all of its 6 positive portability runs and 39 hostile cases. Its normal, -O and -OO runs preserve explicit checks. However, under a deliberately recomputed manifest pin, the original verifier also accepts seven ambiguous or type-invalid variants:

1. A floating-point encoding of the four-point norm.
2. A floating-point encoding of one four-point coordinate.
3. A floating-point encoding of one balanced-product coordinate.
4. A duplicate claim key whose last value is valid.
5. Boolean true as manifest schema version.
6. Floating-point 1.0 as manifest schema version.
7. A duplicate manifest key whose last value is valid.

The coordinate defects arise because equality between Python integers and equal-valued floats succeeds, after which the checker validates regenerated integer coordinates instead of the supplied coordinates. The schema-version defect has the same equality issue. The default JSON decoder silently keeps the last duplicate key. These are validation gaps, not counterexamples to the mathematics. An unchanged external pin still rejects every changed input; none of these variants bypasses the original frozen pin.

VALIDATION_HARDENING.patch changes validation to inspect the supplied witness norm and points, requires an exact integer schema version, and rejects duplicate keys and nonfinite JSON constants. It expands the author's hostile suite from 13 to 21 cases per interpreter mode. The original mathematical output remains byte-for-byte unchanged.

The hardened packet passes 6 positive and 63 hostile controls. A separately written mathematical checker, which does not import the author's code, performs 101,403 exact checks. Its independent harness passes 6 positive runs, 48 malformed/false-claim cases, reproduces all 21 original permissive cases across the three interpreter modes, and confirms all 21 are rejected by the hardened version. Normal, -O and -OO independent outputs are identical. Read-only relocated runs leave bytes unchanged.

The patch makes no correction to the proof and no escalation of the result: full_problem_solved remains false, novelty_claim remains false, and the larger sharp squarefree problems remain unresolved. ACCEPTANCE.json records the final hardened pin and the artifact inventory. The author's original “independent audit pending” text is preserved as checkpoint history; this separate audit is the acceptance record.
