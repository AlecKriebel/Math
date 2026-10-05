# Stable-polynomial largest-root partial theorem

Problem 30003442 / OWR-15219-012, queue rank 736. **Status: unsolved, 5/5 turns.**

The frozen author proof establishes the largest mixed-characteristic-root comparison for every positive pair m,d with **min(m,d) ≤ 3**. The independent audit passes this complete partial theorem with no mandatory mathematical corrections. The unrestricted question remains unresolved by this work. No novelty, priority, human peer-review, or formal proof-assistant certification is claimed.

The permutation-averaging obstruction and the printed-flow countercheck invalidate auxiliary arguments, not the original conjecture. The corrected flow is derived, but no general largest-root monotonicity is established. The 34 positive sampled simple-root velocities are finite checks only; two repeated-largest-root cases are omitted. The author's `flow_numerator_interval` field uses a quantity scaled by positive f-prime relative to the displayed simple-root formula, so its sign test remains valid.

## Frozen inputs and integrity

`author/` and `independent_audit/` preserve all 29 frozen files byte for byte. The two ZIP archives are likewise unchanged. Their manifest and archive hashes are pinned in `verify_publication.py` and recorded in `PUBLICATION_STATUS.json`.

The independent audit found one nonblocking hardening issue: the author checker alone accepts a symlink at `MANIFEST.json`. All actual frozen files are regular files. The publication wrapper and independent pinned checker reject manifest symlinks. The optional patch is retained separately and **has not been applied to the freeze**.

Statements about pending audit or no remote writes inside frozen files describe their historical creation. The completed audit is in `independent_audit/AUDIT_REPORT.md`; this wrapper records the publication-stage scope.

## Offline replay

Requires Python 3.11+ and SymPy 1.14.0. No network, source PDFs, corpus, or private inputs are required. From this directory:

    python -B verify_publication.py
    python -B -O verify_publication.py
    python -B verify_publication.py --integrity-only

The wrapper checks the exact file boundary, the original ZIP members, both manifests, normal and optimized author and independent replays, four author false-claim controls, fourteen author corruption controls, fourteen independent mathematical negative controls, and nineteen independent integrity controls, including the manifest-symlink rejection. It must also be replayed after relocation.

The published payload contains only original proof, code, exact computations, independent audit, and public verification metadata. It excludes source PDFs, text extracts, screenshots, raw datasets, copied source matrices, and private coordination material. The separate queue change alters only this row's Status and Turns; all other existing bytes, including Findings, Chat, DOI and the historical header, are preserved.
