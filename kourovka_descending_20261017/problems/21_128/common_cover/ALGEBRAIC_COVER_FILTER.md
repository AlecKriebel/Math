# Candidate bounded theorem: no common finite étale algebraic cover

Prepared 2026-10-24. Full Kourovka21.128 completion estimate: **8%**.
This is a candidate partial result awaiting a fresh adversarial review. It is
**not a solution of21.128** and has no asserted priority.

Let `U_T = P^3_C \ union(H in A_T) P(H)` be the projectivized complement of
the complexified real reflection arrangement of type T, for T=F4,H4. The
precise claim is:

> There is no connected smooth complex algebraic variety Y with finite étale
> surjective algebraic morphisms Y→U_F4 and Y→U_H4.

The adjectives **algebraic** and the requirement of a **single Y as an
algebraic variety** are essential. Abstract commensurability gives finite
covers of the two complements with isomorphic fundamental groups, not a
common algebraic variety or an algebraic isomorphism of those covers. No
rigidity theorem filling that gap is known here. In particular this claim
does not imply that the Artin groups are noncommensurable.

## 1. The two cover-scaling quantities

For a smooth complex quasi-projective variety U, define its log canonical
volume as `vol(K_X+D)`, where X is a smooth projective SNC compactification
with reduced boundary D. This is independent of the chosen SNC
compactification. If the log divisor is nef, this is its top intersection
number. A finite étale algebraic morphism V→U of degree e satisfies

    chi(V) = e chi(U),       logvol(V) = e logvol(U).

The Euler assertion is the standard finite covering Euler formula, also
following by lifting a finite cell decomposition. For completeness, the
log assertion uses normalization of X in the function field of V. In
characteristic zero the resulting finite cover is tamely ramified over the
SNC boundary. Locally it is toroidal (Abhyankar's lemma), with reduced
boundary E, and the logarithmic ramification formula is

    K_X' + E = f^*(K_X+D).

A toroidal resolution is log crepant for the reduced toroidal boundary.
Volumes of pullbacks by a finite degree-e morphism multiply by e. In the
present situation K_X+D is globally generated, so its pullback is nef and
the latter assertion follows directly from the projection formula for its
top self-intersection. This argument applies to every finite étale cover
of our two U, without presupposing that the cover is another arrangement
complement.

The usual log-volume independence also follows by taking a common SNC
resolution: any boundary blowup of a codimension-c center lying in r
boundary components contributes `(c-r)E` to the log divisor, an effective
exceptional divisor. Such exceptional additions do not change volume;
toroidal blowups have c=r and are log crepant. This paragraph is a standard
birational fact, not a new group invariant.

Primary arrangement source: J.Tevelev, *Compactifications of subvarieties of
tori*, Amer.J.Math.129(2007),1087–1104, arXiv math/0412329, Theorems1.4,1.5
and §4 (paragraph immediately before Example4.1 discussion ends).
Section4 explicitly allows the compactification BL obtained by blowing up
**all** partial projective intersections, identifies it as the maximal
nested-set compactification, and proves that its log divisor is globally
generated and is the pullback of the ample divisor of the visible-contour
log canonical model. Thus our log divisor is nef and big and its cube
really is the log canonical volume. Both reflection arrangements are
essential and connected, as can be seen from their connected irreducible
Coxeter diagrams. P.Hacking–S.Keel–J.Tevelev, *Compactification of the moduli
space of hyperplane arrangements*, §2 Theorem2.2, independently states
the log canonical model and its very ample log canonical divisor.

## 2. Explicit all-flat cube formula in projective dimension three

Take an essential connected arrangement of N planes in P³. Blow up every
intersection point P (rank-three flat), then every strict transform of
an intersection line L (rank-two flat), obtaining X with reduced total
boundary D. Distinct line centers are disjoint after all the points have
been blown up. Let m_P,m_L denote the numbers of arrangement planes
containing the indicated flat, and p_L the number of listed points on L.
Let H denote the hyperplane class. Initially `K_P³ + union planes = (N-4)H`.

Blowing up a point of multiplicity m_P changes the log divisor by
`(3-m_P)E_P`. Since E_P³=1 and the cross terms with a pulled-back divisor
vanish, the cube becomes

    (N-4)^3 + sum_P (3-m_P)^3.

For a transformed line L, its log-divisor degree at this stage is

    d_L = (N-4) + sum_{P on L}(3-m_P).

Its normal bundle degree is `nu_L=2-2p_L`: adjunction gives
`deg N_L = -K·L-2`, and every point blowup subtracts2 from `-K·L`.
Blowing up L changes the log divisor by `a_L E_L`, where a_L=2-m_L.
The intersection rules for a blowup of a smooth codimension-two center are

    (pi^*B)^2 E=0,   pi^*B E² = -B·L,   E³ = -deg N_L.

Consequently its cube correction is

    -3 a_L² d_L - a_L³ nu_L.

Adding these corrections for every line gives the final cube. This
includes multiplicity-two lines and ordinary normal-crossing points: their
coefficients can vanish or merely describe log-crepant blowups, so no
special exception is silently omitted. The calculation only uses the
explicit intersection lattice and its point-line incidences.

## 3. Exact input and independently checkable arithmetic

`compute_log_volume.py` uses standard-library Fraction arithmetic in
`Q(phi)`, phi²=phi+1. Equality, rank, root closure, flats, and incidence are
all exact; no floating-point test occurs. It outputs `log_volume_data.json`.

F4 normals, up to scalar, are the24 lines represented by

    e_i (4),  e_i ± e_j (12),  (±1,±1,±1,±1) (8 modulo sign).

H4 normals, up to scalar, are the60 lines represented by

    e_i (4),  (±1,±1,±1,±1) (8 modulo sign),
    even coordinate permutations of (0,±1,±phi,±(phi-1))
      (48 modulo sign).

The irrelevant conventional factor1/2 has been dropped. The program also
checks that reflection in each listed normal permutes the complete set,
finds a full-rank simple chain with squared angle cosines corresponding to
3,4,3 respectively5,3,3, and verifies that the simple reflections generate
the whole listed root-line set. Chain signs can be chosen consecutively
so all neighboring inner products are negative, since the diagram is a
tree. These certify the intended reflection systems.

Each pair gives a rank-two normal span via its six wedge coordinates.
Each independent triple gives a projective intersection point via its
four signed3×3 minors. Canonical normalization identifies duplicate spans.
Every closure is then checked again against all normals. A point lies on
a line exactly when the line's containing-plane set is a subset of the
point's containing-plane set. This covers every flat and incidence.

The resulting tables are:

|Type|N|Line multiplicities, counts|Point multiplicities, counts|log volume|
|---|---:|---|---|---:|
|F4|24|2:72;3:32;4:18|4:96;9:24|2496|
|H4|60|2:450;3:200;5:72|4:600;6:660;15:60|51660|

The Euler characteristic is computed from this very same lattice by
Möbius inversion, without assuming tabulated exponents. A plane has
Möbius value−1, a line has `mu_L=m_L−1`, and a point has

    mu_P = -1+m_P-sum_{L containing P}(m_L−1).

Additivity on projective flats gives

    chi(U) = 4−3N+2 sum_L mu_L + sum_P mu_P.

This yields chi(U_F4)=−240 and chi(U_H4)=−5040. Hence

    logvol(U_F4)/|chi(U_F4)| = 52/5,
    logvol(U_H4)/|chi(U_H4)| = 41/4.

These rational numbers differ by3/20. A common finite étale algebraic cover
would force them equal by Section1, proving the stated bounded theorem.

## 4. Positive-control checks

Run the code with `--type tests` for A4 and B4. It returns volumes61 and488
and Euler characteristics−6 and−48. The ratios agree as required by the
explicit degree-eight algebraic étale map U_B4→U_A4. In coordinates with
the fifth A4 configuration point fixed at0, this map is

    [x1:x2:x3:x4] -> [x1²:x2²:x3²:x4²].

The B4 complement has xi≠0, xi≠±xj, so the image avoids all A4 hyperplanes
yi=0 and yi=yj; the derivative is invertible on the torus, and after
projective scaling each target has2³ lifts. Thus this is a genuine known
commensurable-case control, not an assumption that all commensurable
arrangements admit such algebraic maps.

For rank-two arrangements the corresponding formula is simply
`deg(K_P¹+N points)=N−2`. For rank-three arrangements blow up all multiple
points and obtain `(N−3)²−sum_P(m_P−2)²`. The A3/B3 root arrangements give5
and20, compatible with the analogous degree-four squaring cover. These
dimension-boundary controls will be recorded in a separate check output.

## 5. Exact remaining research gap

No common finite-index subgroup or algebraic-cover construction has been
found. The inequality rules out an algebraic geometric route through a
common finite étale cover of the **given projective complements**. It does
not rule out other group models, topological covers, homotopy equivalences,
or finite-index group isomorphisms. Turning it into a negative answer to
21.128 would require a strong algebraic recognition/rigidity theorem that
is neither proved nor assumed here. That route is blocked at precisely
this gap, not promoted to a conjectural solution.

All computations were developed with extensive AI assistance. There has
been no independent human peer review. No publication upload is authorized
by this partial theorem alone under the project workflow.
