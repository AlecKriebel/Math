# Problem 30001148: a known negative answer

The general local-global implication is false. This packet credits the 2016 counterexample of Colliot-Thélène–Parimala–Suresh and checks a second constant-torus construction from the 2020 work of Colliot-Thélène–Harbater–Hartmann–Krashen–Parimala–Suresh.

- [Exact question, matched counterexamples, and hypothesis checks](RESULT.md)
- [Sources and place conventions](SOURCE_AUDIT.md)
- [Research record and early stopping](RESEARCH_LOG.md)
- [Machine-readable status](STATUS.json)
- [Supplementary exact checks](checks/check.py) and [their receipt](checks/result.json)
- [Frozen author manifest](AUTHOR_MANIFEST.json)

This is a credited literature resolution, not a new discovery or a claim about projective homogeneous spaces. Author recommendation: already_solved, 1/5, subject to independent review. The five-turn limit permits stopping early on a complete resolution. No human peer review or formal verification is claimed.

To reproduce the supplementary checks, use Python 3 and SymPy (tested with 1.14.0):

    python checks/check.py

The program prints JSON to stdout and does not access the network or write files. Mathematical proofs and theorem hypotheses remain the decisive evidence.
