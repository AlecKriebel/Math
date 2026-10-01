# Gaussian singular-value monotonicity: source correction and validation limits

**Disposition: external resolution preprints located; source hold.**
This package is a literature and normalization audit, not a new solution.
The real-case proof has not been completely independently certified in this
attempt. Retain `unsolved` in the campaign queue, with a source-hold note;
do not give this campaign a solved-result credit. No human peer review of
the recent preprints is asserted.

Target: **2800102 / AMR-027-0102**, Bandeira's Open Problem 1.2.
Checked: **2026-09-30**. The original imported report is preserved unchanged
in `prior_report.json`, including its later withdrawal correction.

## 1. Exact problem and normalization

The full [2013 author post](https://afonsobandeira.wordpress.com/2013/11/01/a-conjecture-on-the-singular-values-of-a-gaussian-matrix/)
and the [MIT Open Problem 1.2 handout](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-of-data-science-fall-2015/a9963e8f7bd9c10b4d48df8115f63116_MIT18_S096F15_Open1.2.pdf)
state two directions, both for every positive integer dimension: the real
expected average singular value increases, and the complex one decreases.
The blog explicitly gives variance 1/2 for each real component of a
standard complex Gaussian. The package's square target is not a statement
about unnormalized nuclear norms or a fixed number of columns.

Write X for a square matrix with independent standard Gaussian entries,
real or complex with `E|X_jk|² = 1`, and put G = X/sqrt(d). Then

\[
 \alpha_{\mathbb K}(d)
 =\frac1d\mathbb E\|G\|_*
 =d^{-3/2}\mathbb E\|X\|_*
 =d^{-3/2}\mathbb E\operatorname{Tr}(XX^*)^{1/2}.
\]

This elementary identity is the normalization bridge to all the sources
below. In the real case the adjoint means transpose. The zero shape
parameter is the square case; positive shape describes an excess of
columns and is unnecessary for the original target. Noninteger shape
extensions do not create a Gaussian matrix model with a noninteger size.

## 2. The old claimed solution was withdrawn

The imported report initially misattributes
[arXiv:1606.00494](https://arxiv.org/abs/1606.00494) to three other authors.
The actual author is **Luís Daniel Abreu**. Version 3, dated **6 March 2023**,
is explicitly withdrawn. The author says the estimate in Lemma 1 is wrong
and invalidates the result; the stated error concerns a hypergeometric
substitution. A recurrence survives, with a sign correction. The old
monotonicity claim therefore cannot serve as a proof certificate.

The historical report's final verification note correctly flags that
withdrawal and must not be lost merely because newer proofs have appeared.
Its malformed integral and ancillary numerical bounds are not reused.

## 3. Current external results and versions

### Real square direction

[Ondrej Hutník, arXiv:2608.12151v2](https://arxiv.org/abs/2608.12151v2),
*Dimension Monotonicity in Laguerre Ensembles II: Average Singular Values
and the Rectangularity Transition in the Orthogonal Case*, **11 September
2026**, is the current version located. The first version was posted
12 August 2026 under a square-case title. The current page has no withdrawal
marker and no journal publication reference.

Section 1.1 uses ordinary real N(0,1) entries at integer shape. At shape
zero its statistic is exactly the normalization above. **Theorem 1.1,
printed p. 2**, states for every N >= 1 the strict increment bound

\[
 \alpha_{\mathbb R}(N+1)-\alpha_{\mathbb R}(N)>
 \frac{1}{160N^2}.
\]

The square route is Proposition 2.2, the diagonal completion in Theorem
2.5, coefficient comparisons, Proposition 3.4 on pp. 17–18, and Appendix
A.1. It compares a real–complex correction with a complex decrement bound.
The bound is stronger than the original requested monotonicity. This is
an external preprint's theorem, not this campaign's independently
established theorem.

### Complex square direction

[Jnaneshwar Baslingker and Biltu Dan, arXiv:2608.27532v1](https://arxiv.org/abs/2608.27532v1),
*On the monotonicity of average singular values of complex Gaussian random
matrices*, **27 August 2026**, gives an alternate proof and attributes the
preceding complex result to Hutník. **Theorem 1.1, printed p. 2**, states
strict decrease for every positive integer dimension and every real
nonnegative shape. Shape zero is exactly the original complex target.
The full three-page paper was read. Its proof uses a moment recurrence,
a scalar convexity inequality at x=1/n in [0,1], and an explicit negative
initial increment. The current page has no withdrawal marker or journal
reference. The brief proof is considerably easier to audit than the
full orthogonal comparison, but finite checks below are not a substitute
for a theorem-level audit of its cited recurrence.

[Hutník, arXiv:2608.12147v2](https://arxiv.org/abs/2608.12147v2),
*Dimension Monotonicity in Laguerre Ensembles I: Fractional Moments and
Shape Transitions in the Unitary Case*, **11 September 2026**, is a
substantially expanded current version of the 12 August complex paper.
Its Section 1.2 and subsequent results include the strict decrease of
`N^(-s-1) E Tr(W^s)` at square shape and `s=1/2`. It explicitly credits the
alternate half-moment proof above. Neither version was marked withdrawn
on the current source page.

[Luís Daniel Abreu and Pratik Patil, arXiv:2609.07802v1](https://arxiv.org/abs/2609.07802v1),
*Non-asymptotic bounds for the average singular value of a complex
Gaussian matrix*, **7 September 2026**, gives positive upper and lower
decrement bounds in **Theorem 1, printed p. 3**. The real paper's equation
(3.1) matches its upper bound, including the normalization and denominator.
This paper is a separate 2026 work and must not be confused with the
withdrawn 2016 claim. Its complete asymptotic and non-asymptotic proof was
not fully independently audited here.

## 4. What was checked, and what remains uncertified

The normalization bridge, square-shape identification, quantifiers,
version dates, current withdrawal notices, attributions and theorem
locations were checked directly. The full Baslingker–Dan argument was
read. The real paper's square dependency chain was read through Sections
2 and 3.1–3.3 and Appendix A.1; its rectangularity-transition sections are
outside the original problem. The Abreu–Patil theorem and recurrence
were checked at their stated locations.

The real-source hold is specific: this package does **not** claim a
complete independent derivation of the LOE density identity and its
rescaling, all analytic interchanges in the Abel-completed diagonal
series, or the supporting Abreu–Patil decrement bound. Those are
mathematical dependencies, not merely bibliographic formalities. No
identified counterexample to the new preprints is asserted either.

`verify.py` directly integrates finite Laguerre polynomial expansions
using rational coefficients after removing sqrt(pi). It checks the
square complex moment recurrence and strict normalized decrease in small
dimensions, independently of numerical quadrature or random sampling.
It also checks elementary rational polynomial inequalities used in the
real square estimate. Its exact arithmetic is useful for catching
normalization and sign mistakes; it cannot certify the real proof or
all-dimensional monotonicity by finite testing.

## 5. Prior attempts and campaign handling

The initial queue row was rank 42, `queued`, 0/5. Repository path, all-state
PR, branch and subject searches found no earlier research attempt for this
ID. A repeated all-state PR query at 04:36 UTC was empty. The related-target
groups did not contain this ID. The imported literature report is prior
source triage, preserved here rather than overwritten.

No fresh proof attempt was made: **0 of 5 substantive proof attempts**.
The source audit materially changes the search decision. Given current
external all-parameter claims, new proof search would risk reproducing an
existing result. The appropriate next step is external-proof validation,
not counting a discovery. The source record remains on hold in this
campaign until that validation standard is met.
