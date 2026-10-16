# Flow/source adversarial review of PR 1041 / problem 30003934

Verdict: **CLEAN in the assigned flow/source scope**, conditional on separate verification of the uniform penalty, rank-one game correspondence, equilibrium uniqueness, and rational nonuniqueness certificates. This is not an overall theorem acceptance, novelty verdict, external peer review, or formal proof-assistant result.

The reviewed target is rational, explicitly listed, variable-dimension games with rank(A+B)=1 exactly, arbitrary degeneracy, and uniqueness of the mixed-strategy pair. The proposed direction is PARTITION→NONUNIQUENESS, with a known strict pure default equilibrium and an extra equilibrium iff the partition exists. The flow interface required for that reduction is established by the submitted §§1–2 as independently derived in FULL_DERIVATION.md.

## Findings and precise disposition

| Issue attacked | Result |
|---|---|
| Source construction and Figure 3 bridge orientation | Exact match: normalized ±a, base ε/5, capacity-one bridge +s0→−t0, 8n+7 arcs, 4n+6 vertices, DAG. |
| Maximum flow and zero-bridge feasibility | F=2^(n+1), distinguished from the individual 2^n connector capacity. An explicit zero-bridge terminal flow scales to every real q∈[0,F]. |
| Universal source SSP behavior versus one selected tie execution | Complete Lemmas 3.1–3.2 were read and Figures 1–3 inspected. The recursive state/two-step argument has no special tie rule. Strict signed-sum comparisons enforce use iff PARTITION yes, forward 0→1, immediate backward 1→0. Corollary 1.7 alone would not supply the all-optimal quantifier. |
| Perturbation coupling | Original path differences are multiples of 1/D; pairwise perturbations have magnitude <1/(4D). Each perturbed shortest path is original-shortest in the **same** residual state; bottleneck-preserving induction gives a legitimate source execution. |
| Every real-q optimum unique | The ternary leading term forbids zero-cost simple residual cycles with nonzero projection. A sign-conformal fixed-value difference of distinct optima yields such a cycle, contradicting optimality and the perturbation. Formal arc/reverse-arc two-cycles have zero projection and cannot occur in that decomposition. |
| Continuous SSP interpolation | Independently justified by residual path/cycle decomposition: no competing value-(q+Δ) flow can improve on Δ times the shortest residual path cost. Applies to real Δ within the bottleneck. |
| Negative cheap arc costs and positive potential | The initial DAG has no circulation; negative original cheap arcs pose no optimality obstruction. The submitted topological potential makes every arc strictly positive and preserves all fixed-q optima, residual path comparisons, and residual cycle costs. |
| Fractional yes witness and range | At a forward midpoint q=2j+1/2≤F−3/2, the unique optimum has e=1/2. Its h=q+K/2<F and λ<F−ε_game. |
| Simplex injectivity and no-case restriction | f,h determine every coordinate uniquely. DAG path decomposition gives sum f≤Lq. On no instances, the unique unrestricted perturbed optimum has e=0 and is feasible for the restriction at every λ∈[0,F]. |
| Polynomial encoding | D divides 240S; ternary denominators add O(p) bits; capacities/F have O(n) bits; topology, H and simplex coefficients have polynomial bit length. No execution of exponentially many SSP steps is part of constructing the reduction. |

No central difficulty was transferred to an unsupported equivalent claim. The two local source slips below have direct algebraic resolutions and do not change the source theorem or the submitted construction.

1. DS printed p.5:8, Lemma 3.1's i=1 paragraph, gives its second path cost as −v1. Figure 1's two expensive arcs give **1−v1**, consistent with the lemma's j+v^[j] formula. The submitted arc costs are correct.
2. DS printed p.5:9 retains the local cost envelope [j−A,j+A] after changing the base cost to δ=ε/5. The correct envelope includes ±δ; state separation remains strict since 2(A+δ)<1. The bridge comparisons on p.5:10 explicitly include δ and remain correct.
3. In submitted §2, “original optimum” is a small terminology ambiguity: the needed object is the **unrestricted perturbed/potential-shifted** network optimum. Its role and the preceding uniqueness argument make the intended meaning clear. Optional editorial clarification only; no proof repair required.

## Fresh primary source receipts and visual evidence

DS source: [The Simplex Algorithm Is NP-Mighty](https://www2.mathematik.tu-darmstadt.de/~disser/pdfs/DisserSkutella18.pdf), final ACM TALG 15(1), Article 5, November 2018; DOI 10.1145/3280847; 19 PDF pages. Fresh retrieval 2026-10-13T22:36:35.770940+00:00, 553046 bytes, SHA-256 88cc527ec698aaa502a93c33183ae58b714a4879ca387b1101208c7dc329ff5a. Complete used source argument inspected: Section 2, §§3.1–3.2 and Lemmas 3.1–3.2; Corollary 1.7 at printed 5:5 and its proof at 5:17. PDF pages 7,8,9,10,17 were rendered and visually inspected. The diagrams verify the actual gadget, base/bridge costs, capacities, endpoints, and residual orientations.

Original question source: [Oberwolfach Report 38/2018](https://ems.press/content/serial-article-files/46760), DOI 10.4171/OWR/2018/38, New Directions in Stochastic Optimisation, workshop 19–25 August 2018. The complete Bernhard von Stengel contribution, Algorithms for Rank-1 Bimatrix Games, printed p.2332 / PDF page 30, including five references, was read and visually inspected. Fresh retrieval 2026-10-13T22:36:37.451779+00:00, 1014372 bytes, SHA-256 850879c0962050da5fb7f99dd0e2218dcc1cb2c9729266fdfd239c7ca1545003. It identifies rank(A+B), motivates uniqueness hardness despite polynomial computation of one equilibrium, and states coNP-hardness of uniqueness as a conjecture. This establishes historical target provenance, not present openness or originality.

Both fresh source identities match the submitted SOURCE_PROVENANCE.json. Raw source PDFs, source text, and rendered source pages are private review evidence under sources/raw and must not be publicly redistributed with these review reports. SOURCE_RECEIPTS.json records URL, byte count/hash, retrieval time, redirects and response headers.

## Independent check receipts, negative controls, and limits

The newly authored flow_check.py uses exact fractions and independently constructs the arc list. CHECKS_NORMAL.json and CHECKS_OPTIMIZED.json both record PASS. Each mode checks 37 distinct weight vectors with n=1–4, 660 SSP augmentations and half-flow optimality certificates, 864 simple residual cycles for n≤2, and six complete searches over the original shortest-path choice sets. The six valid original cases happened to have no shortest ties; every permitted execution was still enumerated and checked. The cases include all 27 ordered triples in {1,2,3}^3, n=1, odd totals, binary weights, symmetry and multiple partitions.

Every half-flow has an exact residual dual/reduced-cost certificate excluding negative cycles; for n≤2 every simple cycle is enumerated and no nontrivial projected zero-cost cycle is found. All tested flows satisfy exact capacity/conservation constraints and the path-sum bound. The selected perturbed path is explicitly checked against all original shortest residual paths in the same state. Topological positivity, telescoping potential costs, unit bottlenecks, immediate bridge reversal, witness range, injective simplex coordinates, and scaled zero-e max-flow feasibility are verified.

Four negative controls pass: setting the base δ to zero allows the yes case [1,1] to skip the bridge; a true projected-nonzero zero-cost cycle is detected; a formal zero-projection two-cycle is distinguished; and an oversized perturbation fails original shortest-path preservation. Runtime guard probes independently force the checker to reject a false condition in both normal and optimized Python; each exits 1 with the expected RuntimeError, recorded in GUARD_PROBES.json. No critical verification uses assert.

These are finite supplementary checks, not a quantified proof or LP/game equilibrium enumeration. The quantified proof is the source argument and independent deductions above. The edition contains eleven prose/metadata files and no executable, fixtures, historical machine check outputs, or logs. Its historical 6-game/39-network checks and older audit's four added game cases were not replayed or simulated. No omitted historical check is claimed reproduced.

## Independence, prior audit comparison, and final pins

Complete PROOF.md was read first. INPUT_PINS.json checks all eleven submitted snapshots and all eleven Git blobs at ad138ddd5bd1a51c0f225f03342c0c058873f790 against SUBMITTED_PINS. The shared working main checkout remains at fa24428a4fa6930fd3df9dc1b2feb0f7c72885c9 and the corresponding original file paths are absent there; immutable git-show blob verification is the correct original check. The full PR edition tree contains exactly those eleven files.

FULL_DERIVATION.md was completed and hash-checkpointed at 2026-10-13T22:41:19.698886+00:00 with no prior AUDIT.md or FINAL_ACCEPTANCE.md read; INDEPENDENCE_CHECKPOINT.json records that fact. Only afterward were those two submitted old reports read. Their flow conclusions agree with this derivation: comparison-preserving source coupling, projected-cycle uniqueness, fractional witness, potential invariance, and injective simplex range. Their broader accepted game/certificate verdict was not imported. Other fresh family reports and the novelty audit were not read. Final original/snapshot pins and review artifact hashes are recorded separately.

All work was confined to reviews/flow_source_01. No original file, Git index/branch, PR, queue, external service state, or individual was changed or contacted. No external outreach was prepared.
