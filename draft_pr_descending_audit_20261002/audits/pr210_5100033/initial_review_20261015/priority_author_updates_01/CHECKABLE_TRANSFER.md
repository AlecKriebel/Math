# Checkable transfer from original focal inversion to outer focal pedals

Derived during this priority audit, 2026-10-15 UTC. This document distinguishes an earlier printed theorem from the additional geometric application supplied here. It is not evidence that an earlier source printed this application. It uses the mathematical/source gate only as context; the construction and transfer are spelled out so root can verify them independently.

## 1. Scope and notation

Fix a>b>0, c²=a²−b², a nondegenerate confocal elliptical caustic with semiaxes α>β>0, and a primitive billiard family of least period n≥3, coprime winding τ. Use modulus k=c/α, K=K(k), K′=K(sqrt(1−k²)), v∈(0,K), h=2v=4Kτ/n, and Stachel's coordinate relations a=α dn(v)/cn(v), b=β/cn(v). All dot products in the complex continuation are bilinear. Put P(u)=(-a sn u,b cn u), F±=(±c,0), L=4K/n and Z=K+iK′.

Let D±(u) be the signed area of the unit inversions of the **original vertices** about F±, in trajectory order. Let B±(u) be the signed area of orthogonal feet of F± onto the ordered **boundary tangent lines**, i.e. sides of the actual outer tangent-intersection polygon. These are different point constructions and different area units. The inversion normalization must be fixed: inversion radius ρ multiplies D by ρ⁴ and changes the proportionality below accordingly.

The earlier source is Alper Ferudun, *Products of the Two Focal Inversion Areas in Elliptic Billiards*, 2 October 2026, version 1.0, DOI 10.5281/zenodo.23096994; canonical six-page PDF SHA256 c7fbcc7e5a7b7746ad102cb7cf0f5e9eb6aa149009d88c3654fdbcc3484126c0. The full proof was read. Theorem 1 is D+D−=positive constant for every odd real billiard family, with coprime stars and odd repeats. Lemmas 2–3 (printed pp. 3–4), §4 (p. 4), provide the pole/order/character facts used below, rather than merely announcing the final product.

## 2. Exact pointwise relation (new comparison calculation)

For s=sn u, t=cn u, direct perpendicular projection to the tangent n(u)·X=1 with n(u)=(-s/a,t/b) gives

q+(u)=(a(c−as)/(a−cs), abt/(a−cs)).

The translated opposite-focus inverse vector is

R−(u)=I_(F−)(P(u))−F−=((c−as),bt)/(a−cs)²,

because (P−F−)·(P−F−)=(a−cs)². Hence

q+(u)=a(a−cs)R−(u).

The factor depends on u, so this is **not** an affine map with a constant area multiplier. It does not itself give B+=constant·D−. The sign of the focus is essential. The exact finite control gives B+/D−=2016/5 in both tested triangular phases, while the same-focus ratio B+/D+ differs between those phases.

## 3. Outer-foot pole lemma (additional geometry, fully checkable)

On C/(4K Z+4iK′ Z), the common poles of sn and cn are removable for q+. The only remaining poles solve sn u=a/c. The standard shift identity sn(Z+z)=dn z/(k cn z), together with a/c=dn v/(k cn v), puts them at Z−v, Z+v and their translates by 2iK′. They are simple: cn and dn there are nonzero for 0<v<K. The solutions exhaust the divisor since sn has four poles on this chosen torus.

At Z±v, sn=a/c and cn=−ib/c. The two numerator vectors of q+ agree, and the derivatives of a−c sn have opposite signs. Thus their nonzero residues are opposite and collinear. A possible double-pole determinant for the adjacent singular pair has leading coefficient det(R,−R)=0. Every other incident edge has at most one simple singular endpoint. Therefore the cyclic signed area B+ has at most simple poles. Primitivity leaves exactly two adjacent singular indices at each phase; 4K and h periods reduce the real period to L. On X=C/(L Z+4iK′ Z), all possible poles of B+ are just

r=Z−v,  r+2iK′.

The imaginary shift sn(u+2iK′)=sn u and cn(u+2iK′)=−cn u reflects the foot vectors. Consequently B+(u+2iK′)=−B+(u). This proof of the foot-map pole bound is the geometric work absent from the printed inverse theorem. It is also the specific work in the submitted proof §§2–4. No complementary-zero conclusion has been assumed here.

## 4. What the earlier inverse proof actually supplies

Ferudun's Lemma 2 gives exactly the same possible pole locations for R−, initially of order two. Lemma 3 reduces its cyclic area D− to at most simple poles. Its proof first bounds the area order by two, using the collinearity of the two negative Laurent coefficients of isotropic inverse vectors, then removes the even Laurent term by cyclic reversal about r. Equation (7) is D−(u+2iK′)=−D−(u). Cyclic relabeling and gcd(τ,n)=1 give real period L in §4. These are proved for the primitive elliptic-caustic family before the odd-parity step, so the present pole-space comparison needs no unstated convex-orbit restriction.

For real forward orbits, both original foci lie strictly inside the caustic and every directed chord leaves the caustic on its left, including the star branch. Each translated inverse edge determinant is positive, hence D−>0. In particular D− is not the zero function. The earlier proof's positivity argument is needed here to justify a nonzero spanning function; its all-odd product theorem by itself would also suffice to show that.

## 5. One-dimensional uniqueness, with no quotient through zeros

Consider meromorphic functions on X with at most simple poles at r and r+2iK′ and with antiperiod 2iK′. This vector space has dimension at most one. Indeed residues at the two points are opposite by the antiperiod. If a function has no residue at r, it has no poles, so compactness makes it constant; the antiperiod forces that constant to be zero. Given a nonzero member g, its residue at r is therefore nonzero. For any member f, choose γ to match that residue in f−γg. The other residue matches automatically. The difference has no poles and is identically zero by the same argument.

Taking g=D− and f=B+ gives a phase-independent finite scalar γ with

B+(u)=γD−(u).

No division by an area at a zero phase occurs. If B+ vanishes identically then γ=0 is allowed. Focus exchange satisfies q−(u)=−q+(u+2K), while the translated inverse vectors satisfy R+(u)=−R−(u+2K). Global negation does not change signed area. Thus

B−(u)=B+(u+2K)=γD−(u+2K)=γD+(u).

For odd n, the earlier theorem now implies

B+(u)B−(u)=γ²D+(u)D−(u)=constant.

For a fixed r-fold repetition, all four signed area traces are multiplied by r and each product by r². Reversal changes each area's sign and preserves both products. Circular boundaries can be treated directly: q=P, R=P/a², hence B=a⁴D and all regular star families rotate rigidly. These are deductions here, not extra words attributed to the source statement.

## 6. Priority interpretation and precise remaining distinction

This establishes an exact mathematical linkage, not a label-based exclusion: the recent original-inversion theorem plus the explicit outer-foot pole lemma yields the target. The geometric lemma and its application to this different map are not printed in the six-page 0062 paper. No earlier general transform theorem asserting B+=γD− was verified in the inspected corpus. Therefore it would overstate the evidence to call 0062 a literal prior proof of k605,a/k606, and it would also understate the evidence to say the inverse paper is irrelevant merely because it concerns different vertices.

The two papers share the same Jacobi lattice, paired adjacent singular phases, a simple-pole reduction, focus exchange as a half-period, and complementary-pole cancellation. The abstract method is established prior mathematics. Any defensible contribution statement must be limited to the explicitly checked outer-tangent-foot application and must discuss this current related work. The immutable submitted log dates its candidate completion before 06:00 UTC on 1 October 2026; 0062's public record is 2 October 2026. Those facts do not establish public priority or independence: a dated internal log is not independently certified dissemination, and a later analogous paper is not automatically the origin of a prior draft. No first-proof or world-open conclusion is justified.
