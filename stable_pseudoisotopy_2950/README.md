# Stable pseudo-isotopy: audited partial reductions

Problem **2950 / KP-4.74**, queue rank **921**. Canonical disposition: **unsolved, 4/5 approaches used**. This is an AI-assisted, unrefereed research checkpoint, accepted unchanged as a scoped partial result. No new solution, geometric example, universal nonexistence result, novelty, formal proof verification, or human peer review is claimed.

## What is established

The endpoint-fibre coset lemma identifies the obstruction in the realized quotient R/L, with R = Σ(P(X)) and L = Σ(J(X)). This is the algebra behind Singh's existing endpoint quotient, credited in the report. Realizing a nonzero first obstruction alone is insufficient: it must avoid the full inertial image on the actual resulting manifold. The inclusion (1 + τ)R ⊆ L gives conditional norm-quotient and vanishing reductions; it is not an equality. A nonzero norm quotient does not prove a nonzero endpoint quotient.

The geometric reduction uses Gabai's theorem only for closed connected **oriented** smooth four-manifolds. The printed existence problem does not explicitly impose orientation, so a universal negative answer would also need the nonorientable case. No actual geometric example or universal R = L is established. The fifth approach remains unused because the attempted routes stalled at the inertial-image computation.

## Reading and provenance

- [Original mathematical report](original/MATHEMATICAL_REPORT.md) and [four-approach log](original/APPROACH_LOG.md)
- [Full independent audit](audit/AUDIT.md) and [exact acceptance](audit/ACCEPTANCE.json)
- [Source inspection](audit/SOURCE_INSPECTION.json) and [full input pins](audit/SOURCE_PIN_RESULTS.json)
- [Final frozen replay receipt](releases/STABLE_PSEUDOISOTOPY_2950_FINAL_REPLAY_RECEIPT.json)

All eight original members and all thirteen audit members are preserved byte for byte. `original/STATUS.json` retains its historical pending-review field; the separate exact acceptance records the completed audit. The two frozen ZIPs, their external manifests, and the audit/replay receipts are under `releases/`. There is no repair patch because the original was accepted unchanged.

Only authored mathematical material and public verification metadata are included. Source PDFs, source text, dataset contents, and private coordination are excluded. The three full corpora and three independently retrieved matching primary PDFs were checked by the audit. Retrieval and source-inspection history describes the audit's dated observations, not a new exhaustive literature search.

## Reproduction and trust boundary

From any working directory, run:

    python -B PATH/verify_publication.py
    python -O -B PATH/verify_publication.py

The fail-closed wrapper pins `PUBLICATION_MANIFEST.json`, authenticates the complete file allowlist before execution, verifies every ZIP member against the separately pinned manifest and expanded copy, checks the exact acceptance, then executes authenticated copies in a temporary directory. It repeats the original/audit packaging verifiers and all 32 packet-corruption controls under normal Python and `-O`. It has explicit exception checks, not optimization-sensitive assertions.

Optional full source-input replay requires all four arguments:

    python -B PATH/verify_publication.py --catalog CATALOG --problems PROBLEMS --reports REPORTS --pdf-directory PDF_DIRECTORY

Supply the full pinned JSON corpora separately. The PDF directory must contain `k3-author.pdf`, `gabai-v2.pdf`, and `singh-v3.pdf`. Optional replay checks all six pins and the complete exact-ID record/report pair in both modes. Without these inputs, the output explicitly says source replay was not run. `--integrity-only` authenticates bytes without executing the packaged replay scripts.

Trust the wrapper bytes and its pinned publication-manifest hash from an independently authenticated commit or receipt. Replacing the wrapper and its embedded pins can defeat this trust anchor. Integrity tests establish packaging behavior, not mathematical truth, source correctness, authorship, novelty, or permission to publish. There is no executable mathematical checker: `verify_packet.py` is a packaging verifier only.

Publication checkpoint: 2026-10-06 UTC. The authorized delivery is one draft PR, with no merge or auto-merge. The queue edit changes only this problem's Status and Turns cells; Findings and unrelated rows stay unchanged. Verification completion concerns the publication packet; the mathematical discovery goal remains unresolved.
