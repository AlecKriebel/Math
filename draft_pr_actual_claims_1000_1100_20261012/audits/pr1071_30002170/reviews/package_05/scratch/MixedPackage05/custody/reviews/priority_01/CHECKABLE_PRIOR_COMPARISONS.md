# Checkable priority comparisons for PR1071

Audit date: 14 October 2026 UTC. These are authored deductions, not quotations or claims of independent historical firstness.

## 1. Exact target and estimator comparison

Let X_T = integral_0^T B^1 dB^2 be the canonical iterated integral of independent standard fBm components with the same fixed H in (1/4,1). Put G_n = sigma(B^i_{jT/n}: i=1,2; 1<=j<=n) and e_H(n,T) = ||X_T-E[X_T|G_n]||_2. The target is e_H(n,T) >= c_H T^(2H) n^(1/2-2H) for all T>0 and n>=1, with c_H>0 depending only on H. Conditional projection shows that this is equivalent to the same lower bound for every F in L2(G_n).

The endpoint product B^1_T B^2_T is observed. If A_T = (I_12-I_21)/2, geometric integration by parts gives A_T = X_T - B^1_T B^2_T/2. Therefore its optimal conditional residual equals that of X_T. The unhalved antisymmetric difference 2A_T has twice that residual. A prior theorem for a differently normalized area must be converted by this equality before comparison.

## 2. Brownian prior entails the entire Brownian slice

The OWR original pp.2524-2525 and the Neuenkirch-Shalaiko author text Remark5 give e_{1/2}(n,T)=T/(2 sqrt(n)). Thus the target holds in this slice with c_{1/2}=1/2 for all n and T. No new lower rate, constant, all-n coverage, or optimum is supplied by the submitted weaker witness at H=1/2. This is exact supersession of this slice.

An elementary check uses independent cells: on a cell of length Delta, E[I^2]=Delta^2/2, E[(Delta B1 Delta B2)^2]=Delta^2, and E[I Delta B1 Delta B2]=Delta^2/2. Subtracting half the observed increment product leaves variance Delta^2/4. Summing independent residuals gives T^2/(4n).

## 3. Smooth prior and the finite-n distinction

Neuenkirch-Shalaiko Theorem1 in the July14,2015 author preprint, independently matched by Shalaiko thesis Theorem3.3 p56, assumes H>1/2. For the same X and both sampled components it gives positive liminf and finite limsup of n^(2H-1/2)e_H(n,T)/T^(2H). This already supplies the optimal asymptotic lower rate in the whole smooth interval. The reported theorem is not an exact normalized-error limit or a sharp constant.

A positive liminf by itself does not imply a bound for initial n: a sequence could vanish at an initial index. There is a checkable supplementary argument here. For any fixed n, a single nonzero smooth covariance path pair supported inside one cell and vanishing on the grid yields invisible Gaussian variables U,V with E[X_T UV] = integral f g' !=0. Cauchy-Schwarz then makes e_H(n,T)>0. This uses the standard Gaussian/Fourier dual test, as explicitly derived in the submitted proof; it does not require its simultaneous n-cell Gram estimate. Self-similarity gives e_H(n,T)=T^(2H)e_H(n,1). If the prior liminf is L_H>0, choose N_H so normalized errors are >=L_H/2 for n>=N_H and take the minimum with the finitely many positive normalized errors for n<N_H. That produces an H-only positive all-n constant.

Consequently the finite-n qualitative strengthening in the smooth interval is a routine deduction after nonrecoverability; it must not be advertised as resolving an unproved smooth rate. The explicit displayed witness constant is a quantitative choice from this proof, not a claim that no earlier explicit bound exists.

## 4. Why Euler or trapezoid error lower bounds do not entail the target

For any fixed grid estimator Q_n, orthogonal projection gives exactly

    ||X_T-Q_n||_2^2 = e_H(n,T)^2 + ||E[X_T|G_n]-Q_n||_2^2.

A lower bound on the left permits the first term to be zero. Thus the NTU Euler asymptotics, a sharp lower bound for one Milstein approximation, or a nondegenerate limiting error distribution for a specified scheme cannot be promoted to an information lower bound without additional control of the second term or of the conditional residual itself. Neither a stable weak limit independent of the limiting path nor an a.s. rate of one approximation fixes this missing uniform-in-estimator fact.

The NTU journal-formatted institutional copy Theorem2 p226 gives an upper bound for the trapezoid scheme for H>1/4 and states the conditional lower estimate as a conjecture. Its Theorem1 p225 concerns Euler. It is exact background for the upper rate, not a prior solution of the rough conditional lower target.

## 5. Why the older smooth proof cannot simply be extended below one half

NS Theorem2 and Shalaiko thesis Theorem2.2 use Var(sum a_j Delta_j B) >= c sum a_j^2 Var(Delta_j B) for H>1/2. With T=1, a_j=1, the left is 1 and the right is c n^(1-2H). No positive c independent of n exists for H<1/2. The contradiction is in both primary bodies. Reusing that proof at rough H without replacing this step is blocked.

The submitted selected covariance paths use the reverse operator inequality: Gram(u^r_0,...,u^r_{n-1}) <= M_r I. A bounded periodized weighted Fourier transform proves this for the two smooth compactly supported shapes. It is not a disguised extension of the false increment lower bound. NS local nondeterminism gives one-point first-chaos information; it does not by itself produce the simultaneous quadratic-area accumulation and upper Gram control needed here.

## 6. Gaussian tensor formulation and the exact remaining corollary gap

Let O_n be the span of the observed K_{jT/n} in the isonormal space and P_n its orthogonal projection. Finite left sums have kernels

    A_m = sum_k K_{kT/m} tensor (K_{(k+1)T/m}-K_{kT/m}).

The independent-component isometry gives ||I_{1,1}(A_m)||_2=||A_m||_{K tensor K}. Established L2 area convergence makes these kernels Cauchy; write their limit A_T. Independence and Gaussian conditional expectation imply

    E[X_T|G_n] = I_{1,1}((P_n tensor P_n) A_T),
    e_H(n,T) = ||A_T-(P_n tensor P_n)A_T||.

For the submitted u_j^f,u_j^g in O_n-perp, set L_n=sum_j u_j^f tensor u_j^g. Then ||L_n||^2=tr(AC)<=n M_f M_g, while <A_T,L_n>=n a (T/n)^(2H). Cauchy-Schwarz gives the claimed inequality.

This demonstrates that nonlinear-estimator orthogonality is standard Gaussian projection geometry. Generic quadratic-functional or average-case multilinear results may formalize this projection identity; such an identity is not the missing fBm rate theorem. To make the exact rough target a corollary of prior literature, a source must additionally control the projected fBm area kernel at scale sqrt(n)(T/n)^(2H), or give a simultaneous family with these pairing and Gram properties. Merely restating the kernel norm as a target unsupported inequality transfers the central difficulty and is blocked. No read primary control supplied that missing estimate. The possibility of a relevant estimate in inaccessible method bodies remains UNKNOWN.

## 7. Rough volatility does not specialize to equal-H fractional area

NS arXiv1606.03854 has a rough fOU integrand and a Brownian stochastic integrator; its lower rate is n^(-H). Itô isometry and a Brownian innovation supply its positivity. The target has two equal-H fBm components, generally neither a semimartingale nor independent across time, and exponent n^(1/2-2H). Replacing the Brownian integrator by another rough fBm destroys the cited isometry and changes the covariance kernel. The desired substitution is an unsupported new lemma, not a direct specialization.

## 8. Foundational analogy does not establish methodological novelty

Wu-Xiao, Geometric Properties of Fractional Brownian Sheets, author version dated26Feb2006, Theorem2.1 proof pp5-6 uses harmonizable representation, local smooth bump functions, Fourier inversion and Cauchy-Schwarz to separate a point from observations. Xiao2006 Theorem3.1 pp174-175 discusses the same spectral dual-test lineage and refers to Pitt and Kahane. These are clear antecedents of the covariance-path localization idea. The submitted polynomial choices and periodization make a useful checkable implementation; no claim to invent local Fourier witnesses, Gaussian conditioning, Parseval periodization, or Cauchy-Schwarz lower bounds is justified.

The audit found no exact prior rough conditional theorem among the read controls. This negative bounded result is weaker than priority clearance. General Gaussian quadratic/multilinear method priority remains UNKNOWN, and no worldwide open-status or firstness conclusion follows.
