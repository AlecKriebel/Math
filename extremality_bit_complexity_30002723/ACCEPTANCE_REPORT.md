# Acceptance report

20 October 2026. Problem ID 30002723; source OWR-13353-006; row 1827.

## Final disposition

**CLAIMED_SOLVED, 5/5 substantive attempts. Package acceptance: PASS.**

The complete authored proof has passed fresh independent mathematical review and isolated exact saved-input replay. This is acceptance for a claimed-solved draft, not a claim of external peer review, journal acceptance, certified novelty, or an implemented polynomial-time solver. The precise statement is the sparse all-rational one-row **polynomial-bit-time extremality decision theorem**, including two-sided discontinuities and unrestricted valid-function competitors.

## Acceptance obligations and evidence

1. **Exact target.** `ATTEMPT_1.md` fixes sparse rational breakpoint, point-value, and left/right-limit input; `ATTEMPT_5.md` states the complete theorem and minimality promise. Discontinuities, including at zero, remain permitted.
2. **Unrestricted competitors.** `ATTEMPT_5.md`, step 2, imports the established BHK complete 4q-grid equivalence. No original-grid or continuity restriction replaces the definition of extremality.
3. **Equality of kernels.** `ATTEMPT_3.md` proves the slope/jump/spike factorization with genuine coarse relative strata, all zero-face cases, 13 feasible endpoint sectors, point-fixed rays, periodic compatibility, and normalization. The fresh audit independently checks both directions.
4. **Succinct orbit computation.** `ATTEMPT_4.md` proves the signed two-sheet dimension formula, D>K cutoff, prefix-based representative extraction, and nonnegative-marker weighted reconstruction on the original graph. It never enumerates exponentially many unmarked orbits.
5. **Bit complexity.** `ATTEMPT_5.md` and fresh audit §9 bound descriptions, counts, trace coefficients, and residual rank computation polynomially in the binary input length. Cleared numerators may be of order N squared; the needed bound is O(log N) bits, not magnitude at most N.
6. **Independent review.** `AUDIT_ORBIT_COMPRESSION.md` records PASS after complete manuscript review. `structural/FULL_REDUCTION_REVIEW.md` independently identifies no mathematical gap. `AUDIT_FULL_THEOREM.md` gives the fresh final PASS after rereading the proof, inspecting BHK/AHT interfaces, independently deriving the fragile steps, and writing additional validators. These are scoped mathematical audits, not external peer review.
7. **Exact replay.** `verification/REPLAY_REPORT.json` records all eight isolated replay suites PASS. Every regenerated result file matched its frozen bytes and SHA-256. NumPy and SciPy remain explicit dependencies because the original validator modules import them; this package is not standard-library-only. No floating-point LP discovery was run by `replay.py`.
8. **Public-only provenance.** The payload contains authored proofs, audits, code, constructed rational test fixtures, and public source/dataset verification metadata. Copied source PDFs/text, original dataset contents, private sources, private personal data, private paths, and coordination materials are excluded.

## Validation inventory

- Same-grid-rigid non-extreme q=5 counterexample: exact 1/15-grid perturbation and epsilon=5/18.
- 35 saved rational sparse minimal inputs: complete, structured, and joint row-space ranks agree; five inputs have two-sided discontinuities at zero.
- Five genuine 4q refinements: exact row-space agreement, including discontinuous extreme and non-extreme inputs.
- Four dense signed-orbit pipelines: nullities 0, 32, 0, and 2 agree with complete 4q systems.
- 204 signed-graph and 230 rational trace-reconstruction checks: PASS.
- One stored all-covered continuous non-extreme example: exact compressed/reference nullity 1.
- Fresh local validator: 739 exact row-space comparisons on N=4,6,8, all 13 states, and 1,296 infeasible relative triples correctly discarded.
- Fresh independently coded decision simulator: 20 nullity comparisons, including genuine 4q examples and the D>K cutoff; PASS.

The legacy 70-case continuous discovery-run output is preserved, but the individual inputs were not stored. It is not claimed as exact saved-input replay. Its optional generator may rerun LP discovery; the archived record is supporting history rather than a reproducibility substitute.

## Boundaries and chronology

The mathematical proof, not finite examples, supplies the theorem. The validators are dense finite checks and do not implement AHT or establish its asymptotic complexity empirically. Strong polynomiality, arbitrary irrational encodings, higher-dimensional problems, explicit exponentially long perturbation output, novelty, and external acceptance are not established.

The initial source gate predates this authored proof. It found no verified prior resolution in a bounded search and preserved the problem for research. That historical finding is not a rejection of this later proof and is not evidence of priority. The source documents remain separate; only their public metadata and citations are included.

The package manifest covers every payload file except itself. Its separate SHA-256 is supplied with the release handoff. Hash matching establishes artifact integrity, not mathematical correctness.
