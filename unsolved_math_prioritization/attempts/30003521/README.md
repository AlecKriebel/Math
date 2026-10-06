# Quadratic graph NLS: audited bounded partial

Problem 30003521 / OWR-15437-003, rank 867. **Unsolved, 5/5 approaches used.** No full solution or novelty priority is claimed.

Read the [unchanged mathematical report](corrected/PROOF_AND_STATUS.md) and [independent mathematical audit and acceptance](audit/INDEPENDENT_AUDIT_AND_ACCEPTANCE.md). The review was performed by an independent AI auditor; no human referee review is asserted.

## Accepted scope

- D(L) is a Kirchhoff multiplication algebra, with credit to its existing use in the literature.
- For D(L squared), the exact vertex slope-product compatibility condition is necessary and sufficient. Infinitely operator-smooth inputs can have a square outside D(L squared).
- An explicitly rescaled periodic necklace graph has a simple carrier with an exact 1:2 resonance and nonzero coupling. Its second-harmonic corrector equation is unsolvable.
- The long-time stability argument is a conditional lemma only. Its graph-specific hypotheses, infinite-band estimates and quadratic transformation are unproved.

The resonance is on the specified rescaled graph, not the conventional fixed pi-length graph. It is a Bloch-fiber obstruction, not a localized-wave-packet failure theorem. The quadratic NLS approximation theorem remains open within this investigation. Searches were bounded and do not certify exhaustive literature absence.

## Historical integrity defect and correction

The original assertion-only bootstrap is **not optimization-safe**: Python -O removed its integrity checks and a substituted harmless checker executed successfully with stale external pins. The archive, original bootstrap, historical status, and historical validation receipt are preserved byte-for-byte. Their earlier statements are superseded by the independent acceptance decision.

The actual [unified correction](audit/FAIL_CLOSED_CORRECTION.patch) replaces the checker's assertion with an explicit failure and hardens the external bootstrap. Patch application reproduces the separately accepted checker and bootstrap exactly. The mathematical report, source metadata and historical STATUS.json are unchanged. Its pending-audit and no-publication fields describe the original freeze, not this draft publication.

Use a trusted interpreter and independently trusted pins before executing code. The corrected release archive is 11,483 bytes, SHA-256 dbf1da376f6f7cb0a0df9dee55c43986b6a6911905b65fe30518c8cfa6d51a67; its bootstrap SHA-256 is 3ec6ce36e3e69d6aefb9221cea0f801c57520ccd8f8bbfe810f1b304cf880706. The independent audit archive is 45,825 bytes, SHA-256 c4916ec80e30e94df4db3a1fbb6098e8b34d97edb23d195f047ce25adc9c8a85; its bootstrap SHA-256 is a16995c590fcb6dfa58dce84159328d160d76a49f857147b4c41c8eacc2c8258.

From this attempt directory:

    python -I -S releases/GRAPH_NLS_30003521_CORRECTED_BOOTSTRAP.py
    python -I -S -O releases/GRAPH_NLS_30003521_CORRECTED_BOOTSTRAP.py
    python -I -S releases/GRAPH_NLS_30003521_INDEPENDENT_AUDIT_BOOTSTRAP.py
    python -I -S -O releases/GRAPH_NLS_30003521_INDEPENDENT_AUDIT_BOOTSTRAP.py

The independent archive bootstrap validates all 15 members before materializing and executing the 46-control suite. Its expected outcomes include demonstration of the historical defect. Diagnostic reanchoring reaches lower validation layers only in disposable test copies; those copies are never accepted releases. The 11 exact finite identities supplement the proofs and do not verify a PDE theorem.

The publication-level verify_publication.py takes a separately trusted PUBLICATION_MANIFEST.json SHA-256 as its argument. It checks the exact file inventory and all bytes, snapshots the verified bytes, then replays the corrected and independent bootstraps. Run with Python -I -S, optionally -O. This is a trusted-byte gate, not an untrusted-code sandbox. Trust in Python, its standard library, the operating system, bootstrap and external pins remains necessary.

## Publication boundary

The packet contains authored proofs, code, correction, mathematical audit, acceptance reports and public verification/source metadata. It contains no copied third-party source documents, source text, dataset contents, private sources or private coordination material. The research log covers mathematical findings and verification only.

Only this problem's Status and Turns queue cells change to unsolved and 5/5. All other queue content is preserved exactly. This is a draft PR; no merge, release, DOI creation or outside outreach is part of this publication. Empty CI status or workflow lists do not imply a CI pass.
