# Checkable implications and rejected shortcuts

This file contains original audit deductions. It does not assert a new RWRE theorem or certify the frozen proof.

## A. Fixed-width estimates really do imply every diverging width

Let alpha_N be a deterministic probability measure and mu_N a random probability measure on Z^d. Write L_P(mu,alpha)=sum_{Q in P}|mu(Q)-alpha(Q)|. Suppose, for each fixed integer m, there is a deterministic partition P_m into cubes of side m such that

    P(L_{P_m}(mu_N,alpha_N)>A m^{-a}+A N^{-a})=O(N^{-K})

for every K>0, where A,a>0 are independent of m. The eventual threshold and tail constants may depend on the fixed m. Suppose also that alpha_N has (i) maximum point mass at most C N^{-d/2}, and (ii) diffusive tightness around some deterministic center z_N: for every eta>0 one can choose R with alpha_N(|x-z_N|_infty>R sqrt(N))<eta eventually.

Then for every deterministic equal-cube partition T_N of side M_N→infinity, with arbitrary deterministic alignment, and every epsilon,K>0,

    P(L_{T_N}(mu_N,alpha_N)>epsilon)=O(N^{-K}).

Proof. Let B_N be the union of fine cells in P_m split by a boundary of T_N. Within an unsplit fine cell, coarsening cannot increase L1. Within a split cell J, writing A=mu(J), B=alpha(J), the sum of absolute differences on its target pieces is at most A+B≤|A−B|+2B. Summing gives the exact deterministic inequality

    L_{T_N}(mu,alpha) ≤ L_{P_m}(mu,alpha)+2 alpha(B_N).       (1)

In the diffusive window there are at most C_d R^d N^{d/2}(m/M_N+m/sqrt(N)) lattice points in split cells, with constants allowed to depend on the fixed m and R. Consequently alpha_N(B_N)≤C_{d,R} m/M_N+O_{d,R,m}(N^{-1/2})+eta. The bound is uniform in the target alignment. Fix eta≪epsilon; fix m so A m^{-a}<epsilon/4; then take N large along the specified sequence. Equation (1) reduces the target event to the fixed-m event. There is no union over m depending on N, no probability rate required of M_N, and no interchange of uncontrolled constants. This proves the claim.

It is enough instead to assume an L1 approximation of alpha_N by a parity-adjusted nondegenerate Gaussian mass function: apply (1) to that Gaussian and charge the deterministic o(1) L1 error. This avoids assuming that an L1 local limit statement by itself bounds every atom. A drift merely changes z_N. BCR also separately supplies the maximal-atom estimate in Lemma 2.14(2.2) and tightness in Lemma 2.16(3). Thus BCR2016 Theorem 5.1 proves the entire arbitrary-diverging-scale conclusion within its covered static d≥4 model, even under the conservative reading that its exceptional-probability constants apply only for fixed M. Likewise BBDS2024/2026 Lemma 4.1 plus its annealed local CLT proves the arbitrary-diverging-scale conclusion in its directed percolation-backbone model for d≥1. These are genuine prior all-scale theorems in their own models. The obstacle to applying them to the frozen target is model inclusion, not a slow-scale quantifier gap.

For one transverse dimension and geometric real target intervals, the number of split fine cells in a length-O(sqrt(N)) window is at most C_R sqrt(N)/M_N+O(1), so the same argument applies.

## B. A prefactor local limit theorem alone does not provide time-superpolynomial tails

A statement of the form ||mu_N−alpha_N f(shift_{x,N}omega)||_1→0 almost surely leaves the distribution of its error at finite N unspecified. Spatial ergodicity of f may yield averaging as M_N→infinity but likewise leaves its rate unspecified. Even a bound exp(−c(log M)^2) for a spatial average at width M does not imply O(N^{-K}) at M_N=ceil(log log(N+e^e)): here (log M_N)^2=o(log N).

This is a logical gap rather than evidence of failure of the desired RWRE theorem. For a concrete general non-implication, take one U uniform on (0,1) and Y_N=1_{U<1/log(N+e)}. Then Y_N→0 almost surely, but P(Y_N>1/2)=1/log(N+e), which is not O(N^{-K}) for any K>0. Almost-sure convergence is therefore insufficient even when it is eventually pathwise exact. Smooth-test convergence is weaker still.

## C. Weak CLTs and positive polynomial scales do not imply slow-scale L1

On L_N=2 r_N m_N lattice sites, let alpha_N be uniform. Let mu_N have density 2 relative to alpha_N on alternating blocks of m_N sites and density 0 on the intervening blocks. Then both are probability measures, and their discrepancy on the aligned m_N partition is exactly 1. Couple excess mass in an occupied block with the immediately following empty block. After scaling space by L_N, their Wasserstein-1 distance is at most m_N/(2L_N)=1/(4r_N), so they have the same weak limit when r_N→infinity. We may take m_N→infinity arbitrarily slowly while r_N≈sqrt(N)/(2m_N), making L_N diffusive.

On a coarser partition of width H, cancellation in each complete pair of blocks gives

    L_H ≤ 2m_N/H+2m_N/L_N,

uniformly in alignment. This tends to zero at every H=N^gamma with gamma>0 (provided the slow m_N=o(N^gamma)), while L_{m_N}=1. These measures are an abstract obstruction to a proposed implication, not an RWRE counterexample. A separate small-scale argument is mathematically necessary.

## D. Dimensional lifting changes or violates the model

Copying a target p_{t,x} into an extra spatial coordinate, tilde p_{t,x,z}=p_{t,x}, creates covariance Var(p)>0 between different sites sharing (t,x); the enlarged environment is not spatially iid. Replacing these copies by independent variables changes the quenched distribution after projecting away the auxiliary coordinate. An elementary favorable test already shows the issue: let a first-coordinate + step use p, and let an independent auxiliary ± coin branch into two distinct fresh sites. At time 2, the native +,+ quenched mass is p_0 p_1, whereas the independently enlarged projected mass is p_0(p_{1,+}+p_{1,−})/2. Put q=E p and s=E p^2. Their variances are respectively

    s^2−q^4,            s(s+q^2)/2−q^4,

whose difference is s Var(p)/2>0 for any nondegenerate law. This toy branching construction is not itself claimed to satisfy Berger's nearest-neighbor theorem; it isolates why fresh independent transverse copies are not a law-preserving cure.

For static uniform-ellipticity theorems, encode the 1+1 target by (u,v)=((t+x)/2,(t−x)/2), on the reachable parity class. A +1 transverse step becomes +e1 and a −1 step becomes +e2. Both negative-coordinate probabilities are identically zero. Hence every encoded law fails the static all-directions ellipticity hypotheses of BCR and Peretz, even if p is bounded away from 0 and 1. Adding small reverse probabilities produces a different model. Without uniform estimates in that added parameter, the limit cannot be interchanged with N→infinity: the elementary continuous example exp(−delta N) has superpolynomial N decay for each fixed delta>0 and equals 1 at delta=0.

BS2002 treats directed kernels separately, so this encoding is legitimate there; one must use its actual directed conclusion rather than importing its different uniformly elliptic high-dimensional results.

## E. What the exact finite checks validate

`implication_checks.py` uses rational arithmetic for 38,814 assertions: arbitrary-alignment inequality (1), abstract alternating-block controls, the two variance formulas for p∈{1/4,3/4}, and the zero backward directions of the NE encoding. The receipt is reproducible. These finite checks support the transparent analytic arguments above; they do not numerically certify any asymptotic theorem or resolve priority by themselves.
