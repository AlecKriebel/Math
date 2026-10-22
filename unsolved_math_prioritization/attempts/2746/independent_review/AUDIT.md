# Independent adversarial audit: KP-1.87 / problem 2746

Date: 2026-10-04 UTC. Frozen packet: rank 592, five approach families.

## Verdict

**PASS for the expressly stated partial mathematical results, with three nonblocking precision clarifications.** No proof or counterexample to the universal Benedetti-Shiota conjecture is present. The proper research disposition remains **unsolved, 5/5**; the audit is not a sixth proof attempt. No novelty claim is justified or made.

The smooth realization, analytic finite-jet transfer, explicit weak-versus-isolated examples, braid polynomialization criterion, and Alexander-polynomial calculations survive independent scrutiny. The main precision issue is that the norm identity in Proposition 5B obstructs **free period 2**. Its heading should say “odd/freely 2-periodic,” rather than suggesting that every free period is tested. This does not change the Newton-class consequence: Bode's odd symmetry is the antipodal involution, which has order two.

A separate suggested patch expands the valid Laurent-unit normalization and makes the Fourier coefficient convention explicit. The frozen packet was not edited.

## Scope and integrity

The accepted frozen manifest SHA-256 is:

`8cb2ac21552e6543d1eb06a5a79d1ec6ce0a9c42c97265504150d04ab43aaa35`

All six entries verified exactly:

- public/README.md
- public/PROOF.md
- public/SOURCE_STATUS.md
- public/APPROACH_LOG.md
- controls/check_controls.py
- controls/CONTROL_RESULTS.json

These six paths plus SHA256SUMS are exactly the audit request's proposed publication allowlist. There are no unexpected manifest entries, links into private material, or source PDFs in that allowlist. The full script output is byte-identical to the frozen CONTROL_RESULTS.json. All 28 entries in the private provenance inventory also match both byte counts and hashes. This does not independently revalidate the two full imported-corpus hashes mentioned in SOURCE_STATUS: the full corpora are not among the supplied packet files.

All audit output is in a separate sibling directory. Private source PDFs, source text extractions, the K3 screenshot, provenance inventory, and audit coordination remain excluded from the original publication allowlist. The suggested patch has not been applied. No remote write, queue change, branch change, findings-cell edit, or external communication was performed.

## 1. Exact target and source status

The actual K3 author's preliminary PDF, rather than a short workshop summary, was inspected through its complete text and the supplied page image. Printed page 78 states the isolated real-polynomial R4-to-R2 realization question. Page 79 supplies the weak-isolation comparison and O. Saeki attribution. The 436-page PDF and its April 2026 metadata match the packet's account. The original Benedetti-Shiota Conjecture 1.6 and Theorem 1.8/blow-down discussion were checked directly in the supplied primary paper.

Primary references:

- [K3 author's preliminary version](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), Problem 1.87, printed pp. 78-79.
- [Benedetti-Shiota, On real algebraic links in S3](https://people.dm.unipi.it/benedett/BUMI_Shiota.pdf), pp. 585 and 588-589.

No replacement target has been smuggled in: rank two is demanded throughout a punctured neighborhood, and the link is required on every sufficiently small sphere. No prescribed open-book representative or monodromy is claimed to be part of the target.

The recent-paper summaries were checked against the supplied primary texts. The T-homogeneous theorem is a subclass theorem. The canonically-fibered result yields P-fibered representatives while its universal version remains a conjecture in that source. The T-positive and essential-torus results do not assert the universal isolated realization. A DOI opening failed in the web reader, but the exact Springer article URL worked; local primary PDFs were also available. This audit does not certify the absence of every possible later or unindexed result. The earlier live repository duplicate-search findings were inspected as provenance, not independently rerun as a new repository search.

## 2. Proposition 1: smooth realization

**Verified.** The open-book collar supplies a smooth complex coordinate normal to the binding. A positive modulus off the binding can be patched to the normal radius, producing the stated smooth h. The flat radial multiplier dominates every power introduced by Cartesian differentiation.

At a point over the binding, the angular/tangent differential of h is onto. Away from the binding, the radial derivative is a nonzero real multiple of h, while the angular derivative has a nonzero component transverse to h. These give real rank two. The zero set is exactly the radial cone, so the link is preserved on every sphere. At the origin every derivative vanishes.

The stated obstruction to this particular Taylor-approximation route is exact: every finite jet is zero. This is a failure of that transfer method, not a nonexistence theorem for analytic or polynomial realizations.

## 3. Proposition 2: simultaneous isolation and all-small-sphere preservation

**Verified under the stated hypotheses.** For x not zero, RI-xx^T has image the tangent space to the centered sphere and is multiplication by R on that space. Thus the six-minor sum for B detects exactly the needed tangent surjectivity.

Both scalar functions are analytic, nonnegative, vanish at zero, and have no other zero sufficiently nearby. In particular, h_f is positive even where tangent rank fails away from the zero fiber, because its |f|^2 summand is then positive. The scalar isolated-zero Lojasiewicz bounds therefore apply to the intended sets.

For a fixed sufficiently high Taylor degree, the polynomial expressions in f and Df are locally Lipschitz in their bounded arguments. The stated O(|x|^m) error bounds are conservative but valid. Their constants can be chosen uniformly in s in [0,1]. Taking m larger than both lower-bound exponents and shrinking one common ball gives positive d and h for every homotopy member and every nonzero point of that ball.

Consequently:

1. There are no off-zero critical points for any s.
2. Every zero fiber is transverse to every sphere with radius in one common interval.
3. The first jet at zero is unchanged, so zero remains critical.
4. For each fixed sphere, the compact total zero locus projects submersively to [0,1]. A horizontal flow gives an isotopy of links; compactness prevents escape or finite-time loss.

The construction does not rely on a merely annular estimate or on a radius depending on s. No unsupported analytic blow-down is inferred from Benedetti-Shiota. An analytic germ downstairs is indeed still missing in the general realization problem.

## 4. Proposition 3: weak and isolated controls

**Verified.** Both G and H have zero set x=y=0. The positive G minor is R(R+2x^2+2y^2). On that plane the H minor is R^3. On (t,0,t,0), the H second row vanishes and its first row is (4t^2,0,2t^2,0), nonzero for t not zero. These points lie off the zero fiber, so the distinction is genuine.

For the conjugate product, the zero set comprises four distinct complex lines, with only their common origin removed when checking weak isolation. At each remaining zero, exactly one factor vanishes and has surjective differential. At w=0 and z not zero, the product is |z|^4 and its differential is nonzero real-valued, hence rank one. No general link-preserving plumbing theorem follows from multiplication.

## 5. Proposition 4: braid criterion and parity

**Verified, interpreting the coefficient condition as applying to every c_(j,l) not equal to zero, including l=0.** A wording clarification is provided because “nonzero Fourier mode” can otherwise be read as excluding the constant mode.

The rescaling is a diffeomorphism on v not zero. A nonzero complex u-derivative gives real rank two. At a u-critical point the simple-root assumption implies g is not zero, and the radial/time determinant is the stated positive radial factor times Im(conj(g) partial_t g). The condition therefore excludes every critical point off the v-axis.

On the v=0 axis away from the origin, every lower-u term has strictly positive total v/conj(v) degree. Both its value and its u-derivative vanish there. Thus F_u=n u^(n-1), giving rank two even if derivatives in the v directions introduce additional terms. The degree condition makes the origin critical.

For the link argument, put s=|q| and rho=r^k s. The sphere equation is rho^2+r^2=epsilon^2. Equivalently, s=rho/(epsilon^2-rho^2)^(k/2), a strictly increasing smooth function of rho in [0,epsilon). This proves the needed injectivity on each braid page. The implicit radial solution is smooth, including at q=0, and remains so while k varies over positive real values. At k=1 it is the usual closed-braid embedding. Hence the construction preserves the original root braid's closure, not merely its number of strands.

The a=1/4 example has a globally positive critical-angle derivative bounded below by 6/25. Its odd Fourier frequency conflicts with 2k for every integer k. Doubling time squares the braid: the original two-strand monodromy is a transposition, whereas its square has two cycles. The unknot-to-Hopf-link change is real, so squaring is not a general link-preserving repair.

## 6. Proposition 5: arithmetic and precise topological scope

**The arithmetic is verified.** The binary polynomial t^6+t^3+1 has no monic factor of degree 1, 2, or 3. Every reducible degree-six polynomial would have such a factor. The order-of-2-modulo-9 argument is also valid. In the Laurent version of the 2-periodic congruence, strip the lowest nonzero monomial from the binary reduction of q. The normalized product then has nonzero constant coefficient. Irreducibility forces the normalized q to be constant; the geometric sum would have to have degree six and does not equal the target.

For the free-period-two norm identity, allow the most general unit ambiguity:

Delta(t^2) = eta t^b q(t)q(-t), with eta in {+1,-1} and q in Z[t,t^-1].

Write q=t^m Q with Q(0) not zero. The lowest exponent on the right is b+2m, so b+2m=0. Its constant coefficient is eta(-1)^m Q(0)^2=1. Hence the combined sign is +1, Q(0)=+1 or -1, and the identity reduces exactly to Delta(t^2)=Q(t)Q(-t). Its degree forces deg Q=6. Thus no Laurent shift or overall minus sign evades the packet's contradiction.

Squaring in F2[t] is injective, so the normalized Q has odd coefficients exactly in positions 0, 3, and 6. Its middle norm coefficient is 1 modulo 4, while the required coefficient is 3. This proves nonfactorization over the integers with all Laurent-unit conventions accounted for. It does not prove the stronger full irreducibility claim over Q, and the packet correctly disclaims that stronger claim.

An independent implementation tested all 16,384 degree-at-most-six polynomials over Z/4Z, not only the 128 selected parity lifts. There were no norm matches. Precisely 128 candidates matched the norm modulo 2, and all had middle coefficient 1 modulo 4. Its separate coefficient-list binary division also excluded all 14 trial divisors.

**Period precision:** [Hartley, Knots with Free Period](https://doi.org/10.4153/CJM-1981-009-7), Theorem 1.2, has a period-p product over pth roots of unity. The two-factor identity is its p=2 case. Bode's odd symmetry is the antipodal involution, so this is sufficient here; this calculation alone does not exclude every odd free period.

**Newton-class precision:** The published [Bode Part II](https://link.springer.com/article/10.1007/s00574-025-00477-0), Example 4.11 and the paragraph after Lemma 6.3, supplies the exclusion of 8_16 from the convenient, inner-nondegenerate, Gamma-nice class. The packet keeps those hypotheses. The published paper's knot polynomial, fibering assertion, and classification remain credited topological inputs, not outputs of the arithmetic script. No obstruction to all real polynomial germs follows.

## 7. Corrections and publication gate

The separate CORRECTIONS.patch suggests only:

1. Specify “odd/freely 2-periodic” in Proposition 5B's heading and first sentence.
2. State the Laurent-unit normalization explicitly as above.
3. Replace “nonzero Fourier mode” with “coefficient c_(j,l) not equal to zero, including l=0.”

Items 2 and 3 make valid intended arguments unambiguous; item 1 prevents a broader reading than the proof supports. None changes the core result or the unsolved disposition. If adopted, make a new version and new manifest rather than overwriting the preserved frozen packet. Neither these audit files nor any private source is added to the original publication allowlist by this report.

**Strongest checked conclusion:** the packet establishes its conditional analytic-to-polynomial transfer and explicit construction/failure controls, plus a source-dependent obstruction to the specified Newton ansatz. The universal Benedetti-Shiota problem remains unresolved by this work.
