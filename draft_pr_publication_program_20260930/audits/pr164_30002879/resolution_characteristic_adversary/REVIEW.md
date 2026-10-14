# PR164: independent resolution and characteristic-map review

**Science verdict: verified in this approach family; no blocking mathematical gap found.** This review concerns original HEAD `7c8acab3ff84c6c8caadec8998296936a156e0bd`, problem `30002879`, and the literal original `claimed_solved` value `2/5`. It does not alter that record or make a novelty finding.

For every characteristic-two field K and the intended nontrivial module M=A/(y), the strongest independently verified result is that the actual coefficient-quotient map gamma is an injective map of cohomology rings and Gerstenhaber Lie algebras, with image

    K·1+(y,u) K[x,y,u,v]/(x²,y²),

where u=d/dx, v=d/dy have degree one. The image in degree zero is K+yA, whereas the characteristic kernel in degree zero is yA. The candidate correctly keeps this scalar exception. The bracket is inherited from the ambient polynomial derivative bracket in these exact coordinates.

The full universal derivation is in `DERIVATION.md`; the untouched initial assessment and seal are in `FIRST_ASSESSMENT.md` and `FIRST_ASSESSMENT_SEAL.json`. No original author code, original independent reviews, original verification.json, original research logs/README, other families' conclusions, or root verdict was read for this assessment or final derivation. The first assessment was sealed at 2026-10-12T08:19:12.569862+00:00, SHA-256 `6f315152f6f7868db7d5c70efd27395acc0ea02924d45df657cdcef4b4f8baac`; both it and the seal have mode 0444.

| Mechanism | Independent evidence | Status / exact gap |
| --- | --- | --- |
| Periodic and tensor bimodule resolutions | Explicit kernel=image computation for l+r; tensor exactness over a field | Verified all degrees; no gap |
| u,v and higher cup normalization | Explicit shuffle chain map; one ordered word evaluates to one | Verified all degrees; no factorial or binomial ambiguity |
| Ext_A(M,M) | y-resolution; identity shifts and coefficient multiplications | M[eta] verified with eta normalized |
| Characteristic map | Q->P tensor M, 1->e_(0,n) tensor 1 | chi(a u^i v^j)=0 for i>0 and (a mod y)eta^j for i=0; onto all degrees |
| Exact original coefficient gamma | Direct E-relative coefficient-I / coefficient-A cochain decomposition and connecting term F(... )m | Injection and image verified, including degree-zero scalar quotient |
| Bracket and cup preservation | All-A endpoint argument for insertions, including degree-zero diagonal outputs | Verified all degrees; higher operations beyond the requested bracket not computed |
| Source module | Official exact-SHA OWR, Hermann v2 and Xu v2 bodies; relevant pages visually inspected | g swaps, h fixes; opposition convention explicitly handled |

The source display alone leaves the action implicit. The cited Hermann/Xu example supplies the nontrivial permutation action. A two-dimensional trivial module would give a different algebra and would fail the characteristic-map surjectivity and center conclusions. That failure is demonstrated by a deliberate negative control rather than silently ruled out by dimensions. Swapping the regular and trivial generators changes the coordinate kernel and is also rejected by the fixed comparison.

`TEST_RUNS.json` contains 16 structured runs, with the final checker and harness SHA pins. The positive mechanism passes 2,277 explicit exception-based checks in each of ordinary Python and Python -O. Every one of seven materially altered mechanisms is rejected in both modes, with `DiagnosticFailure` rather than an accidental interpreter error:

- trivial module: Q augmentation ceases to be onto;
- exchanged regular generator: the fixed y resolution augmentation identity fails;
- omitted right x action: tensor resolution augmentation chain identity fails;
- pure-y comparison killed from degree two: chain identity fails at degree two;
- factorial-weighted shuffle: chain identity fails at (0,2);
- omitted scalar e corner: coefficient-I degree-zero exception fails;
- characteristic-three constant differential: its square is nonzero 2lr.

The finite diagnostics construct resolution/comparison/cup/characteristic calculations through degree 10 and direct relative cohomology through degree 4. F4 checks exercise non-F2 coefficients and ranks. These diagnostics are expressly bounded evidence; the all-degree and arbitrary-field conclusions come from the universal derivation. The new independent checker initially had an incorrect expected rank formula, which it caught; it was corrected using the exactness recurrence and the initial code/output is preserved privately. This was a checker correction, not an original proof defect. Neither checker nor harness uses `assert` as a correctness gate.

No central difficulty was transferred to an unsupported equivalent claim. There is no remaining mathematical issue in this family's requested mechanism. Still outside its conclusion are priority, a full current literature-status determination, the original author's code reliability, characteristic-two squaring and higher brace operations, and the judgment of other review families.

`POST_SEAL_COROLLARY.md` independently verifies a root-suggested later consequence: under the verified L description, the ordinary Gerstenhaber ideal generated by homogeneous cup-nilpotents is the augmentation kernel, so this specific algebra's quotient is K. It is not part of the original candidate and does not resolve the general Question 9.8 or establish priority. The first independent assessment predates this suggestion and remains sealed unchanged.

All source PDFs, full extractions, response headers, rendered pages, the initial self-check correction and internal task/corollary inputs are private. `PUBLIC_OUTPUT_WHITELIST.json` names the only outputs permitted for publication from this family. `FINAL_MANIFEST.json` pins every preserved local artifact and original scientific input, with explicit self exclusion. No Git, index, branch, main checkout, PR, release, Zenodo, Google Workspace, or human outreach action was taken.
