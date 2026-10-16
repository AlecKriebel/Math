# Independent adversarial review: arrangement 30004601

Reviewed 2026-10-01 UTC. Frozen artifact: `CANDIDATE_PROOF.md`, SHA-256 `f31cc44405f91c91af044f7d6a8306faa38c9221ad8a23c639d80bba251e4ef9`.

## Verdict

**PASS: full counterexample to the corrected primary-source conjecture.** Over characteristic zero, the arrangement

    Q = x y (x−y) (x−2y) z w (x+z+w)

has second-variable pure-power threshold 8 in its degree-reverse-lexicographic generic initial Jacobian ideal, and has a minimal generator of degree 7 involving the third variable. The proof establishes the needed generic section values algebraically. No genericity conclusion rests on a single specialization. No mathematical correction is required in the frozen proof.

This is a correctness verdict for the explicitly corrected conjecture, not a certification of priority, novelty, or minimality of the number of hyperplanes. It does not refute the easier mistranscribed statement using the first variable. No additional proof-search turn was consumed by the review.

## Primary-source and convention audit

The [OWR Report 5/2021, printed p. 234, Conjecture 7](https://ems.press/content/serial-article-files/46883) uses the least exponent of the **second** variable and bounds minimal generators involving the third. The printed page was inspected visually. [Bigatti–Palezzato–Torielli, Conjecture 5.7](https://arxiv.org/pdf/1801.09868) gives the same bound with a reduction-number shift of one; Theorem 6.2 supplies the generic-section identity used here. Their variables are ordered x1>x2>… in degree reverse lexicographic order and the field has characteristic zero.

The [final Marchesi–Palezzato–Torielli paper, Port. Math. 83 (2026), pp. 1–18](https://ems.press/content/serial-article-files/52275), still states the general conjecture as Conjecture 4.6 and proves the three-variable arrangement case in Theorem 4.7. That paper numbers variables starting at zero, so its second-variable threshold is written with x1 and its third variable with x2. The four-variable example here does not contradict their three-variable theorem.

## Algebraic audit

1. **Actual arrangement and ideal.** All seven factors are homogeneous, distinct, and linear over characteristic zero. The coordinate factors give rank four, so the arrangement is central and essential. Q has degree 7; its four ambient partial derivatives have degree 6. Euler's identity, 7Q=xQ_x+yQ_y+zQ_z+wQ_w, puts Q in their ideal. Thus this is precisely the arrangement Jacobian ideal, not an unrelated equigenerated ideal.

2. **Restrictions are handled correctly.** The section ideal consists of restrictions of all four ambient polars. It is not silently replaced by the Jacobian ideal of the restricted product, which in three variables would have only three partial derivatives. This distinction is essential to the example.

3. **Genericity is genuine.** Independence and pairwise nonproportionality of the restricted factors are open conditions on the injective section map. The given nested flag satisfies them, establishing nonemptiness. On every such three-dimensional section, X,Z,W are independent; on every such binary section, X,Z,W have exactly one relation. The relevant parameter and flag spaces are irreducible, so these nonempty opens meet the generic-coordinate open used for the reverse-lexicographic initial ideal. There is no reversal of semicontinuity.

4. **All degree-one syzygies are counted.** Reducing a polar relation modulo each distinct factor L_i forces its corresponding linear coefficient U_i to be divisible by L_i. The product of the other factors is nonzero modulo L_i. Hence U_i=λ_i L_i, and the relation is equivalent to sum λ_i=0. This implication is reversible. Applying the same argument to constant coefficients proves independence of the four degree-6 polars.

5. **Scalar compatibility has the claimed dimensions.** The four-member pencil forces one scalar a for X,Y,X−Y,X−2Y. The other scalars b,c,d satisfy (a−d)X+(b−d)Z+(c−d)W=0 and 4a+b+c+d=0. In three dimensions the former equation makes all four scalars equal, and the latter gives 7a=0. In two dimensions the former equation has the displayed two-parameter description; its trace condition has nonzero coefficient 7 on d, leaving exactly one dimension. The map to actual syzygy coefficients is injective. This checks both rank bounds, not merely existence of one syzygy.

6. **The binary cutoff is fully proved.** If the four binary polars had a common projective zero, restricted Euler would force one factor to vanish there. Exactly one vanishes, by pairwise nonproportionality, and the polar vector is then a nonzero scalar times that factor's nonzero ambient normal vector. This contradiction gives height two after algebraic closure, hence over the original field. Four minimal degree-6 generators therefore have a free syzygy module of rank three by Hilbert–Burch. The Artinian numerator's double zero at 1 gives total coefficient degree 6. Exactly one degree-one syzygy forces degrees 1,2,3. Thus H2(6),H2(7),H2(8) are 3,1,0 for generic binary sections.

## Generic-initial-ideal inference

The classical reverse-lexicographic generic-section identity gives the Hilbert functions of B∩K[x1,…,xi], where B=rgin(J). Strong stability is available in characteristic zero.

For the binary quotient, nonzero degree k is equivalent to x2^k being standard: if x2^k were in B, strong stability would put every binary degree-k monomial in B. Consequently H2(7)=1 and H2(8)=0 prove that the threshold is exactly 8.

For the three-variable quotient, multiplication by x3 has kernel dimension

    H3(k−1)−H3(k)+H2(k).

The verified values give zero at k=6 and one at k=7. There are no ideal elements below degree 6. Therefore no generator involving x3 can occur through degree 6, while some degree-6 standard monomial m is killed by x3 in degree 7. A minimal generator dividing x3m must involve x3, otherwise it would already divide m; its degree is consequently exactly 7. It is also minimal in the full four-variable ideal because its divisors cannot involve x4. This verifies the strict violation 7<8 without guessing an explicit full gin.

The generic three-variable degree-8 Hilbert value is not needed or asserted in the proof. The value 24 at that degree is only an explicit-flag diagnostic, as stated by the author.

## Independent exact certificates

The author checker was inspected but not executed. The separate standard-library program `independent_rank_certificate.py` independently expands the seven factors, differentiates before restriction, checks Euler's identity, constructs all six Macaulay matrices, and row-reduces over exact rational numbers using `fractions.Fraction`.

All recorded ranks agree:

- Three variables in degrees 6,7,8: ranks 4,12,21 in matrices of sizes 4×28, 12×36, 24×45
- Two variables in degrees 6,7,8: ranks 4,7,9 in matrices of sizes 4×7, 8×8, 12×9

`RANK_CERTIFICATES.json` includes every matrix, monomial/multiplier ordering, an invertible rational row transformation E, and RREF R. The checker verifies E M=R entry by entry, invertibility of E, and every pivot/zero-row condition. It also checks a nonzero original-matrix minor for each rank. The six determinants, in the order above, are:

    −359424
    4109478395904
    −87259283473884512256
    782480160
    −181324946880000
    −8016077405952000000

These provide independently checkable upper and lower rank certificates. The displayed binary syzygy is also verified exactly as a polynomial identity. All six author-manifest hashes match their frozen files. The receipt `INDEPENDENT_CHECKS.json` records the independent checker and certificate hashes.

## Scope and publication recommendation

The full mathematical counterexample survives this adversarial audit. Keep the original x2 source correction visible, attribute all classical generic-initial/Hilbert–Burch inputs, and preserve the distinction between the proved three-variable arrangement theorem and a three-variable section of a four-variable Jacobian ideal. Historical substantive-turn uncertainty must not be reset; the candidate was found in one documented recovered author turn, and this review adds none.

A bounded primary-source search corroborated that the cited 2026 paper retains the general conjecture; it did not certify exhaustive novelty or priority. No claim of a smallest counterexample is supported. Public review artifacts consist of this report, the independently authored checker, its receipt, and the rational certificates. Full downloaded PDFs, source-page images, and environment-specific paths are excluded. The reviewer made no remote writes or publication action for this arrangement.

Review completion: **100% for the frozen full candidate**.
