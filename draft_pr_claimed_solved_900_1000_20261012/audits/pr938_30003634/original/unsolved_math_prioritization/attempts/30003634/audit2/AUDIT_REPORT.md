# Independent second audit: problem 30003634 / OWR-15955-011

## Decision

**ACCEPT the counterexample and its stated mathematical scope.** No mathematical correction is required to the frozen proof identified below. The result is

\[
P_3^{(3)}\not\subset F_1^3,
\]

with the same failure at index 1 after adding split trivial strands for every strand number at least 3. This disproves the universal containment asked in OWR Question 3. It does not prove failure separately at every higher filtration index, historical novelty, or present worldwide open status. This is a mathematical and computational audit, not formal verification or human peer review.

The reviewed author manifest has SHA-256 `d1e1467c6d36b6c62283af2ec50ddff8864020ad8a7c9e0ba9a6704dacb4246a`; the proof has SHA-256 `0492e0e0de785be263174e86d69855120b2f5c24b105c6479739cd72d64abe3b`. All 11 listed author files match their recorded sizes and hashes. The author files were not changed.

## Independence and replay

The second-audit checker was inspected and rerun without modification. It imports no author module. Its independent output reproduces the preserved 18,092-byte output byte-for-byte. The checker reconstructs the planar half-edge diagram rather than relying only on the author's syllable formula, uses maximum-magnitude rather than first-available scalar pivots, and computes the Meyer quadratic form from a kernel and pullback rather than the author's specialized generator formula. The new controls also import only this reviewer checker. The original second-audit code and outputs are preserved unchanged.

The author's executable and adversarial harness were separately replayed as tests of the supplied certificate software; these are not represented as independent mathematical algorithms. Their four execution modes accept the original certificate and reject all 88 mutated inputs.

## 1. Target and derived-series membership

The inspected [OWR report](https://publications.mfo.de/bitstream/handle/mfo/3612/OWR_2017_50.pdf?isAllowed=y&sequence=1), printed pages 34–35, defines the ordinary derived series starting with the whole group at index zero and asks about the `(n+2)` term versus filtration index `n`, for `n >= 1`. Thus third-derived membership and failure of 1-solvability are the correct indices. This is the classical disk pure braid group in ordered oriented string-link concordance, using ordinary link closure. It is not a lower-central or rational-derived-series question.

For `a = sigma_1^2` and `b = sigma_2^2`, both inputs are pure. The commutator `c = [a,b]` and its two conjugates `d = a^-1 c a`, `e = b^-1 c b` lie in the first derived subgroup by normality. Consequently `u = [c,d]`, `v = [d,e]` lie in the second derived subgroup, and `beta = [u,v]` lies in the third. This membership proof does not infer group membership from vanishing numerical invariants.

Direct free reduction gives precisely the author's 104-letter word and its 46 syllables. Tracking strand labels returns the identity permutation and all three signed pairwise crossing sums equal to zero. Dividing those sums by two gives the three linking numbers zero. The two exponent sums also vanish. Deleting other strands leaves the single trivial pure strand, so the individual components are unknotted; this is auxiliary and is not used to manufacture the signature obstruction.

## 2. Diagram and signature

The independent planar construction has 104 vertices, 208 edges, and 106 faces, with 49 alpha regions. Deleting the exterior alpha region gives a 48-dimensional Goeritz matrix. The saved region permutation carries that diagram matrix **entry-for-entry** to the supplied matrix.

The [Erle version of record](https://da.lib.kobe-u.ac.jp/da/kernel/E0003685/E0003685.pdf), section 2, was checked in text, and printed pages 162–165 were inspected visually. The crossing rule, exterior region, exceptional-crossing rule, and illustrated block matrix agree with the construction. The displayed off-diagonal index in Proposition 2.3 and the corresponding sentence of its proof use the preceding block's sign; the picture and direct crossing count use the current block's sign. The frozen proof already discloses this qualification correctly.

A negative control implemented the erroneous preceding-block off-diagonal index while retaining the printed diagonal rule. It changes 68 matrix entries for this word but happens to retain inertia `(23,25,0)`. Agreement of signatures alone would therefore be an inadequate check of this indexing issue. The actual diagram-to-certificate matrix identity is the decisive check.

Exact rational symmetric congruence, with a 2-by-2 fallback available for zero diagonals, gives

\[
(n_+,n_-,n_0)=(23,25,0),\qquad \det(G)=-7154819319988224.
\]

The independent exact determinant uses SymPy's domain Gaussian elimination. The author separately supplies and replays scalar Schur-complement pivots and a Bareiss determinant. The exceptional crossings are the sigma-1 crossings; their signed sum is zero. Accordingly the signature is `23 - 25 - 0 = -2`. No floating-point eigenvalue threshold is involved.

## 3. Independent Meyer corroboration

The independent checker uses the two 2-by-2 Burau matrices printed in section 4.2 of [Gambaudo–Ghys](https://www.numdam.org/item/10.24033/bsmf.2496.pdf). For each prefix `A` and next generator `B`, it takes the kernel of `[A^-1-I | -(I-B)]`. Mapping a kernel vector `(v1,v2)` to the common image `e` pulls back the quadratic form `det(v1+v2,e)`. The kernel of this map is in the form's radical because the form is well defined on the common image; pulling back therefore preserves signature. This also handles singular matrices without inverting a nonexistent inverse on the whole space.

The 104 terms agree individually with the author's list: 50 positive, 48 negative, and 6 zero. Theorem A gives the negative of their sum since the individual generator closures have signature zero. The resulting signature is again `-2`. The final Burau matrix also agrees exactly and has determinant one.

No signature homomorphism assumption appears. Indeed the controls find signature `c = d = e = 0` but signature `[c,d] = 2`. This explicitly demonstrates why a homomorphism shortcut would invalidate the argument.

## 4. The full 1-solution obstruction

The relevant definition is [Otto Definition 2.3](https://msp.org/agt/2014/14-5/agt-v14-n5-p05-s.pdf), printed pages 2631–2632. It is an integral smooth zero-surgery definition with an integral `H1` isomorphism and an embedded framed hyperbolic basis in `H2`; at index one both sets of surface groups land in the commutator subgroup. The source explicitly defines a string link's solvability through its closure. The frozen proof matches these requirements.

Here is the reasoning independently checked in full:

1. Zero pairwise linking makes the zero-surgery first homology free on the meridians. Sending every meridian to `-1` is therefore a well-defined character, and the integral `H1` isomorphism extends it to a putative 1-solution `W`.
2. The sign-character cellular matrices are integral. Modulo 2 they become the untwisted cellular matrices. A minor nonzero modulo 2 is odd and hence nonzero over the rationals. Each twisted boundary-map rank is consequently at least its untwisted mod-2 rank. The chain dimensions are equal, giving `dim H2(W;Q_alpha) <= dim H2(W;F2)`.
3. The integral hyperbolic basis makes `H2(W;Z)` free of rank `2r`, and `H1(W;Z)` is free. The universal coefficient theorem therefore gives `dim H2(W;F2) = 2r`; no hidden torsion term is omitted.
4. Both sets of surfaces have trivial restricted sign character. Each hence defines a twisted homology class. Framing kills self-intersections; disjointness kills all unintended pairings; each dual pair has one transverse intersection with a nonzero coefficient `+1` or `-1`. Rescaling one class in a pair gives a hyperbolic block. The resulting nondegenerate `2r`-dimensional subspace proves independence. Combined with the upper bound, it is all twisted `H2`.
5. Thus both ordinary and twisted signatures of `W` vanish. This argument uses local coefficients on the zero-surgery filling itself, not a presumed relative solvable cobordism of link exteriors.

Finally, [Toffoli](https://epub.uni-regensburg.de/52299/1/the-atiyahpatodisinger-rho-invariant-and-signatures-of-links.pdf), equation (1.1), gives the bounding signature defect. The one-color specialization in Remark 4.25, equation (4.21), equivalently Corollary 4.28, identifies that defect with minus the ordinary Levine–Tristram signature when the linking and framing matrix is zero. The one-color Seifert framing is zero here. The permitted domain is the unit circle excluding 1, so `-1` is allowed without an Alexander-polynomial nonvanishing assumption. This forces the ordinary signature to vanish, contradicting the computed `-2`.

[Cha Theorem 8.2](https://ems.press/content/serial-article-files/31720), at `n=1`, `p=2`, `d=2`, corroborates the finite-character obstruction; its statement, rank comparison, and the proof's twisted pairing argument were checked. The direct argument above does not require importing the general tower machinery. A stronger spin convention would only restrict the possible fillings and cannot remove this obstruction.

## 5. Controls and acceptance limits

In addition to the 12 known-link normalization controls in the original independent output, the recovery controls passed:

- 6 exact matrix-inertia tests, including a zero matrix, a singular form, and an off-diagonal hyperbolic block;
- all 256 four-syllable words with exponents in `{-4,-2,2,4}`, comparing the half-edge diagram, syllable matrix, correction, and independent Meyer result;
- 9 target transformations, including inverse, mirror, reversal, doubling, and cyclic rotations;
- 12 contextual Artin-relation tests, 16 adjacent inverse-pair insertion tests, and 4 conjugation tests;
- the non-homomorphism and wrong-index controls explained above.

The independent controls were also replayed from read-only relocated copies, in a different working directory, in normal, `-O`, `-OO`, and `PYTHONOPTIMIZE=2` modes. The output is identical and the relocated files are unchanged. The independent checker requires SymPy; the author verifier requires only Python's standard library. Tested versions are Python 3.12.14 and SymPy 1.14.0.

All nine stored source PDFs match the author's public size/hash metadata. Mathematical source inspection in this audit is limited to the six dependencies identified above; matching the other PDF hashes is not represented as reviewing their claims. Copied PDFs, extracted source text, source screenshots, private search/coordination material, and the author packet are excluded from this audit packet. Novelty and literature-completeness assertions were not independently established.

**Final assessment:** the explicit third-derived word, the exact signature computation, and the full zero-surgery 1-solvability obstruction form a valid proof of the stated counterexample. No unresolved mathematical blocker was found.
