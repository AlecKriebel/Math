# Independent review of the component-counting partial results

**Verdict: PASS_SCOPED_EXPANDED_FORMULA_AND_ARITHMETIC_OBSTRUCTIONS.** The expanded formula, its boundary correction, and the narrow arithmetic diagnostics are correct. The original more-closed-form request remains **unsolved, 3/5**. No mandatory correction is required. This is an independent adversarial AI review, not human peer review or a novelty claim.

The frozen `OBSTRUCTION.md` has SHA-256 `d61362249f605820d868da5c1aef8c7da80a924573a5743703cae7261b220bdf`. All 7,775 author controls reproduce byte-identically. A separate implementation passes 10,900 exact controls on 1,173 involution-pair cases and arithmetic diagnostics.

## 1. Original task and coordinate conventions

I inspected Penner's complete preprint and the rendered manuscript pp.106–107 of the cited volume. Problem 2 asks for a tractable component-count expression for one weighted disjoint curve-and-arc family. The next paragraph explicitly acknowledges serial train-track splitting and asks for a more closed-form expression. Merely exhibiting a terminating or polynomial-bit algorithm therefore does not justify claiming the requested result. The source does not formalize a grammar of closed forms, so the partial results also cannot prove impossibility for every admissible interpretation. [Primary volume, pp.106–107](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf), [Penner's complete preprint](https://arxiv.org/abs/math/0505595).

The source uses nonnegative intersection coordinates and the identification of opposite twist rays when intersection is zero, with a framed pants decomposition and boundary windows. Those conventions differ from an unconstrained signed integer vector. The candidate correctly restricts its finite formula to an actual integral realization after admissibility and conversion have been checked. In particular, it does not supply a conversion theorem showing that every formal coordinate tuple yields its chosen unit-strand normalization. Parallel integral copies are counted with multiplicity, in agreement with the source's torus gcd example; arbitrary real measured foliations are outside this finite formula.

## 2. Expanded formula, including boundary arcs

Let alpha pair the two ends of each segment, and let beta identify interior cut ends while fixing the genuine boundary endpoints. Alpha is a fixed-point-free involution. In the colored multigraph on segment ends, every vertex has one alpha edge and either one beta edge or is fixed by beta. Consequently every connected component is an alternating even cycle or an alternating path with two beta-fixed ends. Parallel edges of the two different colors must be retained: an alpha edge paired to the same beta edge is a circle with one segment, not an interval.

On a cycle with 2k ends, alpha beta advances two steps and has two cycles of length k. On a path with 2k ends, it advances along one parity, turns at a beta-fixed endpoint, returns on the other parity, and forms one cycle of length 2k. Thus, writing f for the number of beta-fixed points and c for the cycle count of alpha beta,

\[
A=f/2,\qquad c=2L+A,\qquad
\#\pi_0(C)=c_0+c/2+f/4.
\]

This includes the single-segment interval, the single-segment circle, parallel copies, and the empty cut realization. The separate term c0 is necessary for closed components that were never cut.

A vector fixed by a permutation matrix is constant on each permutation cycle, so c=dim_Q ker(I−P). After ordering each cycle consecutively, its characteristic determinant contributes 1−z^ell. Its zero at z=1 is simple in characteristic zero; hence ord_(z=1)det(I−zP)=c. This independently verifies both displayed formulas. Using the closed-case factor one-half without the f/4 correction fails already for one arc.

The cited meander Proposition 2.2 distinguishes the cycle count of its single meander permutation from the cycle count of the product of its two matchings; the latter is twice the number of closed components. The candidate uses this latter convention correctly. Its separate path argument supplies the boundary extension. [Karnauhova–Liebscher, Section 2.2](https://arxiv.org/abs/1504.03099).

## 3. Size obstruction and arithmetic diagnostics

A weight K on a pants curve can represent K parallel circles. Cutting each once creates 2K ends, alpha=beta, and P=I_(2K). The formula returns K, but explicitly listing even the nonzero entries requires order K entries. When K=2^B, this expands exponentially relative to its B+1-bit encoding. The determinant is thus not, by itself, a compressed-coordinate solution. This is a limitation of this representation and evaluation proposal, not a lower bound for component counting.

For the global-gcd diagnostic, choose two distinct pants curves on a genus-two surface with unit weights. Their zero-intersection twist coordinates are both one, giving coordinate gcd one but two components. This disproves exactly the single-gcd shortcut, not a richer arithmetic formula.

The continuity obstruction is also valid: a degree-one positively homogeneous extension F of gcd would satisfy F(1,1+1/n)=1/n, whereas its value at (1,1) must be one. Continuity would force that same value to be zero. This excludes only the stated continuous homogeneous ansatz, including compositions of the listed continuous homogeneous operations. It does not exclude gcd itself, case distinctions, recursion, or every possible meaning of closed form.

## 4. Existing algorithms and restricted impossibility results

The source attributions are accurate and must remain prominent:

- Agol–Hass–Thurston Theorem 12 gives orbit counting polynomial in k log N. Corollary 13 gives component counting for a normal curve polynomial in t log W. I checked both statements and the corollary's reduction to interval pairings. The candidate does not claim this as its own consequence. [Primary paper](https://arxiv.org/abs/math/0205057)
- Lackenby's Theorems 3.1–3.2 state the interval-pairing and compact-surface standard-one-manifold versions, with polynomial dependence on simp(C), log(w(C)+|boundary C|), and the triangulation or handle-structure size. Boundary endpoints are explicitly retained. [Primary paper](https://arxiv.org/abs/2401.16056)
- Yurttas–Hall's Algorithm 9 and Lemma 10 use O(n²M) arithmetic operations in the stated sum-of-absolute-coordinates parameter M. This displayed bound is not polynomial in log M; the candidate makes the correct distinction. [Primary paper](https://arxiv.org/abs/1512.08341)
- Karnauhova–Liebscher Theorem 5.3 excludes the gcd of two homogeneous integer polynomials for every bi-rainbow meander with at least four upper families. It is a restriction on that formula class and encoding. The candidate neither transfers it without proof to all Dehn–Thurston charts nor turns it into a universal nonexistence theorem. [Primary paper, Theorem 5.3](https://arxiv.org/abs/1504.03099)

The complete 2025 Yaguchi–Yamamoto paper was unavailable to the author. This review has not filled that literature gap, and does not certify that no later solution exists. The candidate expressly records the limit. The justified disposition is that this work does not resolve Penner's requested general expression.

## 5. Independent controls and remaining gap

The submitted verifier was replayed with its exact frozen receipt. The independent program enumerates every fixed-point-free alpha and every involution beta on zero, two, four and six ends, rather than fixing one alpha. It counts glued components by disjoint-set union and computes permutation cycle counts using Burnside fixed-point averages over a common period. Thus its two sides are obtained by separate methods. It also checks uncut-component offsets, both smallest arc/circle cases, and the narrow arithmetic diagnostics.

Reproduction:

```
python author_replay/verify.py
python independent_checks.py
```

All 10,900 independent assertions pass. These are finite expanded-gluing checks; they prove no coordinate admissibility theorem, compressed complexity bound, or exhaustive topological classification.

The missing step remains a suitable general expression directly controlled by compressed coordinates, or a justified formal interpretation of the requested closed form with an evaluation meeting that interpretation. The correct status is unresolved. Preserve the exact boundary correction, integral-realization qualification, exponential expansion example, credited algorithms, and unavailable-literature qualification in publication.
