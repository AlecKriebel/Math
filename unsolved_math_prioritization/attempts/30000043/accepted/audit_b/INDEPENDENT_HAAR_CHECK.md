# Independent check of the explicit Haar construction

This check is independent of the complex-perturbation bridge and does not depend on a literature counterexample.

Let h=1_[0,1/2)-1_[1/2,1), Df(x)=sqrt(2)f(2x), T_k f(x)=f(x-k), and e_(j,k)=D^jT_kh. The Haar family is an orthonormal basis for all L²(R). Define the isometry V on this basis by

    V e_(j,k)=e_(j+1,2k).

The index map is injective, so this extends to an isometry of all L²(R). Its adjoint is

    V* e_(j,k)=e_(j-1,k/2) if k is even, and 0 if k is odd.

For epsilon=1/100 and A=I+epsilon V, set phi=h+epsilon Dh. The relation T_kD=DT_(2k) implies exactly

    D^jT_k phi=A e_(j,k).

Since ||epsilon V||<1, A is boundedly invertible and this is a Riesz basis for all L²(R), with frame bounds (1-epsilon)² and (1+epsilon)². Its frame operator is F=AA*.

The canonical tightening has atoms Q e_(j,k), where Q=(AA*)^(-1/2)A. Write

    E=AA*-I=epsilon(V+V*)+epsilon²VV*,
    q=2epsilon+epsilon²=201/10000<1.

The norm-convergent binomial series gives

    (I+E)^(-1/2)=I-E/2+B,
    ||B||≤q²/(1-q),

because the absolute binomial coefficients after the constant term are at most 1. Multiplying by I+epsilon V and collecting the first-order term gives

    Q=I+(epsilon/2)(V-V*)+R,
    ||R||≤(3/2)epsilon²+(1/2)epsilon³
               +(1+epsilon)q²/(1-q)
           <1/1000.                                         (1)

The three explicit polynomial contributions to R are

    -(epsilon²/2)VV*,
    -(epsilon²/2)(V+V*)V,
    -(epsilon³/2)VV*V,

and the remaining contribution is B(I+epsilon V). This verifies (1) without truncating the underlying Hilbert space.

Let T=T_1. Since Th=e_(0,1), V*e_(0,1)=0, V*h=e_(-1,0), and TVh=T e_(1,0)=e_(1,2)=VTh,

    (V-V*)Th-T(V-V*)h=T e_(-1,0).

This vector has norm 1. Therefore

    ||QTh-TQh||≥epsilon/2-2||R||>3/1000.

Finally, Tphi=ATh is the atom at (j,k)=(0,1), so

    QTh-TQh=F^(-1/2)Tphi-TF^(-1/2)phi.

This is precisely the required nonzero canonical-tight translation defect under the fixed-index contract. The candidate generator is forced by index (0,0); no other single generator can repair the failed identity.

All calculations work over both real and complex L²(R). There is no numerical approximation in the proof. No novelty assertion is made.
