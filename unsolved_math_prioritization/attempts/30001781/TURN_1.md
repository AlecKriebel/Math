# Turn 1: common isometric images of unconditional rows

2026-10-01. A scoped positive theorem toward the corrected original conjecture. One substantive author turn. The original remains unresolved. This is a consequence of the credited Chevet inequality, not a historical novelty claim.

## The non-unconditional class and theorem

Let D>=N and let T:R^D->R^N be a fixed linear map with TT*=I_N. Let Z_1,...,Z_n be independent isotropic unconditional log-concave random vectors in R^D; their distributions need not be identical. Put X_i=T Z_i and let A have rows X_i*. Then every X_i is centered, isotropic and log-concave. It need not be unconditional in the coordinates of R^N.

There are universal constants C,c>0 such that, for every k<=n,m<=N,

    E A_(k,m) <= C [sqrt(m) log(3N/m)+sqrt(k) log(3n/k)],

and, for every t>0,

    P(A_(k,m)>C [sqrt(m) log(3N/m)+sqrt(k) log(3n/k)]+t)
       <= exp(-c min(t^2,t)).                                 (1)

Constants are independent of D and T. The same common T is essential in the proof. We do not assert that every isotropic log-concave law has such a latent representation, or that unrelated maps T_i can be substituted row by row. This theorem therefore does not settle the original arbitrary-row conjecture.

## 1. A tail-count width lemma

Let E=(E_1,...,E_D) have independent centered symmetric exponential coordinates of variance one. For every coefficient vector a of Euclidean norm one,

    P(|<a,E>|>u)<=C_0 exp(-c_0 u), u>=0,                        (2)

with universal constants. One elementary justification uses the moment generating function

    E exp(s E_j)=1/(1-s^2/2), |s|<sqrt(2).

For a fixed sufficiently small |s|, the product over j has logarithm

    sum_j -log(1-s^2 a_j^2/2) <= C s^2 sum_j a_j^2 = C s^2.

Chernoff's bound at that fixed s gives (2) for the positive and negative tails, with an enlarged constant covering small u. This argument does not depend on the number of coordinates.

Every row of T has Euclidean norm one. Thus the N coordinates of W=T E satisfy (2), even though those coordinates need not be independent. For any vector w write ||w||_(m) for the Euclidean norm of its m largest coordinates in absolute value. Deterministically, for every a>=0,

    ||w||_(m)^2 <= m a^2 + sum_(j=1)^N (|w_j|^2-a^2)_+.

Taking expectations and applying the tail integral gives

    E||W||_(m)^2
       <= m a^2 + C_0 N integral_a^infinity 2u exp(-c_0 u) du.

Take a=C_1 log(3N/m) with a sufficiently large universal C_1. The integral is bounded by C m(1+a), and since log(3N/m)>=log3, the whole expression is at most C m log^2(3N/m). Jensen then yields

    E||T E||_(m) <= C sqrt(m) log(3N/m).                       (3)

Only marginal exponential tails were used. In particular no sign invariance or independence of the transformed coordinates is being smuggled into this estimate. Taking T=I also gives the analogous bound in dimension n for the row-sparse width.

## 2. Apply the valid Chevet theorem in latent coordinates

Let Gamma be the n-by-D matrix with rows Z_i*. Independence makes its full nD-dimensional law isotropic, log-concave and unconditional. This is precisely the hypothesis of Adamczak–Latała–Litvak–Pajor–Tomczak-Jaegermann, Studia Mathematica210(2012), Theorem3.1 and Corollary3.2.

Let U_m(N) denote the m-sparse Euclidean unit vectors and put K_0=conv U_m(N). Define L=(conv U_k(n))^polar. In latent coordinates use

    K=T* K_0 subset R^D.

The supremum of <Gamma v,u> over v in K and u in conv U_k is exactly A_(k,m), because A=Gamma T*. Since TT*=I, T* is a Euclidean isometric embedding. Hence the Euclidean radii of K and L^polar are both one. The two exponential widths in the published Chevet bound are

    E sup_(v in K) <E_D,v> = E||T E_D||_(m),
    E sup_(u in L^polar) <E_n,u> = E||E_n||_(k).

Equation (3) bounds these by the two terms of the claimed scale. Theorem3.1 proves the expectation bound.

For the deviation inequality, Corollary3.2 has variance-scale parameter sigma=R(K)R(L^polar)=1 and coordinate parameter

    sigma_prime = sup_(v in K)||v||_infinity
                    sup_(u in L^polar)||u||_infinity <=1.

Its tail is at most exp(-c min(t^2/sigma^2,t/sigma_prime)), which is no larger than the right side of (1). This proves the stated deviation bound after absorbing the width constants into C.

If D>N, K has empty interior in R^D, while the source states the theorem for convex bodies. To justify this step explicitly, apply it first to K_epsilon=K+epsilon B_2^D. Its Euclidean radius is at most1+epsilon; its exponential width is the width of K plus epsilon E|E_D|; and its coordinate radius is at most1+epsilon. For each fixed finite D, let epsilon decrease to zero. The random suprema decrease to the desired supremum; expectations converge by domination by the epsilon=1 supremum, which is integrable by the source theorem. For the tail, fix0<t'<t. Once epsilon is small, the source threshold for K_epsilon with deviation t' is below the limiting threshold with deviation t. The strict-exceedance event for K is then contained in the source event for K_epsilon. Let epsilon decrease to zero in the bound, and then let t' increase to t in its continuous numerical right-hand side. Thus no dimension-dependent epsilon term remains.

## 3. The class really contains non-unconditional laws

In dimension two take

    T = [[3/5,-4/5],[4/5,3/5]],

and take Z to have independent variance-one symmetric exponential coordinates. Then TT*=I and X=T Z has density proportional to

    exp(-sqrt(2) ||T* x||_1).

At x=(1,2), ||T*x||_1=13/5; at the coordinate-sign flip (-1,2), it equals3. The density is different, so this law is not unconditional. Independent rows with this law are covered by (1). Higher-dimensional examples follow by block-diagonal extensions. Rotations preserving coordinate sign symmetry are not needed.

The conclusion also holds for common orthogonal images of independent unconditional log-concave rows with dependent coordinates. The latent matrix, not its transformed image, is the object to which the Chevet theorem is applied.

## 4. What this route excludes and what remains

Searching for a counterexample merely by a common rotation, or more generally by a common isometric quotient, of unconditional latent rows cannot disprove the corrected conjecture. The sharp scale and benchmark tail hold throughout that class.

The missing step for arbitrary independent isotropic log-concave rows is a valid replacement for the common latent unconditional representation. Coordinate symmetrization of a general log-concave vector need not preserve the needed law or log-concavity, and the published arbitrary-norm comparison is known to fail. Nothing above supplies such a reduction. Subsequent substantive turns should test row-dependent transforms, genuinely non-unconditional convex bodies or a different chaining mechanism. The source correction and this theorem must remain separate from a claimed full solution.
