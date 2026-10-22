# Turn 1: exact Gaussian tilting and removal of radial fluctuations

**Substantive author turn 1 of 5. Original centered-area limit unresolved.** This attempt first derives exact identities for the intended Brownian-increment flat-disk ensemble. It does not replace the disk by its excursion code or an unweighted Brownian polygon. The finite disk count is a credited input from the primary source; the following probabilistic reductions are proved from it.

## 1. Finite ensemble and area conventions

Fix n≥3. Let G_0,...,G_(n−1) in R² be the increments of a standard planar Brownian bridge over intervals of length 1/n. For each coordinate their covariance is

    Cov(G_i^a,G_j^b)=delta_(ab)[delta_(ij)/n−1/n²].           (1)

Their unordered set is almost surely generic in the sense of SOURCE_GATE.md. Conditional on that set, the source ensemble chooses uniformly among its (n−2)! flat translation disks, with boundary side vectors oriented counterclockwise. Write A_n for intrinsic area, including multiplicity of the developed image.

For any ordered zero-sum increments g=(g_0,...,g_(n−1)), put z_0=0, z_j=sum_(i<j)g_i and

    S(g)=1/2 sum_(j=0)^(n−1) det(z_j,z_(j+1)).              (2)

If this ordered boundary admits a flat-disk filling, every such filling has area S(g)>0. To justify independence from the filling, let (x,y) be its global developing coordinates, defined up to translation on the simply connected disk. The flat area form is dx wedge dy, and Stokes gives

    Area=1/2 integral_boundary (x dy−y dx)=S(g).

A triangulation, or piecewise-smooth Stokes, gives the same identity at the corners. Thus multiple fillings affect probability weights but not the area attached to one ordered boundary. Counting only the planar union would discard multiplicity and would not equal (2) in general.

Let W(g) be the number of flat-disk fillings of this ordered counterclockwise boundary, rooted at its distinguished first side and modulo translation. It is a nonnegative integer and is zero if S(g)≤0. A cyclic boundary order has a unique representative beginning with any designated side, since the generic vectors are distinct. The source enumeration therefore says, for a fixed generic set Z and a chosen g_0 in it,

    sum_(permutations of Z\{g_0}) W(g_0,g_1,...,g_(n−1))
                          =(n−2)!.                         (3)

All statements below use the conditional finite ensemble from the source; no unproved explicit formula for W is introduced.

## 2. The exact annealed change of measure

For every nonnegative measurable test function h, or integrable signed h,

    E[h(A_n)]=(n−1) E[W(G) h(S(G))].                         (4)

**Proof.** Given the unordered increment set and its designated first vector, exchangeability of (1) makes the remaining ordered increments uniform over (n−1)! permutations. The average of W h(S) is consequently the sum over all disk fillings of h(area), divided by (n−1)!. The conditional uniform-disk expectation divides the same sum by (n−2)!. Their ratio is n−1. Averaging over the increments proves (4). QED.

In particular E[W(G)]=1/(n−1). The annealed boundary-order law is the multiplicity tilt (n−1)W of the ordinary ordered Gaussian bridge. It preserves the unordered increment-set law: the conditional total weight in (3) is constant. It is not generally ordinary conditioning on an event, because W is not asserted to take only the values zero and one. In particular the unknown correlation of W with signed area is essential to the area question.

## 3. Exact separation of Gaussian energy and shape

Define the total quadratic side energy

    Q_n=sum_(j=0)^(n−1)|G_j|².

The two real coordinate vectors in (1) are independent isotropic Gaussians on the (n−1)-dimensional zero-sum subspace. Hence on their direct sum, of dimension 2(n−1),

    Q_n has law (1/n) chi-square_(2(n−1))
               = (2/n) Gamma(n−1, scale 1),
    mu_n=E Q_n=2(n−1)/n,
    Var(Q_n)=4(n−1)/n².                                    (5)

The normalized vector D=G/sqrt(Q_n) is uniform on the unit sphere in that real subspace and independent of Q_n. Positive dilations give a bijection between all disks with the corresponding side sets, preserving their conditional uniform probabilities. Equivalently W is invariant under positive dilation in (4). Thus the flat-disk sampling can be performed by first sampling D and its uniform disk, then multiplying every length by sqrt(Q_n). If V_n is the area of the unit-energy disk from D, then

    A_n=Q_n V_n,       Q_n and V_n independent.              (6)

This is an equality in a natural coupling, not a heuristic independence of area and the raw side lengths. The variable V_n still contains the difficult disk-shape law.

For p≥0, all the finite-n moments in the next display exist, and

    E[A_n^p]=(2/n)^p Gamma(n−1+p)/Gamma(n−1) E[V_n^p].        (7)

A deterministic area bound proving moment finiteness is given in Section 5 below. The radial Gamma law in (5) remains unchanged by the disk selection; replacing the whole selected boundary by an unweighted Gaussian bridge would be a different assertion and is false as a description of this ensemble.

## 4. An equivalent fixed-energy limit, with quantitative error

Use the mean asymptotic stated and credited in the primary report:

    E A_n=(log n)/(2pi)+C+o(1).                              (8)

By independence in (6), E V_n=E A_n/mu_n. Cauchy–Schwarz and (5) give the useful explicit coupling bound

    E|A_n−mu_n V_n|
      =E|Q_n−mu_n| E V_n
      ≤[2sqrt(n−1)/n] [E A_n/mu_n]
      =E A_n/sqrt(n−1)=O(log n/sqrt n).                     (9)

Consequently the original convergence question is equivalent to

    mu_n V_n−(log n)/(2pi) converges in distribution,          (10)

with the same limiting law. Indeed (9) makes the difference tend to zero in L1, hence in probability, and Slutsky's theorem applies in both directions. Tightness, convergence along any subsequence, and any resulting limit are likewise equivalent. One may replace mu_n by 2 because

    E|(2−mu_n)V_n|=E A_n/(n−1)=O(log n/n).                  (11)

For bounded 1-Lipschitz test functions, (9) bounds the difference of their expectations by the same explicit error. Thus the Gaussian radius is quantitatively negligible at the centered O(1) fluctuation scale. This does not prove tightness or convergence of the remaining fixed-energy shape variable.

## 5. A deterministic discrete area bound and the ordinary bridge-area law

Identify R² with C. For any zero-sum complex increments g_j, use unitary discrete Fourier transforms

    U_p=n^(−1/2) sum_j g_j exp(−2pi i p j/n),
    V_p=n^(−1/2) sum_j z_j exp(−2pi i p j/n).

For p≠0, U_p=(exp(2pi i p/n)−1)V_p. The zero Fourier component of the increments vanishes. Formula (2) becomes

    S(g)=1/2 Im sum_j conjugate(z_j)z_(j+1)
        =1/4 sum_(p=1)^(n−1) cot(pi p/n)|U_p|².             (12)

Since cot decreases on (0,pi), Parseval yields

    |S(g)|≤[cot(pi/n)/4] sum_j|g_j|².                       (13)

This is sharp, attained by a suitably oriented regular n-gon. Every flat-disk filling obeys it because its area is S(g)>0. In particular

    0<V_n≤cot(pi/n)/4,

which proves the finite moment claim in (7). The bound grows with n and does not itself imply the desired logarithmic concentration.

For the *unweighted* Gaussian increments (1), the U_p for p=1,...,n−1 are independent proper complex Gaussian variables, with E|U_p|²=2/n. This follows either from unitary invariance on the complex zero-sum subspace or from E U_p conjugate(U_q)=(2/n)delta_(pq) and E U_p U_q=0. Hence |U_p|²=(2/n)E_p, where the E_p are independent mean-one exponentials, and

    S_n:=S(G) has law sum_(p=1)^(n−1) [cot(pi p/n)/(2n)] E_p.

Pairing p with n−p gives its exact characteristic function

    E exp(it S_n)
      =product_(p=1)^floor((n−1)/2)
            [1+(t cot(pi p/n)/(2n))²]^(−1).                 (14)

The unpaired even-n term has cot(pi/2)=0. Also

    E S_n=0,
    Var(S_n)=(n−1)(n−2)/(12n²).                             (15)

For completeness, the identity sum_(p=1)^(n−1) cot²(pi p/n)=(n−1)(n−2)/3 used here follows by differentiating the product formula for sin(nx), or the equivalent sum-of-cotangents identity, and comparing constant terms at x=0.

The factors in (14) tend to those with coefficients 1/(2pi p), and cot(pi p/n)/(2n)≤1/(2pi p) for 1≤p<n/2. Dominated convergence for the logarithm of the product therefore gives

    E exp(it S_n) -> (t/2)/sinh(t/2),                        (16)

using the classical Euler product for sinh and the continuous value 1 at t=0. This is the usual Brownian-bridge signed-area law, recovered here for the polygonal approximation. It is tight without logarithmic centering. In fact (15) and Chebyshev imply

    S_n−(log n)/(2pi) -> −infinity in probability.             (17)

Equations (4), (8) and (17) demonstrate why this familiar signed-area limit cannot be quoted as the answer for the selected disks. The tilt by the number of fillings changes the area law in a substantial way; convergence of the unweighted path alone is insufficient.

## 6. Covariance normalization is exact, not cosmetic

Let Sigma be a positive-definite 2 by 2 covariance matrix and replace the standard bridge by one with covariance (min(s,t)−st)Sigma. Let L be its positive-definite square root. Composing each translation chart with L gives a bijection of flat disks with transformed side sets; intrinsic area is multiplied by det L=sqrt(det Sigma). Conditional uniform sampling is preserved. Therefore

    A_n^(Sigma) has law sqrt(det Sigma) A_n^(I).              (18)

The correct logarithmic centering is correspondingly sqrt(det Sigma)(log n)/(2pi), and any limit law scales by the same factor. Degenerate covariance is excluded, since genericity and the flat-disk ensemble can fail. This exact affine covariance confirms why the Brownian normalization omitted in the imported short statement matters.

## 7. What is gained, and what remains open

The exact multiplicity tilt (4), independent radial factorization (6), quantitative removal of radius (9), deterministic bound (13), and ordinary Gaussian-area control are proved. The source's disk enumeration and mean are credited inputs; no claim is made to have independently proved those source theorems or found an explicit multiplicity formula W.

A complete solution still needs the centered law of the selected unit-energy shape, or a valid finite combinatorial area representation that controls its fluctuations. Neither the coding excursion's ordinary area, the unweighted bridge's Lévy area, nor the winding analogy supplies that missing identification. No original counterexample is claimed.

**Original unresolved, author count 1/5.** The next genuine attempt should identify a finite area functional compatible with the excursion-to-disk bijection, or obtain a rigorous fluctuation bound for the tilted measure. The present reduction narrows the target but does not supply its limiting distribution. Uncalibrated completion estimate: 15%.
