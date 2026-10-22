# Turn 4: the continuum sharp-cutoff limit with an L2 error bound

**Substantive author turn 4 of 5. Original finite-polygon limit unresolved.** This turn closes the sharp-cutoff gap for the candidate continuum width functional. It uses a credited uniform variance bound for additive functionals of conditioned Galton–Watson trees, transfers that bound to the Brownian excursion, and combines it with the previous Gaussian estimate. It does not yet identify the source's finite disk areas with the continuum approximation.

## 1. Notation and the additional credited input

Keep the standard Brownian excursion e, independent real Brownian bridge X, interval measure nu_e and width functional W_epsilon from Turns 2–3. For a real interval-weight function f put

    F_e(f)=integral f(s(I)) nu_e(dI).

The first-moment identity already proved from the credited excursion normalization is

    E F_e(f)=c_0 integral_0^1 f(s)s^(−3/2)(1−s)^(−1/2) ds,
    c_0=1/sqrt(8pi),                                        (1)

for nonnegative measurable f.

We use S. Janson, *Asymptotic normality of fringe subtrees and additive functionals in conditioned Galton–Watson trees*, [arXiv:1312.1211](https://arxiv.org/abs/1312.1211), Theorem 6.7, equation (6.24), published in Random Structures & Algorithms 48 (2016), 57–101, DOI 10.1002/rsa.20568. For a fixed admissible critical offspring law and any real toll f, its additive functional A_f(T_n)=sum_(v in T_n) f(T_(n,v)) obeys

    sqrt(Var A_f(T_n))
      ≤C sqrt(n)[sup_k sqrt(E f(T_k)²)
                       +sum_(k≥1) sqrt(E f(T_k)²)/k].       (2)

The constant is independent of the toll, hence applies also to n-dependent tolls. The theorem and its proof setup were checked in the primary manuscript, and the display was visually inspected. This result, and the conditioned-tree contour convergence used below, are pre-existing inputs; no priority claim is made for them.

For definiteness choose the critical Poisson(1) offspring law, so its variance is one, all size conditionings are possible, and all moments required by the Fill–Janson convergence statements are finite. This auxiliary approximation is a tool for Brownian-excursion analysis. It is not asserted to be the combinatorial law of the source's flat disks.

## 2. Transfer of variance bounds to the excursion interval measure

Let k_v be the size of the fringe subtree at vertex v in T_n and set

    J_n(f)=1/(2sqrt(n)) sum_v f(k_v/n),
    mu_n=1/(2sqrt(n)) sum_v (k_v/n) delta_(k_v/n).

The corresponding continuum finite measure is mu_e(ds)=s nu_e(ds), of total mass integral e. The standard contour convergence and the explicit power-functional identities in Fill–Janson, Section 7, imply jointly

    mu_n -> mu_e weakly as finite measures on [0,1],          (3)

with the same normalized Brownian excursion e. Here is sufficient detail to specify the passage rather than assume a new measure convergence theorem. Couple the normalized contours to converge uniformly to e. For every integer m≥0, the deterministic contour formulas in that section give

    integral s^m mu_n(ds)=J_n(s^(m+1)) -> F_e(s^(m+1)).

The case m=0 is the total-path-length/contour-area identity; higher m follow from the double-minimum formula with an integrable kernel, with an error tending to zero. These simultaneous moment limits give (3) by polynomial approximation, since the zeroth moments also converge. The factor 1/2 matches the contour normalization to e rather than 2e.

The total masses mu_n([0,1]) have uniformly bounded second moments by the credited moment convergence for the alpha=1 functional. Thus if f vanishes near zero and is bounded with finitely many discontinuities, all at fixed s-values, J_n(f) converges in distribution to F_e(f), and their expectations converge. Indeed J_n(f)=integral[f(s)/s]mu_n(ds); its integrand is bounded and the limit measure has no atom at any fixed positive s, by (1). The second-moment bound on total masses gives the needed uniform integrability for the means.

Fix 0<delta<epsilon≤1 and 0<alpha≤1, and choose the size-only toll

    f_n(T)=(|T|/n)^alpha 1_{delta<|T|/n≤epsilon}.

Its supremum in (2) is at most epsilon^alpha. With N=floor(epsilon n),

    sum_k |f_n(T_k)|/k
       ≤n^(−alpha) sum_(k=1)^N k^(alpha−1)
       ≤epsilon^alpha/alpha.

(The sum is zero if N=0.) After normalization by 2sqrt(n), (2) gives

    Var J_n(s^alpha 1_{delta<s≤epsilon})≤C_alpha epsilon^(2alpha).

Pass to the limit using (3), convergence of means and lower semicontinuity of the second moment. The result is the uniform continuum bound

    Var F_e(s^alpha 1_{delta<s≤epsilon})
                       ≤C_alpha epsilon^(2alpha),           (4)

independent of delta and epsilon. No second-moment convergence for the discontinuous band function is required: the stated lower semicontinuity is enough. The only constants come from the fixed auxiliary offspring law and alpha.

## 3. Critical sharp-cutoff renormalization of the conditional mean

At alpha=1/2 define

    C_epsilon=F_e(sqrt(s) 1_{s>epsilon})
                      −E F_e(sqrt(s) 1_{s>epsilon}).

By (4),

    E[(C_delta−C_epsilon)²]≤C epsilon,  0<delta<epsilon.

Consequently C_epsilon converges in L2 to a mean-zero variable C_* and

    ||C_*−C_epsilon||_2≤C sqrt(epsilon).                    (5)

This is a genuine sharp-cutoff result, additional to the Abel statement of Turn 3.

It also identifies C_* with the same critical tree functional. Write epsilon=exp(−T). Nonnegative Tonelli gives, for z>0,

    F_e(s^(1/2+z))=z integral_0^infinity exp(−zT)
                              F_e(sqrt(s)1_{s>exp(−T)}) dT.

Centering preserves this identity as a Bochner L2 integral because the C_epsilon have uniformly bounded L2 norms. As z decreases to zero, the right side tends to C_* in L2: split the integral at a fixed large T, use the L2 convergence on the tail, and note that the bounded initial part has vanishing weight. Turn 3 and the credited centered analytic continuation give the left side's centered limit. Therefore, in the same excursion realization,

    C_*=1/2 Y_tilde_e(1/2).                                 (6)

There is no general Abel-to-sharp-cutoff inference here; the essential new ingredient is the uniform band variance bound (4). This is why the positive random-measure obstruction in Turn 3 does not apply.

Now write the conditional mean of the width cutoff as

    M_epsilon=sqrt(2/pi)[F_e(sqrt(s)1_{s>epsilon})+R_epsilon],
    R_epsilon=F_e(sqrt(s)[sqrt(1−s)−1]1_{s>epsilon}).

Its expectation is exactly (log(1/epsilon))/(2pi), by (1). Since |R_0−R_epsilon|≤sqrt(epsilon)T_epsilon, where
T_epsilon=F_e(s1_{s≤epsilon}), the residual is harmless. To quantify it, use (4) at alpha=1, let delta decrease to zero, and use (1): for epsilon≤1/2,

    Var(T_epsilon)≤C epsilon²,
    E T_epsilon=O(sqrt(epsilon)),
    E T_epsilon²=O(epsilon).                               (7)

The passage to delta=0 is justified by nonnegative monotone convergence for the first and second moments, using the bound on the band variances and their finite limiting means. Consequently ||R_0−R_epsilon||_2=O(epsilon). Together with (5)–(6), this proves

    || M_epsilon−log(1/epsilon)/(2pi)−V(e) ||_2
                                      =O(sqrt(epsilon)),    (8)

where V(e) is exactly the centered conditional-mean limit defined in Turn 3, including its stated constant. No alternative random variable is introduced by the cutoff change.

## 4. The complete sharp-cutoff continuum theorem

Turn 2 supplies the Gaussian centered-tail estimate

    E[(Z−Z_epsilon)²]
                      ≤2E[H T_epsilon]+E[T_epsilon²].

By E H²<infinity, Cauchy–Schwarz and (7), this is O(sqrt(epsilon)). Hence

    ||Z−Z_epsilon||_2=O(epsilon^(1/4)).                      (9)

Combining (8)–(9) proves

    || W_epsilon−log(1/epsilon)/(2pi)−U ||_2
                                   =O(epsilon^(1/4)),       (10)

where U=Z(e,X)+V(e) is the same finite-variance mean-zero variable obtained by Abel renormalization in Turn 3. This is a complete theorem for the continuum excursion-layer functional with the standard excursion/bridge normalization.

In particular, setting epsilon=1/n is legitimate for this continuum model:

    W_(1/n)−(log n)/(2pi) -> U in L2,

with the indicated O(n^(-1/4)) bound. This statement concerns W_(1/n), not the original random disk area A_n. The equality of their leading logarithmic means is not a proof that their random difference vanishes or has a specified constant limit.

## 5. A precise sufficient finite-model bridge

If one could couple the source's actual areas A_n with the independent excursion/bridge construction so that, for a deterministic constant b,

    A_n−W_(1/n) -> b in probability,                         (11)

then Slutsky and (10) would give A_n−(log n)/(2pi) -> U+b in distribution. More generally, any justified limiting joint error could be incorporated, but cannot be guessed from expectations alone. An L1 version of (11), together with the source expectation asymptotic, would force b to equal its constant C. Convergence in probability alone would not force that conclusion without uniform-integrability information.

Equation (11) is not proved here and must not be renamed a result for the original target. The source's finite excursion-to-disk bijection is presented in a sketch and an in-preparation manuscript was not located. The developed boundary limit itself is conjectural in the available slides. Even proving uniform boundary convergence would need an additional area-control argument, because area can be sensitive to microscopic winding/multiplicity.

## 6. Status

The sharp-cutoff continuum L2 construction and rate (10) are proved from the explicitly credited tree results and the preceding Gaussian covariance proof. The required source inputs, cutoff quantifiers and normalization are recorded. The main obstacle has narrowed to the finite uniform-disk representation and approximation, not to the existence of a natural renormalized continuum width variable.

**Original unresolved, author count 4/5.** The final genuine attempt will test the finite representation/area-continuity bridge. No claim of an original limiting law or novelty certification is made. Uncalibrated completion estimate: 45%.
