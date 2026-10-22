# A published2001 determinant covers the full stationary law

UTC authored: 2026-10-15T04:02:20Z; source inspection confirmed 2026-10-15T04:02:39Z. Completion estimate: 90% of this scoped historical audit. **Review status:** the parent reports that its independent falsifier confirmed the corrected bridge and coefficients; the parent retains the separate verification artifacts. This family records its own checks only in the files below. No assertion of the original problem author's acceptance is made.

## Source statement and exact pin

Benny Levikson, Tomasz Rolski and Gideon Weiss, *Layering of the Poisson process in the quadrant*, Probability and Mathematical Statistics21, fasc.2(2001),417–440. Primary journal archive:

https://www.math.uni.wroc.pl/~pms/files/21.2/Article/21.2.11.pdf

Retrieved byte count3,126,456; SHA256 a5745a08113987d9a1db2b4b8403144c99a2f4a1355032538f8a588bccd6aa0d. The file title page gives2001; the archive scan's PDF creation date2008 is not the publication date. A February2000 manuscript surfaced through an author-uploaded index, but this audit relies on the published2001 journal copy.

Relevant locators visually inspected: printed418 identifies layers with empty-boundary Hammersley particles; printed420(PDFpage4) defines the finite initial configuration and the event that the last particle has not jumped; printed423(PDFpage7), equation(2.4), expresses its probability using H; printed425(PDFpage9), equations(2.10),(2.13) and Theorem2.5, evaluates H as a determinant. Printed432 Proposition2.9 concerns selected no-jump events. Printed434–435 Theorem3.2 takes a diagonal specialization to one layer's marginal. The multivariable result needed below is Theorem2.5, not merely that marginal specialization.

Write, for integer theta,

    l_theta(z)=sum_{s>=max(0,theta)} z^s/[(s-theta)! s!].                 (L1)

Equivalently l_theta(z)=z^(theta/2) I_|theta|(2 sqrt(z)), with its continuous value at zero. For m>=1,

    H_m(z_1,...,z_m)=det[l_(i-j)(z_j)]_(i,j=1..m), H_0=1.              (L2)

For the pure-left-jump nearest-right process Y started at
0<y_1<...<y_k, their equation(2.4) and Theorem2.5 give

    Fbar_k(t;y):=P_y(Y_k(t)=y_k)
               =e^(-t y_k) H_(k-1)(t y_1,...,t y_(k-1)).              (L3)

All rates are exactly one. There is no deterministic drift in this auxiliary finite process. Because each Y_i is nonincreasing and a jump changes it strictly, the event in(L3) is exactly that particle k makes no jump on(0,t].

## The full-law identity

Let X be the stationary target process with positive linear drift, unit PPP left-jumps, and finite-prefix consistency. For 0<x_1<...<x_k, put x_0=0. Then

    P(X_i>x_i for i=1,...,k)
      =e^(-x_k) H_(k-1)(x_k-x_(k-1),...,x_k-x_1)                     (L4)
      =e^(-x_k) det[l_(i-j)(x_k-x_(k-j))]_(i,j=1..k-1).

Revision note2026-10-15: the original Step2 incorrectly prohibited creation of a(k+1)-st unrestricted pile. The original is preserved under history/. Formula(L7) now distinguishes unrestricted U from the finite count min(k,U); the event equivalence is unchanged.

This identity is an audit deduction from the published no-jump determinant. It is **not claimed to be a displayed formula or a claimed resolution in that paper**. The steps below establish actual mathematical coverage, not a bibliographic inference from ingredient dates.

## Proof of the exact equivalence

**Step1: stationary law as empty-boundary layers at height1.** Let a unit PPP lie in the quadrant, let L(a,s) be the longest strictly increasing chain in(0,a]x(0,s], and put Z_i(s)=inf{a:L(a,s)>=i}. Patience sorting gives the empty-boundary nearest-right Hammersley positions. For real u set X_i(u)=e^u Z_i(e^u). Between jumps the derivative is X_i; the transformation(a,s)->(as,log s) preserves area and maps nearest-right events to nearest-right events. Area-preserving quadrant scaling shifts u and preserves the PPP law, so this is stationary. Its state at u=0 has inverse-counting function L(a,1). Finite-prefix uniqueness identifies this with the source's stationary law. Thus

    {X_i>x_i for all i} = {L(x_i,1)<=i-1 for all i}.                  (L5)

The last-particle event below uses only the finite rectangle(0,x_k)x(0,1); no particle supplied from infinity participates in its proof.

**Step2: a deterministic finite-word identity.** The mechanism is also the arbitrary-initial-configuration graphical formula in Aldous–Diaconis1995, author PDF internalpage6, immediately after Rule2. A direct finite-word proof is given here to check conventions. Define

    y_j=x_k-x_(k-j), j=1,...,k; y_0=0.                                (L6)

These satisfy0<y_1<...<y_k=x_k. Start the pure-jump finite particle process at this row. Given a finite point configuration in(0,x_k)x(0,1), process its horizontal labels in increasing vertical-time order by replacing the first larger pile top.

Equivalently, place the virtual increasing word(y_1,...,y_k) before the real labels and run **unrestricted** ordinary patience sorting. Its first k pile tops evolve autonomously by the finite-k rule: an insertion to their right changes no tracked top. Additional piles can appear after the tracked rightmost top first drops; this does not change first-k autonomy. Delete the single initial label y_k when counting unrestricted pile tops strictly below x_k: low-label compatibility shows that this unrestricted count U equals the LIS length of the augmented word

    (y_1,...,y_(k-1), real labels in temporal order).

Any increasing subsequence of that word either uses no initial label, or ends its initial portion at y_j. In the latter case it can and optimally does use all j preceding initial labels, and its remaining labels must lie strictly above y_j. Consequently

    U=max_{j=0,...,k-1} [j+L((y_j,x_k)x(0,1))],
    #{i<=k:Y_i(1)<x_k}=min(k,U).                                     (L7)

Particle k starts at exactlyx_k and can only decrease. It stays there precisely when min(k,U)=k-1, equivalently U=k-1 (or U<k, since the virtual initial row already supplies k-1). It cannot return after a strict jump, and no PPP point has horizontal coordinatex_k. Therefore

    {Y_k(1)=x_k}
      =intersection_{j=0,...,k-1}
          {L((y_j,x_k)x(0,1))<=k-j-1}.                               (L8)

**Step3: reflect the rectangle in both axes.** Map each point(a,s) to(x_k-a,1-s). This is area preserving and sends a unit PPP to a unit PPP in the same rectangle. Reversing both axes sends every increasing chain to an increasing chain with its order reversed, preserving its length. The suffix rectangle(y_j,x_k)x(0,1) becomes the prefix rectangle(0,x_k-y_j)x(0,1). Since x_k-y_j=x_(k-j), the events in(L8) become exactly the events in(L5), in reverse index order. Hence their probabilities agree:

    P(X_i>x_i for all i)=Fbar_k(1;y_1,...,y_k).                        (L9)

Inserting(L6) into the published formula(L3) proves(L4).

This proof treats the exact target's drift, rate, boundary condition and whole finite-prefix law. It does not infer independence between particles, a Markov property in particle index, or a product of marginal laws.

## Boundary cases, arbitrary queries and checks

- k=1 uses an empty determinant and gives P(X_1>x)=e^(-x).
- With all x_i equal to x, the H arguments vanish, its matrix is upper triangular with diagonal1, and(L4) again gives e^(-x), as required by the strongest first-particle constraint.
- To query only X_k>x, let x_1,...,x_(k-1) decrease to0. Formula(L4) becomes e^(-x)H_(k-1)(x,...,x), exactly the published marginal Theorem3.2.
- For k=2, it gives e^(-x_2)I_0(2 sqrt(x_2-x_1)), matching the known joint survival law, not merely the second marginal.
- Arbitrary finite thresholds and selected indices reduce to weakly increasing thresholds on all first K coordinates: assign each coordinate i the maximum positive threshold imposed on a queried index at most i, or0 if none. Ordering of the particles makes the events equivalent. Continuity extends(L4) from strict positive thresholds to ties and zeros. There are no deterministic location atoms because the positions at height1 are PPP horizontal coordinates.
- The selected-particle no-jump event in Proposition2.9 is not itself a position-threshold event. In particular no jump of both first particles has probability e^(-y_2), whereas the stationary two-coordinate survival contains a Bessel factor. The correct coverage is the **last** no-jump event with the reflected initial row(L6).

lrw_reflection_check.py is an independently written exact validation. It imports no campaign or sibling implementation. It enumerates uniform permutations, all strip-count compositions and independent factorial-series determinants, and verifies(L4)'s raw Taylor coefficients through degree7 for four sets of rational thresholds with k=2,3,4,5. It additionally tests the pathwise reflected no-jump equivalence on11,534 distinct finite configurations. The check intentionally runs unrestricted pile insertion and compares its kth top, so first-k autonomy was already respected computationally. A separate negative control starts at y_1=2 and inserts1/2 then1: unrestricted sorting has two piles, finite-one-particle evolution has one, both have first top1/2, and the last-unchanged event is false. LRW_REFLECTION_CHECK.json records every coefficient, input and negative control. All checks pass. These finite tests validate conventions and implementation; the deterministic argument establishes the general identity.

## Historical conclusion and its exact limit

The2001 published multivariable determinant, combined with the already-known exact stationary-layer mapping and the elementary reflected-word identity above, gives a finite determinant for **every** joint stationary threshold probability. This is stronger mathematical prior coverage than a collection of one-particle marginals, an unevaluated B-rank law, or a bare reference to RSK.

What is not established is an older source explicitly writing(L4), identifying it as a resolution of Aldous's February2018 question, or a universal bibliographic firstness/acceptance verdict. This audit's new work is the explicit equivalence check and source identification. The campaign may still offer a useful positive-series/certified-arithmetic presentation, but it should not promote the underlying simultaneous stationary law as a novel mathematical discovery without distinguishing that presentation from this prior complete covering description.
