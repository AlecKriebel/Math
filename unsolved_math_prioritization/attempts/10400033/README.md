# Willerton’s bound for the third Vassiliev invariant

A candidate proof of Ohtsuki Conjecture 2.11 is in [CANDIDATE.md](CANDIDATE.md). It uses the Polyak–Viro formula and random tournament completions, with a slightly stronger bound for even crossing counts. The complete argument passed a separate [adversarial AI review](review/REVIEW.md); historical novelty and human peer review remain unestablished. The candidate retains its original review-pending header to preserve the exact reviewed bytes. The review establishes its current status.

Run python3 verify.py here. The two distinct exact methods pass 42,867 assertions: direct Jones bracket calibration on 59 classical braid closures, and graph/sign controls on 1,814 oriented chord diagrams and 1,099 tournaments. The general theorem rests on the written proof, not the bounded computation.

[SOURCES.md](SOURCES.md) records normalization, exact source scope, and a discrepancy in the original problem list’s older-bound display. No source PDFs are redistributed. Only one substantive proof attempt was used.

The independent reviewer reproduced all author controls and passed 115,776 additional exact assertions. Run `python3 review/independent_checks.py` for the independent checks. The preserved `review/author_replay/CANDIDATE.md` is a required hash-check dependency.
