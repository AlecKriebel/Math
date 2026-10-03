# Turn 3: small-amplitude stability and the failure of an edit-distance shortcut

**Original unresolved, author turn 3/5.** This turn proves an explicit local optimality statement at the conjectured multipartite graphon for edge-value perturbations small in L∞. It then gives an exact density-preserving family with unchanged C4 density and arbitrarily small positive L1 distance. Thus a first-variation calculation cannot be promoted to strict edit-distance stability or the global conjecture.

These topologies are genuinely different. A nonzero change between two ordinary 0/1 graphons has L∞ amplitude1, even when it affects a vanishing fraction of pairs. The local theorem below therefore covers small probabilistic edge-value changes, not all small vertex-set surgeries or finite graph edits.

## 1. Baseline and exact first variation

Fix an intermediate x∈(1/2,1), excluding the knot densities1−1/r. Let W_0 be the proposed complete multipartite graphon with r≥2 parts of mass a and one part of mass b, where

    ra+b=1,      0<b<a,      q=ra²+b²=1−x.

Let h be any symmetric measurable perturbation with 0≤W_0+h≤1 and ∫h=0. It need not be constant on blocks. Write

    η=||h||∞,     T=||h||1.

The signs are forced: h≥0 inside each part and h≤0 between parts. Since its integral vanishes, its total positive mass and absolute negative mass both equal T/2.

Let K(s,t) be the conditional change in the probability of inducing C4 when the edge between sampled vertices s,t is switched from absent to present, with all other five edge states sampled from W_0. For s,t in parts i,j of masses a_i,a_j, direct enumeration gives

    K_ii=−(q−a_i²),
    K_ij=(a_i+a_j)²−q       (i≠j).                      (1)

For i=j the two vertices have the same other adjacencies. Adding their edge cannot create C4; it destroys one exactly when the other two vertices are in a common different part. For i≠j the old C4 configurations use one additional vertex in each of parts i,j, of probability2a_i a_j. When that edge is absent instead, new C4 configurations use both remaining vertices in one common part outside i,j, of probability∑_{k≠i,j}a_k². Their difference is (1).

By symmetry of the six possible edges, the exact linear term in the C4-density expansion is

    D(h)=6∫h(s,t)K(s,t) ds dt.                          (2)

Among within-part values the largest K is at a large part:

    K_in,max=−[(r−1)a²+b²].

Among between-part values the smallest K is between a large and the small part:

    K_out,min=−(r−1)a²+2ab.

Their gap is

    K_in,max−K_out,min=−b(2a+b)<0.

Using the sign restrictions and the equal positive/negative masses yields

    D(h) ≤ −3b(2a+b)T.                                 (3)

This is an exact universal first-variation inequality, not a finite scan over blockwise perturbations.

## 2. Theorem: an explicit L∞ neighborhood

If

    ||h||∞ ≤ b(2a+b)/114,

then

    c(W_0+h) ≤ c(W_0) − (3/2)b(2a+b)||h||1.             (4)

In particular every nonzero admissible density-preserving perturbation in this L∞ neighborhood strictly decreases the induced-C4 density.

**Proof, including the remainder.** The probability of inducing an unlabeled C4 is the sum of three products, one for each possible missing perfect matching. Each product has six factors, with every factor either W_e or1−W_e. Substitute W_0+h and expand exactly. The degree-zero terms give c(W_0); the six degree-one terms combine to (2).

A term of degree k≥2 has k factors ±h on distinct sampled pairs and remaining factors between0 and1. Bound one |h| factor in integral by T and every other such factor pointwise by η. Its absolute integral is at most η^(k−1)T, regardless of whether the chosen pairs share endpoints. Since η≤1, this is at most ηT. There are at most

    3∑_{k=2}^6 binom(6,k)=171

such terms. Hence the full remainder R satisfies

    |R| ≤171ηT.                                       (5)

Combining (3) with η≤b(2a+b)/114 gives

    D(h)+R ≤[−3+171/114]b(2a+b)T
            =−(3/2)b(2a+b)T,

as asserted. ∎

The radius depends on the fixed density and tends to zero in certain limiting regimes; no uniform neighborhood for all x is claimed. Knot densities are not treated by this formula with a fictitious zero-mass part. Their unrestricted sharp values are already known from the cited source.

## 3. Exact tying paths arbitrarily close in L1

Keep the baseline on a fixed probability space. Select one large part A of mass a and the small part B of mass b. For any

    0<s<a−b,

split A into three pieces U,E,Z of masses

    u=a−s,
    e=bs/(a−s),
    z=s−bs/(a−s)>0.

Replace its internal interaction with B by a complete bipartite component between U and V=B∪E, leaving Z isolated inside A∪B. All adjacencies to the remaining r−1 large parts are unchanged. Call the resulting graphon W_s. Its masses satisfy

    |V|=b+e=ab/(a−s),     |U||V|=ab,
    |U|+|V|+|Z|=a+b.

It is precisely the non-multipartite tie construction from turn2, with its known triangle-minimizer flexibility credited there. Consequently

    p(W_s)=p(W_0),      c(W_s)=c(W_0)=F(x).             (6)

The only added edges are between U and E, with ordered-pair mass2ue=2bs. The only deleted edges are between B and E∪Z, also with ordered-pair mass2bs. Therefore, for h_s=W_s−W_0,

    ∫h_s=0,       ||h_s||1=4bs →0 as s→0,
    ||h_s||∞=1.                                       (7)

For every s>0 this graphon has positive one-edge-triple density6abz, so it is not a relabeling of any complete multipartite graphon.

In this particular direction, all added pairs were inside the selected large part, and all deleted pairs were between that large part and B. Thus the inequality (3) is an equality:

    D(h_s)=−12b²s(2a+b)
           =−3b(2a+b)||h_s||1.                         (8)

But the actual change in c is zero by (6). The exact higher-order remainder is therefore

    R(h_s)=+3b(2a+b)||h_s||1.                           (9)

In particular R is not o(||h||1) uniformly over admissible perturbations approaching zero in L1. Several changed edges can share one vertex in a small exceptional set; their combined probability is then of the same order as the mass of that exceptional set. Treating every quadratic term as O(||h||1²) would be invalid.

## 4. Consequence for the research route

There is no conflict between (4) and (6): the exact tying paths have amplitude1 and are outside the small-amplitude neighborhood. The result explains why a local derivative argument can look strictly favorable while missing exact equality deformations in edit distance. It also rules out a strengthened claim that the multipartite construction is an isolated C4 maximizer in L1, even within the already controlled complete-join class.

Nothing here gives a global upper bound for arbitrary graphons. No full-resolution or historical-novelty claim is made. The remaining author turns must address a new structural or global inequality, rather than reusing the strict first variation as a substitute for the missing global argument.

## Verification

`verify_turn3.py` exactly enumerates the conditional kernel values, checks selected fractional density-preserving perturbations and the explicit171-term remainder bound, and independently counts the fixed-space tying paths with their L1 masses and first variations. The universal inequalities and all-parameter paths are proved in the text. The source and prior family credits are unchanged from turns1–2.
