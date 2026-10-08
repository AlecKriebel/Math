# Independent audit: universal nonabelian SU(2) surgery slopes

Problem KP-1.14, record 2673, rank 1039. Reviewed 2026-10-08.

## Disposition

**Accept as partial mathematical progress, not a solution of the universal classification.** The published-input corollary for reduced slopes with 0 < |p/q| < 7 and |p| = 4ℓ^e, where ℓ is odd prime and e ≥ 1, is valid. No correction to the frozen original report or code is required. Its five approaches remain five approaches. The supplement below strengthens the fifth approach without adding another approach or claiming novelty.

The ≤8 extension remains conditional on the identified Ghosh–Miller Eismeier preprint and its foundational dependencies. It must not be described as part of the published-only theorem. All finite checks are arithmetic and integrity safeguards; none certify gauge theory, the universe of knots, literature completeness, or novelty.

The original eight-file bundle is unchanged. ORIGINAL_FREEZE.json records each file's external audit hash and size, including its original manifest. No source documents, copied source passages, dataset contents, or private coordination material are included here.

## 1. Identity, conventions, and source attribution

The inspected K3 preliminary volume identifies the question as Problem 1.14 on printed page 24, with John Baldwin as scribe. It asks about every nontrivial knot, not only prime or hyperbolic knots. Coefficient zero is outside this question; infinity is not rational. We use reduced p/q with q > 0, the standard positively linked meridian, and the zero-linking Seifert longitude.

For p ≠ 0, the filled manifold has first homology Z/|p|. Therefore an abelian SU(2) image is cyclic. Reducibility of a complex two-dimensional unitary representation is equivalent to abelian image, but reducibility of the filled three-manifold is a different property. No irreducibility hypothesis on that manifold is introduced. Mirroring changes r to −r and reverses the manifold orientation, preserving the existence of the required group representation.

The exact published inputs used by the original proof were checked against the retained source bytes. The publisher-hosted BS online-first text was additionally checked at [EMS Press](https://ems.press/content/serial-article-files/32949). It agrees on Proposition 9.1, Theorem 1.15, Corollary 7.13, and Lemma 9.5. This additional web inspection supplies no new PDF byte hash. The original source registry accurately distinguishes manuscript bytes from final-published bytes.

Klassen's original full PDF was not independently recovered. Attribution must continue to say that the required consequence is inspected in BS Lemma 9.5 and the published BLSY proof of Theorem 6.2. This is adequate for the stated dependency audit: both explicitly give the count (det(K)−1)/2 and the needed descent. It is not a claim to have independently audited Klassen's complete proof.

## 2. Approach 1: trefoil character and peripheral calculation

**Accepted, including all signs and endpoints.** For the positive trefoil use x² = y³ = h, μ = xy⁻¹, and λ = hμ⁻⁶. Centrality forces h to be scalar in a nonabelian SU(2) image. The choice h = +1 would make x scalar, so h = −1. The noncentral options are x a unit imaginary quaternion and y = 1/2 + (√3/2)v. The excluded cases v = ±x are exactly the commuting endpoints. Thus the meridian angle ranges over the open interval (π/6,5π/6).

Filling imposes (p−6q)α + qπ ∈ 2πZ. Writing d = |p−6q|, the available α are kπ/d with k ≡ q modulo 2 and d/6 < k < 5d/6. For d = 0, reduction forces (p,q) = (6,1); the scalar filling relation is −1 = 1 and fails. For d = 1 there is no witness. If d = 2, reduction forces q odd and k = 1 works. For d = 3 one may choose k = 1 or 2 according to q's parity. For d ≥ 4 the interval has length greater than 2 and meets both parity classes.

Consequently the positive trefoil filling has a nonabelian SU(2) representation exactly when |p−6q| ≥ 2. Its exceptional rational coefficients are precisely 6 and 6±1/n for n ≥ 1. Negative p cause no additional exception for this positive trefoil; the mirrored knot supplies the reflected obstruction. The scalar argument also explains why the reducible filling at 6 is a valid counterexample.

This agrees with [Sivek–Zentner, Proposition 4.3](https://arxiv.org/abs/1912.01866v2). For general nontrivial torus knots, products ab±1/n and the additional product coefficient when a factor has absolute value 2 are used only as exclusions. Absence of one such obstruction is not a universal affirmative certificate.

## 3. Approach 2: automatic nondegeneracy and its precise failure

**Accepted.** Squaring maps the pth roots onto the Nth roots, where N = |p|/gcd(|p|,2). A primitive dth root zero of the Alexander polynomial forces the integral cyclotomic factor Φ_d after multiplying by a Laurent monomial. Evaluating at 1 rules out d = 1 and all prime powers. Thus N equal to 1 or a prime power is sufficient for every knot. This is exactly the numerator class stated in the report, with the small values 1 and 2 included explicitly.

The conversion from a hypothetical SU(2)-abelian positive filling to an instanton L-space requires this nondegeneracy. BS then supplies 2g−1 ≤ r; r < 5 implies g ≤ 2. The genus-one knot is the positive trefoil, while [Farber–Reinoso–Wang, Corollary 1.4](https://msp.org/gt/2024/28-9/gt-v28-n9-p07-p.pdf) identifies the positive cinquefoil in genus two. Their first SU(2)-abelian positive slopes are 5 and 9, respectively. This excludes both in the required open interval.

When the cyclotomic condition fails, the genus upper bound is unavailable. The original report correctly avoids combining that unavailable bound with the independent lower bound deg Δ ≥ φ(d). Orders 12 and 15 genuinely survive the two evaluation tests used later. These polynomial obstructions are not constructions of exceptional surgeries.

## 4. Approach 3: determinant descent and the 4ℓ^e theorem

**Accepted, with no added primeness assumption on the knot.** In the binary-dihedral group D = S¹ ∪ S¹j, a meridian of a nonabelian image must lie outside S¹. Otherwise normal generation would force the whole image into S¹. Such an element has square −1 and fourth power 1. The Seifert longitude belongs to the knot group's second derived subgroup, whereas D has trivial second derived subgroup. It therefore maps to 1.

The representation consequently descends whenever 4 divides p, for every denominator q, without changing its nonabelian image. The Klassen count, in the inspected published restatements, supplies such a representation whenever det(K) > 1. A hypothetical SU(2)-abelian filling with 4|p must therefore have det(K) = 1. This descent is reproduced explicitly for arbitrary q in the [published BLSY proof of Theorem 6.2](https://msp.org/gt/2024/28-4/gt-v28-n4-p07-p.pdf), not merely asserted from the special coefficient 4 in BS.

For p = 4ℓ^e, N = 2ℓ^e. Every remaining possible non-prime-power divisor of N has form 2ℓ^j, 1 ≤ j ≤ e. Its cyclotomic value at −1 equals ℓ. Divisibility of the Alexander polynomial by that factor would make ℓ divide Δ(−1), contradicting det(K) = 1. Hence the nondegeneracy hypothesis is restored.

For 0 < r < 7, the genus bound gives g = 1, 2, or 3. The genus-one determinant is 3. The published BLSY proof supplies the complete genus-two/three Alexander-polynomial alternatives used here, whose determinants are 5, 7, and 3. All contradict determinant one. Mirroring proves the negative half of the result. The strict upper bound 7 is retained; the argument does not silently exclude genus four at r = 7.

The more general necessary condition in the original report also follows: an exceptional filling with 4|p and 0 < r < 7 needs a divisor d of |p|/2 with Φ_d(1) = Φ_d(−1) = 1. If no such zero exists, the same instanton L-space and determinant contradiction applies.

## 5. Approach 4: conditional characteristic-two extension

**Accepted only with its declared preprint dependencies.** Fresh checks of the [Li–Ye arXiv entry](https://arxiv.org/abs/2511.17877), [Fan Ye's page](https://fanye.scholars.harvard.edu/), [Ghosh–Miller Eismeier arXiv entry](https://arxiv.org/abs/2511.18885), and [Mike Miller Eismeier's page](https://millereismeier.github.io/) support the report's stated manuscript status. Li–Ye's stated prime-power-or-twice-prime-power result has the open range 2 < r < 6. The later ≤8 deduction uses the separate characteristic-two result. The author's foundational indefinite-cobordism draft is public, while the small-dg-module book remains listed as forthcoming. Those foundations have not been audited here.

Here is a direct derivation of the numerical step, avoiding the inconsistent floor symbols in the GME text. For a positive nondegenerate SU(2)-abelian filling, its untwisted characteristic-two instanton dimension is p. Let R and M be the integers from Theorem 1.3, with R ≥ |M| and both divisible by 4. At r = M the exceptional dimension R+2 is larger than p = M, so equality is impossible. Away from that coefficient the equation is

R + |r−M| = r.

It forces M ≥ 0, r > M, and R = M. Every rational t > M then also has minimal characteristic-two dimension. Universal coefficients and the Euler-characteristic lower bound imply minimal complex dimension at those t. BS's instanton L-space slope characterization consequently gives 2g−1 ≤ t for every t > M, so 2g−1 ≤ M. Since the knot is nontrivial, g ≥ 1 and M > 0.

Thus 0 < r ≤ 8 forces M = 4 and g ≤ 2. Published small-genus classification leaves only trefoil and cinquefoil; the latter has no exceptional slope through 8. The former contributes exactly the previously identified family. For p = 4ℓ^e the determinant argument restores nondegeneracy and then excludes the trefoil as well. This proves the conditional extension with the endpoint 8 included.

More generally the correct rounded lower bound is

M ≥ 4 ceil((2g−1)/4) = 4 ceil(g/2),

which is 2g for even g and 2g+2 for odd g. The arithmetic is derived from integrality, not copied from a floor expression. The original preprint's page 4 was visually inspected to distinguish its actual printed symbols from extraction artifacts.

## 6. Approach 5: closure fails even for the universal set

**The original argument is accepted. This supplement strengthens it.** Let U denote exactly the universal set in the original question. For every integer k ≥ 4 define

p_k = 2^k,   q_k = (2^(k−1) + (−1)^k)/3,   r_k = p_k/q_k.

1. Since 2 ≡ −1 modulo 3, the numerator defining q_k is divisible by 3. It is odd, so the resulting integer q_k is odd.
2. For k ≥ 4 this numerator is at least 7, and its positive integral quotient is at least 3. Therefore q_k ≥ 3.
3. Since p_k is a power of 2 and q_k is odd, gcd(p_k,q_k) = 1. These are reduced slopes with positive denominators.
4. Direct calculation gives p_k−6q_k = −2(−1)^k. Hence |r_k−6| = 2/q_k ≤ 2/3 < 1, so 5 < r_k < 7.
5. The published BLSY Theorem 6.2 applies to every r_k, establishing r_k ∈ U for every k ≥ 4, for all nontrivial knots.
6. As k tends to infinity, q_k tends to infinity and r_k tends to 6. The trefoil calculation proves 6 ∉ U.

Thus U is not closed even as a subset of the nonzero rationals with their ordinary topology. Mirroring gives the analogous failure at −6. The sequence alternates sides of 6 and uses only the already published power-of-two theorem. This is a consequence of that theorem, with no novelty assertion and no extra approach count.

The original fixed-trefoil sequence remains valid. Its additional lesson is that filling relations change with the numerator and denominator; a fixed irreducible representation can satisfy every relation in a converging slope sequence while failing the limiting relation. Compactness of a representation space does not repair that issue.

## 7. Independent computation and integrity review

Both the author suite and independent suite passed in normal Python, -O, and -OO, with mode-identical output. The author suite retains its original 5,860 slope checks, 149 cyclotomic evaluations, 78 divisor checks, and 49 density controls.

The independent suite checks:

- 23,492 reduced signed slopes in |p| ≤ 240 and 1 ≤ q ≤ 80, using separately implemented numerator and torus tests;
- 3,678 trefoil witnesses using closed-form strict integer bounds instead of the author's witness search;
- 160 entire cyclotomic polynomials constructed by Möbius products and constant-term division, independent of the author's proper-divisor recurrence;
- 5,000 numerator-class comparisons and 251 residual divisor cases;
- 1,000 exact rounding cases, 97 terms of the universal nonclosure sequence, and six exact CLI boundary cases;
- 51 hostile CLI cases per mode, including both Boolean fields, floats, strings, arrays, nulls, duplicate keys, nonfinite values, exponent overflow, 5,000-digit integers, bad reduction, unknown fields, and input bounds;
- 41 integrity attacks per mode, including linked roots and files, malformed or oversized manifests, path traversal, extra entries, exact byte-count types, invalid hashes, changed bytes, missing bytes, and bad external pins.

The original author script, author verifier, and independent arithmetic suite all ran in every mode as uid 1000 from a 0555 directory containing 0444 files. An attempted write was actually denied. Before/after byte snapshots match, including the original source bundle. Eleven retained public-source PDF byte counts and hashes match the original source registry.

Schema attacks with intentionally recomputed test pins only exercise parser branches; they do not purport to defeat a trusted original external pin. The integrity verifier is not a race-safe hostile-filesystem sandbox. Helpers are tested in their documented fixed-bundle/CLI scope, not claimed as unrestricted public APIs. The field unresolved_by_this_audit follows the published-only decision boundary even when the separate conditional-preprint flag is true; this is consistent with the original explanatory text.

## 8. Exact remaining scope

The universal set U remains unclassified. In particular, the methods here do not settle 15/4 or 24/5, and the audit makes no literature-wide open-status claim for either coefficient. No exceptional surgery is constructed at those two slopes. Neither a finite successful test grid nor exclusion of all tested torus knots supplies a proof for all knots.

The final disposition is therefore **accepted partial progress, five approaches, unchanged original freeze, conditional preprint extension separated, and an additional published-input nonclosure consequence in this audit supplement**. No source correction patch is required because no incorrect mathematical or documented CLI claim was found.
