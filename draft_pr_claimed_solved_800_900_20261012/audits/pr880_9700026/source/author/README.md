# 9700026: literal conjecture refuted by persistence

The attached proof gives a geometric lower bound on every city weight for beta>2alpha. In particular alpha=2, beta=8 contradicts the alpha>1 collapse clause of the 2007 associated-system conjecture, for all distinct interior sites and all positive starting weights. The illustrated three-city configuration is certified by exact rational arithmetic.

- PROOF.md: self-contained argument, model scope, and remaining questions.
- SOURCE_AUDIT.md: source-version and literal-versus-intended distinctions.
- certificate.json: authored rational witness.
- verify.py: standard-library exact checks and adversarial tests.
- verification_results.json: normal, optimized, isolated, and relocated execution receipts.
- PUBLIC_METADATA.json: public-source and corpus hashes, byte counts, and verification results only.

Run: python verify.py certificate.json
Run adversarial tests: python verify.py --self-test

These checks support the constants and algebra; they are not a formal proof assistant and do not certify the source interpretation or replace review of the analytic proof. No source PDFs, copied corpus records, dataset contents, or private coordination files are included. The author bundle awaits independent mathematical and source review.
