# Current packet version 2 — source and priority addendum, 2026-10-13 UTC

**Status:** `claimed_solved`, author turns 2/5; zero new proof-search turns. **Novelty, first assertion, first proof, and current community-open status are WITHHELD.** Lauret's **23 July 2018** talk already announced precisely the nonglobal non-solvsoliton local-maxima existence claim; credit for that prior announcement is explicit. The known `D_t` family, value 1/3 and nonglobality machinery are prior work. This packet supplies a direct small-parameter all-nearby-metrics argument for the literal fixed-group Question 14; its `R²×H₃` metric is a Ricci soliton even though it fails the original group's solvsoliton derivation equation.

The inspected full texts are I arXiv v1 (3 August 2018), I arXiv v2 (9 May 2019), and II arXiv v2 (27 November 2019). Both I preprints state the small-coefficient existence issue as unknown; full final I/II journal texts were inaccessible and are NOT ATTESTED. The old phrase “later paper” below denotes inspected preprints. No withdrawal or false announcement is inferred from the chronology. The current aggregator wording/status remain unverified: historical 403 and root-observed HTTP 429 on 13 October are access observations. See the prominent [current source addendum](SOURCE_AUDIT.md) for the bounded 40-query/13-PDF priority review, separately sealed bibliographic erratum, correct displayed `E_t` values 25/91 and 25/67, and exact trust limits. The separate priority-classification parent gate is not certified by this software component.

**Current verification guidance supersedes v1 paths below:** authenticate the independent custody digest for the **`verification_v2/`** bundle, then run `python /path/to/verification_v2/run_all.py` and `python -O /path/to/verification_v2/run_all.py` in a private environment with SymPy 1.14.0. V2 binds this exact 19-file current prose/metadata set, original 19 inputs, 39 preserved static predicates and 54 actual mandatory evaluations. The three guarded mathematical scripts and successful output hashes remain exact v1 bytes; the standalone runner's allowed source-prose path and versioned schema are updated and require a new software adversary. V1's 55-file original bundle and actual seal remain preserved, with its parent software acceptance explicitly historical. Direct algebra-script runs do not bind prose or manifests.

No source PDFs/corpora/private state belong to the 19-file author-proof packet. Separate preprint/verification artifacts require an explicit parent positive delivery whitelist; the old omission language does not exclude an independently authored preprint PDF from a separate approved package. The complete historical/v1 README is retained below; this dated addendum supersedes its source-version and verification-path interpretations. No proof or human-review status changed.

---

## Historical README and v1 guard addendum retained verbatim

# AMR-067-0014: Ricci pinching on solvable Lie groups

**Problem:** 6800014, queue rank 444.  
**Status:** `claimed_solved`, 2/5 substantive attempts; complete counterexample with a fresh independent full-proof PASS. The draft PR is not a peer-reviewed publication.  
**Substantive attempts:** 2. Retrieval and packaging are not counted.  
**Novelty:** Not claimed. A 2018 talk already announced the existence of non-solvsoliton local maxima, while the later paper explicitly left their existence open. The packet supplies a self-contained construction rather than relying on the conflicting announcements.

The exact family is already Lauret–Will I, §6.4, printed p. 20, family `D_t`. The contribution of the argument in this packet is a direct local-slice proof of its small-parameter local maximality; priority is not asserted.

## Result

For every `0 < u < 1/2`, the standard metric on the five-dimensional simply connected almost-abelian group determined by

\[
A_u=\begin{pmatrix}0&-1&0&0\\1&0&0&0\\0&0&0&u\\0&0&0&0\end{pmatrix}
\]

is a local maximum of `F = Scal² / |Ric|²`, with value `1/3`, but is not a solvsoliton. The independent audit found no required mathematical repair: this disproves the universal assertion in the listed problem.

The proof controls **all nearby left-invariant metrics on the fixed group**, not merely a diagonal or block-diagonal family. Its main step is an orthogonal normal form using the generalized zero eigenspace, followed by an explicitly positive transverse quadratic form. Flat directions are treated by a uniform Taylor estimate, not by assuming that a semidefinite Hessian alone proves local maximality.

- [First attempt: full conjugacy Hessian](attempts/turn01_hessian.md)
- [Second attempt: complete local-slice proof](attempts/turn02_slice_proof.md)
- [Source and scope audit](SOURCE_AUDIT.md)
- [Exact symbolic verification](verify.py)
- [Independent Hessian calculation](check_hessian.py)

Run the checks with Python and SymPy: `python verify.py` and `python check_hessian.py`. The proof itself does not depend on floating-point evidence.

No source PDFs, scraped pages, research corpora, screenshots, or private conversation records belong in this packet.

## Audit and reproducibility

- [Full independent audit](audit/INDEPENDENT_AUDIT.md), preserved byte-for-byte
- [Independent exact checks](audit/independent_checks.py)
- [Editorial change map](EDITORIAL_CHANGES.md)
- [Frozen author hashes](FROZEN_AUTHOR_HASHES.json) and byte-identical originals in `frozen_author/`
- [Research log](RESEARCH_LOG.md)

Tested with Python 3.12.14 and SymPy 1.14.0. From this directory, run `python verify.py`, `python check_hessian.py`, and `python audit/independent_checks.py`. The scripts also run from another working directory.

The main proof is the exact frozen text that received the audit; its historical pending-audit phrases are superseded by this README and the attached PASS. The live aggregator page remains unverified because of its 403 response.

## Software guard addendum — 2026-10-13 UTC

This dated addendum supersedes only historical software execution guidance above. Current `verify.py`, `check_hessian.py`, and `audit/independent_checks.py` use explicit mandatory failure branches; every original predicate and its short-circuit evaluation are retained. The supplied verification bundle checks their AST relation and executes all 54 mandatory guard evaluations (24, 2, 28) in normal and optimized Python. No theorem, proof, author turn, or historical audit text changed.

For complete package integrity and exact algebra, obtain the accompanying `verification/` bundle, authenticate its published seal through independent package custody, and run `python /path/to/verification/run_all.py`, then `python -O /path/to/verification/run_all.py`. Use a private virtual environment and install `sympy==1.14.0`; the current replay used Python 3.14.6. The entrypoint resolves all paths from its own location and checks the complete positive file set, candidate prose, current publication manifest, frozen metadata, original PR inputs, guard relation, checkpoint counts, and exact output hashes. Direct execution of the three algebra scripts checks algebra only and does not bind prose or the publication manifest.

The frozen author scripts remain historical byte-identical originals. Their assertions disappear under `-O`; their optimized printed success is not validation evidence. The historical standalone source manifest digest `f5446c816081c5322e4279bcd9a61dca5bfb63cfacf69d105d1587ed9d93b7fb` and pre-path-adjustment checker digest `eccde3c2a903b1fca0f232e7e392d537479ddd3936281a37e87c4f7e7047be97` remain UNATTESTED because the corresponding bytes are absent. Checking the six included frozen files does not attest those missing objects. Current status remains `claimed_solved`, author turns `2/5`, and zero new author proof-search turns.
