# Version 2 manuscript alignment

Checkpoint: 21 September 2026 (America/Los_Angeles). Completion estimate: **100% of the bounded source manuscript alignment**. The parent owns final PDF/layout and complete-package verification. No release or DOI is asserted. Files owned here: `paper/main.tex`, `paper/appendices.tex`, `paper/references.bib`; this note is the only additional artifact.

## Evidence read and scope

Read the September 13 `VERSION_2_PLAN.md`, `section3_audit.md`, `version_diff_audit.md`, the September 20 `LEAN_COMPLETION_2026-09-20.md`, current `CERTIFICATION.md` and `docs/CERTIFIED_COVERAGE.md`, and the relevant production declarations. The historical receipt remains historical: no new full verifier run is claimed by this editing task.

The parent separately reported fresh current Zenodo API/latest-record and download verification in `archive_current/manifest.json`: latest identifiers remain 21699161, 21699069, 21699181, 21699224; all four downloaded MD5 values verified; old software archive contains zero `.lean` files. No manuscript paragraph depends on uninspected archive metadata and no new DOI is invented.

The primary current Zhu record and full text were read directly on September 21:

- https://arxiv.org/abs/2608.01317v2
- https://arxiv.org/html/2608.01317v2

Authors are Lin Zhu, Ranyiliu Chen, Xin Wang, Shenggen Zheng; title *Analytic Qubit Separation between POVMs and Projective Measurements*; arXiv v2 dated August 31, 2026. Their Theorems 1 and 2 distinguish analytic arbitrary-state qubit PVM separation from an exact unrestricted finite-dimensional optimum for their particular rational functional. The new paragraph reports those results and distinguishes universal two-input equality. It makes no private-correspondence, counterexample, comparative gap, or priority claim.

## Changes and rationale

1. Working date now reads **Version 2.0.0 working revision — September 2026**. No purported publication day or new DOI.
2. Abstract and roadmap now describe the formally used deterministic-gap and differentiable-curve route. Main equality and minimum-input claims remain unchanged.
3. Section 3 is explicitly a supporting exact certificate at the already known Vértési–Bene architecture. It credits the shared CH/CHSH-plus-ternary mechanism, does not claim first existence or architecture novelty, and keeps the displayed rational functional, physical witness, original global bound and exact gap.
4. Removed the ambiguous comparison-table row `Global optimum claimed / No / No`. Kept the qualified all-state PVM comparison; it does not deny Vértési–Bene's fixed-state analytic optimum or matching numerical/NPA evidence.
5. Added the strictly stronger formal SOS upper bound 289/10 as an alternative certificate, explicitly not an exact optimum and not a claim that the original physical-to-scalar route is fully formalized. Main theorem retains original constants.
6. Compact pointed-cone proof preserves the support-minimal signed perturbation and count N−1=rank R≤dim K≤3. It correctly distinguishes canceled one-versus-one common rays from nontrivial reduced four-ray circuits. The support perturbation remains nonzero because a coefficient outside the proper subset cannot change.
7. Replaced the strict multiplier positivity proof by the actual deterministic-reset argument. With S=PᵀQP, reset R_j sends the selected ray to u, other same-input rays to zero, and leaves the other input unchanged. R_j u=u cancels normalization; null equations and stationarity give L(P)−L(PR_j)=2λ_j r_jᵀSu. Physical future-null/timelike pairing is positive. The physical whole-input reset is local, so strict separation forces a strictly positive gap and λ_j>0. The first four basis rays give Λ>0.
8. Retained the Lorentz signature prerequisite and future-cone orientation correction without weakening it.
9. Replaced stale 'only finite algebra checks' verification prose with principal-endpoint coverage, exact names, the physical matrix model, reproducible command, pinned toolchain/Mathlib, receipt fingerprint boundary, standard axiom/trust statement, and clear distinction between agent review and external expert review.
10. General alternative arguments remain displayed but now carry explicit scope labels at relevant sections and in the appendix coverage boundary. The full paper is not described as wholly formalized.

## Retained-only matrix

| Retained manuscript material | Formal status / replacement | Relevant production evidence |
|---|---|---|
| General finite POVM dual attainment and complementary slackness (main lemma and Appendix E) | Manuscript proof, not general formal endpoint; no longer used in displayed positivity proof | `DeterministicGap.stationary_gap`, `multipliers_positive`; physical gap derived in `IncidenceScores` |
| General determinant pullback / Hermitian KKT normalization multiplier | Supplementary manuscript interpretation | Actual incidence stationarity derived in `IncidenceStationarity` |
| Full smooth 14-dimensional incidence manifold | Manuscript proposition | Surjective derivative plus `exists_level_curve` and local physical reconstruction suffice |
| Full inverse-metric Hessian and inertia (4,12), Appendix F square completion | Manuscript argument, not full formal endpoint | `IncidenceAlgebra.polynomial_score_gap`, `ImplicitCurve.quadratic_gap_limit`, compatible rank-one uphill direction |
| Arbitrary pointed-cone formulation | Manuscript generalization; needed qubit specialization checked | Physical binary-party cone circuit reduction |
| General mixed-state common-span and arbitrary rank-square inequality | Manuscript broader statements; only needed specializations formalized | Qubit filtering and extremal reduction chain |
| Original physical-to-scalar projective-bound route | Retained prose plus exact scalar checks, replaced formally | `ProjectiveSOS`, `ProjectiveBound` certify 289/10 |
| Ideal auxiliary PVM discrimination optimum 3/5; selected spectral/coordinate identities | Not all separate formal endpoints | Direct witness and universal SOS bound suffice |
| Appendix B dual slacks, derivatives, unique critical point | Retained manuscript calculations | `strengthened_attainment` checks physical attained value, not global optimum |

## Review and checks

- Source `git diff --check` passed on the three edited manuscript files.
- Lightweight source validation found no duplicate labels, undefined cross-references, missing/duplicate bibliography keys, or unmatched environment counts. This is not a PDF build.
- Exact endpoint names, namespaces, and file names were checked against production Lean sources; no Lean source was edited.
- `/root/repair_calculus` independently reviewed the deterministic-reset replacement against `DeterministicGap`, `IncidenceScores`, and physical cone hypotheses. It found the sign/factor 2, normalization cancellation, λ=0 exclusion, whole-input locality, and Λ positivity sound. Adopted its precision edit: the block **represents** the physical behavior.
- No PDF build was run by this task; parent owns the build, rendered inspection, and resulting artifact hashes.

## Pending integration: local notes only

These are deliberately not claims or placeholders in the paper. After agents provide exact compiled declarations, add a concise model-convention paragraph and contract references for:

- generic local Hilbert spaces of dimension at most two, including basis/isometry transport and normalized complement assignment;
- finite dependent input/output label equivalences to the canonical `Fin` architecture.

Parent will supply the final named receipt and any necessary correction to verification wording after all sources are frozen. No bridge is claimed in the manuscript before that evidence exists.

## Stochastic bridge integration checkpoint

21 September 2026. The core stochastic agent reports successful production build, semantic contracts, and standard-only axioms (18 declarations), independently reviewed by the calculus agent. I inspected `Bell/StochasticProcessing.lean`, `validation/StochasticContracts.lean`, and `stochastic.md`. Appendix I now cites `Bell.StochasticChannel.decomposition`, `Bell.StochasticProcessing.behavior_decomposition`, and `Bell.StochasticProcessing.mem_convexPVM`, explaining one whole-strategy selector, zero probabilities, empty-source/empty-target cases, and convex rather than raw closure. The arbitrary-finite-label wrapper remains pending with the finite-label bridge; generic Hilbert transfer remains pending.

The calculus reviewer independently accepted the compact cone proof, including the nonzero endpoint after perturbation, rank count, and extreme-ray sign partition; no closure hypothesis is needed. Adopted its optional precision clarification: combine repeated occurrences of each ray before canceling common rays.

## Final bridge integration in progress

21 September 2026, after the parent requested final completion. FiniteLabels/FiniteStochastic production builds and all 17 combined anonymous contracts are confirmed, along with 25 standard-only axiom checks. Appendix I states arbitrary finite input-dependent **outcome** types accurately and explicitly retains Fin-indexed inputs. HilbertSimulation production build, HilbertContracts (zero diagnostics), and eight standard-only axiom checks are confirmed. The manuscript now explains actual source-space operators, basis-independent tensor form, linear isometries, complement assignment, zero-dimensional impossibility, exact raw-union correspondence, and source-Hilbert whole-strategy simulation. The composed arbitrary-Hilbert/arbitrary-outcome adapter is the final outstanding paragraph before source freeze.

## Source freeze: final bridge integration complete

21 September 2026. Parent confirmed production compilation of `Bell.HilbertFiniteLabels`; I inspected the final actual-source model, raw-union transport, hull equality, complete matrix-branch simulation, and source-Hilbert-branch simulation endpoints. Appendix I now cites `Bell.HilbertFiniteLabels.rawPOVM_eq_fixed`, `rawPVM_eq_fixed`, `at_most_two_input_equality`, and `finite_source_projective_simulation`, plus `validation/HilbertFiniteLabelContracts.lean`. This final endpoint retains arbitrary finite outcome types and returns actual Hilbert-space PVM branches on C² with one common finite random selector. No bridge placeholders remain in the manuscript. The earlier pending notes above are historical checkpoints.

The parent requested source freeze at the successful production build while the combined anonymous contracts finish. A final package receipt remains parent-managed; this note does not pretend that the whole-package fresh check has already run. Source `git diff --check` and lightweight cross-reference/citation/environment checks passed after the final paragraph. No PDFs were built by this subtask, and no other source files or git state were changed here. **Completion: 100% of the assigned manuscript editing and source checks.**

## Layout repair and renewed source freeze

21 September 2026. At the parent's explicit request, repaired only TeX layout after the strict build reported overfull/underfull boxes around long paths and declaration names. Added `xurl` break opportunities, made both endpoint-table columns ragged-right, and used breakable path formatting for the three standard axiom names. Mathematical content, wording, constants, and theorem names were preserved. The PDF skill had already been activated by the parent with its required one-time authoring marker; it was not rerun.

`bash paper/build.sh` now exits **0** and reports **Built warning-free main.pdf and review.pdf**. The retained transcript is `evidence/pdf_layout_build.log`. Both publication and line-numbered review builds passed the strict warning gate. Source is frozen again after this layout-only change. Parent retains rendered visual QA and final release-artifact verification. The combined Hilbert/finite-label agent also confirmed all13 anonymous contracts and15 endpoint axiom queries passed with standard axioms only. **Completion: 100% of manuscript source alignment and warning-free PDF compilation.**
