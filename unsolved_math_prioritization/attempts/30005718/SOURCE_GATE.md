# Exact source and prior-attempt gate: 30005718

Checked2026-10-02. Numeric identity30005718, codeOWR-14298007-013, *Ultra-Log-Concavity from a Matrix Recursion*. Source triage is complete; fresh proof work is recorded as author turn1, not hidden in this gate.

## Primary scope and a metadata correction

The live [UnsolvedMath page](https://www.unsolvedmath.com/problems/30005718) returned a retrieval error. The authorized fallback was the repository-pinned UnsolvedMath dataset revision `37e53eabe540fb458758e198be61634bd02ee008`. Its manifest-bound source hashes are `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf` for problems.json and `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b` for research_results.json. No research report keyed by this code was present.

The full primary item is Poullot's Problem6 in [OWR58/2023](https://ems.press/content/serial-article-files/48169), printed3308–3309, DOI10.4171/OWR/2023/58. Both pages were read and visually inspected. The printed 3×3 matrix and initial vector match the cleaned record. Its coefficient sequence varies in k at fixed n; the printed subscript `(v_n,k)_n` is a typographic index slip. The paper's homogenization remark fixes the finite-degree ULC normalization used in TURN_1.

The record's background/literature assessment mistakenly discusses realizable M-convex functions and Plücker vectors, belonging to the preceding source problem. This is a metadata contamination, not part of the matrix-recursion target. The complete imported record is retained unchanged for provenance, with this correction separate. A second harmless source typo says v_n,4=4 while calling it the constant coefficient; the recurrence has v_n,3=4, as also confirmed in the later primary paper.

The full task contains a precise ULC conjecture for V_n and a qualitative request for methods for general polynomial-matrix recursions. The general request is not interpreted as a claim that every nonnegative matrix preserves ULC. Any sufficient criterion must state its hypotheses. Ordinary log-concavity or bounded-n verification is not silently promoted to the stronger ULC claim.

## Current primary literature

- [Poullot, arXiv:2411.14102v3](https://arxiv.org/abs/2411.14102v3), dated23Oct2025: Proposition5.4 reproduces exactly the matrix and starting vector; Theorem5.6 gives the degree and leading coefficients; Theorem5.7 treats fixed low-degree coefficients. Conjecture6.2 still asks even ordinary log-concavity. The relevant statement and its surrounding discussion were read.
- [Juhnke–Poullot, arXiv:2504.20739v3](https://arxiv.org/abs/2504.20739v3), dated11Aug2026: Example3.8 repeats this exact recursion, and Problem3.9 leaves its unimodality/log-concavity open. The published paper appeared7Sep2026 in IMRN, DOI[10.1093/imrn/rnag191](https://academic.oup.com/imrn/article-abstract/2026/17/rnag191/8787275). Its general counterexamples concern other polytopes and do not settle this special family.
- Related methodological references located are [Gross–Mansour–Tucker–Wang, arXiv:1407.6325](https://arxiv.org/abs/1407.6325), on synchronized log-concave sequences, and [Brändén–Huh, Lorentzian polynomials](https://annals.math.princeton.edu/2020/192-3/p04), on suitable preservation operators. They are not invoked as unchecked black boxes to solve this recursion.

Bounded web searches covered the exact title, Poullot with matrix recursion/log-concavity, hypersimplex ULC, and newer primary papers. They located no resolution. The latest retrieved directly relevant primary paper explicitly retains the weaker question as open, which is stronger evidence than the imported dated desk note. This remains a bounded literature search, not a novelty certificate.

## Prior and duplicate checks

Live GitHub returned no all-state PR for the numeric ID, source code, or distinctive title words; no target branch or commit was found. The read-only recovered repository's remote-head paths and all-ref commit-message scan also found no target-specific attempt. The recovered inventory had335 remote refs at this gate. No complete historical blob-content search is claimed.

A complete pinned-record title/statement search for ultra-log-concavity variants and matrix recursion returned only this target. Current related-target groups contain no matching group. The current QUEUE row is rank337, queued0/5. The current assessments blob `f09cf05130386a13dc73b57fa04ad330b56fe6b1` matched a recovered copy exactly; its target review hash is `93db0d08259ca3bbeb9a3b42d9e043b83645b324d78cdf2c40f257a87023b1d6`, with no holds. Base main for the first checkpoint is `069ade12a0fb7226804d4412575f9e19dfd9596d`.

## Source bindings

Third-party PDFs are retained locally for verification and are not republished in this packet.

| Primary file | Bytes | SHA256 |
|---|---:|---|
| OWR58/2023 | 670397 | 416426fae5c204fbcf574be1da44b34c7cab126ded75d6b4e44f730e4a92d2ac |
| Poullot2411.14102v3 | 1679132 | a7353e014d1c6d4e6361dd5553ac0e758d714edfa750c5e8739a4f98e5bdbbcc |
| Juhnke–Poullot2504.20739v3 | 989449 | b159a2a3798fad8748ff632128f41fc3e4f115c9b1b031a6a732834531d2eece |
