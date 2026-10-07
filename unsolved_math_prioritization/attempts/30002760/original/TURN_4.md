# Approach 4: local Dörfler marking and a rate theorem

## Aim and disposition

Replace exhaustive search by local marking. The following conditional theorem isolates exactly the estimator and contraction properties that make the standard optimality argument work. It is a reconstruction of the established axioms-of-adaptivity mechanism, not a proof that all required properties hold robustly for the source's PDE class.

## Set-up

Use the refinement family, root T_0, complexity m(T)=#T-#T_0 and overlay bound from Approach 3. Each mesh has a discrete solution U_T and nonnegative indicators eta_T(K), with eta_T(S)^2=sum_{K in S}eta_T(K)^2 and eta_T=eta_T(T). Write d(T,H) for the distance between the two solutions in a fixed norm. Assume the following for every refinement H of T:

- There is R subset T containing T\\H, with #R<=C_R(#H-#T), and d(T,H)<=C_D eta_T(R).
- On the unchanged subset T\\R, eta_T(T\\R)<=eta_H(T\\R)+C_S d(T,H).
- Quasi-monotonicity: eta_H<=C_M eta_T, with C_M>=1.

The set T\\R consists of elements of H because R contains every removed element. For an adaptive sequence T_l, choose a set M_l satisfying Dörfler marking eta_l(M_l)^2>=theta eta_l^2 and cardinality at most C_mark times that of any qualifying set. Any bounded-factor additional marking is absorbed into C_mark. Assume mesh closure

m(T_l)+1 <= C_cl sum_{j=0}^{l-1}#M_j,  l>=1,

and R-linear estimator convergence

eta_{l+k} <= C_lin q^k eta_l, l,k>=0,

where C_lin>=1 and 0<q<1. All constants must be independent of l. For an epsilon-uniform conclusion they must also be independent of epsilon; that extra uniformity is not silently assumed from mere fixed-epsilon validity.

Let a=C_S C_D and 0<theta<1/(1+a^2). Choose 0<kappa<sqrt(1-theta)-a sqrt(theta). The upper bound is positive by the stated restriction on theta.

## Lemma 4.1 (reduction forces marking)

If eta_T>0 and eta_H<=kappa eta_T, then R satisfies Dörfler marking. Put r=eta_T(R)/eta_T in [0,1]. The assumptions give

1 = eta_T(T\\R)^2/eta_T^2 + r^2 <= (kappa+a r)^2+r^2.

If r^2<theta, monotonicity of the right-hand side for r>=0 gives
1 <= (kappa+a sqrt(theta))^2+theta <1,
a contradiction. Thus r^2>=theta. The strict kappa condition even excludes equality at the endpoint; only the non-strict marking conclusion is needed.

## Theorem 4.2 (conditional optimal exponent)

For s>0, define A_s=sup_{N>=0}(N+1)^s min_{m(P)<=N}eta_P. Assume A_s<infinity. If eta_l>0 throughout, then for every l>=1,

eta_l <= C A_s (m(T_l)+1)^-s,

where one valid constant is

C=[ C_cl C_mark C_R (C_M/kappa)^(1/s)
      C_lin^(1/s)/(1-q^(1/s)) ]^s.

Proof. Since T_l refines T_0, eta_l<=C_M eta_0<=C_M A_s. Define z=(C_M A_s/(kappa eta_l))^(1/s)>1 and N=ceil(z)-1, so 1<=N<=z and N+1>=z. Choose P with m(P)<=N and eta_P<=A_s(N+1)^-s; the minimum exists by finiteness. For H=T_l join P, quasi-monotonicity relative to P gives eta_H<=C_M eta_P<=kappa eta_l. The overlay inequality gives #H-#T_l<=N. Lemma 4.1 and minimal marking therefore imply

#M_l <= C_mark C_R N
       <= K A_s^(1/s) eta_l^-1/s,
K=C_mark C_R (C_M/kappa)^(1/s).

R-linear convergence from j to l implies
eta_j^-1/s <= C_lin^(1/s) q^((l-j)/s) eta_l^-1/s.
Insert the cardinality bound into mesh closure, sum the geometric series, and obtain

m(T_l)+1 <= C_cl K C_lin^(1/s)/(1-q^(1/s))
             A_s^(1/s) eta_l^-1/s.

Rearranging proves the result. If eta_l=0 occurs, an algorithm that terminates there has zero certified error whenever reliability holds; it needs no inverse-error estimates. This theorem concerns estimator classes. Identification with best solution approximation requires a further efficiency/oscillation comparison. Reliability alone only transfers the upper rate to solution error.

## Proposition 4.3 (plain convergence does not replace contraction)

Take abstract scalar data eta_j=1/(j+1), #M_j=j+1 and n_l=1+sum_{j<l}#M_j=1+l(l+1)/2. Then eta_j ->0 and #M_j=eta_j^-1, so the ideal cardinality bound for s=1 holds exactly. Nevertheless n_l eta_l=(1+l(l+1)/2)/(l+1) is unbounded. Thus eta_l is not O(n_l^-1); it has order n_l^-1/2. This is a counterexample to an implication between numerical assumptions, not a finite-element/PDE counterexample. It shows why the contraction hypothesis cannot simply be omitted from this proof.

## Remaining gap and credit

The local marking, overlay and geometric-summation strategy is established by the adaptive-FEM literature, including Carstensen-Feischl-Page-Praetorius (2014). The proof above exposes its needed constants in a self-contained special formulation. Erath-Praetorius verify a related framework only asymptotically for their stationary SUPG algorithm. A source-general parabolic, or parameter-uniform preasymptotic, verification of all hypotheses has not been supplied here.
