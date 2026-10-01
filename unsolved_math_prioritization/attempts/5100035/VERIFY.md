# Verification

Run `python check_exact.py` with the already available SymPy 1.14.0.
No network or package installation is performed. The deterministic
receipt records 3,297 exact assertions.

The symbolic checks form each of the eight antipedal intersections,
verify both incidence equations, verify the opposite-focus cyclic
inversion, and compute the signed area. Polynomial remainders modulo
c²=a²−1 and a²=(1−t)³(1+t)/(4t³) certify the exact factorization in
PROOF.md. Separate checks certify the squared positive chord-length
relation, common confocal-caustic parameter, normal-reflection ratio,
and rational signs isolating the quartic root.

The rational controls check central equivariance and signed area for
105 generic centrally symmetric polygons. These are not asserted to be
billiard orbits; their role is to challenge the purely Euclidean lemma.
The genuine billiard 8-orbit is certified symbolically in the preceding
checks and analytically in the proof.

No floating-point root or numerical zero is used to certify the example.
The source symmetry theorem and the universal geometric argument require
independent mathematical review; finite controls are not substitutes.
