# Boundary-corrected Hodge ampleness: corrected partial results

Problem **30004494 / OWR-1703871-010**, rank 753. **Unsolved, 5/5 substantive approaches exhausted.** AI-assisted, unrefereed; no complete solution, counterexample to the full target, or novelty claim.

Start with the [corrected result](hodge_30004494_v2/RESULT.md), the [complete retained arguments](hodge_30004494_v2/PROOFS.md), and the [source and hypothesis audit](hodge_30004494_v2/SOURCE_AUDIT.md). The target requires a single fixed effective integral boundary divisor E such that mL-E is ample on the original smooth projective compactification for every sufficiently large integer m, under everywhere fibrewise logarithmic local Torelli. The precise augmented Hodge bundle and extension assumptions are retained.

## Review and correction history

The [original independent audit](hodge_30004494_independent_audit/AUDIT_REPORT.md) passed the mathematical partials but required literature-scope correction M1. Both the original author freeze and adverse audit are preserved byte for byte. The separately pinned [v2 delta acceptance](hodge_30004494_v2_delta_audit/DELTA_ACCEPTANCE.md) resolves M1 and gives **PASS_SCOPED_PARTIAL_RESULTS**. Frozen v2 statements that delta acceptance was pending are historical, not the current controlling review status. The exact v1-to-v2 patch is included. No frozen source record is silently rewritten.

The correction recognizes Deng–Tsimerman Theorem 2.11 on the original compactification. In the stated integral/unipotent framework, logarithmic local Torelli gives independent local monodromy logarithms and the simplicial condition. Base modification is therefore not a necessary obstacle for this input. Projectivity remains Conjecture 2.12 in the inspected version, and the completion theorem does not produce the required fixed effective boundary correction.

Retained controls include the complete closed-null-face criterion, real/rational/integral coefficient equivalence, a constructive surface argument valid for disconnected intersection matrices, relative ampleness and boundary-blowup results, and finite cone feasibility with dual obstructions. Generic immersion alone is shown insufficient by a construction explicitly outside the full target hypotheses. For the rational-certificate conclusion in Theorem 5.1, its finite cone must be **rational polyhedral**, with rational generators and intersection data, as specified in the frozen theorem's rationality convention.

The modern full-Griffiths semiampleness result is distinguished from the upper-half augmented bundle in odd weight. The withdrawn progress report and corrected determinant-descent claims remain disclosed. The sharp unresolved step is one effective boundary combination negative on every nonzero class of the complete closed L-null face. The computations do not establish that geometric compatibility.

## Reproduce

Run `python3 verify_publication.py` from any working directory. Python 3.10+ and the system `patch` command are required; no network or third-party Python packages are used. The publication verifier checks the exact inventory, hard-pinned original and corrected freezes, both audits, all archive members, unchanged proof/code/output bytes, zero-fuzz exact patch reconstruction, and byte-exact original, corrected, independent and delta replays. It repeats the checks and replays in a fresh relocated directory. A trusted SHA-256 of PUBLICATION_MANIFEST.json can optionally be supplied with `--manifest-sha256 HASH`.

The author finite controls report 18,549 checks; the independent finite controls report 33,222 checks. These are arithmetic and integrity controls, not formal verification of classical positivity, Hodge geometry, the full cited preprint proofs, or the original conjecture. The wrapper uses explicit checks that remain active under `python3 -O`; historical frozen runners are deliberately run with assertions enabled.

Only authored research, proofs, code, audit material and public bibliographic/integrity metadata are included. Source PDFs, extracted source text/images, raw datasets, private sources and private coordination records are excluded. The queue patch changes only this row's Status and Turns to unsolved and 5/5. Findings, Chat, DOI, every other queue byte and the stale embedded header are preserved. No merge, release or external outreach is part of this publication.
