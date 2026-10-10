# A complete decision on the periodic {2,3} sandpile subclass

Problem 20000976 / AIM-COMBINATORICS-0101. Accepted partial result, substantive attempt 1 of 5. The general periodic {0,1,2,3} decision problem is unresolved by this work; no novelty or priority claim is made.

## Established results

For a P×Q-periodic square-grid background taking only heights 2 and 3, some finite addition at the origin explodes exactly when every cell row and every cell column contains a 3. Scanning the cell decides this subclass in O(PQ) time. On the explosive subclass the proof supplies the explicit, nonsharp source bound

N(c) ≤ 4^(ceil((P−1)/2) + ceil((Q−1)/2) + 1).

The [complete mathematical report](MATHEMATICAL_REPORT.md) and [independent mathematical audit](MATHEMATICAL_AUDIT.md) also establish:

1. An explicit integer tent-barrier certificate whenever one periodic family of whole rows OR columns has height at most 2. Every finite origin source then stabilizes pointwise, even for general stable heights 0 through 3.
2. An effective conversion from a full-rank lattice input to rectangular periods by the signed adjugate identity.
3. A decidable sufficient certificate class using periodic integer-Laplacian modifications, with full proof of bounded-potential source-threshold invariance. Exhaustiveness for arbitrary four-height input is not proved.
4. A full-rank periodic example with infinitely many total topplings but at most one toppling at each site: heights 3 on even rows and 2 on odd rows, with one chip added at the origin. Its exact odometer is the indicator of the central row.

All analytic arguments, displayed formulas, constructions, examples and mathematical qualifications are included. The known face-propagation mechanism is explicitly credited to Fey–Levine–Peres. The report gives its elementary finite seed and complete one-direction barrier arguments without relying on supplemental programs.

## Essential distinctions and limits

Pointwise stabilization means every individual site's total toppling count is finite. It does not require finitely many total topplings or a finite toppled set. The strip barrier proves only the stated pointwise conclusion. Fey–Levine–Peres use “robust” for the stronger finite-growth notion.

The general case with low sites and a height-3 site in every row and column is not decided here. The two sufficient certificate mechanisms are not claimed to be complementary on arbitrary periodic input. No undecidability theorem, finite-torus replacement, density classification, three-to-two-dimensional reduction, or exhaustive periodic-potential reduction is established.

## Review and distribution

[ACCEPTANCE.json](ACCEPTANCE.json) binds the exact distributed report and audit; [STATUS.json](STATUS.json) records accepted partial attempt 1/5 and the remaining gap. This AI-assisted, unrefereed proof-and-audit edition is not external human peer review, journal acceptance or formal proof-assistant certification. Acceptance rests on the complete written mathematics. Aggregate supporting check totals are retained as historical audit metadata; they are not infinite-volume proofs and were not rerun during edition preparation.

[SOURCE_METADATA.json](SOURCE_METADATA.json) records public citations, three public-PDF byte identities and bounded retrieval/inspection history. Edition preparation makes no fresh source retrieval, source-file rehash, source inspection or literature-search claim. No comprehensive current-openness claim is made.

[MANIFEST.json](MANIFEST.json) lists exactly seven distributed files and hashes the other six; the pull-request body independently pins the manifest. File hashes verify packaging integrity, not mathematical correctness.

Programs, fixtures, detailed computational output, datasets, copied source documents or text, source-derived images and private coordination material are excluded. There is no omitted-file dependency. This addition-only edition leaves QUEUE.md and unrelated entries unchanged, adds no substantive proof turn and does not reset attempt accounting.
