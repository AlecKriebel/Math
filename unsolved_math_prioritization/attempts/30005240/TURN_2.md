# Turn 2: a quantitative dominant-mode theorem for a normalized return operator

**Substantive author turn 2 of 5. Original actual-density problem unresolved.** This turn supplies a rigorous mechanism that would exclude the hidden larger mode from Turn 1. It proves a quantitative theorem for a weighted contracting return map and small perturbations in one fixed function-space operator norm. The missing step is to verify that hypothesis for the actual Helmholtz boundary transfer. No fixed-function stationary-phase expansion is substituted for an operator-norm estimate.

## 1. Precise abstract hypotheses

Let (X,d) be a compact metric space of positive diameter D. Let F:X→X have Lipschitz constant theta<1, with fixed point x_*. Let a:X→(0,infinity) be Lipschitz. On complex Lipschitz functions use the Banach norm

    ||f||_* = |f(x_*)| + D Lip(f).

Then sup_X |f|≤||f||_*. Put lambda=a(x_*)>0 and define

    (Wf)(x)=a(x)f(Fx).

For each real k≥1 let T_k be a bounded operator on this same Banach space, and let xi_k be a complex number of modulus one. Assume

    ||xi_k^(-1)T_k−W||_* ≤ C/k                              (1)

with a constant C>0 independent of k (an exact family also satisfies this with any positive bound). The phase xi_k accommodates the optical phase of one full period. This is a strong operator norm on the whole specified space, not an estimate only on one chosen amplitude.

The initial data f_k may depend on k. A uniform leading-mode excitation condition will be stated below. These abstract hypotheses are not claimed for the source PDE in this turn.

## 2. Exact conjugation of the optical operator

Set b=a/lambda and define

    g(x)=product_(j≥0) b(F^j x).                              (2)

This converges to a strictly positive Lipschitz function. Indeed log b(x_*)=0, and log b is Lipschitz with some constant L because a has a positive minimum. Therefore

    |log b(F^j x)|≤L D theta^j,
    Lip(log b composed with F^j)≤L theta^j.

The logarithmic series converges uniformly, has Lipschitz constant at most L/(1−theta), and has absolute value at most LD/(1−theta). Exponentiation proves the assertions, including bounded Lipschitz reciprocals. In particular g(x_*)=1 and

    g(x)=b(x)g(Fx).

Writing M_g for multiplication by g gives the exact identity

    M_g^(-1) W M_g = lambda C_F,
    C_F f=f composed with F.                                (3)

Both multiplication operators are bounded and invertible. For example
||M_g||_*≤sup g+D Lip(g), and similarly for 1/g. Let

    K=||M_g||_* ||M_g^(-1)||_* < infinity.

After phase removal and conjugation, set

    S_k=lambda^(-1) M_g^(-1) xi_k^(-1)T_k M_g=C_F+V_k,
    epsilon=KC/(lambda k),  so ||V_k||_*≤epsilon.             (4)

## 3. A direct block perturbation proof

Let Delta=1−theta>0. Write the Banach space as constants plus

    B_0={f:f(x_*)=0}.

Its norm is the direct-sum norm |s|+||y||_*, and evaluation/projection onto either component has norm one. On B_0, C_F has norm at most theta. In these coordinates write

    S = [[1+alpha, b],[c,D_0]],

where |alpha|,||b||,||c||≤epsilon and ||D_0||≤theta+epsilon. Assume epsilon≤Delta/16 and put

    q=epsilon/(Delta−3epsilon)≤1/13.

For |z−1|≤2epsilon, the resolvent of D_0 exists by its norm bound and obeys

    ||(z−D_0)^(-1)||≤1/(Delta−3epsilon).

The scalar map

    H(z)=1+alpha+b(z−D_0)^(-1)c

maps that closed complex disc into itself, since |H(z)−1|≤epsilon+epsilon q<2epsilon. The resolvent identity gives Lipschitz constant at most q²<1 there. The contraction principle supplies a unique fixed point zeta in the disc. Set

    R=(zeta−D_0)^(-1),
    u=(1,Rc),     phi(s,y)=s+bRy,
    d_0=phi(u)=1+bR²c.

Then S u=zeta u, phi S=zeta phi, and |d_0−1|≤q²<1. Thus

    Pi(v)=u phi(v)/d_0

is a commuting rank-one projection. The complementary invariant space ker(phi) is parameterized by J y=(-bRy,y). Direct multiplication gives

    S J y = J(D_0−cbR)y,
    ||D_0−cbR||≤theta+epsilon+epsilon q≤theta+2epsilon=:beta.  (5)

Consequently every v has an exact invariant decomposition into its Pi part and a J part. The elementary bounds ||u−1||_*≤q, ||J||≤1+q and |d_0|≥1−q² imply

    ||S^j v−zeta^j Pi v||_*≤2 beta^j ||v||_*,       j≥0.       (6)

For detail, write s=phi(v)/d_0 and y=v_0−s Rc. Then |s|≤||v||_*/(1−q²) and ||y||_*≤[1+q/(1−q²)]||v||_*. Multiplying this by ||J||≤1+q is less than 2 for q≤1/13, proving (6). Also ||Pi−P||≤3q, where P is projection onto constants.

This explicit decomposition proves the relevant spectral gap without assuming compactness of C_F or invoking a finite-dimensional eigenvalue analogy. The remaining operator has norm at most beta<|zeta|, since |zeta|≥1−2epsilon and 4epsilon<Delta. In particular no weakly excited mode of larger modulus is hidden outside the rank-one part under these hypotheses.

## 4. Uniform quotient theorem and initial excitation

Put v_k=M_g^(-1)f_k and suppose v_k is nonzero and, for a fixed a_0 in (0,1],

    |v_k(x_*)|≥a_0 ||v_k||_* .                              (7)

Assume also q≤a_0/2. Then

    |phi(v_k)|≥(a_0−q)||v_k||_*≥(a_0/2)||v_k||_*.

Since |d_0|≤1+q²<2 and |u(x)|≥1−q>1/2, this yields

    |(Pi v_k)(x)|≥(a_0/8)||v_k||_*    for every x in X.         (8)

Let kappa=beta/|zeta|<1. Whenever kappa^j≤a_0/32, (6) and (8) guarantee S^j v_k(x) is nonzero and

    | S^(j+1)v_k(x)/S^j v_k(x) − zeta |
       ≤ (96/a_0) kappa^j.                                  (9)

Indeed the denominator has absolute value at least
(a_0/16)|zeta|^j ||v_k||_*, while subtracting zeta times the j-th iterate leaves a numerator of size at most 2beta^j(beta+|zeta|)||v_k||_*≤6beta^j||v_k||_*.

Undoing (4), multiplication by g cancels pointwise in the quotient. The resulting theorem is

    | (T_k^(j+1)f_k)(x)/(T_k^j f_k)(x) − xi_k lambda |
      ≤2lambda epsilon+(96lambda/a_0) kappa^j.                (10)

It is uniform in x and in the indicated k,j range. The actual perturbed leading multiplier is xi_k lambda zeta, within 2lambda epsilon of the optical one.

An explicit useful regime follows. For

    k≥max(1,32KC/(a_0 lambda Delta)),

both smallness conditions hold. Furthermore

    kappa≤(theta+2epsilon)/(1−2epsilon)
          ≤1−3Delta/4=:kappa_bar<1.

Thus for integers

    j≥[log k+log(32/a_0)]/|log kappa_bar|,                     (11)

equation (10) gives

    sup_x | (T_k^(j+1)f_k)(x)/(T_k^j f_k)(x)−xi_k lambda |
       ≤(2KC+3lambda)/k.                                    (12)

Here j counts full return-operator iterations. Translating it into the original reflection count requires multiplication by the fixed period and keeping the return obstacle fixed. It is not a theorem for fixed j as k tends to infinity, nor for arbitrary input data orthogonal to the leading functional.

## 5. Why a derivative-losing stationary-phase estimate is insufficient

The decisive hypothesis (1) has not been obtained for the actual boundary-density operator. A familiar fixed-function expansion does not imply it. For a simple exact illustration, let U_h f(x)=f(x+h) on the circle, with h=1/N. For each fixed smooth f, Taylor expansion gives

    U_h f=f+h f'+O_f(h²)

in appropriate lower derivative norms. But on the Lipschitz space take f_N(x)=N^(-1) exp(iNx). Its norm remains bounded above and below, while

    U_(1/N)f_N−f_N=(exp(i)−1) f_N.

Hence the operator norm of U_h−I on that Lipschitz space stays bounded below by a positive constant along h=1/N. Smooth fixed-function asymptotics, even with explicit derivative-loss bounds, cannot be substituted for a small perturbation in the same strong norm.

For the source scattering problem one would have to specify a return region and phase conjugation, prove a contracting limiting ray map and positive transport weight there, and establish (1) on a Banach space where the actual oscillatory boundary transfer is bounded with the required uniform approximation. One must also prove the uniform excitation condition for the physical incident data. A compact illuminated-region proof would still not automatically extend through shadow boundaries or possible zeros of the global density.

These are substantive analytic obligations. They are listed as gaps, not added as unnamed assumptions to a claimed PDE theorem. The abstract theorem does explain exactly how a verified strong approximation would eliminate the Turn 1 hidden-mode counterexample.

## 6. Status

The weighted-composition conjugation, explicit one-dimensional Schur contraction and quantitative ratio estimate are proved above. They are an application of classical contraction/resolvent tools; no claim of historical novelty is made. Finite exact controls test the constants and block identities, not the source PDE hypotheses.

**Original actual-density problem unresolved, author count 2/5.** Next possible routes are a legitimate two-norm/regularity argument for the oscillatory transfer or a proved microlocal restriction that supplies the needed strong norm. Repeating the optical calculation or treating fixed-function remainders as uniform operators would not close the gap. Uncalibrated completion estimate: 25%.
