# Paper II superseding-version release notes

## Result

Let `R_hyb` be the unique root in `(3/2,151/100)` of

\[
R^6-8R^5+22R^4-30R^3+21R^2-6R+1.
\]

One fitness-independent family of finite connected loopless undirected
weighted graphs simultaneously amplifies every fixed `1<r<R_hyb` for all
sufficiently large population indices.  Thus

\[
R_{\rm sim}\ge R_{\rm hyb}=1.5028569127905696\ldots>3/2.
\]

The release also gives a specialization with entirely rational edge weights
and threshold `1.50176815223369...>3/2`.  It proves optimality among fixed
positive parameters in the displayed first-order pair--pendant response
model.  It does not determine the unrestricted value of `R_sim` or prove a
universal upper bound.

## Reproducibility boundary

The standalone 19-member archive contains the manuscript source and PDF,
three paper-local exact certifiers, the paper-level integration audit, pinned
dependencies, and deterministic replay/build/release scripts.  The manuscript
itself is the analytic proof.  The archive omits duplicate or stale proof
notes, discovery scripts, sparse numerical diagnostics, the retired affine
workstream, temporary compiler products, rendered QA images, virtual
environments, venue metadata, and cover letters.

The exact programs audit finite transition aggregation and symbolic/rational
identities.  The all-order weak-cut, establishment, cleanup, reciprocal-
invasion, and sweep estimates are analytic arguments in the manuscript and
are not replaced by computation.

This checkpoint makes two previously compressed stochastic steps explicit:
the Bd cleanup proof now includes a stopped strong-Markov block recursion,
and the reciprocal dB proof includes a finite-horizon exponential-moment
bound for its dominating immigration--death process.

## Related public versions

- <https://doi.org/10.5281/zenodo.21852072> is the v1 source/software archive
  containing an earlier manuscript version of the beyond-`3/2` result.
- <https://doi.org/10.5281/zenodo.21850042> is the superseded source/software
  archive for the earlier `R_sim>=3/2` construction.

Both records are unrefereed repository snapshots rather than peer-reviewed
articles or bioRxiv postings, and neither is the persistent identifier for
this superseding manuscript package.  A new versioned deposit may be named
only after the human author creates it.
