# Exact point-pair target for a final concentration attempt

Shared PASS4. This supplies an exact observable and a proof obligation for a later attempt; it does not estimate that observable or prove the weak limit.

## 1. A necessary and sufficient uniform-law criterion

Let Inc(pi) count unordered position pairs i<j with pi(i)<pi(j), and let mu_pi be the square-spread permuton. The footrule distance from the decreasing permutation is

    D(pi)=sum_i |i+pi(i)-(n+1)|.

Adjacent swaps sort pi into decreasing order in exactly Inc(pi) swaps. Each adjacent swap changes D by at most two, because the two target values at adjacent positions differ by one. Thus D(pi)<=2 Inc(pi).

Couple a point (X,Y) sampled from mu_pi with (X,1-X). Within the square corresponding to position i, the absolute vertical discrepancy is at most |i+pi(i)-(n+1)|/n+1/n. Hence

    d_BL(mu_pi, anti-diagonal)
        <=D(pi)/n^2+1/n
        <=2 Inc(pi)/n^2+1/n.                               (1)

Consequently, for exactly uniform Pi_n in Av_n(1324),

    E Inc(Pi_n)=o(n^2)                                     (2)

implies anti-diagonal convergence in probability, hence the desired weak limit.

Conversely, the two-point increasing density is continuous for weak convergence of permutons: the boundary of the defining event consists of ties in x or y, which have probability zero under independent samples from measures with uniform marginals. Its finite-permutation value is Inc(pi)/binom(n,2), up to an O(1/n) square-spreading discrepancy. Boundedness then implies (2) from convergence in probability to the deterministic anti-diagonal. Thus (2) is an equivalent exact-uniform-law target, not only a sufficient largest-cell condition.

## 2. The exact directed-kernel formula

Use the canonical nonempty Av(213) states A, exact directed kernel K, and h_A,ell_A. Let inc(A) be the number of increasing pairs within A. The normalization involution S preserves this count.

For a particular allowed shuffle e from A to C, let X(e) count its increasing pairs with one endpoint in each cell. In its vertical representation the upper cell is A and the lower cell is S(C), so these are exactly lower points lying to the left of upper points. Define the nonnegative integer kernel

    K_inc(A,C)=sum_{e counted by K(A,C)} X(e).              (3)

Do not replace this by K(A,C) times an unconditioned-shuffle average. Both the1324 condition and the greedy witness remain in its definition.

Nonadjacent staircase cells are northwest/southeast ordered and contribute no increasing pair. Adjacent horizontal cells are obtained from the normalized vertical representation by S, which preserves increasing pairs. Therefore the generating series for all increasing pairs over all avoiders is exactly

    I(z):=sum_n z^n sum_{pi in Av_n(1324)} Inc(pi)
       =sum_A z^|A| ell_A(z)h_A(z) inc(A)
        +sum_{A,C} z^(|A|+|C|) ell_A(z)h_C(z)K_inc(A,C).    (4)

The first sum marks a within-cell pair. The second marks an edge and a cross-cell pair; its two endpoint states occur once each. Every old incoming and outgoing completion weight is retained. All expressions are coefficientwise finite, and for positive z<rho they converge because the left coefficient is at most binom(n,2)a_n.

Thus the precise target is

    [z^n]I(z)/(n^2 a_n) -> 0.                              (5)

## 3. Why this is a useful distinct route

The exponential whole-state mark H(z,u) would imply (5), but it is stronger than necessary. A large decreasing cell has no internal increasing pairs, and a large cell can still be harmless if its weighted adjacent interactions contribute o(n^2). Equation (4) isolates the actual bad geometry rather than charging every point in a large state equally.

A concrete next estimate should control the inc(A)-weighted paired completion term and the K_inc edge term, possibly with state-dependent penalties. The pointwise PASS4 lift

    z ell_A(z)<=2 h_(12 skew-sum A^{-1})(z)

reduces the first term to a paired-outgoing expression, but does not estimate it. The second term still requires an actual two-boundary shuffle estimate. Any proof based only on state size would return to the unresolved whole-cell problem.

One local geometric constraint may help: if two points form an increasing pair in a1324-avoider, all points strictly between their positions and values form an increasing sequence. Otherwise a decreasing pair inside that rectangle, together with the endpoints, would be1324. This statement is deterministic. It does not imply that every positive increasing-pair density supplies a large occupied rectangle: two decreasing blocks in direct sum have many increasing cross-pairs and may have empty such rectangles. An estimate must cover this second configuration too.

No claimed asymptotic estimate, independent-cell law, or critical-radius inference is hidden in (4) or (5). The final shared attempt should attack these exact two weighted terms if the common exponential mark remains inaccessible.

## Inputs

The only structural input is the accepted exact canonical staircase transfer, `pass2_staircase_bias/EXACT_GREEDY_TRANSFER.md`, SHA-256 dfbab3a20d05861a7c4aba868b89a225f2ac5db201a467358f015f6efabe2b03, credited there to the primary staircase source:
https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf

The deterministic coupling, sorting argument, and coefficient identity are proved above. The universal fixed-alpha target and the1324 limit remain open here.
