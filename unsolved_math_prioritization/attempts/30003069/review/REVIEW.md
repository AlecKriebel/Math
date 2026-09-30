# Independent review: corrected complemented rectangle seed and FFLV

**Verdict: PASS_CORRECTED_COMPLEMENTED_SEED_KNOWN_RESULT. No mandatory correction.** Recommend `already_solved 1/5` for the explicitly corrected complemented-seed formulation. This verdict does not validate the literal mixed-cardinality display or the imported unchanged non-mirror graph claim.

Reviewed `SOURCE_STATUS.md` SHA-256 `db3d5e5671e34de9d2f9942d8f11b0b71b4673cf6834c88500f87bd65cd17c12`. Separate AI source/mathematics review; no human peer-review or novelty certification.

## 1. Original statement and the two distinct source defects

I visually inspected the full rendered OWR printed p.627, alongside its text and the preceding context. The conjectured graph really has an overbar: it is the graph associated to the preceding complemented cluster, not the unchanged rectangle graph. The earlier Theorem4 separately refers to the mirror graph. The imported removal of the bar and insertion of “non-mirror” therefore change the question.

The printed cluster display really leaves the first, frozen labels uncomplemented and complements the mutable labels. These original labels have cardinality n−k, while the asserted target Grassmannian has k-element Plücker indices. For n different from2k the literal list is ill-typed. The artifact records rather than hides this defect and does not claim a solution for an unspecified interpretation of frozen variables across different Grassmannians.

The 2018 Fang–Fourier published paper was read in full, and printed p.582 was visually checked. Its formula complements every label, and its Corollary1 states the corresponding FFLV equivalence. Although the introduction reuses G in an abbreviated manner, p.581 first fixes the distinguished rectangle graph, and Section4.2/Theorem3 explicitly restrict the conclusion to its dual. Thus the artifact correctly avoids an all-plabic-graphs claim. The paper's references explicitly identify the 2016 announcement being audited. The 2025 Schlößer Lemma3.7, Definition3.8 and Theorem8.6 independently corroborate the all-complement dual-rectangle formulation; its different checkboard theorem is not substituted.

## 2. Frozen labels and boundary relabeling

For cyclic intervals J_s^(d), taking complements gives J_(s+d)^(n−d), exactly as stated. At n=2k, this permutes the frozen family as a set. It does not fix frozen variables individually. A complement of a non-cyclic-interval label is still not a cyclic interval, so the mutable/frozen families are not accidentally mixed in the self-dual case. Consequently the original partial-complement display and the all-complement display yield the same set of labels at Gr(3,6), explaining the announced example without removing the general typing defect.

Schlößer's proof reverses trips by swapping vertex colors and shifts boundary indices to recover complements. Its i−k indexing and the 2018 complementary Grassmannian convention amount to the source-dependent cyclic relabeling described by the artifact. The target Grassmannian is explicitly tracked. No claim that a color swap with all boundary labels rigidly fixed always gives the stated coordinate assignment is needed.

## 3. Valuation and full-body scope

Fang–Fourier Section3.2 uses network face variables, path weights from faces to the left, vertex-disjoint flows, an acyclic perfect orientation with the specified source set, and lexicographic lowest terms. Its embedding of sections into the rational function field is normalized by the appropriate Plücker coordinate. These conventions agree with the artifact; replacing this by a naive exponent valuation in cluster Plücker coordinates would be a different construction.

Rietsch–Williams v2 Definitions8.1–8.6 explicitly distinguish the full asymptotic body from the degree-one valuation polytope. Remark8.7 states the independence of the bodies and degreewise polytopes from the auxiliary total order, although individual valuations can vary. The artifact reproduces that distinction and does not infer a full-body theorem merely from degree-one lattice points.

The 2018 Theorem3 itself states the full Newton–Okounkov body equivalence. This review verifies the theorem's identity, hypotheses and applicability, not an independent reconstruction of every general flow/unimodularity step in that published theorem.

The normalization translation is correct: replacing tau by tau' adds the fixed valuation of tau/tau' to every normalized degree. The tensor-power scaling argument is also sound. On the integral Grassmannian a nonzero section has a nonzero rth power, so each normalized point in degree d reappears unchanged in degree dr. Restricting degrees to multiples of r therefore loses no generating points of the closed convex hull. Changing the denominator from rm to m then multiplies the body by r. The r-omega_k FFLV chain inequalities have the same homogeneous scaling. An affine unimodular map Ux+b becomes Ux+rb between the dilated bodies. Positive integral r preserves the lattice translation.

## 4. Independent check of the facet diagnostic

For a rectangular grid, the order-polytope irredundant inequalities consist of its covers and its two unique extremal bounds. The chain-polytope inequalities consist of nonnegative coordinates and maximal-chain sums. I independently constructed exact rational points saturating just one inequality at a time for every grid through5×5, rather than relying on the author's vertex enumeration.

For an order cover, contracting its endpoints creates no directed cycle: such a cycle would imply an intermediate point between a covering pair. A strict ordering of the contracted poset therefore provides a point with exactly the chosen equality. Extremal bounds have analogous strict witnesses. For a chain bound, all maximal grid chains have equal length h; assigning1/h on the selected chain and a strictly smaller positive number elsewhere makes only that chain tight. Coordinate facets have small positive values on every other coordinate. Both polytopes have strict interior points, so these witnesses genuinely certify facets.

At3×3 this gives14 versus15 facets. Affine equivalence, hence unimodular equivalence, is impossible. This refutes the imported unchanged-rectangle interpretation using the credited ordinary-rectangle/GT and FFLV/order-chain identifications. It does not refute the correctly barred complemented-graph statement, which is the published result.

## 5. Reproduction and classification

All9,642 submitted exact controls reproduce with a byte-identical receipt. Independent controls pass42,438 assertions, including826 rational facet witnesses, cyclic frozen-label complements, and degree scaling. Neither set of computations certifies a general plabic-flow theorem.

The intended, author-corrected complemented-rectangle question is fully covered by the 2018 result and the elementary positive-power argument. Keep that formulation and the original literal defect prominent in any publication or queue summary. Preserve the one diagnostic approach count. No new general equivalence, claim of priority, or statement about the separate all-plabic-bodies/birational-sequences question is justified.

Only copy the files listed in `review_summary.json`; source PDFs, rendered pages and redundant expected receipts are excluded.
