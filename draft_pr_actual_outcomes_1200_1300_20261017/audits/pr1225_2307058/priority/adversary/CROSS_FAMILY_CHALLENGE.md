# Reverse challenge of the frozen classical-energy deduction

Verdict: **PASS for the zero-length branch and its outer-modulus bridge.** No actionable mathematical gap was found in the frozen energy deduction. This does **not** certify an independently supplied proof of the positive-length reduction in that note, an earlier explicitly printed resolution, firstness, current openness, or complete 2019 wording.

This review deliberately began after both initial audit families had frozen. The challenged deduction is `../independent/CLASSICAL_ENERGY_DEDUCTION.md`, SHA256 `ac8bb4d3a6dce6012804afbd1bafd2d5461f758969333e62b4fd3fa3e9d870c5`; the report is `6e7d029b0da77c08a2a5f1c069c6821132aaf7d5c334215a7f8d276756ac99f1`. Its evidence manifest and outside seal match the root-provided pins. All ten members of this family's initial freeze, including the original research/query logs, remain unchanged. This is a new challenge artifact; its explanations below are verification expansions, not edits or repairs to the frozen note.

## 1. Precisely what passes

For a compact set E contained in [0,1] of real Lebesgue measure zero, the following implication is verified:

> If a probability measure on E has finite logarithmic energy, then the planar 2-modulus of **all** globally rectifiable curves joining E to the real complement F=R\\E is infinite.

Positive outer modulus from E to the circle |z|=2 supplies such a probability. The implication consequently covers null-length sets of positive capacity, including Cantor-type sets. For a locally rectifiable endpoint family, the globally rectifiable subfamily already forces the same infinite conclusion. The outer-modulus conventions also agree under the continuous compact-image endpoint convention, as checked below.

The frozen energy note expressly imports the finite-density-to-zero-length reduction from the submitted proof. That positive-length/full-target passage is outside this energy note's independent contribution and outside this challenge verdict. Combining separately validated pieces is an audit-composed deduction; it is not evidence that an earlier author printed this particular application.

## 2. Primary authentication and normalization

[Bagby's official IUMJ scan](https://www.iumj.indiana.edu/IUMJ/FTDLOAD/1968/17/17017/pdf) was freshly fetched during this challenge: HTTP200, 1,273,020 bytes, SHA256 `824ed73036a947158add27c616e89276e1e132bf76c3f981ad3c97961116dd0d`, identical to the frozen source. Visually inspected printed pp.315–318 and Theorem3 on p.323; the intervening OCR was consulted as context, not certified as a complete proof audit.

Bagby's p.315 definition permits a connected open subset R of the sphere whose complement is the union of two disjoint nonempty compact plates A,B. The plates need not themselves be connected. He defines capacity by C1 separating functions for plane condensers and by a Möbius transfer for arbitrary spherical condensers. On p.317 the variational definition also permits continuous ACL test functions. His normalization is `mod R = 2π / cap R`; an annulus has modulus log(r2/r1), so there is no missing 2π factor. The energy definition on p.318 uses positive unit mass on one plate and negative unit mass on the other, with Möbius-invariant cross-ratio energy. When infinity is off both supports, this equals the usual signed logarithmic energy. Theorem3 on p.323 identifies conformal and transfinite modulus for an arbitrary condenser. Therefore

    cap R = 2π / inf I(μ−ν)

has the normalization used in the frozen note, with the reciprocal endpoint conventions. Bagby's positivity lemma applies to the finite, absolutely convergent signed energies below. In particular these test energies are strictly positive because their two unit components have disjoint supports and are unequal.

The physical scan footer says1967, volume17, number4; the current publisher catalog and DOI `10.1512/iumj.1968.17.17017` label the paper1968. Preserve both descriptions rather than inventing an exact priority date from that discrepancy. Either predates the historical target edition by decades. The review does not resolve the bibliographic discrepancy.

[Kallunki–Shanmugalingam's official paper](https://www.acadsci.fi/mathematica/Vol26/kallunki.pdf) was also freshly fetched: HTTP200, 131,985 bytes, SHA256 `76220c66aa41ce484d3cd8fbe9c8997b2b6b672401d8bc29bc2c4c8cd451c6f0`, identical to the frozen source. Printed pp.455–457 were read in full for definitions and Theorem1.1. Its compact plates must be disjoint, nonempty, and contained in an open connected domain. Euclidean R2 with area, p=2 and the domain R2 satisfies properness, doubling, phi-convexity and the (1,2)-Poincare inequality (tau=1). The theorem identifies all-rectifiable-path modulus with locally Lipschitz capacity. The definitions allow all upper gradients; their weak-upper-gradient alternative gives the same infimum and does not replace all-curve admissibility by an unproved exceptional-curve statement.

The inspected university-hosted Heinonen–Koskela manuscript, sections2.3 and2.9, explicitly permits nonnegative extended Borel densities. Its precise version/numbering is not confused with the publisher's final pagination. The Kallunki theorem is applied only to separated compact plates; neither that theorem nor Bagby's theorem is applied directly to the touching noncompact F.

## 3. The compact-plate bridge, including infinity

For the compact real plates E,K used here, the spherical complement is connected: both half-planes connect around a point to the right of all plates, and every remaining real point connects vertically to a half-plane. Thus Bagby's condenser hypothesis holds even for disconnected Cantor plates.

Kallunki supplies bounded locally Lipschitz separators u with upper-gradient energy arbitrarily near M2(E,K). Truncate u to [0,1]. In Euclidean space its weak gradient satisfies |grad u|<=g almost everywhere for an all upper gradient g: directional line inequalities, Fubini and differentiation give this first for a countable dense set of directions. Rademacher differentiation then gives the full gradient bound. Thus its Dirichlet energy is no greater than the upper-gradient energy.

Choose R large enough to contain both plates and let chi_R be1 on B_R,0 outside B_(R²), and linear in log radius between. Then

    integral |grad chi_R|² = 2π/log R.

For any c in [0,1], put v_R=c+chi_R(u−c). It retains both plate values, is constant near infinity, and

    ||grad v_R−grad u||_2
       <= ||grad u||_(L2(R2\\B_R)) + ||grad chi_R||_2 ->0.

It extends continuously and as an ACL function on the spherical condenser; in a chart near infinity it is constant. Bagby's admissible variational class therefore contains v_R. Taking limits gives the required one-sided inequality

    cap(sphere\\(E union K)) <= M2(E,K;R2).

No equality for touching plates, no interchange of an exhaustion infimum and limit, and no implicit boundary condition at infinity is needed.

## 4. Positive outer modulus gives a finite-energy probability

Consider R=B(0,2)\\E and the other spherical plate B=sphere\\B(0,2). The domain R is connected; upper and lower portions of the disk connect around the left end of [0,1]. Any admissible smooth separating function for Bagby's outer condenser gives a Borel density |grad u| on R, zero elsewhere. Every continuous E-to-circle curve has a first circle hit and, before that, a last E hit. The intervening open subcurve lies in R. Apply the elementary gradient integral inequality on closed interior subcurves and pass to the endpoints using u's prescribed boundary limits. This works for globally rectifiable paths and locally rectifiable paths with actual finite endpoint limits. It is an all-curve argument. Hence

    M_outer <= cap R.

The capacity is also finite, by a smooth radial separator equal0 on a neighborhood of [0,1] and1 near the radius2 circle. Therefore positive outer modulus implies 0<cap R<infinity, so Bagby's transfinite infimum is finite. A finite-energy signed charge consequently exists; one does not need to assume that an arbitrary infimum is attained.

To interpret its component energies, send a point a of R, for example i/2, to infinity by f(z)=1/(z−a). Neither plate contains the pole. Both transformed plates are disjoint bounded compact subsets of the plane, and Bagby's signed cross-ratio energy is invariant. The cross logarithmic kernel is bounded on their product; each self kernel is bounded below on a bounded support. Thus finite signed energy forces each component self energy to be finite, with no infinity-minus-infinity cancellation. Pulling the positive unit component back to E preserves finite energy, because for x,y in E,

    log(1/|f(x)−f(y)|)
       = log(1/|x−y|)+log|x−a|+log|y−a|,

and the two correction functions are bounded on E. This completes the finite-log-energy input used by the null-length deduction.

## 5. Smoothing and all energy limits

Let mu be that finite-energy probability and let nu_eps be its convolution with normalized real Lebesgue measure on [−eps,eps], 0<eps<1/4. This is an absolutely continuous probability supported in [−eps,1+eps]. Since E has length zero, nu_eps(E)=0 exactly.

On every support product at issue use k(t)=log(4/|t|). It is nonnegative there. Finite logarithmic energy is equivalent to finite k-energy on E; in particular mu has no atoms and (mu times mu) gives the diagonal zero mass. For either a uniform translation S or the difference of two independent uniform translations, |S|<=2eps and the density of S is at most1/(2eps). For fixed nonzero t, the averaged kernel tends to k(t). The asserted uniform domination is valid:

* If |t|>=4eps, then |t+S|>=|t|/2 and the average is at most k(t)+log2.
* If |t|<4eps, split off log(4/eps). The average of the positive part of log(eps/|t+S|) is at most `(2eps)^−1 integral_(−eps)^eps log(eps/|r|) dr =1`, and log(4/eps)<=k(t)+log4.

Thus the averaged kernels are bounded above by k(t)+1+log4 and below by0 on the relevant products. Dominated convergence with respect to mu times mu proves both mixed-energy and convolved-self-energy convergence. Every component integral is finite. In particular

    I(mu,nu_eps)->I(mu),
    I(nu_eps)->I(mu),
    I(mu−nu_eps)->0.

The diagonal is discarded only after proving it has mu-product mass zero. Adding log4 to the logarithmic kernel does not alter energy for a signed measure of total mass zero.

For fixed eps, take K_j=supp(nu_eps) intersect {dist(x,E)>=1/j}. These are increasing compact subsets of the real F, separated from E; their union has full nu_eps mass. Thus m_j=nu_eps(K_j) tends to1, and positive m_j occurs eventually. By nonnegativity of k and monotone convergence, both the self integrals on K_j times K_j and the mixed integrals on E times K_j converge to their finite full-measure integrals. Division by m_j² and m_j gives the normalized energies. Therefore

    I(mu−nu_eps,j)->I(mu−nu_eps),
    nu_eps,j=nu_eps|K_j/m_j.

All cross and self energies are finite before taking their difference. On the bounded combined support the negative part of the unshifted log kernel is bounded, so the signed integral is absolutely defined. Its strict positivity also follows from Bagby's positivity lemma and the different supports. For any delta>0 choose eps and then j with 0<I(mu−nu_eps,j)<delta. The compact-plate bridge and family inclusion imply

    M2(E,F) >= M2(E,K_j)
             >= cap(sphere\\(E union K_j))
             >= 2π/I(mu−nu_eps,j) > 2π/delta.

Hence M2(E,F)=infinity. The sets chosen for different eps need not be nested: arbitrary large lower bounds suffice. The noncompact, touching nature of F has been handled by subfamilies with actual separated compact endpoints.

## 6. Endpoint conventions

For the usual continuous curves with actual endpoint limits, the image after endpoint extension is compact. Set w(z)=(1+|z|²)^−1; its squared area integral is pi. It has a positive lower bound on each such compact image. Adding eps*w to a globally rectifiable admissible density therefore gives infinite cost on every locally rectifiable curve of infinite total Euclidean length. A finite-total-length path with those endpoint limits extends to a globally rectifiable curve. This proves equality of the two outer moduli by letting eps decrease to0; the opposite inequality is family inclusion. The estimate follows in L2 for every finite-energy density. If no finite-energy globally admissible density exists, equality follows immediately from inclusion. Curves without compact continuous endpoint extension are outside the convention being certified.

## 7. Edition evidence and permissible conclusions

The peer family's new permitted Google Books observation is deliberately admitted as a **post-freeze cross-input**, not retroactively attributed to this family's initial search. Its frozen receipt records a public publisher-permitted search snippet at indexed p.206 and unavailable full p.205/206 previews. This reviewer read that receipt and authenticated publisher book metadata; the Books UI observation itself was not independently replayed here. Treat it at exactly the receipt's level: partial primary snippet evidence of a terminology remark, not authenticated complete wording, withdrawal, or resolution. Do not supplement the missing words from a nonprimary copy.

The official [Springer book metadata](https://link.springer.com/book/10.1007/978-3-030-25165-9) identifies the 2019 fiftieth-anniversary edition (eBook7 September2019; hardcover20 September2019), with Miscellaneous pp.185–216. These dates and pagination do not identify its full target wording. The original arXiv1809.07200v2 target remains independently authenticated in the initial audit at printed178/PDF179.

The [official Springer extras archive](https://extras.springer.com/?query=978-3-030-25164-2) links the package freshly retrieved here. The ZIP hash matches the frozen receipt, and its sole PDF member's hash is `44d6fe24868b8f4f3ab128f859c3ed1cc2c538bc87ef0b398025e91c2d82497f`. The complete January2021 problem-update list was read; it contains no7.58 entry. This is bounded evidence about that list. It does not certify current openness or complete the 2019 page. This new primary evidence narrows the initial audit's access limitation without contradicting its historical statement.

The verified positive result is an explicit null-length corollary mechanism assembled now from older general condenser theorems and checked estimates. The oldest exact published resolution remains unidentified. No publication should describe the frozen energy note as an independently complete prior proof of the entire target. Suitable framing remains a proof of the explicit historical modulus implication, with its classical foundations acknowledged and any novelty claim restricted to separately established contributions. There are no required mathematical fixes to the frozen energy note under its stated scope.

