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
