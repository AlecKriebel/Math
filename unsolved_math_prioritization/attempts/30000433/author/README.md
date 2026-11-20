# Five-or-six edge-degree triangulations: scoped partial research

Problem 30000433 / OWR-1194-002; catalog rank 812.

The universal weak 5/6 and stronger TCP questions remain unresolved by this work. Four substantive approaches produce necessary incidence constraints, universal barriers to specified local-move methods, a lower bound on octahedral replacement size, and a conditional gluing lemma with exact S3 and S2×S1 controls. No novelty claim is made.

Read MATHEMATICAL_NOTE.md for complete arguments and the exact remaining gap. SOURCE_AUDIT.md separates nearby published theorems from this target and records access limits. SOURCE_METADATA.json contains hashes and inspection provenance only.

Python 3 standard library is sufficient:

    python3 verify.py
    python3 -O verify.py
    python3 test_replay.py
    python3 -O test_replay.py

For externally anchored file-integrity checking, pass the SHA-256 of MANIFEST.json:

    python3 verify.py --manifest-sha256 HEX_DIGEST

The tests run normal and optimized replay from a relocated directory, reject semantic result mutations even when no checksum pin is used, and reject source/result/manifest tampering when the external pin is supplied. A manifest cannot authenticate itself; keep its digest or the outer ZIP digest outside the package. An adversary allowed to rewrite both the program and its external trust anchor is outside this integrity model.

The exact computations reconstruct the classical 600-cell in Q(sqrt(5)), check every supporting hyperplane and manifold link, and build controlled simplicial gluings. They supplement the written mathematics; they are not formal proof-assistant verification or proof of the general existence conjecture. This AI-assisted note has not undergone conventional human peer review.
