# One-point staircase rerooting and arbitrary-index upward-jump tails

Shared PASS3, 14 October 2026. This reconstructs the shape lane's provisional rerooting argument and incorporates the direct bridge supplied by the kernel-bounds lane. It supersedes the provisional three-point construction in REROOTING_LOCAL_BOUND.md. Complementary review is recorded separately; the proof below does not claim acceptance merely from a provisional message or finite tests.

## 1. Exact statements

Use the accepted canonical normalized state path A_1,...,A_r for a1324-avoider, with each A_j in Av(213), cell sizes c_j=|A_j|, and exact directed edge kernel K. Let a_n=|Av_n(1324)|, lambda=lim a_n^(1/n), rho=1/lambda and gamma=log C(rho)>0, where C is the Catalan generating function. Let B_N(m) count size-N avoiders whose first canonical cell has size at least m.

For fixed integers n,m>=1 and 0<=p_0<=floor(n/2), the number of marked pairs (pi,i) satisfying

    i>=2, c_i>=m, c_(i-1)<=p_0

is at most

    (n+1) binom(n,p_0) B_(n+1)(m).                           (1)

For fixed positive integers a,b, the number Z_n(a,b) of marked pairs with i>=2, c_i=a and c_(i-1)=b satisfies the sharper bound

    Z_n(a,b) <= (n+1) binom(a+b,b) B_(n+1)(a).               (2)

Impossible parameter choices give zero counts. Both statements concern the full uniform finite avoidance class after division by a_n; no induced-state uniform law is imposed.

Two consequences are:

- For fixed epsilon in (0,1] and delta in (0,1/2),

      limsup (1/n)log P[exists i>=2:
                  c_i>=epsilon n, c_(i-1)<=delta n]
          <= h(delta)-epsilon gamma.                       (3)

- Put f(c)=(1+c)log(1+c)-c log c for c>0. If f(c)<gamma, then for every fixed epsilon in (0,1],

      limsup (1/n)log P[exists i>=2:
                  c_i>=epsilon n, c_(i-1)<=c*c_i]
          <= -epsilon[gamma-f(c)]<0.                       (4)

The indices range over the entire canonical staircase, not a fixed prefix. Neither assertion excludes a gradually increasing or graded macroscopic profile.

## 2. First-entry inflation and its incoming edge

For a nonempty213-avoider A, define A^+ by inflating its first entry by12. Its first two entries are ascending and consecutive in value. Removing either of them and standardizing recovers A.

A^+ avoids213. An occurrence selecting at most one inflated point reduces to an occurrence in A. If both points are selected, their adjacent increasing positions cannot be the decreasing first pair of213. They cannot be the last pair because no point precedes the first-entry block, and they cannot be the first and third positions with an external point between them.

Every shuffle in K(P,A) lifts injectively to one in K(P,A^+). The involution S takes the first-entry inflation to a12 inflation of the highest point of the lower pattern S(A). Duplicate that lower maximum adjacently in the global shuffle. Any occurrence using at most one twin was already present. One using both twins would require the two-colour order lower,upper,lower,upper, impossible with adjacent twins. The cell classes remain correct, and the new highest lower point stays in the old gap between upper points, preserving the greedy witness. Deleting the indicated twin inverts this lift.

## 3. Direct bridge from an ascent state to any state

For every213-avoider U containing an ascent and every nonempty state A,

    K(U,A)>=1.                                               (5)

Here is a deterministic choice. Let B=S(A), and write B=L,M,R around its maximum M. Since B avoids132, every value of L exceeds every value of R: a contrary pair l<r would form l,M,r=132.

Choose a fixed adjacent ascent of U, for example its first. Place the entire consecutive block L,M in the gap between these two upper points, and place all of R after every upper point. Preserve all internal orders.

The lower maximum M is bracketed by the upper ascent, giving the greedy witness. A1324 in two such cells must use an increasing lower pair and an increasing upper pair in the order lower,upper,lower,upper. No increasing lower pair crosses from L,M to R because all left-block values exceed all right-block values. A pair entirely within L,M has no upper point between its points, while a pair entirely within R has no later upper point. Thus the shuffle avoids1324. This proves (5), including empty L or R.

In the application U=A_r^+, its first two entries provide the prescribed ascent. The bridge is chosen by this fixed rule, not freely from all possible kernel edges.

## 4. Rotate at the marked cell

For a marked i>=2, remove the old edge A_(i-1)->A_i. Inflate the final state A_r to A_r^+. Rotate the normalized state path to

    A_i,...,A_r^+,A_1,...,A_(i-1).                           (6)

Use the deterministic bridge from A_r^+ to A_1. Retain every other old edge, with the injective incoming lift into A_r^+ when that edge survives. If i=r, the incoming edge to A_r was the removed edge, so no lift is needed.

Every edge in (6) is an allowed K edge. The accepted exact normalized kernel theorem reconstructs one1324-avoider whose canonical state chain is exactly (6). The normalization already includes parity reflections; cyclic rotation does not require preserving the original geometric parity of a state.

The output size is n+1. Its first cell has size c_i if i<r and c_i+1 if i=r, hence at least the marked original size.

## 5. Reconstructing every preimage

Read the output's unique canonical chain and all edge shuffles. A possible original marked object is specified by the index of the new bridge edge and the deleted old edge shuffle.

For a proposed bridge index, the state just before it is the inflated original terminal state. Collapse its first-entry12 block and, if applicable, invert the adjacent-maximum lift on its incoming edge. Incorrect proposals may be rejected; they never increase the number of possible preimages. Rotate the path so that the state after the bridge is first. This uniquely recovers the original state order, the marked index, and all retained shuffles. The only missing data are the cut edge from the output's last state to its first, after deflation if the first was the old terminal state.

There are at most n+1 possible bridge indices. If the original marked and predecessor sizes are a and b, the lost edge has at most binom(a+b,b) possible binary interleavings. This proves (2). In particular, if b<=p_0<=n/2 then

    binom(a+b,b)<=binom(n,b)<=binom(n,p_0),

proving (1). No additional factor is missing for internal state patterns, old cell boundaries, the marked index, or deleted-point allocations: these are reconstructed from the output and bridge choice. The argument also counts all eligible marked indices of one original permutation, so the corresponding existence event is bounded as claimed.

## 6. Exact-law derivation of the absolute predecessor bound

The accepted first-cell estimate is

    limsup_N (1/N)log[B_N(ceil(theta N))/a_N]<=-theta gamma

for each fixed theta>0. The size-change ratio is retained explicitly. Deleting the minimum gives at most N insertion positions per predecessor, so

    a_(n+1)/a_n<=n+1.

Take m=ceil(epsilon n), p_0=floor(delta n) in (1), divide by a_n, and use this polynomial ratio. For any fixed theta<epsilon, the new first-cell threshold m/(n+1) exceeds theta for all sufficiently large n. Apply the accepted fixed-theta tail and then let theta increase to epsilon. The polynomial factors have zero logarithmic rate, and n^(-1)log binom(n,floor(delta n)) tends to h(delta). This proves (3) without any uniform conditional-law assumption.

## 7. Relative predecessor bound with a uniform coefficient estimate

The independently audited absolute frontier amplification yields, for every eta<gamma, a finite constant C_eta such that

    B_N(a)<=C_eta lambda^N exp(-eta a)                       (7)

simultaneously in N and a. This is an absolute count estimate; lambda^N/a_N is not assumed bounded. It follows by summing the Catalan descendant bound against s^t for a fixed s<rho, and is explicitly proved in WEIGHTED_OPERATOR_BOUNDARY.md.

For a,b>0, the ordinary binomial entropy bound gives

    binom(a+b,b)<=exp(a f(b/a)).

The function f is increasing because f'(c)=log(1+1/c)>0. Thus b<=ca implies the right side is at most exp(a f(c)). Choose eta with f(c)<eta<gamma. Combining (2) and (7), summing over a>=ceil(epsilon n) and b<=ca, and bounding the number of pairs by n^2, gives

    P[the event in (4)]
      <= polynomial(n) * (lambda^n/a_n)
                         * exp[-epsilon n(eta-f(c))].

The count growth identity log a_n=n log lambda+o(n) makes lambda^n/a_n subexponential. Taking the logarithmic limsup and then eta increasing to gamma proves (4). Uniformity over all eligible a,b is supplied by (7), rather than inferred from a pointwise fixed-scale limit.

## 8. Remaining scope

The new estimates require a large upward jump from a smaller predecessor. Iterating them at successively decreasing scales does not force a total-mass contradiction: positive lower bounds on predecessor sizes may decrease geometrically, with finite total sum. A large cell at an escaping index can therefore remain outside what has been ruled out.

Largest-cell sublinearity is only a sufficient condition for the anti-diagonal limit. The decreasing permutation itself has one full-size canonical cell and already tends to the anti-diagonal. No converse, largest-cell sublinearity, or universal weak-limit theorem is proved here.

## Exact inputs

- Canonical kernel: `pass2_staircase_bias/EXACT_GREEDY_TRANSFER.md`, SHA-256 `dfbab3a20d05861a7c4aba868b89a225f2ac5db201a467358f015f6efabe2b03`.
- First-cell tail: `pass2_1324_shape/FIXED_STAIRCASE_PREFIX_THEOREM.md`, SHA-256 `1049ab2c021a6398831e8251d0a07cd03b1db98d9a88d64e4faa3660cb1a2037`, based on the accepted PASS1 frontier proof.
- Uniform absolute bound: `pass3_kernel_bounds/WEIGHTED_OPERATOR_BOUNDARY.md`, SHA-256 `b4b2057622a189442bcff813648db124642862ce65f3805bc843bc25550d9597`, Theorems B–C.

No new external enumeration theorem, numerical growth estimate, or finite-coefficient radius inference is used. Complementary independent acceptance and any finite diagnostics are recorded separately.
