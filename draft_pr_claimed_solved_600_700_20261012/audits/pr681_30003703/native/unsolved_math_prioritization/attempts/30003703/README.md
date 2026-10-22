# Audited counterexample: Andreadakis and SL2 matrix-entry filtrations

Problem 30003703 / OWR-15987-013, queue rank 710. Current status: **claimed_solved**, substantive proof-attempt budget **1/5**. One successful algebraic-identity route, including its rank-three specialization, reached the complete-counterexample stopping condition. This is not a claim of five failed routes or of historical priority.

## Exact accepted result

For the rational algebra of matrix-entry functions on Hom(F_n, SL(2,C)), with J its augmentation ideal, let D_n(k) be the kernel of the action on J/J^(k+1). Let A_n(k) be the kernel of the action on F_n/Gamma_(k+1)F_n, using the integral free-group lower central series. The proof constructs genuine automorphisms giving:

- D_n(5) != A_n(5) for every n >= 4.
- D_n(6) != A_n(6) for every n >= 3.

The universal Lie identity, filtered ideal-power bridge, spare-generator transvections with explicit inverses, and nonzero integral Magnus coefficients supply a proof. Finite symbolic checks supplement that proof.

No degree-five rank-three result, failure in every degree, SL_m extension for m > 2, character-ring result, or resolution of the different lower-central-series Andreadakis conjecture is claimed. Independent adversarial acceptance is not human peer review or a novelty/priority certification.

## Read the accepted proof and audit

1. [release/PROOF.md](release/PROOF.md): complete mathematical proof.
2. [independent_audit/AUDIT.md](independent_audit/AUDIT.md): accepted independent review and source-scope analysis.
3. [independent_audit/BINDING.json](independent_audit/BINDING.json): exact release bytes reviewed, accepted claims, and limitations.
4. [PUBLICATION_STATUS.json](PUBLICATION_STATUS.json): present publication assessment.

All 19 original author and audit packet files are preserved byte-for-byte. The author's original README, STATUS, and log describe independent review as pending at their historical freeze time. The separate completed audit and current status above supersede that historical pending-review field; it has deliberately not been rewritten.

## Offline portable verification

Python 3.8 or newer; standard library only. From this directory, run:

    python3 -B verify_publication.py
    python3 -O -B verify_publication.py

The entrypoint checks exact file/directory sets, SHA-256/byte counts, fixed original manifest and proof/audit bindings, retained outputs, and both original validators. It runs the frozen assertion-based scripts in subprocesses with optimization explicitly disabled. Its own integrity checks remain active under -O and PYTHONOPTIMIZE. The original scripts are historical artifacts and should not be used directly under -O as integrity checks. Paths are resolved relative to the entrypoint; no network or source downloads are needed.

The independent implementation never imports the authored verifier. It checks the generic traceless identities, universal determinant quotients in all matrix entries, integral free-word expansions, two-sided inverses, and 12 mathematical negative controls. The author's five negative controls and the audit's eight recorded corruption tests are also retained. The publication manifest excludes only itself from its file list; its hash must be obtained from the PR or an independently trusted receipt.

## Source and claim limits

The original conjecture and definitions were independently verified in Satoh's contribution to [Oberwolfach Report 2/2018](https://ems.press/content/serial-article-files/46724), printed pp. 88–89. Exact metadata and access history are in the two source-verification records. The unsolvedmath page returned HTTP 403, so its identifier mapping remains catalog-based; raw AI-solution corpora were unavailable and uninspected. No exhaustive literature-absence or historical-openness claim follows.

This draft contains authored proof, audits, code, and public verification metadata. Source PDFs, extracts, images, raw records, and private coordination files are excluded. The queue edit changes only this problem's Status, Turns, and previously blank Findings; its Chat and DOI cells and all unrelated bytes remain unchanged. This draft does not merge, publish a scholarly release, mint a DOI, or contact third parties.
