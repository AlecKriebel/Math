# Problem 6200061: safe author package

This package studies Kleiner's Problem 61 on Ahlfors-regular versus equivariant conformal dimension. It does not solve the general conjecture.

The main partial result is a complete elementary obstruction to a stronger, marked version of realization: a surface-group boundary admits an optimal Ahlfors 1-regular metric for which one group element is not Lipschitz, whereas every isometry acts bilipschitz on a visual boundary. This does not contradict the existence of another optimal visual metric.

Read PROOF.md for the argument, APPROACHES.md for all five routes, and SOURCES.json for public-source credit and inspection metadata. IDENTITY.json records the reviewed target and corpus hashes without distributing any corpus contents. RESULTS.json contains only authored algebra/cylinder checks.

Run:

    python3 verify.py
    python3 -O verify.py
    python3 test_suite.py

The verifier uses only Python's standard library. It checks the exact file roster and byte hashes, the declared claim scope, exact polynomial identities and Bernstein positivity, and finite rational regression data. It is not a proof assistant and cannot certify the geometric arguments or the completeness of a literature search. The Bernstein certificate is a finite symbolic certificate for a universal polynomial inequality; the 80 dyadic samples and finite cylinder checks are regression checks only.

The test suite checks a relocated copy under normal and optimized Python and requires corruptions, missing/extra files, false claim status, and semantic algebra mutations to fail. Some semantic mutations are rehashed deliberately, so detection is not solely a manifest-hash effect. The frozen archive and external receipt provide the package identity; an adversary able to replace the verifier and the external receipt is outside this integrity model.

No third-party PDFs, extracted source text, corpus records, private sources, or coordination material are included. Public titles, URLs, hashes, byte counts, and inspection metadata are included. No remote repository mutation, publication, or outreach was performed for this package.
