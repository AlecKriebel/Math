# A weighted circle-exchange reduction and proved partial classifications

## Status and scope

Problem 4500001 / AMR-044-0001. **The general arithmetic classification is not solved here.** The results below give an exact geometric coding, a terminating classification for rational pairs, several complete one-parameter classifications, and an explicit all-parameter periodic-cylinder certificate. The latter is an unbounded search characterization, not a terminating solution of Question 2. No novelty or current worldwide openness claim is made.

The table is the union of the right half-disc of radius R1 and the left half-disc of radius R2, with R1 > R2. Its two straight boundary segments lie on the y-axis. Rotating or reflecting the table makes this equivalent to the source's two-semicircle table. Fix 0 < r < R2 and put

    a = arccos(r/R1)/pi,  b = arccos(r/R2)/pi,  d = a-b.

Thus 0 < b < a < 1/2. If the radius labels are reversed, relabel before using these formulas. The equal-radius case is the ordinary circle and has period the reduced denominator of a=b when rational; otherwise all its orbits are nonperiodic. Zero-radius and grazing caustics are not included in the nondegenerate statements.

**Corner convention.** At a reflex corner the trajectory stops, and there is no periodic continuation assigned to it. At a convex right-angle corner we use the continuous nearby-orbit limit: reverse the velocity and count the event as two reflections. This is the convention explicitly described in Section 1 of [DR12]. If all corner collisions are instead excluded, remove the entire trajectories containing convex-corner contacts as well. Every remaining complete trajectory retains its collision period, but the deletion can split an oriented cylinder. All region formulas and oriented-cylinder counts below use the continuous convex-corner convention stated above; under strict exclusion the exceptional trajectories must be deleted and the component counts checked again. Such exceptional trajectories must not be reported as ordinary smooth-boundary periodic orbits.

A “period” always counts boundary reflections, including reflections on straight segments. It is not the number of caustic contacts or of circular-arc reflections.

The accompanying [mathematical audit](MATHEMATICAL_AUDIT.md) accepts the partial classifications under this continuous corner convention, conditional on the correction now applied above. [CORNER_CORRECTION.md](CORNER_CORRECTION.md) preserves the exact correction and its counterexample. This AI-assisted manuscript and audit are unrefereed; acceptance does not mean external human peer review, journal acceptance or formal proof-assistant certification.

## 1. The return map, derived from the billiard

Scale r to 1. At a caustic contact of polar angle theta, counterclockwise velocity is (-sin(theta),cos(theta)). Define

    theta0 = pi(1/2 - 2a + b).

Represent a counterclockwise contact by theta=theta0+2pi x and a clockwise contact by theta=-theta0-2pi x, with x on R/Z. Write epsilon=0 for counterclockwise and epsilon=1 for clockwise. The section is therefore two circles, not one circle with the direction forgotten.

Partition the x-circle at the three physical singular values

    A=(0,d),   B=(d,d+1/2),   C=(d+1/2,1).

Define, away from singular trajectories,

    F(x) = x+a+1/2 (mod 1),  x in A;
           x+b     (mod 1),  x in B;
           x+a     (mod 1),  x in C.

The full return map and reflection weight are

    T(x,epsilon) = (F(x), epsilon XOR 1_A(x)),
    w(x) = 1 + 1_A(x).

Branch B has one collision on R2. Branch C has one collision on R1. Branch A has one collision on R1 and one on a straight segment. This is a three-branch **circle** exchange; splitting at the mod-1 wrap and keeping the orientation recovers the interval permutations of [DR12, Section 7]. One printed translation in the inspected arXiv:1206.0163v1 lower-sign case has a sign error, isolated below; the geometric map here does not inherit that entry. It is not a three-interval exchange on an ordinary interval without an additional wrap cut.

### Geometric proof

The forward intersection of a tangent ray with the full circle Ri has polar angle theta+pi*rho_i. Hence its contact with the smaller left semicircle occurs precisely when

    pi/2 < theta+pi b < 3pi/2,

which is x in B. The following caustic contact is at theta+2pi b, giving F=x+b and unchanged direction.

For a right-semicircle reflection the corresponding full-circle next contact would be at theta+2pi a. In C the actual segment reaches that contact without crossing a straight boundary segment, so F=x+a and direction is unchanged. In A it has one circle reflection and one upper straight-segment reflection: the circle comes first when x<d/2 and the straight segment comes first when x>d/2. A y-axis reflection sends the contact normal angle to pi-theta and reverses the angular direction. Composing it with the circle reflection in either of these two orders gives the next contact angle pi-theta-2pi a. In the clockwise coordinate this equals x+a-1/2 modulo 1, yielding the A formula. Reflection in the x-axis gives the clockwise case identically. The entry and exit inequalities are exactly x=0,d,d+1/2 at the three reflex-corner separatrices. A convex corner occurs at x=d/2 on the A branch; the two reflections there have the same limiting map and total weight two.

Between consecutive caustic contacts there is exactly the circular reflection specified above and, only on A, one straight reflection. Conversely, the construction from a contact and direction gives one and only one billiard segment sequence up to its next contact. Every complete regular trajectory meets the section repeatedly. Thus this coding is both sufficient and necessary, with no lost regular trajectories and no extra trajectories introduced by choosing a half-open extension at the corners.

For completeness, F is bijective as a circle exchange. The image of B is the circular interval [a,a+1/2), the image of A follows it from a+1/2 for length d, and the image of C fills the remaining length 1/2-d and ends at a. Their interiors are disjoint and together cover the circle.

### A printed source-entry discrepancy, independently isolated

In the inspected arXiv:1206.0163v1 [DR12, p.19], in the case 1/2+b-2a<0, the second negative interval is

    -1/2-a <= xi < a-b-1.

The displayed translation there is xi+a-1/2. It must be **xi+a+1/2** for the geometric coding, and this correction also agrees with the permutation printed immediately below it. The sign is visible in the original PDF, so this is not an extraction/OCR artifact.

An exact witness is a=3/10, b=1/14. The printed map sends both xi=-79/100 and xi=21/100 to -99/100, although these are different interior points. It therefore fails injectivity. Their actual return coordinates are respectively +1/100 and -99/100: both reflect once on a straight edge, so their directions both flip. The corrected entry fills the missing image interval (0,1/35) instead of duplicating (-1,-34/35). The geometric derivation above proves the correction; the audit records independent ray-tracing corroboration. This discrepancy is asserted only for that inspected v1 location, with no claim about later versions or the journal publication. All three source examples requested in the 2015 paper lie in the other regime, so this issue would escape example-only testing.

### Collision-period conversion

Let x have least F-period q, and let k be the number of A visits in that primitive cycle. The least oriented return is q if k is even, and 2q if k is odd. Its **least billiard collision period** is therefore

    P = (q+k) if k is even;  P = 2(q+k) if k is odd.                 (1)

A smaller billiard period would return a caustic contact with its direction earlier, contradicting the least oriented return. This proves minimality of P, rather than only producing a closing polygon.

Time reversal on the section is

    J(x,epsilon) = (2a-b-1/2-x mod 1, 1-epsilon).

It reverses T. Phase cylinders related by J have the same projected boundary region; a cylinder can also be J-invariant. This distinction explains why the sources describe two boundary regions while some examples have three or four oriented phase components.

## 2. Complete finite arithmetic classification when a and b are rational

Let L be the least common multiple of 2 and the reduced denominators of a,b. Put A0=La, B0=Lb, D=A0-B0. For j=0,...,L-1 form the permutation

    p(j) = j+A0+L/2 mod L,  j<D;
           j+B0       mod L,  D<=j<D+L/2;
           j+A0       mod L,  j>=D+L/2.                         (2)

For every 0<t<1, F sends (j+t)/L to (p(j)+t)/L. Thus every regular orbit is periodic. For each cycle of p, count q cells and k cells with j<D, and apply (1). This is an exact terminating criterion for **all possible least collision periods**, not a sample of initial conditions. In particular q<=L and P<=4L. Regular auxiliary-grid points obey the same map; actual corner separatrices are excluded as specified above.

### Exact maximal region decomposition

The following finite construction removes auxiliary-grid overcounting.

1. On the grid endpoints j/L, the right-sided map is p(j)/L and the left-sided map is (p(j-1)+1 mod L)/L.
2. Form the finite undirected graph given by both maps and their inverse edges. Take the closure S of the three true breakpoints 0,D,D+L/2 in this graph. These are exactly the grid endpoints whose one-sided trajectory meets a reflex corner in forward or backward time.
3. Start with the 2L signed open grid cells (j,epsilon). Join a cell to (p(j),epsilon XOR [j<D]). Also join cells adjacent across j/L when j is not in S, keeping epsilon unchanged.
4. The connected components are the maximal regular oriented flow cylinders. Each component's collision period is obtained from any of its signed permutation cycles; it is constant on the component. Apply J to pair components. The J-orbits are the maximal boundary regions.

Why this is complete: deleting the finite singular set S leaves the genuine open intervals of the section, and the return map permutes them by translations with constant reflection data. The only remaining identifications needed to build the flow cylinders are return-map identifications and passage across regular auxiliary cuts. Both are exactly the graph edges in step 3. At a smooth boundary point the two caustic-compatible trajectories are time reverses, so step 4 introduces neither missing nor overlapping open boundary regions.

### Converting the certified section intervals into actual boundary arcs

The region data are not limited to abstract section labels. Here is an explicit projection recipe. Restore the caustic radius r and, on the counterclockwise sheet, put theta=theta0+2pi*x. Angles below are taken modulo 2pi.

- B: the collision is on the left semicircle R2 at polar angle theta+pi*b.
- C: the collision is on the right semicircle R1 at polar angle theta+pi*a.
- A with x<d/2: first the R1 point of angle theta+pi*a, then the upper straight point (0,r/sin(theta+2pi*a)).
- A with x>d/2: first the upper straight point (0,r/sin(theta)), then the R1 point of angle pi-theta-pi*a.
- At x=d/2 these are the same convex corner, counted twice under the stated convention.

The clockwise formulas are their reflections in the x-axis. Apply these formulas to every interval of a phase component and combine its time-reversed partner. This gives precisely its open bouncing-point arcs on the physical boundary. Split an interval at d/2 only for this projection formula; that is a regular limiting continuation, not an extra dynamical region. For rational a,b all arc endpoints have rational multiples of pi as angles, and the straight-edge endpoints are the displayed exact trigonometric expressions. The finite graph and this recipe therefore determine actual regions as well as their periods.

### Required source examples, with exact finite derivations

The following are explicit substitutions in (2) and the singular-strip construction above. They expand the same three examples already accepted in Section 5 of the mathematical audit; no new parameter family or region-count claim is introduced. All interval endpoints below are numerators divided by L. A list of starts is a cyclic list, with the last returning to the first. A strip of width h denotes the whole open interval (j/L,(j+h)/L), so these calculations prove statements for every transverse coordinate, not sampled points.

For the singular-set calculations, the right images of the three true breakpoints equal their left images as a set: {a,a+1/2,2a-b+1/2} modulo 1. At all other endpoints the two maps agree. Therefore the union of their right-permutation cycles is already closed under both one-sided maps and their inverses, and is exactly S. This is also the audit's independent justification of the finite singular closure.

**a=1/3, b=1/4.** Here L=12, A0=4, B0=3, D=1. The cell shifts are +10 on j=0, +3 on j=1,...,6, and +4 on j=7,...,11, all modulo 12. The complete permutation is the disjoint union of

    (0,10,2,5,8),       word A C B B C;
    (1,4,7,11,3,6,9), word B B C C B B C.

Substitution verifies each arrow and the return; the two lists cover 0,...,11 without repetition. The breakpoints 0,1,7 meet both cycles, so S is the full grid and every maximal strip has width 1. The first strip cycle has (q,k)=(5,1), and therefore one orientation-doubled cylinder with least collision period 12. It has three outer and two inner reflections per base cycle; doubling gives six outer, four inner and two straight reflections. The second cycle has (q,k)=(7,0), hence two oriented cylinders of period 7. Reversal acts on cell indices by j -> 10-j modulo 12, with orientation flipped. It preserves each listed base cycle, pairs the two period-7 lifts and preserves the single period-12 lift. Thus there are exactly three oriented cylinders and two boundary regions, of periods 12 and 7.

**a=1/4, b=1/6.** Now L=12, A0=3, B0=2, D=1. The cell shifts are +9 on j=0, +2 on j=1,...,6, and +3 on j=7,...,11. The auxiliary-cell cycles are

    (0,9);
    (1,3,5,7,10);
    (2,4,6,8,11).

The true breakpoints 0,1,7 generate S={0,1,3,5,7,9,10}/12. Thus the maximal strips have starts and widths

    starts 0,1,3,5,7,9,10;
    widths 1,2,2,2,2,1,2.

Their return cycles are (0,9), with word AC and width 1, and (1,3,5,7,10), with word BBBCC and width 2. Each image interval has the displayed successor start and unchanged width. These seven strips exhaust the complement of S. In particular the two auxiliary 5-cycles are joined across regular cuts into the same width-2 strip cycle. The AC cycle has one A visit and gives one period-6 oriented cylinder; BBBCC gives two period-5 cylinders. Reversal sends an interval (j/12,(j+h)/12) to the interval with start -2-j-h modulo 12 and the same width, with orientation flipped. It preserves each base strip cycle, pairs the period-5 lifts and preserves the period-6 lift. Hence the exact counts are three oriented cylinders and two boundary regions, of periods 6 and 5.

**a=1/3, b=1/5.** Here L=30, A0=10, B0=6, D=4. The shifts are +25 on j=0,...,3, +6 on j=4,...,18, and +10 on j=19,...,29. The full cell cycles are

    (0,25,5,11,17,23,3,28,8,14,20),
    (1,26,6,12,18,24,4,10,16,22,2,27,7,13,19,29,9,15,21).

Every arrow follows by the three shifts, and the lists are disjoint and cover all 30 indices. The true breakpoints 0,4,19 meet both cycles, so S is the full grid and every maximal strip has width 1. Their branch words are respectively

    A C B B B C A C B B C;
    A C B B B C B B B C A C B B C C B B C.

Thus (q,k)=(11,2) and (19,2). Each cycle has two orientation lifts, of least collision periods 13 and 21 respectively. Reversal acts by j -> 28-j modulo 30 and flips orientation. Each base cycle is invariant under this action. To see that its two lifts are paired, J takes the start 0 to start 28 in the first cycle and the start 1 to start 27 in the second. Forward travel from 0 to 28, or from 1 to 27, crosses exactly two A strips, so it preserves the initial sheet, whereas J flips it. Therefore J interchanges the two lifts of each cycle. There are exactly four oriented cylinders and two boundary regions, of periods 13 and 21.

These finite derivations specify every maximal strip and its return, and the preceding projection formulas recover its physical bouncing-point arcs. They require no omitted program, generated dataset or verification output. All these counts use the continuous convex-corner convention.

## 3. The whole line a=1/4: an explicit mixed decomposition

Let 0<b<1/4 and d=1/4-b. The two intervals

    U=(0,d) union (3/4,1-b)

are interchanged by F. Every base orbit there has q=2 and k=1. Consequently U lifts to one period-6 phase cylinder and one period-6 boundary region.

The complementary intervals, with the relevant endpoints removed, are

    V=(d,3/4) union (1-b,1).

No point in V visits A. Collapse the two omitted gaps with the coordinate

    h(x)=x-d,     d<x<3/4;
         x-2d,    1-b<x<1.

Its target is a circle of length ell=1/2+2b, with one harmless cut inside it. Direct substitution gives

    h(F(x)) = h(x)+b mod ell.                                  (3)

This proves the full complementary dynamics, not merely absence of short periodic orbits.

- If b is irrational, b/ell is irrational. Every complete regular orbit in V is nonperiodic and dense in V on its orientation sheet. The two sheets are time reverses and project to one nonperiodic boundary region.
- If b=u/v in lowest terms, every regular orbit in V has least collision period

    (v+4u)/gcd(2u,v).

There are still two boundary regions: U of period 6 and V of the displayed period. They may have equal periods for particular rational b, but remain separated by the reflex-corner separatrices.

In particular b=1/sqrt(30) is irrational and lies between 0 and 1/4. This exactly proves the source's coexistence of period 6 with nonperiodic orbits. For b=1/6, (3) gives period 5, as required.

## 4. Every rational a with irrational b: exact periodicity threshold

Let a=p/q be reduced, 0<a<1/2, and let b be irrational with 0<b<a. Write

    g=gcd(q,2), Q=q/g, h0=1/(2Q).

There is a regular periodic trajectory **if and only if b<h0**. If so, there is exactly one periodic boundary region and all its trajectories have least collision period

    q+2p.                                                       (4)

All remaining complete regular trajectories are nonperiodic. This result identifies the entire periodic set; it does not, by itself, count all minimal components in the nonperiodic complement for an arbitrary p/q.

### Proof

If a complete oriented orbit closes with m outer and n inner reflections, the map gives

    m*a+n*b in Z.                                               (5)

The straight-reflection count is even in a closed oriented orbit, which removes the half-integer contribution. As a is rational and b irrational, (5) forces n=0. Thus any periodic trajectory must avoid B completely.

For an outer-only orbit put y=x mod (1/2). For each y there is precisely one outer branch state:

    x=y       when 0<y<d,
    x=y+1/2   when d<y<1/2.

Its next reduced coordinate is y+a mod 1/2. The next full state is again outer precisely when y avoids the hole H=[1/2-b,1/2) (with boundary convention understood). Therefore the outer-only set is the survivor of the rational rotation by a on a circle of length 1/2, avoiding H.

This rotation has order Q; its points are spaced by h0. The hole and its Q translates cover the circle if b>=h0, with the equality case leaving only corner endpoints. If b<h0, the complete regular survivor consists of Q intervals

    (j*h0, (j+1)*h0-b), j=0,...,Q-1.

They form one base return cycle. In it k=2p/g visits lie in A, and its contact period is Q. Formula (1) gives q+2p in both parity cases: for odd q, k=2p is even; for even q, k=p is odd. The orientation lift yields one phase cylinder in the even-q case and two time-reversed cylinders in the odd-q case. Thus there is one periodic boundary region. No other periodic trajectories are possible by (5).

For comparison, if a is irrational and b rational, there are **no periodic regular trajectories**. Equation (5) would force m=0, while an orbit cannot remain in B forever: B translates strictly forward by b until it leaves B.

## 5. A whole irrational-capable fully periodic band

Suppose

    a+b=1/2,  1/6<b<1/4,
    d=1/2-2b, e=3b-1/2.

Both d and e are positive. There are exactly two boundary regions, of least collision periods 14 and 4, even when both a and b are irrational.

The interval (0,d) has base itinerary A C B B B C. Its six successive image intervals start at

    0, 1-b, d, 1/2-b, 1/2, 1/2+b

and each has length d. Its least base period is 6 and it visits A once, so its collision period is 14.

The interval (2d,2d+e) has itinerary B B C C. Its successive image intervals start at

    2d, 1-3b, 1-2b, 3/2-3b

and each has length e. Its least contact and collision periods are 4. The ten intervals just listed have disjoint interiors and total length 6d+4e=1; in order, their types are

    P, P, Q, P, Q, P, Q, P, P, Q.

Every consecutive endpoint agrees exactly. Consequently they cover the entire section except finitely many corner separatrices. None of the intermediate translations is an integer, which proves the stated periods are least periods. This is a complete decomposition on the open band, not a conclusion drawn from finite tests.

The earlier source's values a=(5-sqrt(5))/10, b=sqrt(5)/10 lie in this band and give the advertised periods 14 and 4. In particular “irrational rotation numbers imply no periodic billiards” would be false.

## 6. A generic nonperiodicity/minimality result and a stronger obstruction

If 1,a,b are linearly independent over Q, no regular orbit is periodic: (5) would be a nontrivial relation.

In fact there is no saddle connection between reflex corners. A physical singular endpoint has the form 0 or a-b+c/2. If an endpoint reaches another after m outer, n inner and k straight reflections, their difference is

    m*a+n*b+k/2 modulo 1.

Q-independence would require (m,n) to equal (0,0), (1,-1), or (-1,1), depending on the endpoints. None is possible for a nonempty path with m,n>=0. Thus the flow has no saddle connections. Applying the measured-foliation decomposition of [DR12, Theorem 5.4] to this connected genus-3 leaf gives one minimal component: every complete regular trajectory is dense in the leaf, and its bouncing points are dense in the boundary. This use of an existing structural theorem is explicit; no genus-one assumption is made.

A useful necessary inequality strengthens (5). Let

    M=ceil(1/(2b)).

An orbit can have at most M consecutive B visits, because B has length 1/2 and each such step increases x by b without wrap. A periodic orbit must have m>=1 outer reflections, and grouping its B visits into runs gives

    n <= M*m.                                                   (6)

This disproves periodicity in the later-section counterexample of [DR12]:

    a=5/11+1/(22pi), b=5/11-1/(220pi).

Although a+10b=5, irrationality of 1/pi implies that any relation (5) has n=10m. Here 1/4<b<1/2, so M=2; (6) contradicts n=10m for m>=1. This is an all-period proof of nonperiodicity, independent of any finite orbit cutoff. The source additionally proves minimality by its modified Keane criterion in Proposition 8.5.

## 7. An exact certificate for any periodic cylinder, with an explicit limitation

For arbitrary parameters one can enumerate words in A,B,C and solve only linear equalities and strict inequalities. This supplies exact verifiable candidate certificates, but no uniform finite stopping criterion.

Let w0,...,w(q-1) be a word. Set branch intervals I_A=(0,d), I_B=(d,d+1/2), I_C=(d+1/2,1) and shifts

    u_A=a+1/2, u_B=b, u_C=a.

Choose integers N0=0,N1,...,Nq and put

    v_j = sum_{i<j} u_(w_i) - N_j.

Require v_q=0. The set of initial contacts realizing the word is exactly

    I = (0,1) intersect intersection_{0<=j<q} (I_(w_j)-v_j).

It is nonempty exactly when its largest lower endpoint is less than its smallest upper endpoint. These endpoints are integer-affine expressions in a,b and 1/2. No geometric search is left inside this test. Membership in each translated interval automatically enforces the correct mod-1 wrap. Integers Nj can be bounded by 0<=Nj<=j, since all unwrapped branch increments lie between 0 and 1.

If no proper prefix has v_j=0, the base period is exactly q; otherwise reduce to the first returning prefix. Count A visits and use (1). Every complete regular periodic orbit is captured: its finite orbit avoids the three true breakpoints, so a neighborhood has the same word and the above interval has positive length. Conversely every positive-length certificate realizes a regular periodic family after deletion of any exceptional corner orbits.

Thus the union of these certified intervals is exactly the periodic set, and its complement among complete regular trajectories is nonperiodic. However, **an unbounded union is not a finite arithmetic decomposition algorithm**. In particular, the nonappearance of another certificate in a finite search does not establish that no further periodic or minimal component exists.

## 8. Sharp remaining gap and scope exclusions

The unresolved part is a terminating, all-parameter arithmetic method to count and locate the periodic and nonperiodic regions for the remaining irrational, rationally dependent pairs. Typical unresolved inputs have a rational relation involving positive multiples of both a and b, outside the explicit band and other classifications proved above. There are also missing minimal-region counts on general mixed rational/irrational lines, even where Section 4 completely identifies their periodic set. A necessary relation alone is insufficient, as Section 6 proves. The finite rational algorithm does not extend merely by replacing rational arithmetic with floating-point arithmetic; an irrational endpoint orbit need not close.

The cylinder certificate in Section 7 is complete as a logical characterization of periodic points, but no general stopping bound, finite minimal-component certificate, or simplified arithmetic criterion is proved here. The general problem therefore remains **partial**.

The two-semicircle geometry is essential to the three-branch map and weight. No extension to arbitrary finite-arc/radial tables (Question 3) is claimed. [DR12, Theorem 7.1] establishes dependence on rotation numbers for the analogous two-half-confocal-ellipse table, but this note does not independently reconstruct all its corner conventions or transplant the circular normalization to a different confocal parametrization. The authored proof claims above are for the stated circular table.

## References

[DR15] Vladimir Dragović and Milena Radnović, “Periods of Pseudo-Integrable Billiards,” Arnold Mathematical Journal 1 (2015), 69–73. DOI https://doi.org/10.1007/s40598-014-0004-0 . Full five-page source, especially Questions 1–3, Examples 1–3, and Remarks 1–4.

[DR12] Vladimir Dragović and Milena Radnović, “Pseudo-integrable billiards and arithmetic dynamics,” arXiv:1206.0163v1, 1 June 2012, https://arxiv.org/abs/1206.0163v1 . Full 24-page retrieved version, especially Sections 1, 3–8; all later sections were read. Public PDF: https://arxiv.org/pdf/1206.0163v1 . The cited version is the retrieved 2012 manuscript, not an asserted bibliographic identity with the later journal pagination.
