# Reviewed result: original problem 3356 remains unsolved

**Disposition: unsolved, 5/5 substantive author turns. Independent scoped review: PASS, no mandatory mathematical revisions.**

The original question asks whether 3 is a primitive root for every prime p=16q^4+1 with q>3 prime. No universal proof or original counterexample is claimed.

The exact finite theorem covers every prime 3<q≤100,000,000. There are 418,013 prime values p, all with a complete Lucas certificate proving that 3 is primitive. The other 5,343,440 values are certified composite. Both the full author replay and a separately implemented million-bound reconstruction passed.

The analytic partial results include the precise order obstruction, an auxiliary fixed-q Kummer–Chebotarev progression theorem, the classical quartic-reciprocity specialization 3^(4q^4)≡−4q^2 modulo p, and a Frobenius split/irreducible dichotomy. The progression primes do not select the diagonal value p=16q^4+1. The exponent-42 neighboring counterexample changes the exponent. The octic sign formula is finite-only. None resolves the original universal assertion.

## Reader map and preservation

- `FINAL_README.md`: final author overview and all five reproduction commands
- `TURN_1.md` through `TURN_5.md`: complete arguments and remaining gaps
- `independent_review/ADVERSARIAL_REVIEW.md`: independent full scoped mathematical and source audit
- `independent_review/independent_checks.py`: separate exact checker with 89,896 passing assertions
- `independent_review/AUTHOR_REPLAY_RECEIPT.json`: all five author replays, including the complete 100-million bound
- `FROZEN_MANIFEST.json`: the unchanged 30-file author packet, including this manifest
- `independent_review/REVIEW_MANIFEST.json`: unchanged independent review evidence
- `PUBLICATION_MANIFEST.json` and `verify_publication.py`: portable hash checks

Earlier files, including the one-turn `README.md`, are historical checkpoints retained byte-for-byte. This document and `FINAL_README.md` give the final five-turn scope; earlier bounds and status statements are not silently rewritten.

The full per-q certificate streams are **regenerable, not retained** in this repository bundle. The scripts generate and hash the streams; the remote files preserve scripts, aggregate receipts and hashes. A stream digest alone is not a stored collection of certificates. The finite theorem rests on the audited exhaustive algorithm and its full replay.

## Exact unresolved statement

For every prime q>100,000,000 with p=16q^4+1 prime, exclude

    3^(16q^3) = 1 (mod p),

or find an original counterexample. Equivalently, rule out complete splitting of T^q−3 over F_p. No proof of this exclusion is supplied.

The anonymous 2012 source reduction, classical reciprocity, Chebotarev and historical sources are credited. AI-assisted research and independent AI review are disclosed; neither human peer review, formal proof-assistant certification nor novelty certification is claimed.
