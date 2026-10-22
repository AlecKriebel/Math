# Independent analytic/trace adversary report

**Disposition:** no mathematical defect found in the exact stated strict-ellipse theorem within this approach family. The universal trace/product step, explicit factor, parity exclusion, and geometric area reduction are justified by the attached analytic argument. This is an approach-family audit, not whole-publication clearance, independent human peer review, formal verification, or a novelty/priority certificate.

The current manuscript audited is `preprint/manuscript.tex`, SHA256 01b7feb398c95ce1a521f379e472e6c856a776408da5b1ccb93db9b0f88a8fe7. Original and revised custody proofs were also read. Every inspected source file is byte-bound in INPUTS.json. No inherited scientific or release script was executed.

## Independence and exact hypothesis

SEALED_PLAN.md and its checksum were written before inspecting the manuscript, inherited proof/review, or other agents' findings. INDEPENDENT_DERIVATION_INITIAL.md then recorded direct tangent, foot, and elliptic edge-vector formulas before source inspection. The hypothesis is the signed shoelace outer-boundary-tangent/center-foot product for a proper confocal elliptic caustic, primitive N>=3 with coprime winding 0<tau<N/2, N not divisible by four. Stars, reversal, and fixed repeats use their original traversal indexing. Hyperbolic/focal/collapsed caustics and unsigned lobe areas are excluded.

## Strongest verified result and attacks resolved

1. Directly solving boundary tangent equations and the orthogonal projection formula reproduces both manuscript area factors. The foot map is an exact fixed linear image of the edge-vector polygon of a phase-shifted billiard. It uses the full boundary tangent lines. The derivation also checks actual unit-velocity reflection and common-caustic geometry, rather than assuming arbitrary Poncelet samples are billiards.
2. The odd finite trace U has simple noncancelling complex poles. Reflection about K+iK' and the exclusion of K from the odd real subgroup give a zero of its K-shift at every pole. All potential poles of U(z)U(z+K) are removable; entire ellipticity then proves a nonzero constant. The exact product-to-sum residue ratio is C_q, with the paired signs cancelling. Thus the manuscript's value `(k')^q/C_q^2` and total area coefficient are correct.
3. Effective trace order is q=N/gcd(N,2), so q is odd exactly for the claimed parity. For even q, K belongs to the subgroup and the trace product is U², which has genuine double poles. This is a structural failure of the proposed extension, not a sampling artifact. The exact period-four counterexample independently has products 32 and 50 on the same proper caustic.
4. Real denominators are nonzero in the strict domain. Apparent complex cancellations in individual foot determinants are covered by exact algebraic identities before applying the trace lemma. No area is divided out, and no unproved nonzero-area assumption is needed. Signed ordering, the reversal signs, repeat-square law, and length-four units all agree.
5. The circular limit gives `N² rho^4 sin²(pi tau/N)` independently and matches the explicit formula. The proof makes no claim at focal/collapsed boundaries or for unsigned filled areas.

ANALYTIC_PROOF.md gives the checkable universal derivation, including a direct route from the geometric caustic hypotheses to the torsion model. It does not merely refer the central difficulty to a classical identity.

## Independent computational evidence

The independently authored audit_checks.py passed at 90 decimal digits using the specified Python 3.11.8 runtime, SymPy 1.14.0 and mpmath 1.3.0. The final run records:

- 2,260 numerical assertions across 11 genuine reflective/common-caustic geometry cases, including odd periods, N=2 mod4, high winding stars, k up to 0.999999, unit scaling, reversal, and triple traversal;
- 18 odd trace cases (q up to 31), checking complex product-to-sum constants, trace products, near-pole residues, and shifted zero slopes;
- four even-q controls showing double poles and real phase variation;
- 34 exact boundary checks covering ellipse incidence, reflection, common-caustic tangency, and period-four area pairs; plus an exact trigonometric circular-limit coefficient identity.

Results, tolerances and reproducible source are preserved in CHECK_RESULTS.json, audit_checks.py and RUN_RECEIPT.json. The samples are arbitrary-precision diagnostics, not interval-certified universal evidence. Two own-checker runs passed; the final one added the exact boundary controls. No failed mathematical probe occurred. No installation, Git command, service mutation, outreach, or external message was performed.

## Residual gaps and scope

No internal mathematical gap remains identified for this family and exact hypothesis. Basic Jacobi theory is a standard input rather than a formally verified library. The audit did not execute or certify the entire inherited reproduction package, exhaust bibliography, verify contemporary-priority statements, inspect publication operations, or authorize promotion. Those remain separate scopes, not defects in the stated area-product proof.

**Approach-family completion estimate: 100%.** The exact residual publication/priority scopes above are outside that denominator. Public artifacts are explicitly listed and byte-bound in PUBLIC_MANIFEST.json, whose SHA256 is bound by PUBLIC_SEAL.json.
