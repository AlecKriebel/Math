# 30002203: specified pentagon-arrangement symmetry

The original two-part lifting question remains unsolved after two approaches.

The package identifies the exact eight-line arrangement, gives its order-four meridian permutation, proves that this permutation has no affine/projective self-realization, and exhibits a geometric lift of its square. An explicit coordinate change identifies the projectivization with the classical Falk–Sturmfels arrangement. Existing unmarked equivalences are distinguished from the requested marked automorphism.

- [Scoped argument and exact remaining gap](OBSTRUCTION.md)
- [Primary sources](SOURCES.md)
- [Research log](RESEARCH_LOG.md)
- [111 exact finite-geometry controls](verification.json)
- [Uncertified exploratory truncation screen](exploratory/README.md)

[Separate adversarial AI review passed](review/REVIEW.md). This has not undergone human peer review. No novelty is claimed.

Reproduce the exact geometry controls with Python3 and SymPy:
    python verify.py

The checker prints JSON and reads the adjacent OBSTRUCTION.md. The exploratory program is separate and does not certify a fundamental-group or E-infinity lift.
