# Adversarial audit: KOU-21.119 / ID 2628 / rank 472

Audit date: 3 October 2026 UTC.

## Verdict

**PASS for the stated partial-progress package. No blocking mathematical error found.** This is not a solution of the original problem. The five attempts leave its existence question unresolved, exactly as the package states.

The audited object is the 12-file publication snapshot whose manifest SHA-256 is `f481a390bfc1ceb0c572cc1ad146771f392d077705416085d25b52317ed61596`. All 11 manifest-bound payload files have the recorded lengths and hashes; the twelfth file is the manifest itself. The reviewed snapshot was subsequently bound to repository commit `8f1d11249dedc994f25d9fb76c308e0512e787d4` by separate byte-for-byte retrieval checks. The independent mathematical audit itself checked local bytes, not the remote commit tree.

## Turn 1: normalization and virtual first Betti number

PASS. For each m, extension permanence transfers F_m from K_m through its trivial or cyclic quotient to G_m, and finite-index invariance transfers it to G. Quantifying over m gives F_infinity before zero characters are excluded. Thus the rejection of zero maps is not circular.

Every restricted character on a finite-index subgroup remains nonzero because its image has finite index in the original infinite cyclic image. The finite intersections of cores are finite-index normal subgroups of G and are nested. Their character kernels have finite index in the original kernels. Both the positive and negative F_m assertions therefore transfer. No compatibility among the different characters is asserted or obtained.

The commensurability argument is valid in both directions. Under the virtual rational Betti bound of one, two nonzero characters restrict to nonzero proportional rational characters on the intersection of their domains. Equality of their restricted kernels gives commensurability of the original kernels, and hence identical finiteness properties. The conclusion is correctly limited to excluding virtual first Betti number at most one; it does not imply that virtual Betti numbers must be unbounded.

## Turn 2: exact spectrum for products of free groups

PASS, including arbitrary finite-index domains and arbitrary nonzero integral characters. A finite-index subgroup H of a finite product contains the product of its intersections with the factors, and that product is finite index. Nonzero restrictions survive further finite-index passage. For each active factor the inverse image of D Z has character image exactly D Z when D is a common multiple of the individual positive image generators. Division by D therefore gives a primitive character on every active factor.

The free-basis normalization is valid: elementary Nielsen changes realize the needed integral basis changes; after obtaining values (1,0,...,0), replacing every other basis generator b by a b is again a free-basis change and produces all values one. All finite-index free factors remain nonabelian. The inactive factors split from the kernel. Thus the reduction covers all characters of all finite-index domains, without falsely asserting that every such character extends to the original product.

The positive bound uses the join of s finite nonempty discrete sets of size at least two, which is (s-2)-connected. The s=1 endpoint is F_0, which is automatic; s=2 gives finite generation. For s at least three, simple connectivity and the relevant homological finiteness combine to give the asserted geometric finiteness. This is consistent with Bestvina–Brady's Main Theorem and Example 6.3(1). [Primary paper](https://people.math.osu.edu/davis.12/courses/8800-20/Bestvina-Brady.pdf)

The cellular negative certificate is complete as a mathematical argument. The cyclic cover of the product of s roses is a K(kernel,1) of dimension s. Its differential is the tensor differential with coefficients t-1. The displayed tensor of edge differences is a cycle with a unit coefficient in the free top chain module. There are no incoming (s+1)-boundaries, so its Laurent-polynomial multiples inject into H_s. That homology is therefore not finitely generated as an abelian group, ruling out FP_s and consequently F_s. The inactive-factor retraction preserves this obstruction, and finite-index invariance finishes the reduction. Hence the finite spectrum is exactly 0 through M-1.

## Turn 3: finite virtual cohomological dimension

PASS. The syzygy index is correct, including d=1. FP_d makes S_d finitely generated through the surjection P_d to S_d. Dimension shifting gives Ext^1(S_d,A) = Ext^(d+1)(Z,A), which vanishes for every module under cd_Z(H) at most d. Hence S_d is projective and the resulting finite-length resolution proves FP_infinity. The d=0 case is also valid.

The conversion to F_infinity correctly retains finite presentation: n at least max(2,d) supplies both F_2 and FP_d. The package does not make the false general inference FP_infinity implies F_infinity. Restricting the resolution from the torsion-free finite-index subgroup L to K is legitimate because the larger group ring is free over the subgroup ring. Consequently the virtual-cd exclusion and its conservative numerical bound are correct.

The shrinking-open-set example correctly refutes a purely topological stabilization inference. Its rational slope lies strictly between 1/(n+1) and 1/n. It is explicitly not asserted to realize BNSR invariants of a group.

## Turn 4: Thompson F

PASS. The finite coset action forces the infinite simple F' into every finite-index H. Perfection then gives [H,H] = F'. Therefore H/F' is a full-rank sublattice of Z^2, and each integral character extends rationally; clearing denominators produces an integral character of F with commensurable kernel. This establishes the virtual reduction independently of any unsupported finite-index BNSR claim.

The endpoint signs and the geometric/homological distinction agree with the primary source. Corollary 1.2 tests both antipodal rays. Theorem A and Proposition 2.8 give: ab=0 means not finitely generated; ab>0 means F_1 but not FP_2; ab<0 means F_infinity. Thus the finite virtual spectrum is exactly {0,1}. The source's subgroups of all finite lengths do not satisfy the required finite-index ambient condition. [BGK, Corollary 1.2, Theorems A/B, Proposition 2.8](https://arxiv.org/pdf/0807.5138)

The rank-2 abelianization argument excludes a finite-index embedded F^r for r at least two; the interval-fixed-point explanation is consistent with it.

## Turn 5: oligomorphic actions and wreath products

PASS. The specialized wreath-product F_m criterion is stated accurately. The lamp Z satisfies both required lamp conditions: F_m for every m and infinite abelianization. Stabilizers require FP_(m-i), not F_(m-i). The necessity and sufficiency claims for F_infinity follow by varying m, and the same criterion applies to the displayed kernels. [Bartholdi–de Cornulier–Kochloukova, Theorems A/B](https://arxiv.org/pdf/1406.5261)

The orbit calculation is exact: N-orbits in H/S are indexed by the cosets of the stabilizer image in the character image. If a tuple stabilizer S lay in the kernel, the well-defined map S h S to psi(h) would surject onto an infinite cyclic group. This contradicts the finite number of H-orbits on the invariant subset (H x) squared of X^(2i). No transitivity, faithfulness, or topological closure hypothesis is missing. Finite-index passage preserves oligomorphicity. The stated finitely generated abelian quotient extension is also valid.

The resulting exclusion is correctly narrow. It rules out a first failure of finite tuple-orbit counts for lamp-killing characters of the displayed virtual wreath products. It does not settle stabilizer-kernel finiteness, lamp-nonzero characters, or other finite-index forms.

## Exact computation and source checks

The checker runs successfully and its parsed JSON output exactly equals the frozen verification.json: 3,279 standard-weight cell checks, seven standard top cycles, six weighted top cycles, and 100 rational inequalities. The program uses exact integer Laurent polynomials and rational arithmetic. Its tensor signs, zero-weight special case, and nonzero weighted cycles are consistent with the mathematical formulas.

These checks are finite consistency tests. They do not computationally establish arbitrary dimensions, identify every group cover, prove the cited finiteness theorems, or solve KOU-21.119. The package discloses those limits adequately. The general top-cycle argument above is what establishes the infinite-family conclusion.

The preserved p.195 source image was visually checked and states the exact one-group, finite-index, integral-character, F_n-but-not-F_(n+1) question, credited to E. Schesler. A fresh fetch of the live Kourovka PDF timed out during this audit; no independent current-openness claim follows. The primary BGK, wreath-product, and Bestvina–Brady PDFs were accessible and their relevant statements were checked.

## Repairs and remaining gap

No mandatory repair is needed for the stated partial results. Optional presentation improvements are to cite Bestvina–Brady's Main Theorem together with its finite-presentation clause when spelling out the positive F_(s-1) bound, and to state explicitly that the character sphere example uses oriented rays, with each chosen slope representing both antipodes. Neither affects validity.

The actual open gap remains the construction or exclusion of one F_infinity group, outside finite virtual cohomological dimension and beyond the excluded commensurability classes, with every required finite virtual fiber length. The report does not prove such a group exists, does not prove universal nonexistence, and establishes no historical novelty. Existing unsolved/full_resolution=false labels should remain.
