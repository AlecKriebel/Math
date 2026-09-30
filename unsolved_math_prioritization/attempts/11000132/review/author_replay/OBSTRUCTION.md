# Component counting: an exact expanded formula and the compressed-coordinate gap

**Target:** 11000132 / AMR-109-0132, R. C. Penner's Problem 2.  
**Status:** unresolved; scoped deductions and source audit, pending separate review.  
**Approaches:** 3/5. No novelty claim.

## 1. Exact source and requested output

The full source is Penner, *Probing mapping class groups using arcs*, Chapter 7 of Farb's *Problems on Mapping Class Groups and Related Topics*. The question begins on printed p.106 and its decisive clarification is on p.107, PDF pp.113–114 of the [complete volume](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf). It also appears on pp.6–7 of the [complete author preprint](https://arxiv.org/abs/math/0505595).

The operation is **counting connected components of one disjoint weighted family of curves and arcs**, not computing intersection numbers between two curves. The input uses a framed pants decomposition and its Dehn–Thurston intersection/twist data, or another coordinate system. The source writes a product of its lattice cone Z, not an unconstrained list of arbitrary signed intersection numbers: m_i≥0 and at m_i=0 the twist ray is identified with its negative, conventionally represented by t_i≥0. Its boundary windows and twisting conventions are part of the input interpretation.

The next paragraph explicitly acknowledges serial train-track splitting and requests something more closed-form. The source does not specify a formal grammar of permitted formulas or a complexity model. We therefore do **not** declare the problem solved merely by an algorithm, even one polynomial in the binary coordinate size.

The concrete results below concern an actual finite integral multicurve/multiarc realization: integer weights are expanded into parallel unit strands, and these parallel components are counted separately. This is the convention underlying the source's torus gcd example. We do not collapse parallel copies to a single support curve, and we do not define a component count for arbitrary real-weight foliations by silently choosing a denominator or changing a coordinate normalization. Admissibility and coordinate conversion must be validated before applying the finite construction.

## 2. What the established algorithms already give

Agol–Hass–Thurston, [Theorem 12 and Corollary 13](https://arxiv.org/abs/math/0205057), count orbits of interval pairings in time polynomial in k log N, and count components of a normal curve on a t-triangle surface in time polynomial in t log W. Here W is its normal-coordinate weight. This is much stronger than mere decidability and avoids expanding W strands.

Lackenby's [2026 paper, Theorems 3.1–3.2](https://arxiv.org/abs/2401.16056), gives the corresponding standard-1-manifold formulation for a compact surface, including boundary endpoints. Its stated bound is polynomial in simp(C), log(w(C)+|∂C|), and the triangulation/handle-structure size. These are credited prior algorithms, not new consequences of our expanded matrix below.

Yurttaş–Hall, [Algorithm 9 and Lemma 10](https://arxiv.org/abs/1512.08341), work directly in Dynnikov coordinates on an n-punctured disk. Their O(n²M) arithmetic-operation bound uses M equal to the sum of absolute coordinate values. It is a useful concrete algorithm, but that displayed bound is not polynomial in log M. Their stated gcd formula for the three-punctured disk is a credited low-complexity case.

A 2025 paper by Yaguchi–Yamamoto, [DOI 10.1142/S0218216524500573](https://doi.org/10.1142/S0218216524500573), studies associated permutations and new cycle-counting notation. Its primary publisher preview and author bibliographies were available, but its complete text was not retrieved. We make no claim that its full results have been exhaustively assessed or that the general source problem is globally still open. The present package does not provide the required general expression.

## 3. Exact arc-sensitive permutation formula

Take a finite cut-and-glue description of a compact one-manifold C, consisting of disjoint circles and properly embedded arcs. Cut at finitely many transverse points so that every component under consideration is a union of compact segments. Normal arcs in triangulated pieces provide one such description. Any closed components deliberately left uncut must be counted separately; denote their number by c₀.

Let S be the set of all segment ends before gluing, and N=|S|. There are two involutions:

- α is fixed-point-free and pairs the two ends of each segment.
- β pairs ends that are identified at an interior cut. It fixes precisely the actual boundary endpoints of C.

Let f be the number of fixed points of β, and let p=αβ. Write c(p) for the number of cycles of this permutation, including one-cycles. Equivalently, if P is its N×N permutation matrix, c(p)=dim_Q ker(I−P).

The closed-case identity is the standard two-matching description of meanders; see Karnauhova–Liebscher, [§2.2, Proposition 2.2](https://arxiv.org/abs/1504.03099). The following proof includes the bookkeeping for boundary arcs. No priority is claimed for this elementary extension.

**Proposition 1.** The numbers A of arc components and L of cut closed components are

    A=f/2,                  L=(c(p)−f/2)/2.

Consequently,

    #π₀(C)=c₀+c(p)/2+f/4
           =c₀+[2 dim_Q ker(I−P)+f]/4.                      (1)

This is an exact identity for the expanded realization, including arcs, zero-width omissions, parallel copies and the empty realization. It is not claimed as the requested tractable formula in compressed coordinates.

### Proof

Construct a graph on S with an α-colored edge for each transposition of α and a β-colored edge for each transposition of β; fixed points of β contribute no β-edge. **Retain both colors when an α-edge and a β-edge have the same endpoints.** Such a two-edge circle must not be mistaken for a path by suppressing parallel edges.

Every vertex has one α-edge. It also has one β-edge unless it is a boundary endpoint. Thus every component is either an alternating even cycle or an alternating path whose two endpoints are fixed by β. These graph components are exactly the components obtained by gluing the segments, so A=f/2.

On an alternating cycle with 2k vertices, p=αβ moves by two steps. Its even and odd positions form two permutation cycles, each of length k. This includes k=1, when p has two fixed points. On an alternating path with 2k vertices, p has a single cycle: it runs in steps of two toward one endpoint, turns there using the fixed β endpoint, and returns on the other parity to the opposite endpoint. Hence each circle contributes two cycles of p, and each arc contributes one. Therefore c(p)=2L+A, which gives (1).

A vector fixed by a permutation matrix is constant on every permutation cycle, freely choosing one value for each cycle. This proves the kernel formula. For S empty, take the kernel dimension and f to be zero. Add back the c₀ uncut closed components. ∎

### A determinant form, and why it is still not enough

If the cycle lengths of p are ℓ₁,…,ℓ_c, then after reordering basis vectors,

    det(I−zP)=∏_(j=1)^c (1−z^ℓ_j).

Every factor has a simple zero at z=1 in characteristic zero. Thus

    #π₀(C)=c₀+½ ord_(z=1) det(I−zP)+f/4.                   (2)

The determinant formula is a restatement of the same expanded identity, not a new compressed evaluation procedure. In the closed case f=0 the factor of one half is essential. With arcs, simply halving the cycle count is wrong.

## 4. The precise size obstruction

A single integer weight K, encoded in binary with O(log K) bits, can stand for K parallel circles. Cut each circle once. The expanded description then has 2K ends, α=β pairing the ends of each segment, p the identity, and an identity-sized permutation matrix of dimension 2K. Formula (1) gives K exactly, but constructing that matrix already requires Ω(K) entries in a sparse explicit representation. A dense determinant is larger still.

Taking K=2^B shows that this expansion can be exponential in the bit length of the coordinate input. Even an O(N) cycle traversal is therefore not a polynomial-bit procedure for this representation. This is a limitation of the expanded formula, **not a computational lower bound for the counting problem**: AHT's compressed interval-pairing algorithm explicitly avoids it.

The missing step is an expression with a genuinely compressed description and controlled evaluation cost, or an independently justified closed-form notion acceptable for the source's request. Replacing serial splitting by an N×N determinant without controlling N does not supply that step.

## 5. Arithmetic diagnostics for possible formula classes

### A single global gcd is already insufficient

Take two distinct curves in a pants decomposition of a genus-two surface, each with unit weight and with all other weights zero. In the source's convention their only nonzero coordinates are the two twist entries 1 corresponding to m_i=0. The actual family has two components, whereas the gcd of every coordinate is 1. Thus the torus answer cannot be generalized by taking one gcd of the full coordinate vector. This does not rule out a more elaborate collection of gcd operations or case distinctions.

### No continuous homogeneous extension, even on a once-punctured torus

For the usual integer slope coordinates (u,v) on a once-punctured torus, the number of parallel components is gcd(u,v). This classical special case is already noted in the source. It gives the following narrow obstruction.

**Proposition 2.** There is no continuous function F on the positive real quadrant, positively homogeneous of degree one, whose values at all positive integer pairs equal gcd(u,v).

**Proof.** If such F existed, then

    F(1,1+1/n)=F(n,n+1)/n=1/n,

because consecutive positive integers are coprime. Continuity at (1,1) would imply F(1,1)=0. But its prescribed integer value is gcd(1,1)=1. ∎

In particular, a formula composed solely from finitely many continuous positively homogeneous operations, such as linear maps, addition, minimum and maximum, cannot be the answer even in this special case. The proposition does not prohibit gcd, discontinuous arithmetic operations, recursion, or other forms of closed expression. It is not an impossibility proof for Penner's broadly worded request.

### Related negative results must retain their own hypotheses

Karnauhova–Liebscher, [Theorem 5.3](https://arxiv.org/abs/1504.03099), rule out representing the component count of every bi-rainbow meander with n≥4 upper families as the gcd of two homogeneous integer polynomials in its family sizes. Their result concerns that specific formula class and meander encoding. It is not a theorem that no tractable expression of any kind exists. No unproved transfer from that encoding to every Dehn–Thurston coordinate chart is used here. Their logarithmic nose-retraction methods also emphasize how narrow a literal gcd-formula restriction can be.

## 6. Unresolved conclusion

The source's more-closed-form request is **unresolved by this work**. Existing polynomial-bit algorithms are credited and do not become discoveries. Proposition 1 is a fully explicit expanded identity and includes the necessary boundary-arc correction, but its uncompressed dimension can be exponentially large. Proposition 2 rules out only a limited continuous-homogeneous ansatz; the global-gcd diagnostic is even narrower.

No general compressed determinant evaluation, finite gcd formula, all-coordinate component formula, or description of A′(F)/Arc′(F) is supplied. The unavailable complete 2025 paper is an additional literature limitation, so this package does not certify the absence of a later answer. Priority for the elementary deductions is not asserted.
