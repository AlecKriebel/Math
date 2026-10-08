# PR148 independent adversarial geometry audit

**Verdict: PASS within mathematical geometry scope.** The submitted two primitive convex six-period orbits are genuine finite-segment billiard trajectories on one connected directed family for the same confocal ellipse pair. Their quotient formed from the orbit's internal angles is exactly unequal. No mathematical correction to the submitted counterexample is required by this audit. This verifies the failure of the printed experimental conjecture; it does not establish historical priority, novelty, publication readiness, or a human peer-review judgment.

Original head: `538fd2584f7dc7375e4eaa91d73daddde3d073cd`. Authenticated original: 20 files, manifest SHA-256 `efd273eb031989bddae0ae89cad8d2e92cc6f531d2076d20d09155a8b508cb02`. Original reported effort remains **1/5**. New central proof-search turns: **0**. Completion of this assigned geometry audit: **100%**.

## 1. Source claim and independence

The preprint is Reznik–Garcia–Koiller, *Eighty New Invariants in the Elliptic Billiard*, arXiv:2004.12497v11, dated 29 October 2020. The published source is the same authors, *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, Arnold Mathematical Journal 7 (2021), 341–355, DOI `10.1007/s40598-021-00174-y`.

The local source PDFs and relevant full pages were inspected visually: preprint pp.1–5; published pp.341–345. Figure 1 and its caption identify the outer polygon as the tangent polygon to the outer ellipse at the orbit vertices, distinct from the polygon of caustic contacts. The preliminaries use signed cross-product areas. Section 3.1 identifies unprimed theta and A with the orbit; primed symbols refer to the outer polygon. Both Table 2 images visibly print

\[
k_{103}=A'/A,\qquad k_{105}=\prod_{i=1}^{N}\sin(\theta_i/2),\qquad
k_{108}=k_{103}/k_{105},\quad N\equiv2\pmod4.
\]

The proof-status column is `?`, so the precise refuted object is the printed experimental invariant assertion/conjecture. The separate odd-N conditions on k103 and k105 do not make their displayed expressions undefined for even N; Table 2 explicitly composes those expressions in the even-N row k108.

Only the displayed ellipse equations and vertex lists were used as inputs to the independently authored checker. The first 115 lines of COUNTEREXAMPLE.md were read to obtain them; this also exposed the submitted elementary prose derivation. Therefore this is **independent implementation and derivation, not a fully blinded rereading of that prose**. No submitted checker, its outputs, or reviewer checker was read as executable source, imported, or run. The new direct proof of the global tangent-map identity below is distinct from the submitted invocation of Poncelet porism.

Exact original and source-byte pins are in `SOURCE_PINS.json`. In particular:

| Artifact | SHA-256 |
|---|---|
| Original COUNTEREXAMPLE.md | `5553f899b1098a321fe2164c3ba0d6eed87bc2424dc8021dee50e01fc14dc4ab` |
| Preprint PDF | `c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da` |
| Published PDF | `c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42` |
| Preprint Table 2 image | `c1ed7836875e802a2c5c0c2165e3a7c01f162e8965e46a440577a2858576a6b4` |
| Published Table 2 image | `99673753a8ac7a346a21a7236fda95cdfcc7ed57e2f13ee78f391fd6c1e4d6a3` |

## 2. Exact inputs and assumptions

\[
E:\ x^2/4+y^2=1,\qquad C:\ x^2/(32/9)+y^2/(5/9)=1.
\]

Both squared axes decrease by lambda=4/9, with 0<lambda<1; the common focal square is 3. Thus C is a strictly interior nondegenerate confocal ellipse. The ordered vertices are

\[
H=((2,0),(4/3,\sqrt5/3),(-4/3,\sqrt5/3),(-2,0),
(-4/3,-\sqrt5/3),(4/3,-\sqrt5/3)),
\]

\[
V=((0,1),(-4\sqrt2/3,1/3),(-4\sqrt2/3,-1/3),(0,-1),
(4\sqrt2/3,-1/3),(4\sqrt2/3,1/3)).
\]

All six points in each list are distinct and exactly satisfy the outer equation. For every directed side v=p(i+1)-p(i), every nonendpoint vertex p(j) satisfies cross(v,p(j)-p(i))>0. These stronger supporting-line inequalities certify strict convexity, a simple boundary, and counterclockwise orientation; positive local turns alone were not substituted for this test.

## 3. Finite chord contacts and physical reflection

Write B=diag(9/32,9/5). Restricting the caustic equation to the actual side segment p+t v gives

\[
\alpha t^2+\beta t+\gamma=0,
\quad \alpha=v^TBv,\quad\beta=2p^TBv,\quad\gamma=p^TBp-1.
\]

The exact checker independently verifies alpha>0, beta²-4 alpha gamma=0, and t=-beta/(2 alpha) strictly between 0 and 1 for **every** side. The complete contact parameters are

\[
H:(1/3,1/2,2/3,1/3,1/2,2/3),\qquad
V:(2/3,1/2,1/3,2/3,1/2,1/3).
\]

The H contacts in cyclic order are

\[
(16/9,\sqrt5/9),(0,\sqrt5/3),(-16/9,\sqrt5/9),
(-16/9,-\sqrt5/9),(0,-\sqrt5/3),(16/9,-\sqrt5/9).
\]

The V contacts are

\[
(-8\sqrt2/9,5/9),(-4\sqrt2/3,0),(-8\sqrt2/9,-5/9),
(8\sqrt2/9,-5/9),(4\sqrt2/3,0),(8\sqrt2/9,5/9).
\]

Each contact independently agrees with the support contact diag(32/9,5/9)n/h for the outward/right side normal n=(v_y,-v_x) and h=n dot p>0. Consequently the entire caustic is to the left of each directed chord, and the tangency is on the **finite segment**, not its extension. No contact occurs at a vertex.

For n(p)=(p_x/4,p_y), arriving unit velocity u and departing unit velocity w, all twelve vertices exactly satisfy

\[
w=u-2\frac{u\cdot n(p)}{n(p)\cdot n(p)}n(p),
\quad u\cdot n(p)=1/3>0,\quad w\cdot n(p)=-1/3<0.
\]

Thus both the full specular equation and the physical incoming/outgoing normal signs hold. The exact side lengths are H:(1,8/3,1,1,8/3,1), V:(2,2/3,2,2,2/3,2), yielding the same perimeter 28/3 and same incoming Joachimsthal constant J=1/3.

## 4. Direct proof of one connected primitive six-period family

This section does not invoke the Poncelet closure theorem. Parametrize the outer ellipse by p(phi)=(2 cos phi,sin phi). For successive CCW chord endpoints phi=m-delta and psi=m+delta, where 0<delta<pi/2, the physical chord line is

\[
\frac{x}{2}\cos m+y\sin m=\cos\delta.
\]

Tangency to C is equivalent to

\[
\cos^2\delta=(8\cos^2m+5\sin^2m)/9,
\qquad \delta(m)=\arcsin\!\left(\frac{\sqrt{1+3\sin^2m}}3\right).
\]

Because

\[
\delta'(m)=\frac{3\sin m\cos m}{\sqrt{1+3\sin^2m}\sqrt{8-3\sin^2m}},
\]

and the denominator squared minus the numerator squared is 8+12 sin²m>0, one has |delta'|<1. Both m-delta(m) and m+delta(m) are strictly increasing smooth degree-one circle maps. Hence

\[
T=(m+\delta)\circ(m-\delta)^{-1}
\]

is a globally smooth orientation-preserving diffeomorphism selecting the unique tangent with C on the left. Its advance is in [2 arcsin(1/3),2 arcsin(2/3)], strictly between 0 and pi. There is no branch jump or degeneracy at an axis endpoint. Every tangent contact is inside the physical outer chord because the caustic is strictly inside the ellipse.

Now use the rational half-angle chart t=tan(phi/2), s=tan(psi/2). The chord line becomes

\[
(1-ts)x/2+(t+s)y=1+ts.
\]

The support equation gives the exact symmetric biquadratic

\[
F(t,s)=5t^2+5s^2-24ts-t^2s^2-1=0.
\]

At s the two roots are the previous and next outer intersections. Vieta's sum gives

\[
r=\frac{24s}{5-s^2}-t,\qquad
w=\frac{24r}{5-r^2}-s.
\]

Let d=5-s² and k=24s-td. The numerator of w+1/t after multiplying by its denominator t(5d²-k²) is

\[
24tkd+(1-ts)(5d^2-k^2)
=F(t,s)(-ts^3+5ts+s^2-125).
\]

The checker verifies this polynomial identity by independently written exact multivariate polynomial division with zero remainder; it does not ask a computer algebra system to infer the identity. Thus T³(t)=-1/t at every generic chart point. Excluded points are only chart poles and finitely many rational-expression poles: the smooth bijective circle map above supplies continuity, so the identity extends to all starting points. In ellipse coordinates -1/t is exactly p mapped to -p. Therefore

\[
T^3(p)=-p,\qquad T^6(p)=p
\]

on the entire left-caustic branch. To justify the dense generic extension explicitly, s²=5 has only two target points and their inverse images under T are finite; r²=5 similarly has only finitely many inverse images under T²; t=0 and the chart point at infinity are isolated. No denominator vanishes identically along the branch.

The map has no fixed point. An orbit of period 3 contradicts T³(p)=-p. Period 2 would imply T(p)=-p, contradicting its advance strictly below pi. Thus all orbits on this branch have least period six. Moreover delta≤arcsin(2/3)<pi/3, so three advances total less than 2pi; T³ is the lift advance pi, and six steps turn once around E. The vertices therefore follow the convex cyclic order.

For completeness, the entire branch obeys reflection, not just the two listed endpoints of the path. For a unit chord velocity z and side support h=cross(p,z), caustic tangency gives

\[
h^2=4z_y^2+z_x^2-\lambda.
\]

Using x²/4+y²=1 gives the elementary identity

\[
4\bigl(n(p)\cdot z\bigr)^2=4z_y^2+z_x^2-h^2=\lambda=4/9.
\]

Thus an arriving chord has n dot z=1/3 and a departing chord -1/3. The CCW tangent component is continuous and never zero: ||n||≥1/2 and |n dot z|=1/3 imply its absolute normalized value is at least sqrt(5)/3. At p=(2,0) both incoming and outgoing tangent components are positive, as explicitly checked for H; continuity on the connected circle keeps both positive. Equal unit lengths and opposite equal normal components therefore force equal tangential components, which is exactly specular reflection at every point.

Finally, phi ranging continuously from 0 to pi/2 moves the initial vertex from H's (2,0) to V's (0,1); the successive T iterates depend continuously on phi. Since the listed first directed sides both put C on the left, their lists coincide with T's iterates. This is a concrete connected path in one primitive convex physical six-period family, with no assumption of the conjectured k108 constancy.

## 5. Outer tangents, signed areas, and internal angles

At p on E the tangent is (p_x/4)x+p_y y=1. For neighboring normals a,b the exact intersection is ((b_y-a_y)/det(a,b),(a_x-b_x)/det(a,b)). All six determinants are strictly positive for each orbit: H has sqrt(5)/6 or 2 sqrt(5)/9; V has sqrt(2)/3 or 2 sqrt(2)/9. The resulting vertices are

\[
Q_H=((2,\sqrt5/5),(0,3\sqrt5/5),(-2,\sqrt5/5),
(-2,-\sqrt5/5),(0,-3\sqrt5/5),(2,-\sqrt5/5)),
\]

\[
Q_V=((-\sqrt2,1),(-3\sqrt2/2,0),(-\sqrt2,-1),
(\sqrt2,-1),(3\sqrt2/2,0),(\sqrt2,1)).
\]

Their strict supporting-line inequalities and both defining tangent equations were checked. The signed shoelace areas are

| Orbit | A | A' | A'/A |
|---|---|---|---|
| H | 20 sqrt(5)/9 | 16 sqrt(5)/5 | 36/25 |
| V | 32 sqrt(2)/9 | 5 sqrt(2) | 45/32 |

All are positive and nonzero. The consistency product AA'=320/9 matches, but its known invariance is not used in this derivation.

The original internal angle is the angle between the vectors **from the vertex to the previous and next vertices**, so cos theta=-u dot w for the arriving and departing velocities. The cosine and squared half-sine lists are

\[
\cos\theta_H=(-1/9,-2/3,-2/3,-1/9,-2/3,-2/3),
\]
\[
\sin^2(\theta_H/2)=(5/9,5/6,5/6,5/9,5/6,5/6),
\]
\[
\cos\theta_V=(-7/9,-1/3,-1/3,-7/9,-1/3,-1/3),
\]
\[
\sin^2(\theta_V/2)=(8/9,2/3,2/3,8/9,2/3,2/3).
\]

Strict convexity puts every theta in (0,pi), so all half-sines have the positive square-root sign. Pairing the repeated values gives

\[
S_H=(5/9)(5/6)^2=125/324,\qquad
S_V=(8/9)(2/3)^2=32/81.
\]

Consequently

\[
k_{108}(H)=\frac{36/25}{125/324}=\frac{11664}{3125},\qquad
k_{108}(V)=\frac{45/32}{32/81}=\frac{3645}{1024},
\]

and their exact positive difference is 553311/3200000.

## 6. Adversarial checks and remaining gaps

- **Finite segment versus support line:** both independently agree; every contact parameter is 1/3, 1/2, or 2/3, never an endpoint or an extension.
- **Physical reflection versus normal parallelism:** full vector equation, unit lengths, and opposite normal signs are checked at all twelve vertices. The branch also has a global elementary reflection proof.
- **Repeated odd period:** six distinct vertices already exclude a repeated triangle; direct T³=antipode excludes every period-three start on the branch.
- **Different components or tangent choices:** a global smooth unique left map, direct closure identity, and explicit phi∈[0,pi/2] path establish one connected family. Reversing an orbit uses the opposite directed branch and preserves the quantity.
- **Convexity versus a hidden star:** every other vertex lies strictly on the inner side of every side line. The primitive family has one full turn in six steps.
- **Orientation and indexing:** reversing both orbit and outer vertex order negates both signed areas and leaves their ratio and all internal angles unchanged; cyclic reindexing only permutes the product. No signed-area cancellation occurs.
- **Half-angle root:** every squared half-sine lies strictly between 0 and 1, and the corresponding convex internal half-angle lies in (0,pi/2), fixing the positive sign.
- **Alternative external-angle reading:** although it is outside the assigned internal-angle claim, replacing internal angles by exterior turning angles also leaves these two quotients unequal; each exterior half-sine product is 1/81. The source's k101 convention gives sum cos(theta)=JL-N=-26/9 in both examples, agreeing with the internal convention used here.
- **Outer object ambiguity:** the computed vertices lie on consecutive outer-ellipse tangents. They are not caustic contacts, pedal feet, antipedal vertices, or outer polygon angles.
- **Axes and rational-chart poles:** both axis starts are nonsingular physical orbits. Only the rational chart formulas have poles; the smooth circle map supplies the exact continuity extension.
- **Confocal degeneration or units:** both ellipses have positive strictly separated squared axes and common focal square 3. Areas have consistent squared-length units, A'/A and the sine product are dimensionless.
- **Code reproducibility:** `python3 -B independent_geometry.py` uses only standard-library exact Fraction arithmetic, an explicit two-dimensional quadratic field, and an explicit polynomial-division implementation. Its assertions verify every recorded conclusion. No floating result is used for a decision.

There is **no remaining mathematical gap in this assigned counterexample geometry scope**. Historical priority, literature after the pinned sources, whether a corrected nearby identity is known, full provenance/process/publication policy, and overall PR promotion remain outside this agent's assignment. `turns.json` remains an approach ledger and is not treated as a timestamped native chat-transition ledger. Nothing here reconstructs absent native history or enlarges original effort.

## 7. Checkable artifacts and action boundary

`independent_geometry.py` is the exact independent implementation. `independent_geometry_results.json` records every side polynomial/contact, each reflection vector, strict convex support crosses, outer intersections, areas, angle data, and the direct family polynomial factorization. `SOURCE_PINS.json` pins all 20 original files and all local source evidence. `RESEARCH_LOG.md` records timestamps and completion estimates. The rendered source-definition PNGs are local visual evidence generated inside this owned folder.

No individual was contacted. No provider action, Git operation, reference/index/cache/program write, original/archive edit, priority investigation, or publication action was performed. All new writes are confined to `geometry_falsification_20261008`.
