# Arbitrary-length low-chain runs: an actual kernel growth gap

Final shared PASS5, row1778 /30005770, 14 October 2026. This is an unconditional partial theorem under the exact uniform1324 law. It does not prove the full increasing-pair estimate or the permuton limit.

## 1. Setting and main statement

Let a_n=|Av_n(1324)|, a_0=1, lambda=lim a_n^(1/n), and let A_1,...,A_r be the exact normalized canonical staircase states. Every state is a nonempty213-avoider; their directed edge multiplicities are the accepted kernel K.

Put

    H_2={A in Av(213): A nonempty and LIS(A)<=2}.

Let b_m count size-m1324-avoiders all of whose canonical states belong to H_2. This allows an arbitrary number of cells. Equivalently, b_m is the total weight of all nonempty finite K-paths of total state size m with every state in H_2.

**Theorem A.**

    limsup_m b_m^(1/m)<=8.                                  (1)

A marked low-chain run means any nonempty consecutive block of canonical cells, all of whose normalized states belong to H_2. The run need not be maximal, and its number of cells is unrestricted. Its mass m is its total number of points; its boundary mass is the sum of the sizes of its immediately preceding and following cells, with a missing neighbor assigned size zero. Define

    Phi(delta)=(2+delta)log(2+delta)-2log2-delta log(delta),
    Phi(0)=0.

**Theorem B.** For every epsilon in (0,1] and delta>=0 such that

    Phi(delta)<log(lambda/8),                               (2)

one has

    limsup_n (1/n)log P[Pi_n has a low-chain run of mass
           >=epsilon*n and boundary mass<=delta*(run mass)]
       <=-epsilon[log(lambda/8)-Phi(delta)]<0.               (3)

Here Pi_n is exactly uniform on Av_n(1324). In particular, the growth gap does not deteriorate when the number of cells in the run grows with n.

The gap is genuinely positive: the inspected primary staircase paper, Bevan--Brignall--Elvey Price--Pantone, *A structural characterisation of Av(1324) and new bounds on its growth rate*, Theorem9, pp.13--14, proves lambda>=81/8=10.125. Only lambda>8 is needed. The stronger bound in its Theorem16 is not needed for (3).
https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf

## 2. Exact enumeration of the allowed states

For p>=1 write A_p=1 direct-sum J_(p-1), with J_0 empty, so A_1=1.

Take any213-avoider and decompose it around its minimum as L,1,R. Every L value exceeds every R value; otherwise l,1,r would form213. If LIS<=2, R must be decreasing, because the minimum followed by an increasing pair of R would form a chain of length3. Recursing on L shows that the state is a skew sum of blocks A_p.

Conversely each such skew sum avoids213 and has LIS<=2. Each A_p is skew indecomposable, including the singleton convention, so this decomposition is unique. Therefore states of size c are in bijection with compositions of c, and

    |H_2 intersect S_c|=2^(c-1),       c>=1.                 (4)

This class is much broader than the single-block family A_p.

## 3. A positive weighted contraction proves Theorem A

For z in (0,1/8), set

    t=C(2z)=(1-sqrt(1-8z))/(4z),       f_A=t^|A|.

Then 1<t<2 and t=1+2zt^2, equivalently (1-2zt)^(-1)=t.

Restrict the actual transition to H_2:

    (T_z v)_A=sum_(C in H_2) K(A,C) z^|C| v_C.

Every allowed shuffle is a binary interleaving, so K(A,C)<=binom(|A|+|C|,|C|). Using the exact state count (4), for a=|A|,

    (T_z f)_A
      <=sum_(c>=1) 2^(c-1) binom(a+c,c)(zt)^c
      =[(1-2zt)^(-a-1)-1]/2
      =[t^(a+1)-1]/2
      <=(t/2)f_A.                                         (5)

Thus T_z is a bounded positive operator on the weighted supremum space with norm sup_A |v_A|/f_A, with operator norm at most t/2<1. Absolute convergence follows from the same majorant. Since 1<=f_A, its minimal outgoing path sum satisfies

    h_A^restricted(z)<=f_A/(1-t/2).

The full starting sum is finite:

    sum_(A in H_2) z^|A|f_A
      =sum_(a>=1)2^(a-1)(zt)^a
      =zt/(1-2zt)=zt^2=(t-1)/2.

Consequently the nonempty restricted-path generating function satisfies

    sum_(m>=1)b_m z^m <= (t-1)/(2-t)<infinity               (6)

for every z<1/8. The exact canonical path theorem identifies these paths with the stated actual avoidance subfamily, including all shuffle multiplicities. Equation (6) proves (1) by the radius formula. No equality of its growth with8 is claimed, and no finite-coefficient extrapolation is used.

## 4. Cutting a marked run retains both full exterior counts

Let Z_(n,m,delta) count all pairs (pi,marked low-chain run) of size n, run mass m, and boundary mass at most delta*m. Then the exact finite upper count is

    Z_(n,m,delta)
      <=(n-m+1) a_(n-m) b_m
          binom(2m+floor(delta*m)+1, floor(delta*m)).        (7)

Proof: cut the normalized path immediately before and after the marked run. The internal path contributes exactly b_m possibilities. For exterior masses p,q with p+q=n-m, the prefix and suffix paths contribute a_p a_q possibilities. They are full paths with all their old multiplicities retained; neither exterior is sampled as a supposedly uniform conditional remainder.

Let l,r be the sizes of the adjacent exterior cells, or zero when the respective exterior is empty. Restoring the two missing edges costs at most

    binom(m+l,l) binom(m+r,r),

because each internal endpoint has size at most m. With k=l+r, the negative-binomial convolution identity bounds this single product by

    sum_(j=0)^k binom(m+j,j)binom(m+k-j,k-j)
       =binom(2m+k+1,k).

This increases with k, so the boundary restriction bounds it by the binomial factor in (7). Discard the restriction on the exteriors after making this bound. Skew-sum closure gives a_p a_q<=a_(n-m), and summing over the n-m+1 possible p proves (7).

There is no extra uncontrolled factor for the number of cells in the run. Its whole path, including its length and all its states, is already among the b_m objects. Its marked location is determined by the chosen prefix path. Invalid reconstructions only decrease the upper count.

## 5. Exact uniform normalization and exponential rate

Divide (7) by a_n and sum over m>=ceil(epsilon*n). By skew closure/Fekete, a_j<=lambda^j and log a_n=n log lambda+o(n). Theorem A implies that for each fixed G>8 there is a finite C_G with b_m<=C_G G^m for all m. Stirling gives, uniformly for epsilon*n<=m<=n,

    log binom(2m+floor(delta*m)+1, floor(delta*m))
       =m Phi(delta)+O(log(m+1)).

Choose 8<G<lambda with Phi(delta)<log(lambda/G). The logarithm of the mth normalized upper summand is at most

    -m[log(lambda/G)-Phi(delta)]+o(n).

The factors polynomial in n and the at-most n values of m contribute only o(n). Taking limsup and then letting G decrease to8 gives (3). The ratio lambda^n/a_n is kept as exp(o(n)); it is not replaced by a fixed constant.

## 6. Dense cross-pair geometry inside the low-chain class

For p,q>=2, the actual kernel between the single-block states A_p,A_q has the exact form

    K(A_p,A_q)=binom(p+q-2,q),
    K_inc(A_p,A_q)=(pq/2)binom(p+q-2,q).                    (8)

Here K_inc sums the number of increasing cross-cell pairs over the genuine allowed shuffles, including the greedy condition.

To prove (8), the upper pattern A_p has increasing pairs only from its first point to a later point. The lower pattern S(A_q)=J_(q-1) direct-sum1 has increasing pairs only ending at its last point, the lower maximum. Greediness puts that lower maximum after the first upper point and before another upper point. A lower point before the first upper point would then combine with those three witness points to form1324. Thus the first letter is U. Because the lower maximum is last among lower points and needs an upper point after it, the last letter is U.

Conversely, any binary word beginning and ending U is valid. It has the greedy witness, and no possible two-color1324 can start with a lower point before the first upper point. The middle word is an arbitrary shuffle of q lower and p-2 upper points, proving the K formula. Each lower point makes an increasing pair with the final upper point. Each of the p-2 middle uppers has q/2 preceding lower points on average under the uniform middle word. The mean cross count is therefore q+(p-2)q/2=pq/2, proving the K_inc formula. The possibly half-integral mean causes no issue; the total in (8) is an integer.

Conditional on a full state chain under the exact uniform law, its edge shuffles are independent and uniform in their actual K sets. Thus pq/2 is also the exact conditional mean at this edge regardless of the exterior paths. Both endpoint states contain an ascent and can occur internally. Their individual LIS values are2 and their internal increasing-pair counts are only p-1,q-1.

This rules out a proposed statewise estimate that cross-pair density vanishes merely because the endpoint LIS values are small. The growth theorem controls entire low-chain runs rather than pretending that their internal edges are harmless.

For the narrower family containing only the single-block states A_p with p>=2, (8) also gives a stronger operator certificate at z=1/4. With f_p=2^p,

    sum_(q>=2) K(A_p,A_q)4^(-q)f_q
       =2^(p-1)-1-(p-1)/2 <= f_p/2.

Its nonempty path generating function is at most1 at z=1/4, so that narrower family has total-size growth at most4. The broader theorem above is the useful extension to all states of LIS<=2.

## 7. Remaining scope

Theorem B suppresses macroscopic low-chain runs only when their boundary mass is small relative to the run. It does not show that all such runs are small without that hypothesis. States of LIS>=3 and configurations with large boundary cells remain uncontrolled. A run outside H_2 can still have LIS=o(n) in every cell, so this finite-height result is not a proof of the needed within-cell chain tail.

The exact pair identity still requires an o(n^2*a_n) bound on both its within-state and cross-edge completion-weighted coefficients. Neither the restricted-path growth bound nor the conditional mean formula establishes that global estimate. In particular, the unconditional uniform avoidance law has never been replaced by uniformity on this restricted path class.

## Inputs and source-status limits

The exact canonical kernel and the definition of K_inc are the accepted PASS2/PASS4 inputs. The two-boundary reconstruction is reproved above with an internal class of arbitrary path length. The primary source was reopened and its Theorem9 inspected on14 October2026; the only numerical fact used for the positive gap is the rigorous lower bound81/8>8, not a conjectured or fitted growth constant. Its Theorem16 states the stronger rigorous lower bound10.271012. No claim about the latest optimal bound is needed.

Finite checker results, independent reviews, exact source pins and the deliverable manifest are separate. They supplement, rather than replace, the all-size proofs. Earlier accepted artifacts and the queue/ledger remain unchanged.
