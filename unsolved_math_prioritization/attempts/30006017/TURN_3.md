# Turn 3: an Abel-renormalized continuum area using the credited critical tree functional

**Substantive author turn 3 of 5. Original polygon limit unresolved.** This turn completes a continuum renormalization for an Abel (power-weight) cutoff. It uses the pre-existing Fill–Janson critical additive-functional theorem, rather than claiming that theorem as new. A separate example proves that this regularization cannot automatically be exchanged for a sharp cutoff, even with positivity and an exact deterministic mean. The finite flat-disk transfer is still absent.

## 1. The published input and its normalization

Let e be a standard Brownian excursion, with interval measure nu_e as in Turn 2, and define

    F_e(alpha)=integral s(I)^alpha nu_e(dI).

For Re alpha>1, elementary interval integration and Fubini give

    F_e(alpha)=alpha(alpha−1)
       integral_(0<u<v<1) (v−u)^(alpha−2) min_(u≤t≤v)e(t) du dv. (1)

Indeed for an interval of length s, the double integral of (v−u)^(alpha−2) over its ordered point pairs is s^alpha/[alpha(alpha−1)]. The levels whose components contain both u and v have total length equal to the minimum in (1).

We use J. A. Fill and S. Janson, *The sum of powers of subtree sizes for conditioned Galton–Watson trees*, Electronic Journal of Probability 27 (2022), paper 114, DOI [10.1214/22-EJP831](https://doi.org/10.1214/22-EJP831). The published PDF, rather than only its earlier arXiv version, was checked. The precise credited inputs are Theorems 1.2–1.3, Theorem 1.24, equations (1.20)/(1.25), and Remark 1.27, including its centered critical formula (1.41):
- Twice (1) is their Y(alpha) for Re alpha>1, jointly in alpha.
- E Y(alpha)=Gamma(alpha−1/2)/(sqrt(2) Gamma(alpha)).
- The centered family Y_tilde(alpha) is analytic on Re alpha>0, has jointly continuous second moments there, and can be realized as a measurable function of the same excursion e. In particular its value at alpha=1/2 is defined.

We select this same-excursion realization. The centered continuation, not the uncentered meromorphic Y, is what is regular at 1/2. Their moment theorem can be applied using any admissible offspring law with a finite extra moment (for example a bounded nondegenerate critical law); the limiting centered family is universal and is the one used here. No assumption on an offspring distribution is being imposed on the polygon ensemble.

The author's published corrigendum concerns an Appendix D variance on the imaginary-alpha boundary. It does not change the listed positive-real/critical inputs. The retrieved corrigendum text and the PDF access limitation are recorded in the source addition.

## 2. The mean interval intensity follows with the correct factor of two

Let bar_nu be the expected interval measure. Multiplying by s gives a finite measure on [0,1], since integral s nu_e=integral e≤H and E H<infinity. For integers m≥0, the preceding source formulas, including Y(1)=2 integral e, give

    E F_e(m+1)=1/(2sqrt(2)) Gamma(m+1/2)/Gamma(m+1).

These are exactly the moments of the finite measure

    s bar_nu(ds)=1/sqrt(8pi) s^(−1/2)(1−s)^(−1/2) ds.

Uniqueness of finite measures on [0,1] from their polynomial moments follows by polynomial approximation of continuous functions. Consequently, for every nonnegative measurable f,

    E integral f(s(I)) nu_e(dI)
       =1/sqrt(8pi) integral_0^1 f(s)s^(−3/2)(1−s)^(−1/2) ds. (2)

There is no mass at zero in this identity; dividing the finite measure by s on (0,1] and using monotone convergence is legitimate. Formula (2) now shows F_e(alpha) is finite almost surely for real alpha>1/2, and that the complex functional is analytic on Re alpha>1/2 by local domination with a slightly smaller real exponent. In that half-plane,

    E F_e(alpha)=1/(2sqrt(2)) Gamma(alpha−1/2)/Gamma(alpha),
    F_e(alpha)−E F_e(alpha)=1/2 Y_tilde_e(alpha).              (3)

The second equality extends the matching on Re alpha>1 by analytic uniqueness in the same-excursion realization. Alternatively, it follows directly from the published excursion representation in that half-plane. The factor 1/2 in (3) is important: our excursion is e, not the alternative tree coding 2e.

## 3. Abel weighting of the width functional

Let X be an independent standard real Brownian bridge. For real z>0 put

    W(z)=integral s(I)^z |X(d_I)−X(g_I)| nu_e(dI),
    M(z)=E[W(z)|e]
        =sqrt(2/pi) integral s^(1/2+z)sqrt(1−s) nu_e(dI).    (4)

By (2) and Tonelli,

    E W(z)=E M(z)=1/(2pi) integral_0^1 s^(z−1) ds
                              =1/(2pi z).                  (5)

In particular these nonnegative variables are almost surely finite. This exact identity concerns the continuum width model, not the finite polygon expectation.

Define

    R_z(e)=integral s^(1/2+z)[sqrt(1−s)−1] nu_e(dI), z≥0.

Since 0≤1−sqrt(1−s)≤s for 0≤s≤1,

    |R_z|≤integral s^(3/2+z) nu_e≤integral s nu_e≤H.

Dominated convergence therefore yields R_z→R_0 almost surely and in L2. Combining (3)–(5) gives the exact centered decomposition

    M(z)−1/(2pi z)
      =sqrt(2/pi)[1/2 Y_tilde_e(1/2+z)+R_z−E R_z].           (6)

The credited second-moment continuity at alpha=1/2 and the preceding bound imply

    M(z)−1/(2pi z) ->
      V(e):=sqrt(2/pi)[1/2 Y_tilde_e(1/2)+R_0−E R_0]
                                  in L2 as z decreases to zero. (7)

Thus the random conditional mean can indeed be renormalized in this Abel scheme. This conclusion does not rely on applying an uncentered analytic function across its pole.

Its harmless constant can also be evaluated from (2):

    E R_0=1/sqrt(8pi)
             integral_0^1 [1−(1−s)^(−1/2)]/s ds
          =−log(2)/sqrt(2pi).                              (8)

The substitution u=sqrt(1−s) reduces the integral to −2 log 2. This constant belongs to the decomposition of the continuum functional; it is not asserted to equal the source's finite-polygon constant C.

## 4. The Gaussian centered part has the same limit as in Turn 2

Put Z(z)=W(z)−M(z). The laminar covariance argument from Turn 2 extends to any interval weights with absolute value at most one. For clarity, truncate all intervals at s>epsilon first, so every measure integral is finite. The conditional variance of the difference between weights 1 and s^z is bounded by

    integral integral |1−s(I)^z| |1−s(J)^z|
                         |c(I,J)| nu_e(dI)nu_e(dJ),          (9)

where c is the bridge increment covariance. The double integral with the weights replaced by one is at most 2HT+T²≤3H², by the nested/disjoint argument. For each positive interval length, 1−s^z tends to zero as z tends to zero. Dominated convergence in (9), followed by removal of the lower cutoff using the same uniform bound, proves

    Z(z) -> Z(e,X) in conditional L2 for almost every e.

Since E H²<infinity, the convergence is also joint L2. Here Z is exactly the conditionally centered limit already constructed in Turn 2, rather than a new unrelated random variable. This also verifies that W(z) itself has a finite second moment for each fixed z>0: M(z) has one by (3) and the bound on R_z, and Z(z) by (9).

Combining this with (7) proves the complete scoped theorem

    W(z)−1/(2pi z) -> U:=Z(e,X)+V(e) in L2 as z↓0.           (10)

The limit has mean zero and finite variance. Moreover E[Z|e]=0, so its two displayed components are orthogonal in L2:

    Var(U)=E[Z²]+Var(V).

They are not asserted to be independent. Equation (10) is an exact construction of an Abel-renormalized candidate continuum area, with its critical tree input explicitly credited. It is not an identification of the original polygon's limit law.

## 5. Why an Abel limit and an exact mean do not imply a sharp-cutoff limit

Here is a general counterexample to that implication. It is a positive random measure, not a flat disk. Fix c>0 and 0<a<c, let Theta be uniform on [0,2pi], and put on t≥0

    dK(t)=[c+a cos(t+Theta)]dt.

This density is strictly positive and its mean measure is exactly c dt. Its Abel integral satisfies

    integral_0^infinity exp(−zt)dK(t)−c/z
         =a[z cos(Theta)−sin(Theta)]/(1+z²)
         ->−a sin(Theta) in L2.                            (11)

In contrast its sharp integral is

    K([0,T])−cT=a[sin(T+Theta)−sin(Theta)].                  (12)

For T=2pi m this is zero; for T=(2m+1)pi it is −2a sin(Theta), a nondegenerate fixed law. Thus (12) does not even converge in distribution. Both its exact mean zero and its bounded variance hold at every cutoff. Under s=exp(−t), (11) is a power-weight cutoff s^z and (12) is a length cutoff s>exp(−T), exactly the two regularization types being distinguished.

This establishes a logical limitation: positivity, an exact logarithmic mean and L2 Abel renormalization are still insufficient for a hard-cutoff convergence theorem. Extra structure of the Brownian excursion may permit that step, but it needs a separate proof. Neither (11) nor (12) is a counterexample for the source ensemble.

## 6. Scope after this attempt

The continuum Abel limit (10) is proved using the credited Fill–Janson theorem and the covariance construction of Turn 2. Its normalization is tied to the standard excursion/bridge convention, and (2) checks the 1/(2pi) coefficient independently of the finite polygon mean. The critical functional is described through its established analytic continuation; no explicit elementary distribution is obtained here.

The remaining route still has two material obligations: establish an appropriate sharp-cutoff/approximation theorem for this continuum model, and prove that the actual finite uniform flat disks are approximated by that model with the right cutoff and centering. Even a verified finite expectation difference would not automatically identify the random error or prove uniform integrability. In particular no claim that the original limit equals U+C is made.

**Original unresolved, author count 3/5.** Next work should target the cutoff/finite-representation bridge, rather than rebrand the credited critical tree theorem as a solution of the polygon problem. Uncalibrated completion estimate: 35%.
