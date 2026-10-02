# Reviewed scoped result: 30005936 / OWR-14298374-005

**Original broad question: unsolved, five of five substantive author turns completed.** The independently reviewed packet includes a complete negative answer to the explicit superlinear continuum mean-square subquestion, together with a positive bounded-test convergence theorem.

For the source's space-time-white-noise LT scheme with g(v)=v_+^(5/4), homogeneous Dirichlet boundary, u0(x)=sin(πx), T=1 and every even spatial grid size N, the midpoint first-moment error is bounded below by a positive constant independent of N and the time-grid size M. Consequently root-mean-square error cannot vanish, including along the balanced refinement M=N². Both first moments are finite. The proof uses a normalized weighted-mass bracket, a concave Itô barrier with localization and Fatou, and explicit positive heat propagation to x=1/2. See [TURN_5.md](TURN_5.md).

For the same superlinear scheme with smooth nonnegative initial data and balanced c h²<=τ<=γh², continuous bilinear interpolation converges uniformly in probability under the same noise. Its path law has bounded-Lipschitz error O([log(e/h)]^(−q)) for every0<q<1/2. These tests are bounded by1 and have Lipschitz constant at most1 in the supremum norm. This theorem is compatible with nonconvergence of the unbounded midpoint observable. See [TURN_4.md](TURN_4.md).

The packet also gives the nonsmooth globally Lipschitz extension, explicit coefficient-dependent high-moment/cutoff estimates and exact supremum exit tails. See [RESULT.md](RESULT.md) for the complete scope. It does not claim infinite coupled second-moment error, an optimal weak rate, every rough coefficient, arbitrary weak tests, arbitrary one-sided refinement, or other integrators.

## Source and attribution

The exact question is David Cohen's second setting in [OWR26/2024](https://ems.press/content/serial-article-files/49484), printed1497, within the full contribution1495–1498. The source specifies white noise and the power1.25 example. The credited [Bréhier–Cohen–Ulander paper](https://research.chalmers.se/publication/542281/file/542281_Fulltext.pdf) distinguishes temporal error against the semidiscrete solution from full continuum error; that distinction is preserved. The negative result uses balanced meshes and does not rely on the OWR display discrepancy.

The common-time-noise result in [PR317](https://github.com/AlecKriebel/Math/pull/317), classical inverse-Bessel/stochastic-calculus tools, Mueller's nonexplosion result and the published spatial/strong estimates retain explicit credit. Ulander's later LTE construction is a different scheme. No novelty certification is made.

## Review, freeze and reproducibility

[Independent full review](review/ADVERSARIAL_REVIEW.md): PASS for all five scoped results, no mandatory correction. This is AI-assisted analytic/source review, not human peer review or formal proof-assistant certification. The five author receipts replay exactly (99,505 assertions); the independent audit adds15,075 exact controls and eight symbolic barrier checks. Finite computation supplements the analytic proof rather than certifying its stochastic limit passages.

All43 frozen author files are unchanged, bound by FINAL_AUTHOR_MANIFEST.json SHA-256 d2e1df9dbe1ca6d60ed45bc9c67fa0fad31299778f53eb89703220b158dbcca7. All10 final review files are unchanged, bound by review/REVIEW_MANIFEST_v2.json SHA-256 6a44649fa8a9629cb3d7498e7b396b9401d7318fa7f5e33a12de3d9745ad311b. The original review manifest/report and additive remote binding are retained. Preliminary review work, raw PDFs and imported records are excluded.

Historical state files remain historical; CURRENT_STATE_T5.json is the final author snapshot. This additive wrapper records the subsequent review disposition without rewriting any frozen proof or claim. The proposed repository change is a draft research PR only, preserving author ancestry and updating only this problem's QUEUE row. No merge or release is part of this publication.
