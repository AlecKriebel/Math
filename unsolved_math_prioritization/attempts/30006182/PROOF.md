# Statistical additive randomized encodings: finite universality

## Status and attribution

This AI-assisted, unrefereed edition records an internal AI audit of a prior published result. Acceptance here is an internal mathematical assessment, not human peer review or formal proof-assistant certification. Finite checks are corroboration only. This is a full written proof and audit edition, not a computational reproduction package. Source retrieval and inspection described below occurred during the preceding audit on 11 October 2026; this editorial preparation performed no fresh scholarly-source retrieval or inspection.

This is an independently checked reconstruction of the finite-existence result of Nir Bitansky, Saroja Erabelli, Rachit Garg and Yuval Ishai, *Shuffling is Universal: Statistical Additive Randomized Encodings for All Functions*, ePrint 2025/1442, Theorem 1.1. It is an audit, not a novelty claim or a formal proof-assistant replay. The core two-party construction is their Theorem 3.3 and Lemma 4.2. The multiparty step below spells out a finite perfect decomposable randomized encoding and the paper's OT-based compilation approach, with explicit accumulated errors. It does not claim the paper's sharp communication bounds.

Primary manuscript: https://eprint.iacr.org/2025/1442.pdf . The inspected file has 23 physical pages, 383423 bytes, SHA256 45510b5dcac7eae92afbaf9a575b02fe861373e713adac4a6987c0f2ac282b3a. Page numbers below are physical PDF pages, also the printed page numbers in this file.

## 1. Exact accepted claim

For every positive integer k, every choice of nonempty finite sets A_1,...,A_k and finite output set B, every function f from their product to B, and every epsilon>0, there exist a finite abelian group G, independently randomized local encoders E_i:A_i -> G, a deterministic decoder D:G -> B, and an output-only randomized simulator S:B -> G such that, for every fixed input tuple x,

    Pr[D(sum_i E_i(x_i)) != f(x)] <= epsilon,
    TV(Law(sum_i E_i(x_i)), Law(S(f(x)))) <= epsilon.

The group and algorithms may depend on f and epsilon. Random coins used by different physical parties are independent. Security is against an observer given only the sum, not all individual encodings, and does not cover an insider colluding with the observer. There are no computational hardness assumptions. Neither error is required to be zero. Infinite input domains and a single finite group serving every input length are not asserted.

The manuscript states the finite-domain case f:D^k -> D in Theorem 1.1, p. 3. The formulation above is equivalent after injectively labeling finite domains by bit strings, padding shorter encodings, defining arbitrary values on unused labels, and decoding back to B. One can choose a fixed element of B for decoding failures. If a finite domain is empty the universal input assertions are vacuous; we avoid that uninteresting case. A one-party function has the immediate encoding E_1(x)=an injective label of f(x).

Definition 2.1, pp. 7-8, uses total variation distance, an output-only simulator, and pointwise correctness for every input. The original OWR contribution, printed pp. 150-151, specifies local maps into a finite abelian group but does not specify zero errors, insider robustness, or an asymptotic efficiency class. This accepted claim resolves its finite, statistical, non-robust existence interpretation, not every possible reading of the under-specified question.

## 2. Elementary leaky encoding

Let h:[d] x Y -> {0,1} be any finite Boolean function and let H be any finite abelian group of order q. A left input a is encoded as a vector U in H^d: U_a=0, and all other coordinates are independent uniform elements of H. A right input y is encoded as V: coordinates with h(j,y)=1 are zero; the other coordinates are independent uniform elements of H. The two encoders use independent coins. Decode U+V as 1 if any coordinate is zero, and as 0 otherwise.

If h(a,y)=1, coordinate a is zero with certainty; every other coordinate is independent uniform. If h(a,y)=0, all coordinates are independent uniform. In the latter case the probability of a zero coordinate is exactly 1-(1-1/q)^d, at most d/q. Hence correctness error is at most d/q.

The entire sum distribution is exactly simulatable from the output and the following allowed leakage: reveal a only when h(a,y)=1. For output 0 sample uniformly in H^d. For output 1 set coordinate a to zero and independently sample every other coordinate uniformly. This is perfect leaky privacy, even though correctness has nonzero error. No property of a field, multiplication in H, or computational assumption is used. This verifies the substantive content of Theorem 3.3, pp. 9-10, with the hidden constant made explicit.

## 3. Removing the leakage in the two-party Boolean case

Let F:[d] x Y -> {0,1}. Write e_a in F_2^d for the unit vector indexed by a and b_y=(F(1,y),...,F(d,y)). Let t>=1 be an integer. The left party samples A_1,...,A_t uniformly subject to XOR_i A_i=e_a. Independently, the right party samples R_1,...,R_t uniformly subject to XOR_i R_i=0. Both use these local shares as inputs to t independent copies of the leaky construction for

    h(A,(b,r)) = <A,b> + r  in F_2.

Here the left input domain has exactly 2^d elements. Each leaky sum is in H^(2^d), so the complete sum is in H^(t 2^d). Let W_i be that leaky sum, and let V_i=<A_i,b_y>+R_i. The decoder XORs the t leaky decoded bits.

Correctness: if all t leaky decoders are correct, their XOR is

    <XOR_i A_i,b_y> + XOR_i R_i = <e_a,b_y> = F(a,y).

The union bound gives error at most t 2^d/q. No independence of the decoder failure events is needed for this bound.

Privacy requires care about conditioning. For each fixed allowed tuple A=(A_i), the map R -> V is a bijection between zero-parity bit tuples and bit tuples of parity F(a,y). Therefore V is uniform on that parity class and independent of the full tuple A. In particular, its law does not reveal anything other than F(a,y).

Let J={i:V_i=1}. Unless every V_i is 1, J is a proper subset of [t]. A proper subset of the t additive shares of e_a consists of independent uniform vectors. Since V is independent of A, this remains true after conditioning on V. Conditional on such V, the visible leaky sums are therefore generated by the following rule: at coordinates with V_i=0 use the all-uniform leaky simulator; at coordinates with V_i=1 draw a fresh uniform A_i and use the corresponding zero-at-A_i leaky simulator. This rule uses only V, hence only the output to sample V.

The exceptional event V=(1,...,1) has probability either zero or 2^(1-t), depending on the parity of the output. Replace the entire tuple on this event by the zero element of H^(t 2^d) in both the real coupling and the simulator. The modified real law equals the simulator exactly. The replacement changes the real law in TV by at most 2^(1-t). Thus an output-only simulator with values in the actual encoding group exists, with privacy error at most 2^(1-t).

Using the group identity in the bad branch avoids the manuscript's merely notational use of a failure symbol outside the group in its displayed simulator. The TV bound is unchanged. This establishes the two-party result without an external simulation theorem. It verifies Lemma 4.2 and Propositions 4.4-4.5, pp. 10-12. The paper additionally allows leaky simulation error delta, in which case t delta is added by a conditional hybrid argument. Our leaky scheme has delta=0.

For multiple output bits, run independent copies coordinatewise and sum their error bounds. This establishes two-party finite-function universality already. For the multiparty construction it suffices to use one particular Boolean function: bit oblivious transfer OT((b_0,b_1),c)=b_c. The left domain has d=4, and the right has two elements (or can be padded to four). Thus each bit-OT ARE has group H^(16t), correctness error at most 16t/q, and privacy error at most 2^(1-t).

## 4. A fully explicit perfect finite DRE

We supply a simple finite perfect decomposable randomized encoding to make the multiparty existence argument self-contained. This is a truth-table-size construction; it is not the optimized DRE used for the paper's complexity corollaries.

After labeling and padding the physical inputs, consider f:{0,1}^N -> {0,1}^m, N=kn, with N>=2 and n,m>=1. Think temporarily of the N individual input bits as N virtual parties. A shared seed R is sampled as follows:

1. Sample a uniform shift alpha in {0,1}^N.
2. Independently for each row z in {0,1}^N, sample N additive shares s_(z,1),...,s_(z,N) in F_2^m, uniformly subject to their XOR being f(z XOR alpha).

The second step is finite and explicit: sample its first N-1 shares uniformly and set the last share to the required XOR. These N-share tuples are independent between rows conditional on alpha.

The j-th virtual party's decomposable message M_j(x_j;R) consists of:

    beta_j = x_j XOR alpha_j,
    all s_(z,j) for rows z with z_j=beta_j,

in the fixed lexicographic order of the remaining N-1 coordinates. Its length is

    b = 1 + m 2^(N-1) bits.

Given all messages, the decoder obtains beta=(beta_j), extracts the N shares associated with row beta, and XORs them. Their XOR is f(beta XOR alpha)=f(x), so correctness is perfect.

For perfect privacy, fix x. The vector beta is uniform. Conditional on any beta, alpha=x XOR beta is fixed. At row z=beta all N shares are observed and their only constraint is XOR=f(x). At every other row z, the observed shares belong to the proper subset {j:z_j=beta_j} of the N parties; their joint law is independent uniform in F_2^m, regardless of f(z XOR alpha). These observations are independent across rows. Therefore an output-only simulator samples beta uniformly, independent uniform visible shares at each nonactive row, and an N-share tuple of the known output at the active row. It arranges these shares into the virtual messages. This is the exact real joint distribution.

In this auxiliary DRE only, a shared seed is allowed. The next step removes the need for preshared randomness among the physical parties. The seed is not assumed to be known to an adversarial evaluator.

## 5. Compiling the DRE to a local, independently randomized multiparty ARE

Choose physical party 1 as coordinator. Its input comprises n of the N virtual bits. It locally samples R and forms the n corresponding DRE messages, concatenating them into a direct block M_direct of nb bits. For every remaining virtual bit j and every position ell in its b-bit DRE message, the coordinator computes both candidate bits

    M_j(0;R)[ell], M_j(1;R)[ell].

It acts as the sender in a fresh bit-OT ARE for that pair. The physical party owning x_j acts as receiver with choice x_j. Everyone else contributes the group identity in that slot. There are

    T=(k-1)n b

bit-OT slots. The overall finite abelian group is

    G = F_2^(nb) x (H^(16t))^T.

In the direct block only the coordinator contributes M_direct; other parties contribute zero. In an OT slot only the coordinator and that slot's receiver contribute. A physical party may correlate its own local steps and outputs; this does not violate locality. Different physical parties use independent randomness, and each OT instance has fresh randomizer coins, conditionally independent of all other instances given R and the inputs. R is generated by one actual party, not preshared between parties.

The sum reveals the direct DRE messages and the sum encodings of the T selected message bits. Decode each OT slot to reconstruct the remaining DRE messages, then apply the deterministic DRE decoder. Set arbitrary malformed encodings to a fixed default output so the decoder is total.

Correctness follows by a union bound: if all T OT decodings are correct, the reconstructed DRE transcript is exactly correct. Thus correctness error is at most T(16t/q).

For privacy, fix x and R. The candidate OT pairs, the choices, and the direct block are then fixed. Replace the T OT sum distributions one at a time by the bit-OT simulators on the selected DRE bits. Each conditional replacement costs at most 2^(1-t) in TV. The auxiliary direct block and other slots do not add leakage to the hybrid bound, because the bound holds for every fixed R and x and the OT randomizer coins are fresh. Averaging over R, the total change is at most T2^(1-t).

After replacement, the sum distribution is a fixed randomized postprocessing of the entire DRE message vector: keep the direct block and apply an independent bit-OT simulator to each remaining message bit. By the perfect privacy proved in Section 4, that DRE vector can itself be sampled from f(x) alone. Apply the same postprocessing to its simulated vector. The resulting G-valued random variable is the required output-only simulator. This proves privacy error at most T2^(1-t).

The argument supplies the complete multiparty existence reduction suggested in the manuscript's technical overview and Section 5.2; it does not rely on any unexpanded asymptotic error convention in Theorem 5.2.

## 6. Explicit finite parameters, size, and uniformity boundary

Let lambda>=1 be an integer with 2^(-lambda)<=epsilon. With T>=1 choose

    t = lambda + ceil(log2 T) + 1,
    h = lambda + ceil(log2(16tT)),
    H = (F_2^h,+), q=2^h.

Then T2^(1-t)<=2^(-lambda) and 16tT/q<=2^(-lambda). This proves the accepted claim with both errors at most epsilon. The construction uses exact sampling of finite uniform bit strings only. All groups have explicit bit-string representations and coordinatewise XOR operations. There is no unspecified group oracle or algebraic-geometric-code dependency.

The aggregate group element has nb+16tTh bits. Counting each sender's nonzero-supported coordinates, the total encoded-input length is nb+32tTh bits, since each OT slot is supplied by exactly two parties. Here b=1+m2^(N-1) and T=(k-1)nb. This cost is exponential in the total succinct input length N; it must not be reported as an efficient construction for every polynomial-time function family.

Given the full finite truth table and integer lambda, the construction is effective and uniform: every sampler, message, and decoder above is explicitly specified. Implementations can use time polynomial in the length of the explicitly padded binary-domain truth table, N, m and lambda. This is not a polynomial-cost claim for an arbitrary-domain function before padding, much less for a succinct description of that function. For a fixed finite f, the cost is polynomial in the accuracy parameter lambda, with f-dependent constants. Neither fact provides a uniform polynomial-time compiler from arbitrary polynomial-size circuits to statistically secure AREs of polynomial size. The latter is a stronger problem; the primary manuscript says an extension of its information-theoretic efficiency result to all polynomial-time functions would require resolving a longstanding DRE problem.

## 7. What this proof does not establish

- Perfect correctness or perfect privacy. The construction relies on nonzero error probabilities. Letting lambda increase produces a family of finite encodings, not a single finite zero-error encoding.
- Robust or malicious-insider security. The coordinator knows R; collusion with an evaluator is outside the simulator claim. Individual encodings are not claimed to be jointly output-private before summation.
- Universality over infinite domains under one finite group, or any fixed field imposed in advance by an unrelated affine-encoding problem.
- The paper's constant-factor DRE-to-ARE overhead, sublinear-truth-table bound, NL/poly efficiency corollary, or computational P/poly corollary as independently audited theorems. These require additional precise statements and dependencies; they are unnecessary for this finite-existence reconstruction.
- A new mathematical discovery or formal verification. Authored exact finite checks corroborate limited instances only and are not substituted for the argument above.

## Public references

1. Bitansky, Erabelli, Garg, Ishai, *Shuffling is Universal: Statistical Additive Randomized Encodings for All Functions*, ePrint 2025/1442, https://eprint.iacr.org/2025/1442 . Full inspected manuscript: https://eprint.iacr.org/2025/1442.pdf . STOC 2026 proceedings identity: https://doi.org/10.1145/3798129.3800890 .
2. *Cryptography*, Oberwolfach Reports 3/2025, DOI 10.4171/OWR/2025/3, https://ems.press/content/serial-article-files/51349 , Ishai's complete Part 1 contribution on printed pp. 150-151. This is the original model source.

The ePrint page identifies a CC BY 4.0 license. The proof above is an authored reconstruction with attribution; no authors' code has been executed.
