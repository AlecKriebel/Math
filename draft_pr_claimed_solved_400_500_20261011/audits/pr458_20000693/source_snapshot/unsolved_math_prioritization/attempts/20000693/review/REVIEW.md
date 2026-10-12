# Independent review: AIM 5.3 / problem 20000693

**Disposition: ACCEPTED as a scoped, credited heuristic, with nonblocking source clarifications.**

**Not a proof of the general moment asymptotic. No new mathematical priority is established.**

Reviewed 2026-10-03 UTC. The frozen input manifest is
`49c26cff89e8c5fcd9fd917c586acaa0902d22f30e1c4c8874ed2d212c9ff110`.
The reviewed mathematical text is `HEURISTIC.md`, SHA-256
`e1173965c7cd160a6aeaa7d9be479c62b5f1f6d668ce8dea038f67f486d0b13d`.
The original packet was not edited.

## 1. Executive finding and scope of acceptance

The candidate gives a coherent leading-term model for

\[
\int_T^{2T}\prod_i |L(1/2+it,\chi_i)|^{2a_i}\,dt,
\]

with finitely many fixed Dirichlet characters, arbitrary fixed moduli, and fixed
real weights \(a_i\geq0\). It correctly groups weights by equality of the primitive
inducer, uses the actual imprimitive Euler factors in the arithmetic constant,
and gives the correct Barnes-G normalization. Its convergence argument for the
defined arithmetic constant is rigorous and does not establish the moment
prediction. The explicitly conjectural modeling steps remain conjectural.

This is responsive to the displayed Dirichlet-product example in the source's
open-ended request for a heuristic. It is not a universal result for every
imprimitive higher-degree L-function or every shifted degree-one factor. It
does not settle the associated asymptotic theorem, prove lower-order terms,
give growing-conductor uniformity, or establish negative-power moments.
The source does not impose any of those additional requirements.

No blocking mathematical defect was found. The recommendations in section 9
improve attribution or remove minor presentation ambiguity; they do not change
the candidate formula or this scoped acceptance.

## 2. Frozen-input and primary-source checks

- All ten files listed by the input manifest match their recorded sizes and
  SHA-256 values. All seven primary-source files listed by the source manifest
  also match. See `INPUT_INTEGRITY.json`.
- The AIM primary problem object was independently extracted from the embedded
  JSON in the hashed cached HTML. It equals the separately cached object.
  Its statement matches the imported dataset statement after whitespace
  normalization. It is AIM section 5, Problem 5.3, attributed to
  C. Turnage-Butterbaugh. See `SOURCE_CHECKS.json`.
- The source asks for a heuristic and leaves powers, integration bounds,
  conductor regime, smoothing, and error terms unspecified. Choosing the fixed
  t-aspect and nonnegative powers is an openly stated scope, not a source quote.
  Neighboring 5.1 specifically invokes Conrey--Keating; 5.3 does not require
  that particular mechanism.
- The cached Heap, Sahay, and Hagen plain-text extractions were regenerated
  directly from their hashed PDFs and match byte for byte.
- This was a local audit. Historical repository-duplicate and user-history
  searches in `SOURCE_GATE.md` were not rerun and are not certified afresh here.
  Mathematical acceptance does not depend on those operational searches.

Primary target: [AIM Problem 5.3](http://aimpl.org/zetamoments/5/).

## 3. Primitive aggregation and the exponent

Let \(\psi_i\) be the primitive inducer of \(\chi_i\). The correct effective
weights are

\[
M_\psi=\sum_{i:\psi_i=\psi}a_i,
\qquad E=\sum_\psi M_\psi^2.
\]

This is equality of primitive characters as arithmetic functions. It is not
equality of modulus labels, and it is not equality up to complex conjugation.
At any prime outside the union of the modulus supports, grouping the local
factors is an exact identity. The primitive zero factors are likewise identical
for characters induced from the same primitive character.

There is no collision between two distinct primitive characters after lifting
to a common modulus: equality of the induced character would contradict the
uniqueness of its primitive inducer. Their quotient character is consequently
nonprincipal. In particular, a genuinely nonreal character and its conjugate
remain distinct constituents; their quotient is its nonprincipal square.

The candidate correctly separates integer factor multiplicities from an outer
real moment parameter. If a product contains multiplicities \(e_i\) and its
absolute value is raised to \(2\kappa\), then the input weights are
\(a_i=\kappa e_i\), and the exponent is
\(\kappa^2\sum_\psi(\sum_{i:\psi_i=\psi}e_i)^2\).
This is not a claim that the integers \(e_i\) themselves range over all reals.

Principal characters with different moduli all have the conductor-one zeta
inducer. Repetitions must therefore combine even when their finite Euler
deletions differ. The packet gets these cases right.

## 4. Imprimitive factors and differing moduli

For the original modulus \(q_i\), the identity

\[
L(s,\chi_i)=L(s,\psi_i)\prod_{p\mid q_i}(1-\psi_i(p)p^{-s})
\]

is correct. Factors at primes dividing the primitive conductor equal one.
Writing \(Q=\operatorname{lcm}_i q_i\) and lifting to modulus \(Q\) gives

\[
L(s,\chi_i)=L(s,\widetilde\chi_i)
\prod_{\substack{p\mid Q\\p\nmid q_i}}(1-\psi_i(p)p^{-s})^{-1}.
\]

The inverse sign is essential and is correct in the candidate. These factors
are not a finite Dirichlet polynomial. On the critical line their denominators
do not vanish, since \(|\psi_i(p)p^{-s}|\le p^{-1/2}<1\).

At a deleted prime, the actual local coefficient series retains exactly those
characters whose original moduli do not delete that prime. Their phases must
be averaged together. Separate local expectations would lose correlations.
For example, factors with local values \(1,-1\) and both weights one have
local mean \((1-x^2)^{-1}\), whereas multiplying the two separate means gives
\((1-x)^{-2}\). At \(x=1/3\), these are respectively \(9/8\) and \(9/4\).

The ratio \(\mathcal A/\mathcal A^*=\prod_{p\mid Q}J_p/J_p^*\) follows
exactly from the definitions of the constants, because their good-prime
factors and exponent \(E\) agree. It is finite and positive. The packet
explicitly and correctly avoids deducing an actual moment asymptotic from
this identity or from upper/lower bounds on the finite deletion product.

## 5. Local analysis, convergence, and positivity

For nonnegative weights, the analytic branch at zero of
\(\prod_i(1-\chi_i(p)z)^{-a_i}\) is well defined in the unit disc.
If \(A=\sum_i a_i>0\), the absolute values of its coefficients are bounded
by \((A)_r/r!\). This gives convergence on \(|z|=p^{-1/2}\), permits Parseval,
and proves

\[
J_p=\sum_{r\geq0}|b_p(r)|^2p^{-r}
=\frac1{2\pi}\int_0^{2\pi}\prod_i
|1-\chi_i(p)e^{i\theta}/\sqrt p|^{-2a_i}\,d\theta>0.
\]

The first coefficient gives
\(J_p=1+|\sum_i a_i\chi_i(p)|^2/p+O_{\mathbf a}(p^{-2})\).
The remainder bound is uniform in the character values, which have modulus
at most one; it is not a hidden assumption about the moduli growing with \(T\).

At good primes,

\[
\left|\sum_\psi M_\psi\psi(p)\right|^2
=E+2\sum_{\psi<\phi}M_\psi M_\phi\Re(\psi(p)\overline{\phi(p)}).
\]

Consequently the proposed \(H_p\), obtained by multiplying
\((1-p^{-1})^EJ_p\) by
\(\prod_{\psi<\phi}|1-\psi(p)\overline{\phi(p)}/p|^{2M_\psi M_\phi}\),
has no term of order \(p^{-1}\). Thus \(H_p=1+O_{\mathbf a}(p^{-2})\).
Every local factor is strictly positive, so the absolutely convergent product
of the \(H_p\) is positive rather than merely nonnegative.

Every off-diagonal quotient character is nonprincipal. Its Euler product at
one converges in increasing prime order, for example by the prime number
theorem in fixed arithmetic progressions, and its value is nonzero. Removing
finitely many primes preserves those properties. This establishes the
candidate's regularized formula for \(\mathcal A\) and its finiteness and
strict positivity.

The conjugate pairing and absolute values in that formula are important.
Arbitrary fractional powers of complex \(L(1,\rho)\) without a log convention
would be ambiguous. The candidate avoids that issue: its cross factors are
positive quantities \(|L^S(1,\rho)|^{2M_\psi M_\phi}\). The unregularized
Euler product is not incorrectly declared absolutely convergent.

This proof concerns only a well-defined proposed constant. It does not prove
independence of L-functions, prime/zero splitting, or a high-moment asymptotic.

## 6. Random-matrix normalization, conductor scale, and domain

The finite CUE identity and its leading Barnes-G factor are correctly written:

\[
\mathbb E_{U(N)}|\det(I-U)|^{2m}
=\prod_{j=1}^N\frac{\Gamma(j)\Gamma(j+2m)}{\Gamma(j+m)^2}
\sim\frac{G(1+m)^2}{G(1+2m)}N^{m^2}.
\]

The asserted domain \(m\geq0\) lies safely within the integrable range.
There is one such factor per positive-weight primitive class. The resulting
cutoff powers in the prime and zero models cancel as
\((e^\gamma\log X)^E\), with no missing Gamma, factorial, or Barnes-G factor.
The zero model, its independence across distinct primitive classes, the
weighted prime/zero splitting, and the joint growing-cutoff approximation
remain hypotheses. Finite-prime equidistribution is not used to justify an
uncontrolled interchange of limits.

For fixed conductors, replacing \(\log T\) by \(\log(f_\psi T)\), or by
\(\log(f_\psi T/(2\pi))\), changes the normalized expression by a factor
tending to one. This does not identify lower-order coefficients, and no
separate conductor-power prefactor is missing. Allowing conductors to grow
would invalidate that equivalence; the packet excludes that regime.

Zero-weight factors are omitted, resolving \(0^0\) at zeros. Adding or removing
zero-weight rows leaves the original local factors and exponent unchanged,
even though an auxiliary choice of \(Q\) or \(S\) might change. The all-zero
case gives exactly the interval length \(T\). Nonnegative powers introduce
no singularities at critical-line zeros. Negative powers can do so, and the
packet correctly declines to transfer Heap's printed negative outer range
without accounting for effective multiplicities and zero orders.

Extending the CUE model to independently chosen real weights is explicitly a
heuristic extrapolation. It is not analytic continuation of a proved
integer-moment identity for L-functions. The compactly supported smoothing
claim is likewise labeled a leading model prediction, not a theorem.

## 7. Known constants and adversarial checks

The following checks were independently reconstructed:

1. One weight-one character gives \(\mathcal G=1\) and
   \(\mathcal A=\phi(q)/q\), agreeing with the mean-square leading coefficient.
2. A weight-two character has good-prime mean
   \((1+x)/(1-x)^3\). Combining \(\mathcal G=1/12\) with the Euler product
   gives \((2\pi^2)^{-1}\prod_{p\mid q}(1-p^{-1})^3/(1+p^{-1})\).
3. For two unit-modulus local values with quotient \(u\), weights one, the
   exact local mean is
   \[(1-x^2)/[(1-x)^2(1-ux)(1-\bar u x)].\]
   For distinct primitive constituents this leaves \(1-x^2\) after cross
   regularization. At primes deleting one or both characters, the resulting
   factors agree with the two-character leading coefficient in
   Topacogullari's Theorem 1.3 (cached PDF pp. 3--4).
4. A nonreal character and its conjugate have exponent two, not four. The
   quotient is checked as a nonprincipal character in the quartic example.
5. For \(\zeta(s)L(s,\chi_0\bmod2)\), the primitive weight is two. Its
   changed local ratio is exactly \(1/6\), giving the proposed coefficient
   \(1/(12\pi^2)\). The deleted prime is not silently ignored.
6. Fractional weights, different moduli sharing an inducer, multiple ramified
   primes, principal factors, empty input, and all-zero input were included
   in the separate test suite.

### Reproducible test evidence

- The author script was copied unchanged to the review directory and replayed.
  It reports **966 checks passed**, and its JSON output is byte-for-byte equal
  to the frozen author result. It did not overwrite the frozen packet.
- `reviewer_checks.py` reports **380 independent cases passed**. It uses a
  logarithmic-derivative recurrence for coefficients instead of the author's
  binomial convolution. It separately checks 72 lift cases, 72 aggregation
  cases, 72 zero-omission cases, 52 regularization cases, 36 finite
  distinct-character witnesses, and 14 exact normalization cases.
- Its 18 high-precision Parseval checks compare the recurrence series against
  direct phase quadrature. The maximum observed absolute difference is
  approximately \(1.14\times10^{-64}\).
- Its 20 fractional-weight CUE checks construct Toeplitz determinants from
  numerically integrated Fourier coefficients and compare them to the Gamma
  product. The maximum relative difference is approximately
  \(2.14\times10^{-65}\). A further 24 exact integer cases verify the
  weight-one and weight-two CUE formulas.
- The suites use different case-count conventions; their totals should not
  be represented as a single uniformly counted theorem certificate.

Finite checks reinforce the algebra and normalizations; they do not replace
the general arguments above and do not test or prove actual L-function
high-moment asymptotics.

## 8. Literature credit and novelty boundary

The principal model is prior mathematics. The audit confirms the packet's
credit to Keating--Snaith, Heap, and Sahay. In particular:

- [Heap, arXiv:1303.6119](https://arxiv.org/abs/1303.6119), cached v1,
  Introduction (18)--(24) and Conjecture 4, pp. 5--6, distinguishes integer
  constituent multiplicities from the outer real moment parameter. Section 7,
  (176)--(188), gives the constituent-wise recipe and the corresponding
  exponent. Its general Selberg-class setting also has additional constituent
  and convolution assumptions; it is not an arbitrary-product theorem.
- [Sahay, arXiv:2103.13542](https://arxiv.org/abs/2103.13542), cached v3,
  definitions p. 4, Theorem 1.3 pp. 5--6, Conjectures 1.4/1.6 and conditional
  Theorem 1.7 pp. 7--8, gives the common-modulus integer-weight model.
  Its displayed constant agrees with the candidate. The author explicitly
  explains that Theorem 1.7 is conjectural because of its hypotheses.
- [Topacogullari, arXiv:1909.11517](https://arxiv.org/abs/1909.11517),
  Theorems 1.1 and 1.3, supplies rigorous low-moment normalization checks,
  including distinct primitive characters of differing moduli. It does not
  establish all weighted product moments.
- [Hagen, arXiv:2609.11619](https://arxiv.org/abs/2609.11619), cached preprint
  dated 10 September 2026, Theorems 1--2, gives bounds for distinct fixed
  degree-one/selected degree-two constituents with positive real powers.
  These support the predicted logarithmic exponent in their scope, not the
  claimed asymptotic constant. The packet does not upgrade them to one.

The Keating--Snaith PDF is referenced but absent from the frozen source cache.
This review therefore does not independently certify its cited equation
numbers or publisher metadata. The finite CUE formula itself was independently
checked and its use is corroborated by the cached Heap/Sahay sources.

The differing-modulus and independently real-weight formulation is properly
described as a synthesis/adaptation. It should not be presented as a new
discovery of the moment model or of the multiplicity principle.

## 9. Nonblocking clarifications recommended

1. **Name the intermediate GRH assumption in the cited zero-model derivation.**
   Sahay section 4, p. 17, explicitly assumes GRH to put primitive zeros at
   \(1/2+i\gamma\) before making the unitary replacement. In section 5 of the
   packet, add a short sentence acknowledging this conventional intermediate
   assumption. The existing unitary-replacement hypothesis already carries
   the model's unproved spectral premise, so this omission does not create a
   claimed unconditional theorem. Do not describe GRH alone as sufficient, or
   add it as an extra formal hypothesis to Sahay's stated Theorem 1.7, whose
   stated conditions are Conjectures 1.4 and 1.6.
2. **Credit prior differing-modulus discussion more precisely.** Sahay at the
   end of p. 33/start of p. 34 notes that Topacogullari's work can verify
   analogous two-factor constants for possibly distinct moduli. Mentioning
   that observation would sharpen the source gate's account. The existing
   claim that Sahay's general displayed theorem uses a common modulus is
   correct, and the packet makes no novelty claim.
3. **Make the cross-character modulus explicit.** Take
   \(\rho_{\psi,\phi}\) modulo \(\operatorname{lcm}(f_\psi,f_\phi)\), or
   induce it to the fixed \(Q\). Either gives exactly the factors used outside
   \(S\). Avoid reading “a common multiple” as introducing additional prime
   divisors outside \(Q\), which would require further finite-factor bookkeeping.
   The explicit product definition already has the intended meaning.

These are recommendations, not prerequisites for the scoped heuristic-level
acceptance. No correction to (H), the exponent, the arithmetic constant,
the Barnes-G factor, or the stated nonnegative domain is required.

## 10. Completion and authorization disposition

The source's displayed fixed-Dirichlet heuristic request has a complete,
audited response within the stated nonnegative-power scope. Any status update
must preserve the labels **heuristic**, **credited synthesis**, and
**general asymptotic unproved**. A categorical claim that the high-moment
problem has been rigorously solved would not be supported by this review.

This review used local reads, local generated files, and local test execution
only. No remote branch, tree, commit, pull request, repository search, or
publication action was attempted. The recorded cancellation/denial of remote
writes remains in force. Review acceptance supplies no new permission to
publish or retry those actions.

Reproduction:

```
python author_verify.py
python reviewer_checks.py
```

Run those commands from this review directory. The first writes a local
`verification.json`; the retained original replay is
`AUTHOR_REPLAY_REPORT.json`. The second writes `REVIEWER_CHECKS.json`.
The frozen input remains separate. `REVIEW_MANIFEST.json` hashes the review
deliverables and records the final input recheck.
