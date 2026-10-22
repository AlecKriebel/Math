# Word-representation half-order bound: accepted corrected partials

Problem 1430 / GRAPH-043, rank 1015. **Unsolved after five substantive approaches (5/5).** The intended target is a finite simple word-representable graph on N>=4 vertices with R(G)>floor(N/2), or a proof that none exists. Literal N=1,2,3 exceptions are not counted as a research resolution.

The accepted 25-file, 205,180-byte candidate is preserved exactly under `accepted/`. It includes an 11-file, 85,362-byte corrected mathematical payload, the corrected author freeze, public source/corpus integrity metadata, and the independent audit. See [the authored proofs](accepted/packet/PROOFS.md), [the five approaches](accepted/packet/FIVE_APPROACHES.md), [the independent audit](accepted/audit/AUDIT_REPORT.md), and [acceptance scope](ACCEPTANCE_REPORT.md).

## Reproducible boundary

Authenticate `BOOTSTRAP.py` and `PUBLICATION_MANIFEST.json` against their separately published SHA-256 digests before executing anything. A self-contained manifest is not an external trust anchor. Using a trusted Python 3.12 or compatible interpreter, run:

    python -I -S -B BOOTSTRAP.py
    python -I -S -B -O BOOTSTRAP.py
    python -I -S -B -OO BOOTSTRAP.py
    python -I -S -B TEST_MUTATIONS.py

Run the mutation controls in all three modes too. `BOOTSTRAP.py` also accepts an explicit publication directory and `--integrity-only`. A full replay requires a non-root account and permission-enforced temporary read-only copies. It verifies exact pathsets, regular-file types, allowed modes, no symlinks/hardlinks, byte counts and hashes before running authenticated code. Strict JSON parsing rejects duplicate keys, nonfinite/overflowing numbers and invalid schemas; integer fields reject booleans. The controls include externally rejected mutations, separately repinned parser tests, hostile-import/code controls and actual denied write probes. They do not claim adversarial concurrent-filesystem safety or mount isolation.

Fresh replay runs the accepted corrected 84-run audit suite and reproduces the independent 313,309-check result byte for byte. Author diagnostics contain 89,818 bounded checks. These finite diagnostics do not prove the missing general half-order theorem or a target-admissible counterexample.

Default source PDF rehash, corpus rehash, record join, fresh retrieval/inspection, external Lean build and external certificate reproduction are explicitly `NOT_RUN`. Historical source and original/corrected replay evidence stays historical. No original quotation-bearing freeze or literal private correction patch is published or freshly replayed by this package.

Optional local-only rehashes: `--source-dir DIR` checks the eight previously retrieved PDFs named by source IDs (`hkp2015.pdf`, `survey2017.pdf`, `hiraguchi1951.pdf`, `prisms2014.pdf`, `computational2018.pdf`, `hefty2024.pdf`, `bipartite2025.pdf`, `colbrook2026.pdf`). Both `--problems FILE --research-results FILE` are required for complete-corpus byte rehash. No source text or dataset contents are emitted. Rehash does not imply fresh reading, record-join validation, or verification of an external proof certificate.

## Citation and provenance limits

The contemporary bipartite theorem is credited to the [Colbrook–Drysdale 2026 preprint](https://arxiv.org/abs/2609.35842v1); it is not presented as independently reproduced Lean/certificate mathematics. The accepted correction adds the noncomplete-graph qualification to the 2c2 cover bound and replaces source quotation with authored paraphrase. No new discovery, complete resolution, human peer review, global openness certificate or formal certification is claimed.

Historical fields such as `claims.remote_writes=false` in the accepted ledger describe its freeze-time state and remain unchanged. This wrapper records later acceptance/publication without rewriting those bytes. GitHub CI is separate: absent Actions/check/status runs mean `NOT_RUN`, not pass. No merge, release or DOI is part of this draft publication.
