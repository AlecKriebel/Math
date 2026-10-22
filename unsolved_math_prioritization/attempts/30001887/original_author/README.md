# 30001887: planar multiple-cover thresholds

**Outcome: unsolved after five distinct substantive approaches.** No full proof, counterexample, prior resolution, or novelty claim is made. Independent audit remains pending.

`PROOF.md` contains the primary-source formulation, fully proved retained statements, and the exact obstruction for each approach. The most useful guardrail is an explicit construction realizing every finite incidence hypergraph by translates of an open planar shape P while all whole-plane thresholds m_k(P) equal 1. Thus finite incidence failure alone cannot settle the whole-plane problem.

Contents:

- `PROOF.md`: self-contained mathematical arguments and scope restrictions
- `APPROACH_LOG.json`, `STATUS.json`: five methods and result status
- `SOURCES.md`, `source_verification.json`: source identities, public download hashes, inspected portions, and limits
- `PRIOR_WORK_CHECK.md`: bounded repository search result
- `verify.py`, `verification_results.json`: deterministic exact finite controls
- `VERIFICATION.md`: execution and failure history
- `MANIFEST.json`: SHA-256 and byte counts for all other frozen files

Run `python3 verify.py` in any directory and compare its JSON with `verification_results.json`. Only the Python standard library is used. The program reads no input files, uses no network, and writes its result to stdout. The tests validate finite controls, not the unresolved geometric conjecture.

Important limits: the exact unsolvedmath webpage and raw AI corpus record were not inspected. The primary OWR question was recovered directly. No source PDFs, source extracts, images, raw records, or private coordination material belong to this packet. No remote write or publication was performed.
