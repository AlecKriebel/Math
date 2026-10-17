# Independent analytic acceptance: arbitrary-length low-chain runs

Final shared PASS5, 14 October 2026.

Reviewed: `pass5_pair_counts/LOW_CHAIN_RUN_THEOREM.md`, SHA-256 `cc9008beda1563339e9f308a2fb1987d38835c1af2c521fb87e7ebb5b7c715fa`.

**Accepted.** The restricted-path growth and isolated-run tail are unconditional partial theorems for the actual canonical kernel. They do not prove the full pair criterion or the uniform permuton limit.

## State enumeration and analytic domain

The minimum decomposition L,1,R of an Av(213) state has L>R. If its LIS is at most two, R must be decreasing. Recursing on L gives a skew sum of the blocks A_p=1 direct-sum J_(p-1). Each block is skew indecomposable, so compositions give exactly 2^(c-1) states of size c. The state class is all height-at-most-two states, rather than only the single-block family.

For 0<z<1/8, t=C(2z) satisfies 1<t<2 and 1/(1-2zt)=t. With f_A=t^|A|, the exact size sum majorizes the actual positive kernel by

    T_z f_A <= (t^(|A|+1)-1)/2 <= (t/2) f_A.

Every row is absolutely convergent. This proves boundedness and contraction on the declared weighted supremum space; no compactness, irreducibility, infinite-dimensional Perron theorem, or critical-radius spectral limit is assumed. The constant vector belongs to that space and is bounded by f, so its nonnegative path sum is at most f/(1-t/2).

The starting sum is z*t^2=(t-1)/2. Thus the full nonempty path series is at most (t-1)/(2-t), for every z<1/8. The actual canonical path bijection makes this a bound on the stated avoidance subfamily, including arbitrary numbers of cells and all edge multiplicities. The radius formula gives growth at most eight. It asserts neither equality nor convergence of that series at z=1/8. The previously accepted primary lower bound lambda>=81/8 supplies the strict gap needed here.

## Arbitrary-length cut and exact uniform normalization

The run is encoded by a complete normalized internal path, counted by b_m. Hence its length is already encoded and requires no additional union factor. Prefix and suffix paths are retained in full, contributing a_p*a_q. Their masses determine the marked block location, including empty-exterior cases.

Each missing boundary edge has at most the relevant binary-shuffle count. Replacing its internal endpoint size by m gives binom(m+l,l)binom(m+r,r). For l+r=k, this individual product is at most its full convolution binom(2m+k+1,k), which increases with k. The boundary condition therefore yields exactly the displayed finite upper bound with floor(delta*m). Sum closure gives a_p*a_q<=a_(n-m); summing p contributes n-m+1. No supposedly uniform deleted remainder is used.

For every fixed G>8, the proven growth bound yields a finite constant C_G with b_m<=C_G*G^m for all m. For fixed epsilon>0 and delta, Stirling's error is uniformly O(log n) throughout epsilon*n<=m<=n; delta=0 has binomial factor one. The actual denominator satisfies log a_n=n log lambda+o(n), so lambda^n/a_n remains exp(o(n)), not a bounded constant. A sum over at most n masses and the polynomial prefactors does not alter the exponential rate. Taking the limsup first and then G decreasing to eight proves the exact stated exponent.

The conclusion requires boundary mass at most delta times run mass. It does not make every macroscopic low-chain run rare regardless of its neighbors.

## Exact dense cross-edge family

For A_p,A_q with p,q>=2, the upper ascending pairs begin at its first point, and the lower ascending pairs end at its last point. Greediness forces the lower maximum between the first upper point and a later upper point. Any earlier lower point would then produce 1324. Thus a valid word must begin and end U.

Conversely, the color classes themselves exclude the one-versus-three mixed forbidden configurations. A two-versus-two occurrence would require a lower point before the first upper point. Words beginning and ending U therefore satisfy avoidance and the greedy condition. This proves K=binom(p+q-2,q).

Each lower point is before the final upper point, giving q cross-pairs. Averaging over the unrestricted middle shuffle gives q(p-2)/2 further pairs, so K_inc=(pq/2)K. The exact path bijection makes edge choices independent and uniform conditional on the complete state chain, because all edge choices reconstruct distinct permutations and their compatibility is pair-local. This conditional fact does not imply a uniform distribution on state chains.

The narrower single-block family also has the displayed contraction at z=1/4: its row sum is 2^(p-1)-1-(p-1)/2, at most 2^p/2; its starting weighted sum is 1/2. The resulting generating-function bound at that point and growth at most four follow.

## Accepted scope

Low endpoint LIS does not make a cross-edge pair count subquadratic: the exact conditional mean is pq/2 even for two height-two states. The positive theorem instead counts whole restricted runs with their exterior weights. States of larger height and blocks with large boundary mass remain outside its probability conclusion. No estimate of the full completion-weighted coefficient [z^n]I(z)/(n^2*a_n) is established.
