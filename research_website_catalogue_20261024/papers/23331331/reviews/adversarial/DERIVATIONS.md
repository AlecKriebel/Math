# Independent derivations and adversarial evidence

This proof and its exact computational evidence were frozen after the manuscript-first initial seal and before supplied scientific code/results or foreign scientific bodies. Root remains CLOSED at this freeze. The framework in the manuscript is known; these are independently expanded algebraic checks and explicit deductions, not a blind discovery claim.

## Geometric and group-theoretic premises

For the chosen oriented tangency branch, the Poncelet map is a circle homeomorphism. Central symmetry preserves the selected branch, giving TA=AT. Assuming the stated Poncelet porism, T has order exactly the least period N. Thus <T,A> is finite. A finite orientation-preserving circle group acts freely: a nonidentity finite-order map fixing a point would be an increasing finite-order interval map, impossible since a moved point has strictly monotone iterates. Its faithful action on one finite orbit preserves circular order and embeds the group in cyclic permutations. The unique involution is T^(N/2)=A, including primitive stars. This proof would fail for odd least period, an arbitrary repeated orbit without the even primitive premise, an orientation-reversing map, or a different tangency branch.

For consecutive eccentric angles u,w, write τ=(u+w)/2 and q=(w−u)/2. With the forward tangent chosen around a caustic containing the origin, 0<q<π/2. The chord covector is L=(cosτ/a,sinτ/b), with positive offset cosq. The support of the confocal caustic squared is (a²−λ)L_x²+(b²−λ)L_y². Tangency therefore says

cos²q=1−λ(cos²τ/a²+sin²τ/b²).

Using cos(u−w)=cos²u? More directly, 2sin²q=1−cos(u−w) and 2cos²τ=1+cos(u+w), 2sin²τ=1−cos(u+w), rearrangement gives

d=cos(u−w)+λ(a^−2−b^−2)cos(u+w).

This equals [1+λ(a^−2−b^−2)]cosu cosw+[1−λ(a^−2−b^−2)]sinu sinw. The outward normals are n=h(cosu/a,sinu/b). Thus

cosΔ=hk(cosu cosw/a²+sinu sinw/b²),
cos(ψ+φ)=hk(cosu cosw/a²−sinu sinw/b²).

The two coefficients match because (F+ed)/a²=1+λ(a^−2−b^−2) and (F−ed)/b²=1−λ(a^−2−b^−2). This proves the support relation d hk=FcosΔ+ed cos(ψ+φ) directly, without assuming a converse to a squared equation. The Gauss map is increasing and commutes with the half-turn; hence 0<Δ<π. Every summand hk sinΔ is positive, including star order, and S(0)>0.

Since λ<b² and a>b>0,

F+ed=a²−λ(a²/b²−1)>b²>0,
F−ed=b²+λ(1−b²/a²)>0.

Consequently F>0 and F²−e²d²>0. None of this forces d positive for stars. H,e,F,λ have units length², d and v are dimensionless, and the final centroid is homogeneous of length under uniform scaling.

## Exceptional rectangle and simple-orbit boundaries

For N=4, n₂=−n₀. The support equations for edges01 and12 have opposite right sides and equal left sides, since h₂=h₀. They force d=0. Conversely d=0 forces cosΔ=0 and every step isπ/2, giving least period four. Direct unrestricted Cartesian shoelace on (A,Y),(X,B),(−A,Y),(X,−B) gives S=2AB, T_x=4ABX, T_y=4ABY. This is an identity in four free variables checked coefficient by coefficient; C=M/3 for every point. It supplies the branch that cannot be divided by d.

For a simple winding-one even orbit with N≥6, half of its normals occupy a half-turn in circular order. Squaring yields at least three distinct cyclically ordered points on the unit circle. Their convex polygon has positive signed area and is traversed twice by Z. Thus S_Z>0. With S(0)=D S_Z/2>0, D>0 and d>0. This argument is deliberately not used for a star.

## Exact all-period algebra

For d≠0 let D=F/d. Support squares h²=H+e cos2ψ and k²=H+e cos2φ together with hk=D cosΔ+e cos(ψ+φ) give

(D²−e²)cos²Δ=H²−e²+e(H−D)(cos2ψ+cos2φ).

The independent Laurent polynomial check verifies that the difference of these two sides is exactly (DcosΔ+e cos(ψ+φ))²−h²k². Thus the reduction is an algebraic identity; no numerical orbit, division by cosΔ, genericity or reconstruction from the squared relation is used. For Z=n² this gives the affine doubled-normal chord relation with v=2e(H−D)/(D²−e²)=−4eλd/(F²−e²d²).

For unit U,V the local identity, after multiplication by2i, is

(V/U−U/V)(U+V)=(2+V/U+U/V)(V−U).

It holds in the free Laurent ring. Summing with the affine chord relation leaves the vector sum Σ(X_i+X_(i+1))(Z_(i+1)−Z_i). Its real part is Σ(X_(i+1)²−X_i²)=0. Its imaginary part is Σcross(Z_i,Z_(i+1))=2S_Z, since the residual coordinate products telescope. Therefore T_Z=2vS_Z without assuming simplicity or S_Z≠0.

Multiplying hk=D cosΔ+e cos(ψ+φ) by sinΔ, the second term is e(sin2φ−sin2ψ)/2 and telescopes. Hence S(0)=D S_Z/2; positivity of S(0) implies S_Z≠0 in the d≠0 branch.

Now Q=z/2+V, V=w−tZ, t=conj(z)/2 and w=hn. Antipodal indices give w↦−w and Z↦Z. The cross terms in signed area cancel, leaving

S(M)=S(0)+|t|²S_Z=(D/2+|z|²/4)S_Z.

To verify the complete first moment from its definition, use formal independent variables x,y,h,k,t,s, with s later specialized to conj(t), and write V₊=hx−tx², W₊=ky−ty², V₋=−hx−tx², W₋=−ky−ty². Conjugates are h/x−s/x² and k/y−s/y² with the corresponding signs. Expand the average of

(conj(V)W−Vconj(W))(V+W)=2i·cross(V,W)(V+W)

over the two antipodal edges in the free Laurent ring. Its exact result is c t+b s−t²s(W/Z−Z/W)(Z+W), with

c=k²x²−h²y²+2hk(x³/y−y³/x),
b=h²x²/y²−k²y²/x²+hk(x/y−y/x).

There are no additional constant or quadratic terms. Deliberately exchanging t and s fails the exact identity, so conjugation is an active falsification control rather than a convention silently inherited from the manuscript.

Substitute the three support expressions in a different free Laurent ring Q[x±1,y±1,H,D,e]. For r=Z/W−W/Z and s₂=Z²/W−W²/Z, independently reducing every coefficient gives

c=D s₂+(3e/2)r+(D+H)(Z−W)+e(Z²−W²),
b=(D/2+H)r+(e/2)s₂+(e/2)(Z−W)+e(W^−1−Z^−1).

All endpoint differences telescope. The exact local identity s₂+(W/Z−Z/W)(Z+W)=W−Z gives Σs₂=−2iT_Z=−4ivS_Z, while Σr=−4iS_Z. Together with the cubic term this proves

T(V)=−2S_Z[t(Dv+3e/2+v|t|²)+conj(t)(D/2+H+ev/2)].

This is a universal finite-support algebraic certificate, not a finite-period interpolation.

Translation for any ordered closed polygon follows directly: Σcross(c,p_(i+1)−p_i)=0, and Σcross(c,p_(i+1)−p_i)(p_i+p_(i+1))=cΣcross(p_i,p_(i+1)), with coordinate-square and coordinate-product differences telescoping. Hence T(p+c)=T(p)+6cS(p). The independent program additionally expands a completely arbitrary four-vertex chain with a free translation as an exact algebra control. No simple-polygon or nonzero-area premise is needed in the identity.

Dividing only when S(M)≠0, applying the translation by z/2, and replacing D=F/d yields precisely the manuscript's full centroid formula. Its denominator is G=2F+d|z|². Because S(0)>0 and F>0, the area formula proves that G=0 is exactly the signed-area-zero locus. For d≥0, G>0 everywhere; for d<0 it is the real circle |z|²=−2F/d. Signed reversal changes both moments by a sign, and repeated traversals multiply both, so their ratio is unchanged where defined.

## Independent unrestricted Cartesian star certificate

Use a²=221/96, b²=27625/20736, λ=125/96. The ratio b/a=5sqrt30/36 allows a separate exact construction over Q(sqrt30) after scaling all coordinates by a. For each printed normalized vertex (u,v), the tangent line in scaled coordinates is uX+(v/r)Y=1, r=b/a. Its Cartesian foot is obtained directly from the line-normal projection; no manuscript moment coefficient or complex formula enters this construction.

Expanding all eight feet by exact polynomial arithmetic and then restoring physical scale gives the complete polynomials

S=sqrt30[9503/10368−(2/13)(X²+Y²)],
T_x=sqrt30·X[1615/648−(64/169)(X²+Y²)],
T_y=sqrt30·Y[2057/576−(92/169)(X²+Y²)].

They equal all three printed polynomials identically for unrestricted X,Y. These are coefficient identities, not point samples. Direct independent checks establish all8 chord tangencies, all8 specular reflections,8 distinct vertices and winding3. The reflection check reflects the incoming segment vector in the tangent line and proves it is positively parallel to the outgoing vector with unchanged norm; therefore the corresponding unit velocities obey the specular law without requiring all segment lengths to belong to Q(sqrt30).

The first own test implementation unnecessarily assumed those segment lengths themselves belonged to that field and stopped with an explicit square-root guard. Its unchanged attempted source and failure record are preserved in private/own-diagnostics. Switching to the equivalent positive-parallel reflection criterion corrects the own checker, not the manuscript or supplied source.

The exact computed parameters are d=−120/221, F=2795/1728, v=7/13 and R₀²=123539/20736. The direct Cartesian polynomials satisfy the full published area factor and both centroid coordinates after multiplying through by3G; this also checks the global formula independently of its local moment derivation. A deliberate coordinate swap fails.

On R²=R₀², T_x/X=17sqrt30/72. At X=13sqrt731/144,Y=0 the first moment is exactly221sqrt21930/10368 and is nonzero, although area is zero. This verifies the stronger nonremovable diagnostic point. Undefinedness on the entire circle already follows from the signed-centroid definition and the area identity, without any need to show nonzero first moment everywhere.

## Own evidence status at this freeze

The own standard-library program completed with811 predicates including field-denominator and ring-dimension guards; those incidental guards are not presented as811 independent mathematical theorems. The decisive outputs are exact polynomial coefficient identities, all edge/vertex checks and explicit negative controls. The all-period proof is the universal algebra and cyclic telescoping above. No native numerical route, supplied expected output, foreign proof companion or scientific review opinion has yet been read. Actual primary definitions, exact source context and unchanged safe native reproduction remain to be assessed before final disposition. Follow-up:null.
