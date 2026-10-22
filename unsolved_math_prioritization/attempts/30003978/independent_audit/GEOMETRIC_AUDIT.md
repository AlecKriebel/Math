# Independent geometric audit

Problem 30003978 (OWR-16628-010), queue rank 743. Audit date: 5 October 2026.

## Verdict and evidence level

**PASS for the prior-literature resolution, with the precise scope and status below.** No blocking mathematical error was found in the argument needed to obtain an ample integral polarization with irrational one-point Seshadri constant on each complex plane blowup at r very general centers, for every integer r >= 9. The requested implication from Nagata follows because these later constructions do not assume Nagata.

This is an ordinary mathematical audit, including reconstruction of the necessary geometric steps. It is stronger than matching abstracts or accepting theorem statements without inspection. It is not a proof-assistant certificate, a journal referee decision, or a guarantee against errors. The two decisive sources are extremely recent preprints. Their authors retain credit for the constructions; this packet claims neither novelty nor a proof of Nagata.

Sources used are pinned in SOURCE_PINS.json. We independently retrieved and read Laface–Ugaglia v2 (LU), including every proof on pp. 2–11, and Malara–Merta–Szpond–Zielinski v1 (MM), including every proof on pp. 3–16. The uniform paper's concluding remarks and references were also inspected. Numerical outputs are corroboration of the reasoning, never a substitute for geometry.

## 1. Exact question and quantifiers

The OWR contribution on printed pp. 2760–2761 has Theorem 1 for r >= 9 under the negative-curve conjecture on X_(r+1). Its final question substitutes Nagata on X_r alone. It does not ask to prove Nagata, and it does not require a uniform equal-multiplicity polarization. The full Hanumanthu–Harbourne article specifies very general plane centers in its setup on p. 2 and in Question 2.6 on p. 5. This supports the packet's explicit very-general interpretation of the conference summary's abbreviated “general.” It does not justify replacing a countable exceptional union by a single Zariski-closed exceptional set for the Seshadri equality.

The object sought is a line bundle on a smooth surface, evaluated at one very general point. Blowing up that evaluation point raises the total number of plane centers from r to r+1. A multipoint constant on the plane, a divisor only on a singular quotient, or an irrational real scalar multiple of a line bundle would each be insufficient. The proof below reaches an integral ample class on the required smooth surface.

The OWR proof sketch contains a negative intersection with the pullback of an ample divisor, which is impossible; the intended boundary class must subtract the evaluation-point exceptional divisor. This typo is visible in the primary PDF and is already disclosed by the author packet. The final question itself is clear and is not altered by this observation.

## 2. Birational dynamics: a nef ray on the special orbit

Work on S = P1 x P1. For odd n >= 5 let the group have generators (x,z) -> (zeta*x,zeta^(n-2)*z) and (x,z) -> (u/x,u^(n-2)/z), with u > 1. Its free orbit through (1,1) lies on the smooth graph z=x^(n-2). There are 2n distinct centers.

The de Jonquieres map preserves the first ruling and is fractional linear in the second coordinate. Its two bihomogeneous sections have bidegree (n,1). To audit their base scheme, write C=c^w, A=c^(n-w), X=x^w, Y=x^(n-w). Their coefficient determinant is the polynomial identity

  -(C-d)(A*d-1)(X*Y-1)(X*Y-C*A).

Under c^n != 1 and d not equal to c^w or c^(w-n), its 2n zeros in the first factor are simple. The second-coordinate coefficient of the first section is nonzero at each zero, so the coefficient matrix has rank exactly one there. There is one reduced base point on each such fiber, no common component, and no extra base scheme because the pencil's self-intersection is 2n. After blowing them up, precisely the 2n disjoint ruling transforms of square -1 are contracted. The target is a smooth ruled product, and the inverse centers have parameters (c,c^(2w-n)/d). This proves the required isomorphism of the two blown-up surfaces, rather than merely a lattice isometry.

The initial weight (n-1)/2 is a unit modulo every odd n, including composite n, with inverse n-2. Exponent pairs begin at (n-2,1). Alternating steps are (a,b) -> (-a-b,a) and (a,b) -> ((n-4)a-b,a). Induction gives |a|>|b|>0, equal signs at even stages, and opposite signs at odd stages. Both forbidden slopes have absolute value at least two. Thus every step is nondegenerate; an infinite sequence of actual isomorphisms exists.

In the symmetric basis (H1,H2,E=sum E_i), the pullback matrix is

  T = [[0,1,0],[1,n,2n],[0,-1,-1]].

It preserves the pairing with H1.H2=1 and E^2=-2n. Put Delta^2=n(n-4), alpha=(n-Delta)/2, beta=(n+Delta)/2, and lambda=(n-2+Delta)/2>1. The vector R=(alpha,beta,-1) is a lambda-eigenvector. The reciprocal vector and K=(-2,-2,1) have eigenvalues lambda^(-1) and 1. The decomposition of H2 has coefficient beta/[n(n-4)]>0 on R. Thus rescaled pullbacks T^j H2 converge to a positive multiple of R. Each is genuinely nef as the pullback of a ruling through the actual isomorphisms. Closedness of the nef cone establishes nefness of R on the special configuration.

The computations in the verifier establish all universal matrix identities over the quotient relation Delta^2=n(n-4). Their geometric interpretation depends on the preceding base-scheme and isomorphism argument, which was separately checked.

## 3. Normal bundle and the reflection, with no ramified shortcut

Move the initial orbit representative to (1+t,1) while keeping the group fixed. This is an algebraic family after removing finitely many bad parameter values from A1. Although MM describes a small disc, its rational formulas extend to this algebraic open neighborhood. The 2n sections are disjoint there and their blowup is a smooth projective family over that neighborhood.

For the special graph Gamma, the pre-blowup normal bundle in the threefold is O(2n-4) direct-sum O. Each moving section causes an elementary transform at its intersection with Gamma. In local normal coordinates v=z-x^(n-2), t, the derivative of a section has normal slope -(n-2)x^(n-2) at roots of x^n=1 and the opposite slope at roots of x^n=u^n. A local blowup chart sends normal directions (h,g) to (xi*h+v_i*g,g), so the transform really imposes the condition f(x_i)=v_i*g(x_i). This checks the geometric origin of the polynomial constraints.

The transformed normal bundle N has degree (2n-4)-2n=-4. After twisting by O(1), a section is a polynomial pair of degrees at most 2n-3 and 1. Its two divisibility conditions give quotient polynomials a,b of degree at most n-3. In the difference of the identities, coefficients of degrees n through 2n-3 force a=b. What remains has one side supported in degrees n-2,n-1 and the other in degrees at most n-3. Since u^n != 1, both vanish. Therefore H0(N(1))=0. Splitting on P1 then forces N=O(-2) direct-sum O(-2). The affine coordinate computation covers all global sections: the original summands are O(2n-4) and O, and no center is at infinity.

The required reflection follows directly in these rational marked families. Every integral class on the geometric generic fiber is represented by a globally defined combination of ruling and exceptional line bundles. If it is effective after algebraic closure, flat extension of scalars for H0 gives a section already over the original function field. No finite or ramified extension of the base is necessary.

Take the closure of its effective divisor. It is Cartier in the smooth total space and has no fiber component. Its restriction C0 is effective and has the same marked class c. If its vanishing order along Gamma is mu, the first nonzero normal term is a section of a bundle of degree c.gamma+2*mu. Hence c.gamma+2*mu >= 0. Also C0-mu*Gamma is effective. It follows that the reflected class c+(c.gamma/2)*gamma is represented by an effective rational divisor. Pairing with the special nef class R shows the reflected R is nef on the geometric generic fiber. Countably many relative effectivity loci transfer this to very general fibers.

This reconstruction deliberately does not certify MM Proposition 2.1 in the greatest abstract generality of an arbitrary marking of Neron–Severi spaces. Its terse finite-base-extension argument would require attention to divisor descent and to the normal bundle under a possibly ramified base change. Neither issue occurs in the globally line-bundle-marked rational families actually used here. LU Lemma 1.4 supplies the detailed safe argument, and replacing ten sections by 2n changes none of its reasoning. MM's general corollary is likewise not used as a substitute for checking domination of the evaluation-point parameter space.

Since gamma=(n-2,1,-1) has square -4, reflection takes R to the positive multiple

  [n(n-3)+(n-1)Delta]/4 * (n-4,1,-Delta/n).

Consequently the symmetric multipoint class is nef on a moving free orbit. Countability and closedness of the bad effectivity loci transfer it first to a very general free orbit of the fixed group, then to a very general ordered 2n-tuple. Its square is zero. The upper bound from the square therefore agrees with the lower bound, with multipoint constant sqrt((n-4)/n).

## 4. Cartier quotient and normalization

Conjugating coordinates gives the action (x,z) -> (zeta*x,zeta^2*z), (x,z) -> (1/x,1/z), without changing ruling classes. Both functions x^n+x^(-n) and z^n+z^(-n) descend to morphisms from the normal projective quotient Y to P1. The weighted sum of their pulled-back O(1) bundles, with weights n-4 and 1, is an actual Cartier line bundle A. Its pullback to S has bidegree (2n(n-4),2n), so A is ample by finite pullback and A^2=4n(n-4). This explicit construction avoids assuming that an invariant divisor automatically descends as Cartier.

For n=5, LU instead uses the natural linearization on -5K_S. At corners the stabilizer characters have order dividing five; at reflection-fixed points the tangent determinant is one. Thus the stabilizers act trivially on that line bundle and finite quotient descent applies. It yields the same numerical polarization.

At a free orbit the quotient is etale. Blowing up its image and the orbit gives a finite map whose pullback of the single exceptional divisor is the sum of the 2n exceptional divisors. Nefness is equivalent under this finite pullback. Scaling the upstairs line bundle by 2n therefore gives one-point constant 2n*sqrt((n-4)/n)=2*sqrt(n(n-4)), not an extra division by 2n or its square root. Finite images of the countably many excluded proper closed sets remain proper, giving the very-general assertion on Y.

## 5. Resolution, ruling, and plane marking

Every nonidentity rotation fixes exactly the four corners because n is odd. They form two group orbits with cyclic quotient types 1/n(1,2) and 1/n(1,n-2). Each reflection fixes four torus points. Distinct reflections have no shared torus fixed point, and their 4n fixed points form four orbits of size n with tangent action (-1,-1). Thus there are exactly four additional A1 singularities and no overlooked branch divisors.

Write n=2k+1. The first invariant function gives a rational ruling on the minimal resolution Z. Its only reducible fibers lie over 2,-2,infinity. The finite fibers have chain weights (-2,-1,-2) and multiplicities (1,2,1). The cyclic continued fractions are n/2=[k+1,2] and n/k=[3,2,...,2], with k the inverse of n-2 modulo n. They give the infinity chain

  (-(k+1),-2,-1,-3,-2,...,-2)

with multiplicities (1,k+1,n,k,k-1,...,1). Intersecting the total fiber with each component gives zero and determines the central square -1. The verifier checks the continued fractions, null vectors and contractions independently using chain intersection matrices.

The invariant graph B: z=x^2 gives a section C on Z. This is an auxiliary curve, different from the original special graph used for reflection. Its quotient square is 4/(2n)=2/n. At the two finite singularities the corrections are 1/2 each. At the cyclic corner, the local invariant chart (z/x^2,x^n) shows that the section meets the -(k+1) end transversely. The inverse intersection-matrix entry there is 2/n. Hence C^2=2/n-1/2-1/2-2/n=-1.

Contract the finite fibers' middle components and then the components away from C. At infinity contract the central -1 component, the neighboring -2 component on the short side, and then the long chain in order. Schur-complement intersection calculations show every contracted curve has square -1 at that stage and is disjoint from C. The remaining fibration is a smooth P1 bundle with a section of square -1. By the classification of ruled surfaces over P1 it is F1: on F_e a section distinct from its negative section has square at least e, so a negative section of square -1 forces e=1. Contract C to obtain P2. Reversing gives exactly 1+4+(k+2)=k+7 blowups, allowing infinitely near centers.

For the total-transform basis (h,e1,...,e_(k+7)), M=nu^*A pairs with C=e1 by n-2 and with the ruling fiber h-e1 by 2n. It is orthogonal to the quotient-resolution exceptional curves, but not to the central components of the three fibers. These equations yield degree 3n-2, multiplicities n-2 once, n four times, 4 k times and 2 twice. In particular the last multiplicity is determined by (2k+1)*m=2n and is exactly 2. The square is 4n(n-4). This checks both the integral plane class and the count of centers.

## 6. Smooth deformation and evaluation-point quantifier

Choose a smooth quotient point attaining the one-point equality and blow up its inverse image on Z. The class M-2*sqrt(n(n-4))*e_(k+8) is nef as a pullback from the blown-up quotient. This special surface is a fiber in the universal family of ordered sequences of k+8 point blowups of P2. Successive universal surfaces construct a smooth irreducible parameter space, including infinitely near centers; the locus of distinct proper centers is dense and open.

Every integral marked class has a global line bundle in this family. For each class intersecting the fixed real boundary class negatively, semicontinuity of H0 makes its effectivity locus closed. The special nef fiber excludes it, so it is proper. There are only countably many integral classes. This proves nefness on very general proper-point fibers, without assuming that nefness is open for a real class.

A quadratic transformation at three multiplicity-n points changes the first k+7 entries from

  (3n-2; n,n,n,n,n-2,4 repeated k times,2,2)

to degree 3n-4 with multiplicities n once, n-2 four times, 4 k times and 2 twice. The evaluation point is not a transformation center and its coefficient is unchanged. For n=5, one more quadratic transformation yields (9;3 repeated five times,2 repeated four times). Quadratic transformations induce birational maps of the open configuration spaces, preserving the very-general qualification.

Finally, forgetting the last proper plane point is smooth and open. For every proper closed exceptional locus upstairs, the image of its open complement contains a dense open set downstairs. Outside the resulting countable union downstairs, each exceptional locus restricts to a proper closed subset of the evaluation-point fiber. This establishes the required order of quantifiers: for very general r plane centers, the equality holds at a very general point of their fixed blowup. Points on its exceptional curves can be excluded; they form a proper closed set. No claim is made for every point.

## 7. Ampleness, not merely nefness

For r=9 the unique cubic through very general centers is smooth and irreducible. Its transform represents -K_X and has square zero, so it is nef: distinct irreducible curves have nonnegative intersections. Contract the last four exceptional curves to the degree-four del Pezzo S5. The final divisor equals 2(-K_X)+eta^*(-K_S5). Every noncontracted curve meets it positively, while each of the four contracted curves has degree 2. Its square is 20. Nakai–Moishezon proves ampleness of this integral divisor.

For n>=7 the multiplicities are positive and decreasing. All hypotheses of Hanumanthu, arXiv:1507.06391v3, Theorem 2.1, were checked directly in the source. That theorem is unconditional; no later conjectural criterion in that paper is being substituted for it. The three linear margins are n-2, n, and 3n-12. The squared multiplicity sum is Sigma=5n^2-8n+16. For every s>=2, (s+3)/(s+2)<=5/4, and

  4(3n-4)^2-5*Sigma = 11n^2-56n-16
                       = 11(n-7)^2+98(n-7)+131 > 0.

Thus the whole family of prefix inequalities holds strictly.

I also inspected the proof of the criterion and its Lemma 2.3 on pp. 3–6. Its essential geometric input is the unconditional Xu/Ein–Lazarsfeld bound e^2 >= sum a_i^2-min a_i for an irreducible moving plane curve with prescribed multiplicities at very general points. For a_i with maximum at least 2, the elementary inequality sum a_i^2 >= (s+3)min a_i, except the isolated pair (2,2), and Cauchy–Schwarz combine with our strict squared margin to give positive intersection. The isolated pair is handled by d>m1+m2. A single positive multiplicity is handled by e>=a1. When all positive multiplicities equal 1, lines and conics meet at most two and five very general points, respectively; for e>=3, independence of simple point conditions gives s<=(e+2 choose 2)-1<=e^2, and Cauchy–Schwarz again gives positivity. This reconstructs the sufficient argument in the present strict-margin case; it does not assume SHGH or the negative-curve conjecture. The published deformation estimate itself is treated as an established theorem, not re-proved here.

## 8. Coverage, irrationality, and limits

For r=9 the final divisor has square 20 and constant 2*sqrt(5). For every r>=10 set n=2r-13 and k=r-7. This covers every odd n>=7 and gives k+7=r, with no missing rank or congruence class. For n>=5,

  (n-3)^2 < n(n-4) < (n-2)^2,

with positive differences 2n-9 and 4. Thus the radical is not a square. All polarization coefficients are integers before computing the Seshadri constant.

No Nagata, SHGH, negative-curve conjecture, or conditional special-nefness assumption remains in this route. Established geometric inputs still include splitting of vector bundles on P1, semicontinuity/base change, finite quotient descent and nef pullback, cyclic quotient resolutions, contraction and ruled-surface theory, Nakai–Moishezon, and the stated moving-curve estimate. This audit checks their applications and reconstructs the specialized argument, without rebuilding algebraic geometry from foundations.

The excluded stronger claims have explicit controls. On the r=9 surface an evaluation point on E6 has Seshadri constant at most 2, below sqrt(20). If all nine centers lie on a line, the displayed divisor intersects that line's transform by -14 and is not nef. At U=1 the normal-bundle determinant degenerates because the orbit configuration collides. Using the wrong quotient degree or reflection coefficient destroys the required identities. These controls rule out several tempting overextensions; they do not replace the positive proof.

The author freeze is intact. Its 85,787-assertion output and integrity tests replay exactly. The independently written verifier records 32,975 assertions, including universal symbolic identities, exact checks for ranks 9–100, composite odd parameters, normal-bundle matrices, quotient fiber contractions and adverse controls. Finite ranges do not carry the unbounded theorem: the induction, universal identities, and geometric arguments above do.

**Publication boundary:** describe this as a prior-literature resolution supported by a fresh mathematical audit of two recent preprints. Preserve their preprint/unrefereed status and authorship. Do not call it peer-reviewed, formally verified, an original solution, or a proof of Nagata. No source PDF, extraction, screenshot, raw dataset, copied record, or private coordination material belongs in the safe packet.
