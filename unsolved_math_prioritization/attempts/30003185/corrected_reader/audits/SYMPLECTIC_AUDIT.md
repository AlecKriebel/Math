**Integrated reader status.** The marginal theorem is accepted. Later stages complete the originally excluded generation obligation. See the [integrated theorem](../README.md) and [dependency map](../DEPENDENCIES.md).

# Independent audit: the natural symplectic Bray marginal bound

Date: 13 October 2026. This is an independent mathematical audit of the symplectic marginal theorem.

## Verdict

**ACCEPTED, for the theorem's explicitly limited scope.** For an odd prime power q, natural G=Sp(n,q), even n≥49152, a strong involution t, and uniform g∈G, each separately fixed t-eigenspace has a strong restriction of inv(t t^g) with probability greater than 1/(40000 ln n). The proof actually establishes the slightly stronger lower bound 1/(36864 ln n). No substantive mathematical correction to the candidate was required.

This does not certify a simultaneous-event bound, an orthogonal-family extension, a projective or quotient sampling statement, the remaining centralizer-generation argument, total algorithmic complexity, or a literature novelty claim.

The reviewed proof identity is recorded in the [artifact manifest](../metadata/AUTHORED_ARTIFACTS.json). The [stage certificate](../certificates/SYMPLECTIC_STAGE.json) records its finite controls. The universal acceptance rests on the proofs below, not on those finite tests.

## 1. Uniform sampling and the graph-chart measure

Set V=A⊥B with dimensions 2a≤2b and t=−I on A, +I on B. Replacing t by its negative is legitimate: −I is central in Sp(V), the product t t^g is unchanged, and the two marginal targets are merely relabeled. Strongness gives a≤b≤2a. A centralizing isometry must preserve the two distinct eigenspaces, even when a=b, so the exact centralizer is Sp(A)×Sp(B); there is no extra factor of two.

A conjugate of t is determined by its nondegenerate negative 2a-space W. Uniform g gives uniform W among exactly |Sp(2(a+b),q)|/(|Sp(2a,q)| |Sp(2b,q)|) possibilities. This denominator includes all conjugates, including those outside the graph chart.

For W=graph(F), K=F*F is self-adjoint. Invertible K makes F injective and F(A) nondegenerate. The induced form on W is ⟨u,(I+K)v⟩, so I+K invertible is exactly its nondegeneracy condition. The projection to A uniquely recovers F from W, preventing graph-map overcount.

For a prescribed invertible self-adjoint K, F*F=K says precisely that F is an isometric embedding from the nondegenerate alternating form ⟨u,Kv⟩ into B. Extending a symplectic basis proves transitivity of Sp(B) on such embeddings. Its pointwise stabilizer is Sp(2(b−a),q), including the case b=a with the trivial group in dimension zero.

A semisimple self-adjoint K with characteristic polynomial f² and squarefree minimal polynomial f has, for a degree-j factor of f, a two-dimensional F_(q^j)-space. Balancedness of the form under F_q[K] gives a unique alternating extension-field form whose trace is the original form. Nondegeneracy follows from nondegeneracy of the trace pairing. All these forms are isometric. Operators commuting with K are extension-field linear, so the exact symplectic centralizer is ∏_(p|f)Sp(2,q^deg(p)). Field automorphisms are not extra centralizer elements. This validates both uniqueness of the class and its orbit size.

Multiplying the two fiber counts and dividing by the complete conjugacy-class size gives

P_f = |Sp(2a,q)|² |Sp(2b,q)|² /
      (|Sp(2(a+b),q)| |Sp(2(b−a),q)| ∏_(p|f)|Sp(2,q^deg(p))|).

The exponent of q after cancellation is −a, not −2a or zero. Writing ψ_r=∏_(i=1)^r(1−q^(−2i)), each ψ_r≥1−∑_(i≥1)q^(−2i)≥7/8. Denominators ψ_(a+b), ψ_(b−a), and the factor corrections are all at most one before reciprocation. Hence P_f≥(7/8)^4 q^(−a)>q^(−a)/2. This is unconditional under uniform g and contains no assumption of uniform K.

## 2. Spectral and involution extraction checks

I independently recomputed the projection to graph(F). With H=(I+K)^−1 and coordinates (u,Fv), the matrix of t s_W is

[(I−K)H, 2KH; −2H, (I−K)H].

Thus λ+λ^−1=2(1−κ)/(1+κ) and κ=−((λ−1)/(λ+1))². Its quadratic discriminant is −16κ/(1+κ)². Because κ is neither zero nor −1, the two roots are distinct, nonzero and different from ±1. Each degree-j factor contributes dimension 4j to V, with dimension 2j in each of A and F(A). The two reciprocal roots, and all their Frobenius conjugates, have the same multiplicative order. Repeated natural-representation eigenvalues therefore introduce no unipotent part here.

The untouched complement F(A)⊥∩B has dimension 2(b−a) and is fixed by both involutions. If one factor has strictly largest 2-part greater than one, raising y to half its order gives −I on exactly that factor's full block and +I on every other block and the fixed complement. Consequently the negative dimensions on A and B are both exactly 2k. The complement is correctly included in B's positive dimension.

## 3. Distinguished factors and two-adic separation

For d=2^h with h≥2 and k an odd multiple of d, (q^k−1)_2=2^(v_2(q²−1)+h−1)≥8. Exactly half the nonzero elements of F_(q^k) have this maximal two-part. The union of all proper subfields contains fewer than (3/2)q^(k/2) elements. The candidate's lower bound is uniform: setting X=q^(k/2)≥9, the difference between its remaining-element count and q^k/4 is at least X²/4−3X/2−1/2, positive already at X=9 and increasing thereafter.

For a full-degree λ in this set, κ is rational in λ while λ is quadratic over F_q(κ). Therefore κ has degree k or k/2, with no other possibility. In the latter case λ^(q^(k/2))=λ^−1, so its order divides q^(k/2)+1. Since k/2 is even, the latter integer has two-part exactly 2, a contradiction. Hence κ has full degree k.

The Cayley map identifies exactly λ and λ^−1, both still in the selected set. It is Frobenius equivariant, and the κ-orbits have length k. The resulting lower bound q^k/(8k) counts distinct irreducible polynomials, not roots or labeled factors. Neither forbidden root 0 or −1 can appear.

For another degree j, the relevant roots belong either to F_(q^j)^× or to its quadratic norm-one group. The maximal possible two-part is 2^(e−1) for j odd and 2^(e+v_2(j)−1) for j even, where e=v_2(q²−1). If d does not divide j, it is strictly below the distinguished two-part. Both split and nonsplit possibilities have therefore been covered.

## 4. The remainder estimate, including q=3

For q≥5 and degree r≥2, the nonsquarefree count is q^(r−1), and excluding the two roots costs at most another 2q^(r−1). This leaves at least 2q^r/5. Degrees zero and one satisfy the stated q^r/3 lower bound directly.

The q=3 normalized squarefree generating function with the two roots removed is

(1−u²/3)/((1−u)(1+u/3)²).

Its coefficients are exactly c_r=3/8+(−1)^r(10−8r)/(16·3^r). The values at r=0,1,2 are 1,1/3,1/3. For odd r≥3 the correction is positive; for even r≥2 its magnitude decreases with r, starting at 1/24. This proves c_r≥1/3 for every degree, avoiding an invalid q=3 union-bound estimate.

Counting all monic polynomials divisible by an irreducible of degree jd gives at most q^r/(jd) for that degree. Summation and a union bound cost at most q^r H_(floor(r/d))/d≤q^r(1+ln a)/d when 1≤r≤a. With d≥12(1+ln a), this is at most q^r/12. Subtracting from q^r/3 gives q^r/4. Degrees r=0 and r<d are handled directly. Repeated factors cause no issue, because this exclusion bound is applied to all monic polynomials before intersecting with the squarefree set.

## 5. Unequal factors, endpoints, and the explicit threshold

The A interval is [a/3,2a/3]. The B interval is [b/3,min(2b/3,5a/6)]. If b≤5a/4, the latter width is b/3; otherwise it is 5a/6−b/3≥a/6 because b≤2a. Thus both intervals have width at least a/6 and upper endpoint at most 5a/6. Their definitions impose exactly the balance conditions on the selected factor, including fractional endpoints.

The arithmetic progression d times odd has spacing 2d, so the number of its points in a closed real interval of width w is at least w/(2d)−1. There is no rounding-to-an-integer assumption. With a≥24d this yields at least a/(24d) admissible k.

The theorem's n≥49152 gives a≥n/6≥8192. The function a/(1+ln a) is increasing for a>1, and at a=8192 it exceeds 576. Since d is the least power of two at least 12(1+ln a), d<24(1+ln a); hence 24d<576(1+ln a)≤a. This validates the threshold for all larger a, not just the tested endpoint.

Every constructed polynomial f=f_*f_0 has exactly one irreducible factor with degree divisible by d. Thus the distinguished factor, its degree k, and the remainder can all be recovered uniquely from f. This prevents both within-degree and cross-degree overcount. Squarefreeness of the product follows since f_* cannot divide the remainder.

There are at least q^a/(32k) polynomials per k. Using k≤a and at least a/(24d) eligible degrees gives at least q^a/(768d) distinct polynomials. Their disjoint graph masses yield a probability greater than 1/(1536d), then greater than 1/[36864(1+ln a)]. Finally n≥4a>ea implies ln n>1+ln a. The claimed constant 40000 is therefore conservative.

## 6. Auxiliary normalization checks

The candidate's warning against the linear regular-semisimple count is valid. For arbitrary symplectic involutions t,s, put y=ts. Over an algebraic closure, t exchanges generalized λ and λ^−1 spaces. For λ≠±1, the form (u,v)↦⟨u,tv⟩ on the generalized λ-space is nondegenerate alternating, so its dimension is even. The ±1 primary spaces are themselves nondegenerate symplectic spaces. Therefore every root of the characteristic polynomial of y has even algebraic multiplicity. This statement does not require y to be semisimple.

A further useful normalization is proved in [the equal-dimension identity](../proofs/EQUAL_NEGATIVE_DIMENSIONS.md): if t and s are conjugate involutions in odd characteristic, the negative space of inv(ts) has equal intersection dimensions with the two t-eigenspaces. The proof covers the global order-two-part-equals-two case and arbitrary unipotent parts. At t-eigenspace dimensions 2a and 4a, simultaneous strongness forces their common negative dimension to be 4a/3; hence it is impossible when 3 does not divide a. This reinforces the necessity of the theorem's separate marginal formulation and is not used to prove its probability bound.

## 7. Independent finite controls

The successful exact finite checks are:

- All monic polynomials over F_3 of degrees zero through seven: the squarefree/two-root-exclusion counts are 1,1,3,11,29,93,271,823, agreeing with the rational coefficient formula.
- All 130 two-dimensional subspaces of F_3^4 in unique RREF form: exactly 90 are nondegenerate; 57 lie in the nondegenerate graph chart; 24 have K=I. The latter mass is 24/90=4/15, agreeing with the exact graph-class formula. Direct projections to the subspaces reproduce the displayed product matrix, which squares to −I on these 24 cases. Across all 90 conjugates, the product-order counts are 1,32,24,32,1 for orders 1,3,4,6,2 respectively. The auxiliary equal-negative-dimensions identity is verified for all 90, including all 32 nonsemisimple order-six cases.
- All 729 self-adjoint four-dimensional operators over F_3: each of the three irreducible quadratic minimal-polynomial classes has 72 elements, agreeing with |Sp(4,3)|/|Sp(2,9)|. The minimal polynomial, not just characteristic polynomial, was checked.
- Direct finite-field Cayley enumeration at the smallest permitted k=4: q=3 gives five distinguished irreducibles, exceeding 81/32; q=5 gives 39, exceeding 625/32. Every retained κ has full degree and exactly two preimages.
- Every integer b from 8192 through 16384, in both target intervals, at a=8192: d=128, minimum six admissible degrees, compared with the proof's lower bound 8/3. These include the extreme b=2a case.

No low-dimensional theorem is inferred from these controls. In particular, a two-dimensional symplectic factor cannot itself have a strong involution under the stated balance convention; the dimension threshold is essential to the scope.
