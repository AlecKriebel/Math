# Independent source-to-curve geometry audit of PR329

Audit family: exact algebraic geometry/source matching. Candidate: frozen head `96395a4f506af6a6045e3cd59afcba2db6b7e2e7`, problem `20000450`, submitted candidate after 1/5 author turns. Prepared for root external closure, not a self-seal or publication decision.

**Outcome:** I found no substantive geometry gap or counterexample in the candidate. The normalized regular-pentagon pencil, projective homogenization, absolute irreducibility and genus-one range, cubic reduction and both inverse compositions, origin, infinity subgroup, cusp boundary, and quadratic-twist map are independently verified in characteristic zero. The arithmetic full-level cover/field assertion and completeness of the division polynomial are other families' tasks; geometry does not establish them.

## Independence and reading scope

I first viewed the original operative page 51 of the supplied AIM primary PDF, including Question 17 and all four remarks. My source-only baseline was frozen at 2026-10-04T08:37:18.827343+00:00. My pre-candidate derivation of the regular pentagon, all infinity points, local vertex singularities, exceptional radial parameters and rotation quotient was frozen before candidate exposure. The source PDF was personally size/hash checked: 502057 bytes, SHA256 `8b64d2f6b91f791c35afae10b2ef79c15a927a94c2142a56386f80c8b8a596e6`.

I then read full frozen `TURN_1.md`, `FINAL_RESULT.md`, and `verify_turn1.py`, and froze the first candidate assessment at 2026-10-04T08:45:52.519217+00:00. I have not read the imported report, historical/inherited author or reviewer verdicts, ADVERSE/ADVERSARIAL review files, README/CURRENT_STATUS verdicts, PR body, sibling namespace or sibling mathematics. I did not run the supplied verifier or treat its count/self-report as evidence. I used no external-individual contact, outside-chat message, Git mutation, or PR write. Two source-only child spawn attempts requested by root both actually failed with `agent thread limit reached`; no children were created by me. Root later arranged those families independently.

Original source URL: https://www.aimath.org/WWN/qptsurface2/qptsurface2.pdf. This report paraphrases the operative claim and keeps primary scans/private copies outside this namespace.

## Source normalization

Let `r=sqrt(5)`, `phi=(1+r)/2`. Independently, use complex coordinates `u=x+iy`, `v=x-iy`, circumcircle `uv=1`, and side normals at angles `2pi*j/5`. Their side constant is `phi=2cos(pi/5)`. Multiplying their equations gives the resultant

`P_ind=u^5+v^5-phi^5+5phi^3uv-5phi*u^2v^2`.

This follows either by the recorded exact resultant computation or from the power-sum recurrence for the roots of `v t^2-phi t+u`. Its restriction to the circle is `(u^5+1)^2/u^5`, so the five consecutive unit-circle vertices have multiplicity two in intersection. Rotating by pi, replacing `(u,v)` by `(-Z,-W)`, and changing the overall sign gives exactly the candidate polynomial

`P=Z^5+W^5+5phi Z^2W^2 T-5phi^3 ZW T^3+phi^5 T^5`,

with `Z=X+iY`, `W=X-iY`. The vertex set after that rotation is the fifth roots of unity, so this is the original regular pentagon rather than an unrelated five-line arrangement. The candidate parameter is the negative of the independent pre-candidate parameter. The coefficient field is explicitly `K=Q(sqrt(5))`; a nonzero scaling of either equation or a similarity changes the numeric parameter convention.

The source affine square of the circle has degree four. Its correct quintic projective pencil is `P+lambda*T*(X^2+Y^2-T^2)^2`, exactly as in the candidate. Omitting `T` was an independently rejected mutation.

## Function field and birational maps

Extracting the candidate affine coefficients directly from this independently reconstructed polynomial yields `A(X)Y^4+B(X)Y^2+C(X)`, with the candidate's three coefficients. Independently recomputed:

`B^2-4AC=(4X^2+2X-1)^2 (20X^2-aX+b)`,

`a=40+20r+8lambda`, `b=a+5`, and `a^2-80b=64lambda(lambda+5r)`.

Put `h=4X^2+2X-1`, `V=(2AY^2+B)/h`, `t=V-2rX`. The conic has the rational parametrization

`X(t)=(b-t^2)/(a+4rt)`, `V(t)=2rX(t)+t`.

I derived `Y^2=(h(X(t))V(t)-B(X(t)))/(2A(X(t)))` directly. With `d=5+2r`, `alpha=1-r/5`, `gamma=2r/5`, set `z=t+d`, `s=z+alpha*lambda`, `w=20Y(z+gamma*lambda)/z`, and `x0=1/s`, `y0=w/s`. Applying these substitutions to the derived rational `Y^2` automatically produced the four cubic coefficients `a0,a1,a2,a3`, all equal to the candidate coefficients. No imported reduction or candidate F coefficient list was needed to derive them.

The resulting monic cubic is `W: eta^2=xi^3+a2*xi^2+a1*a3*xi+a0*a3^2`, with `xi=a3/s`, `eta=xi*w`. The candidate inverse is recovered exactly:

`s=a3/xi`, `z=s-alpha*lambda`, `t=z-d`,

`X=(b-t^2)/(a+4rt)`, `Y=eta*z/(20xi(z+gamma*lambda))`.

Both compositions were checked, not merely one curve-membership substitution. For the plane-to-cubic-to-plane X-coordinate I proved the exact residual identity

`b-t^2-X(a+4rt)=-4A*G/h^2`,

where `G=A Y^4+B Y^2+C`. Thus the residual vanishes in the original function field. Its Y-coordinate cancels literally. For the opposite composition I substituted `eta^2` from the independently derived W cubic, recovered the exact `Y^2` branch and conic lift, proved `t'=t`, and recovered `xi` and `eta` literally.

A dense open excludes zero/poles of `A`, `h`, `a+4rt`, `s`, `z`, `z+gamma*lambda`, and `xi` as required in the chosen affine expressions. These are proper rational functions, not additional parameter exclusions. The inverse to the plane is interpreted through its normalization. A function-field isomorphism between smooth projective curves extends uniquely everywhere; the finitely many affine poles are not missing normalization points. No claim that those displayed affine fractions are valid at their poles is needed.

## Irreducibility, genus and complete parameter range

Over an algebraic closure in characteristic zero, `20X^2-aX+b` has distinct roots when `lambda(lambda+5r)!=0`, so it is a nonsquare in the rational function field. The quadratic equation for `Y^2` therefore defines a degree-two conic extension. Over that rational conic, the remaining square-root extension has four odd-valuation branch points when F has three distinct roots and `F(-alpha*lambda)!=0`. The independent exact computations give

`F(-alpha*lambda)=(-16/5+16r/25)lambda^2(lambda+5r)`,

`disc(F)=(24064+10752r)lambda(lambda+5r)^3(lambda+phi^5)`.

Consequently the total field has degree four over the X-line; the original quartic in Y is irreducible over the algebraic closure of K, not just a selected component. Riemann-Hurwitz for the double cover of the rational conic with four simple branch points gives `2g-2=2*(-2)+4=0`, hence `g=1`.

Independently recomputed from the derived cubic:

`Delta_W=2^24(161-72r)lambda^5(lambda+5r)^5(lambda+phi^5)`.

Thus the exact elliptic finite range is `lambda not in {0,-5sqrt(5),-phi^5}`.

- At `lambda=0`, the curve is the product of the five original side lines.
- At `lambda=-5sqrt(5)`, an exact polynomial identity replaces phi by `(1-r)/2`, giving another product of five lines.
- At `lambda=-phi^5`, the conic remains nonsingular and the cubic F has exactly one double root, no triple root. The personally computed gcd in the s-coordinate is `s-1-3sqrt(5)/5`. Removing its even square factor leaves two odd branch points, giving genus zero. The plane still has one function field; it is not an elliptic normalization.
- At projective parameter infinity, the pencil member is `TQ^2=0`, reducible and nonreduced.

My pre-candidate local calculation found that five ordinary vertex nodes become five ordinary cusps at independent lambda `5phi+15/4`; the candidate value is `-(25+10sqrt(5))/4`. At each vertex the double tangent has a nonzero cubic term, so each cusp has delta one. The independently recomputed W discriminant is nonzero at this value. The candidate correctly includes it instead of wrongly equating singular plane presentation with singular elliptic normalization.

## Infinity points and the group-law origin

At `T=0`, the quintic is `2X(X^4-10X^2Y^2+5Y^4)`. The points have `X/Y=0, +/-sqrt(5+2r), +/-sqrt(5-2r)`. All five are distinct and smooth for every finite parameter: in complex homogeneous coordinates the restriction is `Z^5+W^5`, whose Z/W partials cannot both vanish on the projective line. The candidate origin `O=[0:1:0]` is one of them; its X partial is exactly 10.

At infinity of W, `xi` has a pole of order two and `eta` of order three. Hence `s=a3/xi` has a zero of order two and `w=eta/xi` a pole of order one. Since `z=-alpha*lambda` and `z+gamma*lambda=(gamma-alpha)lambda` are nonzero in the elliptic range, Y has a simple pole. The conic denominator there is exactly `4(3-r)lambda`, nonzero, and

`X=-(5phi+lambda)/10` is finite.

Thus the plane projective image is precisely `[0:1:0]`; the Weierstrass and plane origins agree, with no translation hidden in the map.

Rotation through 72 degrees preserves the pencil and permutes the five infinity directions cyclically. On the normalization it has exact order five. In characteristic zero an elliptic automorphism fixing the origin has order dividing 2, 4 or 6, so the origin-fixing part of this order-five automorphism is trivial. It is therefore translation by an exact point of order five. The orbit of O is exactly the five infinity points, proving the source's infinity-subgroup assertion with the explicit origin. Their coordinate field is `K(sqrt(5+2r))`, since `(5+2r)(5-2r)=5`. This does not by itself identify the other twenty torsion points or their complete division field.

## Actual twist, not just j-invariant

I completed the square in the candidate Tate equation directly:

`(y+((1-beta)x-beta)/2)^2=x^3-beta*x^2+((1-beta)x-beta)^2/4`.

With candidate `beta=(11-5r)lambda/[2(lambda+5r)]`, `k=4(lambda+5r)/r`, `q=(5+2r)k^2`, the independently derived W cubic obeys exactly

`W_R(q(x-beta))=q^3*[x^3-beta*x^2+((1-beta)x-beta)^2/4]`.

Also `q^3=(k*delta)^6` for `delta^2=5+2r`. Therefore the candidate coordinate isomorphism over K(delta) is exact and origin-preserving. Its inverse is `x=xi/q+beta`, `y=eta/(k*delta)^3-((1-beta)x-beta)/2`. Both scaling factors are nonzero in the full elliptic range. Changing delta's sign composes with elliptic negation, so the quadratic-twist sign is verified. No exceptional j=0 or 1728 restriction is introduced.

## Evidence, negative controls and run limitations

The decisive independent run is `validate_candidate_geometry.py`, native UTC 2026-10-04T08:51:04.444236+00:00 through 2026-10-04T08:51:28.862420+00:00; exit code 0, full stderr empty. It has 27 labeled exact rational-identity checks plus the separate gcd, cusp/bad-parameter and mutation assertions. Every equality is tested as an exact polynomial numerator over Q(sqrt(5)); no floating-point inference is used.

Four deliberate changes were rejected: omitted projective T factor, reversed inverse Y sign, removed conic t shift, and reversed Tate x translation. False ellipticity at each of the three excluded finite parameters was also rejected. The mutations were computed without editing candidate files.

Additional source-only computations and full outputs are `independent_source_geometry.py` and `independent_quotient_geometry.py`. The latter provides a materially different check: the rotation quotient with `q=uv`, `h=(u^5-v^5)/(q-1)` has cubic discriminant `-16lambda(lambda-5sqrt(5))(lambda-phi^5)^5` in my original parameter convention. It agrees with the finite exceptional set and distinguishes a degree-five quotient from a birational model.

Two preliminary Python imports failed because SymPy was absent; those are explicitly recorded and are not mathematical evidence. The first candidate run stopped on a syntactic nonzero comparison of an algebraically zero expression containing unreduced sqrt(5) denominators. A second run passed that assertion after exact algebraic numerator reduction but was terminated by me during inefficient nested rational simplification; it has exit -15, not a pass. Both exact historical scripts and full outputs are preserved. The final run uses the exact rational-function domain over Q(sqrt(5)) and completed. These limitations affect the abandoned runs, not the final successful identities. The own `.runtime/` environment is ignored and must not be published.

## Remaining gap and closure state

Strongest verified geometry result: the candidate's entire specified characteristic-zero regular-pentagon pencil has an absolutely integral elliptic normalization exactly at the claimed finite parameters, is birational to its displayed W cubic with its stated origin, has the stated five-point infinity subgroup, and is the stated quadratic twist of Tate normal form through an explicit exact coordinate isomorphism.

**Exact remaining geometry gap: none identified within that explicitly normalized characteristic-zero claim.** The universal modular full-level identification, specialization of the complete division-field equality, Galois/extension data, and division-polynomial completeness are intentionally unverified by this geometry family. Those are required other-family evidence before promotion of the full submitted claim. Nonregular/star variants and nontrivial Sha/local-solubility constructions are outside the candidate's scope, as explicitly stated; no proof of those variants is inferred.

Best-guess completion of my assigned family: 98%, with root external closure and any new root-directed check pending. This report does not self-seal the namespace, designate the candidate publication-ready, or authorize a release.
