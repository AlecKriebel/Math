# Triangle-removal spread: scoped partial results

Problem **30005114 / OWR-10252930-024**, rank 790. **General problem UNSOLVED; five-turn budget exhausted, 5/5.** Independent AI-assisted audit: **PASS for the explicitly scoped partial results**, with no required mathematical correction. No full solution, novelty, or priority claim is made.

## Exact scope

Start from K_n, select a uniformly random current triangle at each step, and delete its edges. The horizon is m = floor(n^2/6 - n^(199/100)), with p_m = 1 - 6m/n^2. The asymptotic results require sufficiently large n with positive m.

One high-probability trajectory event E_n, chosen independently of the prescribed family and k, gives:

- For every deterministic family of k distinct triangles, a conditional inclusion bound with base O(n^(-0.98)), uniform in k and the family.
- The sharper conditional bound (4/n)^k when the family's edge-shadow maximum degree is at most n p_m^2/10. Shared vertices are allowed; a shared edge makes inclusion impossible.
- A dense clique decomposition disproves an unrestricted extension of the particular potential inequality. The K_5 terminal process disproves automatic negative correlation. **Neither is a counterexample to the original conjecture.**

The missing step is a C/n base for unrestricted high-degree families, including quadratic k, under one family-independent high-probability event. The finite K_486 audit witness has negative m and checks first-step potential drift only; it is not an experiment at the original horizon. The author uses a separate K_402 witness with the same limitation.

## Proofs, evidence, and literature boundaries

Read `author/REPORT.md`, `audit/AUDIT.md`, and `audit/CORRECTIONS_AND_CLARIFICATIONS.md`. The original seven-file author freeze and nineteen-file audit freeze are unchanged; `audit/author_frozen/` preserves the identical author files. Historical statements that an audit was pending remain frozen; the current audit disposition above controls.

Bohman–Frieze–Lubetzky's concentration results from *Random triangle removal*, Theorems 2.1–2.2, are imported and credited, not re-proved. Jain–Pham and Sah–Sawhney–Simkin construct or analyze different measures; they are not asserted to identify the ordinary triangle-removal output law. The author inspected SSS v1, and the audit adds current v2 inspection. Dated bounded searches found no inspected resolution of the exact target; this is not an absence theorem.

Source titles, public URLs, PDF identities, inspected locations, dataset hashes, and retrieval/search limitations are in the frozen source metadata and `PUBLICATION_PROVENANCE.json`. No source contents are distributed.

## Portable verification

Python 3.10+, standard library only; assertions must remain enabled:

    python3 /path/to/packet/verify_publication.py --expected-manifest <PUBLICATION_MANIFEST.json SHA-256>
    python3 /path/to/packet/test_publication_integrity.py

The wrapper validates exact recursive inventory, externally pinned publication manifest, both frozen manifests, original ZIP identities and all archive-member bytes, including the audit's unchanged author copy. It replays both author and independent exact verifiers and requires byte-identical recorded results. The audit checks 141,040 graph/family cases; finite checks support the analytic proof and do not establish the imported asymptotic concentration result.

`frozen_archives/` contains canonical base64 encodings of the original ZIP streams. Decode with Python's standard-library base64 module to recover the exact ZIP bytes.

Optional `--queue-before` and `--queue-after` paths check complete queue hashes and the exact permitted Status/Turns patch. Full corpus and PDF rehashing requires excluded external files; the standalone replay does not silently claim to rerun those stages.

Only this target's queue Status changes to unsolved and Turns to 5/5. Every other queue byte, including its stale literal header and empty Findings cell, is preserved. No other target, catalog, state, release, DOI, merge, or outreach is changed by this draft.
