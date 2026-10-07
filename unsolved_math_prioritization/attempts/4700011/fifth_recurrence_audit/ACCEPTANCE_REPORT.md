# Independent audit of Turn 5: periodic rational recurrences

Problem 4700011, Gasull Problem 11. Audit date: 2026-10-07 UTC.

## Verdict

**ACCEPTED as a uniform mixed-support exclusion and arithmetic/finite-decision reduction, within the stated hypotheses.** No mathematical correction to the frozen Turn 5 manuscript is required.

The mixed-support theorem applies to arbitrary positive real values of its active coefficients, with either zero or positive constant. Its contracting-ray case is as conclusive as its expanding-ray case. The total-positivity, gap, central-third, large-gap parameter-list, and rationally scaled constant results are valid. The finite decision procedure is a genuine per-order termination result for the specified rationally scaled subclass; its computational practicality is not asserted.

**The full arbitrary-order classification remains unresolved by this work.** Arithmetic bounds, cyclotomic norm tests, and root-of-unity spectra are not accepted as sufficient for nonlinear periodicity. No novelty, priority, or literature-completeness claim is established.

This is an independently authored mathematical review with exact computational checks, not a formal proof-assistant verification. It makes no publication, repository, or queue changes.

## 1. Frozen bytes and reproducibility

Acceptance applies only to these exact bytes, copied unchanged into `frozen/`:

| File | Bytes | SHA-256 |
|---|---:|---|
| `turn05_mixed_lags_and_arithmetic.md` | 17577 | `7db70a64a47e64beb165210571248aee9c641599e144940bee7d6b0930239840` |
| `verify_turn05.py` | 4511 | `5a07bd42cc090030c731a4960115c773e60a9b477c8ef5c6f1a96ae9f6410c96` |
| `turn05_verification.json` | 4920 | `334a06dd3545e4680659cc77d38b5eeed76ec4668f7cc8c2ce471831e9d19765` |

The author manifest was also copied. All three pins were checked before review and again at completion. The supplied verifier was executed only in `replay/`; its generated JSON is byte-identical to the frozen JSON. Original authored files were not modified.

`checks/independent_checks.py` neither imports nor executes the author's verifier. Its generic tropical-state simulator discovers each base winning set and compares the actual tangent values using exact rational interval arithmetic for the selected algebraic root. It checks 502 distinct support patterns in orders 6, 10, 14, 18, 22, 26, 30, and 34, both constant statuses, and three complete tangent returns for every case. Its ten named check groups all pass.

Additional independent checks reject altered proposed eigenrays, do not falsely exclude midpoint-only classical supports, recover the norm polynomial by a resultant, recover Newton traces from companion matrices, and check classical cyclotomic orders and the nonperiodic order-eight control. Finite samples supplement the uniform proof; none is extrapolated into an all-order classification.

Reproduce from this audit directory:

```sh
python checks/independent_checks.py
python replay/verify_turn05.py
cmp replay/turn05_verification.json frozen/turn05_verification.json
```

The detailed results are `checks/independent_results.json`; the inventory is `audit_manifest.json`.

## 2. Problem convention and accepted dependencies

The primary statement was independently inspected in [Gasull, *Some open problems in low dimensional dynamical systems*, Section 2.8, equations (12)–(13), Problem 11](https://arxiv.org/html/2012.02524v1). Its convention is a common global period on the positive orthant. Thus the relevant shift map must satisfy one finite-order identity for all positive initial states. It is not required that every individual orbit have the same least period.

The two prior independent acceptance reports were read, together with the relevant structural, homogeneous rational-ratio, tropicalization, tangent-return, finite-order linearization, sparse-support, algebraic-unit, and Kronecker arguments. Their accepted claims are dependencies, not new claims silently reproved here. All twelve corresponding authored inputs from Turns 1–4 remain byte-identical to their prior frozen copies.

The historical source and prior partial results do not settle current novelty. No result in the present acceptance requires importing an uninspected proof from the 2004 classification article or a quiver classification.

## 3. Theorem 1: uniform mixed-support tropical obstruction

### 3.1 Exhaustive support encoding and the base orbit

Let `k=4L+2`, `L>=1`, and midpoint `m=2L+1`. Every reflected pair of even lags is uniquely of the form

`{4a, 4(L-a)+2}`, with `1<=a<=L`.

Consequently a nonempty reflection-closed set E is exactly a nonempty subset of these L pairs. With `A=max{a:4a in E}`, its smallest lag congruent to two modulo four is `4(L-A)+2`. No extra support pattern within the theorem's hypothesis is omitted by this parameterization. Equal reflected coefficient magnitudes are unnecessary for this support-only obstruction.

For the scalar base sequence repeating `0,0,1,1`, each reflected pair supplies a coordinate of value one at every phase. The maximum is therefore exactly one. Since k is two modulo four, the recurrence gives `z_(n+k)=1-z_n`, exactly the chosen base sequence. The k-dimensional state returns after four shifts.

A present constant contributes exponent zero, strictly below the maximum one. Thus it never participates in the directional maximum, and both constant statuses have the same tangent map.

### 3.2 Actual tangent branches and both multiplier regimes

The proposed sequence is

`w_(4t)=w_(4t+2)=0`, `w_(4t+1)=U lambda^t`, and `w_(4t+3)=-lambda^t`.

At either even time the base-winning even-lag coordinates have tangent value zero. A base-winning midpoint, when present, has a negative tangent value. Therefore the tangent maximum is zero, as required by the zero even coordinates.

If L is odd, the midpoint is three modulo four. The equation

`lambda^(2L+1)-lambda^(2L-A+1)-1=0`

has a unique root lambda greater than one: equivalently, `lambda^(2L-A+1)(lambda^A-1)=1`, with strictly increasing left side on `(1,infinity)`. With `U=lambda^L-lambda^(L-A)>0`, the phase-one winning negative tangent is `-lambda^(L-A)`; the midpoint is below the base maximum at that phase. This gives `-lambda^L=-lambda^(L-A)-U`. At phase three the midpoint is a base winner with zero tangent and dominates the negative even-lag tangents. The remaining equation is `U lambda^(L+1)=1`, precisely the selected polynomial identity.

If L is even, the midpoint is one modulo four. The equation

`lambda^(2L+1)+lambda^A-1=0`

has a unique root in `(0,1)` by strict monotonicity. With `U=lambda^L`, the phase-one midpoint contributes tangent maximum zero, giving `-lambda^L=-U`. At phase three the midpoint is not a base winner. Because lambda is less than one, the largest even-lag tangent is `-lambda^A`, yielding `U lambda^(L+1)=1-lambda^A`.

These are comparisons on the actual tangent maximum, not arbitrary selections of a desirable matrix branch. The nonzero initial tangent vector has fourth coordinate minus one. Its four-step return is exactly lambda times itself. The relation for all subsequent phases follows by positive scaling, since `w_(n+4)=lambda w_n` and the base sequence is four-periodic.

### 3.3 Why contraction also proves infinite order

The directional return is positively homogeneous. Therefore its p-th iterate sends the ray vector to `lambda^p w`. With lambda positive and unequal to one, this differs from w for every positive integer p, whether the ray expands or contracts. An unbounded orbit is not needed in the contracting case.

The accepted tropicalization lemma passes a rational finite-order identity to the tropical map for any fixed positive active real coefficients. The accepted tangent-return lemma passes that identity to the directional return at its fixed base point, even when the maximum is tied. Thus the constructed ray contradicts finite order of the original recurrence.

The index-dilation corollary is valid: a suitable power of the dilated shift acts on independent residue-class systems, so finite order would force finite order of each original subsystem. The L=A=1 example correctly reproduces the previously accepted order-six support `{2,3,4}`. Midpoint-only supports are excluded from the theorem by the essential nonempty-E hypothesis and are retained by the independent control.

## 4. Lemma 2: total positivity of the normalized constant

For `c0>0`, the prior algebraic-unit theorem supplies both finite-order spectra

`P_+(z)=z^k-sum(cj z^j)+1` and `P_-(z)=z^k+sum((cj/c0) z^j)+1`.

Their coefficients lie in a totally real cyclotomic field. Every embedding of a coefficient field extends to an embedding of a splitting field and takes roots of unity to roots of unity. Consequently each conjugated polynomial still has real coefficients and unit-modulus roots.

At one, neither polynomial vanishes: the original values are `1+c0` and `1+1/c0`, and embeddings cannot send a nonzero algebraic number to zero. For every real conjugate polynomial, nonreal roots pair to contribute positive factors at one, while any root minus one contributes two. Hence both values are strictly positive in every embedding.

Writing `u=sigma(c0)`, the resulting inequalities are `1+u>0` and `1+1/u>0`. If u were negative, the former would force `u>-1` and the latter `u<-1`. Zero is excluded by the unit property. Thus every conjugate is strictly positive.

This also handles the empty-variable-support case `c0=1`. No illegitimate division by a possibly zero conjugate occurs.

## 5. Theorem 3 and Corollary 4: normalization, gap, and central-third supports

### 5.1 The scalar rescaling is correct

For primitive nonnegative integer weights `mj` and original coefficients `aj=b mj`, the substitution `x=b u` gives constant `A=a0/b²` and variable coefficients mj. The positive fixed point rho satisfies `rho²=N rho+A`. Therefore

`tau=1/rho`, `c0=A/rho²=1-N tau`, `d=tau/c0=rho/A`, and `M=1/A=tau d`.

It follows exactly that `d-tau=N M`, with no missing square or factor of b. The arithmetic statements require `A>0` and nonempty variable support. Their excluded homogeneous and empty-support cases are handled separately by the earlier classification.

### 5.2 Integrality and all embeddings

The two spectral coefficient lists contain `mj tau` and `mj d`, up to the harmless characteristic-polynomial signs. Bézout's identity for the primitive weights expresses tau and d as integer linear combinations of these algebraic integers. Both are therefore totally real algebraic integers.

For any embedding, total positivity of c0 gives `sigma(d)=sigma(tau)/sigma(c0)` with the same nonzero sign as `sigma(tau)`. Thus `sigma(M)=sigma(tau)^2/sigma(c0)>0`. This proves total positivity and integrality of M, even when A was initially an arbitrary positive real number. Considering embeddings of a common coefficient field is legitimate; every embedding of the smaller field generated by M extends to that field.

### 5.3 Newton trace and the strict bound

Reflection symmetry makes r, the least active lag, also the distance of the first nonzero coefficient below the leading term. Newton's identities give the r-th power sums `r m_r tau` and `-r m_r d`. In each conjugate spectrum these are sums of k unit-modulus numbers. Hence the absolute values of both tau and d are at most `k/(r m_r)`.

The identity `sigma(d)-sigma(tau)=N sigma(M)>0` combines with their common nonzero sign to give a strict inequality:

`N sigma(M) < max(|sigma(d)|,|sigma(tau)|) <= k/(r m_r)`.

The strictness is important. It proves `0<sigma(M)<B=k/(r m_r N)`. If B were at most one, the positive integer norm of nonzero integral M would be strictly less than one. Thus `r m_r N<k`, equivalent to the displayed integer bound `<=k-1`.

For B at most two, every conjugate of the integral number M-1 lies strictly between minus one and one. If nonzero, its absolute integer norm would be less than one. Therefore M equals one, including the endpoint B=2.

For central-third supports, three or more active terms imply `N>=3`, `m_r>=1`, and `r>=k/3`, contradicting the bound. At most two terms are left and the accepted sparse-support theorem applies. The homogeneous rational-ratio case is separately covered, so the corollary omits no constant status.

## 6. Corollary 5: finite list when the gap bound is below four

When B is less than four, all conjugates of M-2 lie strictly between minus two and two. The accepted Kronecker lemma applies and gives `M=2+zeta+zeta^(-1)`. The root of unity may be taken primitive of its order n. Orders one and two give four and zero and are impossible.

Among the primitive n-th root conjugates, the largest real value is `2+2 cos(2pi/n)`, so it too must be strictly below B. The elementary estimate `cos t>=1-t²/2` yields the stated bound `n²<4pi²/(4-B)`. Thus only finitely many orders and conjugate values need inspection. When the upper bound admits none, the retained list is empty; this is consistent rather than exceptional.

This is a necessary finite parameter list for each such weight pattern, not a periodicity assertion about each listed parameter. The infinite sequence at B=4 correctly illustrates why these positivity and gap tests alone need not give a finite list at or above that boundary.

## 7. Theorem 6 and the finite per-order procedure

### 7.1 Rationally scaled constant and the norm polynomial

With rational A, the totally positive integral number `M=1/A` is a positive integer. The fixed-point equation becomes `tau²+NM tau-M=0`.

Tau cannot be rational: it is a positive algebraic integer strictly below `1/N<=1`. Therefore this quadratic is its minimal polynomial, and its conjugate is `tau'=-NM-tau=-d`. The negative-spectrum r-th trace and `d>NM` give `r m_r N M<k`; the integer form is exactly `r m_r N M<=k-1`.

Multiplying the conjugate characteristic polynomials yields

`Q=(z^k+1)²+NM(z^k+1)R-MR²`.

The independent resultant calculation gives the same expression. The polynomial is monic and integral, and all its roots are roots of unity under periodicity; its irreducible rational factors must therefore be cyclotomic. Multiplicities are permitted in Q.

### 7.2 Exhaustiveness and termination

The bound gives `N<=k-1`. There are finitely many palindromic nonnegative integer weight vectors of that bounded sum, and primitiveness is an exact finite check. For each nonempty vector, M lies in a bounded positive integer interval. Thus the arithmetic enumeration is finite for every fixed k.

The cyclotomic test by itself is not a nonlinear test. The manuscript correctly requires squarefreeness of the individual positive characteristic polynomial. A companion matrix has equal characteristic and minimal polynomials; root-of-unity eigenvalues therefore yield finite matrix order precisely when this polynomial is squarefree. It would be wrong to demand squarefreeness of Q: the classical order-three example has a repeated `(z+1)` in Q while each fixed-point spectrum is simple. The independent control checks this distinction.

A field embedding exchanging tau and tau' extends to the algebraic closure and preserves the multiplicative order of each root of unity. Hence the two spectra have the same set of root orders. The least common multiple of the cyclotomic orders in Q is the exact order of the positive companion derivative once its spectrum is simple.

If the rational map is globally finite order, the accepted averaging-linearization argument makes its order equal to the derivative's order. Thus the explicit final rational-function identity `F^p=id` is necessary. Conversely, passing that identity test proves global periodicity because all positive iterates are defined. No converse is inferred from the spectrum alone.

Exact factorization, quadratic-field arithmetic, finite composition, and rational-function equality testing terminate. The independent bound `phi(n)<=2k` and `phi(n)>=sqrt(n/2)` gives `n<=8k²` for relevant cyclotomic orders. These statements establish mathematical decidability per fixed order, not an efficient implementation or a completed enumeration of all orders.

The subclass includes recurrences with all reduced coefficients rational: primitive rational variable coefficients have rational common scale b, so `a0/b²` is rational. It also includes arbitrary positive rescalings of those coefficient patterns. The conclusion is not a finite-list theorem for all arbitrary-real even-order coefficient ratios.

## 8. Failure controls and the remaining gap

For the order-eight weights `m1=m7=1`, `m4=2`, with A=M=1, the stated gap, parity, and algebraic-unit checks pass. The negative fixed-point parameter is `d=2+sqrt(5)`. Its actual companion matrix has second-power trace `9+4sqrt(5)>8`. This independently verifies the contradiction with eight unit-modulus eigenvalues. The example is a nonperiodic control, not a new periodic solution.

For the order-sixteen pattern `R=z+z⁴+z¹²+z¹⁵`, the gap bound is B=4. The distinct values `2+2cos(2pi/n)`, n at least three, are totally positive algebraic integers whose conjugates all lie strictly between zero and four. This correctly shows a limitation of the named necessary tests. It does not claim that all other conditions or nonlinear periodicity are satisfied.

The manuscript does not invoke a quiver/T-system theorem without verifying its hypotheses. It expressly retains the unresolved larger supports, unrestricted irrational even-order ratios, and uniform odd-factor elimination problem. Its summary of previously accepted orders 6, 13, and 15 and sparse-support classification agrees with the prior audit scope.

## 9. Acceptance boundaries

Accepted without correction:

- The all-L mixed-lag exclusion for arbitrary real active coefficients and both constant statuses, including index dilations.
- Total positivity of the normalized constant unit.
- All conjugate gap bounds, central-third classification, and the finite large-gap parameter list under their rational-variable-ratio hypotheses.
- The integer reciprocal-constant and cyclotomic norm conditions when `A=a0/b²` is rational.
- The exact finite per-order procedure for the stated rationally scaled subclass, including its final nonlinear identity test.
- The supplied consistency and failure controls, with independent exact reconstructions.

Not established:

- Full arbitrary-order classification or construction of a new example outside the five known equivalence classes.
- Sufficiency of the arithmetic bounds, total positivity, cyclotomic norm, or finite-order derivative alone.
- A completed all-order execution of the finite procedures.
- Novelty, priority, or absence of related later literature.

No correction patch is needed for the accepted frozen bytes.
