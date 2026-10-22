# Weighted operator boundary and a uniform one-sided exponential mark

Shared PASS3, row1778 /30005770, 14 October 2026.

## Scope and exact inputs

Let a_n=|Av_n(1324)|, a_0=1, lambda=lim a_n^(1/n), and rho=1/lambda. Skew-sum closure gives a_n<=lambda^n, and 4<=lambda<infinity. Use the accepted canonical greedy staircase kernel K(A,C) on nonempty 213-avoiding states. A and C are ordered: K is not assumed symmetric. Put w_A=z^|A| and

    F(z)=sum_{n>=0} a_n z^n,
    h_A(z)=1+sum_C K(A,C) w_C h_C(z),
    ell_A(z)=1+sum_B ell_B(z) w_B K(B,A).

All sums have nonnegative coefficients and mean the minimal path-sum solutions. For 0<z<rho they are finite, and

    F(z)-1=sum_A w_A h_A(z)=sum_A w_A ell_A(z).

These are exact counts of uniformly weighted permutations, not a new random path model. The once-marked series needed for a largest-cell proof is

    H(z,u)=sum_A u^|A| w_A ell_A(z) h_A(z).                 (1)

The accepted PASS2 exact transfer is `pass2_staircase_bias/EXACT_GREEDY_TRANSFER.md`, SHA-256 dfbab3a20d05861a7c4aba868b89a225f2ac5db201a467358f015f6efabe2b03. The accepted frontier amplification is `pass1_concentration/ACTIVE_FRONTIER_PROOF.md`, SHA-256 6058827dafd2c16dc53c66452c4da6cc010619d80508b07a08eaaaaffdc6957b. The PASS3 structural reciprocal-pair certificate used below is `pass3_kernel_feasibility/SQUARED_KERNEL_GAP_IMPOSSIBLE.md`, SHA-256 99e3262041ff09e1ce308fbc5a13704d286602e0eb5af7d814d99915848c314f.

The primary staircase source is Bevan, Brignall, Elvey Price and Pantone, *A structural characterisation of Av(1324) and new bounds on its growth rate*, Proposition 1 and proof, and Theorem 8:
https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf
The present proofs use the explicitly stated earlier lemmas; no numerical growth estimate or finite-data radius extrapolation is used.

## A. No positive diagonal reweighting makes the kernel Hilbert--Schmidt beyond rho

For each z>0, let (q_A) be any family of finite strictly positive real numbers. They may depend on z. Define the entrywise reweighted matrix

    B_q(z)_(A,C)=z^((|A|+|C|)/2) K(A,C) q_C/q_A.           (2)

We deliberately call this an entrywise reweighting. If q or 1/q is unbounded, it need not be a similarity of everywhere-defined operators on ell^2.

**Theorem A.** For every z>rho and every such family q,

    sum_{A,C} |B_q(z)_(A,C)|^2 = infinity.                  (3)

**Proof.** Write T_n=sum_{|A|+|C|=n}K(A,C)K(C,A), with both states nonempty. The reciprocal-pair encoding in the cited PASS3 certificate gives

    a_n<=T_(n+4) for every n>=0.                           (4)

For any finite state set E, apply 2xy<=x^2+y^2 to each ordered reciprocal pair in E x E, with

    x=z^((|A|+|C|)/2) K(A,C) q_C/q_A,
    y=z^((|A|+|C|)/2) K(C,A) q_A/q_C.

The diagonal weights cancel in xy. Swapping A,C permutes E x E, so

    sum_{A,C in E}|B_q(z)_(A,C)|^2
       >=sum_{A,C in E}z^(|A|+|C|)K(A,C)K(C,A).

Increase E through all states of size at most M and let M tend to infinity. Monotone convergence of nonnegative sums and (4) give, in the extended reals,

    sum_{A,C}|B_q(z)_(A,C)|^2
       >=sum_n T_n z^n >= z^4 F(z).                        (5)

Since the radius of F is rho, F(z)=infinity for positive z>rho. This proves (3). The same argument also applies at z=rho if F(rho)=infinity; no assertion about that boundary value is needed or made. QED.

This excludes any attempt to repair the impossible unweighted squared-growth gap by a positive diagonal Hilbert--Schmidt reweighting extending to a positive real point beyond rho. It does not exclude bounded operators, compact operators that are not Hilbert--Schmidt, different spaces, or estimates valid only below rho. It says nothing against the conjectured permuton limit.

## B. Absolute frontier counts have a uniform exponential size bound

The following statement applies generally to tau=alpha skew-sum 1 with |alpha|>=2. Let a_n count tau-avoiders, lambda=lim a_n^(1/n), and L(sigma) be the first alpha-occurrence endpoint, or n+1 if alpha is absent. Define

    N_n(m)=|{sigma in Av_n(tau): L(sigma)>=m}|,  m>=1.

The accepted finite amplification states, for every t>=0,

    N_n(m) B(m,t)<=a_(n+t)<=lambda^(n+t),
    B(m,t)=[s^t] C(s)^m,
    C(s)=(1-sqrt(1-4s))/(2s).                             (6)

The zero-count case m>n+1 is included. Fix 0<s<rho=1/lambda. Multiply (6) by s^t and sum over t>=0 to get the exact estimate

    N_n(m)<= lambda^n / [(1-lambda s) C(s)^m].             (7)

The left generating series converges because s<rho<=1/4. The right is a geometric series, so no saddle estimate or limit interchange of signed terms is involved.

**Theorem B.** Put gamma=log C(1/lambda)>0. For every 0<eta<gamma there is a constant C_eta<infinity such that, simultaneously for every n>=0 and integer m>=1,

    N_n(m)<=C_eta lambda^n exp(-eta m).                    (8)

**Proof.** By continuity and monotonicity of C on [0,1/4], choose s<1/lambda with log C(s)>eta. Equation (7) implies (8), for example with C_eta=(1-lambda s)^(-1). This includes lambda=4. QED.

This is an absolute count bound. Dividing by a_n retains the exact uniform law; lambda^n/a_n is subexponential but is not silently replaced by a constant.

## C. A fixed exponential mark for the first greedy cell

Return to 1324. Let T(pi) be the first greedy cell size: the largest top-value interval avoiding 213. The bijection pi -> reverse(pi^{-1}) maps Av_n(1324) onto Av_n(4231), where 4231=312 skew-sum 1, and takes that interval to the longest 312-free prefix. Hence

    T(pi)=L(reverse(pi^{-1}))-1.                           (9)

The equality includes the absent-pattern sentinel. The counts and lambda are identical under this bijection. Consequently, with gamma=log C(1/lambda), every 0<eta<gamma admits C_eta' such that

    |{pi in Av_n(1324):T(pi)>=m}|
       <=C_eta' lambda^n exp(-eta m)                       (10)

for all n,m>=1.

**Theorem C.** For every 1<u<C(1/lambda) and every 0<z<rho,

    G_first(z,u):=sum_A u^|A| z^|A| h_A(z)<infinity.        (11)

The same u works for every subcritical z.

**Proof.** Choose eta with log u<eta<gamma. For each nonnegative integer T,

    u^T=1+(u-1)sum_{m=1}^T u^(m-1).

Summing this identity over permutations of size n and using (10) bounds sum_pi u^T(pi) by a constant (depending on eta,u only) times lambda^n. Therefore its z-series converges whenever lambda z<1. The exact path decomposition identifies this series, after excluding n=0, with (11), because the first state has size T(pi) and its remaining continuations contribute h_A(z). QED.

This improves a mere pointwise linear-tail statement to a common positive exponential marking radius over all z<rho. However, (11) lacks the incoming factor ell_A in (1). It does not prove that a cell at an arbitrary index has an exponential mark. In particular, ell_A cannot be discarded or bounded uniformly without a new argument.

## D. An always-valid subcritical weighted contraction

For 0<z<z'<rho, define the outgoing transition T_z by

    (T_z f)_A=sum_C K(A,C)z^|C| f_C,

and the weighted supremum norm ||f||_(h(z'))=sup_A |f_A|/h_A(z'). Since every state is nonempty,

    sum_C K(A,C)z^|C|h_C(z')
       <=(z/z')sum_C K(A,C)(z')^|C|h_C(z')
       =(z/z')[h_A(z')-1].                                (12)

Thus T_z is a bounded positive operator on this weighted space with norm at most z/z'<1. Absolute convergence for every f in the space follows from the same bound. Its Neumann resolvent is consequently bounded. Applying the identical argument to the reversed transition with weight ell(z') gives an incoming weighted contraction.

These are actual subcritical operator estimates and do not require symmetry, Hilbert--Schmidt membership, or truncation limits. Their weights depend on z' and can grow with the state. They do not yield a common exponential factor for the product ell_A(z)h_A(z), and hence do not close (1).

## Remaining mathematical boundary

A sufficient route still is to establish, for some fixed u>1, finiteness of H(z,u) for all z<rho, or another exact coefficient estimate suppressing a positive mass in large cells. The new positive estimate (11) controls the outgoing half of that expression. Theorem A proves that one broad two-sided smoothing mechanism cannot bridge the gap for this exact kernel. Neither statement resolves the 1324 weak limit or the universal fixed-alpha target.
