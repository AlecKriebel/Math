# Problem 30003070: partial research packet for independent audit

**Unsolved, 5/5 approaches. Independent audit pending.** This is an author packet; no remote publication was performed.

Read `MATHEMATICS.md` for the exact all-Grassmannian, all-reduced-top-cell-graph target, complete partial proofs, and the precise gap in each approach. The source's numeric landing page was unavailable, and the imported full raw statement and prior AI report were not inspected. The original 2016 OWR question was inspected directly.

The most useful retained result is the all-degree unit-cube bound for type-A root-sequence bodies. A determinant-one calculation shows that a known nonintegral Gr(3,6) plabic body passes this test, so it supplies no counterexample. The packet also contains a complete small semigroup proof and explicit controls against identifying birational charts, tropical mutations, or abstract toric fibers with one global unimodular valuation comparison.

Run from any directory, with Python 3.10+ and no third-party packages:

    python3 /path/to/packet/verify_release.py
    python3 -O /path/to/packet/verify_release.py
    python3 /path/to/packet/verify_negative_controls.py

The first command checks the strict file manifest and reproduces every byte of `expected_math.json`. `verify_math.py` contains explicit runtime checks, so Python optimization does not disable them. The negative controls independently corrupt copies of the packet and require rejection.

Optional source-byte verification is available only when the reader has separately retrieved the six public PDFs:

    python3 /path/to/packet/verify_release.py --source-dir /path/to/private/pdfs

The source metadata distinguishes retrieved bytes from selectively inspected passages and from unrerun computational classifications. No PDF, source text extraction, rendered page, imported dataset, or private coordination file is included. Finite controls verify the stated finite algebra; they do not prove the universal target.
