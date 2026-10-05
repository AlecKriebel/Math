# Independent audit for 30002046

Verdict: PASS WITH SCOPE LIMITS. Exact partial results verified; fixed-point count, uniqueness and transcendence remain unproved in the audited investigation.

Files:
- AUDIT_REPORT.md: full mathematical and source-scope review
- BINDING.json: immutable input binding
- independent_verify.py: independent exact implementation, standard library only
- INDEPENDENT_RESULTS.json: rebuilt certificate, bisection trace, scan and negative controls
- INDEPENDENT_RUN_LOG.txt: independent execution log
- AUTHOR_REPLAY_LOG.txt: separate replay of the author's checker
- SOURCE_AUDIT.json: public-source retrieval and inspection metadata
- AUDIT_MANIFEST.json: hashes and sizes of this audit's payload files

Recheck without modifying either packet:

    python3 independent_verify.py /path/to/original/safe --check

The original directory must have the exact eight payload files and original MANIFEST.json. The command reads that packet and compares regenerated audit results byte for byte. It uses no network and never imports the original verify.py.

PDFs, source text and images, raw records and private coordination are excluded. The input packet was preserved. No remote repository writes were performed by this audit.
