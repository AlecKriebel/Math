# Independent audit: periodic rational recurrences, problem 4700011

Audit date: 2026-10-07 UTC.

## Verdict

**ACCEPTED AS A PARTIAL CLASSIFICATION.** The frozen Turn 1 arguments are valid within their stated scope. The frozen Turn 2 arguments prove the complete classification at order six for arbitrary nonnegative real coefficients, under the primary source's common-global-period convention. All five excluded palindromic variable-support patterns, with and without a positive constant term, have valid exact infinite-order obstructions. No mathematical correction to either frozen manuscript is required by this audit.

The classification of all orders is **not solved** by these files. Priority or novelty is **not established**. In particular, the 2020 source's omission of order six does not establish that no subsequent order-six classification exists.

No source documents, dataset contents, or private coordination material are included in this report. No repository or queue changes are part of this audit.

## 1. Frozen evidence and reproducibility

The reviewed files are copied unchanged into `frozen/`:

| File | Bytes | SHA-256 |
|---|---:|---|
| `turn01_reduction.md` | 14019 | `212b908dda29ed72783e68063213532a918f3de10a4526f7b1e2ed5f3303533a` |
| `verify_turn01.py` | 2912 | `194e076c9a620d5562dff022d9b0761a8327bfb18c7228d122d2c42811824563` |
| `turn01_verification.json` | 1496 | `b8a1282aa3ed6bd49ee4e5b5b6f9c456dbd2c066f160c3c65964d3d3359312e7` |
| `turn02_order_six.md` | 16259 | `74190da2325dcaf03b209fc281f830c688ea2ba8d9fc9b0bd39cd3ac74a27f29` |
| `verify_turn02.py` | 5297 | `ed6069b288b99fd3d6d1af7c4a4a6c142212522335a9bf4b230c7798bad3be3a` |
| `turn02_verification.json` | 8826 | `361165903f459936c8b714b000c18936bb72ae821ab6dbf0ec98df78a650e3d4` |

Both supplied verifier scripts were executed in the separate `replay/` directory. Their output JSON files are byte-identical to the frozen authored JSON. The frozen files themselves were not executed in place or overwritten.

`checks/independent_checks.py` is an independent implementation. It does not import the author's verifier. It reads the frozen certificate claims, reconstructs the scalar tropical sequences and their linearized rows, derives the entire drift tangent map symbolically, and selects expanding-ray branches through exact algebraic comparisons. Its 22 named checks pass. The full output is `checks/independent_results.json`.

Reproduce from the audit directory:

```sh
python checks/independent_checks.py
python replay/verify_turn01.py
python replay/verify_turn02.py
cmp replay/turn01_verification.json frozen/turn01_verification.json
cmp replay/turn02_verification.json frozen/turn02_verification.json
```

The mathematical acceptance rests on the arguments below, supplemented by exact replay. It is not inferred from numerical testing, long finite orbits, or unexamined success flags.

## 2. Primary statement and scope

The exact v1 primary formulation was independently inspected at [Gasull, *Some open problems in low dimensional dynamical systems*, Section 2.8, equations (12)–(13), Problem 11](https://arxiv.org/html/2012.02524v1). It defines a single least period that works for every positive initial condition. The corresponding shift map therefore has finite order. Individual points may have smaller least periods. The manuscript's convention is correct.

The source states that the five displayed classical families, their positive rescalings, and index dilations are the known examples, and records classification at orders 1, 2, 3, 4, 5, 7, 9, and 11. This historical source check does not establish current novelty. The 2004 paper cited there was not independently inspected in full for this audit; no part of the accepted proof depends on importing an uninspected theorem from it.

## 3. Turn 1: structural and odd-order arguments

### Surjectivity reduction

Finite order makes the shift map bijective. For each fixed positive tail, surjectivity requires the first-coordinate fractional-linear function to cover the entire positive half-line. A nonconstant fractional-linear function is strictly monotone, so its endpoint limits must be zero and infinity in one order. Nonnegative coefficients then force either the increasing form with numerator proportional to the first coordinate and denominator independent of it, or the reciprocal form with numerator independent of the first coordinate and denominator proportional to it.

This reasoning includes vanishing constants, sparse supports, order one, and the possibility of proportional numerator and denominator. The latter cannot be surjective. A nonnegative affine form vanishing at a positive tail has every coefficient zero, so no hidden tail-dependent case survives.

### Increasing branch

When there is no variable denominator, periodicity forces the positive scalar multiplier to be one. With a variable denominator, a coefficient at most the constant denominator term gives a strict decrease after every order-length jump, contradicting periodicity. Otherwise there is a positive diagonal fixed point. Its companion characteristic polynomial has opposite signs at zero and one, giving an eigenvalue strictly between them. A finite-order derivative cannot have such an eigenvalue. The exclusion is complete.

### Palindromic coefficients

The positive diagonal fixed point exists for every allowed reciprocal branch. Its monic characteristic polynomial has constant term one. Finite order puts all its roots on the unit circle. Real coefficients make the multiset invariant under complex conjugation, which there equals inversion. The reciprocal polynomial is therefore the same monic polynomial, giving the asserted coefficient symmetry. Multiplicities do not invalidate this argument.

### Homogeneous rational ratios

When the constant vanishes, the normalized variable coefficients sum to one. Under the stated rational-ratio hypothesis they are rational. The root-of-unity spectrum makes them algebraic integers; hence they are integers. Nonnegativity and the sum then force exactly one nonzero coefficient. Palindromic symmetry places it at the middle index. The proof does not claim this for arbitrary irrational ratios.

### Odd two-cycle identity

Reflection of odd-order palindromic indices exchanges parity, giving equal positive odd and even coefficient sums. The positive two-cycle family is correctly parametrized by the displayed equation for its two values. Its sum varies over a nondegenerate real interval.

The Floquet two-by-two determinant expands to the asserted polynomial. A nonzero Floquet null vector produces a nonzero initial perturbation and a monodromy eigenvector, since both parities occur in the state. The polynomial's constant term is minus one, so zero roots are absent. It is sufficient that each polynomial root is a monodromy eigenvalue: no unsupported equality of multiplicities is needed.

Under finite global order every root lies in a fixed finite root-of-unity set. There are only finitely many degree-k monic polynomials with roots in that set, even with repetition. Continuous dependence on the two-cycle parameter therefore makes the polynomial constant. Differentiation gives the asserted identity `h C = a0 H` and the root-of-unity polynomial in Turn 1. As a further independent algebra check, the audit computes the monodromy characteristic polynomial for orders 3, 5, and 7 without imposing palindromic coefficients; the more general underlying identity passes.

If the constant vanishes, the resulting equality of a square and t times another nonzero square is impossible by orders of vanishing at zero. Thus the odd homogeneous exclusion requires no rationality assumption.

For rational variable-coefficient ratios, the even and odd blocks in the root-of-unity polynomial have disjoint degrees. Integer-coefficient reasoning therefore forces one nonzero coefficient in each parity block. Comparing the signed monomials in the resulting identity gives the third-order classical dilation and the square relation for the constant. This also fully covers order three, where palindromic symmetry makes the ratio hypothesis automatic.

### Periods

All five base rational identities and their least global periods are checked symbolically by the authored verifier. The index-dilation argument is valid: a shift between distinct residue classes cannot identify arbitrary independent data; shifts preserving classes reduce to the base order. Independent exact positive-data witnesses also realize the stated order-six periods.

## 4. Tropical finite-order implication

The implication holds for **arbitrary fixed positive real coefficient values**, including irrational and transcendental values. It depends only on support.

An explicit bound strengthens the manuscript's already sufficient compact-uniform argument. Let m be the smallest positive active coefficient and B their sum, including the constant only when positive. The logarithm of the active exponential sum differs from R times its maximal exponent by a number between `log m` and `log B`. Thus the logarithmic conjugate differs uniformly from the tropical map by at most `C/R`, for a constant depending only on the given coefficients.

Both maps have Lipschitz constant at most two in the maximum norm: the shift coordinates have constant one, and the last coordinate is a maximum or log-sum-exp minus the first coordinate. For any fixed iterate p, the iterate error is at most `(2^p-1) C/R`. Passing a finite-order identity to the limit is therefore legitimate. No interchange of an unbounded number of iterates with a limit occurs, and no equality between least rational and tropical periods is assumed.

## 5. Finite certificates really prove infinite-order obstructions

### Tangent and derivative transfer

At a strict tropical cycle, all finitely many maxima stay strict in a neighborhood. The return derivative is therefore a genuine linear derivative at a fixed point. If the tropical map had common order p, the return derivative would satisfy `M^p=I`.

At a tied cycle, the directional return is a positively homogeneous piecewise-linear map. Along any fixed direction the expansion is exact for sufficiently small positive displacement. For any fixed finite number of tangent iterations, a common sufficiently small displacement can be chosen. Hence a finite-order identity for the original map induces the same identity for the tangent return. Unbounded tangent drift or an expanding eigenray is a valid obstruction even though it does not directly assert an unbounded actual orbit through the base point.

### Support {b}, with and without the constant

The audit independently advances the base point through all five steps and obtains precisely the asserted tie sets. It derives the complete symbolic directional return from those sets, rather than assuming the supplied return formula. It then verifies the three-return drift and symbolic translation equivariance in the two inactive coordinates. Induction yields a nonzero linear drift for arbitrarily many returns. Both constant statuses pass.

### Supports {b,c} and {c,d}, with and without the constant

The audit works in the exact field defined by `alpha^3-alpha^2-1=0`, with the real root in `(1,3/2)`. All ordering decisions use rational interval arithmetic. It computes the base tie sets, selects actual maximizing tangent entries, and obtains exactly `alpha` times the listed nonzero vector in each case. It does not choose a matrix branch merely because it has a desirable eigenvalue.

The zero tangent gap for the {b,c} ray is harmless: tied entries give the same scalar maximum. Base maxima are one, so the constant is strictly inactive throughout both four-step base cycles. Positive homogeneity yields unbounded eigenrays for both constant statuses.

### Support {b,d}

Both strict certificates replay exactly, with minimum winning margin one, including the full winning-index list and return matrix.

- No constant: the 99-step return matrix has characteristic polynomial `(t-1)^3 (t^3-4t^2+3t-1)`. The cubic changes sign between 3 and 4, giving an eigenvalue outside the unit circle.
- Constant present: the 47-step return matrix has characteristic polynomial `(t-1)^3 (t^3+7t-1)`. The cubic changes sign between zero and one, giving an eigenvalue strictly inside the unit circle.

Either proves infinite matrix order for every possible proposed global period.

### Support {b,c,d}

Both 65-step strict certificates replay exactly, again with minimum winning margin one. The two claimed rank-one decompositions are independently verified. In each case `M=I+N`, `N` is nonzero, and `N^2=0`. Therefore `M^n=I+nN` for every positive integer n, and the matrix has infinite order.

The characteristic polynomial alone would not suffice here: all eigenvalues equal one. The nonzero nilpotent part is explicitly checked.

### Adversarial controls

The independent checker rejects a changed winning index, an altered return-matrix entry, a truncated proposed return, and removal of the active constant from the constant-present {b,d} certificate. It also rejects the negative of the valid {b,c} eigenray as an expanding eigenray, because the actual maximizing branches change.

Two exact matrix controls guard the logical distinction: a nonidentity matrix of order four is not accepted as an infinite-order obstruction, while a nonidentity unipotent matrix illustrates that unit-circle eigenvalues are insufficient for finite order. The audit does not treat any long observed orbit as an infinite-order certificate.

## 6. Exhaustiveness and surviving coefficients

There are exactly eight subsets of `{b,c,d}`. The five excluded subsets and the three surviving subsets are a disjoint exhaustive partition. Each excluded subset is eliminated for both possible constant statuses. Thus there is no omitted palindromic support mask or coefficient-ratio assumption.

The survivors are:

1. Empty variable support: a positive constant is required and gives the reciprocal dilation.
2. Only d positive: rescaling gives the second-order Lyness parameter `A=a0/d^2`. Its fifth iterate has a genuine rational extension to the positive boundary, with image `(0,Ay)`. Both cancelled denominators at that boundary are `(A+y)^2>0`; the audit rederives this. For `A>0`, all finitely many boundary iterates remain valid, so finite order gives `A^p=1`, hence `A=1`. The separately handled case `A=0` is globally periodic. Thus exactly `a0=0` and `a0=d^2` survive.
3. Only c positive: the two independent order-three subsequences have equal variable coefficients. Turn 1 therefore applies without any additional rationality assumption and forces `a0=c^2`.

Together with the increasing branch, this gives exactly the five order-six formulas in the frozen theorem, with least common periods 6, 12, 18, 15, and 16. Their arbitrary positive scales are unrestricted.

## 7. Acceptance boundaries

Accepted:

- Turn 1 structural reductions and the stated rational-ratio and odd homogeneous partial classifications.
- Complete order-six classification over arbitrary nonnegative real coefficients.
- The stated index-dilation corollary for higher-order recurrences whose entire numerator variable support lies on the corresponding sublattice.

Not established:

- Full classification for arbitrary order and support.
- Irrational-ratio classifications outside the portions expressly proved.
- Priority, novelty, or absence of later related literature.

The two frozen manuscripts require no mathematical correction for these accepted claims. This audit is an authored mathematical review with exact reproducibility checks, not a formal proof-assistant verification.
