# Problem 30003571: relative Kähler–Ricci flow

**Candidate result:** a counterexample to total-space positivity preservation for the normalized flow on \(\mathcal O_E(r)\) defined by Naumann. The catalogue's narrower flow-construction question was already answered in the cited source and its published update.

The example uses the compact base \(\mathbf P^1\), the ample bundle \(E=\mathcal O(1)\oplus\mathcal O(1)\), and a smooth strictly positive metric on \(\mathcal O_E(2)=\mathcal O(2,2)\). At time \((\log2)/2\), its horizontal curvature at one point equals exactly \(-1/96\). No numerical PDE solution is used.

Files:

* `PROOF.md`: complete construction, global positivity, exact evolution, and analytic dependencies.
* `SOURCE_GATE.md`: primary-source recovery, corrected scope, and source-normalization checks.
* `ATTEMPT_LOG.md`: three substantive approaches, stopping upon the full counterexample candidate.
* `verify.py`: exact symbolic verification and supplementary rational-grid checks.
* `verification_results.json`: reproducible verification output.
* `FROZEN_MANIFEST.json`: hashes and sizes of the public files submitted for review.

Reproduce using Python 3 with SymPy:

```sh
python verify.py --output verification_results.json
```

The program checks the algebra. The paper's finite-time smooth-existence theorem is an explicitly cited analytic input. The strict universal positivity bound is proved, not inferred from the grid.

This candidate is awaiting independent mathematical review. It is not a proof of, or a counterexample to, the Griffiths conjecture. No novelty or historical-priority claim is made. Source PDFs and full extracted texts are not included in the public package.
