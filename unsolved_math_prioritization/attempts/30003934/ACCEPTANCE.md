# Edition acceptance and chronological disposition

## Exact accepted theorem

On 9 October 2026, the independent mathematical audit accepted the exact frozen proof of coNP-completeness for uniqueness of the mixed-strategy equilibrium pair in explicitly encoded rational, variable-dimension bimatrix games satisfying rank(A+B)=1. Arbitrary degeneracy is allowed. A separate complete reading of the proof, certificate report, full audit and final acceptance accepted the same scope and found no remaining mathematical blocker.

The reduction is from PARTITION to NONUNIQUENESS. Every constructed game has a known strict pure equilibrium; another equilibrium exists exactly for yes instances. The certificate report proves NONUNIQUENESS is in NP for all rational bimatrix games, without a nondegeneracy assumption. Together these give the stated coNP-completeness theorem.

## Exact preserved documents

All four documents are included in full and without changing a byte:

- PROOF.md: 13,596 bytes; SHA-256 5392acc347fe0eaf8597ac619341b2946d21781e6118676248a4ee83baad6c1b.
- certificates/LEMMA_REPORT.md: 15,545 bytes; SHA-256 c498514fa147cce010ad5a4bd90eefd9dd2532d70edbf5930e85520ae65862e6.
- independent_audit/AUDIT.md: 18,916 bytes; SHA-256 c0d1ae53175d4ae02815930b3ca305f430aaf0a6dc893b1d8a23bf18a979847f.
- independent_audit/FINAL_ACCEPTANCE.md: 3,042 bytes; SHA-256 a994e2b0f0b2bb3dac88aa0bab907351ce8b18cd6a45786843ea7569195ef324.

## Chronology and interpretation

1. The certificate report independently proves the rational-witness and coNP-membership statements; it is not itself a hardness proof.
2. The full audit initially examined an earlier HARDNESS_DRAFT.md and gave a conditional verdict, requiring an explicit source-preservation argument and precision corrections. Its opening hash identifies that earlier authored draft, not the final proof. The entire conditional audit is retained, including its rejected inferences and limitations.
3. The frozen PROOF.md incorporates those corrections. Its candidate/pending header and concluding historical language are retained solely to preserve the exact reviewed bytes.
4. The later FINAL_ACCEPTANCE.md explicitly accepts that frozen proof hash and records that no unresolved mathematical blocker remains. Its hash-specific verdict supersedes the earlier conditional disposition. This edition-level record makes that sequence explicit without editing the mathematics or presenting the early conditional verdict as unconditional.

References to computation/verify_reduction.py, exact_rerun.json and other auxiliary material in the preserved documents describe historical supplementary checks. Those files are not part of this proof-only edition. The earlier HARDNESS_DRAFT.md is also not needed to read the complete final proof. No omitted computational artifact is a premise of the universal mathematical argument. Original auxiliary inventories are not included; the edition manifest identifies only the documents actually supplied here.

## Basis and limits

Acceptance covers the source-comparison-preserving ternary perturbation, sign-conformal residual-cycle uniqueness for every real flow value, injective simplex embedding, parameter-uniform exact penalty for every minimizer, two-way equilibrium correspondence, unique strict default strategy pair, all remaining parameter values, exact rank one and polynomial binary encoding. It also covers the independent rational-certificate proof needed for membership.

The substantive proof-search disposition is accepted on approach 1 of a maximum of 5. Editorial preparation consumes no additional substantive approach. No queue modification is part of this edition.

The proof is a synthesis using the Disser–Skutella parametric-flow construction and the established rank-one game/parameter correspondence. The bounded related-work review provides attribution, not a novelty or historical-priority determination. The result does not prove hardness for nondegenerate games, strong hardness, hardness in fixed dimensions, or uniqueness of equilibrium payoffs as a different decision problem. The reviews do not constitute external human peer review, journal acceptance or formal proof-assistant verification. Any material change to the accepted proof requires a fresh hash-specific review.
