# Independent review: 30004313 / OWR-17294-014

## Binding verdict

**PASS_SCOPED_PARTIALS. The original classification remains unsolved, with five substantive author turns completed. No mandatory mathematical or source correction.**

This review binds the unchanged author `FROZEN_MANIFEST.json`, SHA256 `abccaf9cf1f2cb23cfce3b3127310f5cf9516acef87a0b05acc3692609eb1022`, and all its 28 files. In particular:

- `PROOF_COLLECTION.md`: `70543aa28dba6dc8ada33e93b45779d271d9b4e97b891a6a3faf4726c877111d`
- `RESULT.md`: `5ea59f98b0b7458e32903eaed09e691c82d991339a522d97832ed807b6903329`
- `turns/TURN_5.md`: `4e261a5b8d2b2b2637d2cc15fffdc62c0b67072e4a982e83a06e180342c9d3a6`

The review is an independent AI mathematical audit, not journal peer review or certification of novelty. The reviewer did not contribute to the author derivations. The reviewer read all five complete proofs, both catalogue programs and all five author diagnostic programs before independently writing the attached checker. No frozen author file was edited.

## Exact target and scope

The target is Catino's Question 2, with Colazzo and Stefanelli, in OWR 51/2019, printed p.3234. Multiplication is an arbitrary completely regular semigroup; addition is any associative semigroup satisfying the specified left compatibility identity. The inverse is the commuting group inverse of each element. Neither a global identity nor inverse anti-multiplicativity is available in general. All three braid coordinates are required, with no bijectivity or nondegeneracy requirement on the map. The source and later-paper distinctions are documented in `SOURCE_AUDIT.md`.

The packet gives exact all-size theorems in selected subclasses. It does not characterize arbitrary two-argument additions on general completely regular multiplication. The rectangular counterexamples disprove automatic solution assertions, not the possibility of a future classification. Five genuine mathematical increments are present; no retrieval, packaging, replay or review was counted as a proof turn.

## Analytic audit of the five turns

### 1. Meet multiplication and retracted addition

For `a+b=f(b)`, associativity is precisely `f²=f`. The compatibility identity is `a∧f(c)=f(a∧f(c))`, equivalently a retraction onto a lower subset. The two three-coordinate braid expressions in the proof were recomputed directly. Their middle coordinate forces deflationarity by choosing the input from the image, and the first coordinate gives monotonicity. Conversely these conditions give both identities. No greatest element of the ambient semilattice is needed.

The reformulation by a greatest image element below each input is valid: a monotone deflationary retraction fixes each image element below the input and hence dominates it. When a top exists this specializes correctly to meet with a fixed element. The fork and chain failures distinguish the two conditions; the constant-zero solution demonstrates that product preservation is not an admissible hidden axiom.

The projection-addition calibration was separately substituted into the original formula. Right-zero addition gives `(ab,b^0)` and left-zero addition gives `(a^0,ab)`. Their stated cryptogroup criteria and idempotence follow without using an inverse anti-law. This resolves the source example's convention discrepancy locally and correctly.

### 2. Projection multiplication and the coinciding-law Rees case

For left-zero multiplication, the compatibility law forces exactly additive idempotence; for right-zero multiplication it forces `x+y+z=x+z`. In the latter case the addition need not be a band. Direct braid composition verifies the asserted solutions in both cases.

The four-element rectangular example has associative addition and satisfies compatibility. Its two braid outputs at `(0,1,1)` differ in the third coordinate, so it is a valid failure of automatic Yang–Baxter, within the original source class.

For coinciding addition and multiplication in an arbitrary Rees presentation, comparison of the group coordinates gives precisely

`p_(mu,k)=p_(mu,i) p_(lambda,i)^(-1) p_(lambda,k)`.

This is equivalent to row-column factorization of the sandwich matrix. The displayed coordinate normalization preserves the order of the noncommuting group factors. After normalization the map decomposes into row duplication, the standard group conjugation solution, and column duplication; recomposition verifies every coordinate. No assertion about arbitrary addition follows from this special case.

### 3. Left-ideal retractions and the one-column criterion

For arbitrary completely regular multiplication, the compatibility equation is exactly `a f(c)=f(a f(c))`. Thus it is equivalent to the left-ideal image condition, once `f²=f` is imposed. Inverse closure of that image follows from `x^-=(x^-)²x`, not an inverse anti-law.

The one-column normalization `N(i,g,lambda)=(i,v_i g,lambda)` with `p'_(lambda,j)=p_(lambda,j)v_j^(-1)` is a valid semigroup isomorphism. Recomputing the two braid words before assuming row preservation shows that their middle rows force it. Only thereafter does the remaining group equation become idempotence of `H(g)=psi(g)^(-1)g`. This also proves sufficiency and recovery of every parameter. No condition that H fix the identity, be a homomorphism, or have subgroup image is needed.

The explicit nonhomomorphic example is valid. For the complementary endomorphic-retraction theorem, uniqueness of the commuting inverse justifies preservation of inverses by the homomorphism. The proof's use of `a f(b)=f(a)f(b)` follows because this product lies in the fixed image. The braid middle coordinates reduce exactly to the right-cryptogroup condition on that image; the third coordinates agree. The proof never assumes the globally invalid formula `(ab)^-=b^-a^-`.

### 4. Complete multi-column Rees parametrization for retracted addition

Every nonempty left ideal is a union of full columns: the explicitly chosen left multiplier reaches an arbitrary row and group coordinate while retaining the column. This covers all such images, including infinite groups and index sets.

Before any simplification, the middle output rows force the retraction to preserve the original row. Then `f(b)^0 b=b` and `(a f(b))h_f(b)=ab` are justified by the local Rees identity. The two complete braid outputs reduce to the same first entry, with middle equality exactly

`f(h_f(c))=f(c)^0`.

This equation also forces `h_f(h_f(c))=h_f(c)`, so the third coordinate is not omitted. Conversely these identities make both full braid words equal.

The parameter formula

`f(i,g,mu)=(i,g H(g)^(-1) p_(kappa(g),i)^(-1),kappa(g))`

has residual `(i,H(g),mu)` with the order shown. The output-column equation is `kappa∘H=kappa`; after it is imposed, the remaining local-group equation is `H²=H`. The prescribed image-column values make f the identity on its image, and recovery of H and kappa from f is unique. The coupled-column failure is genuine. These are necessary and sufficient conditions on the entire stated retracted-addition family, not only endomorphic examples.

### 5. Clifford component rigidity and the remaining gap

Here central idempotents first establish the inverse anti-law and `(xy)^0=x^0y^0`. A left ideal is a union of full groups and is two-sided: `xs=(xs)x^0` with `x^0` in the ideal. These facts justify that both coordinates of the map land in the fixed image.

Recomputing all three braid coordinates gives the author's expressions. The third coordinate makes `h(c)` idempotent. The middle equation, evaluated at `b=f(c)`, then gives `e_c≤c^0` and hence `f(c)=e_c c`. In the first equation, setting `a=(b f(c))^-` is legitimate and yields `b^0 e_c≤e_b`; choosing c to be any image idempotent below `b^0` proves that `e_b` is its greatest such lower image idempotent. This proves uniqueness without cancellation in the semigroup.

Conversely, the greatest-element map tau preserves meets: each side of `tau(ed)=tau(e)tau(d)` is bounded by the other using the lower-image property and the two greatest-element conditions. Thus `f(b)=tau(b^0)b` is an endomorphic retraction and yields a solution. In a monoid the criterion reduces correctly to a principal central-idempotent ideal. The diamond obstruction has no greatest image idempotent below the top, despite having many compatible set retractions.

The product with an arbitrary nontrivial group produces genuine dependence on both additive inputs and retains the explicit rectangular failure. Taking addition equal to multiplication on the same rectangular group instead gives a solution. This establishes the claimed obstruction family without turning it into a characterization of arbitrary addition.

## Finite evidence and its limits

All 28 author hashes and all four pinned primary PDF hashes match. The five author outputs reproduce byte-for-byte, with 436,129 total recorded exact assertions. Both bounded catalogue outputs also reproduce byte-for-byte. Their enumeration is labeled and finite: the size-at-most-three enumeration exhausts binary tables; the fixed four-element rectangular enumeration exhausts its forced column profiles and remaining row bits before applying associativity. These bounds cannot establish an infinite classification.

The independently written `independent_checks.py` imports no author code. It passes **2,760,310 exact assertions**, including all three coordinates for the positive tested solutions. Its test families include:

- All associative labeled additions of sizes 1, 2 and 3 for both projection multiplications
- Meet retractions on a chain, a non-top fork and a Boolean diamond
- All 216 retractions onto two columns of a nine-element C3 Rees semigroup, with exactly 38 solutions
- Six noncommutative D4 parameter models on 48 elements with a genuinely nonfactorizing sandwich matrix, plus a direct normalization check
- A global inverse anti-law negative control and direct left/right projection-addition substitution
- 164 retractions in a 13-element Clifford semigroup with top group D4, two different C2 quotient components, and a trivial bottom component
- The four-element failure, its D4 direct product, and the successful coinciding-law comparison

The fresh controls are diagnostics for the analytic audit, not substitutes for the arbitrary-cardinality proofs or a proof of historical novelty. Fixed-seed sampling is identified as such in the checker; only the specified small families are exhaustively enumerated.

## Publication disposition

The unchanged packet is suitable for a scoped partial publication with **unsolved, 5/5**, preserving the full arbitrary-addition/general-component gap. No author proof or result correction is required. Retain the source convention caveat, no-novelty qualification, and separation of exact structural subclasses from the original unrestricted request. Publication remains subject to the parent campaign's authorization gate.
