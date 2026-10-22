# Independent audit of problem 30001603

**Verdict: mathematics passes; a factual source-description correction is required.**

The prior DJS example refutes the inspected primary conjecture at k=1. Its toric bundle is locally free, nef, has tau=1, and has value/first-jet ranks 2/3 and 7/9 at the bad fixed point. The author packet incorrectly claims that the journal prints a sign error. Both independently inspected PDFs print the correct (-1,-2) coordinate. No mathematical change is required; the false attribution must be removed before acceptance.

Files:

- AUDIT.md: full independent mathematical and source audit
- CORRECTIONS.md: exact locations, replacement prose, and dependency trace
- EXACT_BINDING.json: complete ten-file frozen-input binding and scoped verdict
- SOURCES.json: public source hashes, byte counts, retrieval and inspection metadata
- INDEPENDENT_VERIFY.py: new symbolic-matrix and polynomial-extension checks
- RESULTS.json: exact output, including 60 independent checks and eight corruption controls
- CHECK_AUDIT.py and MANIFEST.json: public-audit integrity and replay

Run `python3 -B CHECK_AUDIT.py /path/to/original/toric_jets_30001603` from this audit directory. Python3 and SymPy1.14.0 were used. The verifier imports no author modules. It independently authenticates the original packet, replays its programs, then solves the global-section problem through a different algebraic formulation. No network is needed. Temporary corruption tests operate only on disposable copies.

The mathematical proof is in AUDIT.md; exact finite arithmetic alone is not a proof of geometric nefness. The verdict is bound to the original manifest and proof hashes, and does not preapprove a revised packet. A source-corrected revision requires fresh binding and a targeted review.

Only original audit prose/code and public verification metadata are included. Scholarly PDFs, extracts, images, raw catalogue records, and private coordination materials are excluded. No remote state was changed.
