# Independent pre-review reconstruction

This note was written after reading the source definition and operative primary Section 5, but before opening the submitted PARTIAL/proofs/code/review. It is a verification route, not a new attempt at the unresolved exact-shift claim.

Put L_0=0 and L_j=sum_{i=1}^j T_{-i}. On the j-th negative-side interval, k=-j-1, u=t-L_j, T=T_k, and Y_t=X_{-t}, one has

Y_{L_j+u}=Y_{L_j}+B^k_{T-u}-B^k_T.

Define W_{L_j+u}=Y_{L_j}-B^k_u. W agrees with Y at both joins, and is obtained by reversing time and reflecting space on each displayed negative-side piece. Its successive driving pieces are (-B^{-1},T_{-1}), (-B^{-2},T_{-2}), ... in this order. They are independent; -B^k is Brownian for the same normal filtration and T_k remains a stopping time. Strong Markov gluing makes W standard Brownian motion. No iid, equilibrium origin, optional stopping identity, or cyclic rotation at an endogenous cut is required. Zero lengths can be skipped, and divergence assures that every fixed finite time is covered after finitely many indexed pieces almost surely. W is independent of the positive half because it uses only negative-index marks.

The exact discrepancy is

Y_{L_j+u}-W_{L_j+u}=B^k_{T-u}+B^k_u-B^k_T
 =W_{L_j}+W_{L_j+T}-W_{L_j+T-u}-W_{L_j+u}.

With T<c, it is bounded by twice the Brownian oscillation on time separations c. Thus at diffusive scale a, the sup discrepancy over any fixed rescaled compact interval is bounded by twice the modulus of a^{-1/2}W_{a t} at mesh c/a (over a slightly enlarged compact). Brownian scaling and continuity make that bound vanish in probability. This proves a candidate weak-limit statement for Y and its independence in the limiting two-sided assembly. It does not produce one finite random shift S of the original unscaled X.

A test that Y itself has Brownian law at 0 is not the source target. Even iid bounded stopping times can make the negative reversed piece locally biased, while the primary theorem allows a different random origin. A stationary renewal construction is a separate law argument requiring iid marks and finite mean; it cannot be reused for arbitrary non-iid marks.

Falsification priorities: orientation/sign/index errors in W; anticipated stopping times falsely passed to optional sampling; paths extended past T using already-conditioned future; confusing forward-endpoint moments with negative fixed-time laws; common-c replacement by indexed c_k; a rotation that uses circular exchangeability at a path-dependent cut; replacing the given non-iid sequence by iid/equilibrium marks; mistaking a scaling limit for an exact finite random recentering.
