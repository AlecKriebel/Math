# Author turn 4: complete local scalar-weight classification for the test pair

**Scoped partial; general source Q1 remains unresolved.** 2026-10-01.

This turn attacks genuinely local two-color weights, rather than arbitrary action cocycles. It completely classifies normalized scalar weighted welded representations for the three-color pair from Turns 2–3 and for its twist-second violin reduction. In this case every such enrichment is a tensor-diagonal coboundary, so it cannot make the second component representation-theoretically essential.

## 1. Exact coefficient model and normalization

Let X=F_3. Use the original pair

    r(x,y)=(y−x,−x),       s(x,y)=(−y,−x)

and its actual twist-second reduction

    R(x,y)=(−x−y,x),       t(x,y)=(y,x).

The latter is **not** the rack-derived r′ of Q2. The coordinate relabeling H_n(x)_i=(−1)^(i−1)x_i directly intertwines (r,s) and (R,t), in every strand number.

Let a,b:X²→K* weight whole classical and virtual generators as in TURN_1 equation (2). Require all weighted YBE, involution, mixed and welded relations. Impose normalization a(x,y)=1 when r(x,y)=(x,y), and b(x,y)=1 when s(x,y)=(x,y), and the corresponding conditions for R,t. This is the ordinary fixed-pair Reidemeister-I normalization in this scalar whole-crossing model.

The theorem below holds for every coefficient field K. More generally, the same multiplicative tables classify weights valued in any abelian group. It does not purport to classify the nonabelian ordered strandwise cocycles in Farinati–Garcia Galofre, and does not replace their definition by this simpler scalar model.

## 2. Complete original-pair classification

Every normalized weight pair for (r,s) has the following tables, with arbitrary A,B in K*; rows and columns are ordered 0,1,2:

    a = [[1, 1, 1],
         [A, B³/A, 1],
         [A/B³, 1, 1/A]],

    b = [[1, B, 1/B],
         [B, B², 1],
         [1/B, 1, 1/B²]].                              (1)

Conversely every A,B gives valid normalized welded weights.

For a conceptual explanation of the converse, put lambda(0)=A/B, lambda(1)=B, lambda(2)=1. For either pair operation p=r or p=s, the corresponding weight in (1) is

    lambda(x)lambda(y)/[lambda(p_1(x,y))lambda(p_2(x,y))].  (2)

Thus it is a local tensor-diagonal coboundary. With D_n e_x=(product_i lambda(x_i))e_x, the weighted representation is D_n^(-1) rho D_n. This proves all group relations, for all n, with no division by an integer or extraction of roots. In particular, this assertion remains true in characteristic three despite the different Q2 result in Turn 3.

## 3. Complete twist-second classification

All normalized weights for (R,t) have, with arbitrary P,Q in K*,

    a′ = [[1, P, 1/P],
          [Q, 1, 1/Q],
          [Q/P, P/Q, 1]],

    b′ = [[1,1,1],[1,1,1],[1,1,1]].                    (3)

Here (2) holds with lambda′(0)=Q, lambda′(1)=P, lambda′(2)=1. Again every such enrichment is conjugate to the unweighted representation for all n.

## 4. Why the classifications are complete over arbitrary coefficients

The check is a finite integer-lattice certificate, not a dimension count over a chosen prime field.

Order the 18 unknown weights as a_00,a_01,...,a_22,b_00,...,b_22. For each triple in lexicographic order, compare the products of weights along these five pairs of words, with rightmost action first:

1. r_1 r_2 r_1 versus r_2 r_1 r_2
2. s_1 s_2 s_1 versus s_2 s_1 s_2
3. s_1 s_1 versus the identity
4. s_1 r_2 s_1 versus s_2 r_1 s_2
5. s_1 r_2 r_1 versus r_2 r_1 s_2

After these 135 rows, append one normalization row for each fixed pair of r and then of s, in pair-index order. This produces a 141-by-18 integral relation matrix M. A row m means product_j w_j^(m_j)=1; no additive logarithm assumption is being made.

For (r,s), take free columns 3 and 10, the parameters A=a_10 and B=b_01. Delete these columns and select zero-based rows

    138,8,15,16,17,21,23,26,45,48,49,50,53,55,58,135.

The resulting 16-by-16 matrix has determinant −1. Its inverse is therefore integral, and its selected equations solve every other weight uniquely as a monomial in A,B, giving (1). Substitution into all 141 equations verifies the converse independently of the coboundary argument.

For (R,t), use free columns 1 and 3, corresponding to P=a′_01,Q=a′_10, and rows

    138,8,15,17,19,20,23,24,25,29,30,45,48,49,55,135.

This minor also has determinant −1 and gives exactly (3). The checker saves both complete relation matrices, verifies both determinants, solves with integral exponents, and checks every original relation. Thus there is no hidden torsion component or characteristic-dependent family omitted by a rational-nullspace calculation.

## 5. Consequence for Q1 and the remaining gap

For this test pair, any normalized scalar local enrichment is first removed by D_n, then transported through H_n to the unweighted twist-second pair. It is therefore realized by a local weighted twist-second pair, even though raw transport of the original a,b need not be slot-independent. The necessary correction is a legitimate diagonal gauge, not an unsupported locality assertion.

This closes a concrete attempted obstruction to Q1, rather than proving that all welded pairs behave this way. General pairs may have nontrivial normalized cocycle classes; nonabelian strandwise weights contain additional order information; and braids without the stated normalization can have extra classes. None is classified here. The general OWR Q1 and its independent characteristic-zero Q2 remain unresolved.

Substantive author turns: 4/5. Completion estimate25% toward the full source bundle. The finite classification is an exact scoped result, with no claim of historical novelty. A fifth distinct attempt will inspect the additional welded descent requirement in the source's actual nonabelian virtual-cocycle reference, where a virtual invariant alone is insufficient.
