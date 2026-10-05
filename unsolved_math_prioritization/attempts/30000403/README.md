# Optimal universal coarse Hurwitz lifting bound

**claimed_solved, 3/5; independent AI audit passed with nonblocking notes.**

In characteristic zero with r >= 3, the universal upper bound for reduced-to-ordinary inner coarse Hurwitz lifting degree is two. An explicit six-branch C2 example attains two over Q. The V4 geometric base-stabilizer stratum has degree one.

Start with [release clarifications](RELEASE_CLARIFICATIONS.md), then the unchanged [complete proof](packet/PROOF.md), [independent audit](audit/AUDIT_REPORT.md), and [separate recommendations](audit/CORRECTIONS.md). The result is a sharp universal constant, not a pointwise classification, a general actual-cover descent assertion, or a novelty certification. AI tools were used extensively; the work is unrefereed, without external human peer review or formal verification.

## Portable verification

Python 3.12 with SymPy 1.14.0 reproduces the recorded environment. From any working directory, run the absolute or relative path to:

    python -B verify_release.py

The release wrapper verifies the complete inventory, fixed author and audit hashes, exact ZIP member sets and bytes, and all author and independent replays. Optimized Python is explicitly rejected. The original audit verifier remains available:

    python -B audit/verify_audit.py --author-root . --replay

The two author replays reproduce 1,754 exact assertions and 32 symbolic assertions byte-for-byte; the independent replay reproduces 96 assertions and its exact certificates. Finite checks support the calculations, not a formal proof of the universal descent theorem.

The frozen author files, author archive, full safe audit files, audit archive, and audit receipt are unchanged. Historical pending-review fields remain historical and are superseded by the release clarifications. Public source titles, URLs, hashes, sizes, and inspection history are retained; source PDFs/text, dataset contents, and private coordination are excluded. LIVE_GATE.json binds the independent live repository check; RELEASE_MANIFEST.json binds every file other than itself.
