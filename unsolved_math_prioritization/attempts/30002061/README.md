# 30002061: collapse preservation under linear subdivision

**General target unresolved.** One substantive family, stopped at a precise higher-dimensional relative-collapse gap. No novelty claim; independent review pending.

`PARTIAL.md` gives the exact reduction to one subdivided simplex with a protected boundary target and reconstructs a planar dual-tree/pruning certificate. It proves the dimension ≤2 case, already covered by known planar theory, without claiming the full Hudson problem solved.

The original source uses linear subdivisions. Adiprasito–Benedetti's published Theorem 4.3 adds one barycentric subdivision to both complexes; that established result is credited and not substituted for the original target.

Run `python3 verify.py` with Python 3's standard library. All 4,200 exact assertions pass across 27 rational planar triangulations and 6 relative gluing controls. It writes `verification.json` and the explicit small `sample_certificate.json`. These are finite controls, not a high-dimensional census or proof.

Model: gpt-6-astra, xhigh. Recommended queue status: **unsolved**, 1/5. The coordinator owns shared queue updates.
