# Circle-minimum extremals: independently audited reconstruction

Problem 2303014, rank 676. Disposition: **unsolved, 5/5**.

The general positive-mean, nonconstant boundary-data target remains unresolved.
This package records partial results in the explicitly chosen class of finite,
interior-continuous, Poisson-majorized subharmonic functions with almost-everywhere
radial trace and the nonpositive circle minimum condition at every radius.
No equivalence with an unspecified boundary interpretation of the original
question is asserted.

## Read the evidence in this order

1. [Authored proofs](author/PROOFS.md): new reconstruction dated 2026-10-05.
2. [Fresh independent audit](audit/AUDIT.md): PASS for Claims C1-C5 within their
   stated scope; the general target C6 is unresolved.
3. [Separate precision notes](audit/CORRECTIONS.md): the ceiling is needed on the
   closed smaller disk, and simultaneous disk exit/contact counts as contact.
   Read the frozen proof with both notes. Neither changes the extremal value.
4. [Audit binding](audit/BINDING.json) and [source inspection](audit/SOURCE_INSPECTION.json).
5. [Research and reconstruction history](RESEARCH_LOG.md).

The author freeze remains byte-for-byte unchanged, including its historical
"audit pending" labels. Those labels describe the authoring checkpoint, not
the current review status. The later audit is preserved separately and binds
that exact freeze. No original lost proof bytes, historical reported control
count, or interrupted historical review has been recovered or inherited.

## Verified partial conclusions

- The explicit majorized class is nonempty for every real L1 boundary datum.
- Dropping only Poisson majorization gives an unbounded point evaluation at
  every nonzero interior point; no center formula is claimed.
- Nonpositive-mean data have the unique maximizer P[F] within the stated class.
- For positive constant c the sharp value is (4c/pi) arctan(sqrt(abs(z0))).
  This is a credited consequence of the classical compact-set Beurling
  projection theorem; no novelty claim is made.
- Nonconvexity, failure of maximum closure, and explicit finite-radius false
  positives rule out several shortcuts. Sampling cannot prove feasibility.

These are independently audited AI-authored partial results, not human peer
review, formal proof-assistant certification, or a solution to the full target.

## Portable verification

Python 3.10+ and its standard library suffice. From this directory run:

    python3 verify_publication.py --replay --selftest

The verifier checks exact inventory, byte counts, SHA-256 hashes, the original
author manifest, the complete fresh audit binding, and the disposition. Both
checkers run only in temporary copies. Their outputs must match the frozen
JSON byte-for-byte: 30,254 author algebra controls and 47,419 independent audit
controls, including deliberate wrong-formula rejection witnesses. These are
finite algebra controls, not numerical proofs of analytic statements.

The integrity self-tests must reject an added file, changed file, missing file,
duplicate manifest entry, unsafe path, changed author binding, and symbolic link.
The public manifest excludes only itself; its hash is reported in the PR.

## Publication scope

Only authored mathematics, code, audit text, and public verification/source
metadata are included. Source PDFs, source screenshots, extracted source text,
dataset contents, private sources, and private coordination files are excluded.
Public source hashes and inspection history are metadata only. No exhaustive
current literature or priority search is claimed.

The queue change alters only this problem's Status and Turns cells. Other rows,
other cells, links, and the existing queue header remain unchanged. No queue
generator, merge, release, DOI, or outreach is part of this draft publication.
