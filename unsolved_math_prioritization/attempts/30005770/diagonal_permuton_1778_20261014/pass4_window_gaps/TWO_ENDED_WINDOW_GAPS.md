# Two-ended profile gaps from exact first and terminal tails

Shared PASS4, row1778 /30005770. This uses the new terminal-tail theorem from the completion lane and the already accepted one-point rerooting construction. It strengthens the quantitative fixed-width certificate. Its gaps still form a summable sequence, so it does not meet the independent adaptive-window divergence criterion.

## 1. Exact inputs and notation

Let lambda, gamma, b_(n,K), g_K and E(p,q) have the definitions in QUANTITATIVE_WINDOW_GAPS.md. Fix0<eta<gamma and choose A_eta so the first-cell tail is at most A_eta lambda^n exp(-eta q), uniformly in n,q.

The new theorem TERMINAL_MARK_AND_POINTWISE_LIFT.md, Section1, gives the terminal-cell tail at most

    2 A_eta lambda^n exp(-eta q).                           (1)

Its proof uses a size-preserving inverse or reverse-complement injection, according to the parity of the terminal cell. It does not assert reversal of the canonical chain. Only(1) is used below.

The one-point rerooting theorem REROOTING_ONE_POINT_BOUND.md gives the exact incoming-edge bound already used in the one-ended quantitative note. We first record the outgoing-edge counterpart using the same construction, rather than an unproved chain-reversal symmetry.

## 2. Cutting the outgoing edge puts the mark last

For a canonical normalized state path A_1,...,A_r, mark a nonterminal index i<r, put q=|A_i| and p=|A_(i+1)|, and remove its outgoing edge A_i->A_(i+1). Inflate the first entry of A_r by12 to get A_r^+, using the accepted injective incoming-edge lift whenever that incoming edge was not the removed edge. Rotate to

    A_(i+1),...,A_r^+,A_1,...,A_i.                         (2)

Insert the accepted deterministic bridge from A_r^+ to A_1. All retained and inserted edges are valid K edges. The exact homogeneous encoding reconstructs an avoider of size n+1 whose last cell is precisely A_i and has size q.

A proposed bridge location, of which there are at most n+1, identifies A_r^+. Collapse its first-entry12 inflation, invert the incoming-edge lift if present, and rotate back. This recovers the original state order, the marked index and every edge except the removed one. The missing edge has at most binom(p+q,p) shuffles. This also handles i=r-1: then the old incoming edge to A_r was removed, and A_r^+ is first in(2), so there is no incoming lift to invert.

Consequently, the number of marked objects with these adjacent sizes satisfies

    Z_n^right(p,q)
       <=(n+1) binom(p+q,p) Last_(n+1)(q),                 (3)

where Last_N(q) is the terminal tail count. If the mark was already terminal, use(1) directly. No involution of the state sequence, conditional uniformity, or loss of either completion weight is used.

## 3. Exact two-direction minimax

For a normalized nonnegative K-vector x, set x_0=x_(K+1)=0 and define

    V_eta^pm(x)=max_(1<=j<=K) max{
                   eta*x_j-E(x_(j-1),x_j),
                   eta*x_j-E(x_j,x_(j+1))},
    kappa_K^pm(eta)=min_x V_eta^pm(x).                      (4)

Let y_0=0 and let y_j be the recurrence from the one-ended note:

    eta*y_j-E(y_(j-1),y_j)=1,

on its unique positive increasing branch. Then

    kappa_K^pm(eta)
       =1/[sum_(j=1)^K min(y_j,y_(K+1-j))].                (5)

Proof. If d=V_eta^pm(x), then d>0, because the first positive coordinate has a positive incoming penalty. The one-ended recurrence argument applied from the left gives x_j<=d*y_j. Applied from the right, using symmetry of E, it gives x_j<=d*y_(K+1-j). Summing proves the lower bound in(5).

For equality put v_j=min(y_j,y_(K+1-j)) and normalize by their sum. The sequence y_j is strictly increasing: its defining positive root increases with its first argument. At every index j, the neighbor toward a nearest endpoint has value y_(s-1), where s=min(j,K+1-j), while the other neighbor has value at least y_(s-1). At a central odd index both neighbors have that value; at central even indices the other neighbor has value y_s. Since E increases in either argument, the larger of the two unnormalized penalties is exactly

    eta*y_s-E(y_(s-1),y_s)=1.

At an endpoint use y_0=0. Homogeneity proves that the normalized profile attains(5).

In particular, for h>=1,

    kappa_(2h)^pm =1/[2 sum_(j=1)^h y_j],
    kappa_(2h+1)^pm=1/[2 sum_(j=1)^h y_j+y_(h+1)],          (6)

with kappa_1^pm=eta. This is the sharp profile guarantee for these two single-edge reroot estimates together; it is not asserted to equal the true gap log(lambda/g_K).

## 4. Uniform count and exponential scale

For every n,K>=1,

    b_(n,K) <=2 A_eta lambda (n+1)^(K+1)
                        lambda^n exp[-n*kappa_K^pm(eta)].   (7)

For each complete cell-size vector choose the maximizing cell and direction in(4), with a fixed tie-breaking rule. Trailing zeros are allowed and do not change the score; since the maximum is positive, a zero coordinate is never selected. For the incoming direction use the first-cell rerooting bound, or the first-cell tail if already first. For the outgoing direction use(3), or(1) if already last. The entropy bound binom(p+q,p)<=exp E(p,q) gives the common bound in(7) before summing over at most(n+1)^K profiles. There is no factor for directions or locations: the chosen mark and direction are deterministic for a profile, and the exact marked-object inequalities already count every possible marked location.

Taking n to infinity with K fixed and then eta increasing to gamma gives

    g_K <=lambda exp[-kappa_K^pm(gamma)].                    (8)

The continuity justification is the same finite recurrence as in the one-ended note.

For eta<=gamma<=log2, let t_eta solve H(t_eta)=eta, where H(t)=(1+t)log(1+t)-t log t, and put R=1/t_eta>2. The proved bounds for y_j in the one-ended note imply y_j is bounded above and below by positive eta-dependent constants times R^(j-1). Equation(6) therefore yields

    kappa_K^pm(eta)=Theta_eta(R^(-K/2)).                     (9)

Thus the improved sequence is summable in K. Formula(7) remains a finite inequality at varying K, but no normalized growing-K probability claim follows without controlling its profile factor and the growth defect of a_n.

## 5. Adaptive limitation and dependencies

The independent adaptive-window criterion would close the largest-cell route if the true gaps delta_K=log(lambda/g_K), or a certified lower sequence for them, had divergent sum. The sequence in(9) does not satisfy that sufficient condition. Failure of this particular divergence test is not a proof that no adaptive window works, and does not imply that the true gaps are summable.

There is a stronger direct diagnostic for this certificate. On the ideal symmetric profile p_i=2^(-|i|)/3, i in the integers, consider any K-cell window containing the center, extending l cells left and r cells right, where l+r=K-1. Write s=2^(-l)+2^(-r). Its mass and exact two-edge boundary entropy obey

    M=(3-s)/3,
    E_boundary=H(1/2)*s/3,
    E_boundary/M=H(1/2)*s/(3-s).                           (10)

At fixed K this ratio is minimized when l and r differ by at most one. On the other hand the finite test vector proportional to2^min(j-1,K-j) has two-direction score eta divided by its total weight: every nonendpoint penalty is negative because H(1/2)>eta, while an endpoint has score eta divided by that total. Therefore

    kappa_(2h)^pm(eta)<=eta/[2(2^h-1)]         (h>=1),
    kappa_(2h+1)^pm(eta)<=eta/(3*2^h-2)       (h>=0).        (11)

The minimum boundary ratios in(10) are respectively H(1/2)/(2^h-1) and2H(1/2)/(3*2^h-2). Since2H(1/2)>eta, every such window has boundary loss strictly larger than this two-ended certificate. This comparison uses the exact endpoint entropy, not a whole-block upper bound.

For any prescribed finite maximum window width, truncating the profile beyond that width preserves all these ratios for center-containing windows. The independent profile lane supplies canonical finite realizations of such fixed local profiles. The infinite profile calculation by itself is a deterministic diagnostic; it does not give positive uniform probability and does not compare with the unknown true gaps delta_K. It shows that combining these two local reroot estimates has not evaded the existing geometric-profile obstruction.

This note combines two genuinely available endpoint tails while retaining the deleted-edge entropy in both directions. It does not estimate the paired interior completion factor ell_A*h_A, and does not prove sublinear largest cell or the1324 anti-diagonal limit.

Input pins:

- QUANTITATIVE_WINDOW_GAPS.md: c66d6b4bd17ec313e0df0989f0bdc7aee6db46007fde953569aa61e9e771e29b.
- REROOTING_ONE_POINT_BOUND.md: the accepted PASS3 one-point construction and exact fibre count; its scope is retained literally.
- TERMINAL_MARK_AND_POINTWISE_LIFT.md: 18af51f210a079b795f00a071271ff2e8839ecd2273316cfd188704a94136cac. Its Section1 terminal count is the new PASS4 input, subject to its complementary acceptance receipt.

All new steps are proved above. No further external result or numerical asymptotic inference is used.
