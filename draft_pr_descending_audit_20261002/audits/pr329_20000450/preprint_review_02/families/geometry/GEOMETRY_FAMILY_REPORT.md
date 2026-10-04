# Independent adversarial geometry-family review

Status: complete for assigned geometry IDs C001-C003 and C011-C030; HOLD for parent closure. This report does not approve publication, certify the division-field theorem, or substitute for the other review families. No mathematical counterexample or remaining geometry gap was found within the assigned IDs. The claims are closed by the explicit proofs below, assisted by independently reconstructed exact symbolic certificates. A printed PASS in a historical report was never used as evidence.

## Independence, candidate binding, and actual attempts

The original AIM source was fetched independently by native curl, HTTP 200, at 2026-10-04T12:39:58.910521+00:00 to 12:39:59.595194+00:00. Its SHA-256 is `8b64d2f6b91f791c35afae10b2ef79c15a927a94c2142a56386f80c8b8a596e6`. The source frontmatter and physical page 51 were extracted and visually read, including all four Question 17 remarks. The source-only reflection/double-cover and dihedral mechanism baseline was frozen at 2026-10-04T12:41:38.633575+00:00, hash `cb8378cf08fe7f1efcab9cc7b023b3541795aa0f43bb4e675812a105b373d9e2`. No candidate or assessment was read before that freeze.

After the freeze, the candidate source, PDF, metadata, and stable ledger were read. Candidate binding is in `CANDIDATE_BINDING.json`: manuscript source hash `3338be58c5c6250a826f2a2af772db5a3838dad1d45c6c4a847c62cc00b4f9df`, PDF hash `0325be9bc4b754ad1d94baadf2f1b88af587e9443b9d242a2d7af7b2dda79420`, metadata hash `b4d99b620320f9a0a46eac60f9e61308cbc859364fadd632fd9976e9e942b863`. Candidate PDF pages 2-4 were rendered and visually checked; the mathematical geometry formulas match the source. The full PDF text is preserved.

Fresh checker `independent_geometry_v01.py` ran from 12:45:38.350315Z to 12:45:48.569830Z with exit 0 and empty stderr; body hash `0eb0125bee0c138702c08aa666ecd4ff020ac2a3395cee310d10faa3e6c76edc`. Fresh checker `independent_boundary_v01.py` ran from 12:48:24.015687Z to 12:48:24.941302Z with exit 0 and empty stderr; body hash `52ea6600e7c615d88a32e957d71d1f79010349082632b41e099bfccd093e4064`. Both use the existing SymPy 1.14.0 environment and import no candidate supplement. Their symbolic polynomial/rational identities are over Q(sqrt(5)); these are universal exact identities, not sampled values. No program failed in this family, and no installation was performed. Native receipts include the actual argv, start/end UTC, full stdout/stderr, exit code, and body hashes. Failed attempts in other namespaces are not attributed to this family.

The additional direct generalized-Weierstrass discriminant check `independent_tate_discriminant_v01.py` ran from 2026-10-04T12:56:02.200608+00:00 to 12:56:02.501529+00:00, exit 0, empty stderr; body hash `f5ae92c3a82003f1a28dd7f294f38e094f4917c7a5606d56258192a091057f70`. It checks the discriminant formula as a polynomial identity in independent beta, before using the pencil pullback.

## 1. Side product, coordinate field, and projective pencil

Set r=sqrt(5), phi=(1+r)/2, c=phi^5, zeta=exp(2 pi i/5), and complex coordinates Z=X+iY, W=X-iY. For j=0,...,4 let

`L_j = Z + zeta^(2j+1) W - (1+zeta) zeta^j T`.

At the two vertices Z=zeta^j, W=zeta^(-j), T=1 and Z=zeta^(j+1), W=zeta^(-j-1), T=1, L_j vanishes. The independent checker verifies these ten evaluations in Q[zeta]/Phi_5, and expands the product there to

`Z^5 + W^5 + 5 phi Z^2 W^2 T - 5 phi^3 ZW T^3 + phi^5 T^5`.

The relation phi=1+zeta+zeta^(-1) follows with the specified root and satisfies phi^2=phi+1. Substituting Z=X+iY and W=X-iY gives exactly the candidate P, so all coefficients descend to K. This also makes the scale explicit. With theta_j=(2j+1)pi/5,

`L_j = 2 exp(i theta_j) [cos(theta_j) X + sin(theta_j) Y - cos(pi/5) T]`.

The product of the five phase factors is -1, hence P is -32 times this ordinary real side-line product. This is a fixed nonzero scaling, as required; changing side-line scalings changes lambda. The affine circle is X^2+Y^2-1=0. Its squared term has degree four, so degree-five homogenization is necessarily `P+lambda T(X^2+Y^2-T^2)^2`. The independent quartic coefficient extraction matches A, B, C exactly. Thus C001, C002, C011 hold.

## 2. First quadratic extension and rational conic

Fix any allowed lambda in a characteristic-zero extension and pass to an algebraic closure k of that coefficient field. All degree and genus assertions below are over k and therefore prove geometric claims. Let `G=A Y^4+B Y^2+C`, h=4X^2+2X-1, D=20X^2-aX+b. Direct exact identities give

`B^2-4AC=h^2 D`, and `disc_X(D)=a^2-80b=64 lambda(lambda+5r)`.

For lambda unequal to 0 and -5r, D has two distinct finite roots. In k(X), their valuations are odd, so D is not a square. The quadratic polynomial in U=Y^2 is irreducible, and its root determines `V=(2AU+B)/h` with V^2=D. Here A and h are nonzero functions; X is a transcendental coordinate. Thus k(X,V)/k(X) has degree two.

Set t=V-2rX. Since r^2=5, expansion of V^2=D cancels the X^2 terms and gives

`(a+4rt) X = b-t^2`.

This yields X=(b-t^2)/(a+4rt), V=t+2rX, and the independent checker verifies the conic equation after substitution. The denominator a+4rt is not identically zero. Indeed if t were constant and both sides vanished, one would need a^2=80b, already excluded; otherwise X would be constant, impossible. Hence t is transcendental and k(X,V)=k(t). This proves C012-C013 with the degree assertion rather than a merely formal parametrization.

## 3. Second quadratic extension, compositions, and genus

In k(t), the U root `(-B+hV)/(2A)` is exactly

`m z^2 F(z) / [400 (z+gamma lambda)^2 (z+alpha lambda)]`,

where z=t+d. This is an independently checked rational identity, retaining the specified conic branch. With s=z+alpha lambda and w=20Y(z+gamma lambda)/z, it becomes

`w^2=m F(s-alpha lambda)/s`.

The nonzero constants m and alpha, and the affine-linear functions z, s, z+gamma lambda, are nonzero in k(t). Thus these replacements are legitimate function-field changes, even when they vanish at individual points. The exact identities

`F(-alpha lambda)=(-16/5+16r/25) lambda^2(lambda+5r)` and

`disc(F)=(24064+10752r) lambda(lambda+5r)^3(lambda+c)`

show on every allowed fiber that the cubic F has three distinct roots and none equals -alpha lambda. The right-hand side of the w equation has a simple zero at each cubic root and a simple pole at s=0. At infinity it has pole order two, since F is monic cubic. There are exactly four odd valuations. In particular this function is nonsquare in k(s), so the second quadratic extension has degree two. Riemann-Hurwitz gives `2g-2=2(-2)+4=0`, hence g=1.

This also proves quartic irreducibility without circularly assuming a chosen component. Construct the degree-four tower k(X) subset k(X,V)=k(t) subset k(t,Y), where Y^2=U. Since `V=(2AY^2+B)/h`, k(X,Y) already contains V; its degree over k(X) is exactly four. G has degree four in Y and annihilates Y, so it is its minimal polynomial up to its nonzero leading coefficient. G is irreducible in k(X)[Y].

The exact shifted identity is

`mF(s-alpha lambda)=a0 s^3+a1 s^2+a2 s+a3`.

For lambda unequal to 0,-5r, a3 is nonzero. Set xi=a3/s, eta=xi w; substitution gives the stated monic cubic W. Its elliptic discriminant is exactly the displayed nonzero Delta_W on the allowed range. This proves C014-C016 and the algebra/branch parts of C020.

Both compositions are independently verified. With t_forward=(2AY^2+B)/h-2rX,

`b-t_forward^2-X(a+4r t_forward)=-4AG/h^2`.

On G=0 the recovered X therefore agrees with X. The recovered Y cancels literally after w and eta substitution. Conversely, substitute X(t) and U(t) into `(2A U+B)/h`: the result is exactly V=t+2rX(t), checked independently. Thus the inverse cubic equation recovers the same t, then s=a3/xi, z, xi and eta. There is no unverified square-root sign in the reverse map. These are inverse field maps and prove C017-C018.

For each allowed specialization the charts are dense and nonempty: X and t are nonconstant; A,h are nonzero polynomials in X; z,s,z+gamma lambda are nonconstant linear functions in t; xi=a3/s is nonconstant. A denominator can vanish at finitely many points, but none becomes the zero function at an additional allowed parameter. A function-field isomorphism of integral curves extends uniquely to their smooth projective models, because local rings there are discrete valuation rings and properness supplies the value of a rational map. Thus C019 is valid on every allowed fiber, including chart poles and plane singularities. Distinct normalization points may share a plane image at nodes; points are counted intrinsically on W/normalization.

## 4. Primitivity and the entire projective curve

Over k[X], A has its only root X0=-(5phi+lambda)/10. Exact substitution gives

`B(X0)=lambda(lambda+5r)(lambda+5(phi+1))/25`.

Away from 0,-5r the sole possible common A,B root is at lambda=-5(phi+1). Then X0=1/2 and C(X0)=-1. Hence A,B,C have no common root in k, and the polynomial G in k[X][Y] is primitive. Its irreducibility over k(X) therefore gives irreducibility over k[X,Y] by Gauss's lemma. This closes C021 for every allowed parameter and also for lambda=-c.

The restriction at T=0 is `2X(X^4-10X^2Y^2+5Y^4)`, nonzero. Thus the homogeneous polynomial has no factor T. Any projective component contained entirely outside T=1 would be the line T=0, already ruled out. Any factor of the homogeneous polynomial dehomogenizes to a factor of G unless it is supported on that line. Consequently the entire projective quintic is geometrically integral, not just a selected component, and W is the model of its normalization. This closes C022 and the global part of C003/C020.

## 5. Exact excluded fibers and all singular/cuspidal cases

At lambda=0, P is the established product of five distinct side lines. At lambda=-5r the independent coefficient identity is

`P-5r TQ^2=P_conjugate`, with phi_conjugate=(1-r)/2.

This is the cyclotomic conjugate zeta -> zeta^2 of the five-factor expression; the five factors are distinct. Geometrically these are the five star-pentagon lines. The candidate only says again five lines, which is correct. Both excluded members are reducible, with normalization the disjoint union of five rational lines. Their lines are tangent to a nondegenerate concentric conic. Three distinct such lines cannot be concurrent, since their dual points lie on a nondegenerate conic and a dual line meets it at most twice. Their five directions are distinct, so the ten pairwise intersections are ordinary nodes and none lies at infinity. Thus neither member is geometrically integral or genus one. This proves C023-C024.

At lambda=-c, the conic discriminant is exactly -64, so the first extension remains degree two. In the s-coordinate the independently factored polynomial is

`F(s+alpha c)=(s-8r/5)(s-1-3r/5)^2`.

The roots 8r/5 and 1+3r/5 differ by r-1, nonzero. Neither equals zero, as also witnessed by `F(s+alpha c)|_(s=0)=-48/5-112r/25`. The monic gcd with its derivative is exactly s-1-3r/5. After removing the square, the w-cover has only the simple root s=8r/5 and the simple pole s=0 as odd valuations; infinity has even valuation. It is still nonsquare, so the tower degree is four and the primitive whole quintic remains integral, but Riemann-Hurwitz gives g=0. This closes C025 and the final finite excluded case of C003.

The infinite member of the compactified pencil is exactly TQ^2=0. It is nonreduced; its reduced support is a line and a conic, both rational. It supplies no additional elliptic member. This proves C026.

For completeness, all finite integral fibers' plane singularities can be identified, not merely inferred generically. The base vertices lie on two incident sides and on Q=0; both P and Q^2 have zero gradient there for every lambda. At the vertex (1,0), with X=1+u, Y=v, the exact constant and linear jets vanish, and the quadratic jet is

`(25+10r+4lambda) u^2 -25v^2`.

Except at lambda_cusp=-(25+10r)/4 this has two distinct tangent lines over k, giving an ordinary node of delta invariant one. At lambda_cusp the quadratic is -25v^2 and the coefficient of u^3 along its kernel v=0 is exactly five. In characteristic zero, formal completion of the square in v reduces the germ to a unit times v'^2 plus a function of u of order three; extracting units yields the ordinary A2 cusp, again delta one. The rotation (Z,W)->(zeta Z,zeta^(-1)W) preserves Z^5+W^5 and ZW, hence P, Q, and the pencil. It cycles the five distinct vertices, so this local conclusion holds at every vertex. The cusp parameter has lambda+c=-3/4 and differs from 0,-5r, so W is nonsingular there and its normalization has genus one. This closes the complete five-vertex statement C027.

For every allowed fiber the five vertices contribute total delta=5. The arithmetic genus of an integral plane quintic is six and its normalization has genus one, so the genus-delta formula permits no other singularities. At lambda=-c the vertex quadratic coefficient is three and the five vertices are nodes. The additional center (0,0) has quadratic jet X^2+Y^2, also an ordinary node over k. These six nodes contribute delta=6, exhausting the difference between arithmetic genus six and normalization genus zero. Thus there are no hidden singularities on that fiber either. This is an all-fiber classification, supported by universal identities and the genus formula, not by a finite scan.

## 6. Infinity, the origin, and all denominators

At T=0 put Y=1. The infinity polynomial is `2X(X^4-10X^2+5)` and its gcd with its derivative is one, checked exactly. The five roots are 0 and +/-sqrt(5+2r), +/-sqrt(5-2r). There is no point with Y=0, since P(1,0,0)=2. Squarefreeness of the restricted binary quintic means at least one X/Y partial is nonzero at each infinity point, independent of lambda; thus all five are smooth for every finite member. At O=[0:1:0] the X partial is exactly ten.

On the smooth monic cubic the usual projective point O has ord_O(xi)=-2 and ord_O(eta)=-3. Therefore s=a3/xi has order two, w=eta/xi has order -1, and

`z(O)=-alpha lambda`, `z(O)+gamma lambda=(gamma-alpha)lambda`,

`a+4rt(O)=4(3-r)lambda`, `X(O)=-(5phi+lambda)/10`.

All relevant constants and lambda are nonzero on the allowed domain. Therefore Y=w z/[20(z+gamma lambda)] has a simple pole while X remains finite, giving the plane limit [0:1:0]. This is a genuine smooth plane point, hence a unique point on the normalization. The origins agree, proving C028.

The boundary checker simplifies all inverse transverse denominators to one divisor:

`a+4rt=4r(z+gamma lambda)`,

`X=(-z^2+2dz+8lambda)/[4r(z+gamma lambda)]`.

Forward denominators are A,h,z,s; inverse denominators are xi,z+gamma lambda,a+4rt and fixed nonzero constants. Each is a nonzero function on every allowed fiber, as proved above. F(0)=16(3+r)lambda[lambda+(25+10r)/4] identifies the z=0 vertex event: at generic allowed lambda two normalization branches map to that node; at the cusp parameter this point becomes a branch point and the germ is unibranch. These chart events introduce no new fiber exclusion.

Although full torsion is outside this family's assigned scope, the displayed inverse-denominator identity relevant to the other twenty points was independently checked:

`z+gamma lambda=(gamma-alpha)lambda x/(x-beta)` after the Tate map.

Thus, conditional only on a point having Tate abscissa distinct from 0,beta, none of the inverse denominators vanishes. This family does not use that calculation to infer that a division polynomial has ten distinct roots; that obligation belongs to the division family.

## 7. Tate model, all-fiber nonsingularity, and actual isomorphism

The parameters simplify exactly to `beta=-lambda/[c(lambda+5r)]`, and

`beta^2-11beta-1=-125(lambda+c)/[c(lambda+5r)^2]`,

`Delta_beta=125 lambda^5(lambda+c)/[c^6(lambda+5r)^7]`.

These are independently checked universal rational identities. The generalized Weierstrass coefficients a1=1-beta, a2=-beta, a3=-beta, a4=a6=0 give b2=beta^2-6beta+1, b4=beta^2-beta, b6=beta^2, b8=-beta^3, and their standard discriminant is beta^5(beta^2-11beta-1). The factorization therefore proves exactly the candidate's finite allowed range corresponds to nonsingular Tate models; lambda=-5r is the transformation pole. This closes C029 without relying on the cited Fisher statement.

Complete the square by v=y+((1-beta)x-beta)/2. Then v^2=T_beta(x)/4. The fresh checker verifies the full identity

`W_R(q(x-beta))=q^3 T_beta(x)/4`.

Because delta^2=d and q=dk^2, `(k delta)^6=q^3`. The candidate's eta=(k delta)^3 v and xi=q(x-beta) therefore give the actual equation isomorphism over K(delta), with its sign fixed. q and k delta are nonzero on every allowed fiber, and the inverse transformations are affine-linear. On projective cubic coordinates they are the invertible linear change

`[x:y:Z] -> [q(x-beta Z):(k delta)^3(y+(1-beta)x/2-beta Z/2):Z]`.

It fixes the unique infinity point [0:1:0]. Hence the map is an origin-preserving isomorphism on every allowed fiber, not simply an equality of j-invariants. No denominator involves j or excludes j=0,1728. This closes C030.

## Stable-ID closure ledger

All entries below are CLOSED within this family's geometric scope. No ID is closed merely by a previous report's verdict. Proofs use characteristic zero, the fixed coordinate field and scaling, and finite lambda unless the infinite member is explicitly discussed.

| ID | Evidence and exact closure | Remaining family gap |
|---|---|---|
| C001 | Cyclotomic quotient-ring product, ten vertex evaluations, real expansion and explicit -32 side scale; Section 1 | None |
| C002 | Exact homogeneous degree-five pencil and identified smooth origin; Sections 1,6 | None |
| C003 | Degree-two tower twice, four branch points, primitivity/projective closure, and complete excluded-fiber analysis; Sections 2-5 | None |
| C011 | Fresh exact coefficient comparison of G and P+lambda TQ^2 at T=1 | None |
| C012 | Fresh quartic discriminant identity | None |
| C013 | Conic discriminant, nonsquare valuation argument, exact inverse and t nonconstant; Section 2 | None |
| C014 | Fresh rational U identity and nonzero-function denominator argument; Section 3 | None |
| C015 | Fresh shifted polynomial coefficient identity | None |
| C016 | Fresh cubic identity, a3 nonzero, discriminant nonzero; Section 3 | None |
| C017 | Both inverse compositions, with conic branch explicitly checked; Section 3 | None |
| C018 | Fresh forward residual and reverse branch identities | None |
| C019 | Dense charts on each allowed specialization and unique extension between smooth projective models; Section 3 | None |
| C020 | All four exact identities plus extension degree, infinity valuation and Riemann-Hurwitz proofs; Sections 2-3 | None |
| C021 | Only A-root, B factor and exceptional C=-1; Section 4 | None |
| C022 | Primitive affine irreducibility and nonzero T=0 restriction; Section 4 | None |
| C023 | Established distinct side-line product; Section 5 | None |
| C024 | Fresh conjugate polynomial identity and distinct cyclotomic conjugate factors; Section 5 | None |
| C025 | Exact -c factorization/gcd, two odd branch valuations, primitive integral whole curve and genus zero; Section 5 | None |
| C026 | Homogeneous infinite member TQ^2, nonreduced rational support; Section 5 | None |
| C027 | Universal vertex jet, nonzero cusp kernel cubic, verified order-five rotational invariance, delta-genus closure; Section 5 | None |
| C028 | Cubic pole orders, nonzero limiting denominators, exact finite X and plane partial ten; Section 6 | None |
| C029 | Direct Weierstrass discriminant and exact pullback factors; Section 7 | None |
| C030 | Fresh actual twist equation identity, nonzero affine-linear inverse and projective origin preservation; Section 7 | None |

## Public export and historical-body audit

At the parent's additional request, `bind_exports_v01.py` independently hashed and diffed the four exported bodies against their actual historical originals and PORTABILITY.json. The native run was 2026-10-04T12:48:24.998182+00:00 to 12:48:25.043927+00:00, exit 0, empty stderr. The script body hash is `513722ab1c5022b4b793c8f8f471e09da4b1e7f25e67979ab469460f0caf6fd2`. Exact path/byte/hash records and complete diffs are preserved in `export_binding.json` and its receipt. All four original byte counts and original/exported hashes match PORTABILITY. The public archive was not modified.

| Public body | Actual original hash | Actual exported hash | Actual change and mathematical scope |
|---|---|---|---|
| geometry_source.py | ec534b8544678dd4490e289f879b9b62773a19f684d6867bbe98c2597f95b822 | b4e6011d6dacff9563e0c959583322679942d1f75505110769eae486d0ea9c7d | Added shebang/optimization guard only. Two static assertions: side resultant identity and vanishing constant/linear vertex jets. Other singular obstructions, center/cusp expressions and gradients are printed computations, not separately asserted global proofs. |
| geometry_quotient.py | 0e164226679c43302ea1f805bb96f3e58611f8447efc786f3cd1286ed8c45141 | 2bcc7f2396343f0d7d5f6c3081a1a167eca042811e89734c2611c3762b70ae50 | Added shebang/optimization guard only. Two static assertions: quotient remainder zero and alternate line-fiber identity. Printed cubic discriminant does not itself prove quotient identification or an all-fiber genus claim. |
| geometry.py | 3317afcac8265e18381aa086074b9d4090ca31fd260f6bbf39aefa5c64095cae | c26a532c7d092b32a76dc204c0845fde8d7a545d4cd9127362616015efadfba4 | Added shebang/optimization guard only. It contains 27 named exact check calls, four mutation rejections, and further direct assertions for denominators/gcd/cusp/excluded discriminants. The reported count is the 27 check calls, not a count of all assertions or a complete logical proof of primitivity/extension degrees. |
| geometry_primitivity.py | 1793c6d3402f2738820339aa784f71ef8de6649516197d08ef26514ca2ad0da9 | 621aa2b21c7d294229cbfde2dc35c3ecf155647637df212f818ceada3213a137 | Added shebang/optimization guard and removed only Python interpreter-version text from the provenance print. Mathematical body unchanged. There are 15 static equal-call sites, one with a dynamic label; loops make the reported exact-identity count 18. It proves the universal resultant/unique-root identities and also checks five concrete boundary contents and explicit mutants. |

These bodies were read as code. Their results are not promoted from historical PASS labels. The parent is separately replaying all exported programs with complete actual output receipts. This family binds body integrity and audits mathematical scope; it does not claim to have performed that parent's archive replay. The first two source programs use the source convention L=-lambda after the real-coordinate bridge, so their printed eliminated obstructions can contain divisions at additional L-values. Those prints are not used here for an exhaustive singular-fiber theorem. The independent double-cover and primitivity proof above closes that gap directly.

The supplement's finite boundary substitutions and mutants are implementation controls. General symbolic discriminant, rational-map and resultant identities are universal algebra certificates. Irreducibility, ramification, Riemann-Hurwitz, projective closure, delta counts, and isomorphism extension are the explicit deductions supplied in this report; identity counts alone do not prove them. No finite group enumeration from another family is used here.

## Findings, limits, and hold

The strongest verified result is the complete global geometric normalization theorem with exactly the stated finite elliptic range, including the five-cusp allowed plane member, both map compositions and all denominator/hidden-component obligations, together with the genuine origin-preserving Tate twist on every allowed fiber. The assigned stable IDs are closed without an additional parameter exclusion. No correction to the candidate geometry is required by this review.

The twenty residual torsion points, exact division field, imported modular/specialization source claims, Galois group/action, priority and publication package outside these four bodies remain parent/other-family obligations. This report does not mark them closed by implication. No external individual was contacted; no candidate, tracker, Git/index/branch/PR, installation, publication or historical namespace was modified. This family is held unchanged for the parent's closure process.
