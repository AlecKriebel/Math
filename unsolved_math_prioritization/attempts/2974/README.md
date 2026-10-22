# Fixed-manifold Lefschetz pencils: accepted partials

Problem 2974 / KP-4.98 remains **unsolved**, with **5/5** substantive approaches. Start with [ACCEPTANCE.md](ACCEPTANCE.md), then the unchanged [author report](author/packet/REPORT.md), [independent audit](audit/packet/AUDIT_REPORT.md), and [Johnson addendum](audit/packet/JOHNSON_QUOTIENT_ADDENDUM.md).

The exact degree-one-factor HH18 qualification, conditional classification consequences, irreducible-Johnson-module limitation, intrinsic saturation-index alternative, and odd-prime factor-two test limitation must accompany any summary. No universal solution, novelty, peer review, or formal certification is claimed.

## Reproduction

Use Python and its standard library. Actual UID and EUID 1000 are required. Before running any code, obtain the BOOTSTRAP.py SHA-256 from the independently recorded PR description or acceptance receipt and compare it with the local file. Do not accept a trust anchor supplied only by an untrusted packet.

    sha256sum BOOTSTRAP.py
    python -I -S -B BOOTSTRAP.py /absolute/path/to/packet
    python -I -S -B -O BOOTSTRAP.py /absolute/path/to/packet
    python -I -S -B -OO BOOTSTRAP.py /absolute/path/to/packet

For the strict negative controls and hostile read-only relocation, first authenticate the bootstrap and verifier, then the complete packet manifest. The included mutation driver is authenticated by that manifest. Supply the separately trusted bootstrap pin:

    python -I -S -B mutation_tests.py --root /absolute/path/to/packet --bootstrap-sha256 TRUSTED_PIN

Repeat with -O and -OO. The driver emits all replay stdout/stderr and checks negative controls on disposable copies; it leaves the packet unchanged. The native historical audit is preserved unchanged and replayed against an exact hash-verified reconstruction of the author archive. The gzip reconstruction deliberately fails if a runtime produces different compressed bytes.

Full local and remote execution receipts are retained separately from the frozen publication so that executing checks cannot alter its manifest. Fresh sources and corpus checks are NOT_RUN. Finite arithmetic checks do not certify geometric existence, smooth equivalence, imported theorems, or the universal problem.
