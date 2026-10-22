# PR 764 stochastic-family verification

Read REPORT.md and INDEPENDENT_DERIVATION.md for the mathematical verdict and
the first derivation saved before historical audit conclusions were consulted.
VERDICT.json records the exact theorem, scope distinction and outstanding
priority question. MANIFEST.json closes all authored public files and excludes
itself. verify_review.py checks that closure and its hashes without mutations.

Independent finite diagnostics use only Python's standard library:

    python3 independent_controls.py
    python3 -O independent_controls.py
    python3 verify_review.py

These diagnostics are not a proof of infinite-graph convergence. They import
no author code and use explicit runtime checks which remain active under -O.

inspect_sources.py is an optional read-only network fetch and rendering helper.
It creates private scratch and a new timed receipt, so do not run it inside
the closed public review if verifying archive immutability. It requires system
pdftoppm. Third-party PDF bodies and rendered pages from this review were
removed after visual inspection; only metadata and original summaries remain.

No Git refs/index, queue rows, PRs, tracker rows or Zenodo records were mutated
by this reviewer. No external individual or other shard was contacted.
