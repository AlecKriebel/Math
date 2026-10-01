# Independent review: Gaussian singular-value source audit

## Verdict

**PASS for the conservative source-status audit; retain the real-proof hold.** The current external preprints state results covering both directions of the original square-matrix question with exactly the required normalization. The withdrawn 2016 claim is correctly rejected as a proof certificate. This review checks the short complex argument against its published recurrence input, but does **not** certify the complete real-case proof or its supporting non-asymptotic bound. The campaign should receive no new solved-result credit.

- Target: **2800102 / AMR-027-0102**, Bandeira's Open Problem 1.2.
- Frozen artifact: `SOURCE_AUDIT.md`.
- SHA-256: `99ae40a387e00e5d2c46ed8db4e479170092b2484cf237f83629ba5e1201ec8e`.
- Date: 2026-09-30 UTC.
- Separate reviewer: `gpt-6-astra`, reasoning effort `xhigh`.
- Required source-text changes: **none**.

The verdict validates the package's explicit source hold. It is not a full independent verification of every external theorem, a novelty claim, or a claim that the new preprints have been peer reviewed.

## 1. Original scope and normalization

The [2013 author post](https://afonsobandeira.wordpress.com/2013/11/01/a-conjecture-on-the-singular-values-of-a-gaussian-matrix/) and the [MIT Open Problem 1.2 handout](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-of-data-science-fall-2015/a9963e8f7bd9c10b4d48df8115f63116_MIT18_S096F15_Open1.2.pdf) were checked. They concern every positive integer square size, real increase and complex decrease. The original inequalities are non-strict; the recent claims are stronger.

For a standard square Gaussian matrix $X$ with $\mathbb E|X_{ij}|^2=1$, setting $G=X/\sqrt d$ gives

$$d^{-1}\mathbb E\|G\|_*=d^{-3/2}\mathbb E\operatorname{Tr}(XX^*)^{1/2}.$$

The blog explicitly specifies variance $1/2$ for each real component of a standard complex entry. The real ensemble uses ordinary real variance one before scaling. Thus the normalization in the audit is correct; there is no extra $\sqrt2$ factor and no confusion between a normalized average and an unnormalized nuclear norm. The square source is shape zero. The rectangular and noninteger-shape extensions are unnecessary to cover it.

## 2. Withdrawal and current versions

The official [arXiv record for 1606.00494](https://arxiv.org/abs/1606.00494) names **Luís Daniel Abreu** and marks version 3, dated **6 March 2023**, withdrawn. The stated defect is an incorrect estimate in Lemma 1 arising from a hypergeometric substitution; it invalidates the claimed monotonicity result. The notice separately preserves a recurrence with a sign correction. The package correctly distinguishes those facts and does not reuse the invalid estimate.

Current records were checked as of the review date:

- [Hutník, 2608.12147v2](https://arxiv.org/abs/2608.12147v2): submitted 12 August 2026, revised 11 September 2026, expanded title and proof. Its square moment result includes $s=1/2$, hence the complex target.
- [Hutník, 2608.12151v2](https://arxiv.org/abs/2608.12151v2): the same submission/revision dates, with a revised real-case proof. Theorem 1.1 on printed p. 2 states the square increment exceeds $1/(160N^2)$ for every $N\ge1$.
- [Baslingker–Dan, 2608.27532v1](https://arxiv.org/abs/2608.27532v1): submitted 27 August 2026. Theorem 1.1 on p. 2 states strict complex decrease for all sizes and nonnegative shapes, including zero.
- [Abreu–Patil, 2609.07802v1](https://arxiv.org/abs/2609.07802v1): submitted 7 September 2026. Its Theorem 1 on printed p. 3 gives the complex decrement bounds used by the revised real paper. The PDF's own front-matter date is 9 September; the audit's 7 September refers to the arXiv submission date.

No withdrawal marker or journal-reference field was present for these four current preprints. That observation is not evidence of external peer review. The new Abreu–Patil work is a separate paper and must not be conflated with the withdrawn 2016 result.

## 3. Short complex proof: mathematical audit

The full three-page [Baslingker–Dan paper](https://arxiv.org/pdf/2608.27532) was read. Its input recurrence was checked in the **final published** [Cunden–Mezzadri–O'Connell–Simm paper](https://maths.ucd.ie/~noconnell/pubs/cmos19.pdf), printed pp. 1107–1108, Theorem 4.4, formula (4.11), and the remark following (4.16). The fractional-moment domain includes $k=1/2$ at square shape zero. The moment is finite there.

For the square case, writing $q_n=\mathbb E\operatorname{Tr}(XX^*)^{1/2}$, the recurrence becomes

$$q_{n+1}=\left(2+\frac{3}{4n^2}\right)q_n-q_{n-1}.$$

Normalizing $c_n=q_n/n^{3/2}$ and $d_n=c_{n+1}-c_n$ gives

$$d_n=(A_n-B_n-1)c_n+B_nd_{n-1},$$

where $A_n=(2+3/(4n^2))(n/(n+1))^{3/2}$ and $B_n=((n-1)/(n+1))^{3/2}$. Both signs in this propagation are correct.

The scalar estimate needed is

$$(1+x)^{3/2}+(1-x)^{3/2}\ge2+\tfrac34x^2\qquad(0\le x\le1).$$

A direct check is to subtract the right side. The difference and its first derivative vanish at zero, and its second derivative is nonnegative by convexity of $t\mapsto t^{-1/2}$. Continuity handles the endpoint. In the argument $x=1/n$, so this is exactly the necessary domain. The paper's wider printed phrase about nonnegative $x$ should not be read past $x=1$ as a real-variable assertion; this harmless domain overstatement is already avoided in the reviewed audit.

The initial values are $q_1=\sqrt\pi/2$ and $q_2=11\sqrt\pi/8$. They give $c_2<c_1$ because $121<128$. Positivity of $c_n$ and the displayed propagation prove all subsequent strict decreases. This verifies the logical complex-square argument with its established moment recurrence as an imported theorem. The review does not reprove the entire 2019 random-matrix moment theorem or certify all broader rectangular extensions.

## 4. Real theorem: coverage and explicit validation limit

The [current real paper](https://arxiv.org/pdf/2608.12151) defines the LOE density with exponential factor $e^{-x/2}$ and shape exponent $(\lambda-1)/2$. At integral shape it identifies this with the spectrum of $XX^T$ for real variance-one entries. Its statistic is $N^{-3/2}\mathbb E\sum\sqrt{x_i}$. The theorem at $\lambda=0$ therefore matches the original real target exactly, not merely up to scaling or a change of matrix aspect ratio.

The square comparison uses the real–complex correction identity, its positive diagonal completion, coefficient estimates, Proposition 3.4 on pp. 17–18, and the low-size checks in Appendix A.1. Equation (3.1) imports the upper bound

$$0<\Gamma_{N,0}<\frac{H_N+6\log2-10/3}{8\pi[N(N+1)]^{3/2}}.$$

That expression, its decrement orientation, and its normalization agree with Abreu–Patil's Theorem 1. The final algebra converting the correction reserve into the claimed $1/(160N^2)$ increment is consistent. In particular the squared coefficient-ratio comparison reduces, for $N=t+3$, to the positive polynomial $4t^3+32t^2+71t+37$.

**What remains unaudited:** a complete independent proof of the LOE correction identity and its scaling; all convergence, interchange, and positivity steps in the Abel-completed diagonal series; and the full proof of the supporting Abreu–Patil all-dimensional decrement estimate. These are genuine mathematical dependencies. Reading theorem statements and matching formulas does not certify them. No counterexample or specific fatal gap in those new papers was found by this bounded audit either.

Accordingly, the real theorem is an external resolution claim whose scope matches the source, while independent full-proof validation remains on hold. The author's package states precisely this distinction.

## 5. Exact reproduction and disposition

The submitted checker was copied to this review directory and replayed without changing the author's files. All **383 exact assertions passed**. A separate checker using the terminating hypergeometric moment formula, without importing submitted code, passed **53 exact assertions**. It confirms the initial moments, square recurrence, normalized inequalities in finite sizes, and the elementary polynomial estimates noted above.

Run from this review directory:

```sh
python3 submitted_verify.py
python3 independent_checks.py
```

Both use only the Python standard library. The receipts are `verification.json` and `independent_results.json`. These computations validate arithmetic consistency; they are not an all-dimensional proof by finite testing and do not certify the real analytic argument.

**Final recommendation:** publish the source audit only with its explicit real-proof hold and attribution to the external authors. Preserve the historical withdrawal correction. Retain the campaign's conservative unresolved/source-hold classification and award no new solved-result credit. The frozen audit is appropriate for that purpose without mandatory changes.
