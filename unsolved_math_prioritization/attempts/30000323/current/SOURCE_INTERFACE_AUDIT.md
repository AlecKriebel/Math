# Source-interface audit

## Passed formulation checks

- Source: Hanke's exact question on printed OWR42/2005 p.2423, with p odd, G finite abelian p-group, and V having no trivial direct summand.
- Theory: MSTOP_(p), as identified in Hanke–Puppe's Lemma 5. Oriented stable topological bundles, with canonical complex orientation induced from MU.
- Base and degree: the associated bundle EG ×_G V over BG, Euler class in cohomological degree 2 dim_C V.
- Group action language: V^G = 0 means absence of a common invariant vector. It does not mean the action on the unit sphere is free.
- No substitution of genuine-equivariant coefficients, unoriented bordism, Euler characteristic, or smooth-manifold bordism for the target.
- The universal assertion is equivalent to nonzero Euler localization. For the finite product of all nontrivial character Eulers, nonnilpotence rather than one-time nonvanishing is required.
- Ordinary mod-p detection and K-theoretic detection are one-way implications back to MSTOP. Joint failure of the detectors is not a counterexample.
- Sullivan-induced and customary complex K-orientations differ by an invertible coordinate factor, so Euler vanishing is unchanged. Madsen–Milgram p.116 verifies multiplicativity of the Sullivan orientation.
- The elementary-abelian quotient map need not preserve nonvanishing under inflation.
- No underived quotient presentation for MSTOP*(BG) is assumed.
- Sullivan's spectrum splitting and its exotic map's coefficient theorem are not treated as a natural MU comparison on BG.
- Transfer of the unit is not replaced by the subgroup index in generalized cohomology.

## Literature coverage and limitations

The full OWR source and full arXiv Hanke–Puppe preprint were inspected, including the precise statement, definition of sensitivity, cyclic proof, and topological orientation. Bibliographic identification of the published paper was checked; its publisher PDF returned HTTP 403 and was not retrieved. There is no claim that the published paper was fully compared to the preprint.

A new structural lead, Madsen–Milgram's Sullivan splitting, was retrieved and inspected through its defining map (5.11), proof of the splitting, Thom-spectrum Corollary 5.20, multiplicativity following Corollary 5.25, and the coefficient theorem 11.22. The critical splitting and exotic-map statements were checked visually against the PDF. This is established background, not a later resolution of the Hanke question.

Bounded exact-phrase/current searches for topological-bordism Euler nonvanishing, MSTOP orientations, and Hanke–Puppe sensitivity did not locate a later full target theorem. Results about genuine equivariant unitary bordism and unrelated uses of “topological bordism” were not substituted. This bounded result makes no worldwide-openness or novelty claim. The tom Dieck original underlying MU sensitivity was not independently proof-audited here; its use is explicitly attributed through Hanke–Puppe.

## Computational limits

The finite-algebra verifier contains no Python assert statements. All checks and negative controls passed in normal, -O, and -OO modes with equivalent mathematical results. The verifier checks representation-ring products and group kernels, not generalized cohomology of MSTOP. The uncomputed class e_MSTOP_(p)(W) is explicitly left unresolved.
