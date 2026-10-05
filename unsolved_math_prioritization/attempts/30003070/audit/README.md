# Independent audit of problem 30003070

**Scoped PASS. Unsolved, five of five approaches.** No full solution, counterexample, verified full prior resolution, novelty or global current-openness claim.

Read `AUDIT.md` for the proof-by-proof adversarial review and four nonblocking precision improvements. `STATUS.json` is the machine-readable disposition. The frozen author packet remains unchanged.

## Portable replay

Python 3.10 or newer; standard library only. Run from any working directory:

    python3 -B /path/to/audit/verify_audit.py
    python3 -B -O /path/to/audit/verify_audit.py
    python3 -B -OO /path/to/audit/verify_audit.py

The standalone mathematical replay checks 68,132 explicit runtime requirements and reproduces `independent_math.json` exactly. It imports no author code and requires no network or scholarly source files.

## Optional complete evidence replay

With the independently obtained author packet, its archive, and the six PDFs named in the author's source metadata:

    python3 -B /path/to/audit/verify_audit.py \
      --author-dir /path/to/author/safe_freeze \
      --archive /path/to/PLABIC_30003070_AUTHOR_SAFE.zip \
      --source-dir /path/to/private-pdfs \
      --negative-controls

This reproduces `independent_results.json` with 68,198 checks, plus `negative_results.json`. The harness checks four optimization configurations, rejects 18 independent deliberate corruptions, and independently executes the author's 32,332-check replay and 13 original corruption controls in each configuration. A false runtime check is explicitly tested under each mode. Zero `assert` statements occur in the checked programs.

The independent mathematics uses sparse-polynomial matrix minors, full-section-space exact elimination, a different partition enumeration, fraction-free determinants, integral inverse checks, and symbolic rational braid identities. The finite checks supplement the all-degree written proof audit; they do not solve the original universal question.

## Evidence and publication boundary

`source_byte_checks.json` records six fresh private scholarly-PDF retrievals and exact matches. `descriptor_verification.json` records descriptor identity matches without reproducing its row. The imported raw problem statement and prior AI report were unavailable and were not inspected; earlier denied raw retrieval was not repeated or circumvented.

The deliverable contains authored discussion, code, exact finite outputs and public verification metadata only. It contains no PDFs, extracted source text, page images, imported dataset content, raw repository responses, or private coordination files. No remote writes were made.
