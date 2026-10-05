# Finite-mean coding radius: audited partial results

Problem **30005024 / OWR-9790359-005**, queue rank **787**. **UNSOLVED after 5/5 substantive approaches.** The independent AI-assisted audit passes only the scoped auxiliary results and unresolved disposition. No mathematical correction is required.

## What is retained

- Explicit all-orders nonzero Hankel determinants for the critical Holroyd-Liggett 1-dependent 4-coloring and 2-dependent 3-coloring. These reconstruct the known exclusion of every **finite-state** hidden Markov representation and finite-order Markov law.
- Tail-integrability and inefficient-representation examples; source-atom and finite-local-operation bounds; cut-information, tail-triviality, additive-concentration and conditional-dependence barriers.
- A synchronizing coupling-from-the-past construction with exponential spatial tail for the finite-state primitive Markov subclass, including finitely dependent finite-order finite-alphabet Markov laws.

These are auxiliary results, including reconstructions of known mathematics. The all-orders proofs are written arguments; finite tests alone establish no infinite-process theorem.

## Exact limits

The original target permits general state spaces and imposes no finite source-alphabet or source-entropy restriction. The countable-output interpretation used in parts of this work does not redefine the source question. **No intrinsic infinite-mean counterexample and no universal finite-mean construction is proved.** Infinite Hankel rank excludes finite hidden states, not countably many states. Spatial finitariness and finite-bit determination remain distinct. One infinite-mean coding of an IID law does not rule out its radius-zero alternative. A second-radius-moment obstruction does not imply an infinite first moment, and coding volume differs from radius in higher dimensions.

Read `author/RESEARCH.md`, `audit/AUDIT.md`, and `audit/CORRECTIONS.md` together. The addendum supplies the independently recomputed review hash and scope clarifications without modifying the author freeze. Review hash: `fb5ee42c259cebb1c28137995be1214779f6c5a20c8e56a417fe7429b3b463fc`.

## Frozen evidence and provenance

`author/` contains the exact ten-file author freeze. `audit/` contains the exact twenty-two-file audit freeze, including a byte-identical copy of those author files. Historical pending-review and no-remote-write statements describe the respective freeze stages. The later audited disposition is given here and in `audit/AUDIT_RESULT.json`.

`frozen_archives/` contains canonical base64 encodings of both exact original ZIP streams. Decode them with Python's standard-library base64 module. Every archive member is checked against the preserved directory. Public source titles, URLs, PDF hashes, sizes and inspection history remain in the frozen metadata. The audit records ten independently downloaded PDFs and three complete verified corpora; the recent quantum paper was inspected only at abstract/metadata level. Publication preparation rehashes the cached full corpora and reconstructs the review hash, with no new scholarly retrieval claim. The bounded literature search is not a worldwide openness or priority certification.

## Verification

Python 3.10+, standard library only; no external inputs are needed for the portable core:

    python3 verify_publication.py --expected-manifest <PUBLICATION_MANIFEST.json SHA-256>
    python3 test_publication_integrity.py

The wrapper rejects optimized Python, verifies the exact recursive inventory, both archives, each frozen manifest and all duplicate-author bytes, and replays **9,093 author assertions, all 9,093 independently rebuilt original cases, and 3,787 additional exact checks**, including **139 primitive three-state directed supports**. Both recorded result files are compared with deterministic recomputation. Publication corruption controls are separate.

Optional `--queue-before` and `--queue-after` inputs verify the full queue byte strings and exact permitted patch. The external source-provenance stage is **NOT RUN** by the portable wrapper; `python3 audit/verify_provenance.py --help` lists the separately required complete corpora, PDFs, pinned queue script and author ZIP. Historical recorded external success is not a new replay with missing inputs.

## Repository scope and credit

Only this target's queue Status and Turns change to `unsolved | 5/5`. Every other queue byte, including Findings, Chat, DOI and the stale embedded header, is preserved. Only authored research, code, computed results and public verification metadata are included. No source PDFs, extracts, images, raw corpora or private coordination are included. This is AI-assisted research with separate AI review, not formal verification, human peer review, novelty certification or publication acceptance. Draft only; no merge, release, DOI or outreach.
