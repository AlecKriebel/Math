# Source and prior-attempt gate: 30005303

Checked 2026-10-02. Exact target: OWR-11695865-001, *Total Positivity and Graphical Model Factorization*. The pinned record asks **both** closure of the MTP2 edge-factorizing model and factorization of all binary MTP2 globally Markov distributions.

## Recovery and source scope

The live UnsolvedMath page could not be retrieved. The authorized pinned fallback is `ulamai/UnsolvedMath`, revision `37e53eabe540fb458758e198be61634bd02ee008`; `problems.json` SHA256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`, `research_results.json` SHA256 `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`. There is no keyed upstream research report for this problem code. The compact record is included; large raw data remain outside the public packet.

The official EMS PDF, DOI [10.4171/OWR/2022/55](https://ems.press/journals/owr/articles/11695865), printed pp. 3125–3126, was read and its first problem page visually inspected. It explicitly allows boundary zeros, uses global graph separation, distinguishes factorizing and extended models, and writes real clique potentials. The second paragraph proposes the stronger lattice-support conjecture. None of the source's definitions requires full support, coordinatewise connected support, or a minimal faithful graph.

The separate Gaussian coordinate-descent problem in the same contribution is not part of this imported numeric target.

## Primary literature and limits

- [Geiger–Meek–Sturmfels 2006](https://math.berkeley.edu/~bernd/AOS0092.pdf), Proposition 1, equation (4.10), gives the quartic used in TURN_1. Its Examples 7–8 are different boundary examples. The quartic itself is credited prior work; the packet does not claim to discover it.
- [Lauritzen–Uhler–Zwiernik 2021](https://par.nsf.gov/servlets/purl/10339054), §4.4, distinguishes the extended graphical model. Its compactness results in that model do not give factorization for every globally Markov mass function. Boundary support matters.
- [Fallat et al. 2017](https://arxiv.org/abs/1510.01290), *Total positivity in Markov structures*, distinguishes support hypotheses for local MTP2 checks and faithfulness. The construction is checked directly for all meet/join pairs, without importing a theorem that requires a stronger support hypothesis.

Bounded current searches used combinations of `Lauritzen conjecture factorization totally positive`, `MTP2 cycle factorization counterexample`, `MTP2 closed Ising factorization`, and dated graphical-model searches through 2026-10-02. They did not locate a later primary resolution of the two source conjectures. This is a search result, not a historical novelty certificate. Search-result crawl dates were not interpreted as publication dates.

## Repository and related-target checks

The live repository returned no all-state PR matching the numeric ID, source code, or exact title, and no matching target branch or commit. A read-only recovered clone had 310 remote refs. Its commit-message scan and all remote-head path-name scans found no target-specific artifact. A full historical object-name scan was incomplete because the partial clone lacked a blob; this limitation is recorded rather than treated as a negative search certificate.

The complete pinned record-title/statement search for `MTP2`, `total positivity`, and `totally positive Markov` found this target plus three unrelated matrix/Laguerre–Pólya questions (20002218, 20002223, 30005048). The repository's current related-target groups contain no group for this target. No prior substantive attempt was recovered.

Fresh main at gate time was `1ebdefcfba7e350989827ada7e0d9764d6486807`; the queue row was rank 333, queued 0/5. Current assessments blob `f09cf05130386a13dc73b57fa04ad330b56fe6b1` was matched exactly against a local recovered copy, including the target's review hash and empty holds. Readiness is recorded separately. Public author work starts at turn 1 rather than resetting any prior count.

## Source-file bindings

Third-party PDFs are retained locally for verification and are not republished here.

| Source | Bytes | SHA256 |
|---|---:|---|
| EMS OWR 55/2022 | 600619 | 56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65 |
| Geiger–Meek–Sturmfels 2006 | 289800 | 1aa0d14f5822f7e5664180b92bb3c0f97e022d8276134ae949eaf4ceccc42441 |
| Lauritzen–Uhler–Zwiernik 2021 | 468190 | 8b205ebbaec009a67e2a8d47578262dbe0717a42aa3e3feff75e8527ac674705 |
| Fallat et al. arXiv 1510.01290 | 346936 | f23ef1ec315f931f9af8bc270096efa5c09081e901b2224ff75e5f9004596b3f |
