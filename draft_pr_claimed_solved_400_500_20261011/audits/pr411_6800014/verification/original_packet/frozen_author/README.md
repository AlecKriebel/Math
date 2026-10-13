# AMR-067-0014: Ricci pinching on solvable Lie groups

**Problem:** 6800014, queue rank 444.  
**Status:** Explicit counterexample proof candidate; independent audit pending.  
**Substantive attempts:** 2. Retrieval and packaging are not counted.  
**Novelty:** Not claimed. A 2018 talk already announced the existence of non-solvsoliton local maxima, while the later paper explicitly left their existence open. The packet supplies a self-contained construction rather than relying on the conflicting announcements.

## Result

For every `0 < u < 1/2`, the standard metric on the five-dimensional simply connected almost-abelian group determined by

\[
A_u=\begin{pmatrix}0&-1&0&0\\1&0&0&0\\0&0&0&u\\0&0&0&0\end{pmatrix}
\]

is a local maximum of `F = Scal² / |Ric|²`, with value `1/3`, but is not a solvsoliton. Thus, if the proof survives independent review, the universal assertion in the listed problem is false.

The proof controls **all nearby left-invariant metrics on the fixed group**, not merely a diagonal or block-diagonal family. Its main step is an orthogonal normal form using the generalized zero eigenspace, followed by an explicitly positive transverse quadratic form. Flat directions are treated by a uniform Taylor estimate, not by assuming that a semidefinite Hessian alone proves local maximality.

- [First attempt: full conjugacy Hessian](attempts/turn01_hessian.md)
- [Second attempt: complete local-slice proof](attempts/turn02_slice_proof.md)
- [Source and scope audit](SOURCE_AUDIT.md)
- [Exact symbolic verification](verify.py)
- [Independent Hessian calculation](check_hessian.py)

Run the checks with Python and SymPy: `python verify.py` and `python check_hessian.py`. The proof itself does not depend on floating-point evidence.

No source PDFs, scraped pages, research corpora, screenshots, or private conversation records belong in this packet.
