# Parallel short trajectories: literal obstruction and a parity-selected signed law

Current mathematical repair v2. This is a reviewable proof artifact, not a declaration of publication readiness or historical novelty. Original PR191 head a2791bdd3f7ecd5694aeeeb5dffb21964a5639fe, effort2/5, and all16 original files remain preserved unchanged under original_submission/files/. The original candidate is not overwritten by this assembly.

There are two explicitly different conclusions. First, the immutable imported global conjunction, including its bare A0 iff beta−alpha=2pi/n condition, is false for every n>=5. Second, the parity-selected type K_PS defined below obeys the all-admissible signed law, with first-vertex existence, for every n>=3. This proves a supported completion of the source convention and its generic-sector law, rather than turning the inconsistent conjunction into a positive theorem. The literal direct-diagonal counterexamples are outside/on the boundary of the source's preceding open fundamental sectors. No counterexample to that restricted generic conjecture is asserted.

Fuchs's published title is Billiard Trajectories in Regular Polygons and Geodesics on Regular Polyhedra, Arnold Mathematical Journal7(2021),493–517, DOI10.1007/s40598-020-00170-8; it appeared online7January2021. The immutable upstream target's differing title and2020 metadata are retained as historical imported metadata. The actual full source body, Figures8/9 and parity paragraph are the mathematical provenance. No author-authenticated erratum or uniquely forced source intent is claimed.

The following source-calibration/counterexample derivation was independently written by the literal/type adversarial family before any sibling report or old opinion. The clean all-direction proof was written by the independent geometric family; its common-label construction credits the submitted candidate. Root independently checked both, including the direct double-surface shear and finite-length descent. Classical polygon surfaces/shears and affine geometry are not claimed as new. The original Veech body is not a load-bearing unread import in the direct proof. Priority is a subsequent separate audit, and no present openness, firstness, awareness or independent chronology is certified here. AI tools were used extensively; this work is unrefereed and has not undergone conventional human peer review.

## Part I. Exact target and convention repair

## 1. Geometric calibration from the primary source

Let (n\geq3), (N=n-2), and (d=N\pi/n). Put (X_0=O=(0,0)), (X_{n-1}=(1,0)), and list the other regular-polygon vertices clockwise above this edge, as in Fuchs Figure 9. The outgoing oriented side at (O) points along the positive horizontal axis. At the terminal vertex the interior angle shown in Figure 8 is (\pi-\beta), rather than (\beta). Consequently

\[
0\leq\alpha\leq d,\qquad 2\pi/n\leq\beta\leq\pi.
\]

For the direct chord (X_0X_j), (1\leq j\leq n-1), the inscribed-angle theorem gives

\[
\alpha_j=(n-1-j)\pi/n,
\qquad \pi-\beta_j=(j-1)\pi/n.
\tag{A1}
\]

In particular,

\[
\beta_j-\alpha_j=2\pi/n
\quad\text{for every direct chord.}
\tag{A2}
\]

Fuchs Figure 9 assigns this chord (A_{j-1}), with (A_N=A_0). For a genuine diagonal, strict convexity puts its open segment strictly inside the polygon. It is therefore a one-segment short trajectory with no intermediate vertex, side encounter, or ambiguity about its first endpoint.

## 2. Universal counterexample to the unqualified imported conjunction

The authenticated imported target says types are unique residues modulo (N) and, without a parity or generic-direction qualification, characterizes (A_0) by (\beta-\alpha=2\pi/n). It then imposes the signed angle rule for all admissible literal angles. These requirements cannot all hold.

For every (n\geq5), take (j=n-2) in (A1). Then

\[
\alpha=\pi/n,\quad \beta=3\pi/n,
\quad \text{so the bare shorthand gives } k=0.
\]

Choose (\ell=2), (\varepsilon=-1). This is permitted for both parities of (n), including the even-(\ell) requirement when (n) is even. The transformed literal slope is

\[
\alpha'=2\pi/n-\alpha=\pi/n=\alpha.
\]

It is the same first-vertex chord, whereas the requested type is (A_{-2}). Since (N\geq3), (0\not\equiv-2\pmod N). This contradicts uniqueness. There is no reduction of an angle modulo (\pi) or (2\pi) in this argument.

The raw printed four triples also fail to supply the requested label. At this chord the difference rows give (A_0), while the sum rows give (A_{N-1}). The demanded residue (N-2) is neither of these when (N\geq3).

There is a version using distinct interior chords, so the obstruction does not require counting a trajectory as parallel to itself. Start at the same chord (X_0X_{n-2}). For odd (n\geq5), choose (\varepsilon=1,\ell=1). The new chord is (X_0X_{n-3}), with endpoint angles (2\pi/n,4\pi/n). For even (n\geq6), choose (\varepsilon=1,\ell=2). The new chord is (X_0X_{n-4}), with angles (3\pi/n,5\pi/n). All of these are strict interior diagonals. Equation (A2) gives the bare label (A_0) to both chords, whereas the rule asks for (A_{-1}) or (A_{-2}), respectively. Neither requested residue equals zero or the other raw printed label of the target chord.

This is an analytic all-(n\geq5) refutation of the **unrestricted imported conjunction**. The source's preceding enumeration takes the initial angle in (0<\alpha<\pi/(2n)) for odd (n), or (0<\alpha<\pi/n) for even (n). Our starting angle (\pi/n) is outside the former and at the endpoint of the latter. Thus this family does **not** refute a conjecture restricted to those open generic sectors. A source-convention repair, rather than a generic-sector counterexample, is needed.

## 3. Exact parity-selected completion of Definition 2.1

For a trajectory of (q) segments, select the sum relation when (q) is odd and the difference relation when (q) is even. This is the sign convention in the paragraph immediately before Definition 2.1. Put (a=n\alpha/\pi\), (b=n\beta/\pi\). Then (0\leq a\leq N\), (2\leq b\leq n\), and the intended type is

\[
\begin{array}{ll}
q\text{ odd}:&s=(a+b)/2\in\mathbb Z,\quad k=n-1-s\pmod N,\\
q\text{ even}:&s=(b-a)/2\in\mathbb Z,\quad k=s-1\pmod N.
\end{array}
\tag{A3}
\]

Here is a full algebraic verification, rather than a numerical assertion that the printed inequalities agree. In the odd-segment case (1\leq s\leq n-1), so take the integer representative (k=n-1-s\in[0,N]). The lower-(k) sum row's restriction on (a) is (a\geq2s-n), precisely the already required (b\leq n). The upper-(k) sum row requires (a\leq2s-2), precisely (b\geq2). For even (n=2m) the ranges meet at (k=m-1) and give the same type; for odd (n=2m+1) they meet between (k=m-1) and (k=m).

In the even-segment case, (s\geq1) yields (k=s-1), and the lower-(k) difference row again reduces to (a\leq n-2s\), or (b\leq n). For (s\leq0) take (k=s-1+N); the upper-(k) difference row reduces to (a\geq2-2s\), or (b\geq2). The ranges of (s) implied by the endpoint-angle bounds put these representatives exactly in the corresponding printed (k)-ranges. Thus there is a unique residue for each selected parity.

The representative (k=N\equiv0) is needed for the one-segment horizontal side, (a=0,b=2,s=1). It is the explicit endpoint identification (A_{n-2}=A_0) in Figure 9. If the prose insists on representatives (0\leq k\leq n-3) **before** applying the printed inequalities, this side has no odd-segment row. Equation (A3) already handles it, but the endpoint representative must be stated when claiming literal equivalence to all printed inequalities.

For (A1), the one-segment formula gives (s=n-j) and (k=j-1), agreeing with Figure 9. In particular the counterexample chord's parity-selected type is (A_{N-1}), not (A_0), and its self-reflection gives (-k-2\equiv k\pmod N). The bare (A_0) characterization is therefore not globally valid for the repaired convention.



## Part II. All-direction proof of the explicit parity-selected law

# All-direction geometric reduction, independent derivation

UTC: 2026-10-15T04:23:08.453528+00:00

This is an audit proof, not a priority claim. It repairs a source-body dependency of the submitted argument and proves the signed-angle rule for the explicit label K_PS defined in Section 6. K_PS is the candidate's parity-selected reading; identification with a raw disjunction of angle branches or the authenticated target's bare A0 endpoint-angle shorthand is not proved here. The source-first assessment was sealed before reading the candidate. The common label and endpoint reflection below are credited to the candidate. The cylinder construction for the exact even double and the finite-length descent were derived during this audit; the odd cylinder formula also appears in Finster, already read before this derivation. No novelty claim is made. No sibling review was read before this derivation.

## 1. Exact surface, including the even families

Let rho=pi/n and N=n-2. Take two distinct labelled polygons P and Q=-P. Glue P side [v_j,v_(j+1)] to Q side [-v_j,-v_(j+1)] by translation z -> z-v_j-v_(j+1). This sends P_j to Q_(j+1) and P_(j+1) to Q_j. The increasing corner-successor cycle alternates P_j,Q_(j+1),P_(j+2),... . For odd n it has 2n corners and total angle 2N*pi. For even n it has two cycles of n corners and total angle N*pi each. Euler counts V-E+F are 1-n+2=3-n and 2-n+2=4-n, giving genera (n-1)/2 and (n-2)/2 respectively. These are the *two-polygon* surfaces throughout, not the smaller even opposite-edge quotient.

For n=0 mod4, the double surface is a connected unramified degree-two cover of the opposite-edge n-gon surface: each of its two vertex preimages has cone angle N*pi, equal to the base angle. The base genus is n/4 and Riemann-Hurwitz gives genus 2*(n/4)-1=(n-2)/2. For n=2 mod4, the base has two vertex points, each with half the double cone angle; the double cover is branched at both and gives genus 2*(n-2)/4=(n-2)/2. The direct gluing calculation, rather than a cover formula, is what is used below.

All vertex points remain marked, including when their angle is 2pi. Thus n=3 is a torus with one marked point, and n=4 a torus with two. For n=6 the double is genus two with two 4pi cone points; it is not a hexagon torus with unmarked ordinary vertices.

## 2. Explicit shear on the exact double, for every n>=3

For this paragraph use centered vertices

    v_j=(cos(2j*rho), sin(2j*rho)), j mod n.

The model direction is vertical. Write m=floor(n/2), and for 1<=j<=m put

    a_j=cos(2j*rho), b_j=cos(2(j-1)*rho),
    H_j=b_j-a_j>0,
    S_j=a_j+b_j,
    L_j=2[sin(2j*rho)+sin(2(j-1)*rho)].

The vertical lines through vertices divide P into the m open strips a_j<x<b_j. Q has the reflected strips -b_j<x<-a_j. A vertical ray crossing the upper edge of P's jth strip enters the lower edge of Q's reflected jth strip with x_Q=x_P-S_j. Crossing its upper edge then returns to P's lower edge with x restored. No other strip is entered. Therefore the two strips form a cylinder. This accounts for all interiors outside vertical saddle connections, exactly one cylinder per j, including the central strip for even n=2 mod4.

The vertical chord length in P is linear in x on this strip, with endpoint values 2 sin(2j*rho) and 2 sin(2(j-1)*rho). Q contributes the complementary linear value (replace x by S_j-x), so their sum is the constant L_j. The transverse width is H_j. Trigonometric subtraction and addition give

    H_j=2 sin((2j-1)*rho) sin(rho),
    L_j=4 sin((2j-1)*rho) cos(rho),
    L_j/H_j=2 cot(rho)=lambda.

All sines in H_j are positive in the stated range. In the even final strip sin(2m*rho)=0, but L_j remains positive for n>=3. In each cylinder use its flat coordinates x in (a_j,b_j), s mod L_j along the vertical direction. The twist

    (x,s) -> (x, s+lambda*(x-a_j))

has one common derivative [[1,0],[lambda,1]] in the original translation charts. It fixes each cylinder boundary pointwise, since the added shift is 0 or L_j. Consequently all twists glue to a global orientation-preserving affine automorphism T, fixing the marked vertex set and every vertical boundary saddle connection. This proves the required shear exists on the double even surfaces directly; no lifting of a shear from a smaller quotient is assumed.

For odd n, rotation by rho exchanges P and Q and respects the side pairing; for even n rotation by 2rho preserves both polygons and their pairing. Thus these rotations are actual affine isometries of the exact surface.

To calibrate this temporary orientation to the source: rotate the centered configuration by -pi/2-rho and translate its v_0 to O. Then centered v_j is the source clockwise vertex P_(-j), and the side v_0 v_1 is the source lower horizontal side O P_(n-1). The temporary vertical direction pi/2 becomes source direction -rho, i.e. h=-1 in theta=h*pi/n. The second even terminal direction, separated by +/-rho, becomes source direction 0 or -2rho. Thus all terminal directions used in the reduction belong to the model family of Section 6, even when they lie outside O's initial sector as physical directions on the surface.

## 3. Finiteness of bounded-length saddle connections

A compact surface made from finitely many Euclidean polygons with cone angles at least 2pi has finitely many saddle connections of length at most B for every B. Retain marked ordinary points in the finite endpoint set.

Here are the geometric details behind this often-used fact. Give the unpunctured surface its complete length metric and its simply connected metric cover the lifted metric. Completeness lifts; locally the cover is a Euclidean disk or a finite-angle Euclidean cone. Complete locally compact length spaces are proper (the length-space Hopf-Rinow argument: compact small balls and completeness let one extend compactness of concentric balls). Deck transformations act properly discontinuously, hence the lifts of the finite endpoint set in a bounded closed ball are finite. Two locally geodesic segments with the same lifted endpoints coincide: otherwise take an innermost disk bigon in the simply connected surface. Its interior cone curvatures are nonpositive, all non-endpoint geodesic boundary turns are nonpositive, and its two endpoint exterior turns have sum strictly below 2pi for a nondegenerate bigon. Gauss-Bonnet would require total curvature/turn 2pi, a contradiction. This is also the usual elementary proof that a simply connected Euclidean cone surface with angles >=2pi is CAT(0).

Fix a lift of each possible initial vertex. Every saddle connection of length <=B ends at one of the finitely many endpoint lifts in its proper radius-B ball and is the unique geodesic to that lift. This proves finiteness. It does *not* assert that the cyclotomic holonomy module is a discrete lattice.

## 4. Finite-length descent replaces the full cusp theorem import

Rotate the plane by pi/2 so the vertical model direction becomes horizontal and T has derivative [[1,lambda],[0,1]], up to replacing it by its inverse. A saddle connection with nonzero holonomy v=(x,y) can be rotated by the available actual isometry so x>0 and its direction eta satisfies

    odd n: |eta| <= rho/2,
    even n: |eta| <= rho.

These ranges use the actual rotation rho (odd) or 2rho (even). If y!=0 and |eta|<rho, replace v by

    v'=(x-sign(y)*lambda*y, y)=(x-lambda*|y|,y).

This is an actual T or T^(-1) image of the saddle connection. Its squared norm change is

    |v'|^2-|v|^2 = lambda*|y|*(lambda*|y|-2x) < 0,

because x/|y|=cot|eta|>cot rho=lambda/2. For odd n every nonhorizontal reduced direction satisfies this strict inequality. For even n it holds except the two boundary directions +/-rho; those are the second model family. If the process did not stop, it would give infinitely many strictly shorter saddle connections of length at most the original length, contradicting Section 3. Hence a finite composition of actual affine maps takes any saddle connection to a vertical model direction, or, for even n, a direction separated by rho. Both are polygon symmetry directions, hence every outgoing ray there is a single polygon chord (a side allowed).

This is stronger evidence than merely quoting a lattice statement: it proves exhaustiveness for all lengths, all genera, and both even congruence families. The argument is not a bounded search, does not presume that an arbitrary non-saddle vector terminates, and does not use Fuchs's type or length-ratio conjectures. The resulting affine map acts simultaneously on all germs, since it is one map of the entire surface.

## 5. Synchronization and the common shift

Return to source orientation with P_0 at the distinguished vertex and its lower side horizontal, delta=N*rho. On each corner-successor cycle number corners by t and give it the coordinate phi in [t*delta,(t+1)*delta]. Odd n has one coordinate of period 2N*pi and physical direction phi mod2pi. Even n has cones c=0,1 based at P_0,Q_0, each of period N*pi and physical direction phi+c*pi mod2pi.

The half-turn exchange h:P->Q, z->-z, is an affine involution of derivative -I. It fixes precisely the n glued side midpoints in the regular part; no polygon interior can be fixed because the copies are distinct. Odd n has the additional fixed sole cone point; even n has no fixed cone point because h exchanges the two. Thus for n>=5 it has 2g+2 fixed points. Riemann-Hurwitz gives genus-zero quotient. If f is any affine homeomorphism then f h f^(-1) also has derivative -I, so is holomorphic away from finitely many cone points and extends holomorphically there by removability. Its quotient remains topologically a sphere. By uniqueness of the hyperelliptic involution for g>=2, f commutes with h.

One quick algebraic proof of the uniqueness used here: two distinct degree-two maps of a genus>=2 curve to P1 would either factor through the same degree-two quotient (and give the same involution), or their product map would be birational onto a curve of bidegree (2,2) in P1 x P1. Such a curve has arithmetic genus (2-1)(2-1)=1, and its normalization has genus at most one, contradiction. Thus this centrality is established using the *quotient-sphere property*, not just the derivative -I or an unsupported uniqueness of affine lifts.

For a real physical direction theta, assign both forward and backward germs the label

    L_theta(phi)=(phi-theta)/pi mod N.

For odd n the N forward labels are the N distinct residues 2j mod N, and the backward labels are 2j+1; for even n each cone supplies N/2 labels of one parity, and the other cone the complementary parity. In either case forward germs and backward germs are each labelled bijectively by Z/N.

Let f be orientation preserving, and choose an increasing real angular lift F of its derivative. Linear antipodality gives F(x+pi)=F(x)+pi: the angle change over every half-circle is pi. On the odd sole cone, f is F(phi)+2pi*q for one integer q modulo the full cone period, and therefore adds the common label shift 2q. On even cone 0, if f maps it to cone e, its cone-coordinate map is

    G(phi)=F(phi)-e*pi+2pi*q mod N*pi.

Because h identifies the two synchronized cone coordinates and f h=h f, the coordinate map on cone 1 is exactly the same G modulo N*pi. For every forward or backward germ, phi-theta is an integer multiple of pi, so taking theta'=F(theta) gives

    L_(theta')(G(phi))=L_theta(phi)-e+2q mod N.

This proves a *single common shift* for all forward and backward germs at both cones. It is invalid to infer this synchronization from a common derivative alone. The intrinsic difference b-a of initial and backward-terminal labels is thus affine invariant. For odd n this part needs no hyperelliptic centrality; the one cone suffices. The even n>=6 case has genus>=2; n=4 is treated arithmetically below.

## 6. Canonical chords, endpoint reflection, and source type

In source orientation the lower physical side direction at P_j is -2j*rho and at Q_j is pi-2j*rho. For a model direction theta=h*rho, a polygon symmetry perpendicular to that direction pairs every non-supporting vertex with its chord endpoint. Convexity makes this the first vertex encounter. At a supporting vertex there is no interior germ. Boundary rays are sides and the two corner descriptions are identified by the gluing.

Let a,b be a chord's initial and backward-terminal labels. If its clockwise endpoint difference is q in {1,...,n-1}, its two interior corner offsets are (n-1-q)*rho and (q-1)*rho; their sum is delta. If its endpoint corner numbers are t,t', direction alignment gives

    t+t'+1 == n-h mod n.

Consequently

    a+b = ((t+t'+1)*N-2h)/n == -h mod N.

This formula is valid for both polygons: passing to Q changes physical directions by pi, irrelevant to the chord alignment modulo pi. Boundary rays have the same label from either corner because phi is a coordinate on the glued cone, not separately re-zeroed at every polygon.

The descent of Section 4 supplies one affine map from any saddle-connection direction to one of these model directions. Every model outgoing germ is finite, so every original outgoing germ is finite under its inverse. The common shift transports the chord equation to

    b=C_theta-a mod N

with one C_theta for all outgoing germs. This is a verified all-direction reflection pairing; simply assuming it would have rephrased the central target difficulty.

For a billiard trajectory from P_0 with actual slope alpha use theta=alpha, so a=0. Let r be its number of segments and let beta have the supplementary endpoint convention of Fuchs Figure 8. Define the explicit label K_PS by

    r odd: s=n*(alpha+beta)/(2pi), k=n-1-s mod N;
    r even: s=n*(beta-alpha)/(2pi), k=s-1 mod N.

Its final corner coordinate is

    r odd (copy P): phi_v=t*delta+pi-beta;
    r even (copy Q): phi_v=t*delta+beta-2rho.

The physical lower-side directions give s+t==0 mod n in the first case and s-t-1==0 mod n in the second. Substitution gives respectively

    b=1+(t*N-2s)/n == n-1-s mod N,
    b=(t*N+2s-2)/n == s-1 mod N.

Thus b-a=K_PS=k with these conventions. The formulas are the corresponding branches of Definition 2.1 *after selection by actual segment parity*. Its branch inequalities select integer representatives. This establishes the bridge for K_PS; it does not establish that K_PS agrees with a parity-free raw disjunction. The odd printed first bound k<=m+1 has no extra nonnegative-alpha interior solutions beyond the expected range, because its alpha upper bound is then negative.

The side calibration must retain k=N as a representative of residue 0. For the lower side O P_(n-1), r=1, alpha=0 and beta=2rho; s=1 gives k=n-2=N==0 mod N. For the upper side O P_1, alpha=delta and beta=pi; s=n-1 gives k=0. For every direct chord O P_(k+1), 0<=k<=N, the same calculation recovers the clockwise diagonal calibration, including both sides. Reducing k to {0,...,N-1} before imposing a branch representative would incorrectly discard the lower side.

## 7. Unwrapped direction law and elementary cases

Let alpha'=alpha+ell*rho in [0,delta], with ell even for even n. Rotate its initial P_0 germ by -ell*rho; the resulting direction is alpha and the corner offset remains alpha'. If its corner number is t, its label is

    a=(t*N+ell)/n, hence 2a==ell mod N.

This is integral from actual physical direction alignment, with no division by two in an even group. The reflection pairing gives b=k-a. Affine invariance gives the new trajectory type b-a=k-2a=k-ell mod N. Finiteness follows from the inverse-transported finite germ, with no length cutoff.

Bisector reflection sends alpha to delta-alpha, beta to pi+2rho-beta, and preserves segment parity. In the two respective parity formulas it sends s to n-s or 2-s; both give k -> -k mod N. Therefore alpha'=ell*rho-alpha=delta-[alpha+(N-ell)*rho] has type -k-ell mod N. The intermediate actual angle is in [0,delta] whenever alpha' is, and N-ell is even whenever needed. No direction is folded modulo 2pi, and no ell is reduced modulo 2n.

For n=3, N=1 makes the label trivial; existence follows already from the same descent/chord argument, or directly from the triangular-lattice unfolding. For n=4, primitive square-lattice first endpoints have K_PS=1 iff both coordinates are odd and K_PS=0 otherwise. For positive coprime coordinates (a,b), the number of segments is a+b-1. When both are odd the two terminal reflection counts a-1,b-1 are even, alpha+beta=pi, and k=3-2=1. When exactly one is even, beta-alpha is pi/2 or -pi/2, giving k=0 modulo two. Side endpoints are read directly. The only interior nonidentity allowed direction operation swaps coordinates. Endpoint sides have type 0. This proves the law modulo two and existence directly. For n=6 all preceding double-surface geometry (including genus-two centrality and the same shear) applies unchanged, furnishing an independent all-direction proof. The source's arithmetic treatment is consistent but unnecessary for this geometric reduction.

## Conclusion and limit

For K_PS and actual angles, the universal rule is proved by the above geometric chain, including existence, odd doubles, both even families, first-vertex stopping, side/diagonal boundary directions, and all lengths. The universal proof uses compactness/finiteness, an explicit cylinder shear, rotations, and hyperelliptic centrality; it does not rest on an unretrieved Veech original or a numerical enumeration. This theorem does not identify K_PS with an authenticated target that imposes a bare beta-alpha shorthand or a raw disjunction of branches; that mismatch remains a distinct obstruction to the original solved claim. No claim of original discovery, present open status, or human peer review is made.

Final clean proof UTC: 2026-10-15T04:27:34.707433+00:00
