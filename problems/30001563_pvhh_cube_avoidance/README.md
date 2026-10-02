# PVHH additive-cube avoidance: credited prior resolution

The exact original conjecture is Theorem18 of Cassaigne–Currie–Schaeffer–Shallit (2011 preprint; JACM2014). Read PRIOR_PROOF_AUDIT.md for the full source alignment, analytic reduction, directed-interval reconstruction and material published-count qualifications. No new theorem or priority is claimed.

Reproduction:

1. `python certify_eigen_bounds.py > eigen.json` (mpmath required)
2. Compare with EIGEN_CERTIFICATE.json and U_CERTIFIED.csv
3. `python replay_certified_graph.py > graph.json`
4. `python replay_certified_graph.py --omit-sum-filter > larger.json`
5. Compare with the corresponding frozen receipts

The finite graph check is an exhaustive ancestor-state exclusion for arbitrary block length. It is not a finite prefix scan. The larger graph reproduces the printed135572 reachability count, while the printed503-vector count is not reproduced. Directed outward bounds produce497 vectors, with zero uncertain membership cases. All this is explicit in the audit. Raw sources and large reachable streams are not included.
