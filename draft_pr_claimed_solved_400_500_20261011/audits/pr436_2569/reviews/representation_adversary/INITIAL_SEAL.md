# Independent representation seal — PR436 / 2569

Frozen head: `c7805ab0804f50c6f4b0d1dda99e433dbb702ae2`.
Scope: exactly the saved candidate `G=SL(2,5)`, `p=2`. Original research budget is 5/5; no new candidate search was performed. Finding: **PASS for the representation and finite-module mechanism**, subject to the explicitly mathematical bridges below. Completion toward this assigned verification: 90%.

This assessment was formed before opening the historical `independent_audit` and `contributor_checks` conclusions or any current peer conclusions. The frozen `COUNTEREXAMPLE.md`, `README.md`, `SOURCE_GATE.md`, and receipt were read; no author program was executed.

## Actual F2 modules and completeness

I enumerate SL2(F4), using F4=F2[t]/(t²+t+1). Its action on P1(F4) consists of 60 distinct even permutations on five points, hence identifies it with A5. Let U be its natural F4² module viewed over F2 and S the augmentation of that five-point permutation action.

The matrices of U span the eight-dimensional algebra M2(F4). The matrices of S span all sixteen dimensions of M4(F2). Independent commutant calculations give dimensions 2 and 1 respectively. Thus U is F2-simple with End(U)=F4, and S is absolutely simple. Each representation homomorphism is checked on all 3,600 products.

The joint map F2A5 -> F2 × M2(F4) × M4(F2) has rank 25. Its 35-dimensional kernel has ideal powers of dimensions 35, 27, 17, 9, 0. A nilpotent ideal with this semisimple quotient is exactly the radical, proving completeness of the three types. This replaces a copied modular character table as the completeness input.

For each simple matrix component, I solve for a preimage of a rank-one diagonal matrix and square repeatedly until obtaining an idempotent. The three actual left ideals have dimensions 12, 16, 4, and their quotient idempotents are primitive. Therefore these are the three PIMs. The S module is also independently regular on a Sylow two subgroup: one basis vector has an orbit spanning dimension four.

## Independently derived classes and rational witnesses

The order-five averaging idempotent produces a 12-dimensional C5 coset permutation module whose simple top is just 1, so it is P(1). Its odd-order character is (12,0,2) at orders (1,3,5). The three simple Brauer characters are

- 1: (1,1,1);
- U: (4,-2,-1);
- S: (4,1,-1).

For U, an order-three natural matrix has primitive third roots as eigenvalues, giving their sum -1 twice after restriction of scalars. An order-five natural matrix and its Frobenius conjugate together have all four primitive fifth roots as eigenvalues, giving sum -1. These are exact root-of-unity identities. S follows directly from permutation fixed points. The three rows are independent. Thus [P(1)]=4[1]+2[U]. The regular module multiplicities are 1, 2, 4 from the dimensions over the endomorphism fields. Subtracting P(1) and 4S from the regular character gives [P(U)]=4[1]+3[U]. The final PIM is S.

The actual rational V4 is the five-point augmentation. The actual rational V5 is the augmentation of the permutation action on the six Sylow-five subgroups. Character norms equal one, proving complex and therefore rational irreducibility. On odd orders their reductions are S and 1+U respectively.

The central square-zero quotient then doubles every PIM composition class. Exact nonnegative witnesses, in coordinates (V1,V5,V4), are (4,4,0), (2,6,0), (0,0,2). The regular dimension identity is 24+2·32+4·8=120; the middle multiplicity is two, not four, because End(U)=F4.

## Actual binary-icosahedral construction

The 120 unit quaternions are constructed over Q(sqrt(5)). I check all 14,400 products for closure and for preservation by an explicit reduction map to SL2(F5): sqrt(5) maps to zero, and i,j map to the anticommuting matrices [[0,1],[-1,0]] and [[0,2],[2,0]]. Their squares are -I. This reduction is a bijection onto all 120 determinant-one matrices; it certifies an actual group isomorphism, beyond quaternion closure alone.

The quaternion embedding a+bi+cj+dk -> [[a+bi,c+di],[-c+di,a-bi]] is an actual representation in SU2. Its symmetric cube is therefore an actual complex degree-four representation, with trace x³-2x. The exact computation gives character norm 1 and Frobenius–Schur indicator -1. Irreducibility follows from the norm only after this actual representation construction.

A separate exhaustive product check certifies SL2(F5)/{±I} -> SL2(F4)=A5. I lift the three previously constructed primitive idempotents across the central kernel by squaring. The actual G-left ideals have dimensions 24, 32, 8. Multiplication by t=z-1 has equal image and kernel dimensions 12, 16, 4, and quotient dimensions 12, 16, 4. The group action commutes with t because z is central; this is the actual filtration used to double the classes.

The enumerated G has nine conjugacy classes with sizes 30,20,12,12,20,12,12,1,1. Their orders, square classes, and both degree-four characters are in the raw result. The forced rank-eight projective character, equal to the odd-order Brauer character and zero on even orders, is exactly chi_plus+chi_minus on all 120 elements. The two degree-four characters are actual irreducibles and orthogonal.

## Mathematical bridges and limits

The following standard deductions are explained mathematically rather than encoded as a proof-assistant certificate: full matrix-algebra image implies the stated simplicity and endomorphism field; a nilpotent kernel and semisimple quotient identify the radical; primitive diagonal idempotents yield PIMs; Brauer characters inject G0; projective integral characters vanish on p-singular elements; Frobenius–Schur -1 forces even multiplicity in real, hence rational, representations; semiperfectness supplies projective lifts. None of these transfers the central difficulty to a new unproved claim in the candidate. The actual character constructions and quotient/idempotent computations avoid the important circularity risks.

This seal does not certify priority, current source status, specialist human review, or formal proof-assistant checking. It verifies the existing exact candidate, not an additional research attempt.

## Verifier failure preserved

The first independent run expected an incorrect ordinary involution value 4 for the C5 coset permutation module. An involution fixes no coset of an odd C5, so the correct value is 0. The original failed source and raw traceback are preserved under `private/failed_run_01.*`. The odd-order values used in the proof were already correct. All checks use explicit exceptions and remain active under Python -O.
