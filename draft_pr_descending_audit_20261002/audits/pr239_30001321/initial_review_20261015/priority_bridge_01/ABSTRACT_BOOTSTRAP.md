# A checkable transfer of the old multiscale mechanism

This is an independent audit derivation dated 2026-10-15, not a claim that the lemma below was stated in this form before that date. Its mechanism is the iteration in Berger–Cohen–Rosenthal (BCR), arXiv:1405.6819v1, Theorem 5.1, and the bad-box density refinement in Bethuelsen–Birkner–Depperschmidt–Schlüter (BBDS), arXiv:2105.09030v1, Section 8. It is written to distinguish an old mechanism from a previously authenticated theorem for the candidate's model.

## 1. Exact input needed

Let the environment consist of independent, identically distributed scalar probabilities p_(s,x) in (0,1), and let X have increments ±1. Write T_n for its annealed transition kernel, mu_t for its quenched law, and alpha_t for its annealed law. Fix gamma in (0,1/2) and b>0. Assume there are C,c,n0 such that, for all n>=n0, every deterministic interval partition Pi of length H>=n^gamma, and every starting space-time point z,

    P_env( L_(n,H)^z > n^(-b) ) <= C exp[-c(log n)^2].       (H)

Constants are uniform over deterministic alignments and starting points. The shift of the starting time is permitted by stationarity. Rounded lengths can be substituted by increasing constants or decreasing b. Assume also the following elementary binomial facts:

    sup_x alpha_t(x) <= C/sqrt(t+1),
    ||T_n(u,.)-T_n(v,.)||_1 <= C |u-v|/sqrt(n+1)            (D)

whenever u,v have the same parity. All measures at each fixed time lie on one parity class.

Conclusion: for all M sufficiently large and all sufficiently large N,

    P_env( L_(N,M) > C M^(-a rho/gamma)+C N^(-b) )
       <= C exp[-c'(log N)^2],                            (Q)

where rho is any fixed number in (2gamma,1), and any fixed 0<a<=min(b,1/2-gamma/rho,1/8) is allowed. In particular (Q) gives the exact target for every deterministic M_N tending to infinity, with no lower rate. It does not establish uniformity over environment laws.

## 2. Iteration geometry

The case M>=N^gamma follows from (H). Otherwise put n_j approximately N^(rho^j). Stop at the first r such that n_r^gamma<=M. Let t0=N-sum_(j=1)^r n_j, and t_j=t0+sum_(i=1)^j n_i. For large N, t0>=N/2 because the total of the decreasing n_j is O(N^rho). Choose any deterministic interval partitions with lengths h0=ceil(N^gamma), h_j=ceil(n_j^gamma) for j<r, and h_r=M with the actual target alignment. Let lambda_j be the coarse L1 discrepancy at t_j on the j-th partition.

For a stage with n=n_j, the old cell length h=h_(j-1) is at most C n^(gamma/rho), including j=1. Thus h/sqrt(n)<=C n^(-d), where d=1/2-gamma/rho>0. This is the reason for changing the square-root time shrink in the printed BCR choice: one polynomial scale gamma<1/2 suffices if rho>2gamma.

## 3. Exact one-step inequality

Call an old cell J bad if some reachable-parity starting site u in J fails (H) for the next segment and the new partition. By the union bound over at most h+1 sites,

    P(J bad) <= C n^A exp[-c(log n)^2]
             <= C exp[-c1(log n)^2] =: p_n.               (B)

No independence among sites inside J is needed. Replace mu_(t_(j-1)) inside each old cell by its quenched conditional distribution carrying the deterministic total mass alpha_(t_(j-1))(J). Call this measure mu_tilde. The three triangle-inequality errors are:

1. mu_old K_n to mu_tilde K_n: at most lambda_(j-1), by Markov-kernel contraction;
2. mu_tilde K_n to mu_tilde T_n on new cells: at most n^(-b)+2 B_j, where

       B_j=sum_(J bad) alpha_(t_(j-1))(J);

3. mu_tilde T_n to alpha_old T_n: at most C h/sqrt(n), by (D) inside each old cell.

The annealed semigroup is exact: alpha_old T_n=alpha_(t_j), because fresh time layers are independent. Therefore

    lambda_j <= lambda_(j-1)+n_j^(-b)+2 B_j+C n_j^(-d).     (R)

Zero-mass cells may be assigned an arbitrary same-parity conditional distribution. Merely elliptic p in (0,1) makes every annealed-reachable site quenched-reachable as well.

## 4. Why a terminal-scale union bound is insufficient

At the last stage n_r is only a power of M. A union bound on every bad cell with cost exp[-c(log n_r)^2] would give a tail in M, not a superpolynomial tail in N. For example M=log log N makes that cost much larger than N^(-K). The old bad-box density mechanism, rather than such a union bound, is essential.

For stages with n_j>N^(1/4), (B) permits a union over the O(N) relevant old cells and the O(log log N) stages. Here log n_j>log N/4, so the total failure is at most C exp[-c2(log N)^2]. On that event B_j=0 at these stages.

For the remaining stages n=n_j<=N^(1/4), badness of an old cell is a function only of the finite environment cone of length n from that cell. Badness variables of cells separated by more than 2n+h are independent. Color the deterministic old cells by their indices modulo D, where D<=C(1+n/h), so each color is an independent family. Set w_J=alpha_(t_(j-1))(J). Since t_(j-1)>=N/2,

    max_J w_J <= C h/sqrt(N),  sum_J w_J<=1,
    D sum_J w_J^2 <= C n/sqrt(N).                         (W)

The relevant set is finite, since the walk has bounded speed. To check the weighted concentration estimate, apply Hölder to the product of the D color moment-generating functions, then Hoeffding's lemma inside each independent color. This gives

    E exp[lambda sum_J w_J(1_bad(J)-P(J bad))]
        <= exp[C lambda^2 D sum_J w_J^2].

Optimizing lambda and using (W) yields

    P(B_j > p_n+t) <= exp[-c t^2 sqrt(N)/n].              (C)

Take t=n^(-b1), choosing a<=b1<=min(b,1/8), for example b1=a; this is possible under the stated cap on a. For n sufficiently large, p_n<=n^(-b1). The exponent in (C), for n<=N^(1/4), is at least c N^(1/4-b1/2). Thus simultaneous control B_j<=2 n_j^(-b1) has stretched-exponentially small failure in N. No independence between different stages is asserted or needed.

## 5. Sum and quantifiers

Input (H) gives lambda_0<=C N^(-b) outside C exp[-c(log N)^2]. For any fixed 0<a<=min(b,d,1/8), the preceding choice of b1 ensures a<=min(b,b1,d). Combine (R) with the stage controls using this a. Because n_(j-1) is approximately n_j^(1/rho),

    sum_(j=1)^r n_j^(-a) <= C n_r^(-a)
                           <= C M^(-a rho/gamma)

once M exceeds a fixed threshold. The first inequality is a convergent geometric comparison on the logarithms; the second follows from n_(r-1)^gamma>M and n_r approximately n_(r-1)^rho. This proves (Q). Rounding contributes only fixed multiplicative constants as M tends to infinity.

For every epsilon,K>0, choose the deterministic sequence threshold so that the right side in (Q)'s discrepancy bound is below epsilon. Then exp[-c'(log N)^2]<=C_K N^(-K). Alignments were arbitrary and deterministic throughout.

## 6. How the frozen TURN_2 supplies (H), and the dating boundary

This paragraph is a new quantitative reading of the submitted argument, not an earlier publication. In TURN_2 take

    gamma=5/16, beta=9/32, eta=1/64, b=1/128.

Apply all its fixed-u concentration steps with u proportional to n^(-b). The relevant exponents are:

    beta-eta-2b = 1/4 > 1/2-gamma = 3/16,
    2beta-1/2-eta-2b = 1/32 > 0,
    gamma-beta = 1/32 > b.

The boundary expectation is therefore negligible compared with n^(-b); the terminal sign union still has a positive exponent margin; and the boundary test still concentrates. The tail/killing terms of size exp[-c(log n)^2] remain of that order after division by n^(-b).

For the common overlap events one can choose moment order k proportional to (log n)^2, using the explicit k! C^k L^(k/2) bound in TURN_2. Their failures are at most exp[-c(log n)^2] for large n. Consequently the submitted proof gives (H), uniformly over H>=n^gamma and alignment. With rho=7/8, d=1/7, a=b=1/128 is allowed, and the displayed M exponent is 7/320.

The overlap input itself has a rigorous earlier source: BRAS06 Lemma 4.1 supplies G_L(0,0)=O(sqrt L) after the exact {0,1}-walk shear described in REPORT.md. The first-hit identity gives sup_z G_L(z,0)<=G_L(0,0). This yields conditional occupation bounds for arbitrary old mu, and ordered-time expansion gives the Kac k! moment estimate. Binomial gradients and scalar concentration are classical. Nevertheless, (H) for this scalar iid model is not stated by the BCR, BCD16, BRAS06, or BBDS theorems examined here. The new derivation of (H), or its reproduction from TURN_2, cannot itself authenticate an earlier publication date for that application.

Therefore this file completes a proof-level transfer and disproves any claim that the general all-scale bootstrap idea originated with this candidate. It does not, without an earlier dated scalar-model theorem or an explicitly general published theorem covering (H), authenticate a previous resolution of the exact scalar iid conjecture.
