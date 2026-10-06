# Connected-sum complexity: corrected audited partial results

Problem 30002054 / OWR-11786-002, rank 838. **Unsolved, 4/5 approaches. No novelty claim.**

Read `corrected/PROOF.md` for the operative proof and `audit/AUDIT.md` for the independent review. The original author freeze is preserved in `author/` and its exact ZIP; the corrected derivative and audit also have their exact ZIPs, manifests and historical bootstraps. `audit/CORRECTION.patch` is the exact three-file repair.

The accepted partial formula is Gamma(N_b)=G(N)+(n+1)(b-1), where G is minimum g2 in the consistently chosen TOP or PL category. The correction separates these domains, explains minimum attainment, states local-flatness hypotheses for boundary gluing, and constructs disjoint inner-facet punctures directly. It does not consume another research approach.

The n+1 cylinder example only disproves the broadened interior-sum formulation for arbitrary manifolds with boundary. It does not disprove intended closed-manifold or boundary-connected-sum additivity. The separator cone-capping defect is g2(S)+f0(S)-(n+1); the zero-defect minimizing-separator gap remains open here.

## Reproduction and trust boundary

Use Python 3 with the standard library and the system `patch` utility. The publication bootstrap must be authenticated against its separately trusted digest before executing it. Its SHA-256 is `961564a5203de0969dc245a186c50b95a8d95846c175252cafd41ab17fb6975c`. Obtain the independent PUBLICATION_MANIFEST.json SHA-256 from the draft PR acceptance comment. Do not derive trust from a checksum supplied only by the package being checked.

Start the trusted verification process with `python -I -S -B` (add `-O` for optimization), hash-check the bootstrap, then execute it with arguments `ROOT MANIFEST_SHA256 --replay`. The bootstrap rejects extra files, directories, symlinks, nonregular members, unsafe archive members, duplicate JSON keys, malformed metadata and changed bytes before any package code is invoked. All 23 archive members must match both their pinned archives and extracted files.

Replay applies the actual patch with `patch --batch --fuzz=0 -p1` to a fresh original extraction and requires exact equality of all six corrected members. It runs 914 author diagnostics and 1,377 independent diagnostics with and without optimization, plus 120 original/corrected integrity controls across both harness modes. The publication boundary has an additional hostile-environment control suite in `publication_controls.py`; run it only after authenticating the complete package. Repeat the complete workflow after relocating all files.

Historical audit bootstraps and harnesses remain byte-for-byte unchanged; their own subprocesses use their original -I -S flags. Publication entrypoints and direct diagnostics use -I -S -B. No local package imports occur before complete inventory verification. These checks do not claim a race-proof operating-system sandbox.

## Evidence and limitations

`PUBLICATION_METADATA.json` gives public source hashes and status. Retained scholarly PDFs were rehashed at publication preparation; no fresh remote byte-equality claim is made. The PDFs, extracted source text, datasets, screenshots and private coordination material are absent. `audit/ACCEPTANCE.json` is the frozen independent audit; its no-publication fields are historical, as are those in the preserved author archives.

The tests check finite combinatorics and integrity. They are not a formal proof of general additivity. Zero GitHub checks is not CI success. This package is for draft review only.
