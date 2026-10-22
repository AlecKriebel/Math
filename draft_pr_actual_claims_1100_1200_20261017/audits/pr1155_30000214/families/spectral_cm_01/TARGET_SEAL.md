# Target seal: independently calibrated original question

Sealed UTC: 2026-10-18T01:21:26.584450+00:00
Reviewer family: spectral_cm_01. Supplied-candidate adversarial review, not blind rediscovery. Before this seal I have read no candidate proof, supplied validation, root notes, or reviewer verdict. Assignment named spectral/cohomological and doubly Cohen-Macaulay focus without describing the candidate mechanism.

## Exact target and quantifiers

Nevo OWR 17/2005, printed pp. 960-961 (PDF pages 36-37), Definition 1, Theorem 7 and Problem 8, asks whether the pieces in the following theorem can be homology spheres. For every finite d-dimensional simplicial complex K, d>=1, doubly Cohen-Macaulay over one fixed field k, does there exist a finite collection of d-dimensional homology-sphere subcomplexes S_i over k whose union is K, with S_i intersecting the previous union in a d-face for each i>1, and with each chosen S_i available as first piece after reordering? The original theorem states this for minimal d-cycle complexes, with all pieces over the same k. It is the possibility of replacing those pieces by homology spheres that is at issue; the problem does not merely ask whether homology-sphere subdivisions or maps cover K.

The arXiv math/0505334v2, Definition 3.1, Theorem 3.4, Problem 3.7, agrees. K is 2-CM if K and every induced vertex deletion K-v are CM of dimension d over fixed k. CM requires purity and reduced homology H_i(lk_K T;k)=0 for all faces T including the empty face and all i<dim(lk_K T). For pure d-complexes, dim(lk_K T)=d-|T|. Empty complex and reduced degree -1 conventions must be handled consistently. A homology d-sphere here uses the standard full face-link condition: for every face T (including empty), reduced homology of lk T over k is k in degree d-|T| and zero otherwise; it is a finite pure simplicial complex. A global homology sphere alone is weaker and is not silently substituted.

A negative answer requires one field and one eligible K with no permitted decomposition. Stronger sufficient obstruction: K contains no d-dimensional homology-sphere subcomplex over that field. Dimension d=2 is within the original theorem and is enough. A claim excluding spheres over every field must rule out characteristic 2, positive odd characteristic, and characteristic zero; CM itself only needs the explicitly chosen coefficient field.

## Independent adversarial plan established before candidate

1. Separate exact negative-answer sufficiency from stronger construction claims, and list all coefficient changes.
2. Verify the proposed finite complex is simplicial, pure, has actual stated face links, and its quotient preserves the relevant local model. Check finite quotient/residual assumptions, group actions, type rotations, and injectivity-radius requirements.
3. Independently derive spectral/cohomological implications needed for H^1 and for every vertex deletion. Check weighted inner products and cocycle identities, normalization and strict threshold; do not infer deletion CM from connectivity alone.
4. Audit all nonempty face links and same-dimension purity after each vertex deletion. Test local model and deleted local links independently using finite geometry computations if helpful.
5. For any sphere-exclusion mechanism verify full link hypotheses, arbitrary field applicability, and any Euler/curvature inequalities; test edge incidence, characteristic 2, and nonorientability boundaries.
6. For imported primary theorems inspect the actual source statements and hypotheses rather than candidate quotations. Stop and report if a central difficulty is merely transferred to an unsupported equivalent claim.

## Source pins and read scopes

- `draft_pr_actual_claims_1100_1200_20261017/audits/pr1155_30000214/private/sources/nevo_owr2005.pdf` SHA-256 `f0200fe70e287441d0fd3dbb0b6b564f4ed5bbdc04eb7513612ad0edf7fa95dc`
- `draft_pr_actual_claims_1100_1200_20261017/audits/pr1155_30000214/private/sources/nevo_owr2005.txt` SHA-256 `2a584d6880aafeb228c01b53ff67461ab71585bd748e448a181df214ec4566ad`
- `draft_pr_actual_claims_1100_1200_20261017/audits/pr1155_30000214/private/sources/nevo_0505334v2.pdf` SHA-256 `767106ae250aeb094bb80234e298ceec3d5534ff3ad74b1e049b1ee7cd734f36`
- `draft_pr_actual_claims_1100_1200_20261017/audits/pr1155_30000214/private/sources/nevo_0505334v2.txt` SHA-256 `7ae201768389fd25374fb4e436747f5132141424b357c5e5877a4b063607368b`

PDF page images were rendered in this family's private directory and visually inspected: OWR PDF36-37, arXiv PDF4-7. Text scopes: OWR lines1845-1961; arXiv lines1-85,182-334 and325-360, with selected intervening context returned by searches. All searches and displays were limited to the original target and its context. No other reviewer read.
