# Local-to-global medianity, record 30006624

Status: **UNSOLVED after five distinct mathematical approach families**. The local-median subquestion of 30006622 shares this budget; its unrelated group questions are not attempted here. No novelty or full-resolution claim.

Read PARTIAL_REPORT.md and VARIATIONAL_AND_BICOMBING.md together. SOURCE_AUDIT.json binds the public primary sources and local corpus hashes. BUDGET.json records the five mechanisms and gaps. Verification is supplemental exact arithmetic and scope auditing, not a proof of the unresolved globalization step.

The source-free frozen candidate includes authored mathematical text, small standard-library checking programs, public URLs, and public provenance metadata only. Source PDFs, extracted source text, corpus bodies, private messages, and global queue files are excluded. The packet is unrefereed and extensively AI-assisted.

## Reproduction

Run from any working directory with Python 3.10+:

    python -B verify_bundle.py
    python -B verify_math.py
    python -B verify_inputs.py --corpus-dir /external/corpus --pdf-dir /external/pdfs

Repeat with -O and -OO. All programs print to stdout and use explicit exceptions, not Python assertions. External corpus and PDF inputs are optional for a math-only replay and are deliberately absent from the packet. Their expected names and hashes are in SOURCE_AUDIT.json.

The six --mutation options of verify_math.py are negative controls and must fail: accept_circle, flatten_weight, ball_closed, unique_geodesic, overclaim_uniqueness, wrong_descent_constant. They correspond to concrete wrong conclusions, not random crashes.
