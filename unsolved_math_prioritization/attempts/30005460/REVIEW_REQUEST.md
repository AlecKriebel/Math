# Full independent audit request

Please audit the exact general source target and the whole tensor-moment proof, including the finite certificate, rather than treating a large count of exact controls as a proof of tensor positivity.

Final candidate: `PROOF.md`; N=10^62, n=3N, m=6, q=3. The 14KB `TENSOR_MOMENT_CERTIFICATE.json` and its self-contained checker use exact rational matrices of size at most35, not an astronomical explicit tensor or an SDP solver. The 90,494 checks replay byte-identically.

## Main attacks

1. Source scope: original OWR14/2023 p779/PDF39 has arbitrary n,m and fixed odd exponent. Is one explicit finite large-dimensional nonconvex cone a full negative answer to that yes/no question? Do not promote it to a ternary result or all-parameter classification. Published2026 §6 leaves the fixed-exponent question open; the union result is different.
2. Local functional: all moments through total degree18 must be consistently specified, including cross-degree and odd-coordinate moments. Verify the order-three full polynomial (not merely homogeneous cubic) moment blocks, their rational principal minors, the Gaussian top blocks, all six extension steps and every Schur trace bound. No arbitrary entrywise PSD completion is assumed.
3. Tensor positivity: a total-degree<=9 polynomial in all N blocks belongs to the separately-degree<=9 tensor monomial space. Its square must be evaluated by the genuine product functional, with the corresponding matrix a principal submatrix of a PSD Kronecker product. Challenge the total/separate degree distinction and the well-definedness of all needed moments.
4. Seed: reconstruct the actual credited 16-term weighted SOS identity for M1³, the nonnegativity and non-SOS of M1, and the interpretation of all p_i in one common n-variable homogeneous sextic space.
5. Cubic formula: check the 1-block/2-block/3-block multiplicities, moment values -1,11292*10^53,35039520*10^116, the bound a2>=1 and strict negativity at N=10^62. The local functional is not a probability measure, but square positivity is sufficient for separation.
6. Convexity: a finite average of N members outside the set disproves convexity; it is not necessary to assert that an untested partial sum has an SOS cube. The least-failing-prefix argument supplies a two-input existential formulation only.
7. General q: audit finite-degree SOS closedness, separation, normalization and tensor leading coefficient for odd q. Higher-degree square summands cannot cancel to produce a lower-degree p. Do not assume an infinite consistent moment measure or use a limiting random-variable law.
8. No contradiction with the published convex union: the displayed sum may enter at a larger odd exponent. It is not claimed stubborn.
9. Turn1 historical partials remain frozen: full fixed-circuit slice convexity and formal-preordering exponent sharpness are not used to infer the new tensor result. Please retain their exact scope if including them in a full-packet disposition.

Full PDFs and text are in ../../../sources relative to the nested attempt path (absolute source directory /workspace/shared/math-30005460/sources). `source_manifest.json` pins the original report, published2026 article and author preprint. The published seed identity is on printed p24 after Theorem6.3; original p779 also states the a³<=15/13 sufficient range.

No novelty claim, outreach, release or final PR. If the candidate fails, identify the exact gap; three substantive author turns remain. Parent owns all publication and user-resolution gates.
