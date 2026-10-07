# Independent audit of Turns 3 and 4: periodic rational recurrences

Problem 4700011, Gasull Problem 11. Audit date: 2026-10-07 UTC.

## Verdict and exact scope

**Turn 3: ACCEPTED as a finite odd-order reduction and exact order-13/order-15 classification.** The finite spectral-factor list includes arbitrary real coefficient ratios after positive scalar conjugacy. Both arithmetic filters are necessary, and the integrality equivalence is correct. The finite derivative-order bound and rational-identity decision procedure are valid mathematical termination statements, not practical complexity estimates. The complete classifications of orders 13 and 15 are supported by exhaustive exact certificates.

**Turn 4: ACCEPTED as an all-order sparse-support classification and collection of necessary obstructions.** The classification for at most two active variable numerator terms, the rational-ratio even-order parity-weight restriction, the normalized algebraic-unit condition, quadratic nonresonance, cubic divisibility, and weighted-variance consequence are valid within their stated hypotheses. No additional rationality assumption is needed for the sparse-support theorem, because reflection symmetry itself makes the two active coefficients equal.

**No mathematical correction to either frozen manuscript is required.** The original arbitrary-order classification remains unresolved. Neither this audit nor the manuscripts establish novelty, priority, or absence of later literature. The arithmetic and cubic restrictions are not accepted as sufficient conditions for global periodicity.

This is an independently authored mathematical audit with exact computer-algebra checks, not a formal proof-assistant verification. It makes no repository, queue, or publication changes.

## 1. Scope, fixed-period convention, and dependencies

The audit inspected the primary statement in [Gasull, *Some open problems in low dimensional dynamical systems*, Section 2.8, equations (12)–(13), Problem 11](https://arxiv.org/html/2012.02524v1). Its periodicity convention requires one common period for all positive initial data. It does not require every individual orbit to have that least period. Thus finite order of the shift map is the correct hypothesis throughout both turns.

The accepted Turn 1 and Turn 2 results are dependencies, rather than being silently reproved by these new files. Their full prior acceptance report was read. The relevant structural, two-cycle, rational-ratio, dilation, and order-two boundary arguments were also inspected in their manuscripts. In particular, the two-variable boundary-return argument in Turn 2 applies to an arbitrary order-two subsystem, independent of the surrounding order-six application.

The independent check of the source's historical list is not a literature-completeness search. No novelty conclusion is drawn from a classification being absent from that list.

## 2. Frozen inputs and reproduction

All reviewed inputs were copied unchanged into `frozen/`. Their byte counts and SHA-256 hashes match the author manifests:

| File | Bytes | SHA-256 |
|---|---:|---|
| `turn03_odd_spectral_factors.md` | 15617 | `dd0ece100266aef905ea43664a2f3de7cab16e16ef881b18776ef04a4c9a0d09` |
| `verify_turn03.py` | 4226 | `2fdce9df6e860bea6549d2e80a0ef5794a96b90ca038c0146ba77febfbd1e18e` |
| `turn03_verification.json` | 57067 | `639926b37f535c411d9c4817b2d1d1beb840b7c064c5ccc1707a66b977ffb818` |
| `turn04_uniform_sparse_and_resonance.md` | 16879 | `79f86832b5c79fd0ad0f9bf74f29d4385ccacc9f376237ac6fc4885e5b450148` |
| `verify_turn04.py` | 3795 | `587fb8783770ca9120a0a9787b582eece3565079ec603d42b622a63e2c3a6e20` |
| `turn04_verification.json` | 3060 | `aa565d7add843c7e41e5416a12b4f8c94903cf58987fe23841ba205802d0e1c5` |

Both supplied verifiers were copied to `replay/` and executed there. Their resulting JSON files are byte-identical to the frozen authored JSON. Original files were neither executed in place nor edited.

`checks/independent_checks.py` does not import or execute either author's verifier. It reconstructs factors with SymPy polynomial quotient arithmetic, computes norms by resultants rather than multiplication matrices, extracts monic minimal polynomials, and counts real roots using an explicitly implemented rational Sturm remainder sequence. It also independently expands scalar jets to recover the cubic source terms and uses a Groebner basis of all remainder coefficients for the low-order cubic ideals.

Reproduce from the audit directory:

```sh
python checks/independent_checks.py
python replay/verify_turn03.py
python replay/verify_turn04.py
cmp replay/turn03_verification.json frozen/turn03_verification.json
cmp replay/turn04_verification.json frozen/turn04_verification.json
```

All 49 named independent checks pass. The complete per-factor results and controls are in `checks/independent_results.json`. Finite consistency checks are supplementary; none is extrapolated into an all-order theorem.

## 3. Turn 3: spectral factorization and normalization

### 3.1 Identity and exhaustive root choices

The two-cycle identity is used only after excluding the homogeneous odd-order case and the zero-variable-support reciprocal case. Thus all divisions by the constant coefficient and the sum of variable coefficients are legitimate.

Writing the even and odd parts of the proposed factor as `1+r E(z²)` and `z^k+r z O(z²)` gives exactly the claimed cancellation when `r=2h/a0`. This proves `A(z)A(-z)=1-z^(2k)` with the correct leading sign for odd k. Its roots are simple, because the roots of the right-hand side are simple in characteristic zero.

Nonnegative coefficients give `A(1)>0`, so the real root in the factor is −1 rather than +1. The remaining roots split into conjugation-and-negation orbits of size four. None has size two: that would require a root ±i of an order dividing 2k, impossible when k is odd. Each orbit contributes exactly one conjugate pair, giving precisely the two signed quadratic choices displayed in the manuscript. There are `(k−1)/2` such orbits. Distinct choices cannot coincide as monic polynomials, because they select distinct simple root sets.

The resulting list is deliberately a superset of periodic candidates. Negative coefficients are not admitted into the original family. A factor with zero interior sum can only be admissible when every nonnegative interior coefficient vanishes. That case is already the constant-numerator family. A zero-sum factor with negative coefficients can also occur and is correctly discarded, without being misidentified as a positive recurrence.

### 3.2 Unique normalized coefficients

The positive diagonal fixed point satisfies `q²=a0+S q`, with `S=2h`. Rescaling by q gives `c0+sum(cj)=1`. The equations `L=S²/a0` and `lambda=a0/(S q)` imply `lambda(lambda+1)=1/L`, so its positive root and all normalized coefficients are uniquely determined by the factor. In particular `c0=lambda/(lambda+1)>0`.

This removes the otherwise arbitrary original coefficient scale, including a transcendental scale. It does not assume rational coefficient ratios. Conversely, the formulas construct positive rational maps from the retained factors; they do not assert periodicity. The bound of at most `2^((k−1)/2)−1` nonconstant normalized patterns is therefore sound.

## 4. Turn 3: arithmetic filters

### 4.1 Field and total-realness

For odd `k>=3`, the maximal real subfield of `Q(zeta_(2k))` has degree `phi(k)/2`, since `phi(2k)=phi(k)`. Each factor coefficient is an algebraic integer in this field.

Finite order at the positive fixed point places all normalized variable coefficients in a real cyclotomic field, so they are both algebraic integers and totally real. This is stronger than merely having real values in one embedding. A nonzero factor coefficient allows `lambda=cj/ellj`; the compositum of totally real fields is totally real. Every embedding of the factor field extends to that compositum and therefore sends lambda to a real value.

Every conjugate of `A(1)` is positive. Indeed its factored expression consists of factors `2+2 epsilon cos(theta)`, and no relevant conjugate cosine equals ±1: multiplication by a unit modulo 2k cannot send an index strictly between zero and k to zero or k. If a conjugate of `A(1)` lay strictly between zero and two, the corresponding quadratic for lambda would have negative discriminant. Equality with two is impossible for a nonzero field element `L=A(1)−2`. Hence all conjugates must exceed two.

### 4.2 Integrality

The relation `cj(cj+ellj)=ellj²/L` proves necessity immediately. Conversely, if the right side is integral, `cj` is integral over the algebraic integers because it solves a monic quadratic with integral coefficients. Transitivity of integrality proves the claimed equivalence. Zero `ellj` is harmless: both associated values vanish.

For an algebraic element in a number field, the rational multiplication characteristic polynomial is a power of its monic minimal polynomial. Its coefficients are all integers exactly when the element is an algebraic integer. Enlarging the field from the real cyclotomic field to the full cyclotomic field adds multiplicities but does not change integrality or the set of conjugate values. The author's multiplication-matrix implementation is therefore mathematically sound.

The independent audit instead uses the resultant norm, removes repeated factors, and checks the monic minimal polynomial. It verifies the total number of real conjugates and exact positivity as well as the rejection interval. No floating-point approximation or chosen approximate embedding enters either method.

## 5. Turn 3: finite period bound and decision procedure

The averaging map in Lemma 6 is defined near the fixed point, has derivative the identity, and intertwines the map with its derivative. The inverse-function theorem applies. If a power of the derivative is the identity, the same power of the original map is the identity locally; the rational-function identity theorem then extends it globally wherever the iterates are defined. All positive iterates exist in this family. This establishes equality of the finite orders, not just divisibility in one direction.

The assumption of finite order is essential. A nonlinear rational map tangent to the identity need not be the identity if it has infinite order; the independent checker includes such a control. The lemma is not being used to infer periodicity from unit-circle eigenvalues.

The coefficient field has degree at most `phi(k)`, including the quadratic extension for lambda. An eigenvalue of the degree-k characteristic polynomial consequently has degree at most `Dk=k phi(k)` over Q. A primitive n-th root of unity has degree `phi(n)`. The prime-power product proof of `phi(n)^2/n>=1/2` is valid, including `n=1` and the exceptional small factor from the prime two. Thus every eigenvalue order is at most `Bk=2 Dk²`.

A finite-order derivative is diagonalizable in characteristic zero, so the least common multiple of its eigenvalue orders is its matrix order. This justifies the passage from the eigenvalue bounds to the stated universal exponent `Nk=lcm(1,...,Bk)`. Lemma 6 gives the same exponent for the rational map.

For each fixed odd k, exact real-algebraic sign determination, construction of the coefficient field, finitely many rational-function compositions, and equality testing in that field are all terminating procedures. The huge size of Nk does not invalidate termination. A map that passes the rational identity test is genuinely globally periodic on the positive domain; a periodic map cannot be missed by the bound. Identity and reciprocal families are added separately. No assumed numerical period cap is used.

## 6. Turn 3: complete exact enumeration at orders 13 and 15

The independent implementation enumerates all 64 and 128 sign patterns, verifies that no two factor polynomials coincide, and verifies every coefficient of `A(z)A(-z)=1-z^(2k)`. It reconstructs every authored rejection polynomial independently, matches the claimed first failing index for integrality rejections, and confirms that all rejection and survivor cases exhaust the sign choices.

| Order | Patterns | Zero interior sum | Total-realness failures | Integrality failures | Negative final factors | Nonnegative survivors |
|---:|---:|---:|---:|---:|---:|---:|
| 13 | 64 | 1 | 62 | 1 | 0 | 0 |
| 15 | 128 | 2 | 114 | 10 | 1 | 1 |

At order 13, the final integrality rejection is the all-two interior factor, with quotient `4/24=1/6`. At order 15, the sole nonnegative survivor is `1+2z^5+2z^10+z^15`. Its normalized coefficients and constant give exactly the already accepted eight-period order-three Lyness family dilated by five. The other arithmetic survivor has negative coefficients and is correctly rejected.

The absence of nonconstant survivors at order 13 and identification of the order-15 survivor establish the complete classifications claimed in the manuscript. The least common global periods are 13 and 26 at order 13, and 15, 30, and 40 at order 15, by the accepted base identities and dilation minimality argument.

The checker rejects an altered rejection polynomial, deletion of a sign pattern, and mutation of a factor coefficient. It distinguishes nonintegral rational numbers from integral irrational cyclotomic elements. It also retains the three important logical controls: integrality without total-realness, total-realness without integrality, and both arithmetic filters without original coefficient nonnegativity.

## 7. Turn 4: parity-weight theorem and sparse classification

### 7.1 Totally real algebraic-integer argument

The companion matrix is cyclic, so its minimal polynomial equals its characteristic polynomial. Finite order makes its minimal polynomial squarefree; thus the spectrum is simple. Embeddings of the coefficient field extend to a cyclotomic splitting field, and the conjugated polynomial still has root-of-unity roots and real coefficients.

Bézout's identity for the relatively prime integer weights makes tau an algebraic integer. It lies in the same totally real field. For even k, the original polynomial takes strictly positive values at ±1, since both are at least `2−s>=1`. No embedding can turn either nonzero algebraic value into zero. Pairing conjugate nonreal unit roots in the even-degree polynomial gives strictly positive values at ±1 in every embedding.

The resulting bounds `−2/D < sigma(tau) < 2/N` are correct when `D=O−E>0`. With `D>=1` and `N>=2`, all conjugates lie in `[-2,2]`. The supplied Kronecker proof is complete: the power-conjugate polynomials are integral, have bounded integer coefficients, and thus finitely many possible roots; repetition of powers forces a root of unity.

Writing tau as a root of unity plus its inverse now excludes every positive tau at most one half. For primitive order `n>=7`, the conjugate `2cos(2pi/n)` exceeds one, contradicting the upper embedding bound. The positive values for `n<=6` are 2, 1, and `(sqrt(5)−1)/2`, all greater than one half. This proves the parity inequality uniformly in the order. No finite check of small orders substitutes for the argument.

### 7.2 Exhaustive sparse cases and degeneracies

Reflection symmetry makes an empty support, a midpoint singleton, or a reflected pair the only possible supports of size at most two. The empty support requires a positive constant and gives the reciprocal family. A singleton can only occur in even order at its midpoint; the previously accepted order-two boundary argument covers both zero and positive constants and forces exactly the six- or five-period base family.

For a distinct reflected pair, coefficients are equal. Dividing indices by `g=gcd(k,j)` gives a primitive subsystem of order K and coprime lag r. The g-th power of the original shift acts on independent residue-class systems, so finite order of the original shift forces finite order of each subsystem. If K is even, coprimality makes both active lags odd, and the parity theorem excludes the pair. If K is odd, Turn 1's rational-ratio theorem forces third-points, and coprimality then forces K=3. This yields exactly the eight-period classical dilation with constant `b²`.

This covers every order, both constant statuses, arbitrary positive coefficient scale, and all support degeneracies. The equal-full-numerator corollary follows from the parity obstruction in even order and the odd rational-ratio theorem in odd order. The claims about at least three active terms for a new example, and at least four in odd order, follow directly.

## 8. Turn 4: negative fixed point and quadratic nonresonance

For positive normalized constant c0, the second diagonal fixed point is `r=−c0`, because the fixed-point quadratic factors as `(r−1)(r+c0)`. Although outside the positive orthant, it is a valid point at which to differentiate the rational finite-order identity. Every iterate remains at this point and every denominator is nonzero there. No continuation through a pole is required.

The last derivative row there is `(-1,−c1/c0,...,−c_(k−1)/c0)`, giving precisely the stated characteristic polynomial. Both `cj` and `cj/c0` are therefore totally real algebraic integers. The identities for c0 and its reciprocal make c0 an algebraic unit. The theorem excludes c0=0 explicitly; empty variable support has c0=1 and causes no difficulty.

For quadratic resonance, a unit root zeta has its k-th power in the closed arc from `2pi/3` to `4pi/3`, because `|1+zeta^k|<=s<=1`. The product of two points of this arc lies back in the arc only when both inputs are the same endpoint. Equality requires s=1 and equality in the triangle inequality for every active coefficient. Their squared phase then contradicts the root equation for the alleged product eigenvalue. This handles repeated choices of the same eigenvalue and the homogeneous boundary `s=1`. If s=0, the problematic equality case is unavailable. Thus all quadratic denominators used later really are nonzero.

## 9. Turn 4: cubic obstruction and variance

The averaging conjugacy is analytic because the rational map is analytic near its fixed point. Its inverse can be complexified near zero. On the two-dimensional complex eigenspace parameterized by independent amplitudes a and b for a nonreal eigenvalue and its inverse, the first scalar coordinate has first-order terms `a zeta^n+b zeta^(−n)`. Companion eigenvectors have nonzero first coordinate and can be normalized as stated.

Expanding the exact scalar recurrence gives the linear recurrence operator applied to the scalar perturbation equal to `−u_n u_(n+k)`. A degree-two monomial has the frequency obtained by multiplying its eigenvalues. Quadratic nonresonance makes the coefficients unique and gives exactly the stated U and V.

The coefficient of `a²b` at degree three has frequency zeta, so its linear recurrence contribution is zero. Multiplying the first- and second-degree scalar jets independently gives the cubic source `U(t²+t^(−1))+V(1+t)`, with `t=zeta^k`. Substitution and clearing the nonzero denominators produces exactly G. Potential coincidences of other cubic frequencies do not affect this argument: a and b are independent formal coordinates and the selected monomial coefficient must vanish separately.

The real root +1 is excluded by `P(1)>=1`. In even order −1 is also excluded; in odd order direct substitution gives `G(−1)=0`. Simplicity of every spectral root, established from the companion finite-order matrix, then turns pointwise vanishing at roots into divisibility by P. No repeated-root gap remains.

For the variance consequence, write `P(zeta²)=t(2v+s−2M2)`, where `M2=sum cj Xj²`. Dividing G by its permitted nonzero factors gives `(2−s)(2v−1)+2v(2v+s−2M2)=0`, yielding exactly the manuscript's second-moment formula. Subtracting the squared weighted mean gives its variance identity. The range `−1<v<=−1/2`, together with `s>0`, makes the displayed prefactor positive. Hence the inequality follows. The excluded case `t=−1` is not silently divided through, and the conclusion never asserts that the variance is zero.

The complete low-order cubic remainder ideals agree with the author's gcd formulas. The extra cubic root at order three genuinely passes all remainder equations and has a unit-circle spectrum in the selected real embedding, while an exact bad conjugate forces a spectrum off the unit circle. This validates the failed-sufficiency example, rather than treating it as a periodic map. Classical-family controls include constant-only, homogeneous, inhomogeneous, odd-order, and nontrivial-dilation cases.

## 10. Acceptance boundaries

Accepted without correction:

- The complete frozen Turn 3 reduction, arithmetic filters, finite exponent/decision theorem, and orders 13 and 15 classifications.
- The complete frozen Turn 4 sparse-support classification and all stated necessary restrictions, including cubic divisibility and its variance consequence.
- The supplied exact rejection and algebraic consistency certificates, with independent reconstructions and adversarial controls.

Not established:

- Classification of arbitrary larger supports or all arbitrary even orders.
- Sufficiency of the arithmetic filters, algebraic-unit condition, unit-circle spectrum, cubic identity, or variance inequality.
- Any claim that a bounded search settles an all-order question.
- Novelty, priority, or literature completeness.

The original full problem remains open within this work. No patch is needed; the `patches/` directory is intentionally empty.
