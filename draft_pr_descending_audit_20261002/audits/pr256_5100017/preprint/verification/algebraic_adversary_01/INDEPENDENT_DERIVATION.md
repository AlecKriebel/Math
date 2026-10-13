# Independent algebraic audit derivation

Target: PR256 / problem 5100017 / AMR-050-0017 / k307, authenticated submitted head `9445a90b57f76493bd901edc544b09dec393e20f` as assigned by the parent. This audit concerns the submitted domain-qualified mathematical theorem, not priority or publication.

The independent mechanism was recorded in `INITIAL_MECHANISM.md` before opening the proof. I subsequently read the complete submitted `PROOF.md` and `verify.py`. I have not read the submitted prior independent-review reports, their conclusions, or their code. The present verifier neither executes nor imports the submitted verifier.

## Scope and exact claim

The outer ellipse has squared semiaxes A=a²>B=b²>0; its caustic is the confocal ellipse with squared semiaxes A−λ, B−λ and 0<λ<B. The selected counterclockwise Poncelet map has least even period N≥4. M is any fixed real planar point. The projection polygon is ordered in trajectory order, and its area and centroid use signed shoelace area and signed first moments. The theorem says its centroid, where defined, has formula (2) and is phase independent; its precise zero-area locus is formula (1). Stars and self intersections are included. Odd least periods artificially traversed twice, circles, hyperbolic caustics, and degenerate caustics are outside this audit's claimed theorem.

## Antipodal hypothesis and signs

The half-turn R commutes with T because central inversion preserves both confocal ellipses and the oriented tangent choice. Since T^N=id, R²=id, and TR=RT, the group consists of at most 2N maps T^jR^ε. Each is an orientation-preserving circle homeomorphism.

A finite-order orientation-preserving circle homeomorphism fixing a point is the identity: cut the circle at that point; if an interior point is moved to the right or left, its iterates move strictly in that direction and cannot return. Hence the finite group acts faithfully on any of its finite orbits. Its action preserves the orbit's circular order, so embeds in the cyclic group of circular-order-preserving permutations of that orbit. It is cyclic and has a unique involution. Since N is the order of T and is even, T^(N/2) is that involution. R is a nonidentity involution, whence R=T^(N/2). This establishes equation (3), with no simplicity assumption.

Each oriented billiard chord tangent to the elliptic caustic has the origin strictly on its selected side. The next endpoint is strictly less than a half-turn ahead of the initial endpoint. The Gauss map of the outer ellipse is increasing and commutes with antipodes, so the outward-normal lift also advances by Δ_i in (0,π). Thus h_i h_{i+1} sin Δ_i>0 for every edge. Consequently S(0)>0, even for a star. This sign argument does not identify trajectory order with the vertices' circular order.

## Adjacent-normal identity

For eccentric-angle endpoints u,w set t=(u+w)/2, q=(w−u)/2, with 0<q<π/2. The chord is (cos t/a)x+(sin t/b)y=cos q. Its caustic tangency gives

    sin² q = λ(cos² t/A + sin² t/B).

Since cos u cos w=(cos 2t+cos 2q)/2 and sin u sin w=(cos 2q−cos 2t)/2, this is equivalently

    d = (1+λ/A−λ/B)cos u cos w
        +(1−λ/A+λ/B)sin u sin w,
    d=1−λ/A−λ/B.

The outer ellipse has support h²=A cos²ψ+B sin²ψ=H+e cos 2ψ, and n=h(cos u/a,sin u/b). Multiplying the preceding relation by h_i h_j yields coefficient A(1+λ/A−λ/B) on n_ix n_jx and coefficient B(1−λ/A+λ/B) on n_iy n_jy. These are respectively F+ed and F−ed, with H=(A+B)/2, e=(A−B)/2, F=Hd+2λ. This proves (5).

The factors are strictly positive:

    F+ed = A−λ(A/B−1) > B > 0,
    F−ed = B+λ(1−B/A) > 0.

Therefore F>0 and F²−e²d²>0 throughout the stated open domain. This also controls all divisions below. For d≠0 define D=F/d; then D²−e²>0 and h_i h_j=D cos Δ+e cos(ψ_i+ψ_j).

## Support square and cyclic moment

Squaring the preceding relation and using

    cos 2ψ_i cos 2ψ_j = cos²(ψ_i+ψ_j)+cos²Δ−1,
    cos 2ψ_i+cos 2ψ_j = 2 cos(ψ_i+ψ_j)cosΔ

gives

    (D²−e²)cos²Δ = H²−e²+e(H−D)(cos 2ψ_i+cos 2ψ_j).

For Z_i=exp(2iψ_i), this is equation (7), with u=2(H²−e²)/(D²−e²)−1 and v=2e(H−D)/(D²−e²). Multiplying numerator and denominator by d² and using F=Hd+2λ gives v=−4eλd/(F²−e²d²).

For any unit complex U,V, direct Laurent multiplication gives

    [U,V](U+V) = −i(1+Re(conj(U)V))(V−U).

This identity is also valid at coincident or antipodal U,V; no division by an angle occurs. Under Re(conj(U)V)=u+v(X_U+X_V), the constant part telescopes. The real part of sum (X_U+X_V)(V−U) is a sum of endpoint differences X_V²−X_U². Its imaginary part equals sum [U,V], because

    (X_U+X_V)(Y_V−Y_U)
      = [U,V]+X_VY_V−X_UY_U.

Thus T_Z=sum [Z_i,Z_j](Z_i+Z_j)=v sum [Z_i,Z_j]=2vS_Z. This proves (8) without an area or simplicity assumption.

The support product gives the exact origin-area edge coboundary

    h_i h_j sinΔ = (D/2)sin 2Δ
       +(e/2)(sin 2ψ_j−sin 2ψ_i).

After summation, S(0)=D S_Z/2, establishing (9). Since S(0)>0, S_Z≠0 whenever d≠0. No prior invariant of the doubled-normal polygon is assumed.

## Area and full cubic moment

Let m encode M, t=conj(m)/2, w_i=h_i n_i, Z_i=n_i². Orthogonal projection has the exact form Q_i=m/2+w_i−tZ_i. Antipodes send w_i to −w_i and fix Z_i. Put V_i=w_i−tZ_i.

For one edge let x,y encode its unit normals, h,k its support numbers, and use formal conjugation x→1/x, y→1/y, t→conj(t). Half the sum of the edge and its antipodal edge's area contribution is

    hk[x,y]+|t|²[x²,y²].

Summing over all N edges counts each actual edge once. Hence S(M)=S(0)+|t|²S_Z=S_Z(D/2+|m|²/4). With S(0)=DS_Z/2 this is exactly (1).

Half the paired edge first-moment numerator has only monomials t, conj(t), and t²conj(t). The independently extracted coefficients, after multiplication by 2i, are

    c = k²x²−h²y²+2hk(x³/y−y³/x),
    b = h²x²/y²−k²y²/x²+hk(x/y−y/x),

and its cubic term is −t²conj(t)[x²,y²](x²+y²). There are no remaining pure-support or quadratic terms.

Substitute h²=H+e(x²+x^−2)/2, k²=H+e(y²+y^−2)/2, and hk=D(y/x+x/y)/2+e(xy+(xy)^−1)/2. With Z=x², W=y², R=Z/W−W/Z, U=Z²/W−W²/Z, the exact edge identities are

    c = DU+(3e/2)R+(D+H)(Z−W)+e(Z²−W²),
    b = (D/2+H)R+(e/2)U+(e/2)(Z−W)+e(W^−1−Z^−1).

The displayed endpoint terms telescope. Further,

    sum R = −4iS_Z,
    U+2i[Z,W](Z+W)=W−Z,
    sum U = −2iT_Z = −4ivS_Z.

Consequently the complete moment is

    T_V = −2S_Z{t(Dv+3e/2+v|t|²)
                       +conj(t)(D/2+H+ev/2)},

which is (12), with its cubic contribution included. This independently verifies every coefficient and factor of two.

For arbitrary cyclic planar vertices, translating by a fixed c leaves signed area unchanged and changes the unnormalized moment by 6cS. To see the factor six, the new cross product is [V_i,V_j]+[c,V_j−V_i]. The sum of [c,V_j−V_i](V_i+V_j) is c sum [V_i,V_j], after the coordinate-square and coordinate-product endpoint terms telescope. Adding the two explicit c terms gives 3c sum cross=6cS. This identity applies to signed self-intersecting polygons as well.

Dividing T_V by 6S(M), translating by m/2, and multiplying numerator and denominator by d gives formula (2). Only the final quotient needs S(M)≠0. Every earlier identity is polynomial or a telescope on the stated geometric constraints.

## Four-period and simple-family cases

For d=0, (5) gives cosΔ=0. Since 0<Δ<π, each normal advances π/2. The primitive period is four, and the four outer tangent lines form a rectangle. For its sides x=±A_*, y=±B_*, the feet are (A_*,M_y),(M_x,B_*),(−A_*,M_y),(M_x,−B_*). Raw signed shoelace gives area 2A_*B_* and moment (4A_*B_*M_x,4A_*B_*M_y), hence centroid M/3 for all M. In formula (2), d=v=0 and F>0 give the same result.

Conversely, for a primitive four-period orbit, antipodality makes the doubled-normal polygon Z_0,Z_1,Z_0,Z_1, of zero signed area. If d≠0, (9) would give S(0)=0, contradicting its positivity. Hence N=4 implies d=0. The submitted proof directly states the other implication and then treats the four-period case as completed; this extra sentence makes that logical dependency explicit. It is a readily checked expository omission, not an unsupported result.

After preserving this independent observation, I also checked the newly supplied `candidate_repair_01/PROOF.md` paragraph directly. Its equation-(5) sign-reversal proof is correct: n_2=−n_0, h_2=h_0 make the first and second edge right sides opposite and their left sides equal; adding gives 2d h_0h_1=0. The positivity of h_0,h_1 proves d=0 without referring forward to (9). The candidate contains only that added paragraph and passes this direct check.

For a winding-one even family with N≥6, the first N/2 normals occupy one half-turn in circular order. Their squares are at least three distinct circularly ordered unit-circle points. The full Z-polygon traverses their convex polygon twice, so S_Z>0. Since S(0)>0 and S(0)=D S_Z/2, D>0, and since F>0, d>0. Along with N=4 ⇒ d=0, every simple even winding-one family has d≥0.

## Exact zero-area locus and exact 8/3 test

Because S(0)>0 and F>0, equation (1) implies S(M)=0 exactly when G=2F+d|M|²=0. For d≥0 it never vanishes. For d<0 its entire zero locus is the phase-independent circle |M|²=−2F/d. This is a statement about signed area; its centroid quotient is undefined there regardless of whether a first moment also vanishes.

The prescribed exact noncircular 8/3 orbit was checked from Cartesian coordinates. Each of the eight distinct points lies on the outer ellipse; each edge satisfies the inner-ellipse support discriminant equation; each edge has positive central cross product; and the normalized incoming vector reflects exactly into the normalized outgoing vector. Eight distinct points establish least period eight for this explicit cyclic orbit. Counting oriented crossings gives winding three (also apparent from the prescribed eccentric-angle increments, all less than π, whose sum is 6π).

Its exact constants are d=−120/221, F=2795/1728, v=7/13, and radius squared 123539/20736. Direct Cartesian perpendicular projections with unrestricted symbolic M=(x,y) give

    S(M) = −sqrt(30)(20736x²+20736y²−123539)/134784,
    T_x = −sqrt(30)x(41472x²+41472y²−272935)/109512,
    T_y = −sqrt(30)y(52992x²+52992y²−347633)/97344.

These raw polynomial results agree exactly with (1) and 6S times (2) for every M. At M=(13sqrt(731)/144,0), the area is exactly zero, while T_x is nonzero. Thus the undefined locus is real and does not result from a removable zero in both numerator and denominator at that diagnostic point.

## Units, signs, limits, and exact gap

H,e,F,λ,D have units length², d and v are dimensionless, S_Z is dimensionless, S(0) has units length², and T_V has units length³. Formula (2) has units length. Reversing order changes every area and moment sign and cancels in the quotient. Positive rescaling of geometry scales area by c², moment by c³, and centroid by c. The expression is continuous at d=0 for every fixed M and becomes M/3; no division by d survives in the final formula.

All domain-qualified algebraic and topological claims have now been checked. No mathematical gap remains in the submitted theorem. Its conclusion applies only where the signed-area quotient exists; an unqualified all-M claim for arbitrary stars would be false, with the exact control above providing a counterexample to definedness. Numeric robustness tests remain secondary corroboration of this all-period derivation, never a replacement for it.
