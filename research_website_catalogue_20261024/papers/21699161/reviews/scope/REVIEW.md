# Independent scope review: Zenodo 21699161

**Scope conclusion:** Publication copy is ready subject to the independent mathematical gates. No substantive scope defect was identified. This verdict does not certify the proof, novelty, priority, or peer review.

## Edition and source binding

Read all 34 pages of the freshly downloaded published PDF, including appendices A–I. Page 1 was rendered and visually checked; its complete abstract was cross-checked against the separately published TeX source. The source receipt binds SHA-256 `1a408e9d98f5166e8ffa6adf607413132facb51fa6f8d3108843b5f0280f2c66`. No archived or current mathematical review verdict was read before forming this scope conclusion.

Zenodo gives publication date 2026-07-30 but **no metadata.version**. The printed title page says **July 2026**, with no numbered version elsewhere in the extracted manuscript; `main.tex` confirms `date{July 2026}`. The deposited filename and related archival labels carry **v1.1.0**. Accordingly, content.version records the printed month edition, while source_binding explicitly preserves the missing metadata/printed numbered version and records the archive label separately. Do not invent a deposited version field or turn the printed month into an exact manuscript day.

The primary record has one PDF and no ZIP. Separate publicly identified companion records were acquired fresh and stored under `sources/related-records/`: [21699069](https://zenodo.org/records/21699069), the 34-page line-numbered presentation; [21699181](https://zenodo.org/records/21699181), the TeX tar.gz; [21699205](https://zenodo.org/records/21699205), the integrity manifest; and [21699224](https://zenodo.org/records/21699224), the verification ZIP. Every record’s checksum and size were checked; SHA-256 receipts were written. The published three-file manifest matches the two PDF hashes and source archive hash. The line-numbered PDF is a second presentation rather than an additional mathematical supplement. The GitHub release API returned404, so no GitHub bytes are claimed as freshly verified.

The public draft deliberately keeps supplement_filename:null and additional_assets empty for the primary record. `related_resources` supplies separate DOI links; the renderer should expose those links if supporting downloads are shown. The distinct records and hashes are fully retained in source_binding. Mathematical reviewers have been told where the immutable companion files were extracted. No old audit opinions were used as evidence.

## The actual claim

The central claimed addition is equality of the **shared-randomness convex hulls** of qubit POVM and PVM behavior sets with two inputs per party and arbitrary finite, input-dependent output alphabets. Dimension is at most two on both sides in every strategy component. A single common shared variable may change the state and all local measurements. This is neither raw-set equality, same-state simulation, nor operator-level simulability of each measurement.

The PVM side includes all zero projections, identity/zero deterministic inputs, support patterns, relabelings, and stochastic postprocessing. Ancillary systems that raise the dimension are excluded. One-input scenarios are local. The explicit 3×2 witness therefore gives a minimum-setting classification when paired with the 2×2 equality. The outcome architecture of that witness is(2,2,3)-by-(2,2); inputs and outcomes must not be conflated.

The exact gap is between an attained POVM lower certificate and a global PVM upper certificate: L0=20√2+16/25, U=20√2+3/5+(4+3√2)/250, L0−U=3(2−√2)/250>0. Neither is an exact global optimum. The stronger Appendix B value is optimal only in its specified one-parameter family. No private-randomness entropy theorem or higher-dimensional/multipartite/sequential generalization follows from the stated result.

## Primary literature and novelty boundaries

- [Vértesi–Bene 2010](https://arxiv.org/pdf/1007.2578), Sections V and VI, supplies the earlier 3×2 phenomenon. The maximally entangled-state analysis is analytic; the unrestricted-qubit comparison in Section V.D uses numerical optimization and an SDP upper bound. The manuscript correctly credits that existence result. Public copy must not call the new witness the first qubit POVM Bell advantage.
- [Barra et al. 2012](https://doi.org/10.1103/PhysRevA.86.042114) refines the earlier witness and studies experimental thresholds. These questions differ from the matching setting lower bound.
- [Oszmaniec et al. 2017](https://arxiv.org/html/1609.06139v2) characterizes projective simulability of individual measurements and discusses ancillary dilation. A behavior reproduced with a different state is a separate object; neither theorem should be promoted as the other.
- [Panahi et al. 2025](https://arxiv.org/html/2505.20519v1), Proposition 2 and Section II.2, combines a Masanes dimension reduction with Schmidt compression when one party has two binary measurements. It establishes a Hilbert-space bound for extremal correlations, not projectivization of arbitrary-output measurements on the other side. This distinction matters particularly for the manuscript’s one-binary-party theorem.
- [Cerf–Ollivier 2026](https://arxiv.org/html/2603.26875v1), introduction and Section VI, studies perturbations around deterministic correlations and proposes a route to POVM–PVM separation. Its proved dichotomic local-geometry statement does not supply global arbitrary-output convexified equality. The current draft does not imply their proposed program was completed or directly refuted.
- [Schwarz et al. 2018 corrigendum](https://arxiv.org/pdf/1511.05253v3), first page, retracts a specific claimed nonprojective requirement because a projective strategy with zero effects attains the same value. This supports why all supports and zero effects must remain in the comparison; it is not a defect of the present paper.

The bounded search used the exact paper title and combinations of two-input/qubit/POVM/PVM/convex terminology. It located no independent prior arbitrary-output 2×2 convex-hull equality theorem. Search absence does not establish absolute priority, and no first-priority wording was added. The claimed contribution is the matching lower bound and exact classification, not the qualitative3×2 phenomenon, standard convex separation, binary-POVM decomposition, or established extremal-POVM facts.

## Public copy, status, and follow-up

The full abstract is retained without an appended editorial sentence. Unrefereed status and extensive AI use appear in status, ai_disclosure, and a concise limitation. The latter two ensure that the current renderer displays the disclosure. There is no dated internal verification replay.

Follow-up remains null. Raw-set equality, higher dimensions, multipartite/sequential extensions, algorithms, robustness and exact optima already appear as directions in the paper. This scope review supplies no new precise, evidence-backed conjecture meeting the requested high bar. The collaboration invitation requests substantive expert review or journal development, without an authorship promise. No outside individual was contacted or outreach prepared.
