# Changelog from the inherited package

## Final pre-send review edits (version 2)

1. Corrected all theorem-like cross-references in the compiled paper. Proof headings and internal citations now explicitly say `Theorem`, `Proposition`, `Lemma`, or `Corollary`; the shared-counter `cleveref` ambiguity was removed.
2. Rewrote the continuous-time proof so the real-analytic implicit-function theorem supplies exact fixed-output preservation, while the algebraic certificate supplies the derivative identity, parameter tangent, and margin signs.
3. Narrowed verifier language accordingly: it verifies the exact tangent identity and the algebraic hypotheses of the analytic corollary rather than claiming to construct a nonzero perturbation.
4. Replaced “exact implicit-function calculation/argument” in author-facing materials by “real-analytic implicit-function argument, with Jacobian and tangent data verified exactly.”
5. Specified the rank target as the 15-dimensional affine space of consistent three-leaf group-based Fourier coordinates with `q_AAA=1`.
6. Replaced “proposed inequality” language by “high-level K3P trinet question” or “K3P analogue of the high-level trinet inequality.”
7. Replaced quotient-ring prose by the quartic number field `Q(h)`, with `h=5^(-1/4)` and basis `1,h,h^2,h^3`.
8. Removed the priority-audit sentence from the paper body; the narrow audit remains in `PRIORITY_AUDIT.md`, `PROVENANCE.md`, and the author handoff.
9. Narrowed the paper’s reproducibility claim to computational identities, inequalities, and determinants; the continuous-time existence step is explicitly attributed to the analytic implicit-function theorem.
10. Restored and checked the distributed `src/` regeneration and audit scripts, aligned their metadata with the revised certificates, and rebuilt all PDFs, reports, hashes, and the final archive.


## Mathematical corrections and clarifications

1. **Semi-directed formulation.** The theorem is now stated directly for the semi-directed trinet. The rooted DAG is retained only as a displayed-tree calculation device.
2. **Root suppression.** The two rooted `K` edges adjacent to the root are explicitly composed into the effective pendant edge `K odot K = (1,1/4,1/4,1/4)`, with transition probabilities `(7/16,3/16,3/16,3/16)`.
3. **Topology presentation.** New reproducible TikZ panels show both the rooted representation and the suppressed semi-directed theta trinet, including the three theta paths, three pendant leaf edges, and two reticulations.
4. **2-sub-blob terminology.** The fragile assertion that there is “no proper induced 2-sub-blob” was removed. The proof now uses only the robust facts that the theta core is a maximal nontrivial 3-blob, has three incident leaf components, and contains two reticulations. A short footnote records the possible convention ambiguity.
5. **Continuous-time correction.** The package no longer describes the closed-form witness as unrelated to continuous time. It proves the exact positive-rate conditions `a_C>a_G a_T`, `a_G>a_C a_T`, `a_T>a_C a_G` and records that `U` and `V` lie on two boundary faces of that smaller cone while remaining strictly interior to `Theta_0`.
6. **Scope correction.** The conclusions are tied specifically to the high-level K3P trinet extension and the direct K3P analogue of the source paper’s JC/K2P local-to-global blob-distinguishability mechanism. The paper explicitly lists questions not settled by the construction.
7. **Research context.** The introduction now identifies the source paper’s level-one K3P result, arbitrary-level JC/K2P results, JC/K2P global corollary, and high-level K3P discussion using exact citation metadata and cautious terminology.

## New exact strengthenings

8. **Full-rank Jacobian.** The fifteen specified output rows and parameter columns were independently differentiated. The determinant was verified exactly as

   `h(10 h^2 + 1)/(2^61 3^4 5^14)`.

   The paper now proves local surjectivity of the fixed theta-trinet map and relative openness of the tree/theta intersection inside the tree model.
9. **Strict continuous-time collision.** The exact fixed-output tangent identity was derived and checked, and a real-analytic implicit-function argument was applied. The two formerly saturated rate margins have positive derivatives, while all remaining inequalities have strict slack. The paper now proves existence of a nearby realization of the same tree distribution with every network edge in the strict positive-rate continuous-time K3P cone.

## Certificate and verifier changes

10. `certificate.json` now includes root-suppression data, every effective semi-directed edge, all inverse-Fourier edge probabilities, all sixteen core entries, all sixty-four Fourier coordinates, all sixty-four pattern probabilities, the full Jacobian matrix, and continuous-time derivative data.
11. Added `jacobian_certificate.json` and `continuous_time_certificate.json` for focused independent review.
12. Replaced the inherited verifier with a dependency-free exact verifier that reconstructs every claimed object from the certificate, including the graph, suppression, four displayed trees, Jacobian determinant, and fixed-output tangent identity.
13. Added a successful clean-package transcript in `verification_report.txt` and a SHA-256 manifest.

## Editorial and reproducibility changes

14. Rewrote the paper as short auditable lemmas and theorems, added a hypothesis-use table, and supplied a compact numerical orientation table clearly separated from the exact proof.
15. Added a two-page technical summary, author handoff, email draft, README, provenance record, and narrow priority-audit record.
16. Removed references to internal work instructions and unsupported claims of genericity or exhaustive priority.
