# 10400099 / Ohtsuki Conjecture 5.3: a consequence of the boundedness theorem

**Status: credited known affirmative answer; independent source/proof review pending.** The exact conjecture follows directly from Michael Eisermann's published 2000 boundedness theorem. No new theorem, priority claim, or fresh proof-search attempt is asserted.

## 1. The recovered statement

The [original source](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), Ohtsuki (editor), *Problems on invariants of knots and 3-manifolds*, Geometry & Topology Monographs 4 (2002), printed p. 459, defines

$$h_X(K)=|\operatorname{Hom}_{\rm Quandles}(Q(K),X)|,$$

where $X$ is a fixed connected finite quandle and $Q(K)$ is the fundamental quandle of a classical knot in $S^3$. Conjecture 5.3 says that $\log h_X$ cannot be a Vassiliev invariant unless it is constant. The material about quandle cohomology following that sentence in the imported record belongs to the next section and is not part of the conjecture.

We use the natural logarithm as a real-valued invariant, hence also as a complex-valued invariant. Any other fixed logarithm base greater than one changes it by a nonzero scalar and does not change finite-type status. The quandle is nonempty, so writing $q=|X|$ gives $q\ge1$.

## 2. The applicable published theorem

Michael Eisermann, [*The number of knot group representations is not a Vassiliev invariant*](https://pnp.mathematik.uni-stuttgart.de/igt/eiserm/publications/twistseq.pdf), Proc. Amer. Math. Soc. **128** (2000), 1555–1561, DOI 10.1090/S0002-9939-99-05287-9, proves in **Theorem 3** the following general boundedness statement:

If a complex-valued knot invariant $F$ satisfies

$$|F(K)|\le\varphi(b(K))$$

for some function $\varphi:\mathbb N\to\mathbb N$, where $b(K)$ is braid index, then $F$ is constant or is not of finite type.

The theorem is not restricted to representation counts or rational-valued invariants. Its proof in §1 uses polynomiality of finite-type invariants on twist sequences, bounded braid index along vertical twist sequences, and crossing-change connectivity to the unknot. Thus its coefficient and knot-category hypotheses include the logarithm in the source question.

## 3. Complete deduction for finite quandles

**Proposition.** For any finite nonempty quandle $X$ and classical knot $K$,

$$q\le h_X(K)\le q^{b(K)}.\tag{1}$$

**Proof.** The $q$ constant colorings exist by the idempotent axiom $x*x=x$. For the upper bound, represent $K$ as the closure of a braid with $b(K)$ strands. Colors at the top of these strands determine every color through the braid: at a positive or negative crossing the quandle coloring rule uniquely determines the outgoing under-strand color, using a right translation or its inverse, and the over-strand color is unchanged. Thus there are at most $q^{b(K)}$ possible braid colorings. The closing conditions can only remove assignments. The standard correspondence between diagram colorings and homomorphisms from the fundamental quandle gives (1). ∎

If $q=1$, the logarithm is identically zero. For $q\ge2$, (1) implies

$$0\le \log h_X(K)\le b(K)\log q\le q\,b(K).$$

Consequently $F(K)=\log h_X(K)$ meets Eisermann's Theorem 3 with the integer-valued bound $\varphi(n)=qn$. If $F$ is finite type, it must be constant. This proves the exact conjecture. Conversely, a constant invariant is finite type of order zero.

Connectedness was not needed for this deduction, so it certainly covers the connected finite quandles in the source. Nothing is assumed about faithfulness, Alexander form, or prime cardinality.

### Why the logarithm creates no coefficient problem

The imported theorem explicitly has target $\mathbb C$, which contains $\mathbb R$. There is no inference that a generally irrational logarithm is rational-valued. The finite-type extension uses the usual additive skein difference, not multiplicative differences of coloring counts.

For context, the key polynomiality step can also be read directly from that skein definition. On a two-strand twist family, an $(m+1)$-fold finite difference is, up to an overall sign, the alternating resolution of $m+1$ selected crossings, one in each extra full-twist block. It vanishes for a type-$m$ invariant. The values therefore form a complex polynomial sequence of degree at most $m$; boundedness makes it constant. The source's Corollary 5 explains how this yields invariance under a crossing change and hence constancy on knots. This argument concerns characteristic-zero numerical invariants; it does not impose the same conclusion on finite-field-valued reductions.

### Normalization

The proof uses the literal total homomorphism count and does not use the preceding source remark about connected-sum multiplicativity. If one instead uses the common normalized count $h_X/q$, its logarithm differs from the literal one by the constant $\log q$. Adding a constant preserves finite-type status and constancy, so the same conclusion holds. No multiplicativity assumption is needed under either normalization.

## 4. Attribution and source status

The general boundedness theorem predates the 2002 problem collection. The quandle-coloring bound and the same bounded-twist argument are also explicitly discussed in Cheng–Gao, [*Positive quandle homology and its applications in knot theory*](https://msp.org/agt/2015/15-2/agt-v15-n2-p11-p.pdf), Algebraic & Geometric Topology **15** (2015), 933–963, §2. Their discussion concerns coloring counts; the present deduction applies the already-published boundedness theorem to the logarithm.

This audit did not locate a publication explicitly advertising a numbered resolution of Ohtsuki Conjecture 5.3. That bibliographic qualification does not leave a mathematical gap in the direct theorem application above. The package is a credited source correction and validation of known results, not a campaign discovery.

## 5. Reproducible controls

Run `python verify.py` here. It checks finite quandle axioms and braid color propagation for small dihedral examples, exact closed two-braid coloring counts, and the finite-difference algebra behind the quoted polynomiality principle. No floating-point logarithms are used. These examples do not prove the universal quandle bound or Eisermann's theorem; their complete applicable arguments are stated above and in the cited source.
