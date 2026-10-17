# Independent acceptance of adaptive boundary entropy and its certificate obstruction

Shared PASS4, 14 October 2026.

## Verdict and pins

**Accepted in their stated, distinct scopes:**

- `pass4_adaptive_profiles/ADAPTIVE_WINDOW_ENTROPY.md`, 7040 bytes, SHA-256 `3d1308f91c0ae353a0662ce34639cdb06a076409c542674d31a337ec91ed04fb`.
- `pass4_adaptive_profiles/EXACT_CANONICAL_WINDOW_OBSTRUCTION.md`, 7554 bytes, SHA-256 `e302b0e4666eb9e0679d0619494b2a742d140d62fe2c0b1d6b7e78ecb97832d1`.

The first proves a conditional sufficient theorem using a divergent sum of certified true-gap lower bounds. The second shows that the particular sharp local-reroot certificate cannot supply a positive fixed-window score, even on actual canonical avoiders. It does not bound the true gaps from above or contradict the conditional theorem. No mathematical correction is required.

## 1. Boundary entropy is counted exactly once per edge

For a center i, the left and right boundary edges of radius-j windows cover the two rays of adjacent edges without overlap. At a clipped endpoint, the actual boundary has zero exterior mass and zero entropy; the zero-padded formula has the same value. Repeated windows after the whole profile has been reached likewise contribute zero.

Each profile mass appears in at most two edge endpoints. Since e(x,y)<=(x+y)log2, the sum of boundary entropies over all radii is at most2 log2. Every selected window retains the central mass at least epsilon. The averaging argument therefore gives the exact positive margin

    [epsilon sum_(j=0)^N d_(2j+1)-2log2]/(N+1)

whenever its numerator is positive. Crucially, N and this margin depend on the fixed epsilon and finitely many gap values, not on n or the random cell count.

## 2. Exact probability normalization and uniformity

The selected block has width at most one of the finitely many fixed K values. Its three normalized path fragments are counted by a_p, b_(m,K) and a_q, including empty exteriors. Thus both exterior completion factors survive. Eligibility of a three-piece datum determines its endpoint masses; restoring the two missing edges costs at most exp(e(a,l)+e(b,r)). The positive score bounds this by exp(m d_K-cn).

One may partition by the integer endpoint masses, at a polynomial cost, or apply this bound directly to each eligible datum. Either route is valid. Summing p+q=n-m uses a_p a_q<=a_(n-m). The marked location is already encoded by the prefix path; no uncontrolled adaptive-selection factor is missing.

For each fixed K and eta>0, g_K's defining limsup gives b_(m,K)<=exp(m[log lambda-d_K+eta]) eventually. A single threshold suffices for the finite chosen list of K. Since m>=epsilon n, it applies uniformly to every counted mass. The exterior bound a_(n-m)<=lambda^(n-m) and exact denominator log a_n=n log lambda+o(n) leave rate at most -c+eta. Choosing eta=c/2 and summing the polynomially many marked configurations proves the claimed exponential bound.

The deterministic selector does not need to be made unique: an existence event is bounded by the union of all eligible marked blocks. There is no growing-K asymptotic or conditional-uniformity replacement.

## 3. Divergence of the true gap sum is sufficient, but unproved

The canonical at-most-K classes increase with K, so delta_K=log(lambda/g_K) decreases. Therefore divergence of the full positive series implies divergence of its odd-indexed subseries. The theorem applies with d_K=delta_K and proves exponential largest-cell tails at every fixed positive fraction, hence the accepted sufficient geometric condition for anti-diagonal convergence.

No such divergence is proved. Positivity at every fixed K alone is inadequate. Conversely, a summable sequence of lower certificates cannot prove that the true gaps are summable. The two directions are separated correctly in the reviewed statement.

## 4. The local-certificate upper envelope

For the normalized vector x_j=2^(j-1)/(2^K-1), the first local penalty is gamma/(2^K-1). Every later penalty is x_j[gamma-H(1/2)]<0, because H(1/2)>log2>=gamma. Thus V_K<=gamma/(2^K-1) is correct, independently of the recurrence that evaluates V_K.

This is an upper bound on the minimax certificate itself. The valid relation to the true gap is delta_K>=V_K; reversing it would invalidate the claimed scope, and the note does not do so.

## 5. Every finite window of the infinite mountain has a negative score

The profile p_j=(1/3)2^(-|j|) sums to one. For a center-containing interval [-u,v], its two exterior neighbors have half the respective endpoint masses. The stated entropy is exactly (H(1/2)/3)(2^(-u)+2^(-v)). Its internal mass is at most K/3.

AM–GM gives 2^(-u)+2^(-v)>=2*2^(-(K-1)/2). Independently, 2^K-1>=K*2^((K-1)/2). Combining these with the certificate upper envelope gives a strict inequality E/M>V_K. The comparison also covers K=1 and intervals with the center as an endpoint.

A window wholly on one side has an inward neighbor of mass2a, where a is its inward endpoint, and total mass strictly less than2a. Since e(a,2a)=2aH(1/2), the inward edge alone gives E/M>H(1/2)>gamma>=V_K. Its outer edge is unnecessary. Thus the conclusion genuinely applies to all windows, not only centered ones.

## 6. Exact finite realization and quantifiers

The increasing-state mountain from the accepted PASS3 construction is a genuine canonical path. Its normalized states and explicit greedy edge shuffles produce an actual1324-avoider, rather than an arbitrary gridding. For every fixed cap B, choosing the mountain parameter m>B keeps both neighbors of every center-containing window of width at most B present. Its entropy ratio then equals the infinite-profile ratio exactly after a common scale factor.

For wholly one-sided windows, the inward-neighbor argument remains valid even at the finite profile's outer endpoint. Therefore every bounded-width window in each sufficiently large member has negative V-score. Zero-padding shows V_L<=V_K when L>=K, so using a larger cap than the actual block length cannot repair the score.

The full staircase has unbounded width and zero external entropy, which is explicitly outside this fixed-B obstruction. Passing to it would require new coefficient uniformity. The central increasing cell has asymptotic mass1/3 and gives a positive increasing-pair density, so these examples fail to approach the anti-diagonal deterministically. Their exact uniform probabilities are not lower bounded.

## Scope conclusion

The conditional divergence theorem and the all-window certificate obstruction are both accepted. Together they identify an actual quantitative gap in the current method. They do not resolve the true gap sequence, largest-cell sublinearity, the uniform1324 limit, or the universal fixed-alpha target.
