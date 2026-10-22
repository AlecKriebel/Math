# Independent mathematical audit: Fuchs's weighted integer-polynomial infimum

**Problem:** Hayman–Lingham 4.25, identifier 2304025 / AMR-022-4025  
**Audit date:** 3 October 2026  
**Verdict:** PASS for the explicitly scoped partial results. No mathematical correction is required. The all-parameter problem is not solved by this work. No novelty or priority is established.

The six reviewed author files are identified by SHA-256 in `AUDIT_MANIFEST.json`. They were read as frozen inputs and remained unchanged. This audit is an independent mathematical review, not a formal proof certificate or a literature-wide open-status determination.

## 1. Exact target and source review

The primary target was checked in the rendered page of W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory*, arXiv:1809.07200v2, printed p.79, Problem 4.25 and its update. It asks for

\[
\inf_{P\in\mathbb Z[z]\text{ monic}}
\int_{-\pi}^{\pi}|1-e^{i\theta}|^{2\lambda}
 |P(e^{i\theta})|^2\,d\theta,
\qquad \lambda>0,
\]

with unrestricted degree. The Fuchs attribution, integer coefficient condition, leading coefficient one, exponent, and parameter range agree with the packet. Consequently the original answer is **\(2\pi F(\lambda)\)**, not \(F(\lambda)\). A possible convention excluding constant polynomials has no effect: multiplication by \(z\) preserves monicity, integrality, and energy.

The relevant classical proof was also read in the rendered author preprint of Peter Borwein and Colin Ingalls, *The Prouhet–Tarry–Escott problem revisited*, Section 2, printed preprint pp.3–4. Proposition 1 gives the power-sum, product-polynomial, and zero-multiplicity equivalences. Proposition 2 gives the minimum-size obstruction. The proofs and adjacent translation and binomial-multiplication lemmas support precisely the classical dependency used here. The packet reproduces the needed reasoning, so its mathematics does not depend on an unavailable or garbled extraction.

Sources:

- [Hayman–Lingham, arXiv version and primary text](https://arxiv.org/abs/1809.07200v2)
- [Borwein–Ingalls, author-hosted preprint](https://www.cecm.sfu.ca/~pborwein/PAPERS/P98.pdf)
- [Borwein–Ingalls, publication DOI](https://doi.org/10.5169/seals-61102)

The 2018 update reports no progress known to its compilers. That historical statement is not evidence of the literature's complete status in 2026. This audit does not independently certify the uninspected 1977 full text or exhaust later literature. Those limitations do not affect the exact target, the reproduced proofs, or the explicitly limited verdict.

## 2. Normalization and the analytic baseline

Let \(E_\lambda\) denote the integral divided by \(2\pi\). The beta integral gives

\[
C(\alpha)=\frac{4^\alpha\Gamma(\alpha+1/2)}
 {\sqrt\pi\Gamma(\alpha+1)}
=\frac{\Gamma(2\alpha+1)}{\Gamma(\alpha+1)^2}.
\]

The normalization is correct, including \(C(0)=1\), \(C(1)=2\), and \(C(1/2)=4/\pi\).

The Hardy lower bound \(E_\lambda(P)\ge1\) is valid. After removal of an initial monomial factor, the constant term is a nonzero integer. The branch of \((1-z)^\lambda\) taking value one at zero is analytic in the disc and continuous on its closure for \(\lambda>0\), including its zero at \(z=1\). Multiplication by the polynomial preserves these properties. Parseval, or radial Parseval followed by dominated convergence, bounds the squared boundary norm below by the square of its constant coefficient. There is no unjustified use of a branch analytic across the boundary point \(1\).

## 3. Fourier kernel, convergence, and discrete energy

### 3.1 Recurrence

Writing

\[
J_k=\int_0^\pi\sin^{2\alpha}t\cos(2kt)\,dt
\]

and differentiating \(\sin^{2\alpha+1}t\cos((2k+1)t)\) gives

\[
0=(\alpha-k)J_k+(\alpha+k+1)J_{k+1}.
\]

The boundary terms vanish; the derivative is integrable at both endpoints for every \(\alpha>0\). Since \(c_k=4^\alpha J_k/\pi\), the claimed recurrence

\[
c_{k+1}=\frac{k-\alpha}{k+\alpha+1}c_k
\]

follows. It remains valid at integer parameters, including the zero coefficient where the sequence terminates. No division by a vanishing Fourier coefficient is needed.

### 3.2 The infinite sum is legitimate

For \(0<\alpha<1\), \(c_1=-\alpha C/(\alpha+1)<0\), and all subsequent recurrence multipliers lie strictly between zero and one. Thus \(b_k=-c_k>0\) decreases strictly. The product formula and \(\log(1-x)\le-x\) yield

\[
b_k=O(k^{-2\alpha-1}),
\]

so \(\sum b_k\) converges. The absolutely convergent Fourier series represents the continuous weight: its coefficients are those of the weight, and uniqueness of Fourier coefficients identifies the functions. At \(\theta=0\) this gives \(C=2\sum_{k\ge1}b_k\). This is a valid evaluation at the zero of the weight, not a conditional summation.

A useful independent algebraic check is the exact identity

\[
C+2\sum_{k=1}^{D}c_k
=-\frac{D+\alpha+1}{\alpha}c_{D+1},
\qquad D\ge0.
\]

It follows by telescoping the recurrence. Its right-hand side tends to zero by the established decay. In particular, this independently recovers the total sum and provides an exact tail expression. At \(\alpha=1\) only \(b_1=1\) remains, so the endpoint has no infinite-series issue.

### 3.3 The difference identity has the right factor

For a finitely supported real sequence, extended by zero in both directions,

\[
\sum_j(a_{j+k}-a_j)^2
=2\sum_j a_j^2-2\sum_j a_ja_{j+k}.
\]

Multiplication by \(b_k\), summation, and \(2\sum b_k=C\) give exactly the Fourier quadratic form for \(E_\alpha\). All manipulations are absolutely convergent: beyond the support diameter the inner difference norm equals \(2\sum a_j^2\). There is neither a missing factor two nor an illegal exchange of conditionally convergent series.

## 4. Exact initial ranges and nonattainment

### 4.1 The integer-chain lower bound

For each step \(k\), a nonzero residue-class chain begins and ends at zero. Its nonzero integer differences sum to zero. It therefore has at least two nonzero differences, giving squared norm at least two. This applies separately for every \(k\); no single chain is required to work simultaneously for all steps. The energy identity proves \(E_\alpha\ge C(\alpha)\).

For \(0<\alpha<1\), any coefficient sequence other than a signed monomial has squared coefficient norm greater than one. Every step larger than the support diameter then contributes strictly more than two, with strictly positive weight. Equality is therefore confined to signed monomials. Under monicity, these are precisely the positive monomials. At \(\alpha=1\), the loss of positive tail weights correctly permits further minimizers.

Thus the claimed \(F(\lambda)=C(\lambda)\) for \(0<\lambda\le1\) is proved analytically, independently of finite tests.

### 4.2 Sign separation after one difference

For \(Q=(1-z)P\), the coefficient sum is zero and \(Q\ne0\), so both its positive and negative parts \(A,B\) are nonzero. Their supports are disjoint. The cross term is

\[
-2\sum_{i,j}a_i b_jc_{i-j}.
\]

Every involved index difference is nonzero, and every corresponding Fourier coefficient is nonpositive for \(0<\alpha\le1\). The sign of the inequality is therefore correct:

\[
E_\alpha(A-B)\ge E_\alpha(A)+E_\alpha(B)
\ge2C(\alpha).
\]

For \(0<\alpha<1\), every such coefficient is strictly negative, and at least one pair exists. Consequently the first inequality is strict for every individual polynomial. There can be no minimizer in \(1<\lambda<2\).

The monic geometric sums satisfy

\[
E_{1+\alpha}(S_N)=2(C(\alpha)-c_N(\alpha)).
\]

The coefficient decay gives the matching limit; strict decrease follows from the strict decrease of \(b_N\). The strict lower bound for each polynomial and the approaching sequence are compatible and prove a nonattained infimum, rather than a minimum. The endpoints are separately correct: \(E_1(S_N)=2\) for all \(N\ge1\), and \(E_2(S_N)=4\) for all \(N\ge2\).

Therefore \(F(\lambda)=2C(\lambda-1)\) on \([1,2]\), with exactly the claimed interior nonattainment.

## 5. Integer parameters and the exact arithmetic equivalence

The map \(P\mapsto(z-1)^mP\) is a bijection between monic integer polynomials and monic integer polynomials divisible by \((z-1)^m\). Monic division stays in \(\mathbb Z[z]\). Parseval gives \(E_m(P)=\sum q_j^2\).

The energy set is a nonempty subset of the positive integers, hence has a least member realized by a polynomial. Parity follows from \(q_j^2\equiv q_j\pmod2\) and \(\sum q_j=0\). There is no compactness or bounded-degree assumption hidden in attainment.

To check the lower bound, place each exponent in the positive or negative multiset with multiplicity equal to its coefficient magnitude. Both multisets have cardinality \(T\). Vanishing to order at least \(m\) implies equal power sums for exponents \(0,\ldots,m-1\), by the Euler operator \(z\,d/dz\). If \(T<m\), their first \(T\) power sums agree, so Newton's identities identify every elementary symmetric function and hence both root multisets. Their disjoint supports and nonemptiness prohibit that. Therefore \(T\ge m\), and

\[
\sum q_j^2\ge\sum|q_j|=2T\ge2m.
\]

Equality in both inequalities forces \(T=m\) and \(q_j\in\{0,\pm1\}\). This yields two disjoint distinct-element sets of size \(m\) with equal power sums through degree \(m-1\).

Conversely, any such sets define a signed polynomial with those vanishing power sums. The conversion from Euler derivatives to ordinary derivatives is triangular with nonzero diagonal; hence it has a zero of order at least \(m\). Translating all exponents preserves the moment equations by the binomial theorem and makes them nonnegative. Negating if necessary makes the leading coefficient one; monic division produces an admissible \(P\). Its energy is \(2m\). This verifies both directions, including the leading-coefficient and negative-exponent issues.

The distinct-term qualification is essential. For example, the multisets \(\{0,3,3\}\) and \(\{1,1,4\}\) have equal sums of powers through degree two. Their coefficient polynomial is \(1-2z+2z^3-z^4\), whose squared coefficient norm is ten, not six. An unrestricted ideal multiset solution is therefore insufficient to establish \(F(3)=6\). The packet does not make that error.

### Independently expanded witnesses

Expanding the displayed binomial products by subset enumeration gives the following positive and negative exponent sets. Changing the whole polynomial's sign, where needed, preserves energy and makes it monic.

| \(m\) | Positive exponents | Negative exponents | Squared norm |
|---:|---|---|---:|
| 1 | 0 | 1 | 2 |
| 2 | 0, 3 | 1, 2 | 4 |
| 3 | 0, 4, 5 | 1, 2, 6 | 6 |
| 4 | 0, 4, 7, 11 | 1, 2, 9, 10 | 8 |
| 5 | 0, 4, 8, 16, 17 | 1, 2, 10, 14, 18 | 10 |
| 6 | 0, 5, 6, 16, 17, 22 | 1, 2, 10, 12, 20, 21 | 12 |

All six have exactly the stated multiplicity at one. Independent successive synthetic division reconstructs the monic quotient coefficients in the author's verification output. These are exact finite identities and, together with the universal lower bound, prove \(F(m)=2m\) for \(1\le m\le6\).

The general upper bound \(F(m)\le2^m\) also holds: binary-spaced binomial factors have distinct subset sums, so all \(2^m\) resulting coefficients are \(\pm1\). This bound and the equality equivalence do not settle every integer case.

## 6. Higher fractional bounds

The rearrangement and level-set proof is valid:

1. For an indicator support \(i_1<\cdots<i_s\), each separation satisfies \(i_t-i_r\ge t-r\). Since \(b_k\) decreases, replacing the support by an interval can only decrease its energy.
2. For integer heights \(u,v\ge0\), the squared difference dominates the number of levels at which their indicators differ: \((u-v)^2\ge|u-v|\). Applying the positive difference kernel gives the required sum of level energies. All level sums are finite.
3. Adjacent intervals have nonpositive Fourier cross terms, so \(G_\alpha(s+t)\le G_\alpha(s)+G_\alpha(t)\). This direction is correct and combines the levels into the total mass.
4. The increment \(G_\alpha(s+1)-G_\alpha(s)=2\sum_{k>s}b_k\) is strictly positive. The Newton mass bound \(T\ge m\) can therefore be used in the direction claimed.

These steps prove \(F(m+\alpha)\ge2G_\alpha(m)\). The additional comparison

\[
|1-e^{i\theta}|^{2(m+\alpha)}
\ge4^{\alpha-1}|1-e^{i\theta}|^{2(m+1)}
\]

holds pointwise on the circle, including its zero, and proves the second stated lower bound. Taking infima preserves the inequality because the factor is positive and independent of the polynomial.

For \(m=2\), the four-term polynomial has the pairwise correlations

\[
4C-4c_N-4c_{N+1}+2c_{2N+1}+2c_1.
\]

The signs and multiplicities are correct. The long-distance correlations tend to zero, leaving \(4C+2c_1=2(\alpha+2)C/(\alpha+1)\). Since every \(S_NS_{N+1}\) is monic and integral, its limiting energy is an upper bound on the infimum; it need not be attained. The lower and upper bounds at \(\lambda=5/2\) are correctly \(32/(3\pi)\) and \(40/(3\pi)\).

The bounds do not coincide in the interior. The proof does not accidentally use a false extension of the negative-kernel sign argument to \(1<\alpha<2\): those weights have positive Fourier coefficients at distances at least two. The stated obstruction and remaining gap are genuine.

## 7. Computation, integrity, and limitations

Run `python3 audit/audit_verify.py` from the directory containing `packet` and `audit`, or invoke that script by its path from another directory.

- The frozen author verifier was executed from a temporary copy, avoiding mutation of its recorded output. All **8,850 author assertions passed**.
- Its generated `verification.json` was byte-for-byte identical to the frozen record.
- The independent verifier passed **117,753 mathematical assertions**, plus twelve before/after input-integrity checks and four replay checks.
- Its Fourier quotients are recomputed as finite products; half-integer cases are additionally checked against a separate closed rational formula.
- Difference energies include an exact tail formula rather than a truncated infinite sum.
- Signed coefficients of magnitude up to three, nonnegative coefficients up to four, eight integer multiplicities, independently expanded witnesses, and the repeated-term counterexample are covered.
- All six frozen author files match the expected hashes after execution.

These are reproducible diagnostic controls, not replacements for the analytic proofs above. A bounded coefficient box, a bounded degree search, and any finite collection of moment tests do not establish the original unrestricted infimum. The computational claims in the packet respect this boundary.

## 8. Release recommendation and residual scope

Accept the packet as a mathematically sound **partial result**. Keep the overall classification **unsolved / unresolved by this packet**, and retain the five-attempt record **5/5**. The five sections describe substantive mathematical approaches, including the higher-parameter attempt that ends in separated bounds. Do not advertise a full solution, a first resolution, or a determination of the current literature's status.

No blocking or nonblocking mathematical error was found in the claims audited. The remaining task is exactly the advertised one: determine the infimum at arbitrary parameters above two beyond the individual cases proved, including the unrestricted integer arithmetic minima. The equality reduction to distinct-term ideal Prouhet–Tarry–Escott solutions is an exact equivalence, not an existence theorem for all multiplicities.
