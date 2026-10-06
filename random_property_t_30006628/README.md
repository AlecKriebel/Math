# Property (T) above one-third density in random free-product quotients

Problem **30006628 / OWR-14299911-031**, queue rank 924. Draft research publication, 2026-10-06.

## Result and scope

At least three fixed nontrivial finitely generated factors, fixed finite inverse-closed generating alphabets (including fixed-radius word-ball alphabets), fixed density 1/3<d<1; property (T) with probability tending to one through all integer relator lengths.

[PROOF.md](PROOF.md) is the exact unchanged 19,961-byte proof accepted by two independent AI mathematical reviews: [first audit](INDEPENDENT_MATHEMATICAL_AUDIT.md) and [second review](SECOND_INDEPENDENT_MATHEMATICAL_REVIEW.md). The accepted proof SHA256 is `3bed7a81c5562d793bc4991fe62e1c06703818a9046495a7fe96d0b38e1ac100`.

The queue status is `claimed_solved`, at **1/5 substantive approaches**. This answers the stated at-least-three-factor OWR scope, not the broader two-factor case in the preprint's Question 1.9. It is an all-length asymptotic theorem; no claim is made for each finite length, critical density, or parameters varying with length. No exhaustive novelty, formal-verification, human-peer-review, or journal-acceptance claim is made.

The author proof and author archive intentionally retain their original pending-audit wording. [PUBLICATION_ACCEPTANCE.json](PUBLICATION_ACCEPTANCE.json) separately records the subsequent acceptance of those unchanged bytes. All three ZIP files and their external manifests are preserved exactly. The loose proof and two review documents duplicate their corresponding archive members byte-for-byte.

## Reproduction

Python 3 and the standard library suffice. Before executing `verify_publication.py`, authenticate its **8,583 bytes** against SHA256 **`11ca693b078d4616b34af6d340327b6dfc262d995a2f1c73b2b1bd4ff1f44eeb`**, obtained from a separately trusted record. A manifest distributed beside a file is not by itself an independent trust anchor.

Run `python -I -B verify_publication.py` from this directory. The wrapper authenticates all three immutable archives and external manifests, all 26 exact ZIP members, and the three readable report/proof copies before running any enclosed code. It creates a fresh temporary layout and executes each original checker with `-I -B`, in normal and `-O` modes, from an unrelated working directory. Every positive output must reproduce its frozen output exactly; each negative test must match its intended error and exit status. No accepted code is patched.

Full provenance replay additionally requires the three original pinned corpora and the six cited PDF files. Supply all of `--catalog PATH --problems PATH --reports PATH --pdf-dir DIRECTORY`. Without them the wrapper explicitly records provenance replay as `NOT_RUN_SOURCE_BYTES_NOT_SUPPLIED`; it does not claim it passed. Those inputs are not redistributed. `--verify-only` authenticates artifacts without running enclosed diagnostics.

[PREFLIGHT_VALIDATION.json](PREFLIGHT_VALIDATION.json) records the executed normal/optimized wrapper replay with all original source inputs and ten publication-integrity negative controls, including altered archive, manifest, readable proof, missing second archive, and externally rejected modified wrapper. These tests support reproducibility and integrity; finite tests do not certify the asymptotic mathematical proof.

## Sources and publication limits

The complete source-pin metadata and retrieval/inspection history are retained in the immutable author and audit archives. Key public sources are the [OWR report, Problem 16](https://ems.press/content/serial-article-files/53603), [Random Quotients of Free Products, v2](https://arxiv.org/abs/2502.08630v2), [Kotowski–Kotowski's spectral criterion](https://arxiv.org/abs/1106.2242v2), and [Tropp's matrix concentration bound](https://arxiv.org/abs/1004.4389v7). The report distinguishes adjacent literature from proof dependencies. Public manuscript status of cited papers does not certify this candidate.

Only authored mathematics, authored code and audits, and permitted public verification metadata are included. Original corpora, primary PDFs, extracted source text, private sources, personal data, and coordination files are excluded. The only queue modification is this problem's Status, Turns, and Findings cells; all unrelated bytes and existing chat links are preserved. This is a draft PR, with no merge, release, DOI, or external outreach.
