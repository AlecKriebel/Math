# Independent proof reconstruction (frozen before earlier reviewer reasoning)

Claim under review: ordinary sequential legal reachability on nonempty loopless strongly connected directed multigraphs, binary adjacency and nonnegative binary x,y, with varying dimension, is coNP-complete. Invalid encodings reject. This is not a claim for simple, unary, bounded-degree/chip, or unrestricted signed membership models.

1. Source and strings. Need a primary-source NP-hard HALTING interface with strongly connected binary multigraphs; its complement is coNP-hard. Invalid strings must be totalized consistently. A source HALTING reduction can replace invalid outputs by a fixed valid nonhalting instance; then its complement has valid outputs. Alternatively literal-complement invalid strings map to reachability YES. The valid-instance nonhalting language rejects invalid strings and maps them to a conservation NO pair.

2. Signed threshold normalization. Adding k_v=max(0,-x_v) loops and chips preserves the entire firing matrix and shifts both current coordinates and legal thresholds equally, so every word retains legality. Removing loops by initially empty packet relays keeps the parent degree unchanged. Relay count s_v<=parent count t_v; projected original parent holdings equal expanded holdings plus the pending packet l_v(t_v-s_v). Thus old moves project legally and infinite expanded words have infinitely many old moves. Immediate relay returns lift original play. Singleton with l loops is nonhalting iff x>=l, including degree zero; it can be classified before the construction.

3. Cutoff. Conservation confines nonnegative states of total C to at most (C+1)^n=N states. N legal moves repeat a state and a nonempty closed legal word can repeat indefinitely. Existence of infinite play is the nonhalting answer by the standard dichotomy. C=0 and all positive source degrees give no move, N=1.

4. Construction arithmetic. M=N+1, B=N(MD+1). H retains M times each old arc, old-to-gate 1, gate-to-old B, and g<->m 1. Old thresholds M d_v+1; gate nB+1; marker 1. It is loopless and strongly connected. X=(Mx+N, nB+1-N,0), Y=(Mx+MN(i-d)+B,(n-1)N,1). Since d<=D, every Y_old >=B-MND=N. X_g positive. Sums both equal MC+(n-1)N+nB+1. Marker proves X!=Y.

5. Prefix exactness. Before first gate, marker cannot fire. With old counts t and total T, h_old=M z+N-t and h_g=nB+1-N+T. Before each of first N old moves, 0<=t_v<=N-1: legal source gives h_v>=Md_v+1; illegal source z_v<=d_v-1 gives h_v<=Md_v-M+N=Md_v-1. Thus equivalence holds in arbitrary order up to N and gate first becomes legal at T=N. No assumption on eventual target firing vector is needed.

6. Forward. Source nonhalting supplies N legal moves. Fire gate; every old vertex has >=B. Complete its individual count to N in any order, without another gate/marker. At most N payments per old vertex of cost Md_v+1 are needed; B covers them even ignoring incoming chips. Counts f=(N each,1,0) give exactly Y. A legal word may stop despite available moves.

7. Reverse. For ANY target-reaching legal word k, marker balance is k_g-k_m=1. Thus it has a first gate; marker cannot have fired earlier. Gate needs >=N old firings beforehand. First N project legally by step5, certifying source nonhalting. Extra periods, delayed gates and subsequent marker/gate firings cannot evade this.

8. Encoding size. n log(C+1), with explicit +1 at C=0, bounds log N. log M, log B, all matrix/output coordinate bit lengths and n+2 dimension are polynomial in binary input length. Computing powers uses polynomial-bit operations. Long witness words and arc multiplicities are not emitted in unary.

9. Membership. Rank n-1 integer kernel has positive primitive p, computable through directed tree cofactors. Integer image membership and a solution h are polynomial-time integer-linear-algebra tasks. Reducing by min floor(h_v/p_v) yields g>=0 with g_w<p_w and all nonnegative solutions g+kp (k>=0). Polynomial bit bound follows from g_w<p_w and the invertible reduced minor's adjugate/Cramer expression; no trajectory bound is assumed.

10. Period deletion. For a legal word with f>=p, delete first p_v occurrences of each v. At a retained v event deletions at v are complete and r_u<=p_u elsewhere; loopless off-diagonals nonnegative imply (Lr)_v<= (Lp)_v=0. The retained word is legal and reaches the same endpoint. Iterating removes the integer k periods, hence target reachability equivalent to a legal word of exactly g.

11. Negative certificate. A vector 0<=u<=g, u!=g, with (x+Lu)_v<d_v for all residual-demand vertices u_v<g_v refutes such a word: take the first event exceeding u; its preceding count at v is u_v and elsewhere <=u, so its chips there are <=(x+Lu)_v. u need not itself be legal or nonnegative-state realizable. If g cannot be realized, a maximal g-bounded legal prefix yields such a proper stuck u. Bit lengths bounded by g. Image nonmembership and invalid cases are polynomial decidable; singleton equality handled separately.

Provisional proof conclusion: algebraic reduction and certificate are internally valid under the stated source theorem and dichotomy. Exact source interfaces and package/code behavior still require independent verification. Finite computation can falsify cases, not establish universal proof. No priority or current-openness conclusion follows from this derivation.
