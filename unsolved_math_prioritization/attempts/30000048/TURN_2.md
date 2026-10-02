# Turn 2: an exact SU(3) classification in a specified character span

2026-10-01. Second substantive author turn. This is a rigorously finite scoped result for a simple rank-two group. It is not the full source classification, which remains unresolved. The finite enumeration below is exact and reproducible; it does not infer global positivity from a grid.

## 1. The precise partial theorem

Let chi_(a,b) denote the irreducible SU(3) character with highest weight (a,b), a,b>=0. Among functions of the form

    f=1+A chi_(1,1)+B(chi_(3,0)+chi_(0,3))+C chi_(2,2),
    A,B,C in Z,                                             (1)

the pointwise nonnegative ones are exactly the following four:

    (A,B,C)=(0,0,0), (1,0,0), (1,0,1), (2,1,1).             (2)

They are respectively the square moduli of the irreducible characters of highest weights (0,0), (1,0), (2,0), (1,1), whose dimensions are 1,3,6,8. Every function in (1) already has Haar mean one because the listed nontrivial irreducibles have mean zero.

This exhausts only the explicitly displayed integral span. It does not assume or prove that every S-character has this support, is invariant under the center, or has bounded degree. Larger weights and other simple groups remain open in this attempt.

## 2. Exact character formulas and Haar coefficient bounds

Write u=tr(g), v=conjugate(u), x=uv and y=u^3+v^3. The relevant characters are

    chi_(1,0)=u,
    chi_(2,0)=u^2-v,
    chi_(1,1)=x-1,
    chi_(3,0)=u^3-2x+1,
    chi_(0,3)=v^3-2x+1,
    chi_(2,2)=x^2-y.                                      (3)

These are standard Weyl-character consequences, rather than names assigned to arbitrary polynomials. To verify the identification explicitly, take eigenvalues z_1,z_2,z_3 with product1. For any (a,b), Weyl's formula is

    chi_(a,b)=det(z_j^(a+b+2), z_j^(b+1), 1) /
              det(z_j^2, z_j, 1),                          (4)

where the displayed lists specify the three rows of each determinant. Multiplying the candidate formulas in (3) by the denominator verifies (4) as Laurent polynomial identities. `verify_turn2.py` performs these exact identities with z_3=(z_1 z_2)^(-1), including every distinct conjugate in (1). Equality extends to coincident eigenvalues by continuity. Dimensions are (a+1)(b+1)(a+b+2)/2, giving 8,10,10,27 for the four nontrivial terms. Serre's final2025 paper, §2.3, Theorem2.4, states the general Weyl formula used here.

For any nonnegative f with integral_G f=1, Schur orthogonality and unitarity give the general coefficient bound

    |<f,chi>| <= integral_G f |chi| <= dim(chi).             (5)

Indeed each unitary representation matrix has trace of absolute value at most its dimension. Therefore a function (1) that is nonnegative must satisfy

    -8<=A<=8, -10<=B<=10, -27<=C<=27.                       (6)

There are exactly17*21*55=19,635 integer triples. No arbitrary experimental coefficient cutoff is imposed: (6) is necessary for every possible S-character in this span.

Using (3), formula (1) becomes the scalar polynomial

    f=(1-A+2B)+(A-4B)x+C x^2+(B-C)y.                        (7)

All arithmetic in the finite certificate below uses rational x,y and integer A,B,C.

## 3. Rational test coordinates realized by actual SU(3) matrices

We use two elementary families, rather than assume an unverified planar trace domain.

**Real trace family.** For any real t in [-1,3], choose theta with cos(theta)=(t-1)/2. The matrix diag(1,e^(i theta),e^(-i theta)) is in SU(3) and has trace t. Thus

    x=t^2, y=2t^3.                                        (8)

The finite certificate uses t=j/10 for0<=j<=30, and t=-j/10 for0<=j<=10. The duplication at zero is harmless.

**Repeated-eigenvalue family.** Let z=e^(i theta) and g=diag(z,z,z^(-2)). Then det(g)=1 and u=2z+z^(-2). Writing c=cos(3theta) gives

    x=5+4c,
    y=4c^2+28c+22=(x^2+18x-27)/4.                         (9)

The identities follow simply by expanding u conjugate(u) and u^3+conjugate(u)^3. Every x in [1,9] occurs, since c=(x-5)/4 is in [-1,1]. The finite certificate uses x=j/10 for10<=j<=90. Thus every one of the123 test records is an actual group element's exact trace coordinates. Negative evaluation at any such record rigorously disproves positivity on the group; no limiting or numerical argument is used.

No claim that these finitely many points characterize positivity for arbitrary polynomials is required. They will only exclude all but four triples in the proven finite coefficient box, and the four survivors receive separate global certificates.

## 4. Exhaustive exact exclusion certificate

The standard-library program `verify_turn2.py` enumerates all triples in (6), in increasing A, then B, then C. For each it evaluates (7) on the123 rational records in §3, using Python `Fraction` arithmetic. If an evaluation is negative, the first such record and the exact rational value are an exclusion witness.

The result is (in fact every exclusion already occurs in the real-trace family; the repeated-eigenvalue records are redundant corroborating controls):

-19,631 triples have a strictly negative exact value at one of the actual SU(3) records.
-Exactly the four triples in (2) have no such negative witness.

The complete algorithm, all bounds and every test point are specified above and in the portable source. It terminates after a fixed finite enumeration; there is no external solver, heuristic tolerance, random seed or unproved positivity routine. The deterministic receipt `TURN_2_CHECKS.json` records the survivor list, counts by witness family and SHA-256 of the ordered witness stream. Re-running the source reconstructs every excluded triple's rational witness, not merely the hash. The earlier `explore_turn2.py`/`turn2_probe.json` are retained as explicitly exploratory history; the theorem depends on the exact coefficient bound, actual group realizations and exhaustive certificate, not that history's grid interpretation.

The character formulas and Haar inner products are checked independently inside the program by multiplying with the Weyl alternant denominator. With normalized Haar measure, the constant term of chi*conjugate(psi)*|denominator|^2, divided by6, is the SU(3) inner product. These finite algebra controls support the analytic applicability of (5); they are not a substitute for Schur orthogonality.

## 5. Global sufficiency of the survivors

Each surviving function has an exact global square identity:

    (0,0,0): f=1,
    (1,0,0): f=x=|u|^2,
    (1,0,1): f=x^2-y+x=|u^2-v|^2,
    (2,1,1): f=x^2-2x+1=(x-1)^2.                          (10)

By (3), the square roots are the irreducible characters specified in §1. Thus positivity holds everywhere on SU(3), and Schur orthogonality gives their Haar means exactly1. The program also verifies these as exact Laurent polynomial identities. This proves the finite-span classification: every potential function is covered by the necessary integer box, every excluded one has an actual negative witness, and every survivor has a global certificate.

## 6. What the attempt learned and what remains

The first low-rank simple-group search produces no counterexample in this natural small center-invariant span. It does not prove that no counterexample exists in a larger span, in a non-center-invariant component, or for Sp(2), G2 or another simply connected compact group. Coefficient bounds by representation dimensions give finite searches only after a support restriction is supplied; they do not provide an a priori support bound for the original problem.

The exact higher-rank Weyl density has more extremal terms than the rank-one density. The all-r product theorem in turn1 does not convert that geometry into the same one-variable equality classification. A subsequent substantive turn must address a genuinely broader mechanism or a different counterexample family.

Original source status in this campaign: **unresolved after2/5 substantive author turns**. This finite classification and the product theorem require separate independent review before any partial-result PR. Classical character formulas, Schur orthogonality and Serre's prior rank-one work retain credit; no historical novelty assertion is made.
