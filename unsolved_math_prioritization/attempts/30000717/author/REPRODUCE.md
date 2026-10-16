# Reproduction and limits

Run from this directory:

    python verify.py > checks.replayed.json
    cmp checks.json checks.replayed.json

Environment used: Python 3; SymPy version recorded in checks.json and pinned in requirements.txt. The output is deterministic. No network, source PDF, dataset, SDP solver, or numerical tolerance is required.

The 185 exact assertions check the homogeneous sextic, coordinate/sign symmetry, Schur identity and its nonnegative ordered-coordinate expansion, ten critical zero lines, cross-product and tangency-minor vanishing on those lines and the axis, the axis polynomial, degree-0 through degree-3 interpolation ranks, the cubic determinant and inverse, the elementary coefficient lemma, Euler's identity, and the separate literal-product diagnostic.

The final epsilon extension relies additionally on two elementary facts proved in PROOF.md: a real polynomial bounded on the whole real line is constant, and a sum of real polynomial squares has twice the maximum degree of its nonzero summands. These are universal mathematical arguments, not finite tests. The exact-only v1 preceded this extension; no v1 limitation that leaves condition (iv) undecided applies to the current candidate.

Finite exact controls supplement the written proof; they do not certify its logic by themselves. No formal proof assistant or conventional external human peer review is claimed. Reviewers should especially check the all-real-t restriction, arbitrary degrees and number of SOS summands, ordinary versus real radical, epsilon constants, and the source-formula discrepancy.
