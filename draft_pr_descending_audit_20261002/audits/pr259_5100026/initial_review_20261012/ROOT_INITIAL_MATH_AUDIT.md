# Root's initial mathematical audit of PR259 / 5100026

This is an ongoing audit, not a final acceptance or novelty decision. The original
submission is frozen at `0524ed734ee8185681d030af98088259134a6af7`.
Its proof has SHA-256
`77afb7626fd4685b9ce7537aa2de3141df8bf087c5eff0698bb1f7834bc0ad7c`.
Root has read that full proof, all four submitted verification programs, the
historical independent review, and the source and publication descriptions.
All 26 intake bodies were independently checked against their byte counts,
SHA-256 digests and native blob identifiers at intake.

## Exact claim under examination

Fix a noncircular ellipse with semiaxes a>b>0, a strictly nested nondegenerate
confocal elliptical caustic, and a billiard with even **least** period N>=4.
Primitive star polygons are included. The outer vertices are intersections of
successive tangents to the original ellipse. At either **original ellipse
focus**, form the antipedal by intersecting successive lines through the outer
vertices perpendicular to their vertex-minus-focus vectors. The asserted
invariant is the arithmetic mean of the resulting vertices. The proof also
asserts finite real intersections, a centroid on the focal axis, negation when
the focus is switched, and centroid zero for least period four.

These are hypotheses until the independent whole-mathematical review is
accepted. Opposite-focus negation does not assert that the centroid is on the
opposite side of the origin from its chosen focus. No signed-area centroid,
outer-locus focus, hyperbolic caustic, collapsed caustic or repeated odd
least-period orbit is covered. A separately stated circular case uses the
origin as focus. Repeating an already even least-period orbit preserves its
arithmetic vertex mean.

## Root's proof examination

The caustic normalization is a Euclidean similarity, not an anisotropic affine
change. Stachel's published Theorem 4.3 and equation (4.9), visually read on
printed p1614, supply the canonical parametrization, the unrestricted initial
phase, and the coprime turning-number parametrization. With caustic semiaxes
1,k', modulus k, and v=2K tau/N in (0,K), the original semiaxes are d/c,k'/c,
where s=sn(v), c=cn(v), d=dn(v). Their squared difference is k^2. The displayed
outer locus is obtained from the two named original tangents; its focus is
generally different from k and must not replace the original focus.

For the positive original focus, Root rederived the real determinant factor

    det(q_minus,q_plus) = 2 B s d dn(u) (a+k sn(u)) / D0,
    D0 = 1-k^2 s^2 sn(u)^2.

Its real factors are strictly positive: dn(u)>0, D0>0, and a+k sn(u)>=a-k>0.
Thus the proposed real construction has no phase exception, including stars
and N4. The opposite focus follows by central reflection.

Root checked the claimed meromorphic mechanism rather than treating the
finite controls as proof. For N>=6 the determinant's dn zeros have finite,
coincident endpoints and a simple zero; both Cramer numerators vanish. At a
common midpoint Jacobi pole the endpoints are regular and the displayed
determinant has a finite nonzero limit. At sn(u)=-a/k the common original
tangent passes through the original focus and is isotropic; both endpoint
bilinear squared norms vanish. The sn root is simple. The only possible
overlap of a focal root and an endpoint pole satisfies s^2 a^2=1, whose
admissible root is s^2=1/(1+k'). This gives v=K/2 and, under coprimality, N4.
The remaining endpoint poles have a simple determinant pole and at most
double numerator poles, so each antipedal coordinate has at most a simple
pole. Complex norms here are bilinear, with no complex conjugation.

At any endpoint pole of the full cyclic sum, the two singular outer vertices
are antipodal, with leading vectors L and -L. Reflection about the common
Jacobi pole gives finite neighbors Q and -Q. Root rederived the residue

    V(M,Q) = -(L dot L) J(Q-M) / det(L,Q-M),
    J(x,y)=(-y,x).

It satisfies L dot V=L dot L and (Q-M) dot V=0. The four distinct incident
edges for N>=6 cancel by
V(M,Q)+V(M,-Q)-V(-M,Q)-V(-M,-Q)=0. The previous local determinant analysis is
needed to make each residue denominator nonzero. Cancellation of all simple
poles on the common compact torus gives constancy. Focal-axis reflection
reverses vertex order but leaves the unordered line intersection unchanged;
the constant therefore lies on that axis. Central reflection switches the
focus and negates it. The submitted proof's separate rectangle/support
calculation handles N4, where the generic singularity classification overlaps.

This examination has not yet found an analytic defect. It is preliminary;
independent derivations and a fresh whole-proof adversary remain required.

## Exact boundary falsification

Root independently constructed two physical least-period-three billiards on
the fixed ellipse x^2/8+y^2/3=1 with confocal caustic parameter lambda=72/25.
The caustic's squared semiaxes are 128/25 and 3/25, so it is strictly nested
and nondegenerate. The fixed original focus is M=(sqrt(5),0).

The first triangle is

    (2sqrt(2),0), (-8sqrt(2)/5,3sqrt(3)/5),
    (-8sqrt(2)/5,-3sqrt(3)/5).

The second triangle is

    (0,sqrt(3)), (8sqrt(3)/5,-sqrt(3)/5),
    (-8sqrt(3)/5,-sqrt(3)/5).

All three original vertices are distinct in each case. For every edge the
checker proves exact caustic tangency at an interior contact point, and for
every vertex it proves the normalized physical specular-reflection equation.
It directly intersects the original tangents and then the named focal
antipedal lines. All determinants are exactly nonzero. The two resulting
vertex means are, respectively,

    (3sqrt(5)+5sqrt(2), 0),
    (3sqrt(5), -10sqrt(3)/3).

Their exact difference is (5sqrt(2),10sqrt(3)/3). Traversing each triangle
twice produces six listed antipedal vertices with the same mean as its
triangle. Consequently the extension to an arbitrary even **listed** vertex
count is false. This is a boundary counterexample, not a counterexample to
the submitted even least-period theorem.

`ROOT_ODD_REPEAT_BOUNDARY.py` passed 159 exact SymPy assertions under
SymPy1.14.0 and Python3.14.6 with optimization disabled. It imports only the
mathematical library and no submitted or prior-case helper. Its full exact
coordinates, line determinants, checks and source digest are recorded in
`ROOT_ODD_REPEAT_BOUNDARY.json`.

## Primary-source qualification and remaining gaps

Root visually inspected the pinned arXiv v11 Table5 on printed p7 and the
published Table5 on printed p348. Both identify k407 as the outer antipedal
vertex-centroid invariant at the original foci, with the period column saying
even. Neither table literally says least or primitive. Section3.5 provides
the construction and distinguishes vertex and signed-area centroids.
The even least-period interpretation is an adopted genuine-period convention,
not a word quoted from those tables. The new exact boundary witness makes this
qualification necessary in every current claim of source resolution. Historical
claims of a complete source-target match must remain historical and be
superseded by an explicit current qualification.

Independent families remain separate: physical Cartesian geometry, an elliptic
analytic derivation, and input/source/reproduction authentication. No preliminary
family report is a Root acceptance. After their full audits and a fresh whole
mathematical review pass, a separate in-depth priority audit is still required.
No novelty clearance, preprint readiness, DOI, tracker row, merge, closure or PR
metadata change is authorized by this research note.

Checkpoint 2026-10-12: intake100%; mathematical verification35%; priority0%;
overall case workflow10%. These are subjective progress estimates, not evidence
of correctness. Strongest fully checkable new result is the exact repeated-odd
boundary counterexample; the all-even-least-period theorem remains under audit.
