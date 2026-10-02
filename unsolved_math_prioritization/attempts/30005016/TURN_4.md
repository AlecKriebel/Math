# Turn 4: the sharp minimum for directional cubic spaces is six

AI-assisted mathematical proof candidate; independent review pending.

## Restricted theorem

Restrict the allowed four-dimensional spaces to V_ℓ=span_K{1,ℓ,ℓ²,ℓ³}, where ℓ is a nonconstant affine linear polynomial. Over every characteristic-zero field K, the least size of a covering family of this restricted kind is exactly six.

This does not determine the original minimum: the unrestricted five-space construction already does better. The purpose of this turn is to close a plausible but inadequate construction route rigorously, rather than substitute univariate interpolation for the original problem. No novelty claim is made.

## 1. Direction reformulation

V_ℓ interpolates a four-point set exactly when the four ℓ-values are distinct, by the Vandermonde determinant. It fails precisely when a secant joining two points has direction ker(linear part of ℓ). Constant shifts and nonzero scalar factors of ℓ do not change the space. Thus a family fails simultaneously exactly when its kernel directions all occur among the at most six secant directions of the configuration.

## 2. Five arbitrary directions can always be realized

Take any five distinct directions d_1,…,d_5 in K². Set A=0 and choose any nonzero B on d_1. Let C be the intersection of the line through A in direction d_2 with the line through B in direction d_3. Let D be the intersection of the line through A in direction d_4 with the line through B in direction d_5.

The intersections exist uniquely because the paired directions are distinct. C is neither A nor B: otherwise the line AB would have direction d_3 or d_2, contradicting distinctness from d_1. The same holds for D. Also C≠D, since a nonzero common point of the two distinct lines through A in directions d_2 and d_4 cannot exist. Therefore A,B,C,D are distinct. The five secants AB,AC,BC,AD,BD have the five prescribed directions.

If a proposed family has at most five distinct kernel directions, extend them to five (the field is infinite) and apply this construction. Every member fails. Repeated directions cannot help. Hence at least six directional spaces are necessary.

## 3. Six explicit directions that cannot all occur

Take slopes S={0,1,2,4,8,16} and linear forms ℓ_s=y−s x. We prove the associated six spaces cover every four-point set.

If all six failed, all six distinct slopes in S would occur as secants. There are exactly six unordered pairs of four points, so every pair would have one of these slopes, each used exactly once. In particular none of these secants is vertical.

Label the points P_1,…,P_4, translate P_1 to the origin, and write the slopes of edges 12,13,14,23,24,34 respectively as a,b,c,d,e,f. The tuple is a permutation of S. There exist scalars α,β,γ such that

P_2=α(1,a), P_3=β(1,b), P_4=γ(1,c).

The last three secant slopes impose the homogeneous equations

−(d−a)α+(d−b)β=0,
−(e−a)α+(e−c)γ=0,
−(f−b)β+(f−c)γ=0.

Their coefficient matrix has determinant

T(a,b,c,d,e,f)=−(d−a)(e−c)(f−b)+(d−b)(e−a)(f−c).

The accompanying exhaustive integer certificate evaluates all 720 permutations. The possible absolute determinant values are exactly

24, 48, 104, 112, 136, 152, 168, 192, 272, 296, 304, 320, 344, 408, 456,

each occurring 48 times. In particular T never vanishes. The checker independently computes each determinant from the 3×3 matrix and from the product formula, and stores all 720 rows in TURN_4_CERTIFICATE.csv. This is a complete finite certificate for this explicitly finite step, not a sample over configurations.

Every listed nonzero integer stays nonzero in characteristic zero. Thus the coefficient matrix is invertible over K, forcing α=β=γ=0. That contradicts the four points being distinct. So at least one directional space interpolates. Combined with Section 2, the restricted minimum is six. ∎

## 4. Scope and remaining gap

The proof handles arbitrary four-point configurations, collinear or not, and every characteristic-zero field. Characteristic zero is used in transporting the integer certificate; no positive-characteristic claim is made. The certificate does not enumerate infinite families of points: it exhausts only the 6! possible slope assignments after the analytic reduction.

The unrestricted minimum is still unresolved. In particular 4≤m_4(K)≤5 for algebraically closed K, with no four-space construction and no unrestricted lower bound five. The obstruction in turn 3 and the sharp restricted result here leave general high-degree polynomial spaces unaddressed.

Completed substantive author turns: 4/5. Informal completion estimate toward the full original parameterized goal: 35%. One genuine author turn remains; final independent review must not turn into a sixth search.
