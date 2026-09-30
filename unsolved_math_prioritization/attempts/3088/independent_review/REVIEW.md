# Independent adversarial review: 3088 / OPG-56328

**Verdict: PASS_SCOPED_LEMMAS_AND_FINITE_CERTIFICATE.** No mandatory mathematical corrections. The original arbitrary four-part partition problem remains **unsolved**, with the author's three recorded approach families. This review does not establish a continuum counterexample or a full rigidity theorem.

Reviewed on 2026-09-30 by a separate gpt-6-astra agent at xhigh reasoning. This is an AI review, not human peer review; no priority claim is made. Frozen `PARTIAL_RESULT.md` SHA-256:

`f53af31e3e4745f6894d6e8874e400cf44046fbaf8a676aa052ec76ad02dc183`.

## 1. Exact primary-source scope

I independently read Jonathan Noel's [MathOverflow question140413](https://mathoverflow.net/questions/140413/partitioning-the-projective-plane), posted26August2013, and the [Open Problem Garden statement](https://www.openproblemgarden.org/op/partitioning_the_projective_plane), posted27August2013. The target is a partition of the actual real projective plane into four arbitrary weakly octahedral sets. No openness, measurability, connectedness, convexity, nonempty-interior, or finite-complexity condition is imposed. The triple inequality is non-strict, so perpendicular pairs are allowed. Closed regular-octahedron faces correspond to orthogonal closed octants, not arbitrary simplicial cones.

Both primary postings explicitly give the sign-invariant triple criterion used by the artifact. Changing representatives multiplies the product by a positive square. The postings also already discuss weakly octahedral sets that are not octahedral, so such a single-set example is not a resolution or novelty claim. I found no resolution in the bounded exact-phrase search. Similarly titled work about simplicial-complex partitionability or finite incidence planes addresses different questions.

## 2. Closure and the interior-dependent cone lemma

**Lemma1 passes.** For three distinct limit points, disjoint projective neighborhoods permit independently chosen approximating points and continuous local unit lifts. The inequality passes to the limit. If two limiting projective points coincide, the expression is automatically a nonnegative square times a positive norm. Thus the restriction to three-element subsets causes no gap at degenerate limits.

**Lemma2 passes with exactly its stated nonempty-interior hypothesis.** If $p$ is an interior representative and $x\perp p$ represents a point of the closed class, the lines of $x,p+tx,p-tx$ are distinct for sufficiently small $t>0$, the latter two belong to the class, and their triple product is $-t^2(1-t^2)<0$. Therefore the compact class avoids the entire perpendicular projective line. The positive-$p$ unit lift is continuous and compact, giving a uniform $\delta>0$. Applying the triple criterion to $p,x,y$ forces $x\cdot y\ge0$; when one line repeats, this conclusion follows directly from the chosen orientation.

The generated cone is genuinely closed. Every finite positive combination $v=\sum a_jx_j$ satisfies $p\cdot v\ge\delta\sum a_j$, so a convergent sequence of such combinations has bounded total coefficient mass. The convex hull of the compact lift is compact in finite-dimensional Euclidean space, for example by Carathéodory's theorem. A subsequence argument in the scalar-times-convex-hull representation gives a limit in the cone. Moreover $p\cdot v\ge\delta\|v\|$ on it, so nonzero cone vectors have positive pairing with $p$ and the cone is pointed. Bilinearity preserves pairwise nonnegative inner products, including on the closure.

For this fixed lift, containment in an orthogonal positive octant is indeed equivalent to its dual cone containing an orthonormal basis. The artifact does not incorrectly deduce existence of that basis from acuteness alone.

The stated limitations are material and correct: Baire applied to the four closed closures supplies at least one with interior, not all four. Closure may introduce intersections, and convexification may introduce further intersections. No step justifies replacing the arbitrary partition by four acute cones forming a face-to-face fan. The proof does not make that replacement.

## 3. Three-central-plane partition rigidity

**Proposition3 passes.** Under the extra sign-partition hypothesis, every open sign chamber belongs to its specified color. Its projective closure is therefore contained in that color's closure, which is weak by Lemma1. Let $v_i$ be the inverse-matrix columns. If $v_i\cdot v_j\ne0$, one of the signed chambers has normalized extreme rays $a,b$ with $c=a\cdot b<0$. Linear independence ensures $-1<c<0$. The sum $z=a+b$ is nonzero and lies in the same closed chamber; its line is different from each extreme line. The exact obstruction is

$$ (a\cdot b)(a\cdot z)(b\cdot z)=c(1+c)^2<0.$$

Thus every off-diagonal Gram entry of the inverse columns is zero. If the forms have matrix $M$ and $V=M^{-1}$, then $V^TV$ is positive diagonal, and $MM^T=(V^TV)^{-1}$ is diagonal as well. Hence the plane normals are orthogonal. The incident-boundary assignment hypothesis then puts every assigned part inside the corresponding pair of opposite closed orthants.

There is no use of a forbidden boundary triple being in the original part: membership in its closure is sufficient. Conversely, the proof relies on all sign-chamber interiors being assigned in the prescribed way; it proves nothing about arbitrary curved or disconnected partition boundaries.

## 4. Four-ray witness

The Gram matrix of the four displayed vectors, in their stated order, is

$$\begin{pmatrix}2&0&1&1\\0&2&1&1\\1&1&2&0\\1&1&0&2\end{pmatrix}.$$

Every triple satisfies the nonnegative-product condition. In any hypothetical common orthant lift, positivity on the connected four-edge cross-pair graph forces all four representative signs to agree. For nonnegative coordinate vectors, zero inner product means disjoint positive-coordinate supports. The two disjoint pairs therefore force the four positive cross-pairs to use four pairwise disjoint nonempty intersections of supports. There are only three coordinates, a contradiction. This verifies nonoctahedrality without conflating arbitrary sign choices with a fixed lift or discarding the allowed zero inner products.

The independent check additionally exhausted all2,401 ordered nonempty support-pattern quadruples in three coordinates; none satisfies those intersection requirements. A four-coordinate support pattern does satisfy them, which provides a useful negative control. The finite enumeration is supplementary; the support proof works directly.

## 5. Finite coloring and verification independence

I copied the submitted proof, verifier, coloring, and receipt to `author_replay/`, then ran the verifier there. All497,651 assertions pass, and the regenerated receipt is byte-for-byte identical. All497,640 triples among145 directions were examined by that verifier;125,614 have negative product. The witness lines all receive color0.

The independent script regenerates the projective directions by rational affine normalization, rather than the submitted primitive-integer/gcd filter. It finds the same145 lines. It recomputes the Gram matrix, checks all35,699 monochromatic triples grouped by color, independently recounts all125,614 negative hyperedges, verifies the fixed witness, and checks exact sign, support, interior-point, and negative-extreme-ray controls. All35,755 independent assertions pass. Color sizes are45,40,41,19, so this is a genuinely four-nonempty-color finite certificate.

I also inspected `search_finite.py`: its hyperedges correspond to negative-product triples, its fixed singleton domains prescribe the four witness lines, and its output is validated without trusting propagation. The search need not be rerun for certificate verification and is not treated as a proof of nonexistence or of any infinite extension.

The certificate only establishes satisfiability of one finite restriction. Nothing in it produces a coloring of all projective directions or colorings satisfying every finite constraint with the prescribed witness. In particular, it does not invoke compactness from one finite instance. The artifact preserves exactly that limitation.

## 6. Reproduction and final classification

Run the following from this review directory:

```sh
python author_replay/verify.py
python independent_checks.py
```

Both scripts use only the Python standard library. The author's source/proof and coloring were not edited. The replay verifier rewrites only the copied deterministic receipt in `author_replay/`.

Recommended classification: **unsolved, 3/5 substantive approaches**. The restricted cone and linear-sign-partition lemmas, four-ray obstruction, and finite certificate are valid at their stated scope. The missing step is still global structure or a global construction for a four-part arbitrary partition. No new novelty or full-resolution claim is warranted.
