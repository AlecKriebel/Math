# Zonotope containment prior applicability certificate

## Conclusion and scope

**Accepted as a credited conditional negative answer in the exact binary-rational model.** For generator matrices in dimension d, deciding non-containment is W[1]-hard parameterized by d; deciding containment is co-W[1]-hard. Consequently containment has no deterministic f(d) N^O(1) algorithm unless FPT = W[1]. Under ETH, neither direction has a deterministic algorithm of running time rho(d) N^o(d), where N is the total binary input length. These are conditional exclusions, not an unconditional separation of complexity classes.

The result is due to **Vincent Froese, Moritz Grillo, Christoph Hertrich, and Moritz Stargalla**, *Parameterized Hardness of Zonotope Containment and Neural Network Verification*, [arXiv:2509.22849v3](https://arxiv.org/abs/2509.22849v3), 3 September 2026, Section 6, Theorem 6.1, printed/PDF p.20. Its convention is exactly the convention in Martin Skutella's question in [Oberwolfach Report 50/2024](https://ems.press/content/serial-article-files/50767), printed pp.2988–2989, PDF pp.40–41. The two matrices retain their actual positions. No independent recentering is performed.

This certificate covers canonical problem 30006105 / OWR-14298804-007, rank 1212, and its duplicate 30006106 / OWR-14298804-008. It does not supply a new research result or consume a new proof-search turn. The report checks applicability and reconstructs the relevant already-published reduction, including its size bounds and complement direction. It is an AI-assisted mathematical audit, not a proof-assistant certification or a human peer-review claim.

## Exact problem being compared

For a matrix A with columns a_i in R^d, put

    Z(A) = sum_i [0,a_i] = {sum_i t_i a_i : 0 <= t_i <= 1}.

The target input is G in R^(d by n), H in R^(d by m), and the question is whether Z(G) is a subset of Z(H). Skutella asks for time f(d) poly(n+m), without specifying how real entries are represented or charged. The source does not demand equal column counts, nonnegative entries, bounded coordinates, general position, or a full-dimensionality promise.

For a rigorous bit-complexity statement, restrict the entries to Q, give each as a signed binary numerator and positive binary denominator, and let N include both matrices, their dimensions, delimiters, and all entry bits. Equivalent reasonable binary encodings differ polynomially and do not alter the assertions here. The prior repeatedly defines N as input bit-length, and its actual hardness instances below have integer entries of logarithmic bit-length. Thus the rational specialization is justified by a concrete hard subclass; it does not rest on assigning finite encodings to arbitrary real numbers.

The correct FPT formulation is f(d) N^C for an absolute constant C. An unqualified bound independent of the lengths of the entries is not a standard bit-model running-time statement, since even reading the input may take longer. The certificate does not assert a lower bound for an unrestricted unit-cost real-RAM or a real-oracle model. If an arithmetic-operation algorithm is proposed for the original shorthand, its bit-cost implementation and intermediate-number growth need separate analysis.

## Source identity and status

The retained prior PDF has 31 pages and identifies itself on p.1 as arXiv v3, dated 3 September 2026. The arXiv record gives first submission 26 September 2025, v2 on 18 May 2026, and v3 on 3 September 2026. The p.1 footnote says the article extends a preliminary ICLR 2026 conference version. The [official ICLR proceedings record](https://proceedings.iclr.cc/paper_files/paper/2026/hash/4db5ca5ff61529e9bebe2089bf466ca8-Abstract-Conference.html) independently confirms the conference publication and the four authors. The inspected expanded v3 is not asserted to have undergone a separate journal review. The theorem numbers here belong to v3, not automatically to the conference version or earlier preprints.

The proceedings abstract uses the less precise shorthand '(non-)containment'. This certificate follows the formal v3 theorem and distinguishes the two decision languages. No W[1]-completeness or co-W[1]-completeness claim is made.

## Support functions give the exact direction

For a compact convex set K, write s_K(x) = max_{z in K} x·z. Independent maximization over segment coefficients gives, for every real vector x,

    s_Z(A)(x) = sum_i max(0, a_i·x).

Hence Z(G) subset Z(H) implies s_Z(G)(x) <= s_Z(H)(x) for every x. Conversely, if z lies in Z(G) but outside Z(H), choose a nearest point q of the compact convex set Z(H) to z and put x = z-q. Convexity and the one-sided derivative of ||z-(q+t(y-q))||^2 at t=0 imply x·(y-q) <= 0 for every y in Z(H). Therefore

    x·z = x·q + ||x||^2 > x·q >= s_Z(H)(x),

where in fact s_Z(H)(x) = x·q. Since s_Z(G)(x) >= x·z, the difference of support functions is strictly positive. This also covers lower-dimensional zonotopes. The exact equivalence is

    Z(G) not-subset Z(H)
        iff there exists x with sum_i ReLU(g_i·x) - sum_j ReLU(h_j·x) > 0.

Here ReLU(t)=max(0,t). The first zonotope is the positive side, the second the negative side, and the threshold is strictly >0. Equality everywhere or a zero maximum is a containment case. Exchanging the matrices changes the question.

Conversely, take any bias-free two-layer scalar network

    h(x) = sum_i lambda_i ReLU(w_i·x).

Delete zero coefficients. For lambda_i>0, use generator lambda_i w_i in G. For lambda_i<0, use generator (-lambda_i) w_i in H. Positive homogeneity of ReLU gives exactly h=s_Z(G)-s_Z(H). A negative coefficient does not authorize replacing w_i by -w_i on the same side. Bias-free input is essential: arbitrary affine biases cannot simply be discarded. If a side is empty, its zonotope is {0}; a zero column can be added if a format insists on at least one column.

These transformations preserve dimension and are polynomial-time on rational binary data. Multiplying two rational numbers adds their numerator and denominator bit-lengths up to a constant; it does not exponentiate those lengths. With dense network input size L, the total generator output has at most polynomial size (a conservative O(L^2) bound suffices). The reverse transformation uses the given generators as hidden weights and output coefficients +1 and -1. Thus this equivalence itself preserves FPT status and N^o(d)-type lower bounds under polynomial changes of input length.

## Translation and centered conventions

Define c_A = (1/2) sum_i a_i and C_A = sum_i [-a_i/2,a_i/2]. Then Z(A)=c_A+C_A. The containment statement is

    c_G + C_G subset c_H + C_H,

or equivalently (c_G-c_H)+C_G subset C_H. One may translate both sets by the same vector. One may not silently test C_G subset C_H after dropping the difference of centers. For example, in one dimension G=(2), H=(-4) gives Z(G)=[0,2] and Z(H)=[-4,0], so containment fails, whereas [-1,1] is contained in [-2,2].

No conversion is needed for Theorem 6.1: both sources define the generator segments as [0,a_i]. In the explicit hard subclass below the two centers happen to agree, as can be checked by summing columns. This extra property is a consequence of that construction, not an assumption silently imposed on general inputs.

## Audited reduction and numerical scales

This section re-expresses the prior's Proposition 4.1 (pp.10–12), Definition 5.1 and Lemma 5.2 (pp.13–14), and Theorem 5.3 (p.14), followed by Section 6 (p.20). It explains all transformations relevant to the target rather than treating the theorem title as sufficient evidence.

Start with Multicolored Clique on a simple graph with k color classes, q vertices, and e cross-color edges. Edges within a class can be removed. It is enough to consider k>=2 and nonempty classes, so k<=q. Trivial empty-class or fixed small-k inputs can be decided separately. The prior uses the standard W[1]-hardness and ETH lower bound rho(k) q^o(k) for Multicolored Clique.

Assign distinct positive integral labels a_v from a Sidon set of size q. All unordered pair sums, including repeated summands, are distinct. The prior uses the polynomial-time greedy construction with maximum label O(q^3). Both the existence/size bound and the source hardness of Multicolored Clique are explicit external dependencies; their original literature is not independently re-proved here.

For scale s>0 define the triangular function

    T_(a,s)(t) = ReLU(s(t-a)+1) - ReLU(2s(t-a)) + ReLU(s(t-a)-1).

It is zero when |t-a|>=1/s, equals 1-s|t-a| when |t-a|<=1/s, lies between 0 and 1, and takes the value 1 only at a. These identities follow by checking the four intervals cut by a-1/s, a, a+1/s.

For color c, sum T_(a_v,8)(x_c) over vertices v of that color; call this p_c. Integral distinct labels ensure disjoint interiors of its supports, so 0<=p_c<=1 and positivity selects a unique vertex within distance 1/8. For each color pair r<l, sum T_(a_u+a_v,4)(x_r+x_l) over edges uv between those colors; call this s_rl. Sidon uniqueness and integrality ensure disjoint supports here too, so 0<=s_rl<=1. Put

    F(x) = sum_c p_c(x_c) + sum_(r<l) s_rl(x_r,x_l),
    B = k + k(k-1)/2.

A multicolored clique, evaluated at its vertex labels, makes every summand 1 and hence F=B. If F>B-1, every one of its B summands must be positive, since all lie in [0,1]. Each x_c then selects a vertex v_c at distance <1/8. Each pair sum is at distance <1/4 from a_(v_r)+a_(v_l). The pair sum also lies at distance <1/4 from the label of an actual edge because s_rl>0. Two different integral pair labels cannot both lie within these distances: their distance would be <1/2. Therefore the selected pair is an edge, using Sidon uniqueness. All selected vertices form a clique. In particular, a graph with no such clique has F<=B-1 everywhere.

There are 3(q+e) ReLU terms before homogenization. Each vertex term has scale 8, each edge term scale 4, and all affine coefficients are integers: the apparent fractions 1/8 and 1/4 multiply away. The output offset is 1-B. Put g=F-(B-1). It has a positive point exactly when the graph has a clique.

### Source typo recorded rather than inherited

The first branch of the piecewise edge-spike definition on v3 p.11 prints 4(t-a-1/4), although the interval is [a-1/4,a]. That branch would be negative, would equal -1 at the alleged peak, and is inconsistent with the accompanying graph and the claimed range [0,1]. The ReLU implementation immediately below uses the correct first term ReLU(4(t-a+1/4)). The rising branch must therefore be 4(t-a+1/4). The reconstruction above follows that correct displayed implementation and checks its values directly. This is a local typographical correction, not a gap in the specified ReLU construction. Its impact is confined to the exposition of Proposition 4.1.

### Explicit bias-free matrices

For each of the M=q+e triangular summands, let r in Z^k be 8 e_c for a vertex of color c, or 4(e_r+e_l) for an edge between colors r and l. Let a be its scale times its label, namely 8a_v or 4(a_u+a_v). In dimension d=k+1, give G the two columns

    (r, 1-a) and (r, -1-a),

and give H the column

    (2r, -2a).

Finally add to H the two columns (B-1)e_d and -(B-1)e_d. Thus G has n=2M columns and H has m=M+2 columns, for n+m=3M+2. All entries are integers; no independent affine centers are part of the input.

Writing x for the first k coordinates and y for the last, their support-function difference is the source's homogenized network h(x,y). At y=1 it equals g(x). For y>0, positive homogeneity gives h(x,y)=y g(x/y). At y=0 each triangular triple cancels because 2 ReLU(r·x)=ReLU(2r·x), and the extra terms vanish, so h(x,0)=0.

For a triangular triple, the signed sum of its three linear input forms is identically zero. The identity ReLU(t)-ReLU(-t)=t therefore shows its value at (-x,-y) equals its value at (x,y). The final -(B-1)|y| term is also invariant. For y<0 it follows that h(x,y)=|y| g(-x/|y|). Consequently h has a positive point if and only if g does, with no spurious witness in the halfspace y<0 or on y=0. The ambient dimension increases only from k to k+1; the network-to-zonotope step adds none.

By the support-function equivalence, this is a yes-preserving reduction

    graph has a multicolored clique iff Z(G) is not contained in Z(H).

Every triple contributes the same column sum to G and H, and the final two H columns sum to zero. The centers agree. With nonempty classes and k>=2, both matrices also span R^(k+1): differences of each G pair yield the last coordinate, vertex columns then yield every color coordinate; the final H pair yields the last coordinate and its vertex columns yield the others. Full dimension is not needed for applicability, but there is no hidden degeneracy on which this reduction relies.

### Bit and parameter bounds

The integer entries have absolute value O(q^3), since labels are O(q^3), edge labels are sums of two labels, and B=O(k^2)<=O(q^2). Each entry therefore needs O(log(q+1)) bits. In a dense encoding the two matrices have O((k+1)(q+e)) entries, so

    N = O((k+1)(q+e) log(q+1)) = O(q^3 log(q+1)),
    d = k+1, and n+m = 3(q+e)+2.

The reduction is polynomial-time with a degree independent of k. Thus an algorithm rho(d) N^o(d) for non-containment would solve Multicolored Clique in rho'(k) q^o(k), contradicting the cited ETH consequence. Polynomial preprocessing time is absorbed as well: a fixed exponent is o(k) as k grows. Equivalently, the dimension increase by one and the fixed-degree polynomial size increase preserve the required exponent scale.

This calculation also identifies a hard family with only logarithmic coordinate bit-length. The failure to get FPT is not caused solely by arbitrarily long numerical entries. It still does not convert a bit lower bound into an unrestricted real-RAM lower bound.

## Complement logic and accepted wording

Let NC be the parameterized non-containment language and C its complement on the same valid encoded inputs, with the same parameter d. The construction is a reduction from Multicolored Clique to NC, not to C. The prior therefore proves NC W[1]-hard and C co-W[1]-hard. For any language L in co-W[1], its complement is in W[1]; a reduction from that complement to NC is, on the same map, a reduction from L to C.

Deterministic FPT is closed under complementation: run the decision algorithm and flip its answer. If C were FPT, so would NC be; W[1]-hardness would then imply W[1] subset FPT, and hence FPT=W[1]. Conversely the cited hardness alone does not show this equality is impossible. The same answer-flipping step preserves a rho(d) N^o(d) running time, so the ETH lower bound holds for C as well. This is exact decision containment, not approximate containment or a promise-gap version; no approximation hardness is inferred here.

Recommended conclusion: 'Froese, Grillo, Hertrich, and Stargalla establish a conditional negative answer to the dimension-FPT question for exact binary-rational zonotope containment: containment is co-W[1]-hard, hence not FPT unless FPT=W[1], and ETH excludes rho(d) N^o(d) algorithms. Their v3 Theorem 6.1 states the complementary non-containment result.'

The word 'solved' alone would obscure the complexity assumptions and the original report's suppressed encoding. Appropriate disposition is **credited prior applicability accepted, conditional on the stated complexity assumptions**, with proof-search turn count unchanged.

## Dependency boundary and checks

The target convention and its question were visually inspected on OWR PDF pp.40–41. The v3 title/version/status, p.11 formulas and typo, Theorem 5.3 on p.14, and Theorem 6.1 on p.20 were visually inspected; Sections 2, 4, 5.1–5.3, and 6 were read in extracted text against those images. The support-function equivalence, signs, parameter map, explicit integer columns, numerical sizes, positive/negative/zero homogenizing coordinate cases, complement implication, and relevant triangle-gadget correctness are proved above.

The remaining imported foundations are standard Multicolored Clique W[1]-hardness and its ETH bound, and the cited greedy Sidon-set construction with polynomial magnitude. We did not re-prove the full W-hierarchy theory, ETH consequences from 3-SAT, or all results of the expanded neural-network paper. The certificate has no need for a Lipschitz-norm oracle, deep-network hardness, or an approximation theorem.
