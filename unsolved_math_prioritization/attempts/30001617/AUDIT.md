# Independent audit: dyadic tail LIL counterexample

## Verdict

**ACCEPT: unrestricted assertion disproved, with prior-result attribution.**

The frozen candidate's mathematical construction is correct. It gives a
real \(L^2([0,1))\) terminal function with total realized square
function bounded by one and normalized tail limsup equal to infinity
almost everywhere on \([0,1)\). Its zero extension meets the original
real-line locally integrable-function hypothesis. The negative result
must be credited to Ghimire's 2011 presentation and 2012 dissertation;
this audit makes no novelty claim.

The candidate audited has 5,909 bytes and SHA-256
`1a17f8e8fed3b5c7311b8bc68197f22a6afbab4537659e0a91e61475e4650589`.
Its identity is bound by the frozen candidate record. The frozen
candidate and its frozen source inputs were not edited. `PROOF.md`
supplies a complete expanded argument, including an elementary
almost-sure convergence proof and a direct check that the conditional
positive theorem's comparison hypothesis fails.

This is an AI-assisted independent analytical audit, supplemented by exact
finite model checks and file-integrity checks. It is not external human peer
review or a formally machine-verified proof. No publication, branch operation, or queue edit
was performed by this audit.

## Detailed mathematical checks

1. **Original question and indexing: PASS.** The original report, printed
   p. 2872 (PDF p. 60), assumes only local integrability on the real line.
   Its sum over \(k\ge n\) of the difference between averages at levels
   \(k+1\) and \(k\) is exactly \(\sum_{j>n}d_j^2\). The absolute
   nested-log expression is precisely \(\log\log(1/Q_n)\) when
   \(0<Q_n<e^{-e}\). There is no missing constant or shifted tail.
2. **Parameter existence, including ceilings: PASS.** With
   \(t=\log(1/a^2)\), the product \(L_k(a)a^2\) is at most
   \(e^{-t}(2(k+2)\log2\,t^{64k^2\log2}+1)\), which tends to zero
   for each fixed \(k\). The prior amplitudes in the induction form
   a finite strictly positive minimum. No simultaneous uniform-in-\(k\)
   limit is assumed. The \(+1\) from the outer ceiling is harmless.
3. **Deterministic global and future budgets: PASS.** The induction gives
   \(\sum b_k\le1\) and
   \(B_k=\sum_{j>k}b_j\le a_k^2\sum_{j>k}2^{-j}=2^{-k}a_k^2\).
   These bounds apply to every path, including failed stages.
4. **Predictability and stopping: PASS.** The activation of a whole
   block depends only on completed prior blocks. Every sign in an
   active block is used. The negative signs of a failing block do not
   terminate that block early. This distinction is essential. Fresh
   signs have conditional mean zero given all earlier digits.
5. **Total square function and L2 terminal function: PASS.** An active
   block contributes exactly \(a_k^2\), so the entire realized square
   function is at most \(\sum b_k\). Orthogonality and Tonelli give
   \(\sum\mathbb E d_j^2\le1\); finite partial sums are Cauchy in
   \(L^2\). The maximal inequality in `PROOF.md` proves almost-sure
   convergence, and the conditional-expectation contraction proves
   \(f_n=\mathbb E(f\mid\mathcal F_n)\). Mere pointwise convergence
   would not suffice for this identification; here it is established.
6. **Independence and success event: PASS.** All potential blocks use
   disjoint digits, including the ones never activated. No actual
   success occurs exactly when none of the potential blocks is all
   positive. Thus the failure probability is \((1-2^{-m_k})^{L_k}\),
   bounded by \(2^{-(k+2)}\). The independent variables are the
   potential-block events; the stopped increments are not falsely
   called independent. The first Borel-Cantelli lemma suffices.
7. **Future terminal error: PASS.** \(M_k\) is deterministic.
   Orthogonality of finite tails, followed by the established L2
   limit, gives \(\mathbb E|f-f_{M_k}|^2\le B_k\). Chebyshev at
   threshold \(a_k\) yields \(2^{-k}\), again summable. There is no
   union over random block positions and no conditioning that could
   enlarge this estimate.
8. **Random subsequence: PASS.** The start of the successful block can
   depend on that block's future signs. It need not be a stopping time.
   The argument uses only pathwise equalities at this chosen index.
   Within the remainder of that stage the successful block is the
   only active block, so its sum is \(a_k\sqrt{m_k}\) and square is
   \(a_k^2\). All genuinely future stages are controlled by \(B_k\).
9. **Logarithmic monotonicity and constants: PASS.**
   \(g'(q)=\log\log(1/q)-1/\log(1/q)>0\) for \(q<e^{-e}\).
   The choice \(a_k<e^{-e}\) ensures
   \(2a_k^2<e^{-e}\) and \(\ell_k>1\). Hence the denominator at
   the selected index is at most \(\sqrt2a_k\sqrt{\ell_k}\), while
   the numerator is at least \(a_k(8k\sqrt{\ell_k}-1)\). The stated
   lower bound \((8k-1)/\sqrt2\) follows.
10. **All asymptotic quantifiers: PASS.** Intersect the full-measure sets
    for convergence, conditional-mean identities, eventual success,
    and eventual future-error bounds. Success then occurs at every
    sufficiently large stage on that one set. The selected indices
    increase because all stage lengths are finite and positive.
    In fact \(Q_n>0\) for every finite \(n\), since each later stage
    always has an active first block. Its limit is zero by summability.
11. **Extension to the real line: PASS.** An L2 function on a
    probability interval is L1. Zero extension is therefore globally
    integrable. The standard small dyadic intervals at points of
    \([0,1)\) remain inside \([0,1)\); their means are unchanged.
    Failure on a measure-one subset of this interval disproves the
    source's almost-everywhere real-line conclusion.

## Source review and exact scope

### Original problem

The statement was checked in the actual page image of the report,
not merely in the curated row. It imposes no independence condition,
no uniform comparison of tail square functions inside dyadic atoms,
and no regularity condition beyond local integrability.

### Prior counterexample and attribution update

Ghimire's 2011 presentation identifies the counterexample in PDF
pp. 51-69. Its title page dates the seminar to October 21-22, 2011.
The mechanism consists of many trials per stage, freezing successful
paths until the next stage, decreasing amplitudes, and controlling
the future tail. Its success estimate uses a central-limit argument.

The dissertation PDF was available after the frozen candidate. Its
title page confirms Santosh Ghimire, Kansas State University, 2012.
Section 3.3 occupies printed pp. 50-59 (PDF pp. 59-68). The final
page explicitly uses the square-tail normalization in the original
question. All ten pages were read as extracted text, and the critical
construction/parameter/future-tail/normalization pages were additionally
inspected as rendered images. Exact inspected page numbers are in
`SOURCE_PINS.json`.

The frozen candidate accurately said that only the dissertation record
had been inspected at its freeze. That historical statement remains
unchanged. This audit's source evidence now supersedes that limitation:
the full Section 3.3 has been inspected. The reconstruction uses a
different elementary success event and a stronger summable second-moment
budget, so it does not rely on the dissertation's particular parameter
choices or the constants in its exponential tail calculation.

### Conditional positive statements

With \(S'_n=\sqrt{Q_n}\), dissertation Theorem 29, printed p. 34,
assumes one finite \(C\) bounding \(|S'_n(x)/S'_n(y)|\) for all
points in each dyadic atom at every level. It states a limsup bound
\(2C\) after normalization by
\(\sqrt{2Q_n\log\log(1/Q_n)}\). The 2011 presentation, PDF p. 50,
has the same comparison condition. The presentation's displayed atom
index list starts at one; the dissertation supplies the conventional
complete list starting at zero. This indexing discrepancy is irrelevant
to the counterexample and is not silently used as a hypothesis.

Acharya-Ghimire (2016), Theorem 1, PDF p. 2, repeats the comparison
condition and the same normalization. Theorem 2 on that page states
a claim along selected times defined using a uniform tail bound over
a dyadic interval. It is not stated as an unrestricted all-index result.
No correctness claim for Theorem 2 or for its proof is needed here.

The reconstruction demonstrably lacks any such uniform comparison:
at a stage-start atom, first-block-success paths have square tail at
most \((1+2^{-k})a_k^2\), and no-success paths have square tail at
least \(L_ka_k^2\). Both occur on positive-measure subevents of every
atom, while \(L_k\to\infty\). Thus no hidden contradiction with the
conditional statement is left unresolved.

### Imports and limitations

The proof uses elementary conditional expectation, Tonelli's theorem,
completeness of L2, Chebyshev's inequality, and the first Borel-Cantelli
lemma. A needed maximal inequality is proved directly in `PROOF.md`.
It imports no specialized LIL, central-limit approximation, optional
sampling assertion, or theorem about infinite quadratic variation.

This audit accepts the stated counterexample and its match to the
source question on independent analytical review. It does not certify every theorem or numerical detail
of the cited literature, determine priority earlier than the inspected
2011 presentation, or conduct an exhaustive survey of later variants.

## Verification artifacts

`SOURCE_PINS.json` contains public bibliographic, retrieval, byte-count,
hash, and page-inspection metadata. `MANIFEST.json` pins this authored
report, the expanded proof, the acceptance record, and the source pins.
Local checks verify the frozen input identities and finite stopped-block
models exactly, including conditional-mean cancellation, success
probabilities, orthogonality, and the selected-block tail identities.
Finite models are sanity checks and do not replace the infinite analytic
proof. Source PDFs, extracted text, page screenshots, and private
coordination inputs are excluded from the publication manifest.
